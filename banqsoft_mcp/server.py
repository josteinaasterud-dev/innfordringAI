"""MCP-server med lesetilgang til Banqsoft Lighthouse.

Serveren eksponerer et lite antall verktøy for kundeservice. Den har ingen
skriveverktøy: ingenting den gjør kan endre en sak.
"""

from __future__ import annotations

import contextlib
from typing import Any

import httpx
from mcp.server.mcpserver import MCPServer

from .audit import AuditLog
from .auth import AuthenticationError, TokenProvider
from .client import LighthouseClient, LighthouseError, NotFoundError
from .config import Settings, load_settings
from .redaction import pick

# Felter kundeservice trenger for å svare på "hvor står saken".
CASE_FIELDS = (
    "caseNumber",
    "status",
    "statusText",
    "createdDate",
    "closedDate",
    "originalAmount",
    "remainingAmount",
    "currency",
    "debtorName",
    "creditorName",
    "creditorOrgNo",
    "lastEventDate",
    "lastEventText",
    "nextActionDate",
    "nextActionText",
)

PAYMENT_FIELDS = (
    "paymentDate",
    "registeredDate",
    "amount",
    "currency",
    "paymentType",
    "reference",
)

SEARCH_FIELDS = (
    "caseNumber",
    "status",
    "statusText",
    "debtorName",
    "remainingAmount",
    "currency",
    "createdDate",
)


class BanqsoftContext:
    """Holder levetiden til HTTP-klient, token og logg."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.audit = AuditLog(settings.audit_log_path)
        self._http = httpx.AsyncClient()
        self.tokens = TokenProvider(settings, self._http)
        self.client = LighthouseClient(settings, self._http, self.tokens)

    async def aclose(self) -> None:
        await self._http.aclose()


def build_server(context: BanqsoftContext) -> MCPServer:
    server = MCPServer(
        name="banqsoft-lighthouse",
        title="Banqsoft Lighthouse (lesetilgang)",
        instructions=(
            "Gir lesetilgang til inkassosaker i Banqsoft Lighthouse for bruk i "
            "kundeservice. Alle oppslag logges. Svarene inneholder kun et "
            "utvalg felter, og personnumre er maskert. Verktøyene kan ikke "
            "endre saker."
        ),
        version="0.1.0",
    )

    @server.tool(
        name="hent_sakstatus",
        title="Hent status på en inkassosak",
        description=(
            "Henter status, saldo og siste hendelse for én sak. "
            "Bruk dette når noen spør hvor en sak står. "
            "Saksnummeret er Lighthouse sitt saksnummer, ikke kreditors fakturanummer."
        ),
    )
    async def hent_sakstatus(saksnummer: str) -> dict[str, Any]:
        args = {"saksnummer": saksnummer}
        try:
            raw = await context.client.get_case(saksnummer)
        except NotFoundError:
            context.audit.record(
                tool="hent_sakstatus", arguments=args, outcome="not_found"
            )
            return {"funnet": False, "melding": f"Fant ingen sak med nummer {saksnummer}."}
        except (LighthouseError, AuthenticationError) as exc:
            context.audit.record(
                tool="hent_sakstatus", arguments=args, outcome="error", error=str(exc)
            )
            raise

        sak = pick(raw, CASE_FIELDS)
        context.audit.record(
            tool="hent_sakstatus", arguments=args, outcome="ok", row_count=1
        )
        return {"funnet": True, "sak": sak}

    @server.tool(
        name="hent_betalingshistorikk",
        title="Hent innbetalinger på en sak",
        description=(
            "Lister registrerte innbetalinger på én sak, nyeste først. "
            "Bruk dette når spørsmålet gjelder om noe er betalt, eller når "
            "en innbetaling ikke er kommet fram."
        ),
    )
    async def hent_betalingshistorikk(saksnummer: str) -> dict[str, Any]:
        args = {"saksnummer": saksnummer}
        try:
            rows = await context.client.get_case_payments(saksnummer)
        except NotFoundError:
            context.audit.record(
                tool="hent_betalingshistorikk", arguments=args, outcome="not_found"
            )
            return {"funnet": False, "melding": f"Fant ingen sak med nummer {saksnummer}."}
        except (LighthouseError, AuthenticationError) as exc:
            context.audit.record(
                tool="hent_betalingshistorikk",
                arguments=args,
                outcome="error",
                error=str(exc),
            )
            raise

        betalinger = [pick(row, PAYMENT_FIELDS) for row in rows]
        context.audit.record(
            tool="hent_betalingshistorikk",
            arguments=args,
            outcome="ok",
            row_count=len(betalinger),
        )
        return {"funnet": True, "antall": len(betalinger), "betalinger": betalinger}

    @server.tool(
        name="sok_saker",
        title="Søk opp saker for en kreditor",
        description=(
            "Lister saker for én kreditor, angitt med organisasjonsnummer. "
            "Bruk dette når en kreditor spør om sine egne saker. "
            "Søket er begrenset til én kreditor om gangen."
        ),
    )
    async def sok_saker(
        kreditor_orgnr: str,
        status: str | None = None,
        maks_antall: int = 20,
    ) -> dict[str, Any]:
        limit = max(1, min(maks_antall, context.settings.max_result_rows))
        args = {
            "kreditor_orgnr": kreditor_orgnr,
            "status": status,
            "maks_antall": limit,
        }
        try:
            rows = await context.client.search_cases(
                creditor_org_no=kreditor_orgnr, status=status, limit=limit
            )
        except (LighthouseError, AuthenticationError) as exc:
            context.audit.record(
                tool="sok_saker", arguments=args, outcome="error", error=str(exc)
            )
            raise

        saker = [pick(row, SEARCH_FIELDS) for row in rows]
        context.audit.record(
            tool="sok_saker", arguments=args, outcome="ok", row_count=len(saker)
        )
        return {"antall": len(saker), "saker": saker}

    return server


def main() -> None:
    settings = load_settings()
    context = BanqsoftContext(settings)
    server = build_server(context)
    try:
        server.run(transport="stdio")
    finally:
        with contextlib.suppress(Exception):
            import asyncio

            asyncio.run(context.aclose())


if __name__ == "__main__":
    main()
