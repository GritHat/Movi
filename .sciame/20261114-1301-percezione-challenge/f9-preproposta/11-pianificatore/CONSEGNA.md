# S12, il piano a 24 e a 38 ore — f9, `sciame-pianificatore`

**In testa.** Lavoro dalle 2026-11-14T15:38:50+01:00 alle 15:52 (`date -Is`). **Cambi di stato proposti:** (1) «taglio minimo garantito a 24 ore» è **smentito** da un conto e da una simulazione del calendario; (2) non sta in 24 ore, alle stime dello sciame, **nemmeno il nucleo** né il mio piano minimo: la fattibilità la decide un fattore di velocità k mai misurato; (3) «38 ore» nel documento v0.5 è la catena in fila, non una durata. **Previsioni:** 12 scritte prima dei lanci (`PREVISIONI.md`); **5 smentite** (PR3 nell'intervallo, PR4, PR5, PR7, PR10 di poco: ero ottimista), 1 confusa e poi separata (PR8 → PR8bis), 2 reggono sulla soglia ma fuori dall'intervallo previsto (PR2, PR6), 4 reggono. **Scostamenti:** il modello è cambiato dopo il primo lancio (ordine dei compiti, sessione unica di registrazione), dichiarato prima del secondo; le stime a tre punti sono fissate a mano prima dello script e non sono cambiate; non ho letto `MISURE*`, `CONTROPROVE`, `TORNEO`, f1, f6 (non servono a S12); delle cartelle vietate ho visto solo i nomi (`ls`); nessuna fonte in rete aperta; la lunghezza è al limite delle tre pagine (circa 2400 parole, tabelle comprese). **Regole violate:** nessuna che io sappia.

**Che cosa vale la prova.** Stime, grafo e simulatore sono miei e condividono con lo sciame il modello linguistico e le ore dei blocchi di `SOLUZIONE_V2.md` (che al §9, punto 9, le dichiara senza prova). La prova decide **l'aritmetica del piano**, non le stime. Rifare, nella mia cartella: `timeout 120 python3 -I piano_mc_v1.py`, `timeout 120 python3 -I piano_mc.py`, `timeout 120 python3 ablazione.py`, `timeout 120 python3 conta_pre24.py` (seme 20261114, 4000 estrazioni per cella, 7–11 s l'uno) → `risultati_v1.txt`, `risultati_v2.txt`, `risultati_ablazione.txt`, `risultati_conta_pre24.txt`. Autocontrolli: una persona = somma delle durate (96,50 h, torna); persone illimitate = cammino critico (torna); braccio che deve stare 1999/2000; braccio che deve fallire 0/2000.

## 1. Verdetto proposto

- **S12-a, «taglio minimo garantito a 24 ore»: RESPINTA.** Controesempio in §2: 96,5 ore-persona probabili contro 39–65 disponibili, e 41,8 ore in fila contro circa 13.
- **S12-b, i due livelli e il contenuto dell'estensione (rete a lato, sensori laterali, selettore completo, confronto con la voxel) come ultime cose: APPROVATA CON CORREZIONI.** Non è un bilancio «a 38 ore»: è «solo dopo che il piano minimo gira dal vivo». Sostituisce S12-a il piano `pianificatore-f9-1` (§4).

## 2. Le ore (ottimista / probabile / pessimista, ore-persona)

| Modulo aggiunto dal taglio a 24 ore | O / P / Pess | Dipende da |
|---|---|---|
| A1 filtri spenti e controllo all'avvio (già condizione 1 del verdetto) | 1 / 2 / 4 | camera |
| A2 tre fasce di quota (S10) | 2 / 4 / 8 | mappa |
| A3 due ipotesi, ritaglio, pesi, regola previsto → perso (S3, S4) | 5 / 9 / 16 | tracce, cuneo |
| A4 taratura della precisione dichiarata (attacco 5; senza, «± X m» è un numero non provato) | 3 / 5 / 9 | A3, registrazioni |
| A5 massimo avvicinamento, probabilità d'intrusione, livelli (S6, S8) | 3 / 6 / 10 | regole, A3 |
| A6 macchina a stati delle attività (S11) | 3 / 5 / 9 | tracce, A3 |
| A7 disegno e suono per due profili (S5) | 3 / 5 / 9 | uscita |
| A8 selettore ridotto (S1) | 2 / 3 / 6 | A1 |
| **Somma dei moduli aggiunti** | **22 / 39 / 71** (media PERT 41,5) | |
| Integrazione che il nucleo non contava: interfacce e dati finti 2,5; innesto 3; dal vivo 4 | 5,5 / 9,5 / 19 | |
| Nucleo senza etichetta e senza area prevista (ore di `SOLUZIONE_V2.md`; O = 0,7 P, Pess = 2 P: ipotesi mia) | 32,5 / 48 / 92 | |
| **Totale del taglio a 24 ore** | **60 / 96,5 / 182** (PERT 104,7) | |

