# Spørsmål til Banqsoft

Underlag for dialogen om integrasjon mot Lighthouse.

**Kilder:** Collect HTTP API 3.0.0-20250116.1 (Cases Service) og Ledger HTTP API 1.0.0 — API-dokumentasjonen på Credit Management Suite Docs.

## Bekreftet så langt

| Forhold | Status |
|---|---|
| Sti-prefiks | `/api/v1` |
| Ressurs for saker | `cases` |
| Enkeltsak | `/api/v1/cases/{caseId}` |
| Bokføringshistorikk per sak | `GET /api/v1/cases/{caseId}/accountingJournal` |
| Autentisering | OAuth2 på samtlige endepunkter |
| Ledger-vertsnavn | `<namespace>.ledger.lighthouse-cm.com`, bekreftet i app-manifestet |
| Ledger-ressurser | `chartOfAccounts`, `ledgerTransaction`, `booking`, `reports`, `vatRegistry`, `settlement` |
| OpenAPI-spesifikasjon | Finnes for begge tjenester, med nedlastingslenke |

---

## 0. Rettighetsmodellen — nytt, og viktig

Ledger-dokumentasjonen viser rettighetene som kan tildeles en systemrolle:

```
CanManageUsers, CanManageCreditors, CanManageCDRs, CanAccessCreditorAccount,
CanManageBusinessConfiguration, CanManageBookings, CanManageDigitalJobs,
CanManageSettlements, CanConfirmSettlements, CanAccessCDRs,
CanAccessBusinessConfiguration, CanCreditInvoices, CanManageAllocations,
CanDeleteOrders, CanManagePayments, CanConfirmRefunds, CanManageRefunds,
CanForcePrintReset, CanManageOrders
```

Nitten rettigheter, hvorav bare tre er lesetilgang: `CanAccessCreditorAccount`, `CanAccessCDRs` og `CanAccessBusinessConfiguration`. Resten er `CanManage*` eller `CanConfirm*`, altså skrivetilgang.

> **Hvilke rettigheter kreves for å LESE kontoplan, hovedbokstransaksjoner og saker — og finnes det lesevarianter, eller må vi ta `CanManage*` for å komme til dataene?**

Dette har direkte betydning for sikkerheten. Vår MCP-server har ingen skriveverktøy, men hvis tokenet likevel må bære `CanManageBookings` for å lese posteringer, hviler skrivesperren utelukkende på vår kode — ikke på rettighetene. Det er en vesentlig svakere garanti, og noe vi må kunne redegjøre for.

Finnes det ikke rene leserettigheter i dag: **er det noe dere kan legge til?** En `CanAccess`-variant for booking, ledger og cases ville løst det.

## 1. Autentiseringsflyt — fortsatt avgjørende

Dokumentasjonen sier `oauth2`, men ikke hvilke flyter som er tillatt. `authenticate-app` i oppsettsguiden er delegert med SPA-redirects, altså laget for en nettleser med et menneske bak. En bakgrunnstjeneste kan ikke bruke den.

> **Støtter Collect-APIet `client_credentials`, eller må alle kall gå on-behalf-of en innlogget bruker?**

Hvis client credentials støttes:
- Hvilken app-rolle eller scope skal vår registrering ha?
- Hvilken verdi skal `scope` ha i token-forespørselen? (`api://<uri>/.default`?)
- Skal `Expose an API` gjøres på vår egen registrering, eller får vi tilgang til en scope dere eier?

Hvis ikke: finnes det en tjenestebruker vi kan opprette, eller må vi vente?

## 2. Er `caseId` det samme som saksnummeret?

Dette har direkte betydning for hvordan verktøyet må bygges.

Internt refererer vi til saker med nummer som **1473** og **1150**. APIet tar `{caseId}`.

> **Er `caseId` den samme verdien som saksnummeret saksbehandlerne ser, eller en intern nøkkel?**

Er de forskjellige, trenger vi et oppslag fra saksnummer til `caseId` — og da: hvilket endepunkt gjør det? `Search`, eller et filter på `/api/v1/cases`?

## 3. OpenAPI-spesifikasjonene

Begge dokumentasjonssidene har en nedlastingslenke. **Kan vi få begge filene?** De løser stier, feltnavn, paginering, feiltyper og tillatte OAuth2-flyter på én gang, og fjerner det meste av gjettingen i punkt 0, 1, 4 og 5.

## 4. Endepunkter vi trenger bekreftet

| Formål | Antatt sti | Status |
|---|---|---|
| Hent én sak | `GET /api/v1/cases/{caseId}` | Bekreftet mønster |
| Innbetalinger på sak | `GET /api/v1/cases/{caseId}/payments` | **Antatt.** Ressursgruppen heter `CasePayments` |
| Søk saker per kreditor | `GET /api/v1/cases?creditorOrgNo=…` | **Antatt.** Filternavnet er ikke bekreftet |
| Bokføringshistorikk | `GET /api/v1/cases/{caseId}/accountingJournal` | Bekreftet |
| Kontoplan (Collect) | `ChartOfAccounts` | Sti ikke lest |
| Kontoplan (Ledger) | `GET /api/v1/chartOfAccounts` | **Antatt.** Ressursnavn bekreftet |
| Hovedbokstransaksjoner | `GET /api/v1/ledgerTransaction` | **Antatt.** Ressursnavn bekreftet |
| Månedsrapport | `reports` | Sti ikke lest |

## 5. Feltnavn i svarene

Vi hvitlister felter framfor å slippe gjennom hele svaret, og trenger de faktiske navnene for: saksnummer, status og statustekst, opprinnelig beløp, restsaldo, valuta, skyldnernavn, kreditornavn, kreditors organisasjonsnummer, siste hendelse med dato og tekst, neste planlagte steg, samt innbetalinger med dato, beløp, valuta, type og referanse.

Ett eksempelsvar fra et saksoppslag dekker hele dette punktet.

## 6. Paginering og grenser

- Hvordan pagineres søk? (`pageSize`/`page`, `top`/`skip`, cursor?)
- Hvilke rate limits gjelder?
- Er det tak på hvor mange saker et søk kan returnere?

## 7. Sandbox

- Kan vi bygge og teste mot `sandbox` med samme registrering?
- Finnes det testdata, eller må vi opprette saker selv?

## 8. Personopplysninger

- Hvilke felter kan inneholde fødsels- eller personnummer? Vi filtrerer allerede, men vil vite hvor de kan dukke opp.
- Loggfører dere våre oppslag på deres side, og kan vi få tilgang til den loggen ved behov?
- Ressursgruppen `Gdpr` — hva dekker den, og er det noe vi må forholde oss til?

---

## Bonus: Ledger løser en flaskehals vi allerede har

`chartOfAccounts`, `ledgerTransaction` og `reports` svarer direkte på det Offshore IT har purret på siden juli:

| Deres spørsmål | Endepunkt |
|---|---|
| Kontonavn for angitte kontonumre (ubesvart siden 17. juli) | `chartOfAccounts` |
| Posteringer bak avvikene 3. og 9. juli | `ledgerTransaction` |
| Månedsrapport med saldo på 2420 og 2429 | `reports` |

Verdt å be om tilgang til alle tre i samme runde.

---

**Kontakt:** Tommy Ottosson, Senior Business Consultant Credit Management, Banqsoft.
