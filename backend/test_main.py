from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_invalid_url_rejected():
    response = client.post("/analyze", json={"url": "https://google.com"})
    assert response.status_code == 400

def test_valid_url_executes():
    # Will likely trigger fallback in CI/CD environment without API keys, which is expected behavior
    response = client.post("/analyze", json={"url": "https://www.amazon.com/Best-Sellers/zgbs"})
    assert response.status_code == 200
    assert "total_estimated_revenue" in response.json()