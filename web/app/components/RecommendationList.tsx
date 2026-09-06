import {FundRecommendation} from "../types";

interface RecommendationListProps {
    recommendations: FundRecommendation[];
}

export default function RecommendationList({recommendations}: RecommendationListProps) {
    if (recommendations.length === 0) {
        return null;
    }

    return (
        <ul>
            {recommendations.map((rec, index) => (
                <li key = {index}>
                    <h2>{rec.fund_name}</h2>
                    <p>
                        <strong>Unit:</strong> {rec.unit_name} | {" "}
                        <strong>Subpurpose:</strong> {rec.subpurpose_name} | {" "}
                        <strong>Minimum gift:</strong> ${rec.capacity_min.toLocaleString()}
                    </p>
                    <p>{rec.rationale}</p>
                    <p><em>Match score: {rec.score.toFixed(4)}</em></p>
                </li>
            ))}
        </ul>
    );
}