**Capacità** (ipotesi mia, non verificata: ore utili per persona 16 / 22 / 27 in 24 / 36 / 48 ore, meno 3 di chiusura per prove generali, video di ripiego e presentazione): 39 / 52 / 65 ore-persona con 3 / 4 / 5 persone in 24 ore. **Cammino critico** del taglio a 24 ore, anche con corsie parallele e persone illimitate: interfacce → Kalman → ciclo di vita e cuneo → due ipotesi → livelli → dal vivo → riprese → taratura = **41,8 ore** (25–77) contro circa 13 di costruzione. **Simulazione:** il taglio a 24 ore sta in **0 estrazioni su 4000** in ognuna delle 27 celle (3, 4, 5 persone; sensore posseduto, nuovo, assente; 24, 36, 48 ore) nel modello v2, e nello 0,0 % nel v1. Per starci con probabilità 80 % la squadra, con il sensore posseduto, dovrebbe andare **4,3 volte più svelta** delle stime in 24 ore (k* = 0,22–0,23), 3 volte in 36 (0,32–0,34), 2,4 in 48 (0,41–0,43). **Con 3, 4 o 5 persone la risposta non cambia** (k* si muove di 0,01–0,02): comanda la catena, non il numero di mani. Stato: **smentito nel modello delle stime**; le stime non sono misurate.

Il nucleo da solo, con l'integrazione: 59,5 ore-persona probabili (39–115), 26,8 in fila con le corsie (le «38 in fila» dell'audit, ipotesi 8, erano la lettura tutta seriale); k* = 0,32–0,34 in 24 ore.

## 3. Critiche

1. **«Garantito» senza una stima.** Il §6 della preproposta non porta un'ora, una dipendenza né un criterio di taglio. Prova: le righe 118–124 del file.
2. **Aggiunge a un piano già fuori bilancio senza togliere niente.** Il v0.5 (§9, punto 3) taglia a 24 ore «etichetta, area prevista e sensori laterali»; la preproposta rimette l'area prevista in forma più costosa (A3 + A4: 14 ore probabili) e aggiunge A5–A8 (19 ore).
3. **La prova sul sensore vero sparisce.** Della «prima ora con l'hardware» (v0.5, §8) resta solo il primo punto; rumore, ombra del pannello, vetro, latenza e i 30 passaggi (14 prove, 2 h 40 in due: 5,3 ore-persona) non sono nel taglio. Senza, la portata dichiarata e «± X m» non hanno un numero.
4. **Una camera sola è una risorsa in fila.** Controllo all'avvio, misure, prova dal vivo e riprese non si sovrappongono. Correzione: una sola sessione di registrazione, poi taratura e accettazione in parallelo sulle registrazioni (PR8bis: fine mediana da 31,8 a 29,3 ore, regge).
5. **L'ordine «prima tutta l'uscita, poi la mappa, poi le tracce, poi la previsione» mette l'obiettivo principale per ultimo.** Con 4 persone la previsione continua arriva a 21,3 ore di lavoro; con una persona fissa sulla corsia della continuità dall'ora 1 arriva a 17,0, e l'uscita con i dati finti passa da 7,9 a 9,1 (PR11, regge).
6. **Dipendenze logistiche assenti:** pannello opaco alto almeno 1,5 m e largo 1 m (condizione 3 del verdetto; audit, ipotesi 5), nastro a terra, luogo lontano da vetri e finestre.

