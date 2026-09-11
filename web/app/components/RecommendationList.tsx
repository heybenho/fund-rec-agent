import {FundRecommendation} from "../types";

interface RecommendationListProps {
    recommendations: FundRecommendation[];
}

export default function RecommendationList({recommendations}: RecommendationListProps) {
    if (recommendations.length === 0) {
        return null;
    }

    return (
        <div>
            <h2 className="mb-3 text-lg font-semibold text-neutral-900">Recommended funds</h2>
            <ul className="flex flex-col gap-4">
                {recommendations.map((rec, index) => (
                    <li
                        key={index}
                        className="flex flex-col gap-2 rounded-xl border border-neutral-200 bg-white p-4 shadow-sm"
                    >
                        <h3 className="font-semibold text-neutral-900">{rec.fund_name}</h3>
                        <p className="text-sm text-neutral-600">
                            {rec.unit_name} &middot; {rec.subpurpose_name}
                        </p>
                        <p className="text-sm text-neutral-700">{rec.fund_terms}</p>
                        <div className="mt-1 flex items-center justify-between text-sm">
                            <span className="rounded-full bg-neutral-100 px-2 py-1 text-neutral-700">
                                Min gift: ${rec.capacity_min.toLocaleString()}
                            </span>
                            <span className="text-neutral-400">Score: {rec.score.toFixed(2)}</span>
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
}