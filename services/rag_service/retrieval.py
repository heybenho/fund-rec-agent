from pipeline.index_funds import FUNDS_INDEX_NAME

SEARCH_PIPELINE_NAME = "funds-hybrid-pipeline"
CAPACITY_DECAY_SCALE_FACTOR = 0.75      # Applies gaussian decay on capacity_min, giving flexibility

def embed_query(model, text):
    return model.encode(text).tolist()

def build_filters(unit_filter, purpose_filter):
    filters = []
    if unit_filter:
        filters.append({"term": {"unit_ancestors": unit_filter}})
    if purpose_filter:
        filters.append({"term": {"purpose_ancestors": purpose_filter}})
    return filters

def build_hybrid_query(interest_text, interest_embedding, capacity, unit_filter=None, purpose_filter=None, k=10):
    filters = build_filters(unit_filter, purpose_filter)
    decay_scale = max(capacity * CAPACITY_DECAY_SCALE_FACTOR, 5000)

    keyword_branch = {
        "function_score": {
            "query": {
                "bool": {
                    "must": [{"match": {"fund_terms": interest_text}}],
                    "filter": filters,
                }
            },
            "functions": [
                {
                    "gauss": {
                        "capacity_min": {
                            "origin": capacity,
                            "scale": decay_scale,
                            "decay": 0.5,
                        }
                    }
                }
            ],
            "score_mode": "multiply",
            "boost_mode": "multiply"
        }
    }

    knn_params = {
        "vector": interest_embedding,
        "k": k,
    }
    if filters:
        knn_params["filter"] = {"bool": {"filter": filters}}

    knn_branch = {"knn": {"fund_terms_embedding": knn_params}}


    return {
        "size": k,
        "query": {
            "hybrid": {
                "queries": [keyword_branch, knn_branch]
            }
        }
    }

def search_funds(client, model, interest_text, capacity, unit_filter=None, purpose_filter=None):
    embedding = embed_query(model, interest_text)
    query_body = build_hybrid_query(interest_text, embedding, capacity, unit_filter, purpose_filter)

    return client.search(
        index=FUNDS_INDEX_NAME,
        body=query_body,
        params={"search_pipeline": SEARCH_PIPELINE_NAME}
    )