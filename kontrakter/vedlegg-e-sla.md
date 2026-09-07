# Vedlegg E – Servicenivå (SLA)

## E.1 Tilgjengelighet

| Måltall | Nivå |
|---|---|
| Garantert tilgjengelighet per kalendermåned | **99,5 %** |
| Måleperiode | Kalendermåned, døgnkontinuerlig |
| Måling | Agaas' overvåkning, tilgjengelig for Kunden på forespørsel |

Fra tilgjengelighetsberegningen holdes utenfor: planlagt vedlikehold varslet etter punkt E.4, nedetid hos tredjepart eller offentlig grensesnitt, force majeure, og nedetid forårsaket av Kundens egne forhold.

## E.2 Support

| Kanal | Åpningstid |
|---|---|
| Sak i Plattformen og e-post | Hverdager 08:00–16:00 |
| Telefon | Hverdager 09:00–15:00 |
| Kritiske hendelser | Døgnkontinuerlig varslingskanal |

## E.3 Prioritering og responstid

| Prioritet | Definisjon | Responstid | Mål for løsning eller omgåelse |
|---|---|---|---|
| P1 – Kritisk | Plattformen utilgjengelig, eller innsending eller lønnskjøring er blokkert nær frist | 1 time i åpningstid | 4 timer |
| P2 – Alvorlig | Sentral funksjon feiler uten praktisk omgåelse | 4 timer | 2 virkedager |
| P3 – Normal | Feil med praktisk omgåelse | 1 virkedag | Neste ordinære utgivelse |
| P4 – Lav | Kosmetisk feil, ønske om endring | 3 virkedager | Vurderes i produktplan |

## E.4 Vedlikehold

Planlagt vedlikehold legges fortrinnsvis til hverdager mellom 22:00 og 06:00 eller i helg, og varsles minst fem virkedager i forveien. Hastevedlikehold av sikkerhetshensyn kan gjennomføres uten forhåndsvarsel, med varsel så snart som mulig.

I periodene 1.–15. i månedene med mva-frist, samt siste og første to virkedager i hver måned, unngås planlagt vedlikehold i åpningstiden.

## E.5 Sikkerhetskopiering og gjenoppretting

| Måltall | Nivå |
|---|---|
| Sikkerhetskopiering | Minst daglig, med kontinuerlig transaksjonslogg |
| Maksimalt datatap (RPO) | 1 time |
| Maksimal gjenopprettingstid (RTO) | 8 timer |
| Oppbevaring av kopier | Minst 90 dager |
| Test av gjenoppretting | Minst årlig, dokumentert |

## E.6 Prisavslag ved brudd på tilgjengelighet

| Faktisk tilgjengelighet i måneden | Prisavslag av månedsvederlaget |
|---|---|
| 99,5 % – 99,0 % | 5 % |
| Under 99,0 % – 97,0 % | 10 % |
| Under 97,0 % – 95,0 % | 20 % |
| Under 95,0 % | 30 % |

Prisavslag krever skriftlig krav innen 30 dager etter månedens utløp og godskrives på neste faktura. Ligger tilgjengeligheten under 95 % i tre sammenhengende måneder, kan Kunden si opp Avtalen med 30 dagers varsel uten kostnad.
