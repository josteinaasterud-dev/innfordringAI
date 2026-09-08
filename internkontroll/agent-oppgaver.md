# Internkontroll — oppgaver for agenten

Kontrolloppgaver agenten kjører mot inkassosystemet. Listen er et utgangspunkt; fyll på nederst.

## Prinsipp

Agenten er **lesende**. Den finner avvik og rapporterer dem — den retter ingenting. Det er riktig konstruksjon for internkontroll: maskinen leter, mennesket bestemmer. Hvert funn skal kunne følges til en navngitt ansvarlig.

Statuskolonnen sier om oppgaven kan kjøres med dagens verktøy:

- **Klar** — mulig med endepunktene vi har
- **Trenger endepunkt** — krever tilgang vi ikke har bekreftet ennå
- **Trenger avklaring** — terskelen eller regelen må fastsettes først

Terskler i klammer må fylles inn. Flere av dem er **forskjellige per land** — Norge, Sverige og Danmark har ulike frister og satser.

---

## 1. Klientmidler

Det viktigste området. Pengene tilhører kreditorene, ikke dere, og Finanstilsynet ser hit først.

| ID | Kontroll | Utløser varsel | Frekvens | Status |
|---|---|---|---|---|
| KM-01 | Saldo på klientmedelskonto mot sum kreditorgjeld i hovedbok (2420/2429) | Differanse over [beløp] eller [%] | Daglig | Klar |
| KM-02 | Negativ saldo på en kreditor | Enhver negativ saldo | Daglig | Klar |
| KM-03 | Innbetalinger mottatt, men ikke allokert til sak | Eldre enn [X] dager | Daglig | Trenger endepunkt |
| KM-04 | Midler som skulle vært utbetalt til kreditor | Holdt lenger enn [X] dager | Ukentlig | Trenger endepunkt |
| KM-05 | Klientmidler blandet med driftsmidler | Enhver postering mellom kontoene | Daglig | Klar |
| KM-06 | Avstemming klientkonto mot bankutdrag | Differanse ved månedsslutt | Månedlig | Trenger endepunkt |

**KM-01 er den dere allerede har hatt problemer med.** Juliavviket kom av en betalingsfil som ikke ble importert, og ble oppdaget av regnskapsfører i ettertid. Kjørt daglig ville det vært fanget samme uke.

## 2. Inkassoprosess og god inkassoskikk

| ID | Kontroll | Utløser varsel | Frekvens | Status |
|---|---|---|---|---|
| IP-01 | Inkassovarsel sendt med lovbestemt frist før neste steg | Frist ikke overholdt | Daglig | Trenger endepunkt |
| IP-02 | Videre skritt tatt på omtvistet krav | Enhver forekomst | Daglig | Trenger endepunkt |
| IP-03 | Salær beregnet ut over gjeldende sats | Avvik fra satstabell | Ukentlig | Trenger avklaring |
| IP-04 | Saker uten fremdrift | Ingen hendelse på [X] dager | Ukentlig | Klar |
| IP-05 | Krav nær foreldelse | Under [X] måneder igjen | Månedlig | Trenger endepunkt |
| IP-06 | Saker eldre enn [X] uten avslutning eller rettslig skritt | Overskredet | Månedlig | Klar |
| IP-07 | Rettslige skritt startet uten dokumentert grunnlag | Manglende `ClaimBases` | Ukentlig | Trenger endepunkt |

**IP-02 er den farligste.** Å fortsette inndrivelse på et bestridt krav er brudd på god inkassoskikk, og det er den typen sak som havner hos Finanstilsynet.

## 3. Betalingsflyt

| ID | Kontroll | Utløser varsel | Frekvens | Status |
|---|---|---|---|---|
| BF-01 | Betalingsfiler som ikke er importert | Enhver feilet import | Daglig | Trenger endepunkt |
| BF-02 | Innbetalinger direkte til kreditor, ikke meldt til oss | Avvik mot forventet saldo | Ukentlig | Trenger avklaring |
| BF-03 | Dobbeltregistrerte innbetalinger | Samme beløp, dato og sak | Daglig | Klar |
| BF-04 | Innbetalinger uten KID eller referanse | Uidentifisert etter [X] dager | Daglig | Trenger endepunkt |
| BF-05 | Refusjoner uten godkjenning | Manglende `CanConfirmRefunds`-spor | Ukentlig | Trenger endepunkt |

## 4. Datakvalitet

| ID | Kontroll | Utløser varsel | Frekvens | Status |
|---|---|---|---|---|
| DK-01 | Saker uten skyldneradresse | Enhver forekomst | Ukentlig | Klar |
| DK-02 | Mulige dobbeltregistrerte saker | Samme skyldner, kreditor og beløp | Ukentlig | Klar |
| DK-03 | Saker uten kravgrunnlag | Manglende `ClaimBases` | Ukentlig | Trenger endepunkt |
| DK-04 | Feil kreditorkobling | Kreditor uten aktiv avtale | Månedlig | Klar |
| DK-05 | Beløp som avviker fra opprinnelig faktura | Differanse uten forklaring | Ukentlig | Trenger endepunkt |

