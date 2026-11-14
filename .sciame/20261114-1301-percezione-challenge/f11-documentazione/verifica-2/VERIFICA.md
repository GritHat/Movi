# Verifica avversaria di `STATO_PROGETTO.md`, parte 2 di 3 — `sciame-validazione`, f11

**Documento:** `f11-documentazione/unione/STATO_PROGETTO.md`, versione 1 (2026-11-14T17:05:19), 1609 righe (`wc -l`).
**La mia parte:** righe 537–1073, cioè §3.6–§3.9, cap. 4 (prove e cifre), cap. 5 (estensioni f7–f10), cap. 6 (piano e rischi), cap. 7 (decisioni dell'utente).
**Lavoro:** dalle 17:05:44 alle 17:20 del 14 novembre 2026 (`date -Is`). I percorsi sono relativi alla cartella della convocazione. «r.» = riga del documento; «f.» = riga del file d'origine.

## 0. In testa

**Esito in una riga.** Le cifre della mia parte tornano quasi tutte (98–99 %): il documento è fedele ai file. I difetti veri sono pochi e di tre tipi: otto cifre sbagliate o imprecise, sette frasi più forti del file, cinque citazioni che puntano al file sbagliato. Nessuna cifra inventata trovata. Niente è provato sull'hardware, e il documento lo dice.

**Cambi di stato che propongo** (dettaglio al §b):
1. «0 su 14 400» (r. 713, r. 814, r. 862): da «sostenuto in simulazione» a «misura solo su 4800 passaggi (ombra a −20 cm); per costruzione sugli altri 9600».
2. «Area prevista ancora mostrata: in tutti i casi sotto il 20 %» (r. 875): **smentita** dai file stessi (28–72 % con il pannello da 0,5 m).
3. «Chiusura per causa: 100 %» (r. 605): vale solo per la forma a particelle; la forma semplice dà 0 % in sosta.

**Previsioni mie**, scritte alle 17:06:07 in `f11-documentazione/verifica-2/PREVISIONI.md`, dopo aver letto il documento e prima di aprire i file d'origine:
- P1 (almeno il 95 % delle cifre torna): **regge** (98–99 %).
- P2 (almeno 3 cifre con un file che non le contiene): **regge** (5).
- P3 (almeno uno stato più forte del file): **regge** (7).
- P4 (le cifre [prel.] dei cap. 5–6 tornano meno spesso di quelle di f1–f6): **smentita** (tornano allo stesso modo: un solo errore su circa 300).

**Regola violata, per errore.** Nell'ultimo controllo ho lanciato un `git status` (sola lettura, uscita scartata, nessuna modifica), contro il «niente git» della consegna.

**Scostamenti.**
- Ho letto anche le righe 1–27, 53–80 (legenda) e 530–536, fuori dalla mia parte, per capire marche e rimandi.
- Ho rieseguito, in sola lettura, due script dello sciame: `f10-dati/02-sensori/controlla_parametri.py` e `f10-dati/04-embedded/geometria_sensori.py` (`PYTHONDONTWRITEBYTECODE=1 timeout 60 python3 -I`), e ho rifatto i sette `diff` del controllo di ripetibilità. Nessun file del progetto è stato scritto.
- **Nessuna pagina in rete aperta da me.** Lo stato delle fonti esterne è quello dei file: «non verificato» da me. Ho solo controllato che le 17 chiavi citate nella mia parte stiano in `RIFERIMENTI.md` e nell'appendice B: ci sono tutte.
- Il conteggio delle cifre (§f) è fatto a mano, sezione per sezione: vale entro il 5 % circa.
- Lunghezza oltre le due pagine: la consegna chiede di essere esaustivi.

**Indipendenza.** Condivido con gli autori del documento e dei file il modello linguistico. Non condivido la lettura: ho riaperto i file grezzi, non i rapporti, dove c'erano. Vale per gli errori di trascrizione e di stato; non vale per gli errori dei simulatori, che non ho rieseguito (salvo i due script sopra).

## a. Cifre sbagliate o imprecise

| # | Dove | Il documento scrive | Il file dice | File |
|---|---|---|---|---|
| a1 | r. 627, H-006 | tempo a 320×240: **4,7 ms** | **5,1 ms** («320x240: mediana 5.1 ms»). Il 4,7 è nel rapporto, non nel file grezzo. Il documento lo sa (r. 883) ma la tabella porta la cifra sbagliata | `f2/04-torneo/esito_attacchi2_parte1.txt`; `f2/04-torneo/TORNEO_parte1.md` |
| a2 | r. 1046, rischio 8 | identità sbagliata in «**392–393 su 400**» | «392 occasioni su 392» (392 passaggi su 400). Il 393 non è nella consegna: compare solo come contatore di un altro evento in `ris_pd09.txt` | `f9-preproposta/05-tracciamento/CONSEGNA.md` f. 49; `PREVISIONI.md` f. 81 **[prel.]** |
| a3 | r. 790, riga 6 | 0,927 / 0,916 / 0,902 con «N = 4000» | il terzo valore ha **n = 1616** (fascia 1,5–2,5 s del terzo generatore); 4000 è il totale. I primi due: N = 4000 | `f2/04-torneo/risultati_A_parte2.txt` |
| a4 | r. 608, creativo | con l'evidenza negativa «**0,1 %**» | **1,6 % a 2 s, 0,1 % a 3 s** (0,0160 e 0,0011) | `f1/e30f9e2dd4d7/esito_sim.txt` |
| a5 | r. 696, A3 bis e A4 | «area prevista ancora *mostrata*: T 0–6,2 %; **D 0–1,5 %**» | 0–1,5 % è un'altra misura: «contenuta **e** ancora mostrata». La sola «mostrata» (A4) in D con pannello da 0,5 m vale **28–72 %** (lettura d1), 0–7 % (d2) | `f4/H-012/03-validazione/MISURE.md`; `out_A_D_w05.txt` |
| a6 | r. 636, H-013 | colonna «Soglia»: «≤ 2 % all'incrocio» | quella è l'attesa dell'avversario. La soglia di smentita è «scambi ≥ 10 % in (ii) o (iii)»; per la regola intera, scambi muti ≥ 2 % in (iii) | `f2/04-torneo/PREVISIONI_parte2.md` |
| a7 | r. 839, riga 55 | imbardata tollerata «0,87°» dal file dei risultati | il file dà **0,873–0,876°**; «≤ 0,87°» è l'arrotondamento per difetto del rapporto | `f6-specializzazione/02-slam/risultati.txt`; `MOTO_PROPRIO.md` §3 |
| a8 | r. 797, riga 13 | «i 12 cm … conto dell'arbitro» | il 12 cm (Gemini 335) è dell'**avversario**; lo ridà il metrologo («sigma 12.0 cm»). La selezione scrive solo «8–16 cm» | `f2/04-torneo/TORNEO_parte1.md`, riga H-001; `f3/H-012/03-metrologo/conti_metrologo.txt` |

## b. Frasi più forti di ciò che il file sostiene, con la riscrittura

**b1. «0 su 14 400» come misura** (r. 713 P1; r. 814 riga 30 [SIM]; r. 862 K-013).
`f4/H-012/03-validazione/MISURE_V2.md`, P1: «regge; a 0 e +20 cm **per costruzione**, a −20 cm è una misura».
*Riscrittura:* «0 su 4800 a −20 cm (misura; limite 0,06 %); 0 su 9600 a 0 e +20 cm (per costruzione: [COSTR])». Nella riga 30 la marca diventa «[SIM] a −20 cm, [COSTR] altrove».

**b2. «In tutti i casi è sotto il 20 %»** (r. 875, punto 3).
Falso sui file: 28,0–72,0 % in D con pannello da 0,5 m (`out_A_D_w05.txt`, «A4 mostrato: d1»); 46,8 e 34,7 % senza C6 (`v2_C6.txt`, righe D05); 49,8–67,6 % nel simulatore dell'avversario (`f4/H-012/01-avversario/risultati_a02.txt`).
*Riscrittura:* «con C6 e pannello da 1 m è sotto il 20 %; con il pannello da 0,5 m e senza C6 sale al 28–72 %».

**b3. «Chiusura per causa: 100 %, fantasma 0,06–0,07 s»** (r. 605).
Sono i numeri della sola forma a particelle. La forma semplice («media in ombra») tiene il 91 % nel transito e lo **0 % in sosta**. L'autore dichiara anche che per la sosta il modello a particelle e la verità non sono indipendenti (`f1/992c41c8860e/PREVISIONI.md`, «Notato dopo»).
*Riscrittura:* «chiusura per causa a particelle: 100 % (oracolo non indipendente sulla sosta); forma semplice: 91 % e 0 % in sosta».

**b4. Visione: «regge»** (r. 609).
Per il raggio al 95 % il file scrive «soglie di smentita non toccate; **il valore atteso era sbagliato** per eccesso» (previsto 1,5–3 s, uscito 1,0–1,4 s) (`f1/c85dbcc51ea6/PREVISIONI.md`, P3).
*Riscrittura:* «regge (P1, P2, P4); P3: soglia non toccata, valore atteso sbagliato».

**b5. A3: «T regge»** (r. 695).
Con la curva pessimista chi torna scende a **82,8–84,8 %**, sotto l'85 % (`MISURE.md`, riga A3). La soglia era scritta su «prosegue» e sulla miscela, quindi il verdetto resta, ma la riga va detta.
*Riscrittura:* aggiungere «torna 82,8–84,8 % con la curva pessimista».

**b6. S11: «corretta, 0 e 0»** (r. 959) **[prel.]**.
Lo stesso file dichiara smentite P1 e P2 per la macchina corretta: avvicinamento mancato 60 e attraversamento falso 86 su 400; uscite false 70 su 2800 (`f9-preproposta/05-tracciamento/CONSEGNA.md` f. 18). L'arbitro di f9 la chiama «prova d'esistenza, stesso autore».
*Riscrittura:* «corretta (variante `cor3`): 0 e 0, ma banco dello stesso autore, e la prima correzione mancava 60 avvicinamenti su 400».

**b7. Strato 2 fra i tagli: «Vale il secondo»** (r. 1033).
Il «secondo» è il triage di f7, **[prel.]**; il «primo» è il verdetto dell'arbitro. Un file non vagliato non prevale su un verdetto. Chi decide è il quarto addendum dell'utente.
*Riscrittura:* «vale il quarto addendum (la continuità visiva è l'obiettivo principale); il triage di f7 lo applica, [prel.]».

**Minori.**
- r. 786, riga 2: «[VER] sulla fonte». Il curatore ha letto 0,665 con lo strumento che riassume (`f3/fonti/FONTI_VERIFICATE.md`, punto 9, marca [r]). Aggiungere «[rias.]».
- r. 794, riga 10: lo «0» della mappa a quattro stati è per costruzione (il documento lo dice alla r. 607). Nella riga manca [COSTR].
- r. 840, riga 56: marca [CONTO], ma è una simulazione con N = 20 000. Più giusto «[SIM] nel modello, non vagliato».

## c. Cifre con un file che non le contiene

| # | Dove | Cifra | File citato | Dove sta davvero |
|---|---|---|---|---|
| c1 | r. 574, §3.8 punto 7 | 5,7 cm con focale 446,8 px | `f2/04-torneo/TORNEO_parte1.md` (non c'è) | `f2/04-torneo/esito_attacchi_parte1.txt` f. 2 |
| c2 | r. 570, §3.8 punto 3 | Gemini 335, 90°×65° | `f10-dati/04-embedded/PREVISIONI.md` (non c'è) | `f10-dati/04-embedded/geometria_sensori.py` f. 16; `INVENTARIO_E_DECISIONE.md` f. 19 |
| c3 | r. 797, riga 13 | 12 cm | `f2/05-selezione/SELEZIONE.md` (non c'è) | `f2/04-torneo/TORNEO_parte1.md` (vedi a8) |
| c4 | r. 609, visione | σ ≈ 66 m/s² | script `calcoli_p2_p3_p4.py` (non la calcola) | `f1/c85dbcc51ea6/CONSEGNA.md` f. 14, conto a mano |
| c5 | r. 1007 | 54 ore-persona | «`SOLUZIONE_V2.md`, B9» | somma dei nove «Costo:» dei blocchi (3+6+6+5+9+4+3+6+12) e §9, punto 9 |

**Non verificabili da me** (nessun file li porta): le ore delle fotografie delle sezioni (16:13:24, 16:15, 16:16: r. 907, 969–971); «previsioni del banco delle prestazioni, 16:10» (r. 915: il file oggi ha l'ora 16:43). Marcarle «ora dichiarata dalla sezione».

## d. Contraddizioni interne

1. **4,7 contro 5,1 ms** (r. 627 contro r. 883): vedi a1.
2. **Area ancora mostrata** (r. 696 contro r. 875): vedi a5 e b2.
3. **Nucleo con l'integrazione: 59,5 o 63,5?** La tabella (r. 1008) dà 59,5 ore-persona. La somma «80,5–87,5» (r. 1013) torna solo con 54 + 9,5 = 63,5. Il 59,5 del pianificatore parte da un nucleo di 48 ore (senza etichetta e senza area prevista) più 2 e 9,5 (`f9-preproposta/11-pianificatore/CONSEGNA.md` f. 25–31). Va scritto quale nucleo si somma.
4. **f9 «senza verdetto»** (r. 909, 917, 945) contro il riquadro in testa (r. 20): il verdetto dell'arbitro c'è dalle 16:37. Il documento lo dichiara, ma il §5.4 dice ancora «non dell'arbitro».
5. **Piano a 14 ore «manca»** (r. 997, 1026) contro `f9-preproposta/13-verdetto/VERDETTO_PREPROPOSTA.md` §1 bis, che lo dà. Dichiarato in testa, non integrato.
6. **Friburgo fra i «dati scelti»** (r. 977: 2,8 GB dentro i 4,04) e «non scaricato» (r. 972). Dichiarato; il totale scaricabile senza Friburgo è un altro.
7. **Ora della seconda previsione di f6:** il documento scrive 14:42:21 (r. 769), come `PREVISIONI.md`; `MOTO_PROPRIO.md` scrive 14:41:49. Discordanza fra file, da aggiungere al §4.4.

## e. Che cosa manca di importante

**Dai file delle fasi chiuse (f1–f6).**
1. **A2 (b) è «smentita alla lettera»**: con l'ombra a +20 cm lo strato 1 copre 0,171 m² oltre 0,60 m dal bordo vero, per al più 7 cm (`MISURE.md`; `out_A2.txt`). La r. 694 dice solo «costo dichiarato».
2. **«Con Pd = 0,9 le misure A3–A4 non valgono»** (`MISURE.md`, scostamenti): manca.
3. **Costo della media di 3 fotogrammi**: con il 2 % di misure anomale i falsi sul muro salgono al 5,7–14,9 % (`MISURE.md`; `out_WALL.txt`). C'è alla r. 283, manca nella riga `validazione-1` (r. 703), dove sta sopra la soglia del 10 %.
4. **Attacco alla specializzazione**: la tabella (r. 758–767) salta S4 («zero elementi del profilo assistivo provati oltre il nucleo») e S6a («cambiano 9 righe su 9»). S4 è alla r. 1170; qui serve almeno il rimando.
5. **Moto del sensore** (§3.6): mancano il costo di allargare la soglia (a 3 m la velocità minima vista passa da 0,07 a 0,27 m/s con 1°/s) e il drone al 7 % oltre 10 m (`MOTO_PROPRIO.md` §3; `risultati.txt`, S2 e S4).
6. **Regola violata in f4**: il primo lancio di `sim_v2bis.py` ha superato i 120 s (`MISURE_V2_bis.md`). Minore.

**Dalle estensioni, dopo la fotografia delle 16:35 (tutto [prel.], non vagliato dall'arbitro salvo f9).** Alle 17:19 le cartelle dei verdetti di f7, f8 e f10 sono ancora vuote (`ls`): «senza verdetto» resta vero per quelle tre. Il riquadro in testa non nomina questi file:
- `f7-estensione/13-soluzione/DECISIONE.md` (17:03). Propone: NO alla mappa voxel; «pannello alto almeno 1,5 m» **smentito per calcolo** (serve 1,7 m); invariante 1 smentito con un soggetto che non rimanda segnale. Tocca r. 1045 (rischio 7) e la condizione 3 del verdetto.
- `f7-estensione/12-prestazioni/BENCHMARK_INDIPENDENTE.md` (16:43).
- `f8-continuita/11-misure/BANCO_DI_PROVA.md` (16:38); `f8-continuita/13-soluzione/MODIFICHE_CONTINUITA.md` (16:52).
- `f10-dati/10-catena/CATENA.md` (16:42); `f10-dati/11-simulatore/SIMULATORE.md` (16:44); `f10-dati/20-validazione/` in corso (17:09).
- `f9-preproposta/13-verdetto/VERDETTO_PREPROPOSTA.md` (arbitro, 16:37), §1 bis: con 5 persone in 14 ore i cinque atti su dati simulati chiudono nel 100 % dei casi, la mappa vera nel 35,0 %, la continuità sul simulatore nell'1,1 % (42,7 % dividendo in due il compito lungo: ipotesi dell'arbitro). Sostituisce la lettura «si chiude T1 e non T2» (r. 1026) e il criterio a 3,3 / 3,8 / 4,5 / 6,0 ore, che diventa 3,1 / 4,1 / 5,2.

## f. Quante cifre ho controllato

Conto a mano, per sezione; «torna» = ritrovata nel file citato, o nel file grezzo quando esiste.

| Sezione | Cifre | Non tornano o imprecise | File sbagliato | Controllo sul |
|---|---|---|---|---|
| §3.6–§3.9 | 64 | 0 | 2 (c1, c2) | file grezzo e rapporto |
| §4.0–§4.1.1 (f1) | 116 | 1 (a4) | 1 (c4) | `PREVISIONI.md`, risultati |
| §4.1.2 (torneo) | 97 | 2 (a1, a6) | 0 | rapporti e file grezzi |
| §4.1.3 (f3) | 25 | 0 | 0 | `conti_metrologo.txt` |
| §4.1.4 (dodici attacchi) | 71 | 0 | 0 | `risultati_a*.txt` |
| §4.1.5–§4.1.6 (prove A, B, versione 2) | 145 | 1 (a5) | 0 | `out_*`, `v2_*`, `bis_*`; falliti ricontati con `awk` |
| §4.1.7–§4.1.9 (f5, f6, ripetibilità) | 88 | 0 | 0 | file; 7 `diff` rifatti |
| §4.2 (56 righe) | 130 | 3 (a3, a7, a8) | 1 (c3) | 56 righe su 56 |
| §4.3–§4.5 | 67 | 0 (b2 è una frase) | 0 | verdetto, file grezzi |
| Cap. 5 **[prel.]** | 235 | 0 | 0 | consegne e triage; 2 script rieseguiti |
| Cap. 6–7 | 80 | 1 (a2) | 1 (c5) | consegne, verdetto |
| **Totale** | **circa 1120** | **8** | **5** | |

**Tornano nel file citato circa 1100 su 1120 (98–99 %).** Delle altre: 8 non tornano o sono imprecise, 5 tornano ma in un altro file, circa 6 non sono verificabili da me (ore delle fotografie).

**Controlli che reggono e che valgono la pena di dire.**
- `v2_R8.txt`: 0 falliti su 14 400; `v2_R8_pd09.txt`: 13 su 4800, in 8 celle su 12; bracci 4800 / 4798 / 4789 su 4800; `v2_R8_cut.txt`: due bracci su tre a 0 su 4800. Ricontati da me.
- Ripetibilità: i sette `diff` danno zero righe numeriche diverse (solo i tempi).
- `controlla_parametri.py`: «D 93, M 5, C 20, I 32; ERRORI: 0». `geometria_sensori.py`: 1,62 / 1,55 / 1,46 m.
- Le impronte dei simulatori cominciano con `c0a94feb` e `dd7a5a1c` (`sha256sum`).
- I 26 asterischi del §4.2 sono 26.
- Le tabelle dei §4.1.4, §4.1.6, §4.1.7 e la tabella delle contraddizioni (r. 848–867) tornano riga per riga.

## Stati proposti

- «Il cap. 4 riporta fedelmente i file di f1–f6»: **verificato** sulle righe 584–901 (controllo esaustivo delle cifre, con le otto eccezioni del §a).
- «I cap. 5–7 riportano fedelmente i file di f7–f10 alla fotografia delle 16:13»: **verificato** sulle cifre; il contenuto resta **[prel.]**, e in parte superato (§e).
- «Le fonti esterne citate nella parte sono giuste»: **non verificato** da me.
- «I simulatori sono giusti»: **non toccato**: ho controllato la trascrizione, non il modello.

## Proposte

- `validazione-f11-1`: ogni riga del §4.2 porta due marche, una per lo stato e una per «misura / per costruzione». *Previsione:* almeno due righe cambiano (la 30 e la 10). *La smentisce:* nessuna riga con una parte per costruzione.
- `validazione-f11-2`: un controllo automatico a ogni aggiornamento: per ogni riga del §4.2, `grep` della cifra nel file citato. *Previsione:* oggi fallirebbe sulla riga 13 (il 12 cm non è nei due file citati). *La smentisce:* zero righe fallite sulla versione 1.

## Che cosa propongo dopo

1. Correggere a1–a8, b1–b7, c1–c5 e d3 prima di portare il documento in `documentazione/`.
2. Fare subito il primo aggiornamento che il documento stesso chiede: §5.4 e §6.1 sul verdetto di f9; poi §5.2, §5.3, §5.5 quando arrivano i tre verdetti che mancano.
3. Far leggere all'arbitro la decisione di f7 sul pannello (1,7 m contro 1,5 m): tocca una condizione obbligata del verdetto del nucleo.
