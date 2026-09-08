"""Ende-til-ende: verktøykall gjennom serveren mot et mocket Lighthouse."""

import json

import httpx
import pytest
import respx

from banqsoft_mcp.config import Settings
from banqsoft_mcp.server import BanqsoftContext, build_server

TOKEN_URL = "https://login.microsoftonline.com/tenant-1/oauth2/v2.0/token"
BASE = "https://ecm-se-sandbox.casesapi.lighthouse-cm.com"


@pytest.fixture
def context(tmp_path):
    settings = Settings(
        tenant_id="tenant-1",
        client_id="client-1",
        client_secret="secret-1",
        api_scope="api://lighthouse/.default",
        namespace="ecm-se",
        environment="sandbox",
        audit_log_path=str(tmp_path / "audit.jsonl"),
    )
    return BanqsoftContext(settings)


def mock_token():
    respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json={"access_token": "abc", "expires_in": 3600})
    )


async def call(server, name, args):
    """Kaller et verktøy og henter ut det strukturerte resultatet."""
    result = await server.call_tool(name, args)
    assert not result.is_error, result.content
    return result.structured_content


@pytest.mark.asyncio
@respx.mock
async def test_case_lookup_strips_fields_and_masks_identifiers(context):
    mock_token()
    respx.get(f"{BASE}/api/v1/cases/1473").mock(
        return_value=httpx.Response(
            200,
            json={
                "caseNumber": "1473",
                "status": "Open",
                "remainingAmount": 12500,
                "debtorName": "Ola Nordmann",
                "ssn": "01011012345",
                "internalScoringModel": "hemmelig",
                "lastEventText": "Ringte 01011012345 om avtale",
            },
        )
    )
    server = build_server(context)
    result = await call(server, "hent_sakstatus", {"saksnummer": "1473"})
    sak = result["sak"]

    assert result["funnet"] is True
    assert sak["caseNumber"] == "1473"
    assert sak["remainingAmount"] == 12500
    # Feltet er ikke hvitlistet og skal være borte.
    assert "internalScoringModel" not in sak
    # Personnummer skal aldri passere, verken som felt eller i fritekst.
    assert "ssn" not in sak
    assert "01011012345" not in json.dumps(sak, ensure_ascii=False)
    assert "[maskert]" in sak["lastEventText"]

    await context.aclose()


@pytest.mark.asyncio
@respx.mock
async def test_missing_case_returns_message_instead_of_raising(context):
    mock_token()
    respx.get(f"{BASE}/api/v1/cases/9999").mock(return_value=httpx.Response(404))
    server = build_server(context)
    result = await call(server, "hent_sakstatus", {"saksnummer": "9999"})
    assert result["funnet"] is False
    assert "9999" in result["melding"]
    await context.aclose()


@pytest.mark.asyncio
@respx.mock
async def test_search_is_capped_by_max_result_rows(context):
    mock_token()
    rows = [{"caseNumber": str(n), "debtorName": f"Skyldner {n}"} for n in range(100)]
    respx.get(f"{BASE}/api/v1/cases").mock(
        return_value=httpx.Response(200, json={"items": rows})
    )
    server = build_server(context)
    # Ber om flere enn taket på 50; skal kappes.
    result = await call(server, "sok_saker", {"kreditor_orgnr": "912345678", "maks_antall": 500})
    assert result["antall"] == 50
    await context.aclose()


@pytest.mark.asyncio
@respx.mock
async def test_every_lookup_is_written_to_the_audit_log(context, tmp_path):
    mock_token()
    respx.get(f"{BASE}/api/v1/cases/1473").mock(
        return_value=httpx.Response(200, json={"caseNumber": "1473", "status": "Open"})
    )
    server = build_server(context)
    await call(server, "hent_sakstatus", {"saksnummer": "1473"})

    entries = [
        json.loads(line)
        for line in (tmp_path / "audit.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert len(entries) == 1
    assert entries[0]["tool"] == "hent_sakstatus"
    assert entries[0]["arguments"] == {"saksnummer": "1473"}
    assert entries[0]["outcome"] == "ok"
    assert entries[0]["timestamp"].endswith("+00:00")
    await context.aclose()


@pytest.mark.asyncio
@respx.mock
async def test_payments_are_listed_with_whitelisted_fields_only(context):
    mock_token()
    respx.get(f"{BASE}/api/v1/cases/1473/payments").mock(
        return_value=httpx.Response(
            200,
            json=[
                {
                    "paymentDate": "2026-07-03",
                    "amount": 500,
                    "currency": "SEK",
                    "debtorBankAccount": "1234.56.78901",
                }
            ],
        )
    )
    server = build_server(context)
    result = await call(server, "hent_betalingshistorikk", {"saksnummer": "1473"})
    assert result["antall"] == 1
    assert result["betalinger"][0] == {
        "paymentDate": "2026-07-03",
        "amount": 500,
        "currency": "SEK",
    }
    await context.aclose()


LEDGER_BASE = "https://ecm-se-sandbox.ledger.lighthouse-cm.com"


@pytest.mark.asyncio
@respx.mock
async def test_chart_of_accounts_can_be_filtered_to_one_account(context):
    mock_token()
    respx.get(f"{LEDGER_BASE}/api/v1/chartOfAccounts").mock(
        return_value=httpx.Response(
            200,
            json=[
                {"accountNumber": "2420", "accountName": "Klientmedel", "internalFlag": True},
                {"accountNumber": "2429", "accountName": "Avräkning klientmedel"},
                {"accountNumber": "3000", "accountName": "Försäljning"},
            ],
        )
    )
    server = build_server(context)
    result = await call(server, "hent_kontoplan", {"kontonummer": "2420"})

    assert result["antall"] == 1
    assert result["kontoer"][0] == {
        "accountNumber": "2420",
        "accountName": "Klientmedel",
    }
    await context.aclose()


@pytest.mark.asyncio
@respx.mock
async def test_ledger_transactions_pass_filters_and_sum_amounts(context):
    mock_token()
    route = respx.get(f"{LEDGER_BASE}/api/v1/ledgerTransaction").mock(
        return_value=httpx.Response(
            200,
            json={
                "transactions": [
                    {"transactionDate": "2026-07-03", "amount": 26278.86, "currency": "SEK"},
                    {"transactionDate": "2026-07-09", "amount": 46752.10, "currency": "SEK"},
                ]
            },
        )
    )
    server = build_server(context)
    result = await call(
        server,
        "hent_hovedbokstransaksjoner",
        {"kontonummer": "2420", "fra_dato": "2026-07-01", "til_dato": "2026-07-31"},
    )

    assert result["antall"] == 2
    assert result["sum"] == pytest.approx(73030.96)
    query = route.calls[0].request.url.params
    assert query["accountNumber"] == "2420"
    assert query["fromDate"] == "2026-07-01"
    assert query["toDate"] == "2026-07-31"
    await context.aclose()


@pytest.mark.asyncio
@respx.mock
async def test_ledger_tools_use_the_ledger_host_not_the_cases_host(context):
    mock_token()
    route = respx.get(f"{LEDGER_BASE}/api/v1/chartOfAccounts").mock(
        return_value=httpx.Response(200, json=[])
    )
    server = build_server(context)
    await call(server, "hent_kontoplan", {})
    assert route.calls[0].request.url.host == "ecm-se-sandbox.ledger.lighthouse-cm.com"
    await context.aclose()
