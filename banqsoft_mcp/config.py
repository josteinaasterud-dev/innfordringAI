"""Konfigurasjon. All hemmelig informasjon leses fra miljøet, aldri fra kode."""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Innstillinger for MCP-serveren.

    Legges i miljøvariabler eller .env. Se .env.example.
    """

    model_config = SettingsConfigDict(
        env_prefix="BANQSOFT_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Entra ID (Microsoft) ---
    tenant_id: str = Field(description="Directory (tenant) ID i Entra ID")
    client_id: str = Field(description="Application (client) ID for MCP-appregistreringen")
    client_secret: str = Field(description="Client secret. Kun fra miljø/hvelv")
    api_scope: str = Field(
        description=(
            "Scope det bes om token for. Normalt "
            "'api://<application-id-uri>/.default' for client credentials."
        )
    )
    authority: str = "https://login.microsoftonline.com"

    # --- Lighthouse ---
    namespace: str = Field(description="Tenantens namespace, f.eks. 'ecm-se'")
    environment: str = Field(default="sandbox", description="'sandbox' eller 'prod'")

    # --- Drift ---
    request_timeout_seconds: float = 20.0
    token_refresh_margin_seconds: int = 120
    audit_log_path: str | None = Field(
        default=None,
        description="Filsti for revisjonslogg. Uten verdi logges det til stderr.",
    )
    max_result_rows: int = Field(default=50, description="Øvre grense per oppslag")

    @property
    def token_url(self) -> str:
        return f"{self.authority}/{self.tenant_id}/oauth2/v2.0/token"

    def service_base_url(self, service: str) -> str:
        """Bygger basis-URL for en Lighthouse-tjeneste.

        Vertsnavnene følger mønsteret i Banqsofts oppsettsguide:
        https://<namespace>[-sandbox].<service>.lighthouse-cm.com
        """
        host = self.namespace
        if self.environment != "prod":
            host = f"{host}-{self.environment}"
        return f"https://{host}.{service}.lighthouse-cm.com"


def load_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
