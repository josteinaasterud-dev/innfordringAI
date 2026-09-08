import httpx
import pytest

from app.creditsafe import (
    CreditsafeClient,
    CreditsafeError,
    CreditsafeNotConfigured,
    is_org_number,
    summarize_report,
    summarize_search,
)

SEARCH_RESPONSE = {
    "totalSize": 1,
    "companies": [
        {
            "id": "NO-0-123456789",
            "country": "NO",
            "regNo": "123456789",
            "safeNo": "NO001",
            "name": "Testselskapet AS",
            "status": "Active",
            "type": "Ltd",
            "address": {"city": "Oslo", "postalCode": "0150", "street": "Storgata 1"},
        }
    ],
}

REPORT_RESPONSE = {
    "report": {
        "companySummary": {
            "businessName": "Testselskapet AS",
            "country": "NO",
            "companyRegistrationNumber": "123456789",
            "companyStatus": {"status": "Active", "description": "Aktivt"},
            "latestTurnoverFigure": {"currency": "NOK", "value": 12000000},
            "latestShareholdersEquityFigure": {"currency": "NOK", "value": 2500000},
        },
        "creditScore": {
            "currentCreditRating": {
                "commonValue": "B",
                "commonDescription": "Moderat risiko",
                "providerValue": {"value": "58"},
                "providerDescription": {"value": "Kredittverdig"},
            },
            "previousCreditRating": {"commonValue": "A"},
            "currentContractLimit": {"currency": "NOK", "value": 300000},
        },
        "negativeInformation": {
            "paymentRemarkDetails": [{"value": 5000}, {"value": 7000}],
            "totalValueOfPaymentRemarks": {"currency": "NOK", "value": 12000},
        },
    }
}


def build_client(handler, **kwargs):
    transport = httpx.MockTransport(handler)
    return CreditsafeClient(
        username="user",
        password="pass",
        base_url="https://example.test/v1",
        client=httpx.AsyncClient(transport=transport),
        **kwargs,
    )


def test_is_org_number():
    assert is_org_number("123456789")
    assert is_org_number("123 456 789")
    assert not is_org_number("12345678")
    assert not is_org_number("Testselskapet AS")


def test_summarize_search():
    [company] = summarize_search(SEARCH_RESPONSE)
    assert company["connect_id"] == "NO-0-123456789"
    assert company["org_number"] == "123456789"
    assert company["city"] == "Oslo"


def test_summarize_report():
    summary = summarize_report(REPORT_RESPONSE)
    assert summary["company_name"] == "Testselskapet AS"
    assert summary["company_status"] == "Aktivt"
    assert summary["credit_rating"]["common_value"] == "B"
    assert summary["credit_rating"]["previous_common_value"] == "A"
    assert summary["credit_limit"] == {"value": 300000, "currency": "NOK"}
    assert summary["latest_turnover"] == {"value": 12000000, "currency": "NOK"}
    assert summary["payment_remarks"]["count"] == 2
    assert summary["payment_remarks"]["total_value"]["value"] == 12000


def test_summarize_report_handles_empty_payload():
    summary = summarize_report({})
    assert summary["company_name"] is None
    assert summary["credit_rating"]["common_value"] is None
    assert summary["credit_limit"] is None


@pytest.mark.asyncio
async def test_search_authenticates_once_and_reuses_token():
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        if request.url.path.endswith("/authenticate"):
            return httpx.Response(200, json={"token": "tok-1"})
        assert request.headers["Authorization"] == "tok-1"
        return httpx.Response(200, json=SEARCH_RESPONSE)

    client = build_client(handler)
    await client.search_companies(name="Testselskapet")
    await client.search_companies(name="Testselskapet")

    assert len(calls) == 3  # én autentisering, to søk
    assert calls[1].url.params["countries"] == "NO"
    assert calls[1].url.params["name"] == "Testselskapet"


@pytest.mark.asyncio
async def test_expired_token_is_refreshed_once():
    tokens = iter(["tok-old", "tok-new"])
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/authenticate"):
            return httpx.Response(200, json={"token": next(tokens)})
        seen.append(request.headers["Authorization"])
        if request.headers["Authorization"] == "tok-old":
            return httpx.Response(401, json={"message": "expired"})
        return httpx.Response(200, json=SEARCH_RESPONSE)

    client = build_client(handler)
    result = await client.search_companies(reg_no="123 456 789")

    assert seen == ["tok-old", "tok-new"]
    assert result["totalSize"] == 1


@pytest.mark.asyncio
async def test_find_connect_id_uses_reg_no_for_org_numbers():
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/authenticate"):
            return httpx.Response(200, json={"token": "tok"})
        assert request.url.params["regNo"] == "123456789"
        assert "name" not in request.url.params
        return httpx.Response(200, json=SEARCH_RESPONSE)

    client = build_client(handler)
    assert await client.find_connect_id("123 456 789") == "NO-0-123456789"


@pytest.mark.asyncio
async def test_no_hits_gives_404():
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/authenticate"):
            return httpx.Response(200, json={"token": "tok"})
        return httpx.Response(200, json={"totalSize": 0, "companies": []})

    client = build_client(handler)
    with pytest.raises(CreditsafeError) as excinfo:
        await client.find_connect_id("Ukjent AS")
    assert excinfo.value.status_code == 404


@pytest.mark.asyncio
async def test_rate_limit_is_surfaced_as_429():
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/authenticate"):
            return httpx.Response(200, json={"token": "tok"})
        return httpx.Response(429, text="too many requests")

    client = build_client(handler)
    with pytest.raises(CreditsafeError) as excinfo:
        await client.get_company_report("NO-0-123456789")
    assert excinfo.value.status_code == 429


@pytest.mark.asyncio
async def test_missing_credentials_gives_503():
    client = CreditsafeClient(username=None, password=None, base_url="https://example.test/v1")
    assert not client.is_configured
    with pytest.raises(CreditsafeNotConfigured) as excinfo:
        await client.search_companies(name="Testselskapet")
    assert excinfo.value.status_code == 503


@pytest.mark.asyncio
async def test_search_requires_name_or_reg_no():
    client = build_client(lambda request: httpx.Response(200, json={}))
    with pytest.raises(CreditsafeError) as excinfo:
        await client.search_companies()
    assert excinfo.value.status_code == 400
