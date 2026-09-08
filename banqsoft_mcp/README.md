# Banqsoft Lighthouse MCP-server

Gir en AI-assistent **lesetilgang** til inkassosaker i Banqsoft Lighthouse, til bruk i kundeservice.

Serveren har egen tjenesteidentitet i Entra ID. Den opptrer aldri som en innlogget person, slik at revisjonsloggen skiller maskinoppslag fra menneskers handlinger.

## Verktøy

| Verktøy | Gjør | Parametre |
|---|---|---|
| `hent_sakstatus` | Status, saldo og siste hendelse på én sak | `saksnummer` |
| `hent_betalingshistorikk` | Registrerte innbetalinger på én sak | `saksnummer` |
| `sok_saker` | Saker for én kreditor | `kreditor_orgnr`, `status`, `maks_antall` |

**Det finnes ingen skriveverktøy.** Ingenting serveren gjør kan endre en sak.

## Sikkerhetsegenskaper

| Egenskap | Hvordan |
|---|---|
| Dataminimering | Hvert felt som slippes ut står på en hvitliste. Rå API-svar returneres aldri |
| Maskering | Person- og fødselsnummer maskeres, også når de står i fritekst som saksnotater |
| Harde sperrer | Kontonummer, IBAN og identitetsfelter fjernes selv om de skulle stå på hvitlisten |
| Revisjonslogg | Hvert oppslag logges med tidspunkt, verktøy, parametre og utfall |
| Volumtak | `maks_antall` kappes mot `BANQSOFT_MAX_RESULT_ROWS` |
| Egen identitet | Client credentials på egen appregistrering, som kan trekkes tilbake alene |

## Oppsett

```bash
python -m venv venv
./venv/bin/pip install -r requirements-mcp.txt
cp .env.example .env      # fyll inn verdiene
```

Kjør serveren:

```bash
./venv/bin/python -m banqsoft_mcp.server
```

Den snakker MCP over stdio. For Claude Code legges den inn slik:

```json
{
  "mcpServers": {
    "banqsoft": {
      "command": "/full/sti/venv/bin/python",
      "args": ["-m", "banqsoft_mcp.server"],
      "cwd": "/full/sti/til/repo"
    }
  }
}
```

## Appregistrering

Lag en **egen** registrering for denne integrasjonen. Ikke gjenbruk `authenticate-app` eller `user-sync-app` fra Banqsofts oppsettsguide:

- `authenticate-app` er delegert med SPA-redirects, laget for nettleserinnlogging
- `user-sync-app` bruker federert legitimasjon og har med vilje ingen secret

En egen registrering gir smalest mulige rettigheter, egen linje i loggen, og kan trekkes tilbake uten å ta ned innloggingen for resten av huset.

## Status

Autentisering, dataminimering, logging og feilhåndtering er ferdig og testet.

**Delvis bekreftet mot Collect HTTP API 3.0.0.** Sti-prefikset `/api/v1`, ressursen `cases` og `accountingJournal`-endepunktet stemmer med dokumentasjonen. Stiene for betalinger og søk er fortsatt antatt.

**Åpent spørsmål med konsekvens for designet:** APIet tar `{caseId}`, mens saksbehandlerne refererer til saker med nummer som 1473. Er de ikke samme verdi, trengs et oppslag fra saksnummer til `caseId` først.

Alle sti-maler kan overstyres med miljøvariabler uten kodeendring. Se [KRAV-TIL-BANQSOFT.md](KRAV-TIL-BANQSOFT.md).

## Tester

```bash
./venv/bin/python -m pytest
```

25 tester dekker token-mellomlagring og fornyelse, 401-retry, feilhåndtering, maskering og hele verktøykjeden mot et mocket API.
