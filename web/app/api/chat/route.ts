import {NextRequest, NextResponse} from "next/server";
import {ChatMessage, ChatResponse} from "../../types";

const RAG_SERVICE_URL = "http://localhost:8000/chat";

export async function POST(request: NextRequest) {
    const {messages}: {messages: ChatMessage[]} = await request.json();

    let response: Response;
    try {
        response = await fetch(RAG_SERVICE_URL, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({messages})
        });
    } catch {
        return NextResponse.json(
            {error: "Could not reach the RAG service. Is it running on port 8000?"},
            {status: 502}
        );
    }

    if (!response.ok) {
        return NextResponse.json(
            {error: "Failed to fetch chat response"},
            {status: response.status}
        );
    }

    const data: ChatResponse = await response.json();
    return NextResponse.json(data);
}