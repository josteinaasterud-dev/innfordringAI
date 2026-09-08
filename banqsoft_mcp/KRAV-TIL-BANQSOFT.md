# Spørsmål til Banqsoft

Underlag for dialogen om integrasjon mot Lighthouse.

**Kilde:** Collect HTTP API 3.0.0-20250116.1, Cases Service — API-dokumentasjonen på Credit Management Suite Docs.

## Bekreftet så langt

| Forhold | Status |
|---|---|
| Sti-prefiks | `/api/v1` |
| Ressurs for saker | `cases` |
| Enkeltsak | `/api/v1/cases/{caseId}` |
| Bokføringshistorikk per sak | `GET /api/v1/cases/{caseId}/accountingJournal` |
| Autentisering | OAuth2 på samtlige endepunkter |
| OpenAPI-spesifikasjon | Finnes, med nedlastingslenke i dokumentasjonen |

---

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

## 3. OpenAPI-spesifikasjonen

Dokumentasjonen har en nedlastingslenke. **Kan vi få filen?** Den løser stier, feltnavn, paginering og feiltyper på én gang, og fjerner det meste av gjettingen i punkt 4 og 5.

## 4. Endepunkter vi trenger bekreftet

| Formål | Antatt sti | Status |
|---|---|---|
| Hent én sak | `GET /api/v1/cases/{caseId}` | Bekreftet mønster |
| Innbetalinger på sak | `GET /api/v1/cases/{caseId}/payments` | **Antatt.** Ressursgruppen heter `CasePayments` |
| Søk saker per kreditor | `GET /api/v1/cases?creditorOrgNo=…` | **Antatt.** Filternavnet er ikke bekreftet |
| Bokføringshistorikk | `GET /api/v1/cases/{caseId}/accountingJournal` | Bekreftet |
| Kontoplan | `ChartOfAccounts` | Sti ikke lest |

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

## Bonus: to endepunkter som løser en annen flaskehals

`ChartOfAccounts` og `AccountingJournal` svarer direkte på det Offshore IT har purret på siden juli — kontonavn og avstemming mot hovedbok. Verdt å be om tilgang til begge i samme runde.

---

**Kontakt:** Tommy Ottosson, Senior Business Consultant Credit Management, Banqsoft.
