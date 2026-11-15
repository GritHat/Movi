# MoVi pitch IT v4 — copione

Video: `video/consegna/MoVi_pitch_IT_v4.mp4`, durata 169.74 s. Voce: Kokoro `im_nicola`, velocità 1,0. Tutto ciò che si vede è un'illustrazione; tutte le cifre sono di simulazione (riga fissa a schermo «PROTOTIPO SIMULATO · ILLUSTRAZIONE»).

Si rigenera con: `python3 video/progetto_v4d/voce/genera_voce_v4d.py`, poi `sh video/progetto_v4d/fai_tutto.sh`.

## Voce e tempi

| clip | inizio (s) | durata voce (s) | testo |
|---|---|---|---|
| A1 | 0.25 | 7.57 | Un drone entra in una nuvola. Per molti sistemi, non c’è più. Ma ciò che smetti di vedere è ancora lì. |
| A2 | 8.12 | 11.06 | MoVi è un sistema di percezione per veicoli senza equipaggio. Tiene traccia di ciò che non vede più: una regione dove può essere, con una confidenza che cala nel tempo. |
| K | 19.48 | 5.60 | Dove non ha guardato, MoVi non dice mai «libero». Dice: presenza possibile. |
| F1 | 25.48 | 5.49 | Primo caso: volo ad alta velocità. Un’avaria improvvisa, una fiammata. |
| F2 | 31.27 | 10.18 | Rallentiamo il tempo. In sessanta prove simulate su sessanta, MoVi dichiara l’evento entro un secondo, e che le camere non sono più affidabili. |
| F3 | 41.75 | 3.33 | E non dice mai «libero» dove c’è un frammento. |
| H1 | 45.75 | 4.23 | Secondo caso. Un drone segue un oggetto veloce. |
| H2 | 50.29 | 3.86 | Accanto, due droni si scontrano: fuoco, fumo, detriti. |
| Z | 54.45 | 5.68 | I sensori si attivano: radar, camera, infrarosso. Un solo nucleo ascolta. |
| P0 | 60.43 | 2.63 | Guardiamo con gli occhi del drone. |
| P1 | 63.36 | 3.07 | La fusione: tre sensori, un solo quadro. |
| P2 | 67.66 | 4.82 | La stima, con un filtro di Kalman, prevede dove può essere il bersaglio. |
| P3 | 72.78 | 5.94 | Il fumo acceca i sensori. La confidenza cala, secondo una formula dimostrata. |
| P4 | 79.02 | 4.57 | Ogni punto ha uno stato: lo vedo; non lo vedo, ma è qui; non lo so. |
| P5 | 83.89 | 2.80 | Il drone viene avvisato subito. |
| P6 | 88.29 | 3.73 | Poi i sensori tornano, e MoVi ritrova il bersaglio. |
| W | 92.59 | 5.36 | Con l’ultima correzione, in prova, l’avviso arriva prima del primo frammento. |
| S | 98.24 | 7.45 | Cinquantanove prove simulate su cinquantanove. E la regione del bersaglio resta, sessanta su sessanta. |
| R | 106.00 | 7.90 | Sotto, una catena a cinque strati: sensori, fusione, stima, mappa a stati, avviso. Pronta per hardware dedicato. |
| I | 114.20 | 12.31 | Dietro c’è una ricerca bibliografica, matematica e sperimentale: oltre quattrocento riferimenti, e un documento tecnico di oltre cento pagine, con dimostrazioni e risultati. |
| U1 | 126.81 | 5.04 | Può salvare vite. Una persona non vedente, avvisata dell’auto. |
| U2 | 132.15 | 3.93 | Un braccio robotico che si ferma prima dell’operatore. |
| U3 | 136.38 | 3.95 | Un muletto automatico che sa di chi è dietro lo scaffale. |
| U4 | 140.63 | 3.48 | Un’auto che ricorda il pedone dietro il furgone. |
| U5 | 144.41 | 3.63 | Una pattuglia che non perde di vista l’auto che segue. |
| U6 | 148.33 | 4.37 | Un satellite che trova il frammento pericoloso fra i detriti. |
| U7 | 153.01 | 3.16 | Un drone veloce, nel fumo e nel maltempo. |
| U8 | 156.51 | 4.45 | Una nave nella nebbia. Sono applicazioni possibili. |
| E | 161.25 | 7.13 | MoVi tiene traccia di ciò che smette di vedere. Del gruppo SDMs, per The Big Hack duemilaventisei. |

## Cifre dette o scritte, con la fonte

Registro: `video/consegna/MoVi_registro_cifre_final.md` (chiave fra parentesi quadre).

| cifra | dove | fonte |
|---|---|---|
| 60 su 60: evento dichiarato e camere dichiarate non affidabili entro 1 s | caso 1 (voce e scheda); scheda «60/60» delle prove | [V-2] 60/60, simulato, innesco ottimista |
| mai «libero» dove c'è un frammento | caso 1 (voce e etichetta), senza cifra | [V-1] 0/200 e 0/60, simulato |
| 59 su 59: drone avvisato prima del primo frammento | scena eroe (scheda 5, voce, quadro delle cifre) | [F7R-C1-AVVISO] 59/59, simulato, correzione in prova: detto a voce e scritto |
| 60 su 60: regione del bersaglio mantenuta | quadro delle cifre, voce | [F7R-C1-LIBERO] regione mantenuta 60/60, «libero» 0/60, simulato |
| 200/200 avvisato in tempo, lunga portata | prove | [LP-1] 200/200, simulato |
| oltre 100 pagine, oltre 400 riferimenti | prove, voce | messaggio del commit 9976563 («documento tecnico v3 (108 pagine)… 410 riferimenti»): non ricontati qui |

## Illustrativo, non un dato

- «non visto da 6,8 s» nella scena del cono: valore d'esempio.
- Matrice 4×4, curva della confidenza e barra: illustrative, senza valori. La formula `C(τ) = 1 − e^(−r²/2σ²(τ))` viene dal pacchetto esterno: non verificata qui sulle fonti del progetto.
- «Pronto per hardware dedicato, per progetto»: intenzione di progetto, non una prova su hardware.
- Gli otto casi d'uso finali sono applicazioni possibili (etichetta su ogni tavola), non risultati.

## Non incluso

- La riga «Indagine sui progetti di R&D del committente» e la frase corrispondente nella voce: il sistema dei permessi ha negato due volte il comando che la conteneva, e la conferma dell'utente è arrivata solo tramite il coordinatore. Nei documenti del progetto l'indagine non risulta.
