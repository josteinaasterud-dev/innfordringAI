import httpx
import pytest
import respx

from banqsoft_mcp.auth import AuthenticationError, TokenProvider
from banqsoft_mcp.config import Settings

TOKEN_URL = "https://login.microsoftonline.com/tenant-1/oauth2/v2.0/token"


def make_settings(**overrides) -> Settings:
    values = dict(
        tenant_id="tenant-1",
        client_id="client-1",
        client_secret="secret-1",
        api_scope="api://lighthouse/.default",
        namespace="ecm-se",
    )
    values.update(overrides)
    return Settings(**values)


@pytest.mark.asyncio
@respx.mock
async def test_fetches_and_returns_token():
    respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json={"access_token": "abc", "expires_in": 3600})
    )
    async with httpx.AsyncClient() as http:
        provider = TokenProvider(make_settings(), http)
        assert await provider.get_token() == "abc"


@pytest.mark.asyncio
@respx.mock
async def test_caches_token_across_calls():
    route = respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json={"access_token": "abc", "expires_in": 3600})
    )
    async with httpx.AsyncClient() as http:
        provider = TokenProvider(make_settings(), http)
        await provider.get_token()
        await provider.get_token()
    assert route.call_count == 1


@pytest.mark.asyncio
@respx.mock
async def test_refetches_when_token_is_near_expiry():
    route = respx.post(TOKEN_URL).mock(
        side_effect=[
            httpx.Response(200, json={"access_token": "first", "expires_in": 30}),
            httpx.Response(200, json={"access_token": "second", "expires_in": 3600}),
        ]
    )
    async with httpx.AsyncClient() as http:
        # Marginen er større enn levetiden, så tokenet regnes straks som utgått.
        provider = TokenProvider(make_settings(token_refresh_margin_seconds=120), http)
        assert await provider.get_token() == "first"
        assert await provider.get_token() == "second"
    assert route.call_count == 2


@pytest.mark.asyncio
@respx.mock
async def test_invalidate_forces_new_token():
    route = respx.post(TOKEN_URL).mock(
        side_effect=[
            httpx.Response(200, json={"access_token": "first", "expires_in": 3600}),
            httpx.Response(200, json={"access_token": "second", "expires_in": 3600}),
        ]
    )
    async with httpx.AsyncClient() as http:
        provider = TokenProvider(make_settings(), http)
        assert await provider.get_token() == "first"
        provider.invalidate()
        assert await provider.get_token() == "second"
    assert route.call_count == 2


@pytest.mark.asyncio
@respx.mock
async def test_raises_on_rejected_credentials():
    respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(401, json={"error": "invalid_client"})
    )
    async with httpx.AsyncClient() as http:
        provider = TokenProvider(make_settings(), http)
        with pytest.raises(AuthenticationError):
            await provider.get_token()
