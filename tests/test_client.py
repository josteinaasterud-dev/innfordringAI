import httpx
import pytest
import respx

from banqsoft_mcp.auth import TokenProvider
from banqsoft_mcp.client import LighthouseClient, LighthouseError, NotFoundError, _as_rows
from banqsoft_mcp.config import Settings

TOKEN_URL = "https://login.microsoftonline.com/tenant-1/oauth2/v2.0/token"
BASE = "https://ecm-se-sandbox.casesapi.lighthouse-cm.com"


def make_settings(**overrides) -> Settings:
    values = dict(
        tenant_id="tenant-1",
        client_id="client-1",
        client_secret="secret-1",
        api_scope="api://lighthouse/.default",
        namespace="ecm-se",
        environment="sandbox",
    )
    values.update(overrides)
    return Settings(**values)


def mock_token():
    respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json={"access_token": "abc", "expires_in": 3600})
    )


@pytest.mark.asyncio
@respx.mock
async def test_get_case_sends_bearer_token():
    mock_token()
    route = respx.get(f"{BASE}/api/v1/cases/1473").mock(
        return_value=httpx.Response(200, json={"caseNumber": "1473"})
    )
    async with httpx.AsyncClient() as http:
        settings = make_settings()
        client = LighthouseClient(settings, http, TokenProvider(settings, http))
        assert await client.get_case("1473") == {"caseNumber": "1473"}
    assert route.calls[0].request.headers["Authorization"] == "Bearer abc"


@pytest.mark.asyncio
@respx.mock
async def test_missing_case_raises_not_found():
    mock_token()
    respx.get(f"{BASE}/api/v1/cases/9999").mock(return_value=httpx.Response(404))
    async with httpx.AsyncClient() as http:
        settings = make_settings()
        client = LighthouseClient(settings, http, TokenProvider(settings, http))
        with pytest.raises(NotFoundError):
            await client.get_case("9999")


@pytest.mark.asyncio
@respx.mock
async def test_retries_once_after_401_with_fresh_token():
    respx.post(TOKEN_URL).mock(
        side_effect=[
            httpx.Response(200, json={"access_token": "stale", "expires_in": 3600}),
            httpx.Response(200, json={"access_token": "fresh", "expires_in": 3600}),
        ]
    )
    route = respx.get(f"{BASE}/api/v1/cases/1473").mock(
        side_effect=[
            httpx.Response(401),
            httpx.Response(200, json={"caseNumber": "1473"}),
        ]
    )
    async with httpx.AsyncClient() as http:
        settings = make_settings()
        client = LighthouseClient(settings, http, TokenProvider(settings, http))
        assert await client.get_case("1473") == {"caseNumber": "1473"}
    assert route.call_count == 2
    assert route.calls[1].request.headers["Authorization"] == "Bearer fresh"


@pytest.mark.asyncio
@respx.mock
async def test_server_error_raises():
    mock_token()
    respx.get(f"{BASE}/api/v1/cases/1473").mock(return_value=httpx.Response(500, text="boom"))
    async with httpx.AsyncClient() as http:
        settings = make_settings()
        client = LighthouseClient(settings, http, TokenProvider(settings, http))
        with pytest.raises(LighthouseError):
            await client.get_case("1473")


@pytest.mark.asyncio
@respx.mock
async def test_search_passes_creditor_and_limit_and_truncates():
    mock_token()
    rows = [{"caseNumber": str(n)} for n in range(10)]
    route = respx.get(f"{BASE}/api/v1/cases").mock(
        return_value=httpx.Response(200, json={"items": rows})
    )
    async with httpx.AsyncClient() as http:
        settings = make_settings()
        client = LighthouseClient(settings, http, TokenProvider(settings, http))
        result = await client.search_cases(creditor_org_no="912345678", status="Open", limit=3)
    assert len(result) == 3
    query = route.calls[0].request.url.params
    assert query["creditorOrgNo"] == "912345678"
    assert query["status"] == "Open"


def test_as_rows_accepts_bare_list_and_wrapped_shapes():
    assert _as_rows([{"a": 1}]) == [{"a": 1}]
    assert _as_rows({"items": [{"a": 1}]}) == [{"a": 1}]
    assert _as_rows({"data": [{"a": 1}]}) == [{"a": 1}]
    assert _as_rows({"unexpected": "shape"}) == []


def test_base_url_switches_between_sandbox_and_prod():
    assert make_settings().service_base_url("casesapi").startswith(
        "https://ecm-se-sandbox.casesapi."
    )
    assert make_settings(environment="prod").service_base_url("casesapi").startswith(
        "https://ecm-se.casesapi."
    )
