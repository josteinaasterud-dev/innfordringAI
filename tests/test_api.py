import httpx
import pytest
from fastapi.testclient import TestClient

from app import main
from tests.test_creditsafe import REPORT_RESPONSE, SEARCH_RESPONSE


@pytest.fixture
def client(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/authenticate"):
            return httpx.Response(200, json={"token": "tok"})
        if request.url.path.endswith("/companies"):
            return httpx.Response(200, json=SEARCH_RESPONSE)
        return httpx.Response(200, json=REPORT_RESPONSE)

    cs = main.creditsafe
    monkeypatch.setattr(cs, "username", "user")
    monkeypatch.setattr(cs, "password", "pass")
    monkeypatch.setattr(cs, "base_url", "https://example.test/v1")
    monkeypatch.setattr(cs, "_client", httpx.AsyncClient(transport=httpx.MockTransport(handler)))
    monkeypatch.setattr(cs, "_owns_client", False)
    monkeypatch.setattr(cs, "_token", None)
    monkeypatch.setattr(cs, "_token_expires_at", 0.0)
    with TestClient(main.app) as test_client:
        yield test_client


def test_search_endpoint(client):
    response = client.get("/creditsafe/companies", params={"name": "Testselskapet"})
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["companies"][0]["connect_id"] == "NO-0-123456789"


def test_report_endpoint(client):
    response = client.get("/creditsafe/companies/NO-0-123456789")
    assert response.status_code == 200
    body = response.json()
    assert body["summary"]["company_name"] == "Testselskapet AS"
    assert "report" not in body


def test_report_endpoint_full(client):
    response = client.get("/creditsafe/companies/NO-0-123456789", params={"full": True})
    assert response.json()["report"] == REPORT_RESPONSE


def test_assessment_endpoint(client, monkeypatch):
    captured = {}

    def fake_ask(system_prompt, user_prompt, max_tokens=500):
        captured["user_prompt"] = user_prompt
        return "Anbefaler inkassovarsel."

    monkeypatch.setattr(main, "ask_openai", fake_ask)

    response = client.post(
        "/creditsafe/assessment", json={"query": "123456789", "amount": 45000}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["assessment"] == "Anbefaler inkassovarsel."
    assert body["summary"]["org_number"] == "123456789"
    assert "45000.0 NOK" in captured["user_prompt"]
    assert "Testselskapet AS" in captured["user_prompt"]


def test_assessment_without_hits_returns_404(client, monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/authenticate"):
            return httpx.Response(200, json={"token": "tok"})
        return httpx.Response(200, json={"totalSize": 0, "companies": []})

    monkeypatch.setattr(
        main.creditsafe, "_client", httpx.AsyncClient(transport=httpx.MockTransport(handler))
    )
    response = client.post("/creditsafe/assessment", json={"query": "Ukjent AS"})
    assert response.status_code == 404