**Dove la preproposta ha letto male.** (a) «24h vs 38h»: nel v0.5 le 38 ore sono la catena in fila delle 54 ore-persona (audit, ipotesi 8), non un bilancio né una durata; l'ipotesi del contratto è 24–48 ore, mai verificata. (b) Il ripiego del selettore a 24 ore, «Side NN OFF», spegne una rete che la stessa preproposta mette solo nell'estensione. (c) La compensazione della latenza (§2.1: «sempre») manca dall'elenco a 24 ore. (d) «Mappa 2D/2.5D» lascia aperta nel «minimo» una scelta che il v0.5 (§7) dà in valutazione. (e) «Sotto 1,1 m» nel nucleo è una **distanza dal sensore** («ostacolo di 15 cm invisibile sotto 1,09 m», blocco B1), non un'altezza: il §4 della preproposta la tratta come quota (tocca S10, non S12).

## 4. La versione corretta: `pianificatore-f9-1`, piano a due corsie costruito all'indietro dalla demo

**Meccanismo.** Ogni tappa sostituisce un finto con un vero dietro la stessa interfaccia: a ogni ora c'è una demo che gira, con la scritta dell'origine dei dati. Piano minimo: 59 ore-persona probabili (39–115,5), 23,5 in fila. Persona A: camera, controllo all'avvio, prima ora di misure, mappa, gruppi. Persona B (**fissa**): interfacce, una traccia con Kalman, ciclo di vita e cuneo, previsione continua, registro degli eventi. Persone C e D: dati finti, schermo, disegno della previsione, suoni e affidabilità persa, regole, poi innesto e registrazioni. Quinta persona: pannello, protocollo, video di ripiego, presentazione; **non accorcia la catena** (k* +0,02). Con 3 persone C fa da sola l'uscita (12,3 ore invece di 9,1).

| Tappa: che cosa gira | Ore di lavoro a k = 1, 4 persone (mediana) | k* a 24 / 36 / 48 ore | Se manca alla scadenza |
|---|---|---|---|
| T1 uscita: i cinque atti a schermo e in suono su dati **simulati**, previsione continua compresa | 9,1 | 1,26 / 1,85 / 2,33 | si misura k; via il secondo profilo sonoro |
| T2 mappa vera a quattro stati, controllo all'avvio, prima ora di misure | 14,0 | 0,80 / 1,18 / 1,48 | camera senza profondità all'ora di lavoro 2: piano B |
| T3 continuità sul simulatore: traccia → cuneo → previsione ritagliata, mai tolta | 17,0 | 0,66 / 0,97 / 1,22 | via l'ungherese e la regola «mobile» fine |
| T4 innesto: rilevamenti veri nelle tracce, su registrazione | 22,7 | 0,50 / 0,74 / 0,94 | atti 3–4 restano su dati simulati, dichiarati |
| T5 dal vivo: 15 cicli al secondo e latenza misurati; video di ripiego **subito** | 27,5 | 0,42 / 0,62 / 0,78 | la demo va sul video |
| T6 una sessione (45 passaggi, 10 soste), poi taratura e accettazione | 32,0 | 0,36 / 0,53 / 0,67 | a schermo «taratura: solo simulazione» |

Con 3 persone T6 ha k* 0,33 / 0,48 / 0,60; con 5, 0,38 / 0,56 / 0,72. Sensore **nuovo o mai provato**: T2 scende a 0,73 / 1,08 / 1,36. Sensore **assente**: T6 a 0,38 / 0,56 / 0,71, ma si perdono latenza, affidabilità persa, la prova scelta dal giurato e «prima prova sul sensore vero»; la fonte delle registrazioni è non verificata.

**Lettura.** Alle stime dello sciame (k = 1): in 24 ore si arriva a T1, in 36 a T2 e quasi a T3, in 48 a T3 e quasi a T4. Dopo T2 la demo mostra già tutti i requisiti della traccia: ostacoli, osservato contro incerto, feedback e perdita di affidabilità **dal vivo**; elementi mobili, interruzioni e continuità **su dati simulati dichiarati**.

**Criterio per cambiare strada (alla chiusura di T1).** k misurato = ora di lavoro vera di T1 diviso 9,1 (12,3 con 3 persone). Ci si impegna sulla tappa più alta con k* ≥ k misurato. Con 4 persone, in 24 ore: T1 chiusa entro 3,3 ore → T6; entro 3,8 → T5; entro 4,5 → T4; entro 6,0 → T3. In 36 ore: 4,8 / 5,6 / 6,7 / 8,8. In 48 ore: 6,1 / 7,1 / 8,6 / 11,1. **Previsione:** se T1 chiude a k ≤ k* della tappa scelta, quella tappa gira prima della chiusura. **La smentisce** una tappa mancata con T1 nei tempi: allora le stime sono sbagliate nelle proporzioni, non solo nella scala.

