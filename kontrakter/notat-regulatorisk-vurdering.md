# Notat – regulatoriske forutsetninger

**Til:** Agaas AS  
**Dato:** [dato]  
**Status:** Beslutningsgrunnlag. Må kvalitetssikres av advokat med konsesjonsrettslig kompetanse.

---

## 1. Valgt modell

Agaas AS selger regnskapssystem og regnskapsføring som én pakke. Regnskapsføringen utføres av Regnskapsagenten og av Agaas' medarbeidere, i Agaas AS.

**Agaas AS må derfor ha autorisasjon som regnskapsforetak og vil stå under Finanstilsynets tilsyn.** Dette er ikke en konsekvens av hvordan avtalen er formulert, men av hva virksomheten er.

Avtaleverket er skrevet ut fra denne forutsetningen.

## 2. Hvorfor det ikke finnes en vei utenom

Tre grep som ofte foreslås, virker ikke her:

| Grep | Hvorfor det ikke hjelper |
|---|---|
| **Næringskode bedriftsrådgivning** | Næringskoden er statistikk uten rettsvirkning for autorisasjonsplikt. Tilsynet vurderer den faktiske virksomheten |
| **Kunden signerer selv** | Autorisasjonsplikten knytter seg til å *utføre* kundens pliktige regnskapsrapportering, ikke til hvem som signerer. Styret signerer alltid årsregnskapet selv, og revisor trenger likevel godkjenning |
| **Arbeidet gjøres av en agent** | En programvareagent er ikke et rettssubjekt. Utfører agenten kundens bokføring, er det selskapet bak agenten som utfører den |

Signeringsmodellen beholdes likevel, jf. punkt 4. Den løser et annet og reelt problem.

## 3. Hva autorisasjonen krever

Kravene må verifiseres mot Finanstilsynets gjeldende rundskriv og søknadsskjema. I hovedtrekk:

| Krav | Status hos Agaas |
|---|---|
| Oppdragsansvarlig regnskapsfører med personlig autorisasjon | **På plass** – én person, ansvarlig for alle oppdrag |
| Tilstrekkelige ressurser og kontinuitet | Bør styrkes med stedfortreder, jf. eget notat punkt 6.3 |
| Egnethetskrav til ledelse og eiere | Må dokumenteres |
| Kvalitetsstyringssystem og rutiner for oppdragsutførelse | Under etablering, jf. eget notat |
| Skriftlig oppdragsavtale med hver kunde, med angitt omfang | Dekket av avtaleverket sammen med Pakkebekreftelsen, jf. Vedlegg D og H |
| Rutiner etter hvitvaskingsloven, med kundetiltak | Må etableres, jf. Vedlegg I |
| Sikkerhetsstillelse og ansvarsforsikring | Må etableres |
| Dokumentasjon av oppdragsutførelsen | Logging på plass; må kunne fremlegges som rapport, jf. eget notat |
| Tilsynsavgift og rapportering | Løpende |

Mye av dette er formalisering av rutiner virksomheten trenger uansett. Det tyngste nybygget er kvalitetsstyringssystemet.

## 4. Automatisering under autorisasjon

Autorisasjonen fjerner spørsmålet om Agaas *kan* føre regnskap. Den skjerper spørsmålet om *hvordan*.

Agaas er faglig ansvarlig for alt arbeid, uavhengig av om det er utført maskinelt eller av en medarbeider. God regnskapsføringsskikk gjelder fullt ut for maskinelt utført arbeid. Det innebærer i praksis:

| Krav | Hvordan det løses |
|---|---|
| Kontroll med agentens arbeid | Stikkprøver og terskelbaserte kontroller, jf. Vedlegg H.5 |
| Håndtering av det agenten ikke kan avgjøre | Eskalering til medarbeider og Oppdragsansvarlig |
| Sporbarhet per postering | Grunnlag, anvendt regel, mandatversjon, tidspunkt, godkjenner — sikret med kvalifisert tidsstempel |
| Dokumentasjon av oppdragsutførelsen | Loggene utgjør oppdragsdokumentasjonen |
| Kundens innsyn | Kunden kan se hvordan enhver postering er fremkommet |

Signeringsmodellen består fordi den plasserer ansvaret for innholdet overfor myndighetene hos kunden, der det hører hjemme, og holder Agaas unna å opptre overfor Skatteetaten på kundens vegne. Den begrenser ikke Agaas' ansvar overfor kunden for utførelsen.

