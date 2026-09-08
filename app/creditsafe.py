"""Klient mot Creditsafe Connect API.

Brukes til å slå opp selskaper og hente kredittrapporter slik at
innfordringssaker kan vurderes mot debitors faktiske betalingsevne.

API-dokumentasjon: https://connect.creditsafe.com/v1 (Connect API).
Autentisering skjer med brukernavn/passord som byttes mot et JWT-token
med ca. én times levetid. Tokenet caches og fornyes automatisk.
"""

from __future__ import annotations

import asyncio
import os
import re
import time
from typing import Any

import httpx

DEFAULT_BASE_URL = "https://connect.creditsafe.com/v1"

# Creditsafe-tokenet varer i ca. 1 time. Vi fornyer litt før utløp.
TOKEN_TTL_SECONDS = 3600
TOKEN_REFRESH_MARGIN_SECONDS = 120

# Norske organisasjonsnummer er 9 siffer.
ORG_NUMBER_RE = re.compile(r"^\d{9}$")


class CreditsafeError(Exception):
    """Feil ved kall mot Creditsafe.

    `status_code` er HTTP-statusen vi bør returnere videre til vår egen klient.
    """

    def __init__(self, message: str, status_code: int = 502) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class CreditsafeNotConfigured(CreditsafeError):
    def __init__(self) -> None:
        super().__init__(
            "Creditsafe er ikke konfigurert. Sett CREDITSAFE_USERNAME og "
            "CREDITSAFE_PASSWORD i miljøet.",
            status_code=503,
        )


def normalize_org_number(value: str) -> str:
    """Fjerner mellomrom og punktum fra et organisasjonsnummer."""
    return re.sub(r"[\s.]", "", value or "")


def is_org_number(value: str) -> bool:
    return bool(ORG_NUMBER_RE.match(normalize_org_number(value)))