**Che cosa si taglia, in ordine.** (1) rete a lato, sensori laterali, voxel, selettore oltre il controllo all'avvio; (2) tre fasce di quota (limite già dichiarato); (3) probabilità d'intrusione; i livelli restano come rilettura della tabella (2 ore); (4) macchina a stati → registro di cinque eventi (2 ore); (5) seconda ipotesi: 7 ore probabili (4–12), parte solo se a T3 chiusa il resto del piano minimo (circa 15 ore × k) sta nelle ore rimaste; con la seconda ipotesi T6 ha k* 0,34 / 0,49 / 0,62; (6) ungherese, regola «mobile» fine. **Non si taglia mai:** «non osservato» mai libero e controllo all'avvio; il cuneo «possibile presenza»; i contatori dell'affidabilità; la previsione continua mostrata come previsione con la sua regione; la scritta sull'origine dei dati e sulla taratura. Il predittore lo sceglie f8: qui è una casella con un bilancio.

## 5. Rischi e contromisure

| Rischio | Segnale | Contromisura |
|---|---|---|
| Hardware assente o guasto | nessun fotogramma di profondità con i filtri spenti all'ora di lavoro 2 | registrazione grezza dei cinque atti fatta **prima** dell'evento, se le regole lo ammettono (non verificato); tutto lo sviluppo gira già sul riproduttore |
| Latenza | 155 ms noti contro la soglia di 150 (verdetto, R7) | misura nella prima ora; suoni preregistrati, audio via cavo; la cifra misurata a schermo, nessuna soglia promessa |
| Luce in sala | pixel validi sotto il 90 % sulla parete | cinque minuti di misura **nel punto e all'ora della demo**; via da finestre e vetri; ripiego sul video |
| Integrazione | la catena dei cinque atti sul riproduttore non gira dopo una modifica | interfacce congelate all'ora 1; un responsabile dell'innesto; nessuna modifica entra se rompe la catena |
| Prova con il pannello | celle «libero» dentro l'ombra vera; banda senza dato di 5–9,5 cm (audit, 10) con margine sotto 10 cm | pannello procurato prima; nastro a terra; attore a non più di 2,3 m; una sola persona dietro; giurati fuori dal campo; al giurato due sole scelte (quando coprire, quando fermarsi) |
| Precisione dichiarata non tarata | T6 non raggiunta | «± X m» esce con «taratura: solo simulazione»; nessuna percentuale di confidenza |

## 6. Che cosa NON promettere

«Garantito»; una data senza k misurato; i cinque atti dal vivo (a k = 1 non ci si arriva nemmeno in 48 ore: k* 0,78); «± X,XX m | conf Z %» come numero tarato; 400 passaggi simulati più 30 veri dentro le 24 ore; «almeno 15 cicli al secondo» con tutti i moduli (mai misurato sulla catena vera); l'estensione entro 48 ore; «validato», «bassa latenza», due persone dietro il pannello.

## 7. Costo, stati, non verificato

- **Costo di S12 corretta:** 9,5 ore-persona d'integrazione (5,5–19) più 3 ore di chiusura a testa. Calcolo per ciclo: nessuno (S12 non aggiunge codice nel ciclo).
- **Stati proposti.** «Il taglio a 24 ore sta in 24 ore»: **smentito** nel modello delle stime. «Il numero di persone fra 3 e 5 decide»: **smentito** nello stesso modello (0,33 → 0,38). «Il piano minimo sta in 24 / 36 / 48 ore»: **non risolto**; lo decide k alla tappa T1.
- **Non verificato:** ogni stima in ore, mie e dello sciame; le ore utili per persona (con 30 ore di costruzione a testa T6 avrebbe ancora k* 0,88); durata, squadra, sensore posseduto; se il simulatore di f4 fa da sorgente in tempo reale; il pannello; la luce in sala; i verdetti di f7 e f8 su S10, S11 e sul predittore; l'effetto di spezzare in due i compiti lunghi della catena (non modellato).
- **Dopo:** chiedere all'utente durata, numero di persone, camera posseduta e già provata, e se è ammesso lavorare prima dell'evento; poi rifare la tabella del §4 con quei valori.
