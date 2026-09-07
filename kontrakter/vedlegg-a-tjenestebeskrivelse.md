# Vedlegg A – Tjeneste- og modulbeskrivelse

## A.1 Leveransemodell

Agaas leverer regnskapssystem og regnskapsføring som **én samlet tjeneste**. Kolonnen **Leverandør** viser hvor ansvaret ligger.

| Lag | Innhold | Leverandør | Avtalegrunnlag |
|---|---|---|---|
| 1. Plattform | Regnskapssystem, moduler, integrasjoner | Agaas AS | Denne Avtalen |
| 2. Regnskapsføring | Løpende bokføring, avstemming, rapportering, årsoppgjør – omfang etter valgt pakke | Agaas AS, som autorisert regnskapsforetak | Pakkebekreftelsen og Vedlegg H |
| 3. Rådgivning | Bedriftsrådgivning, prosess, rapportering, opplæring | Agaas AS | Denne Avtalen |
| 4. Inkasso | Inndrivelse av forfalte krav | Inkassoforetak med bevilling | Egen oppdragsavtale, Vedlegg G |
| 5. Revisjon | Revisjon og attestasjon | Kundens uavhengige revisor | Kundens egen avtale |
| 6. Tredjeparter | Bank, aksesspunkt, oppslag, nye tjenester | Ekstern leverandør | Vedlegg C og G |

## A.2 Regnskapsagenten

Regnskapsagenten er den automatiserte delen av produksjonen. Den utfører løpende bokføringsoppgaver innenfor Regnskapsoppdraget: bilagstolkning, kontering, avstemming, periodisering og klargjøring av rapportering.

| Egenskap | Beskrivelse |
|---|---|
| **Faglig ansvar** | Agaas, uavhengig av om arbeidet er utført maskinelt eller av medarbeider |
| **Eskalering** | Saker agenten ikke kan avgjøre forsvarlig, flagges og avgjøres av autorisert regnskapsfører |
| **Kvalitetskontroll** | Stikkprøver av ikke-flaggede saker og terskelbaserte kontroller, jf. Vedlegg H.5 |
| **Sporbarhet** | Grunnlag, anvendt regel, tidspunkt og godkjenner logges per postering |
| **Kundens innsyn** | Kunden kan se hvordan enhver postering er fremkommet |
| **Overstyring** | Kunden kan kreve manuell behandling av angitte områder |

Automatiseringen er en produksjonsmetode, ikke en ansvarsfraskrivelse. Kunden forholder seg til Agaas som regnskapsfører, ikke til agenten.

## A.3 Plattformens moduler

### A.3.1 Regnskap og bokføring
Hovedbok, reskontro, bilagsmottak med maskinell tolkning, kontering, periodisering, avstemming, anleggsregister, prosjekt- og avdelingsdimensjoner, SAF-T-uttrekk.

### A.3.2 Fakturering og betalingsoppfølging
Salgsordre, fakturautstedelse, distribusjon på EHF, e-post eller print, purrerutine, samt klargjøring av saker for overføring til inkasso.

### A.3.3 Bank og betaling
Kontoinformasjon og transaksjoner via konsesjonspliktig tilbyder, automatisk bankavstemming, betalingsforslag. Betaling godkjennes og frigis av Kunden i banken.

### A.3.4 Lønn og personal *(dersom pakken omfatter lønn)*
Lønnskjøring, feriepenger, reiseregning, fraværsoppfølging og klargjøring av a-melding.

### A.3.5 Rapportering og innsending
Klargjøring, signering og innsending av mva-melding, a-melding, skattemelding, næringsspesifikasjon, aksjonærregisteroppgave og årsregnskap. Signeringen utføres under Kundens egen elektroniske identitet, jf. Vedlegg F.

### A.3.6 Innsikt
Resultat- og balanserapporter, likviditetsoversikt, nøkkeltall, budsjett og avviksrapportering, samt tilgangsstyrt deling med revisor og rådgivere.

### A.3.7 Integrasjonsrammeverk
API og forhåndsbygde koblinger mot tredjepartstjenester, jf. Vedlegg C. Nye koblinger aktiveres av Kunden.

## A.4 Rådgivning

Ut over Regnskapsoppdraget leverer Agaas alminnelig bedriftsrådgivning: rapporteringsmodeller og nøkkeltall, budsjett- og likviditetsstyring, prosess- og rutineforbedring, systemoppsett og opplæring, samt prosjektbistand ved migrering.

**Ikke omfattet:** juridisk rådgivning, skatterettslige utredninger og revisjonstjenester. Slikt henvises til Kundens advokat, skatterådgiver eller revisor.

## A.5 Systemkrav

Plattformen leveres som skytjeneste og krever oppdatert nettleser og internettforbindelse. Drift og lagring skjer hos Hetzner Online GmbH i datasenter i Tyskland, jf. Vedlegg C. Kunden er ansvarlig for eget utstyr og lokal sikkerhet.
