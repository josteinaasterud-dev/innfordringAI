# Vedlegg C – Underdatabehandlere og tredjepartstjenester

Oppdatert: [dato]. Gjeldende versjon publiseres på [nettadresse]. Endringer varsles etter Vedlegg B punkt 6.

## C.1 Underdatabehandlere for Plattformen

| Leverandør | Tjeneste | Datakategorier | Behandlingssted |
|---|---|---|---|
| Hetzner Online GmbH | Skyinfrastruktur: drift, lagring, sikkerhetskopi | Alle Kundedata | Tyskland |
| [Aksesspunkt] | Utveksling av EHF-dokument | Faktura- og partsopplysninger | EØS |
| [Bankintegrasjonstilbyder] | Kontoinformasjon og transaksjoner | Kontonummer, transaksjoner, betalingsreferanser | EØS |
| [E-post/varsling] | Utsending av varsler og fakturaer | Navn, e-post, dokumentinnhold | EØS |
| [Support-/saksverktøy] | Brukerstøtte | Kontaktopplysninger, saksinnhold | EØS |
| [Bilagstolkning] | Maskinell tolkning av bilag | Bilagsinnhold | EØS |
| Signicat | Kvalifisert tidsstempling (QTSA) og elektronisk signering | Hashverdier av dokument og postering, signatarens identitetsopplysninger | EØS |

## C.2 Selvstendige behandlingsansvarlige

Følgende mottakere opptrer som **selvstendig behandlingsansvarlig** for egen behandling. Agaas' databehandleransvar opphører ved overføringspunktet, jf. hovedavtalen punkt 14.

Agaas er i tillegg selvstendig behandlingsansvarlig for egne lovpålagte plikter, herunder kundetiltak etter hvitvaskingsloven og oppdragsdokumentasjon etter regnskapsførerloven, jf. hovedavtalen punkt 14.2.

| Mottaker | Grunnlag for overføring | Utløses av |
|---|---|---|
| Skatteetaten, Altinn, Brønnøysundregistrene, SSB, NAV | Rettslig forpliktelse | Kundens egen innsending |
| Inkassoforetak | Kundens oppdragsavtale, Vedlegg G.1 | Kundens overføring av sak |
| Kundens bank | Kundens kundeforhold og samtykke | Kundens samtykke |
| Kundens revisor | Revisorloven | Kundens tilgangstildeling |

## C.1b Skyinfrastruktur

All drift og lagring skjer hos **Hetzner Online GmbH**, org.nr. [HRB _____], Gunzenhausen, Tyskland.

| Forhold | Beskrivelse |
|---|---|
| Rolle | Underdatabehandler for Agaas |
| Tjeneste | Skyinfrastruktur (IaaS): servere, lagring, nettverk, sikkerhetskopi |
| Behandlingssted | **Datasenter i Tyskland** – [Nürnberg / Falkenstein] |
| Jurisdiksjon | Tysk rett, EU-medlemsstat |
| Avtalegrunnlag | Databehandleravtale (Auftragsverarbeitungsvertrag) med Hetzner |
| Tredjeland | Hetzner tilbyr også datasentre utenfor EØS. Agaas skal låse ressursbruken til datasentre i Tyskland, og kontrollere dette ved oppsett av ny infrastruktur |
| Tilgang | Hetzner har ikke tilgang til innholdet i Kundedata utover det som følger av drift av infrastrukturen |

**Kontrollpunkt:** valg av datasenterregion er en teknisk innstilling som kan endres ved utrulling av ny infrastruktur. Agaas skal ha rutine som hindrer at ressurser opprettes utenfor EØS.

## C.2b Tillitstjenester

Agaas benytter kvalifisert tidsstemplingstjeneste fra Signicat for å sikre integriteten og tidfestingen av regnskapsmateriale og oppdragsdokumentasjon. Tjenesten leveres som kvalifisert tillitstjeneste etter eIDAS.

| Forhold | Beskrivelse |
|---|---|
| Tjeneste | Kvalifisert tidsstempling, samt elektronisk signering, jf. Vedlegg F |
| Hva som sendes | Som hovedregel kun hashverdier, ikke innholdet i bilag eller posteringer |
| Rettsvirkning | Presumsjon for tidspunktets riktighet og dataenes integritet |
| Verifikasjon | Stempler kan verifiseres uavhengig av Agaas |
| Arkivfornyelse | Periodisk ny stempling for å bevare bevisverdi i oppbevaringsperioden |

## C.3 Overføring ut av EØS

All behandling skjer innenfor EØS. Overføring ut av EØS skjer ikke uten at Kunden er varslet på forhånd og gyldig overføringsgrunnlag foreligger, som hovedregel EUs standard personvernbestemmelser med supplerende tiltak og dokumentert vurdering av mottakerlandet.

Se særskilt kontrollpunktet om datasenterregion i punkt C.1b.

## C.4 Endringslogg

| Dato | Endring | Varslet |
|---|---|---|
| [dato] | Første versjon | – |
