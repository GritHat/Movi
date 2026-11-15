# Controllo statistico delle prove di volo e della perdita di confidenza (sciame-statistico, f19-volo/21-statistica)

15-11-2026, dalle 05:26:26 alle 05:31 (`date -Is`). Previsioni scritte prima in `PREVISIONI.md` (05:26:26), prima di aprire i
due rapporti. Riconto indipendente dai grezzi con `controllo.py` (proprio Wilson, propri conteggi; condivide con i rapporti
i **grezzi**, la funzione `mezzo()`/`dividi()` di `prove_reali.py`, importata, e i simulatori: è indipendente solo
sull'aggregazione e sui test). Uscite: `controllo_esito_v2.json` (vale questa); `controllo_esito.json` è la v1, con i
p-value del chi-quadro sbagliati per x grande (mia serie numerica imprecisa; corretta con scipy, file lasciato).
Tutto è **simulato** o **su dati pubblici con rumore di sensore simulato**; nessuna prova su hardware.

## 0. In testa

- Regole: nessuna violata. Nessun file cancellato, niente git, nessuna rete, un processo alla volta con `timeout`.
- Esito delle mie previsioni: **P1 regge** (tutte le k/N del § 2 di PROVE_VOLO coincidono; le fasce di calibrazione
  riportate coincidono una per una). **P2 regge con riserva** (sotto). **P3 regge** (Wilson coincide entro 10⁻⁴).
  **P4 regge** (16 aerei distinti in prova; nel simulato un solo scenario per F#). **P5 regge** nella prima parte ma la
  seconda è **smentita**: il test d'adeguatezza **rifiuta** quasi ovunque. **P6 regge** (F3: 0/60).
- **Cambio di stato proposto (importante).** La frase di PROVE_VOLO § 2.1 «le fasce alte (C ≥ 0,9) sono vicine
  all'osservato entro 0,01–0,10» è **smentita come affermazione generale**: le celle **F1/att** e **F6/att**, nel modello
  (prima di ogni evento), sono **omesse** dalla tabella e sono gravemente ottimiste. Vale solo in sda e in F2/F5 att.

## 1. Critiche numerate

1. **Soglie prima.** `10-prove/PREVISIONI.md` dichiara 04:49:34; il primo avvio è 04:52:41 (`avvio_v3.txt`); le aggiunte
   a posteriori (04:53, 05:04, 05:15:46) sono marcate e precedono i rispettivi avvii (05:15:56 per v3i). Riserva: il
   file ha mtime 05:15:46 (riscritto per le aggiunte), quindi l'ora del blocco originale **non è verificabile**
   indipendentemente. `03-confidenza/PREVISIONI.md`: mtime 04:38:08 < avvio 04:41:29: **verificato**.
2. **Calibrazione omessa (F1/att, F6/att).** Un campione per passaggio e per fascia, v3b e v3i identici:
   F6/att, C ≥ 0,9: vero nella porta in **1/78 campioni**; per fasce 0/14, 0/16, 1/20 (C media 0,93–0,999).
   F1/att, C ≥ 0,9: 104/224; fascia 0,99–1: 15/45 = 0,33 [0,21; 0,48] contro C 0,999. Causa probabile (non verificata):
   radar rotante a 1 Hz con aereo a 120–135 m/s, covarianza del nucleo troppo piccola. È lo scenario d'alta velocità
   centrale: **la curva C(τ) del nucleo in att non va mostrata**.
3. **Test d'adeguatezza (Hosmer–Lemeshow per fasce, un campione per passaggio, gradi = fasce con n ≥ 10).** Rifiuta in
   F1/sda (χ² 59,9, df 8, p 5·10⁻¹⁰), F2/att (104,5; p 5·10⁻¹⁹), F5/att (39,7; df 6; p 5·10⁻⁷), F1/att e F6/att
   (p ≈ 0). Non rifiuta dove c'è una sola fascia (F2/F5/F6 sda, C ≈ 1: 60/60, 60/60, 29/29): lì il test non ha potenza.
   Dopo l'evento (F3/sda, F4/att) rifiuta: atteso, fuori modello.
4. **Dati reali (`03-confidenza`).** Divisione per mezzo **verificata**: intersezione taratura/prova = 0 in tutte e tre
   le classi. Ricostruita la mappa caso→sequenza→mezzo (56/56, 28/28, 98/98 blocchi). Il Wilson «per caso» del rapporto
   ignora il grappolo: con il bootstrap a grappoli sui mezzi (2000 ricampionamenti) gli intervalli per gli aerei restano
   simili (deff 0,4–2,9), per l'ala fissa si allargano molto (deff fino a 5,2; n efficace 38 a 6–10 s).
   Un aereo pesa il **24,5 %** dei casi; a 1–2 s i mezzi sono **12**, non 16.
5. **Quanti mezzi distinti.** Aerei veloci: **16** in prova (indirizzi ICAO distinti; 15 in taratura). Ala fissa: 16
   «mezzi» sono voli ALFA per data-ora, ma il dataset ALFA usa, per quanto noto, **un solo velivolo** (fonte non
   riaperta: non verificato). Multirotori: 98 voli CMU, presumibilmente **un solo esemplare** di M100 (non verificato).
   Simulato F1–F6: **una sola geometria per scenario**; i 60–200 passaggi variano solo semi e rumore. N grande ≠ molti
   casi diversi.
6. **PIT (forma della distribuzione).** Decili del PIT, tutti i casi, χ² diviso per il deff medio (Rao–Scott): rifiutano
   per ogni mezzo e filtro (aerei CV 1049, IMM 1073, df 9, p < 10⁻²⁰⁰; ala fissa CV p 7·10⁻⁷). Gli aerei hanno eccesso
   in **entrambe** le code (regione talvolta troppo larga, talvolta troppo stretta): la copertura al 90 % è vicina in
   media, la distribuzione non è tarata. Si può dire «copertura al 90 % vicina», non «confidenza tarata».
7. **Virate.** La mia classe «non rettilineo» (virata + accelerazione) dà IMM 0,80 / 0,94 / 0,91 e CV 0,42 / 0,47 / 0,56
   su **7, 7, 11 aerei**: la conclusione del rapporto (IMM coerente in manovra, CV no) regge, ma poggia su 7–11 mezzi.
8. **Minimi nascosti dalle mediane.** F4 margine dell'operatore: mediana 1,2 s, **minimo 0,25 s** (att), 0,45 s (sda).
   F4/sda frammenti in V: 0,995 sui campioni, ma il passaggio peggiore ha **0,736**. Copertura r99-o-insieme di F6/att:
   0,984 è sui campioni; per passaggio (tutti i cicli coperti) **49/51 [0,87; 0,99]**; F1/att 47/50 [0,84; 0,98].

## 2. Tavola delle cifre presentabili

Stato: S = simulato, R = dati pubblici con rumore simulato, C = calcolato, I = ipotesi. Intervallo: Wilson 95 % per
passaggio, salvo «mezzi» (bootstrap a grappoli sui mezzi). Classe: **solido** (estremo inferiore ≥ 0,90 o 0 eventi con
sup ≤ 0,06 nello scenario dichiarato), **incoraggiante** (stima ≥ 0,80 con base matematica, estremo inferiore ≥ 0,70),
**limite** (sotto).

| cifra | stato | N | stima [intervallo] | classe |
|---|---|---|---|---|
| Mai «libero» sul punto vero, F1–F6, att e sda (v3i) | S | 1000 passaggi; 12 celle | 0 in ogni cella; F6 0/200 [0; 0,019] | solido (una geometria per scenario) |
| Nessun falso evento, F6 quasi collisioni a 40 m (v3i) | S | 200 + 200 | 0/200 [0; 0,019] per cfg | solido |
| F4 avaria in volo: evento entro 1 s | S | 60 + 60 | 60/60 [0,940; 1] | solido |
| F4 camere dichiarate inaffidabili entro 3 cicli | S | 60 + 60 | 60/60 [0,940; 1] | solido |
| Continuità in sda (nessun ciclo senza regione) | S | 60 per cella, F6 200 | 60/60 [0,940; 1]; F6 200/200 [0,981; 1] | solido |
| Copertura (r99 o insieme di presenza) dopo collisione F3/sda | S | 60 passaggi, 1024 campioni | 60/60 [0,940; 1] | solido |
| F1 avviso di prossimità ≥ 20 s prima del CPA, sda | S | 60 | 56/60 [0,841; 0,974] | incoraggiante |
| F3 avviso di prossimità prima dell'urto (≥ 10 s) | S | 60 + 60 | 60/60 [0,940; 1] (soglia non scritta prima) | incoraggiante |
| F4 avviso tempestivo all'operatore | S + I (5,4 s di risposta) | 60 + 60 | 60/60 [0,940; 1]; margine min 0,25 s | incoraggiante |
| F4 passaggi con tutti i frammenti in V(τ) | S | 60 + 60 | 58/60 [0,886; 0,991] | incoraggiante |
| F6/att continuità | S | 200 | 186/200 [0,886; 0,958] | incoraggiante |
| Aerei reali, IMM, copertura al 90 %, τ 3–30 s | R | 16 aerei; 374–416 casi per fascia | 0,92–0,98; mezzi [0,895; 0,99] | incoraggiante (prudente oltre 10 s) |
| Aerei reali in manovra, IMM, 6–30 s | R | 7–11 aerei | 0,80–0,94; Wilson casi [0,68; 0,97] | incoraggiante |
| Aerei reali, CV, copertura al 90 %, 3–30 s | R | 16 aerei | 0,82–0,87; mezzi [0,75; 0,91] | incoraggiante |
| Multirotori, CV, al 90 %, 1–30 s | R | 98 voli (1 esemplare?) | 0,86–0,91; mezzi [0,82; 0,93] | incoraggiante |
| C(τ) chiusa, integrale sull'ellissoide | C | 20 + 20 casi; MC 10⁶ | scarto ≤ 7,6·10⁻⁸; \|z\| ≤ 2,11 | solido (dimostrato nel modello) |
| Calibrazione del nucleo, fasce alte, sda | S | 42–60 passaggi per fascia | F1: 40/42, 48/50, 60/60 | incoraggiante (HL rifiuta sulle fasce medie) |
| Aerei reali, 1–2 s, al 90 % | R | 12 aerei, 733 casi | CV 0,72, IMM 0,71; mezzi [0,67; 0,76] | limite |
| Calibrazione del nucleo, att, F1 e F6 | S | 17–45 per fascia | F6 C ≥ 0,9: 1/78; F1 0,99–1: 15/45 | limite (non mostrarla) |
| F1/att continuità | S | 60 | 39/60 [0,52; 0,76] | limite |
| F3 collisione dei droni come evento entro 2 s (v3i) | S | 60 + 60 | 0/60 [0; 0,060] | limite (smentita) |
| F5 scambio d'identità dopo 2–4 s di solo radar | S | 60 + 60 | 0,47 [0,35; 0,59]; 0,63 [0,51; 0,74] | limite |
| Zona «al 99 %» della sola covarianza | S | per cella | 0,003–0,91 | limite (smentita) |
| Distribuzione del PIT (forma) | R | tutti i casi | rifiutata, p < 10⁻⁶ ovunque | limite |
| Latenza sda 1,2 ms | I | — | stima per analogia | ipotesi: niente cifra in giuria |

La regola v4 (F3 59/60 [0,911; 0,997]) **non è presentabile**: falsi eventi F6 198/200 e 158/200.

## 3. Stati che propongo

- stat-1: «Mai libero il non osservato» nei 6 scenari di volo: **sostenuto dai dati (simulato)**, una geometria per
  scenario; non universale.
- stat-2: «C(τ) del nucleo tarata»: **smentito** in att (F1, F6); **non risolto** in sda (una fascia, test senza potenza).
- stat-3: «copertura al 90 % vicina su aerei reali, IMM, 3–30 s»: **sostenuto dai dati (pubblici + simulato)**, 16 aerei.
- stat-4: «distribuzione della confidenza tarata»: **smentito** (PIT).

## 4. Che cosa propongo dopo

1. Nel video mostrare la **regione che cresce dell'IMM tarato su aerei reali** (stat-3) e l'insieme di presenza, non la
   C del nucleo in att. Previsione: nessuna cifra mostrata con estremo inferiore < 0,70.
2. Rifare la calibrazione F1/F6 att con la covarianza gonfiata dal fattore tarato in `03-confidenza` (q×4 per l'IMM).
   Previsione: C ≥ 0,9 osservata ≥ 0,80 per passaggio; smentita se < 0,60.
3. Per il documento: ogni cifra con N di **mezzi distinti** accanto a N di passaggi; scenari di volo come «una
   geometria nominale per scenario».
