export interface DonorProfile {
    interest: string;
    capacity: number;
    unit?: string;
    purpose?: string;
}

export interface FundRecommendation {
    fund_name: string;
    unit_name: string;
    subpurpose_name: string;
    capacity_min: number;
    score: number;
    rationale: string;
}

