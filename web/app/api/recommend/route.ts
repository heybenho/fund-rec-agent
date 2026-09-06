import {NextRequest, NextResponse} from "next/server";
import {DonorProfile, FundRecommendation} from "../../types";

const RAG_SERVICE_URL = "http://localhost:8000/recommend";

export async function POST(request: NextRequest) {
    const profile: DonorProfile = await request.json();

    const response = await fetch(RAG_SERVICE_URL, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(profile),
    });

    if (!response.ok) {
        return NextResponse.json(
            {error: "Failed to fetch recommendations"},
            {status: response.status}
        );
    }

    const recommendations: FundRecommendation[] = await response.json();
    return NextResponse.json(recommendations);
}