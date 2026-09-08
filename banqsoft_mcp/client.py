"""Klient mot Banqsoft Lighthouse.

Dekker to tjenester: Collect HTTP API 3.0.0 (saker) og Ledger HTTP API 1.0.0
(regnskap). Begge bruker /api/v1 og OAuth2.

Bekreftet mot API-dokumentasjonen: prefikset er /api/v1, ressursen heter
cases, og stier for enkeltsaker tar {caseId}.

IKKE bekreftet: om {caseId} er samme verdi som saksnummeret brukerne ser
(f.eks. 1473), eller en intern nøkkel. Stiene for betalinger og søk er heller
ikke lest i detalj. Alle sti-maler kan overstyres via miljøet, slik at de kan
rettes uten kodeendring. Se KRAV-TIL-BANQSOFT.md.
"""

from __future__ import annotations

import os
from typing import Any

import httpx

from .auth import TokenProvider
from .config import Settings

CASES_SERVICE = os.getenv("BANQSOFT_CASES_SERVICE", "casesapi")

# Bekreftet mønster i Collect HTTP API 3.0.0.
PATH_CASE = os.getenv("BANQSOFT_PATH_CASE", "/api/v1/cases/{case_id}")
# ADAPTER: ressursgruppen heter CasePayments i dokumentasjonen, men den
# eksakte stien er ikke lest. Bekreft mot OpenAPI-spesifikasjonen.
PATH_CASE_PAYMENTS = os.getenv(
    "BANQSOFT_PATH_CASE_PAYMENTS", "/api/v1/cases/{case_id}/payments"
)
PATH_CASE_SEARCH = os.getenv("BANQSOFT_PATH_CASE_SEARCH", "/api/v1/cases")
# Bekreftet i dokumentasjonen. Gir bokføringshistorikk per sak, og er
# grunnlaget for avstemming mot hovedbok.
PATH_CASE_ACCOUNTING = os.getenv(
    "BANQSOFT_PATH_CASE_ACCOUNTING", "/api/v1/cases/{case_id}/accountingJournal"
)

# --- Ledger ---
# Vertsnavnet er bekreftet i app-manifestet (<namespace>.ledger.lighthouse-cm.com).
LEDGER_SERVICE = os.getenv("BANQSOFT_LEDGER_SERVICE", "ledger")
# ADAPTER: ressursnavnene er bekreftet i Ledger-dokumentasjonen, men de
# eksakte stiene er ikke lest. Bekreft mot OpenAPI-spesifikasjonen.
PATH_CHART_OF_ACCOUNTS = os.getenv(
    "BANQSOFT_PATH_CHART_OF_ACCOUNTS", "/api/v1/chartOfAccounts"
)
PATH_LEDGER_TRANSACTIONS = os.getenv(
    "BANQSOFT_PATH_LEDGER_TRANSACTIONS", "/api/v1/ledgerTransaction"
)


class LighthouseError(RuntimeError):
    """Kallet mot Lighthouse feilet."""


class NotFoundError(LighthouseError):
    """Ressursen finnes ikke."""


class LighthouseClient:
    def __init__(
        self,
        settings: Settings,
        http: httpx.AsyncClient,
        tokens: TokenProvider,
    ) -> None:
        self._settings = settings
        self._http = http
        self._tokens = tokens

    async def get_case(self, case_id: str) -> dict[str, Any]:
        return await self._get(PATH_CASE.format(case_id=case_id))

    async def get_case_payments(self, case_id: str) -> list[dict[str, Any]]:
        payload = await self._get(PATH_CASE_PAYMENTS.format(case_id=case_id))
        return _as_rows(payload)

    async def get_case_accounting_journal(self, case_id: str) -> list[dict[str, Any]]:
        payload = await self._get(PATH_CASE_ACCOUNTING.format(case_id=case_id))
        return _as_rows(payload)

    # --- Ledger ---

    async def get_chart_of_accounts(self) -> list[dict[str, Any]]:
        payload = await self._get(PATH_CHART_OF_ACCOUNTS, service=LEDGER_SERVICE)
        return _as_rows(payload)

    async def get_ledger_transactions(
        self,
        *,
        account_number: str | None,
        from_date: str | None,
        to_date: str | None,
        limit: int,
    ) -> list[dict[str, Any]]:
        params: dict[str, Any] = {"pageSize": limit}
        if account_number:
            params["accountNumber"] = account_number
        if from_date:
            params["fromDate"] = from_date
        if to_date:
            params["toDate"] = to_date
        payload = await self._get(
            PATH_LEDGER_TRANSACTIONS, params=params, service=LEDGER_SERVICE
        )
        return _as_rows(payload)[:limit]

    async def search_cases(
        self, *, creditor_org_no: str, status: str | None, limit: int
    ) -> list[dict[str, Any]]:
        params: dict[str, Any] = {"creditorOrgNo": creditor_org_no, "pageSize": limit}
        if status:
            params["status"] = status
        payload = await self._get(PATH_CASE_SEARCH, params=params)
        return _as_rows(payload)[:limit]

    async def _get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        service: str = CASES_SERVICE,
    ) -> Any:
        url = self._settings.service_base_url(service) + path
        response = await self._request(url, params=params)

        if response.status_code == 401:
            # Tokenet kan ha blitt trukket tilbake. Ett nytt forsøk, så gir vi opp.
            self._tokens.invalidate()
            response = await self._request(url, params=params)

        if response.status_code == 404:
            raise NotFoundError("Fant ikke ressursen i Lighthouse")
        if response.status_code >= 400:
            raise LighthouseError(
                f"Lighthouse svarte {response.status_code}: {response.text[:300]}"
            )

        try:
            return response.json()
        except ValueError as exc:
            raise LighthouseError("Lighthouse returnerte ikke gyldig JSON") from exc

    async def _request(
        self, url: str, *, params: dict[str, Any] | None
    ) -> httpx.Response:
        token = await self._tokens.get_token()
        try:
            return await self._http.get(
                url,
                params=params,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/json",
                },
                timeout=self._settings.request_timeout_seconds,
            )
        except httpx.HTTPError as exc:
            raise LighthouseError(f"Kunne ikke nå Lighthouse: {exc}") from exc


def _as_rows(payload: Any) -> list[dict[str, Any]]:
    """Tåler at APIet svarer med liste, eller med liste pakket i et objekt."""
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if isinstance(payload, dict):
        for key in (
            "items",
            "results",
            "data",
            "value",
            "cases",
            "payments",
            "accounts",
            "transactions",
        ):
            value = payload.get(key)
            if isinstance(value, list):
                return [row for row in value if isinstance(row, dict)]
    return []