**Merk:** sporbarhet og dokumentasjon er ikke bare et tilsynskrav. Det er også Agaas' eget bevis for forsvarlig utførelse dersom en kunde reklamerer.

Sporbarhet med kvalifisert tidsstempling, mandatdokumenter og løpende tilsyn er på plass i Plattformen. Den kvalifiserte tidsstemplingen gir presumsjon for tidspunkt og integritet, og er et sterkere utgangspunkt enn de fleste regnskapsforetak har. Gjenstående arbeid — versjonering av mandatet, binding mellom postering og versjon, endringskontroll ved trening, og fremleggbar oppdragsdokumentasjon — er behandlet i [`notat-kvalitetsstyring-regnskapsagent.md`](notat-kvalitetsstyring-regnskapsagent.md).

## 5. Øvrige regelverk

### 5.1 Inkasso
Inndrivelse av forfalte krav for andre krever bevilling. Agaas driver ikke inndrivelse, men overfører saksdata teknisk til inkassoforetak på kundens initiativ.

Grenser Agaas må holde: ingen kommunikasjon med skyldner i eget navn, ingen vurdering av kravets berettigelse, ingen mottak av innbetaling på kravene, og regelstyrt overføring må være kundens egen konfigurasjon som kunden kan se og slå av. Vederlag fra inkassoforetaket bør være systemvederlag, ikke andel av inkassosalær.

**Konflikt med prislisten.** Prislisten angir at renter og gebyrer fra skyldner tilfaller Agaas, for inkassovarsel, betalingsoppfølging og inkasso. Dette må avklares før modellen tas i bruk:

| Forhold | Vurdering |
|---|---|
| Hvem eier renter og gebyrer? | Forsinkelsesrenter og purregebyrer tilhører som utgangspunkt **kreditor**, altså kunden. Overføring til Agaas krever uttrykkelig avtale, og har regnskaps- og skattemessige konsekvenser for kunden |
| Purregebyrenes størrelse | Inkassoloven med forskrift setter grenser for hva som kan kreves av skyldner før inkasso, og for antall purringer |
| Bevillingsspørsmålet | At Agaas mottar vederlag **fra skyldner** for oppfølging av andres forfalte krav, er den økonomiske kjernen i det inkassoloven regulerer. Dette er den sentrale risikoen |
| Motstrid i avtaleverket | Kundeavtalen punkt 3.5 bokstav a og Vedlegg G forutsetter at Agaas ikke driver inndrivelse og ikke har andel i inkassoinntekter |

**Enten justeres inntektsmodellen, eller så må avtaleverket og den regulatoriske posisjonen skrives om.** De to kan ikke stå ved siden av hverandre. Dette bør høyt på listen til advokaten.

### 5.2 Bank og betaling
Kontoinformasjons- og betalingsinitieringstjenester er konsesjonspliktige, og det å opptre som agent for et betalingsforetak krever registrering. Bruk konsesjonspliktig tilbyder der kunden er samtykkegiver og betaling frigis hos banken. **Avklar med tilbyderen om deres modell gjør Agaas til agent.**

### 5.3 Revisors uavhengighet

Agaas fører kundens regnskap. Revisor kan derfor ikke være tilknyttet Agaas eller Agaas-gruppen.

**Konflikt med prislisten.** Prislisten inneholder posten «Agaas Revisjon». Tilbys revisjon fra gruppen, kan den ikke selges til kunder som samtidig har regnskapsføring hos Agaas — det er selvrevisjon, og rammes av uavhengighetskravene i revisorloven.

| Mulig håndtering | Merknad |
|---|---|
| Revisjon tilbys kun til kunder uten regnskapsføring hos Agaas | Krever sperre i salgs- og onboardingflyten, ikke bare en instruks |
| Revisjon legges utenfor gruppen | Ryddigst, men da er det ikke Agaas' tjeneste |
| Revisjon utgår | Enklest |

Sperren må være teknisk. En kunde som kjøper begge deler i onboardingen, skaper et uavhengighetsbrudd i det øyeblikket bestillingen registreres.

### 5.3b Agaas Invest

Prislisten nevner «Agaas Invest» som egen tjeneste. Avhengig av innholdet kan investeringsrådgivning og formidling av finansielle instrumenter være konsesjonspliktig. Innholdet må beskrives før det vurderes.

### 5.4 Bokføringsloven

Plattformen må understøtte sporbarhet, ingen sletting av bokførte data, oppbevaring i lovpålagt periode og tilgjengelighet for kontroll. Bør verifiseres teknisk mot bokføringsforskriftens krav til elektronisk oppbevaring.

