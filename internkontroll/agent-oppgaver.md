# Internkontroll — uppgifter för agenten

Kontrolluppgifter som agenten kör mot inkassosystemet. Listan är ett utgångspunkt; fyll på längst ned.

**Bolag:** Equity Credit Management AB (Sverige)
**System:** Banqsoft Lighthouse — Collect och Ledger

> Dokumentet är på svenska eftersom det gäller ett svenskt bolag och kan komma att visas för svensk tillsynsmyndighet och revisor. Säg till om ni hellre vill ha det på norska för internt bruk.

## Princip

Agenten är **läsande**. Den hittar avvikelser och rapporterar dem — den rättar ingenting. Det är rätt konstruktion för internkontroll: maskinen letar, människan beslutar. Varje fynd ska kunna följas till en namngiven ansvarig.

Statuskolumnen anger om uppgiften kan köras med dagens verktyg:

- **Klar** — möjlig med de endpoints vi har
- **Endpoint** — kräver åtkomst vi inte bekräftat ännu
- **Utred** — tröskeln eller regeln måste fastställas först

## Rättslig ram — måste verifieras

Trösklar och belopp nedan bygger på svensk rätt, men **flera punkter måste bekräftas av jurist innan registret läggs till grund för internkontrollen**:

| Fråga | Varför den är öppen |
|---|---|
| **Vilken myndighet utövar tillsyn över inkassoverksamhet?** | Tillsynen har flyttats mellan myndigheter. Bekräfta vad som gäller nu, och vad tillståndet är utfärdat under |
| **Omfattas bolaget av penningtvättslagen?** | Ren inkassoverksamhet är inte självklart anmälningspliktig. Förvärv av förfallna fordringar kan däremot vara finansiell verksamhet |
| **Aktuella kravavgifter** | Påminnelseavgift, inkassokravsavgift och avgift för amorteringsplan är reglerade och har ändrats över tid |
| **Arkiveringstid** | Bokföringslagen anger sju år. Kontrollera vad som gäller för ärendehandlingar specifikt |

---

## 1. Klientmedel

Det viktigaste området. Pengarna tillhör uppdragsgivarna, inte er.

| ID | Kontroll | Utlöser larm | Frekvens | Status |
|---|---|---|---|---|
| KM-01 | Klientmedelskonto mot summa borgenärsskuld i huvudbok (2420/2429) | Differens över [belopp] eller [%] | Daglig | Klar |
| KM-02 | Negativt saldo på en borgenär | Varje negativt saldo | Daglig | Klar |
| KM-03 | Inbetalningar mottagna men ej allokerade till ärende | Äldre än [X] dagar | Daglig | Endpoint |
| KM-04 | Medel ej redovisade till uppdragsgivare inom avtalad tid | Hållna längre än [X] dagar | Veckovis | Endpoint |
| KM-05 | Klientmedel sammanblandade med egna medel | Varje bokning mellan kontona | Daglig | Klar |
| KM-06 | Avstämning klientmedelskonto mot kontoutdrag | Differens vid månadsslut | Månadsvis | Endpoint |

**KM-01 är den ni redan haft problem med.** Juliavvikelsen berodde på en betalningsfil som inte importerades, och upptäcktes av redovisningskonsulten i efterhand. Körd dagligen hade den fångats samma vecka.

## 2. Inkassoprocess och god inkassosed

| ID | Kontroll | Utlöser larm | Frekvens | Status |
|---|---|---|---|---|
| IP-01 | Inkassokrav med lagstadgad betalningsfrist innan nästa steg | Frist ej iakttagen | Daglig | Endpoint |
| IP-02 | Åtgärd vidtagen på bestridd fordran | Varje förekomst | Daglig | Endpoint |
| IP-03 | Kravavgifter över lagstadgat tak | Avvikelse mot avgiftstabell | Veckovis | Utred |
| IP-04 | Ärenden utan framdrift | Ingen händelse på [X] dagar | Veckovis | Klar |
| IP-05 | Fordringar nära preskription | Under [X] månader kvar | Månadsvis | Endpoint |
| IP-06 | Dröjsmålsränta beräknad enligt räntelagen | Avvikelse mot referensränta plus åtta | Veckovis | Utred |
| IP-07 | Ärenden utan dokumenterat kravunderlag | Saknat underlag | Veckovis | Endpoint |
| IP-08 | Konsumentärenden hanterade enligt konsumentregler | Felaktig ärendetyp | Veckovis | Utred |

**IP-02 är den farligaste.** Att fortsätta indrivning på en bestridd fordran strider mot god inkassosed, och är den typ av ärende som når tillsynsmyndigheten.

**IP-08 spelar roll för mycket annat.** Konsument och näringsidkare har olika preskriptionstider och olika skydd. Är ärendetypen fel, blir IP-03, IP-05 och IP-06 också fel.

## 3. Kronofogden

Svenskt särdrag. Ansökan om betalningsföreläggande är ett rättsligt steg med egna krav.

| ID | Kontroll | Utlöser larm | Frekvens | Status |
|---|---|---|---|---|
| KF-01 | Ansökan om betalningsföreläggande utan tillräckligt underlag | Saknat kravunderlag | Daglig | Endpoint |
| KF-02 | Ansökan inskickad trots att fordran betalats | Betalning före ansökningsdatum | Daglig | Endpoint |
| KF-03 | Återkallelse ej gjord efter full betalning | Öppen ansökan mot nollsaldo | Daglig | Endpoint |
| KF-04 | Utslag ej verkställda inom rimlig tid | Äldre än [X] dagar | Månadsvis | Endpoint |
| KF-05 | Ansökningsavgifter vidarefakturerade korrekt | Avvikelse mot faktisk avgift | Veckovis | Utred |

