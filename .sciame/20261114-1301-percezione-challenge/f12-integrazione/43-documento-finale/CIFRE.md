# CIFRE del testo finale di due pagine — una riga per cifra (`sciame-redattore`, f12, 43-documento-finale, 14 novembre 2026)

**In testa.** Tabella rifatta dalla prima stesura (`40-documento/CIFRE.md`) con `fai_cifre.py` e riletta contro il testo finale. Nessuna cifra è mia, salvo tre conti a mano dichiarati nella riga (0,655; 0,548; 0,92 m/s). Nessuno stato è cambiato rispetto al verdetto d'integrazione: niente è «validato». Le cifre sono **lette** nei file indicati, non ricontate da me; «[R]» = ricontato dall'arbitro nel suo verdetto. Percorsi relativi a `.sciame/20261114-1301-percezione-challenge/`. Sigle: **VI** `f12-integrazione/30-arbitro/VERDETTO_INTEGRAZIONE.md`; **CH** `f5/CHIUSURA.md`; **V3** `f12-integrazione/20-finale/SOLUZIONE_V3.md`; **BL** `f14-classificazione/20-inclusione/BLOCCO_CLASSIFICAZIONE.md`; **SCH** `f12-integrazione/22-schermo-finale/SCHERMO_E_DEMO.md`; **PIA** `f12-integrazione/21-piano-finale/PIANO_14_4.md`; **DF** `f13-allegato/DISCORDANZE_DEI_FASCICOLI.md`; **VD** `f10-dati/23-verdetto/VERDETTO_DATI.md`; **VN** `f4/H-012/09-arbitro/VERDETTO.md`; **CI** contratto `f12-integrazione/CONTRATTO_INTEGRAZIONE.md`. Marca: [S] provato in simulazione, [C] per regola scritta, calcolo o scheda tecnica, [P] in progetto, non provato.

