"""Forhåndssjekk av oppsettet.

Kjøres med:  python -m banqsoft_mcp.verify

Sjekker at konfigurasjonen er komplett, at Entra ID utsteder token, og at
Lighthouse svarer. Hemmeligheter skrives aldri ut.
"""

from __future__ import annotations

import asyncio
import sys

import httpx

from .auth import AuthenticationError, TokenProvider
from .client import CASES_SERVICE, LEDGER_SERVICE, LighthouseClient, LighthouseError
from .config import Settings, load_settings

OK = "  OK   "
FEIL = " FEIL  "
HOPPET = " HOPP  "


def _mask(value: str) -> str:
    """Viser nok til gjenkjenning, ikke nok til bruk."""
    if len(value) <= 8:
        return "*" * len(value)
    return f"{value[:4]}…{value[-4:]}"


def sjekk_konfigurasjon() -> Settings | None:
    print("1. Konfigurasjon")
    try:
        settings = load_settings()
    except Exception as exc:  # pydantic ValidationError m.fl.
        print(f"{FEIL} Mangler eller ugyldig konfigurasjon.")
        print(f"       {exc}")
        print("\n       Kopier .env.example til .env og fyll inn verdiene.")
        return None

    print(f"{OK} tenant_id   {_mask(settings.tenant_id)}")
    print(f"{OK} client_id   {_mask(settings.client_id)}")
    print(f"{OK} secret      {'satt' if settings.client_secret else 'TOM'}")
    print(f"{OK} scope       {settings.api_scope}")
    print(f"{OK} namespace   {settings.namespace} ({settings.environment})")
    print(f"{OK} cases       {settings.service_base_url(CASES_SERVICE)}")
    print(f"{OK} ledger      {settings.service_base_url(LEDGER_SERVICE)}")

    if not settings.client_secret:
        print(f"{FEIL} BANQSOFT_CLIENT_SECRET er tom.")
        return None
    return settings


async def sjekk_token(settings: Settings, http: httpx.AsyncClient) -> TokenProvider | None:
    print("\n2. Token fra Entra ID")
    provider = TokenProvider(settings, http)
    try:
        token = await provider.get_token()
    except AuthenticationError as exc:
        print(f"{FEIL} {exc}")
        print("\n       Vanlige årsaker:")
        print("       - feil tenant_id, client_id eller secret")
        print("       - secret utløpt")
        print("       - feil scope. Prøv 'api://<application-id-uri>/.default'")
        return None
    print(f"{OK} Token mottatt ({len(token)} tegn)")
    return provider


async def sjekk_api(
    settings: Settings, http: httpx.AsyncClient, provider: TokenProvider
) -> bool:
    print("\n3. Kall mot Lighthouse")
    client = LighthouseClient(settings, http, provider)
    try:
        await client.get_chart_of_accounts()
    except LighthouseError as exc:
        melding = str(exc)
        print(f"{FEIL} {melding}")
        if "403" in melding:
            print("\n       Token er gyldig, men mangler rettigheter.")
            print("       Se spørsmål 0 i KRAV-TIL-BANQSOFT.md om rettighetsmodellen.")
        elif "404" in melding:
            print("\n       Endepunktet finnes ikke på den stien vi antok.")
            print("       Overstyr med BANQSOFT_PATH_CHART_OF_ACCOUNTS i .env.")
        return False
    print(f"{OK} Ledger svarte på /api/v1/chartOfAccounts")
    return True


async def main() -> int:
    print("Forhåndssjekk av Banqsoft MCP-server\n")

    settings = sjekk_konfigurasjon()
    if settings is None:
        return 1

    async with httpx.AsyncClient() as http:
        provider = await sjekk_token(settings, http)
        if provider is None:
            return 1
        api_ok = await sjekk_api(settings, http, provider)

    print()
    if api_ok:
        print("Alt klart. Serveren kan tas i bruk.")
        return 0
    print("Autentisering virker, men APIet svarte ikke som ventet.")
    print("Serveren starter likevel — se meldingen over for hva som må rettes.")
    return 2


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
