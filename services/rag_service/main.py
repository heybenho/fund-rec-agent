import json
from contextlib import asynccontextmanager

import ollama
from fastapi import FastAPI
from pydantic import BaseModel

from pipeline.index_funds import get_opensearch_client, load_model
from services.rag_service.retrieval import search_funds, format_hits_for_llm, SEARCH_FUNDS_TOOL

OLLAMA_MODEL = "llama3.1:8b"
MAX_TOOL_ITERATIONS = 5

SYSTEM_PROMPT = (
    "You are a donor advising assistant for a university's gift fund program. "
    "Use the search_funds tool once you know the donor's intreest and roughly how "
    "much they want to give. If either is missing, ask a short clarifying question "
    "instead of calling the tool. When you answer, only reference facts returned "
    "by the tool - do not invent fund details. "
    "When presenting search results, keep the response short. Only justify the "
    "top fund. Do not describe every fund returned."
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.client = get_opensearch_client()
    app.state.model = load_model()
    yield

app = FastAPI(lifespan=lifespan)

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[ChatMessage]

class FundRecommendation(BaseModel):
    fund_name: str
    unit_name: str
    subpurpose_name: str
    capacity_min: int
    score: float

class ChatResponse(BaseModel):
    reply: str
    recommendations: list[FundRecommendation]

def run_search_funds_tool(app, arguments):
    interest = arguments.get("interest")
    if not isinstance(interest, str) or not interest.strip():
        return {"error": "Interest is required and must be a non-empty description of what the donor wants to support. Ask the donor for what they want to support."}

    try:
        capacity = float(arguments["capacity"])
        if capacity <= 0:
            raise ValueError
    except (TypeError, ValueError):
        return {"error": f"The donor's interest ('{interest}') was understood correctly — do not ask about interest again. The only missing piece is the gift capacity (a dollar amount). Ask the donor for that."}


    response = search_funds(
        app.state.client,
        app.state.model,
        interest,
        capacity,
        arguments.get("unit"),
        arguments.get("purpose"),
    )

    return format_hits_for_llm(response)

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += [m.model_dump() for m in request.messages]

    last_hits = []
    for _ in range(MAX_TOOL_ITERATIONS):
        result = ollama.chat(model=OLLAMA_MODEL, messages=messages, tools=[SEARCH_FUNDS_TOOL], options={"temperature": 0.2})
        message = result["message"]
        tool_calls = message.get("tool_calls")

        if not tool_calls:
            return ChatResponse(reply=message["content"], recommendations=last_hits)
        
        messages.append(message)
        for tool_call in tool_calls:
            hits = run_search_funds_tool(app, tool_call["function"]["arguments"])
            if isinstance(hits, list):
                last_hits = hits
                model_hits = hits[:1]
            else:
                model_hits = hits
            messages.append({"role": "tool", "content": json.dumps(model_hits)})

    return ChatResponse(reply="I wasn't able to find a match. Please try rephrasing.", recommendations=last_hits)