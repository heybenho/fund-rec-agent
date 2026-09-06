import pytest
from fastapi.testclient import TestClient

from services.rag_service.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client

def test_recommend_returns_valid_response_shape(client):
    payload = {"interest": "graduate engineering research", "capacity": 500000}
    response = client.post("/recommend", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    for item in data:
        assert isinstance(item["fund_name"], str)
        assert isinstance(item["unit_name"], str)
        assert isinstance(item["subpurpose_name"], str)
        assert isinstance(item["capacity_min"], int)
        assert isinstance(item["score"], float)
        assert isinstance(item["rationale"], str)
        assert len(item["rationale"]) > 0

def test_recommend_missing_required_field_returns_422(client):
    response = client.post("/recommend", json={"capacity": 10000})
    assert response.status_code == 422