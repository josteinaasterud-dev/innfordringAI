# Vedlegg A – Tjeneste- og modulbeskrivelse

Vedlegget beskriver hva som leveres, av hvem, og hvor grensesnittet mot Kunden går. Kolonnen **Leverandør** er avgjørende for ansvarsplassering etter hovedavtalens punkt 3.

## A.1 Oversikt over leveransemodell

| Lag | Innhold | Leverandør | Avtalegrunnlag |
|---|---|---|---|
| 1. Plattform | Regnskapssystem, moduler, integrasjonsrammeverk | Agaas AS | Denne Avtalen |
| 2. Rådgivning | Bedriftsrådgivning, prosess, systembruk, opplæring | Agaas AS | Denne Avtalen |
| 3. Regnskapsføring | Ekstern regnskapsføring, pliktig rapportering | Autorisert regnskapsforetak i gruppen | Egen oppdragsavtale, Vedlegg G.1 |
| 4. Inkasso | Inndrivelse av forfalte krav | Inkassoforetak med bevilling i gruppen | Egen oppdragsavtale, Vedlegg G.2 |
| 5. Revisjon | Revisjon og attestasjon | Kundens egen, uavhengige revisor | Kundens egen avtale, Vedlegg G.3 |
| 6. Tredjeparter | Bank, aksesspunkt, oppslag, nye tjenester | Ekstern leverandør | Vedlegg C og leverandørens vilkår |

## A.2 Plattformens kjernemoduler

### A.2.1 Regnskap og bokføring
Hovedbok, reskontro for kunder og leverandører, bilagsregistrering med maskinell bilagstolkning, konteringsforslag, periodisering, avstemming, prosjekt- og avdelingsdimensjoner, samt uttrekk i SAF-T-format.

*Forslag generert maskinelt er beslutningsstøtte. Kunden godkjenner all bokføring, jf. hovedavtalen punkt 5.6.*

### A.2.2 Fakturering og innfordring
Salgsordre, fakturautstedelse, distribusjon på EHF, e-post eller print, purrerutine og betalingsoppfølging, samt klargjøring av saker for overføring til inkasso, jf. Vedlegg G.2.

### A.2.3 Bank og betaling
Innhenting av kontoinformasjon og transaksjoner via konsesjonspliktig tilbyder, automatisk bankavstemming, samt klargjøring av betalingsforslag. **Betaling frigis og godkjennes av Kunden i bankens eller tilbyderens egen løsning.**

### A.2.4 Lønn og personal *(dersom aktivert)*
Lønnskjøring, feriepenger, reiseregning, samt a-melding klargjort for Kundens signering og innsending, jf. Vedlegg F.

### A.2.5 Rapportering og innsending
Klargjøring, signering og innsending av mva-melding, skattemelding, aksjonærregisteroppgave, næringsspesifikasjon og årsregnskap. Signeringen utføres i Plattformen under Kundens egen elektroniske identitet, jf. hovedavtalen punkt 7 og Vedlegg F.

### A.2.6 Rapportering og innsikt
Resultat- og balanserapporter, likviditetsoversikt, nøkkeltall, budsjett og avviksrapportering, samt tilgangsstyrt deling med Kundens rådgivere og revisor.

### A.2.7 Integrasjonsrammeverk
API og forhåndsbygde koblinger mot Tredjepartstjenester, jf. Vedlegg C. Nye koblinger gjøres tilgjengelige løpende og aktiveres av Kunden.

## A.3 Rådgivningstjenester fra Agaas AS

Agaas leverer bedriftsrådgivning innenfor følgende, alle uten å overta Kundens rapporterings- eller bokføringsansvar:

- systemoppsett, kontoplan- og dimensjonsdesign, arbeidsflyt og attestasjonsrutiner
- prosess- og automatiseringsrådgivning, herunder valg av moduler og integrasjoner
- opplæring av Kundens ansatte og superbrukere
- struktur- og styringsrådgivning, herunder rapporteringsmodeller og nøkkeltall
- prosjektbistand ved migrering fra tidligere system

Agaas har regnskapsfaglig kompetanse knyttet til **Plattformens faglige kvalitet**, herunder kontoplan, avgiftskoder, valideringsregler og oppdatering ved regelverksendringer. Denne kompetansen benyttes til produkt, opplæring og generell rådgivning, og innebærer ikke at Agaas påtar seg oppdragsansvar for Kundens regnskapsføring.

**Ikke omfattet:** utarbeidelse eller innsending av Kundens pliktige regnskapsrapportering, regnskapsfaglige konklusjoner Kunden kan legge til grunn uten egen kontroll, skatterettslig eller juridisk rådgivning, og enhver form for attestasjon.

## A.4 Grensesnittet mellom Plattform og regnskapsføringstjeneste

| Aktivitet | Agaas AS | Regnskapsforetaket | Kunden |
|---|---|---|---|
| Stille funksjonalitet til rådighet | Utfører | – | – |
| Registrere og kontere bilag | – | Utfører (ved oppdrag) | Utfører (ved egenregi) |
| Avstemme bank og reskontro | – | Utfører (ved oppdrag) | Utfører (ved egenregi) |
| Utarbeide pliktig rapportering | **Nei** | Utfører (ved oppdrag) | Ansvarlig |
| Avgi signatur ved innsending | **Nei** (formidler teknisk) | **Nei**, jf. Vedlegg F | **Utfører** |
| Oppbevare regnskapsmateriale | Tilrettelegger | Bistår | Ansvarlig |

## A.5 Systemkrav og forutsetninger

Plattformen leveres som skytjeneste og krever oppdatert nettleser og stabil internettforbindelse. Data lagres innenfor EØS, jf. Vedlegg C. Kunden er ansvarlig for eget utstyr, nettverk og lokal sikkerhet.