| Cifra | Frase del testo in cui compare | Origine (file, paragrafo) | Stato |
|---|---|---|---|
| 1,2 m; 3 m | «camera ferma a 1,2 m da terra, al chiuso, fino a 3 m» (riquadro) | V3 §7, prima riga; SCH §1, riga fissa | [P] parametro di progetto |
| 0,5° | «posa della camera nota (inclinazione entro 0,5°)» (riquadro); «se l'inclinazione è nota entro 0,5°» (§1); tabella 1, ultima riga | VI testa, cambio 5, e §5 condizione 4 («posa»); V3 §1.3 («errore d'inclinazione entro 0,5°»); CH §1 (c) | [C] premessa della dimostrazione condizionata; a 1° cade [R] |
| 1,24 m; 1,7 m | «il suolo a meno di 1,24 m davanti e di 1,7 m ai lati» (riquadro) | V3 §7 «Limiti»; VI §5 condizione 15 | [C] conto geometrico, campo di 58° (DF, geometria 2: 1,71–1,73 m ai lati). **Non scritta nel testo:** la coppia 1,22 m e 1,69 m, che vale con f = 424 px (campo 59,0°) |
| 1,70 m; 2,01 m | «la testa di una persona di 1,70 m a meno di 2,01 m» (riquadro) | DF, da `02-geometria`, II.2 punto 3; V3 §7 «Limiti» | [C] conto del fascicolo (2,41 m vale per 1,80 m: non usata) |
| 10 su 10 (prove) | «tolto l'ostacolo e rivisto il suolo, l'avviso non si spegne (10 prove su 10)» (riquadro) | VI testa, cambio 10, e §4 riga K-505; V3 §1.7 «Difetto aperto» | [S] controesempio certificato [R]; causa non diagnosticata |
| 15° | «inclinata di 15° in basso» (§2) | V3 §7, prima riga; SCH §1, riga fissa | [P] parametro di progetto |
| 1° × 0,1 m | «celle di 1° × 0,1 m fino a 3 m» (§2) | SCH §1, riga fissa; consegna del coordinatore | [P] parametro di progetto |
| 4 (stati); quattro | «Mappa del suolo a 4 stati» (schema); «in quattro stati» (§2) | V3 §3 «Comune» | [P] |
| 400 | «viene da 400 percorsi di camminatori simulati, lo stesso generatore delle prove» (§2) | V3 §1.6, predittore `sd-1`; verdetto sulla continuità (f8), riga 31: libreria e passaggi dallo stesso generatore | [S] sul banco ideale; nel prototipo entra per primo il ripiego `sd-0` (disco a velocità costante, senza cifra: V3 §1.6, VI §5 condizione 11) e `sd-1` è fra i lavori delle 4 ore (PIA §1) |
| 0,40 m | «una fascia di 0,40 m» (§2; §4 punto 4) | V3 §1.7 (w, scelta) | [P] parametro scelto |
| 0 su 20 000 | «sulla sola fascia 0 violazioni su 20 000 sequenze» (§2) | BL §0 e §7; VI §7 affermazione 14 | [S] sulla sola fascia; letto dall'arbitro, non ricontato; mai sulla catena |
| 0 su 23 402 | «0 interruzioni su 23 402 passaggi» (§1, marca dell'obiettivo) | VI §3 e §7 affermazione 5; CH §1 (a) | [S] sensore ideale [R]; per costruzione la regola. **Non scritto nel testo:** i camminatori distinti sono 6 000, quindi «meno di 6,4 su 10 000» |
| 24 su 23 402; 928 | «l'avviso può non nascere (24 passaggi su 23 402 con la regola che lo cura, che parte spenta; 928 senza)» (§3) | VI testa, cambio 3, e §7 affermazione 10 | [S] [R]; la regola (c7) parte spenta: VI §3 e §5 condizione 5 |
| 2 m; 9 su 10; 2 s; 85 su 100; 3 s | «Con un ostacolo largo 2 m, il bordo dell'ombra noto e la persona sul proprio percorso … almeno 9 casi su 10 fino a 2 s e … almeno 85 su 100 fino a 3 s» (§3) | VI §7 affermazione 6 e §5 condizione 11; CH §1 (b) | [S] 30 celle su 30 [R]; limiti peggiori 0,921 e 0,899 |
| 1 m; 87 su 100; 1 s | «Con il pannello da 1 m della demo: almeno 87 su 100 a 1 s» (§3) | VI §7 affermazione 7 e testa, cambio 1 | [S] [R]; la soglia di 9 su 10 è smentita |
| 6–8 su 10 | «Chi svolta o esce dal lato lontano: circa 6–8 casi su 10 a 2–3 s» (§3) | VI §7 affermazione 8 («circa 6–8 su 10») e §3 (0,57–0,86 a 2–3 s) | [S] controesempio in simulazione; V3 §3 vieta una cifra per chi svolta, VI la dà: seguo VI (dubbio 1 nel testo) |
| 3–5 su 10; 1 s | «Bordo dell'ombra stimato e non dato: 3–5 su 10 a 1 s» (§3) | VI §3 «Dove cede» (0,30–0,46 a 1 s senza riconoscerlo); V3 §1.6 | [S]; **arrotondamento mio** di 0,30–0,46 (era già «3–5 su 10» nella v0.8) |
| 3 s | «oltre 3 s: nessuna cifra, resta l'avviso» (§3) | VI §3 «Dove cede»; V3 §1.6 (orizzonte) | [P] regola |
| 2 983 su 4 552 | «il segno «previsto» manca in 2 983 fotogrammi su 4 552, circa due su tre» (§3) | VI testa, cambio 9 (424 px); CH §2 punto 1 | [S] [R]; a 848 px: 2 968 su 4 553; «due su tre»: conto mio, 2 983 / 4 552 = 0,655 |
| 300; 9 000; due (lanci) | «(camera ideale, cioè profondità calcolata dalla geometria: 300 condizioni, 9 000 fotogrammi, due volte)» (§4.1) | VI §7 affermazione 4 e §1 riga C-D; camera ideale: `03-libero/PREVISIONI.md` riga 9 (camera a foro, rumore k·z²) | [S] verificato sull'insieme dichiarato [R] |
| 1° | «Con 1° d'errore d'inclinazione cede» (§4.1) | VI testa, cambio 5 | [S] controesempio [R] |
| 3 m; 0 su 4 324; 0 (replica) | «Una persona nascosta entro 3 m non è mai rimasta senza avviso (0 fotogrammi su 4 324; replica: 0)» (§4.2) | VI testa, cambio 7, e §7 affermazione 9 | [S] profondità simulata [R]; 424 px (0 su 4 325 a 848 px); **non scritto:** la replica è 0 su 3 608 |
| 0 su 90 | «Coi parametri di partenza reggeva 0 volte su 90» (§4.3) | VD §5 punto 5; VI testa, cambio 6 | [S] smentita su profondità simulata realistica |
| 176 su 180; 94–99 % | «con una correzione che parte spenta, 176 su 180 (94–99 %)» (§4.3) | VI testa, cambio 6 ([94,4–99,1 %], 424 px), e §7 affermazione 11 | [S] tasso in un dominio stretto [R]; il criterio di VD (28 su 30 per caso) non è superato; 174 su 180 a 848 px; interruttore spento di norma: VI §5 condizione 13 |
| 0,5 m; 2,6 m | «a 0,5 m dal pannello, entro 2,6 m» (§4.3) | VI §2 riga «identità al ritorno» e §7 affermazione 11 | [S] dominio della cifra |
| 19 su 20 | «prende il numero (19 volte su 20)» (§4.3) | VI §2 riga «identità al ritorno» e §7 affermazione 11 | [S] [R] |
| 3 m; 1,44 m/s; 1 s | «I 3 m di portata bastano … fino a 1,44 m/s, con 1 s di reazione (ipotesi)» (§4.4) | VI §7 affermazione 15; BL §6 | [C] per conto; reazione ipotizzata, latenza stimata |
| 1,13 m/s | «La fascia di 0,40 m copre chi è nascosto fino a 1,13 m/s» (§4.4) | VI §5 condizione 8 e §3; DF, da `01-dimostrazioni`, D4; V3 §1.7 | [C] conto del fascicolo, riconosciuto dall'arbitro (sostituisce «1,4 m/s») |
| 360°; 180° | «Tre sensori a tempo di volo per 360°. Coprono 180°» (§5) | VN riga 82, punto 8 («Tre ToF non danno 360° … 180°») | [C] lettura della scheda, «verificato sulle fonti per i sensori citati» |
| 80 505 su 146 901 | «80 505 falsi su 146 901» (§5) | V3 §4, riga «Mappa a voxel» (da V7 §1) | [S] letto in V3, non ricontato; 0,548 (conto mio), non scritto |
| 38–100 % | «nel 38–100 % dei transiti» (§5) | V3 §4, riga «Due ipotesi con pesi» (da V9, V8) | [S] letto in V3, non ricontato |
| 15 cm; 2 m; 10 su 10 | «scatola di 15 cm a 2 m: 10 su 10» (tabella 1) | V3 §3, riga R2 | [S] **preliminare** (f10) |
| 79 su 90 | «Pannello fermo dato per mobile 79 volte su 90» (tabella 1) | VI §2 riga «mobile»; VD | [S] controesempio coi gruppi del nucleo |
| 0 su 140 | «0 su 140 con una correzione che parte spenta, nel suo dominio» (tabella 1) | VI §2 riga «mobile» | [S] [R]; fuori dominio 7 passaggi su 10 (VI, cambio 10) |
| 1,3 m | «suolo visto libero da 1,3 m a d metri» (tabella 1) | VI §5 condizione 6; V3 §3 «Parole» | [P] dicitura |
| 6 ms; 81 ms | «calcolo su un portatile, un solo filo: 6 ms per ciclo in media su scene simulate, 81 ms su una registrazione pubblica affollata» (tabella 1) | VI §7 affermazione 16; VD §5 punto 6 | [S]; un filo di un portatile, non la scheda di bordo; registrazione vera di una camera D415, non nostra, 254 tracce (VD riga 16) |
| 0,13 s | «segnale in 0,13 s (rumore ipotizzato)» (tabella 1) | V3 §3 riga R6 e §1.9 | [S] rumore dell'IMU ipotizzato; valore da rifissare (V3 §1.9, righe 223–224) |
| 0,3 s | «Segnali sonori di 0,3 s» (tabella 2) | V3 §3, tabella dei profili | [P] mai provati con persone |
| cinque (atti); cinque (minuti) | «Cinque atti, cinque minuti» (§8) | SCH §4 (tabella degli atti) e titolo del §7 (5 minuti, 300 s) | [P] |
| 1,8 m (alto); 1 m (largo) | «pannello alto 1,8 m e largo 1 m, un adulto a passo lento» (§8) | SCH §4; V3 §7 «Geometria della demo»; VI §5 condizione 14 | [P]; **non scritti:** a 1,8 m dal sensore, adulto a 2,3 m |
| 14; 4; cinque (persone); 18 | «Il piano: 14 + 4 ore, cinque persone»; «Ore 12–18» | CI, priorità 3 | dato della consegna |
| sei (gradini); 0; 12 | «Ore 0–12. Sei gradini … All'ora 12 il programma si congela» (§9) | PIA §1 (scala ①–⑥, gelo all'ora 12); VI §5 condizione 18 | [P] |
| 5–6; 30 (passaggi) | «Ore 5–6. Se arriva una camera: posa, pavimento vuoto, pannello sul suolo segnato, 30 passaggi» (§9) | PIA §6 ramo A; VD §6 | [P] mai eseguite; **non scritti:** 30 s di pavimento vuoto, 150 fotogrammi |
| 14; quattro (gradini); 0,82; 0,99 | «i primi quattro gradini all'ora 14 con probabilità 0,82–0,99» (§9) | VI §6; PIA §9 | [C] simulazione di **stime**, non misure; 0,47 nel modello duro (non scritto) |
| 0,04; 0,43 | «tutti e sei, con tabellone e demo, 0,04–0,43» (§9) | VI §6 e §7 affermazione 16; PIA §0 e §9 | [C] simulazione di stime; 0,005 nel modello duro (non scritto) |
| 4 (fotogrammi) | «una persona già vista per almeno 4 fotogrammi» (§1) | VI §5 condizione 9 e §7 affermazione 5 | [C] premessa della garanzia |
| 5 cm | «Su sensore ideale (la persona è un punto, con 5 cm di rumore)» (§3) | VI §3, riga «Cifra» | [S] definizione del banco |
| 14; 4 (ore) | «Nelle 14 ore lo schermo mostra prima un disco, senza cifra; la zona con la cifra è un lavoro delle ultime 4 ore» (§2) | V3 §1.6 (`sd-0` per primo, senza cifre); VI §5 condizione 11; PIA riga 55 (`sd-1` fuori dal minimo), riga dell'ora 15 e ordine dei tagli (quarto) | [P]; se si taglia, la zona con la cifra non c'è |
| 1,8 s; 0,92 m/s | «Con un operatore remoto (1,8 s): 0,92 m/s» (§4.4) | BL §3, riga «lo stesso, con operatore remoto» | [C] per conto; **rifatto da me**: (3 − 0,95) m / (0,267 + 0,155 + 1,8) s = 0,92 m/s; con 1,0 s: 1,44. **Non scritto:** 1,07 m/s con 1,5 s (ipotesi per la persona non vedente) |
| 98–100 %; 9 persone (non scritte) | — (punto tolto per spazio) | VI §7 affermazione 12; VD §5 punto 4; DF, stima D6 | [S] è il cerchio del filtro con q = 0,2, non la zona mostrata; q tarato 0,05–0,1 (VD riga 14) |
| 100 (in «85 su 100», «87 su 100»); 10 (in «su 10»); 10 000; 20; 90; 180; 2 (s); 1 (s, m); 3 (s, m) | denominatori e unità delle righe qui sopra | le righe corrispondenti | come la riga corrispondente |

## Note

**Non letti per intero, contro la consegna** (20 minuti): VD (righe 14, 16 e 86; il resto tramite VI), DF (righe 21 e 45; il resto tramite la consegna e la prima stesura), il decimo addendum (solo il titolo), V3 (righe cercate: §1.2, §1.3, §1.6, §1.7, §1.9, §3 «non si dice mai»), BL (§3, §6, §9), SCH (§6), PIA (quattro righe su `sd-1`), il verdetto sulla continuità (riga 31); **non aperti:** VN, V7, V9, l'audit, f6, i file di f14 diversi da BL, gli addendum 1–9, `STATO_PROGETTO.md`, `RIFERIMENTI.md`, la prova sull'identità e la sua controprova (esistono, viste con `ls`: ne uso le cifre ricontate dall'arbitro in VI). Letti per intero: il contratto, la prima stesura con CIFRE.md, le due letture, VI.

**Indipendenza.** `controlla.sh` ha lo stesso autore del testo e viene dalla prima stesura: vale per conteggi e ricerche testuali, non per il contenuto. **Nessun lettore ha riletto il testo finale: il controllo C-G resta «non verificato» sulla versione finale.**
