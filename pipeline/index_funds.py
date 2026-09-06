import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from sentence_transformers import SentenceTransformer
from opensearchpy import OpenSearch
from opensearchpy.helpers import bulk

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

FUNDS_INDEX_NAME = "funds"

FUNDS_INDEX_BODY = {
    "settings": {
        "index.knn": True
    },
    "mappings": {
        "properties": {
            "fund_id": {"type": "integer"},
            "fund_name": {"type": "text"},
            "fund_terms": {"type": "text"},
            "unit_id": {"type": "integer"},
            "unit_name": {"type": "keyword"},
            "unit_type": {"type": "keyword"},
            "unit_ancestors": {"type": "keyword"},
            "subpurpose_id": {"type": "integer"},
            "subpurpose_name": {"type": "keyword"},
            "purpose_ancestors": {"type": "keyword"},
            "capacity_min": {"type": "long"},
            "fund_terms_embedding": {
                "type": "knn_vector",
                "dimension": 384,
                "method": {
                    "name": "hnsw",
                    "engine": "lucene",
                    "space_type": "cosinesimil"
                }
            }
        }
    }
}


# Embedding pipeline
load_dotenv()
def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        dbname=os.getenv("POSTGRES_DB"),
    )

def fetch_funds(conn):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT
                f.id, f.fund_name, f.fund_terms, f.capacity_min,
                u.id AS unit_id, u.name AS unit_name, u.unit_type, u.path AS unit_path,
                s.id AS subpurpose_id, s.name AS subpurpose_name, s.path AS purpose_path
            FROM funds f
            JOIN units u ON u.id = f.unit_id
            JOIN subpurposes s ON s.id = f.subpurpose_id
        """)
        return cur.fetchall()

def build_ancestors(path):
    parts = path.split(".")
    return [".".join(parts[:i+1]) for i in range(len(parts))]

def load_model():
    return SentenceTransformer(EMBEDDING_MODEL)

def embed_funds(model, funds):
    texts = [fund["fund_terms"] for fund in funds]
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=32)

    return [
        {"fund_id": fund["id"], "embedding": embedding} for fund, embedding in zip(funds, embeddings)
    ]


# OpenSearch index mapping

def get_opensearch_client():
    return OpenSearch(
        hosts=[{"host": "localhost", "port": 9200}],
        use_ssl=False,
    )

def create_funds_index(client):
    if client.indices.exists(index=FUNDS_INDEX_NAME):
        client.indices.delete(index=FUNDS_INDEX_NAME)
    client.indices.create(index=FUNDS_INDEX_NAME, body=FUNDS_INDEX_BODY)

def build_documents(funds, embedded_funds):
    documents = []
    for fund, embedded in zip(funds, embedded_funds):
        documents.append({
            "fund_id": fund["id"],
            "fund_name": fund["fund_name"],
            "fund_terms": fund["fund_terms"],
            "unit_id": fund["unit_id"],
            "unit_name": fund["unit_name"],
            "unit_type": fund["unit_type"],
            "unit_ancestors": build_ancestors(fund["unit_path"]),
            "subpurpose_id": fund["subpurpose_id"],
            "subpurpose_name": fund["subpurpose_name"],
            "purpose_ancestors": build_ancestors(fund["purpose_path"]),
            "capacity_min": int(fund["capacity_min"]),
            "fund_terms_embedding": embedded["embedding"].tolist(),
        })

    return documents

def bulk_index(client, documents):
    actions = [
        {"_index": FUNDS_INDEX_NAME, "_id": doc["fund_id"], "_source": doc}
        for doc in documents
    ]
    success_count, errors = bulk(client, actions)
    print(f"Indexed {success_count} documents.")
    if errors:
        print(f"Errors: {errors}")

def main():
    conn = get_connection()
    funds = fetch_funds(conn)
    conn.close()
    print(f"Fetched {len(funds)} funds from Postgres.")

    model = load_model()
    embedded_funds = embed_funds(model, funds)
    print(f"Generated {len(embedded_funds)} embeddings.")

    client = get_opensearch_client()
    create_funds_index(client)

    documents = build_documents(funds, embedded_funds)
    bulk_index(client, documents)

if __name__ == "__main__":
    main()