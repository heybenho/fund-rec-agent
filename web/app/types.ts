export interface ChatMessage {
    role: "user" | "assistant";
    content: string;
}

export interface FundRecommendation {
    fund_name: string;
    unit_name: string;
    subpurpose_name: string;
    capacity_min: number;
    score: number;
    fund_terms: string;
}

export interface ChatResponse {
    reply: string;
    recommendations: FundRecommendation[];
}