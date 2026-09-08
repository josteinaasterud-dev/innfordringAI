from contextlib import asynccontextmanager
import json
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel, Field

from app.creditsafe import (
    CreditsafeClient,
    CreditsafeError,
    summarize_report,
    summarize_search,
)

load_dotenv()

creditsafe = CreditsafeClient()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await creditsafe.aclose()


app = FastAPI(title="innfordringAI", lifespan=lifespan)

# Allow frontend (Wix) to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CHAT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1")

SYSTEM_PROMPT = "Du er NettJus AI. Svar kort, presist og juridisk forsiktig."

ASSESSMENT_PROMPT = (
    "Du er NettJus AI og hjelper med innfordring i Norge. Du får et utdrag av en "
    "kredittrapport fra Creditsafe. Vurder kort: (1) debitors betalingsevne, "
    "(2) risiko for tap, og (3) anbefalt neste steg i innfordringen "
    "(purring, inkassovarsel, betalingsoppfordring, rettslig inndriving eller "
    "avskrivning). Bygg kun på tallene du får – ikke gjett. Si tydelig fra hvis "
    "datagrunnlaget er for tynt. Svar kort, presist og juridisk forsiktig."
)

_openai_client: OpenAI | None = None


def get_openai_client() -> OpenAI:
    """Lager OpenAI-klienten ved første bruk.

    Klienten opprettes lazy slik at Creditsafe-endepunktene kan brukes selv om
    OPENAI_API_KEY ikke er satt.
    """
    global _openai_client
    if _openai_client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise HTTPException(
                status_code=503,
                detail="OPENAI_API_KEY er ikke satt. Sett den i `.env` eller miljøvariablene.",
            )
        _openai_client = OpenAI(api_key=api_key)
    return _openai_client


def ask_openai(system_prompt: str, user_prompt: str, max_tokens: int = 500) -> str:
    client = get_openai_client()
    try:
        response = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=max_tokens,
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"OpenAI request failed: {exc}") from exc

    answer = None
    if getattr(response, "choices", None):
        first = response.choices[0]
        if isinstance(first.message, dict):
            answer = first.message.get("content")
        else:
            answer = getattr(first.message, "content", None)

    if not answer:
        raise HTTPException(status_code=502, detail="No answer returned from OpenAI")
    return answer


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)


class AssessmentRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=1,
        description="Organisasjonsnummer (9 siffer) eller selskapsnavn.",
    )
    countries: str | None = Field(
        default=None, description="Landkoder, f.eks. «NO» eller «NO,SE»."
    )
    amount: float | None = Field(
        default=None, description="Utestående beløp i saken, brukt i vurderingen."
    )
    currency: str = Field(default="NOK")


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
        "creditsafe_configured": creditsafe.is_configured,
    }


@app.post("/chat")
async def chat(payload: ChatRequest):
    return {"answer": ask_openai(SYSTEM_PROMPT, payload.message)}


@app.get("/creditsafe/companies")
async def search_companies(
    name: str | None = Query(default=None, description="Selskapsnavn å søke på."),
    reg_no: str | None = Query(default=None, description="Organisasjonsnummer."),
    countries: str | None = Query(default=None, description="Landkoder, f.eks. «NO»."),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=200),
):
    """Søker opp selskaper hos Creditsafe på navn eller organisasjonsnummer."""
    try:
        result = await creditsafe.search_companies(
            name=name,
            reg_no=reg_no,
            countries=countries,
            page=page,
            page_size=page_size,
        )
    except CreditsafeError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc

    return {
        "total": result.get("totalSize"),
        "companies": summarize_search(result),
    }


@app.get("/creditsafe/companies/{connect_id}")
async def company_report(
    connect_id: str,
    language: str = Query(default="NO"),
    full: bool = Query(
        default=False, description="Ta med hele rårapporten fra Creditsafe."
    ),
):
    """Henter kredittrapport for en Creditsafe connect-id."""
    try:
        report = await creditsafe.get_company_report(connect_id, language=language)
    except CreditsafeError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc

    response = {"connect_id": connect_id, "summary": summarize_report(report)}
    if full:
        response["report"] = report
    return response


@app.post("/creditsafe/assessment")
async def credit_assessment(payload: AssessmentRequest):
    """Slår opp debitor hos Creditsafe og lar modellen vurdere innfordringen."""
    try:
        report = await creditsafe.get_report_by_query(
            payload.query, countries=payload.countries
        )
    except CreditsafeError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc

    summary = summarize_report(report)

    lines = ["Kredittdata fra Creditsafe:", json.dumps(summary, ensure_ascii=False, indent=2)]
    if payload.amount is not None:
        lines.append(f"Utestående krav i saken: {payload.amount} {payload.currency}.")
    lines.append("Gi en kort innfordringsvurdering.")

    answer = ask_openai(ASSESSMENT_PROMPT, "\n\n".join(lines), max_tokens=700)
    return {"summary": summary, "assessment": answer}
