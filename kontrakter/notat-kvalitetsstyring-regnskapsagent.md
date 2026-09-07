# Notat – kvalitetsstyring for Regnskapsagenten

**Formål:** Koble Agaas' eksisterende logging, mandatdokumenter og tilsyn med Oskar til kravene som følger av autorisasjonen. Dokumentet er ment som grunnlag for kvalitetsstyringssystemet og som vedlegg til autorisasjonssøknaden.

---

## 1. Utgangspunkt

Agaas har allerede på plass:

- **Sporbarhet** – alt logges i Agaas' database, med kvalifisert tidsstempling (QTSA) via Signicat
- **Mandatdokumenter** – egne dokumenter som definerer området Oskar tar avgjørelser innenfor
- **Løpende trening** av Oskar, utført av autoriserte regnskapsførere
- **Menneskelig godkjenning** – saker Oskar er usikker på, flagges og avgjøres av autorisert regnskapsfører
- **Løpende tilsyn** med Oskar

Dette dekker substansen i det som kreves. Punktene under er oversettelsen til regulatoriske krav, og de stedene der teknisk god logging likevel pleier å komme til kort.

### 1.1 Hva den kvalifiserte tidsstemplingen gir

Et kvalifisert tidsstempel etter eIDAS har **presumsjon for riktigheten av tidspunktet og for integriteten til dataene det er knyttet til**. Det snur bevisbyrden: den som hevder at en postering er endret i ettertid, må bevise det — Agaas må ikke bevise det motsatte.

Praktisk betyr det:

| Situasjon | Uten QTSA | Med QTSA |
|---|---|---|
| Kunde hevder postering er endret i ettertid | Agaas' egen logg mot kundens påstand | Presumsjon for Agaas' versjon |
| Tilsyn ber om dokumentasjon på når noe ble gjort | Intern tidsangivelse | Kvalifisert bevis |
| Revisor kontrollerer at materialet ikke er manipulert | Tillit til systemet | Verifiserbart uavhengig av Agaas |
| Bokføringsforskriftens krav om sikring mot endring | Må argumenteres | Sterkt underbygget |

Dette er vesentlig bedre enn ren databaselogging, og det er verdt å fremheve i autorisasjonssøknaden.

Fire forhold må likevel være løst for at verdien skal være reell.

## 2. Fire forutsetninger for at tidsstemplingen holder

### 2.1 Omfang – hva stemples?

Tidsstemplet beviser det som er stemplet, og ingenting annet. Stemples posteringer, men ikke mandatversjon, kontrollresultat og eskaleringsbeslutninger, står de siste like usikret som før.

| Bør stemples | Hvorfor |
|---|---|
| Posteringer og bilag | Kjernen i regnskapsmaterialet |
| **Mandatdokumenter ved publisering** | Beviser hvilket mandat som gjaldt på en gitt dato, jf. punkt 4 |
| Modellversjoner ved produksjonssetting | Samme formål |
| Kontrollresultater og stikkprøver | Beviser at kontrollen faktisk ble utført da den sier |
| Eskaleringer og faglige avgjørelser | Beviser Oppdragsansvarliges befatning |
| Periodeavslutning og kundens godkjenning | Knytter ansvar til tidspunkt |

### 2.2 Fullstendighet – kan man bevise at ingenting mangler?

Dette er den vanligste svakheten. Stemples hver hendelse enkeltvis, bevises hver hendelse for seg — men **en hendelse som er fjernet, har heller ikke noe tidsstempel**. Fraværet er usynlig.

Løsningen er å kjede loggen: hver oppføring inneholder hash av den forrige, og roten av kjeden tidsstemples periodisk. Da kan man bevise at ingenting er fjernet mellom to stempler. Uten kjeding beviser man at det som er der er ekte, men ikke at det som er der er alt.

### 2.3 Levetid – tidsstempler forvitrer

Et kvalifisert tidsstempel har begrenset bevisverdi over tid: sertifikater utløper, og algoritmer svekkes. Regnskapsmateriale skal oppbevares i årevis.

Uten fornyelse vil stemplene på det eldste materialet — som ofte er det mest omstridte — være svakest. Løsningen er arkivtidsstempling: periodisk ny stempling av materialet med gjeldende algoritmer, før de gamle svekkes. Dette bør avklares konkret med Signicat, og settes opp som en driftsrutine med kalender, ikke som et engangstiltak.

