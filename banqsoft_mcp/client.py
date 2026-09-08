"""Klient mot Banqsoft Lighthouse.

ADAPTERLAG. Endepunktene under er utledet av tjenestenavnene i Banqsofts
oppsettsguide og manifestene, men er IKKE bekreftet mot dokumentasjon.
Sti-malene ligger derfor som konstanter og kan overstyres via miljøet, slik at
de kan rettes uten kodeendring når Banqsoft har svart. Se KRAV-TIL-BANQSOFT.md.
"""

from __future__ import annotations

import os
from typing import Any

import httpx

from .auth import TokenProvider
from .config import Settings

# ADAPTER: bekreft stier og tjenestenavn med Banqsoft.
CASES_SERVICE = os.getenv("BANQSOFT_CASES_SERVICE", "casesapi")
PATH_CASE = os.getenv("BANQSOFT_PATH_CASE", "/api/v1/cases/{case_number}")
PATH_CASE_PAYMENTS = os.getenv(
    "BANQSOFT_PATH_CASE_PAYMENTS", "/api/v1/cases/{case_number}/payments"
)
PATH_CASE_SEARCH = os.getenv("BANQSOFT_PATH_CASE_SEARCH", "/api/v1/cases")


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

    async def get_case(self, case_number: str) -> dict[str, Any]:
        return await self._get(PATH_CASE.format(case_number=case_number))

    async def get_case_payments(self, case_number: str) -> list[dict[str, Any]]:
        payload = await self._get(PATH_CASE_PAYMENTS.format(case_number=case_number))
        return _as_rows(payload)

    async def search_cases(
        self, *, creditor_org_no: str, status: str | None, limit: int
    ) -> list[dict[str, Any]]:
        params: dict[str, Any] = {"creditorOrgNo": creditor_org_no, "pageSize": limit}
        if status:
            params["status"] = status
        payload = await self._get(PATH_CASE_SEARCH, params=params)
        return _as_rows(payload)[:limit]

    async def _get(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        url = self._settings.service_base_url(CASES_SERVICE) + path
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
        for key in ("items", "results", "data", "value", "cases", "payments"):
            value = payload.get(key)
            if isinstance(value, list):
                return [row for row in value if isinstance(row, dict)]
    return []
