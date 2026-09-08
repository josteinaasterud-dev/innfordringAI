# innfordringAI

FastAPI-backend for NettJus AI med integrasjon mot **Creditsafe Connect API**.
Slår opp debitor, henter kredittrapport og lar modellen gi en
innfordringsvurdering basert på faktiske kredittdata.

## Oppsett

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fyll inn nøkler
uvicorn app.main:app --reload
```

Interaktiv API-dokumentasjon ligger på `/docs`.

## Miljøvariabler

| Variabel | Beskrivelse |
| --- | --- |
| `OPENAI_API_KEY` | Nøkkel for chat- og vurderingsendepunktene. |
| `OPENAI_MODEL` | Modellnavn, standard `gpt-4.1`. |
| `CREDITSAFE_USERNAME` | Brukernavn til Creditsafe Connect. |
| `CREDITSAFE_PASSWORD` | Passord til Creditsafe Connect. |
| `CREDITSAFE_BASE_URL` | Standard `https://connect.creditsafe.com/v1`. |
| `CREDITSAFE_COUNTRIES` | Standard landkoder for søk, f.eks. `NO`. |

Nøklene leses ved oppstart, men klientene opprettes først ved bruk – mangler
`OPENAI_API_KEY` svarer chat-endepunktene `503` mens Creditsafe-oppslag
fortsatt virker, og motsatt.

## Endepunkter

| Metode | Sti | Beskrivelse |
| --- | --- | --- |
| `GET` | `/health` | Status og hvilke integrasjoner som er konfigurert. |
| `POST` | `/chat` | Fritekstspørsmål til NettJus AI. |
| `GET` | `/creditsafe/companies` | Søk på `name` og/eller `reg_no`. |
| `GET` | `/creditsafe/companies/{connect_id}` | Kredittrapport. `full=true` gir rårapporten. |
| `POST` | `/creditsafe/assessment` | Oppslag + AI-vurdering av innfordringen. |

### Eksempel

```bash
curl "http://localhost:8000/creditsafe/companies?reg_no=123456789"

curl -X POST http://localhost:8000/creditsafe/assessment \
  -H "Content-Type: application/json" \
  -d '{"query": "123456789", "amount": 45000}'
```

`query` tar både organisasjonsnummer (9 siffer) og selskapsnavn – ni siffer
slås opp direkte på `regNo`, ellers søkes det på navn og første treff brukes.

## Creditsafe-klienten

`app/creditsafe.py` håndterer autentisering (`POST /authenticate` → JWT),
cacher tokenet i overkant av en time og fornyer det automatisk ved `401`.
Feil oversettes til meningsfulle HTTP-statuser: `404` når selskapet ikke
finnes, `429` ved oppbrukt kvote, `503` når integrasjonen ikke er konfigurert.

Rapportformatet varierer mellom land, så `summarize_report()` plukker ut
feltene som betyr noe for innfordring – rating, kredittgrense, omsetning,
egenkapital og betalingsanmerkninger – uten å feile på manglende felter.

> Integrasjonen følger Connect API v1-konvensjonene. Verifiser
> endepunkter og feltnavn mot avtalen og dokumentasjonen deres før
> produksjonssetting.

## Tester

```bash
pip install -r requirements-dev.txt
pytest
```

Testene kjører mot en mocket Creditsafe (`httpx.MockTransport`) og treffer
ikke det ekte API-et.