### 2.4 Innhold – stempelet beviser eksistens, ikke forsvarlighet

Et tidsstempel beviser at posteringen forelå i denne formen på dette tidspunktet. Det sier ingenting om at posteringen var **faglig riktig**, at mandatet var forsvarlig, eller at kontrollen var tilstrekkelig.

Oppdragsdokumentasjon etter regnskapsførerloven krever innhold: hva ble vurdert, hvorfor, av hvem. Tidsstemplingen sikrer dokumentasjonen — den erstatter den ikke.

## 3. Logging er råmateriale – oppdragsdokumentasjon er et produkt

En database som logger alt, og oppdragsdokumentasjon etter regnskapsførerloven, er ikke det samme. Loggen er råmaterialet. Dokumentasjonen er det som kan **fremlegges**.

Testen er enkel: *kan Agaas, for en gitt kunde og en gitt periode, produsere en rapport som viser hva som er utført, hva som er kontrollert, hvilke avvik som oppsto og hvordan de ble løst — uten å skrive en spørring for anledningen?*

| Krav | Hva som må kunne fremlegges |
|---|---|
| Utført arbeid | Hvilke oppgaver er gjort, når, av agent eller medarbeider |
| Kontroller | Hvilke stikkprøver og terskelkontroller er kjørt, med resultat |
| Avvik | Hva ble eskalert, til hvem, hvordan avgjort, av hvem |
| Faglige vurderinger | Grunnlaget for skjønnsmessige valg |
| Oppdragsansvarliges befatning | Hva Oppdragsansvarlig har gjennomgått og godkjent |

**Anbefaling:** bygg et rapportuttrekk «oppdragsdokumentasjon per kunde per periode» som genereres av loggen. Det er en dags arbeid nå og en uke i panikk senere.

## 4. Mandatet må versjoneres, og posteringen må peke på versjonen

Dette er det viktigste tekniske punktet i notatet.

Mandatdokumentene som definerer Oskars beslutningsområde er en del av kvalitetsstyringssystemet. Når Oskar trenes løpende, endres den faktiske beslutningsatferden over tid. Da oppstår spørsmålet:

> En postering fra mars blir bestridt under revisjonen i mai året etter. Kan Agaas rekonstruere hvilke regler og hvilket mandat som gjaldt **i mars**?

Logges bare utfallet, og ikke hvilken versjon av mandat og modell som produserte det, kan Agaas dokumentere *hva* som ble gjort, men ikke *hvorfor det var forsvarlig på det tidspunktet*. Det er den siste halvdelen et tilsyn og en revisor spør etter.

**Her ligger den største gevinsten ved QTSA-oppsettet.** Tidsstemples hver mandatversjon ved publisering, kan Agaas bevise — med presumsjonsvirkning — nøyaktig hvilket mandat som var i kraft da posteringen ble gjort. Rekonstruksjonsproblemet går fra å være en påstand fra Agaas til å være et verifiserbart faktum. Det er en sterkere posisjon enn de fleste regnskapsforetak har for manuelt arbeid.

| Krav | Konkret |
|---|---|
| Versjonering | Hvert mandatdokument og hver modellversjon har entydig versjonsnummer og ikrafttredelsesdato |
| Binding | Hver postering logger hvilken mandat- og modellversjon som var i kraft |
| Historikk | Tidligere versjoner oppbevares like lenge som oppdragsdokumentasjonen |
| Stempling | Hver mandatversjon tidsstemples ved publisering |
| Rekonstruksjon | Det skal være mulig å hente frem mandatet slik det lød på en gitt dato |

## 5. Endringskontroll ved trening

Løpende trening er en styrke faglig, men det er også en løpende endring i hvordan kundens regnskap føres. Det krever en port, ikke bare et tilsyn.

| Spørsmål | Må være besvart i rutinen |
|---|---|
| Hvem godkjenner at en ny versjon settes i produksjon på kundeoppdrag? | Bør være Oppdragsansvarlig for faglig relevante endringer |
| Hva testes før produksjonssetting? | Regresjonstest mot historiske saker med kjent riktig behandling |
| Hva skjer ved utvidelse av mandatet? | Egen vurdering og godkjenning — utvidet beslutningsområde er en faglig beslutning, ikke en produktbeslutning |
| Kan en versjon rulles tilbake? | Ja, og tilbakerullingen skal logges |
| Varsles kunden? | Ved vesentlige endringer i hvordan kundens regnskap behandles |

