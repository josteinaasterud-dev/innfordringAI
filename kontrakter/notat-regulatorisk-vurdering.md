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
| Oppdragsansvarlig regnskapsfører med personlig autorisasjon | **På plass** – fagansvarlig i selskapet |
| Egnethetskrav til ledelse og eiere | Må dokumenteres |
| Kvalitetsstyringssystem og rutiner for oppdragsutførelse | Under etablering, jf. eget notat |
| Skriftlig oppdragsavtale med hver kunde | Dekket av avtaleverket, jf. Vedlegg H |
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
| Sporbarhet per postering | Grunnlag, anvendt regel, tidspunkt, godkjenner |
| Dokumentasjon av oppdragsutførelsen | Loggene utgjør oppdragsdokumentasjonen |
| Kundens innsyn | Kunden kan se hvordan enhver postering er fremkommet |

Signeringsmodellen består fordi den plasserer ansvaret for innholdet overfor myndighetene hos kunden, der det hører hjemme, og holder Agaas unna å opptre overfor Skatteetaten på kundens vegne. Den begrenser ikke Agaas' ansvar overfor kunden for utførelsen.

**Merk:** sporbarhet og dokumentasjon er ikke bare et tilsynskrav. Det er også Agaas' eget bevis for forsvarlig utførelse dersom en kunde reklamerer.

Sporbarhet, mandatdokumenter og løpende tilsyn er på plass i Plattformen. Gjenstående arbeid — versjonering av mandatet, binding mellom postering og versjon, endringskontroll ved trening, og fremleggbar oppdragsdokumentasjon — er behandlet i [`notat-kvalitetsstyring-regnskapsagent.md`](notat-kvalitetsstyring-regnskapsagent.md).

## 5. Øvrige regelverk

### 5.1 Inkasso
Inndrivelse av forfalte krav for andre krever bevilling. Agaas driver ikke inndrivelse, men overfører saksdata teknisk til inkassoforetak på kundens initiativ.

Grenser Agaas må holde: ingen kommunikasjon med skyldner i eget navn, ingen vurdering av kravets berettigelse, ingen mottak av innbetaling på kravene, og regelstyrt overføring må være kundens egen konfigurasjon som kunden kan se og slå av. Vederlag fra inkassoforetaket bør være systemvederlag, ikke andel av inkassosalær. **Bør avklares særskilt.**

### 5.2 Bank og betaling
Kontoinformasjons- og betalingsinitieringstjenester er konsesjonspliktige, og det å opptre som agent for et betalingsforetak krever registrering. Bruk konsesjonspliktig tilbyder der kunden er samtykkegiver og betaling frigis hos banken. **Avklar med tilbyderen om deres modell gjør Agaas til agent.**

### 5.3 Revisors uavhengighet
Agaas fører kundens regnskap. Revisor kan derfor ikke være tilknyttet Agaas eller Agaas-gruppen. Skulle gruppen vurdere å eie revisjonsvirksomhet, må dette avklares grundig først.

### 5.4 Bokføringsloven
Plattformen må understøtte sporbarhet, ingen sletting av bokførte data, oppbevaring i lovpålagt periode og tilgjengelighet for kontroll. Bør verifiseres teknisk mot bokføringsforskriftens krav til elektronisk oppbevaring.

## 6. Sjekkliste

| # | Tiltak | Ansvar | Status |
|---|---|---|---|
| 1 | Advokatgjennomgang av avtaleverk og struktur | Ledelsen | ☐ |
| 2 | Søke autorisasjon som regnskapsforetak | Ledelsen | ☐ |
| 3 | Utpeke oppdragsansvarlig og dokumentere egnethet | Ledelsen | ☐ |
| 4 | Etablere kvalitetsstyringssystem, inkludert kontroll av Regnskapsagenten | Fagansvarlig | ☐ |
| 5 | Etablere sikkerhetsstillelse og ansvarsforsikring | Økonomi | ☐ |
| 6 | Etablere hvitvaskingsrutiner og kundetiltak i onboarding | Fagansvarlig | ☐ |
| 7 | Versjonere agentens mandat og binde posteringer til versjon, jf. [`notat-kvalitetsstyring-regnskapsagent.md`](notat-kvalitetsstyring-regnskapsagent.md) | Teknologi | ☐ |
| 8 | Verifisere at Altinn-roller følger Vedlegg F, uten signeringsrett | Teknologi | ☐ |
| 9 | Avklare vederlagsmodell mot inkassoforetaket | Økonomi | ☐ |
| 10 | Avklare med bankintegrasjonstilbyder om Agaas blir agent | Teknologi | ☐ |
| 11 | Etablere databehandleravtaler med alle underdatabehandlere | Personvernansvarlig | ☐ |
| 12 | Teknisk verifikasjon mot bokføringsforskriften | Teknologi | ☐ |

**Merk rekkefølgen:** punkt 2 tar tid. Søknadsprosessen bør startes tidlig, og punktene 3 til 6 er i praksis forutsetninger for at søknaden skal kunne innvilges.

---

> Notatet er strukturert beslutningsgrunnlag, ikke juridisk rådgivning. Konkrete lovhenvisninger, terskler og Finanstilsynets gjeldende praksis må verifiseres av advokat.
