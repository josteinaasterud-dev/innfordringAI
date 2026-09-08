# Spørsmål til Banqsoft

Underlag for dialogen med Banqsoft om integrasjon mot Lighthouse. Uten svar på punkt 1 kommer resten ikke i drift.

## 1. Tjeneste-til-tjeneste-tilgang — avgjørende

`authenticate-app` i oppsettsguiden er delegert, med SPA-redirects og `User.Read`. Den er laget for en nettleser med et menneske bak. En bakgrunnstjeneste kan ikke bruke den flyten.

> **Støtter Lighthouse client credentials mot Cases- og Ledger-APIene, eller må alle kall gå on-behalf-of en innlogget bruker?**

Hvis client credentials støttes:
- Hvilken app-rolle eller scope skal registreringen ha?
- Skal `Expose an API`-steget gjøres på vår egen registrering, eller får vi tilgang til en scope Banqsoft eier?
- Hvilken verdi skal `scope` ha i token-forespørselen? (`api://<uri>/.default`?)

Hvis det **ikke** støttes: finnes det en tjenestebruker vi kan opprette, eller må vi vente på at dere åpner for det?

## 2. Endepunkter

Vi har antatt følgende ut fra tjenestenavnene i manifestet. Bekreft eller korriger:

| Formål | Antatt tjeneste | Antatt sti |
|---|---|---|
| Hent én sak | `casesapi` | `GET /api/v1/cases/{saksnummer}` |
| Innbetalinger på sak | `casesapi` | `GET /api/v1/cases/{saksnummer}/payments` |
| Søk saker per kreditor | `casesapi` | `GET /api/v1/cases?creditorOrgNo=…` |

- Finnes det OpenAPI/Swagger vi kan få? Manifestet peker på `swagger/oauth2-redirect.html` på flere tjenester, så det finnes trolig et spec-dokument.
- Er vertsnavnmønsteret `https://<namespace>[-sandbox].<tjeneste>.lighthouse-cm.com` riktig?

## 3. Feltnavn i svarene

Vi hvitlister felter framfor å slippe gjennom hele svaret. Vi trenger de faktiske feltnavnene for:

- saksnummer, status, statustekst
- opprinnelig beløp, restsaldo, valuta
- skyldnernavn, kreditornavn, kreditors organisasjonsnummer
- siste hendelse med dato og tekst
- neste planlagte steg med dato
- innbetalinger: dato, beløp, valuta, type, referanse

## 4. Paginering og grenser

- Hvordan pagineres søk? (`pageSize`/`page`, `top`/`skip`, cursor?)
- Hvilke rate limits gjelder?
- Er det noen tak på hvor mange saker et søk kan returnere?

## 5. Sandbox

- Kan vi bygge og teste mot `sandbox`-miljøet med samme registrering?
- Finnes det testdata, eller må vi opprette saker selv?

## 6. Personopplysninger

- Returnerer APIene fødsels- eller personnummer i noen felter vi bør kjenne til? Vi filtrerer allerede, men vil vite hvor de kan dukke opp.
- Loggfører Banqsoft våre oppslag på deres side, og kan vi få tilgang til den loggen ved behov?

---

**Kontakt:** Tommy Ottosson, Senior Business Consultant Credit Management, Banqsoft.