**Skillet som er lett å overse:** tilsyn med *utfall* (stikkprøver på posteringer) og kontroll med *endringer* (godkjenning før ny versjon settes i drift) er to forskjellige kontroller. Begge kreves. Stikkprøver fanger opp feil i etterkant; endringskontroll hindrer at en hel måned føres feil før noen oppdager det.

## 6. Menneskelig kontroll og kalibrering

Modellen er at Oskar flagger det han er usikker på, og at en autorisert regnskapsfører avgjør de flaggede sakene. Det er riktig konstruksjon: det profesjonelle skjønnet utøves av en autorisert person, og avgjørelsen kan tilbakeføres til hvem og hvorfor.

To forhold avgjør om kontrollen holder over tid.

### 6.1 Det farlige er ikke usikkerhet – det er feil selvtillit

Kontrollen fanger opp det Oskar **vet** at han er usikker på. Den fanger ikke opp det Oskar tar feil om uten å være usikker. Er kalibreringen skjev, passerer nettopp de sakene stille.

Konsekvensen er at kontrollen ikke kan måles ved å se på de flaggede sakene alene:

| Populasjon | Hva gjennomgang av den viser |
|---|---|
| Flaggede saker | At eskaleringen virker når den utløses |
| **Ikke-flaggede saker** | **Om eskaleringen utløses når den burde** |

**Anbefaling:** trekk et tilfeldig utvalg av saker Oskar har behandlet med høy sikkerhet, og la en autorisert regnskapsfører vurdere dem uten å vite at de er automatisk godkjent. Andelen feil i dette utvalget er den egentlige feilraten. Den er samtidig det beste beviset overfor Finanstilsynet på at kontrollen fungerer — «vi kontrollerer alt som flagges» er en beskrivelse av rutinen, mens en målt feilrate i den ukontrollerte populasjonen er dokumentasjon av at den virker.

Utvalget må ha en nedre grense som ikke faller bort etter hvert som Oskar blir bedre. Blir kontrollvolumet en andel av det flaggede, svekkes tilsynet nøyaktig når systemet håndterer mest.

### 6.2 Godkjenninger som treningsdata

Brukes regnskapsførerens godkjenninger til å trene Oskar, oppstår en tilbakekobling som må håndteres:

| Risiko | Tiltak |
|---|---|
| En feil godkjenning læres og gjentas i skala | Ikke tren på godkjenninger som ikke er reelt vurdert |
| Godkjenningstretthet ved høyt volum | Logg behandlingstid; svært raske godkjenninger merkes og holdes utenfor treningsgrunnlaget |
| Flaggraten synker, og mennesket ser stadig færre saker | Fast minstevolum til gjennomgang, uavhengig av flaggrate |
| Skjevhet fra én regnskapsfører forplanter seg | Periodisk validering av et utvalg godkjenninger ved en annen autorisert regnskapsfører |
| Oskar er trygg på gammel fordeling, men møter ny | Flaggraten heves ved ny kunde, ny bransje, ny bilagstype og ved regelverksendringer |

Skillet mellom «godkjent» og «godkjent etter reell vurdering» bør være eksplisitt i datamodellen. Det er den distinksjonen som avgjør om treningsgrunnlaget er godt.

### 6.3 Oppdragsansvar er per oppdrag

En generell godkjenning gitt under trening er ikke det samme som oppdragsansvar. Ansvaret etter regnskapsførerloven ligger hos Oppdragsansvarlig for det enkelte oppdraget.

Godkjenner regnskapsfører A en sakstype under trening, og atferden anvendes senere på kunde B der regnskapsfører C er oppdragsansvarlig, er ikke C sitt ansvar oppfylt ved A sin godkjenning. Oppdragsansvarlig må ha innsyn i hva Oskar gjør på **sine** oppdrag, og mulighet til å sette strengere rammer for dem.

**Anbefaling:** skill i loggen mellom generell godkjenning under trening og godkjenning i et konkret oppdrag, og gi Oppdragsansvarlig en oversikt per oppdrag over hva som er behandlet automatisk, hva som er flagget, og hva som er avgjort av hvem.

### 6.4 Kontrollparametere

«Under oppsikt» må kunne tallfestes for å kunne dokumenteres:

