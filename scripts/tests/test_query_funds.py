import pytest

from pipeline.index_funds import get_opensearch_client, load_model
from scripts.query_funds import search_funds

@pytest.fixture(scope="module")
def client():
    return get_opensearch_client()

@pytest.fixture(scope="module")
def model():
    return load_model()

def test_hard_unit_filter_restricts_all_results(client, model):
    response = search_funds(
        client,
        model,
        interest_text = "student support and career development",
        capacity=500000,
        unit_filter="chancellor.business",
    )
    hits = response["hits"]["hits"]
    assert len(hits) > 0
    for hit in hits:
        assert "chancellor.busness" in hit["_source"]["unit_ancestors"]

def test_chemistry_scholarship_persona_top_result_aligned(client, model):
    response = search_funds(
        client,
        model,
        interest_text = "undergraduate scholarship in chemistry",
        capacity=100000,
    )
    hits = response["hits"]["hits"]
    assert len(hits) > 0
    assert "chancellor.chemistry" in hits[0]["_source"]["unit_ancestors"]

def test_engineering_research_persona_top_result_algined(client, model):
    response = search_funds(
        client,
        model,
        interest_text = "graduate student research in engineering research and innovation",
        capacity=10000000,
    )
    hits = response["hits"]["hits"]
    assert len(hits) > 0
    assert "chancellor.engineering" in hits[0]["_source"]["unit_ancestors"]