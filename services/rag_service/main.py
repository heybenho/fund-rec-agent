from contextlib import asynccontextmanager

import ollama
from fastapi import FastAPI
from pydantic import BaseModel

from pipeline.index_funds import get_opensearch_client, load_model
from services.rag_service.retrieval import search_funds

OLLAMA_MODEL = "llama3.2:1b"
TOP_N = 5

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.client = get_opensearch_client()
    app.state.model = load_model()
    yield

app = FastAPI(lifespan=lifespan)


class DonorProfile(BaseModel):
    interest: str
    capacity: float
    unit: str | None = None
    purpose: str | None = None

class FundRecommendation(BaseModel):
    fund_name: str
    unit_name: str
    subpurpose_name: str
    capacity_min: int
    score: float
    rationale: str

def generate_rationale(fund, interest_text):
    prompt = (
        f"A donor is interested in: {interest_text}\n\n"
        f"Recommended fund: {fund['fund_name']}\n"
        f"Unit: {fund['unit_name']}\n"
        f"Subpurpose: {fund['subpurpose_name']}\n"
        f"Minimum gift: ${fund['capacity_min']:,}\n"
        f"Fund description: {fund['fund_terms']}\n\n"
        "Write 1-2 sentences explaining why this fund matches the donor's interest."
        "Only reference facts given above. Do not invest additional details."
    )

    result = ollama.generate(model=OLLAMA_MODEL, prompt=prompt)
    return result["response"].strip()

@app.post("/recommend", response_model=list[FundRecommendation])
def recommend(profile: DonorProfile):
    response = search_funds(
        app.state.client,
        app.state.model,
        profile.interest,
        profile.capacity,
        profile.unit,
        profile.purpose,
    )

    hits = response["hits"]["hits"][:TOP_N]

    recommendations = []
    for hit in hits:
        fund = hit["_source"]
        rationale = generate_rationale(fund, profile.interest)
        recommendations.append(FundRecommendation(
            fund_name=fund["fund_name"],
            unit_name=fund["unit_name"],
            subpurpose_name=fund["subpurpose_name"],
            capacity_min=fund["capacity_min"],
            score=hit["_score"],
            rationale=rationale
        ))

    return recommendations