**Oppbevaringssted må avklares særskilt.** Regnskapsmaterialet lagres hos Hetzner i Tyskland. Bokføringsloven har egne regler om hvor oppbevaringspliktig regnskapsmateriale kan oppbevares, med særskilte vilkår for oppbevaring i utlandet — typisk knyttet til at materialet er elektronisk tilgjengelig i lesbar form fra Norge for kontrollmyndighetene i hele oppbevaringsperioden, og i enkelte tilfeller til melde- eller dokumentasjonsplikt.

| Å avklare | Merknad |
|---|---|
| Er elektronisk oppbevaring i Tyskland tillatt uten dispensasjon? | Reglene har vært endret over tid; gjeldende ordlyd må sjekkes |
| Kreves melding eller dokumentasjon til Skatteetaten? | Bør avklares før første kunde |
| Er tilgjengelighetskravet oppfylt? | Materialet må kunne fremvises i lesbar form fra Norge, også etter avtalens opphør |
| Gjelder noe særskilt for sikkerhetskopier? | Kopiers lagringssted omfattes normalt av samme regler |

Dette er et konkret og etterprøvbart punkt som en kontroll vil se på, og det bør avklares av advokat eller direkte med Skatteetaten. Valget av tysk leverandør er i seg selv uproblematisk personvernrettslig — spørsmålet er bokføringsrettslig.

## 6. Sjekkliste

| # | Tiltak | Ansvar | Status |
|---|---|---|---|
| 1 | Advokatgjennomgang av avtaleverk og struktur | Ledelsen | ☐ |
| 2 | Søke autorisasjon som regnskapsforetak | Ledelsen | ☐ |
| 3 | Utpeke oppdragsansvarlig og dokumentere egnethet | Ledelsen | ☐ |
| 3b | Etablere stedfortrederavtale og kontinuitetsplan for oppdragsansvarlig | Ledelsen | ☐ |
| 3c | Etablere ordning for ekstern kvalitetskontroll | Fagansvarlig | ☐ |
| 4 | Etablere kvalitetsstyringssystem, inkludert kontroll av Regnskapsagenten | Fagansvarlig | ☐ |
| 5 | Etablere sikkerhetsstillelse og ansvarsforsikring | Økonomi | ☐ |
| 6 | Etablere hvitvaskingsrutiner og kundetiltak i onboarding | Fagansvarlig | ☐ |
| 7 | Versjonere agentens mandat og binde posteringer til versjon, jf. [`notat-kvalitetsstyring-regnskapsagent.md`](notat-kvalitetsstyring-regnskapsagent.md) | Teknologi | ☐ |
| 8 | Verifisere at Altinn-roller følger Vedlegg F, uten signeringsrett | Teknologi | ☐ |
| 9 | Avklare vederlagsmodell mot inkassoforetaket | Økonomi | ☐ |
| 10 | Avklare med bankintegrasjonstilbyder om Agaas blir agent | Teknologi | ☐ |
| 11 | Etablere databehandleravtaler med alle underdatabehandlere | Personvernansvarlig | ☐ |
| 12 | Teknisk verifikasjon mot bokføringsforskriften | Teknologi | ☐ |
| 13 | Avklare oppbevaringssted i utlandet mot bokføringsloven, jf. punkt 5.4 | Ledelsen/advokat | ☐ |
| 14 | Signere databehandleravtale med Hetzner og låse datasenterregion til Tyskland | Teknologi | ☐ |
| 15 | Sikre at onboardingflyten genererer Pakkebekreftelse som fastsetter leveranseomfanget | Produkt | ☐ |
| 16 | **Avklare inntektsmodellen for renter og gebyrer fra skyldner, jf. punkt 5.1** | Advokat | ☐ |
| 17 | Avklare Agaas Revisjon mot uavhengighetskravene, med teknisk sperre, jf. punkt 5.3 | Ledelsen | ☐ |
| 18 | Beskrive innholdet i Agaas Invest og vurdere konsesjonsplikt | Ledelsen | ☐ |
| 19 | Definere «fair use» for Oskar som en målbar grense | Produkt | ☐ |

**Merk rekkefølgen:** punkt 2 tar tid. Søknadsprosessen bør startes tidlig, og punktene 3 til 6 er i praksis forutsetninger for at søknaden skal kunne innvilges.

---

> Notatet er strukturert beslutningsgrunnlag, ikke juridisk rådgivning. Konkrete lovhenvisninger, terskler og Finanstilsynets gjeldende praksis må verifiseres av advokat.