## 5. Hvitvasking

| ID | Kontroll | Utløser varsel | Frekvens | Status |
|---|---|---|---|---|
| HV-01 | Nye kreditorer uten gjennomførte kundetiltak | Sak opprettet før tiltak | Daglig | Trenger endepunkt |
| HV-02 | Kundetiltak som ikke er oppdatert | Eldre enn [X] år | Månedlig | Trenger endepunkt |
| HV-03 | Uvanlige innbetalingsmønstre | Kontant, tredjepart, utland | Ukentlig | Trenger avklaring |
| HV-04 | Innbetaling som overstiger kravet vesentlig | Over [%] av saldo | Daglig | Klar |
| HV-05 | Kreditorer i høyrisikobransjer uten forsterkede tiltak | Mangler dokumentasjon | Månedlig | Trenger avklaring |

## 6. Personvern

| ID | Kontroll | Utløser varsel | Frekvens | Status |
|---|---|---|---|---|
| PV-01 | Saker forbi oppbevaringsfrist, ikke slettet | Over [X] år etter avslutning | Månedlig | Trenger endepunkt |
| PV-02 | Personopplysninger i felter de ikke hører hjemme i | Treff på fødselsnummer i fritekst | Ukentlig | Klar |
| PV-03 | Innsynsbegjæringer uten svar innen frist | Over [X] dager | Ukentlig | Trenger endepunkt |

**PV-02 kan agenten gjøre allerede** — maskeringen i MCP-serveren finner fødsels- og personnummer i fritekst. Den logikken kan brukes til å *finne* dem, ikke bare skjule dem.

## 7. Tilgang og systemkontroll

| ID | Kontroll | Utløser varsel | Frekvens | Status |
|---|---|---|---|---|
| TS-01 | Brukere med rettigheter ut over rollen sin | Avvik mot rollemal | Månedlig | Trenger endepunkt |
| TS-02 | Inaktive brukere med aktiv tilgang | Ingen pålogging på [X] dager | Månedlig | Trenger endepunkt |
| TS-03 | Feilede bakgrunnsjobber | Enhver feil | Daglig | Trenger endepunkt |
| TS-04 | Endringer i systemkonfigurasjon | Enhver endring | Daglig | Trenger endepunkt |
| TS-05 | Oppslag utenfor arbeidstid eller i uvanlig volum | Over [X] oppslag per bruker per dag | Ukentlig | Trenger endepunkt |

---

## Frekvensoversikt

| Frekvens | Oppgaver |
|---|---|
| **Daglig** | KM-01, KM-02, KM-03, KM-05, IP-01, IP-02, BF-01, BF-03, BF-04, HV-01, HV-04, TS-03, TS-04 |
| **Ukentlig** | KM-04, IP-03, IP-04, IP-07, BF-02, BF-05, DK-01, DK-02, DK-03, DK-05, HV-03, PV-02, PV-03, TS-05 |
| **Månedlig** | KM-06, IP-05, IP-06, DK-04, HV-02, HV-05, PV-01, TS-01, TS-02 |

## Hva agenten leverer

For hver kjøring: en liste over avvik med saksnummer, hva som utløste varselet, og når det ble oppdaget. Ingen avvik gir en kvittering på at kontrollen er kjørt — det er den kvitteringen som dokumenterer at internkontrollen fungerer, og den er like viktig som funnene.

Alt logges med tidsstempel, jf. revisjonsloggen i MCP-serveren.

## Hva som mangler

Av 36 oppgaver kan **11 kjøres med dagens verktøy**. Resten trenger endepunkter vi ikke har bekreftet. De viktigste å be Banqsoft om:

| Behov | Dekker |
|---|---|
| `CasePayments` og `Payments` | KM-03, KM-04, BF-03, BF-04 |
| `Dispute` | IP-02 |
| `ClaimBases` | IP-07, DK-03 |
| `importPayment` med feilstatus | BF-01 |
| `ChangeLog` | TS-04 |
| `Jobs` / `BackgroundProcess` | TS-03 |
| `Gdpr` | PV-01, PV-03 |
| `accessDefinitions` og `users` | TS-01, TS-02 |
| `Log` | TS-05 |

Alle finnes som ressursgrupper i Collect- og Ledger-dokumentasjonen.

---

## Egne oppgaver

Fyll på her.

| ID | Kontroll | Utløser varsel | Frekvens | Status |
|---|---|---|---|---|
| | | | | |
