from pipeline.index_funds import get_opensearch_client, load_model, FUNDS_INDEX_NAME
import argparse
from services.rag_service.retrieval import embed_query, build_filters, build_hybrid_query, search_funds

SEARCH_PIPELINE_NAME = "funds-hybrid-pipeline"
CAPACITY_DECAY_SCALE_FACTOR = 0.75


def create_search_pipeline(client):
    pipeline_body = {
        "description": "Normalize and combine BM25 and kNN scores for hybrid search",
        "phase_results_processors": [
            {
                "normalization-processor": {
                    "normalization": {"technique": "min_max"},
                    "combination": {
                        "technique": "arithmetic_mean",
                        "parameters": {"weights": [0.4, 0.6]}
                    }
                }
            }
        ]
    }

    client.transport.perform_request(
        "PUT", f"/_search/pipeline/{SEARCH_PIPELINE_NAME}", body=pipeline_body
    )

# CLI Wrapper

def print_results(response):
    hits = response["hits"]["hits"]
    if not hits:
        print("No matching funds found.")
        return

    for hit in hits:
        source = hit["_source"]
        print(f"[{hit["_score"]:.4f}] {source["fund_name"]}")
        print(f" Unit: {source["unit_name"]} | Subpurpose: {source["subpurpose_name"]} | Capacity min: ${source["capacity_min"]:,}")
        print(f" {source["fund_terms"]}")
        print()

def main():
    parser = argparse.ArgumentParser(description="Search for matching gift funds.")
    parser.add_argument("--interest", required=True, help="Donor's stated interests, e.g. 'support of graduate students in Engineering'")
    parser.add_argument("--capacity", required=True, type=float, help="Donor's giving capacity in dollars")
    parser.add_argument("--unit", help="Optional unit ancestor path filter, e.g. 'chancellor.engineering'")
    parser.add_argument("--purpose", help="Optional purpose ancestor path filter, e.g. grad_support")
    args = parser.parse_args()

    client = get_opensearch_client()
    model = load_model()

    response = search_funds(client, model, args.interest, args.capacity, args.unit, args.purpose)
    print_results(response)

if __name__ == "__main__":
    main()