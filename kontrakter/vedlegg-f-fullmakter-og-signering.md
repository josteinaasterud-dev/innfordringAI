# Vedlegg F – Fullmakter, roller og signeringsrutine

Vedlegget gjennomfører hovedavtalens punkt 7. Formålet er at **enhver innsending til offentlig myndighet skjer under Kundens egen signatur**, og at ingen aktør i Agaas-gruppen har rettigheter som gjør noe annet mulig.

## F.1 Grunnprinsipp

Signeringen kan skje **i Plattformen** – Kunden behøver ikke logge seg inn i Altinn separat. Det avgjørende er ikke hvor signeringen utføres, men **hvem sin elektroniske identitet som benyttes**:

> Innsendingen skal skje under **Kundens egen elektroniske identitet**, utløst av en aktiv handling fra en person hos Kunden med gyldig signeringsrett. Plattformen er teknisk formidler av signaturen, ikke avgiver av den.

## F.2 Signeringsmodeller

| Modell | Slik virker den | Hvem signerer rettslig | Anvendes |
|---|---|---|---|
| **1. Ekstern signering** | Kunden går til Altinn og signerer der | Kunden | Ja |
| **2. Signering i Plattformen** | Kunden autentiserer seg med egen elektroniske ID i Plattformens signeringssteg, og innsendingen skjer under Kundens identitet | **Kunden** | **Ja – hovedmodell** |
| **3. Maskinell signering** | Innsending skjer på Agaas' virksomhetssertifikat eller systemautorisasjon, uten at Kunden signerer i det enkelte tilfellet | Agaas | **Nei**, jf. F.3 |

Modell 1 og 2 er likeverdige etter Avtalen. Modell 2 gir best brukeropplevelse og er den Plattformen tilbyr som standard.

## F.3 Avgrensning mot maskinell signering

Plattformen skal ikke innrettes slik at Agaas signerer eller sender inn på Kundens vegne uten Kundens signeringshandling i den enkelte sak. Konkret:

- Agaas skal ikke tildeles Altinn-roller som gir selvstendig signeringsrett, jf. F.4.
- Teknisk systemautorisasjon, herunder Maskinporten-integrasjon, benyttes kun til **oppslag, henting og innlevering av grunnlagsdata**, ikke til å avgi Kundens signatur.
- Der en etat tilbyr innsending under systemautorisasjon, kan dette bare tas i bruk dersom autorisasjonen er etablert av Kunden i Kundens eget navn, er avgrenset til angitte formål, kan trekkes tilbake av Kunden når som helst, og den enkelte innsending utløses av Kundens godkjenning. Bruk av slik funksjonalitet krever egen skriftlig avtale mellom partene.

Bakgrunnen er at det er Kunden som er rapporteringspliktig overfor myndighetene. At Agaas utarbeider rapporteringen som Kundens regnskapsfører, endrer ikke hvem som avgir den. Dette begrenser ikke Agaas' ansvar overfor Kunden for utførelsen, jf. hovedavtalen punkt 19.

## F.4 Rollematrise – Altinn

| Altinn-rolle | Gir adgang til | Tildeles Agaas? | Begrunnelse |
|---|---|---|---|
| Begrenset signeringsrettighet | Signere utvalgte skjema | **Nei** | Ville gitt Agaas signeringsadgang |
| Kontaktperson / Daglig leder | Bred myndighet | **Nei** | Utenfor leveransen |
| Regnskapsfører med signeringsrettighet | Signere og sende inn | **Nei** | Forbeholdt Kunden selv |
| Regnskapsfører uten signeringsrettighet | Utfylling og innsyn | Ja, som Kundens regnskapsforetak | Nødvendig for oppdragsutførelse |
| Revisorattesterer | Attestasjon | **Nei** | Forbeholdt Kundens revisor |
| Tilgangsstyring | Delegere roller videre | **Nei** | Skal ligge hos Kunden |
| Maskinporten-tilgang til datauttrekk | Oppslag i angitte datasett | Ja, avgrenset per formål | Nødvendig for integrasjon, jf. F.3 |

**Kunden gjennomgår rollematrisen ved oppstart og bekrefter tildelingen.** Agaas skal avvise rolletildelinger som går ut over tabellen, og skal be Kunden trekke slike tilbake.

## F.5 Signeringsflyt i Plattformen (modell 2)

| Steg | Handling | Utført av | Sporing |
|---|---|---|---|
| 1 | Grunnlag genereres og valideres | Plattformen | Systemlogg |
| 2 | Faglig kontroll og klargjøring | Agaas | Oppdragsdokumentasjon |
| 3 | Kundens gjennomgang, status «Klar til signering» | Kunden | Godkjenningslogg med bruker og tidspunkt |
| 4 | **Kunden autentiserer seg med egen elektroniske ID og signerer** | **Kunden** | Signaturbevis med person, tidspunkt og autentiseringsnivå |
| 5 | Innsending og henting av kvittering | Plattformen, under Kundens identitet | Kvittering fra etaten, arkivert |

Steg 4 kan ikke omgås, forhåndsutføres eller utføres av Agaas.

## F.6 Skatteetaten og øvrige etater

Samme prinsipp gjelder for mva-melding, skattemelding, næringsspesifikasjon, a-melding, aksjonærregisteroppgave og annen rapportering, uavhengig av om signeringen skjer i Plattformen eller hos etaten, jf. F.2.

## F.7 Bank og betaling

| Handling | Utført av |
|---|---|
| Etablere samtykke til kontoinformasjon | Kunden, med egen BankID hos konsesjonspliktig tilbyder |
| Hente transaksjoner og saldo | Plattformen, innenfor Kundens samtykke |
| Lage betalingsforslag | Plattformen |
| Godkjenne og frigi betaling | **Kunden, i banken eller hos tilbyderen** |
| Trekke tilbake samtykke | Kunden, når som helst |

Agaas har ikke disposisjonsrett over Kundens konti og kan ikke gjennomføre betalinger.

## F.8 Dokumentasjon og etterprøvbarhet

Agaas skal kunne dokumentere, for hver innsending: hvem som godkjente, hvem som signerte, tidspunkt, autentiseringsnivå, og at signaturen ble avgitt under Kundens egen elektroniske identitet. Loggene oppbevares i minst fem år og gjøres tilgjengelige for Kunden, Kundens revisor og myndigheter på forespørsel.

## F.9 Kundens bekreftelse

Kunden bekrefter ved signering av hovedavtalen at Kunden:

- utpeker minst én person med gyldig signeringsrett som skal utføre innsending,
- sørger for at denne har gyldig elektronisk ID og nødvendig Altinn-rolle,
- har eget ansvar for frister, og
- ikke tildeler Agaas roller med signeringsrett, jf. F.4.

**Utpekt signeringsansvarlig hos Kunden:** ______________________  
**Stedfortreder:** ______________________