**KF-02 och KF-03 är de dyra.** Att driva en betald fordran vidare hos Kronofogden ger en betalningsanmärkning för någon som inte är skyldig något — det är både ett skadeståndsansvar och en tillsynsfråga.

## 4. Betalningsflöde

| ID | Kontroll | Utlöser larm | Frekvens | Status |
|---|---|---|---|---|
| BF-01 | Betalningsfiler som ej importerats | Varje misslyckad import | Daglig | Endpoint |
| BF-02 | Inbetalningar direkt till borgenär, ej anmälda | Avvikelse mot förväntat saldo | Veckovis | Utred |
| BF-03 | Dubbelregistrerade inbetalningar | Samma belopp, datum och ärende | Daglig | Klar |
| BF-04 | Inbetalningar utan OCR eller referens | Oidentifierad efter [X] dagar | Daglig | Endpoint |
| BF-05 | Återbetalningar utan godkännande | Saknat godkännandespår | Veckovis | Endpoint |

## 5. Datakvalitet

| ID | Kontroll | Utlöser larm | Frekvens | Status |
|---|---|---|---|---|
| DK-01 | Ärenden utan gäldenärsadress | Varje förekomst | Veckovis | Klar |
| DK-02 | Möjliga dubbelregistrerade ärenden | Samma gäldenär, borgenär och belopp | Veckovis | Klar |
| DK-03 | Ärenden utan kravunderlag | Saknad dokumentation | Veckovis | Endpoint |
| DK-04 | Fel borgenärskoppling | Borgenär utan aktivt avtal | Månadsvis | Klar |
| DK-05 | Belopp som avviker från ursprungsfaktura | Differens utan förklaring | Veckovis | Endpoint |

## 6. Penningtvätt

**Villkorat.** Kör dessa först när det är bekräftat att bolaget är verksamhetsutövare enligt penningtvättslagen. Ren inkassoverksamhet är inte självklart anmälningspliktig; förvärv av förfallna fordringar kan vara det.

| ID | Kontroll | Utlöser larm | Frekvens | Status |
|---|---|---|---|---|
| PT-01 | Nya uppdragsgivare utan genomförda kundkännedomsåtgärder | Ärende skapat före åtgärd | Daglig | Endpoint |
| PT-02 | Kundkännedom ej uppdaterad | Äldre än [X] år | Månadsvis | Endpoint |
| PT-03 | Inbetalning som väsentligt överstiger fordran | Över [%] av saldo | Daglig | Klar |
| PT-04 | Betalning från tredje part eller utlandet | Avvikande betalarinformation | Veckovis | Utred |

## 7. Dataskydd

| ID | Kontroll | Utlöser larm | Frekvens | Status |
|---|---|---|---|---|
| DS-01 | Ärenden förbi gallringsfrist, ej raderade | Över [X] år efter avslut | Månadsvis | Endpoint |
| DS-02 | Personnummer i fält där de inte hör hemma | Träff på personnummer i fritext | Veckovis | Klar |
| DS-03 | Registerutdrag utan svar inom frist | Över en månad | Veckovis | Endpoint |

**DS-02 kan agenten göra redan.** Maskeringen i MCP-servern hittar personnummer i fritext. Samma logik kan användas för att *hitta* dem, inte bara dölja dem.

## 8. Behörighet och systemkontroll

| ID | Kontroll | Utlöser larm | Frekvens | Status |
|---|---|---|---|---|
| BS-01 | Användare med behörighet utöver sin roll | Avvikelse mot rollmall | Månadsvis | Endpoint |
| BS-02 | Inaktiva användare med aktiv behörighet | Ingen inloggning på [X] dagar | Månadsvis | Endpoint |
| BS-03 | Misslyckade bakgrundsjobb | Varje fel | Daglig | Endpoint |
| BS-04 | Ändringar i systemkonfiguration | Varje ändring | Daglig | Endpoint |
| BS-05 | Uppslag utanför arbetstid eller i ovanlig volym | Över [X] uppslag per användare per dag | Veckovis | Endpoint |

---

## Vad agenten levererar

För varje körning: en lista över avvikelser med ärendenummer, vad som utlöste larmet, och när det upptäcktes. Inga avvikelser ger en kvittens på att kontrollen körts — det är den kvittensen som dokumenterar att internkontrollen fungerar, och den är lika viktig som fynden.

Allt loggas med tidsstämpel, jämför revisionsloggen i MCP-servern.

## Vad som saknas

Ressursgrupperna finns i Collect- och Ledger-dokumentationen. Detta är underlaget för vad ni ska be Banqsoft öppna:

| Behov | Täcker |
|---|---|
| `CasePayments` och `Payments` | KM-03, KM-04, BF-03, BF-04 |
| `Dispute` | IP-02 |
| `ClaimBases` | IP-07, DK-03, KF-01 |
| `CourtInvoices` och `LegalBasis` | KF-01 till KF-05 |
| `importPayment` med felstatus | BF-01 |
| `ChangeLog` | BS-04 |
| `Jobs` och `BackgroundProcess` | BS-03 |
| `Gdpr` | DS-01, DS-03 |
| `accessDefinitions` och `users` | BS-01, BS-02 |
| `Log` | BS-05 |
| `InterestTables` | IP-06 |
| `Pricelists` | IP-03, KF-05 |

---

## Egna uppgifter

Fyll på här.

| ID | Kontroll | Utlöser larm | Frekvens | Status |
|---|---|---|---|---|
| | | | | |
