"""Autentisering mot Entra ID med client credentials.

Serveren har sin egen tjenesteidentitet. Den opptrer aldri som en innlogget
person, slik at revisjonsloggen skiller maskinoppslag fra menneskers handlinger.
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass

import httpx

from .config import Settings


class AuthenticationError(RuntimeError):
    """Token kunne ikke hentes."""


@dataclass
class _CachedToken:
    value: str
    expires_at: float

    def is_valid(self, margin_seconds: int) -> bool:
        return time.monotonic() + margin_seconds < self.expires_at


class TokenProvider:
    """Henter og mellomlagrer access tokens."""

    def __init__(self, settings: Settings, client: httpx.AsyncClient) -> None:
        self._settings = settings
        self._client = client
        self._cached: _CachedToken | None = None
        self._lock = asyncio.Lock()

    async def get_token(self) -> str:
        margin = self._settings.token_refresh_margin_seconds
        if self._cached is not None and self._cached.is_valid(margin):
            return self._cached.value

        async with self._lock:
            # En annen oppgave kan ha fornyet mens vi ventet på låsen.
            if self._cached is not None and self._cached.is_valid(margin):
                return self._cached.value
            self._cached = await self._request_token()
            return self._cached.value

    async def _request_token(self) -> _CachedToken:
        data = {
            "grant_type": "client_credentials",
            "client_id": self._settings.client_id,
            "client_secret": self._settings.client_secret,
            "scope": self._settings.api_scope,
        }
        try:
            response = await self._client.post(
                self._settings.token_url,
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=self._settings.request_timeout_seconds,
            )
        except httpx.HTTPError as exc:
            raise AuthenticationError(f"Kunne ikke nå Entra ID: {exc}") from exc

        if response.status_code != 200:
            # Feilteksten fra Entra kan inneholde korrelasjons-ID, men aldri
            # hemmeligheter. Den tas med fordi den er nyttig ved feilsøking.
            raise AuthenticationError(
                f"Token avvist ({response.status_code}): {response.text[:400]}"
            )

        payload = response.json()
        token = payload.get("access_token")
        if not token:
            raise AuthenticationError("Svaret fra Entra ID manglet access_token")

        expires_in = int(payload.get("expires_in", 3600))
        return _CachedToken(value=token, expires_at=time.monotonic() + expires_in)

    def invalidate(self) -> None:
        """Kaster mellomlagret token, f.eks. etter 401 fra APIet."""
        self._cached = None