| Parameter | Fastsettes til |
|---|---|
| Andel ikke-flaggede saker som stikkprøvekontrolleres | [__] %, minimum [__] saker per periode |
| Målt feilrate i ikke-flagget populasjon | [__] %, med terskel for tiltak ved [__] % |
| Beløpsgrense for obligatorisk manuell kontroll | [_____] kroner |
| Kategorier som alltid flagges | [nye leverandører, avvikende mva-behandling, transaksjoner med nærstående, ny kunde de første [__] periodene] |
| Kontrollfrekvens | [løpende / ukentlig / ved periodeavslutning] |
| Hvem godkjenner flaggede saker | Autorisert regnskapsfører |
| Terskel for eskalering til Oppdragsansvarlig | [kriterium] |
| Oppfølging ved funn | [rutine] |

Tallene føres inn i Vedlegg H.5 i kundeavtalen, slik at kunden vet hva som faktisk kontrolleres.

Kontrollresultatene bør tidsstemples, jf. punkt 2.1 — ellers kan man vise *at* det kontrolleres, men ikke *når*.

## 7. Tre oppbevaringsregimer i én database

Logges alt samlet, blir sletting vanskelig — tre regelverk med ulike eiere, formål og frister møtes i samme datasett:

| Datatype | Regelverk | Eier | Sletting |
|---|---|---|---|
| Kundens regnskapsmateriale | Bokføringsloven | Kunden | Etter oppbevaringsplikten; skal utleveres ved opphør |
| Oppdragsdokumentasjon | Regnskapsførerloven | Agaas | Etter lovpålagt periode |
| Kundetiltak | Hvitvaskingsloven | Agaas | Egen frist, jf. Vedlegg I |
| Driftslogger og telemetri | Ingen særskilt plikt | Agaas | Bør slettes etter kort tid |

**Anbefaling:** merk data med regime ved skriving, ikke ved sletting. Uten det blir en sletteanmodning etter personvernforordningen, en utleveringsplikt etter bokføringsloven og en oppbevaringsplikt etter hvitvaskingsloven vanskelig å håndtere samtidig — og de vil før eller siden treffe samme kunde.

## 8. Sjekkliste

| # | Punkt | Status |
|---|---|---|
| 1 | Mandatdokumenter er versjonert med ikrafttredelsesdato | ☐ |
| 1b | Mandatversjoner tidsstemples ved publisering | ☐ |
| 1c | Loggen er hash-kjedet og roten stemples periodisk | ☐ |
| 1d | Rutine for arkivtidsstempling er avtalt med Signicat og satt i kalender | ☐ |
| 1e | Bekreftet at tjenesten som brukes faktisk har kvalifisert status | ☐ |
| 2 | Hver postering logger gjeldende mandat- og modellversjon | ☐ |
| 3 | Tidligere versjoner kan hentes frem for en gitt dato | ☐ |
| 4 | Godkjenningsrutine før ny versjon settes i produksjon | ☐ |
| 5 | Regresjonstest mot historiske saker inngår i rutinen | ☐ |
| 6 | Utvidelse av Oskars mandat krever faglig godkjenning | ☐ |
| 7 | Kontrollparametere i punkt 5 er tallfestet | ☐ |
| 8 | Rapportuttrekk «oppdragsdokumentasjon per kunde per periode» finnes | ☐ |
| 9 | Data er merket med oppbevaringsregime | ☐ |
| 10 | Oppdragsansvarliges befatning logges særskilt | ☐ |
| 11 | Stikkprøvekontroll av ikke-flaggede saker er etablert, med minstevolum | ☐ |
| 12 | Feilrate i ikke-flagget populasjon måles og rapporteres | ☐ |
| 13 | Behandlingstid per godkjenning logges; rask godkjenning holdes utenfor treningsgrunnlaget | ☐ |
| 14 | Flaggraten heves ved ny kunde, ny bransje og regelverksendringer | ☐ |
| 15 | Oppdragsansvarlig har oversikt per oppdrag over automatisk behandlede og flaggede saker | ☐ |

---

> Notatet er strukturert beslutningsgrunnlag, ikke juridisk rådgivning. Kravene til kvalitetsstyring og dokumentasjon må verifiseres mot regnskapsførerloven med forskrift, god regnskapsføringsskikk og Finanstilsynets gjeldende rundskriv.