class CreditsafeClient:
    """Tynn, asynkron klient mot Creditsafe Connect.

    Instansen er trygg å dele mellom requests: token-fornyelse er beskyttet
    av en lås slik at parallelle kall ikke autentiserer flere ganger.
    """

    def __init__(
        self,
        username: str | None = None,
        password: str | None = None,
        base_url: str | None = None,
        default_countries: str | None = None,
        timeout: float = 30.0,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.username = username if username is not None else os.getenv("CREDITSAFE_USERNAME")
        self.password = password if password is not None else os.getenv("CREDITSAFE_PASSWORD")
        self.base_url = (base_url or os.getenv("CREDITSAFE_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        self.default_countries = (
            default_countries or os.getenv("CREDITSAFE_COUNTRIES") or "NO"
        )
        self._timeout = timeout
        self._client = client
        self._owns_client = client is None
        self._token: str | None = None
        self._token_expires_at: float = 0.0
        self._auth_lock = asyncio.Lock()

    @property
    def is_configured(self) -> bool:
        return bool(self.username and self.password)

    async def aclose(self) -> None:
        if self._client is not None and self._owns_client:
            await self._client.aclose()
            self._client = None

    def _http(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self._timeout)
        return self._client

    # -- autentisering ---------------------------------------------------

    async def _authenticate(self) -> str:
        if not self.is_configured:
            raise CreditsafeNotConfigured()

        try:
            response = await self._http().post(
                f"{self.base_url}/authenticate",
                json={"username": self.username, "password": self.password},
            )
        except httpx.HTTPError as exc:
            raise CreditsafeError(f"Kunne ikke nå Creditsafe: {exc}") from exc

        if response.status_code in (401, 403):
            raise CreditsafeError(
                "Creditsafe avviste påloggingen. Sjekk CREDITSAFE_USERNAME/CREDITSAFE_PASSWORD.",
                status_code=502,
            )
        if response.status_code >= 400:
            raise CreditsafeError(
                f"Autentisering mot Creditsafe feilet (HTTP {response.status_code}).",
            )

        token = (response.json() or {}).get("token")
        if not token:
            raise CreditsafeError("Creditsafe returnerte ingen token.")

        self._token = token
        self._token_expires_at = time.monotonic() + TOKEN_TTL_SECONDS - TOKEN_REFRESH_MARGIN_SECONDS
        return token

    async def _get_token(self, force_refresh: bool = False) -> str:
        async with self._auth_lock:
            if not force_refresh and self._token and time.monotonic() < self._token_expires_at:
                return self._token
            # En parallell request kan ha fornyet tokenet mens vi ventet på låsen.
            if force_refresh:
                self._token = None
            return await self._authenticate()

    async def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        token = await self._get_token()
        url = f"{self.base_url}{path}"

        async def send(auth_token: str) -> httpx.Response:
            headers = {"Authorization": auth_token, "Accept": "application/json"}
            try:
                return await self._http().request(method, url, headers=headers, **kwargs)
            except httpx.HTTPError as exc:
                raise CreditsafeError(f"Kunne ikke nå Creditsafe: {exc}") from exc

        response = await send(token)
        if response.status_code == 401:
            # Tokenet kan ha utløpt tidligere enn antatt – prøv én gang til.
            response = await send(await self._get_token(force_refresh=True))

        if response.status_code == 404:
            raise CreditsafeError("Fant ikke selskapet hos Creditsafe.", status_code=404)
        if response.status_code == 429:
            raise CreditsafeError(
                "Creditsafe-kvoten er brukt opp (rate limit). Prøv igjen senere.",
                status_code=429,
            )
        if response.status_code >= 400:
            raise CreditsafeError(
                f"Creditsafe svarte HTTP {response.status_code}: {response.text[:200]}"
            )

        try:
            return response.json()
        except ValueError as exc:
            raise CreditsafeError("Creditsafe returnerte ugyldig JSON.") from exc

    # -- oppslag ---------------------------------------------------------

    async def search_companies(
        self,
        name: str | None = None,
        reg_no: str | None = None,
        countries: str | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> dict[str, Any]:
        """Søker opp selskaper på navn og/eller organisasjonsnummer."""
        if not name and not reg_no:
            raise CreditsafeError("Oppgi enten `name` eller `reg_no`.", status_code=400)

        params: dict[str, Any] = {
            "countries": countries or self.default_countries,
            "page": page,
            "pageSize": page_size,
        }
        if name:
            params["name"] = name
        if reg_no:
            params["regNo"] = normalize_org_number(reg_no)

        return await self._request("GET", "/companies", params=params)

    async def get_company_report(
        self, connect_id: str, language: str = "NO"
    ) -> dict[str, Any]:
        """Henter full kredittrapport for en Creditsafe connect-id."""
        if not connect_id:
            raise CreditsafeError("`connect_id` er påkrevd.", status_code=400)
        return await self._request(
            "GET", f"/companies/{connect_id}", params={"language": language}
        )

    async def find_connect_id(self, query: str, countries: str | None = None) -> str:
        """Slår opp connect-id fra organisasjonsnummer eller selskapsnavn."""
        query = (query or "").strip()
        if not query:
            raise CreditsafeError("Oppgi organisasjonsnummer eller selskapsnavn.", status_code=400)

        if is_org_number(query):
            result = await self.search_companies(reg_no=query, countries=countries)
        else:
            result = await self.search_companies(name=query, countries=countries)

        companies = (result or {}).get("companies") or []
        if not companies:
            raise CreditsafeError(f"Fant ingen selskaper for «{query}».", status_code=404)

        connect_id = companies[0].get("id")
        if not connect_id:
            raise CreditsafeError("Creditsafe returnerte et treff uten id.")
        return connect_id

    async def get_report_by_query(
        self, query: str, countries: str | None = None, language: str = "NO"
    ) -> dict[str, Any]:
        """Kombinerer søk og rapporthenting i ett kall."""
        connect_id = await self.find_connect_id(query, countries=countries)
        return await self.get_company_report(connect_id, language=language)


# -- oppsummering --------------------------------------------------------


def _get(data: Any, *path: str) -> Any:
    """Henter en nøstet verdi uten å kaste hvis noe mangler."""
    current = data
    for key in path:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def _money(value: Any) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        return None
    amount = value.get("value")
    if amount is None:
        return None
    return {"value": amount, "currency": value.get("currency")}


def summarize_report(report_response: dict[str, Any]) -> dict[str, Any]:
    """Trekker ut de feltene som betyr noe for en innfordringsvurdering.

    Creditsafe-rapporten er stor og varierer mellom land, så alt hentes
    defensivt: manglende felter blir `None` i stedet for å feile.
    """
    report = (report_response or {}).get("report") or {}
    summary = report.get("companySummary") or {}
    identification = report.get("companyIdentification") or {}
    basic = identification.get("basicInformation") or {}
    credit_score = report.get("creditScore") or {}
    current_rating = credit_score.get("currentCreditRating") or {}
    previous_rating = credit_score.get("previousCreditRating") or {}
    negative = report.get("negativeInformation") or {}
    remark_details = negative.get("paymentRemarkDetails") or []
    remark_count = negative.get("numberOfPaymentRemarks")
    if remark_count is None and remark_details:
        remark_count = len(remark_details)

    rating = current_rating or (summary.get("creditRating") or {})

    return {
        "company_name": summary.get("businessName") or basic.get("businessName"),
        "org_number": summary.get("companyRegistrationNumber")
        or basic.get("companyRegistrationNumber"),
        "country": summary.get("country") or basic.get("country"),
        "company_status": _get(summary, "companyStatus", "description")
        or _get(basic, "companyStatus", "description"),
        "legal_form": _get(basic, "legalForm", "description"),
        "credit_rating": {
            "common_value": rating.get("commonValue"),
            "common_description": rating.get("commonDescription"),
            "provider_value": _get(rating, "providerValue", "value"),
            "provider_description": _get(rating, "providerDescription", "value"),
            "previous_common_value": previous_rating.get("commonValue"),
        },
        "credit_limit": _money(credit_score.get("currentContractLimit"))
        or _money(summary.get("creditLimit")),
        "latest_turnover": _money(summary.get("latestTurnoverFigure")),
        "latest_equity": _money(summary.get("latestShareholdersEquityFigure")),
        "payment_remarks": {
            "count": remark_count,
            "total_value": _money(negative.get("totalValueOfPaymentRemarks")),
            "has_bankruptcy_history": bool(negative.get("bankruptcyHistory")),
        },
    }


def summarize_search(search_response: dict[str, Any]) -> list[dict[str, Any]]:
    """Forenkler søkeresultatet til det frontend faktisk trenger."""
    companies = (search_response or {}).get("companies") or []
    simplified = []
    for company in companies:
        if not isinstance(company, dict):
            continue
        address = company.get("address") or {}
        simplified.append(
            {
                "connect_id": company.get("id"),
                "name": company.get("name"),
                "org_number": company.get("regNo"),
                "safe_number": company.get("safeNo"),
                "country": company.get("country"),
                "status": company.get("status"),
                "type": company.get("type"),
                "city": address.get("city"),
                "postal_code": address.get("postalCode"),
                "street": address.get("street"),
            }
        )
    return simplified
