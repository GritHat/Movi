Canarino: sciame-canarino-fe9992e292215898

# Consegna — sciame-creativo, f8 (continuità visiva), f1, corsia B

Lavoro dalle 2026-11-14T15:14:10+01:00 alle 15:39 (`date -Is`). Tutto è **simulazione**, a sensore fermo, pedone puntiforme: nessun fotogramma vero.

## 1. Scostamenti e regole violate

- **Il disegno che propongo (v2) è nato dopo** aver visto fallire quello registrato (v1): tre mie previsioni su v1 sono smentite, tre su v2. Tutto è in `PREVISIONI.md`, con le ore.
- **Due prove di fumo viste prima dei lanci registrati** (8 e 3 passaggi, stessi semi); codice non toccato fra fumo e lancio. Dopo i lanci di v2 ho aggiunto opzioni esplorative: la copia registrata è `cono2_registrato.py`.
- **Indipendenza.** Scena, filtro e quattro comportamenti di prova (prosegue, sosta, torna, esce dal lato lontano) sono copie degli script dell'avversario (`f2/04-torneo/scena_parte3.py`); i percorsi di «taratura» vengono da un altro suo generatore (`g1`, `torneo_parte2.py`). Sono miei: «rallenta», «svolta», il predittore, le misure, la regola del nucleo riscritta in questa scena (senza la correzione C6, griglia fino a 6 m). **Ho letto il generatore di prova prima di progettare**: indipendente è il codice, non la mia conoscenza. Stesso modello linguistico per tutto.
- **Un file temporaneo fuori dalla mia cartella** (nella cartella provvisoria della sessione), poi cancellato.
- **Non letti:** `f6-specializzazione/`, `proposta/`, `MISURE*.md`, `AUDIT.md`, `CONTROPROVE.md`. Q3 qui sotto vale solo per la previsione del nucleo e per la demo.
- La previsione P-creativo-7 era mal posta (§3, critica 6). Nessuna soglia d'errore «utile» dichiarata prima.

## 2. Q3 — l'imperativo è rispettato? (le parti che mi competono)

| Parte | Esito | Prova |
|---|---|---|
| Nucleo, regola dell'area prevista (blocco B5, strato 2) | **non rispettato** (continuità) | Rifatta nella scena del torneo, la regola mostra una stima nel 38–39 % dei cicli senza osservazione se il soggetto sosta, nel 34–35 % se esce dal lato lontano, nell'86–88 % se prosegue (pannello da 1 m; da 2 m: 28 %, 28 %, 48 %). `esito_v1_w1.txt`, `esito_v2_w2.txt`. Nella geometria della demo `SOLUZIONE_V2.md` §1 dà l'area ancora mostrata alla riemersione nello 0–6,2 % dei transiti |
| Nucleo, cerchio «al 95 %» (blocco B4) | **non rispettato** (taratura per comportamento) | Contiene chi torna nel 48 % a 2 s (n = 29) e chi esce dal lato lontano nel 51 % e 48 % a 2 e 3 s (n = 100). Il torneo dava 56–66 % e 55–69 % |
| Nucleo, incertezza controllata | **non rispettato** | Passata la soglia il sistema smette di disegnare, invece di cambiare segno; il cerchio non usa ciò che il sensore vede (torneo, parte 3: 51 % dell'area su celle viste libere a 2 s) |
| Nucleo, sicurezza (strato 1, invarianti) | **rispettato**, non toccato | Le mie proposte non producono «osservato» né «libero» |
| Demo e criterio R3 | **rispettato in parte** | L'identità al ritorno c'è; manca una misura dal vivo della precisione della previsione |

## 3. Critiche

1. **Il nucleo spegne la previsione proprio quando serve.** Sosta dietro il pannello: stima assente nel 61–72 % dei cicli nascosti (righe sopra).
2. **Il «95 %» del cerchio non è un 95 %** per chi torna o svolta: 48–51 % (`esito_v1_w1.txt`, colonna «cerchio contiene»).
3. **Una regione «al 90 %» unica presuppone una miscela di comportamenti che nessuno conosce.** La mia v1 (400 percorsi registrati pesati 60/15/10/15, più uno sfondo) è smentita: a 1 s copre il 64–71 % di chi sosta, torna, svolta o esce lontano; la regione al 50 % copre il 3–9 % a 2 s. Senza sfondo: 1 % a 3 s (`esito_v1_w1_eps0.txt`).
4. **Fra l'ingresso e l'uscita attesa nessuna evidenza distingue chi prosegue da chi si è fermato.** Ogni regione che segue solo il fronte perde chi resta indietro. La cura è geometrica: tenere tutta la scia.
5. **Chi lascia il percorso non si copre con una regione piccola.** Con il ventaglio della libreria (virate di 45–90°): 57–94 % fino a 3 s, al prezzo di 20–44 punti d'ombra in più. Con virate di 30–135° (esplorativo): 92–98 % fino a 3 s, ma la regione è il 97–98 % dell'ombra a 2 s.
6. **Un tabellone aggregato inganna.** Lo stesso predittore (fronte + scia, regione al 90 %, a 3 s) dà 38 % o 67 % secondo la miscela ipotizzata (`esito_tabellone.txt`). Il conto va fatto per comportamento, e dietro un pannello vero il comportamento non si vede.
7. **Con 30 prove non si distingue 0,90 da 0,80** (soglia 24 su 30: passa nel 97,4 % e nel 60,7 %); servono 60 prove (92,7 % e 21,3 %).

## 4. Stati proposti

| Enunciato | Stato |
|---|---|
| Il nucleo emette una stima in ogni ciclo senza osservazione | **Smentito** (28–39 % su sosta e uscita lontana; mia riscrittura) |
| Il cerchio del nucleo è tarato per comportamento | **Smentito** (48–51 %) |
| Una miscela di percorsi con sfondo (v1) è tarata per comportamento | **Smentito** |
| Fronte + scia copre chi resta sul percorso (prosegue, rallenta, sosta, torna) da 0,5 a 5 s | **Sostenuto dai dati**: 99–100 % (pannello 1 m), ≥ 96 % (2 m), ≥ 98 % con l'ombra stimata 20 cm più stretta, 96–100 % su un terzo generatore; 100 passaggi per cella |
| La regione fronte + scia resta limitata | **Sostenuto dai dati**: al più 39 % dell'ombra (1 m) e 53 % (2 m) in media per tempo e comportamento; mai oltre il 63 % e il 76 % |
| Fronte + scia copre chi lascia il percorso | **Smentito**: 0–21 % da 2 s |
| Il ventaglio 45–90° copre chi svolta almeno al 75 % | **Smentito** oltre 3 s (42 %, 32 %; uscita lontana 57 % a 3 s) |
| Il fantasma batte «fermo» e «velocità costante» | **Sostenuto dai dati** nell'aggregato (a 2 s: 1,02 m contro 1,37 e 1,69; a 3 s: 1,51 contro 2,02 e 2,80); **smentito** per chi torna (1,08 m contro 0,46 di «fermo») |
| Il calcolo sta nel ciclo a 15 Hz | **Sostenuto dai dati**: 0,48 ms per ciclo (p95 0,56), 4,3 ms all'ingresso; Python puro, macchina condivisa |
| Il pannello virtuale misura la precisione dietro un pannello vero | **Non risolto**: lo decide l'hardware (§5) |

## 5. Proposte per Q4

**creativo-2 — «Fronte, scia, ventaglio»** *(cono degli uragani; scenari senza probabilità; cerchio di massimo allontanamento della ricerca in mare)*
- *Analogia tradotta.* Il cono dei meteorologi non viene dalla covarianza di un modello: è l'**area spazzata** da cerchi tarati sugli errori storici (fonte letta). Qui: quando la traccia entra nell'ombra nascono 400 «membri», percorsi rettilinei registrati trapiantati sul punto e sulla velocità d'ingresso. Metà sono il **fronte** (prosegue). Metà sono la **scia**: lo stesso percorso congelato a un istante uniforme fra l'ingresso e la propria uscita dall'ombra, cioè chi rallenta, si ferma o torna sui suoi passi. A ogni ciclo un membro che cade in una cella vista libera oltre una fascia di 0,2 m pesa un decimo: le bocche dell'ombra sono sorvegliate, e chi «sarebbe dovuto uscire» sparisce. La regione al livello p è l'**unione** delle celle più dense di ciascuno scenario: nessuna scommessa sulla miscela.
- *Enunciato.* Per chi resta sul proprio percorso la regione dichiarata «90 %» lo contiene almeno nel 90 % dei cicli nascosti, a ogni tempo fra 0,5 e 5 s e per ogni comportamento; non sta mai su celle viste libere oltre la fascia; per chi lascia il percorso vale lo strato 1 del nucleo, che non cambia.
- *Prima → dopo* (pannello 1 m, sosta): stima mostrata 39 % → 100 % dei cicli nascosti, informativa (sotto metà dell'ombra) nel 99 %; copertura a 2 e 3 s: 82 % e 91 % (cerchio) → 100 % e 99 %; area a 2 e 3 s: 62 % e 80 % dell'ombra (cerchio, torneo) → 37 % e 34 %. Punteggio logaritmico (più basso è meglio) a 3 s sulla sosta: 0,67 contro 4,41 del filtro; ma 10,6 contro 5,7 per chi esce lontano.
- *Vincoli.* Fuori percorso dice «possibile presenza», non una percentuale. La regione al 50 % scende sotto il 50 % a 5 s per chi rallenta o sosta (31 % e 42 %, pannello 2 m): non è tarata lì. Il terzo scenario, il **ventaglio**, si accende solo se si accetta il suo prezzo (critica 5).
- *Che cosa è parametro:* libreria di percorsi per classe, fascia, cella, numero di membri. *Da riprovare:* corpo largo e occlusione parziale, sensore in moto (maschere ricalcolate a ogni ciclo), più soggetti.
- *Chi la prova:* tracciamento e kalman; avversario; statistico per la taratura.
- *Falsificatore (≤ 5 minuti), eseguito.* Stesso predittore su traiettorie di un terzo autore (`traiettoria()` del rovesciatore: pannello da 1,5 m, soste di 2–6 s). **Atteso, scritto prima:** celle con n ≥ 30 al 90 % o più; smentita sotto l'85 %. **Esito: regge**, 96–100 % in 12 celle su 12 (`esito_terzo.txt`); informativa nell'89–97 % dei cicli nascosti (nucleo 31–63 %). *Prossimo:* corpo largo 40 cm e Pd 0,7; atteso ≥ 90 %, smentita sotto l'85 %.

**creativo-1 — «Il pannello virtuale»** *(gioco del cucù; verifica a posteriori delle previsioni del tempo; il «fantasma» del giro migliore)*
- *Meccanismo.* Una **copia** della catena di tracciamento riceve le misure con un cuneo cancellato via software, mentre la catena vera continua a vedere. Sulla copia gira lo stesso predittore; a ogni ciclo si confronta con la posizione davvero osservata. A schermo: la persona vera e il suo fantasma tratteggiato insieme. Un tabellone conta «dentro il 50», «dentro il 90», «fuori» **per comportamento** (riconosciuto dopo, dalla traccia vera) e per tempo senza osservazione, con l'intervallo. Lo stesso registro, raccolto prima, tara i parametri su dati diversi da quelli della prova.
- *Guadagno.* La giuria misura la precisione dal vivo, anche provando a ingannarla: fermarsi, tornare, svoltare. Circa 22 passaggi in 3 minuti (conto: 7,6 m di campo a 1,25 m/s più 2 s di giro).
- *Vincoli.* La copia non tocca mai l'uscita vera. Non prova la maschera d'ombra di un pannello reale, l'occlusione parziale, i buchi di profondità. Servono 60 prove per separare 0,90 da 0,80.
- *Chi la prova:* validazione, statistico, visualizzatore.
- *Falsificatore.* Su hardware: 30 passaggi dietro un pannello vero (verità da una seconda camera che il sistema non usa) contro 30 con il pannello virtuale, stesso comportamento. **Atteso:** differenza di copertura sotto 15 punti. **Smentita:** oltre 15 punti: il pannello virtuale non vale come misura. **Non verificato.** In simulazione il confronto è cieco (stesso codice).

**creativo-3 — «L'elastico e la rosata»** *(regia televisiva e moviola; tiro a segno)*
- *Regola di visualizzazione.* (a) All'ingresso il segno pieno diventa fantasma tratteggiato nello stesso punto: nessun salto. (b) Il fantasma non supera 2,5 m/s e **non sparisce mai**: quando il fronte è estinto o la regione supera metà dell'ombra cambia segno («diffuso»: regione a righe, fantasma vuoto, età in secondi). (c) Alla ricomparsa un **elastico** unisce per un secondo il fantasma alla prima misura, con la lunghezza in centimetri, e il colpo finisce su un bersaglio i cui anelli sono le regioni al 50 % e al 90 %: l'errore si mostra, non si nasconde nel taglio.
- *Numeri (fronte + scia, pannello 1 m).* Passo massimo 0,12–0,17 m per ciclo (limite 0,167 per costruzione). Passi all'indietro oltre 2 cm: 0,2 % dei cicli se prosegue, 6–18 % negli altri casi (**non verificato** che avvengano solo dopo l'uscita attesa). Salto mediano alla ricomparsa: prosegue 0,43 m (0,32 con il fantasma sullo scenario più probabile; velocità costante 0,28); rallenta 0,78 contro 1,50; sosta 0,91 contro 3,55; torna 1,52 contro 2,13 (e 0,12 di «fermo»). Prima misura entro 0,45 m dalla regione al 90 %: 393 su 393 sul percorso, 31 su 50 per chi svolta.
- *Vincoli.* Il fantasma non usa mai la grafica di «osservato». Il canale sonoro per chi non vede non è progettato qui.
- *Chi la prova:* visualizzatore, designer dell'interazione.
- *Falsificatore (5 minuti, tre persone).* Sei filmati di 10 s, tre con questa regola e tre con il nucleo; domande: «dov'è adesso?», «il sistema lo sta vedendo?». **Atteso:** almeno 16 risposte giuste su 18 con la regola nuova. **Smentita:** 12 o meno. **Non eseguito.**

## 6. Che cosa propongo dopo

1. Triage: adottare «fronte + scia» come strato 2 del nucleo, con la dicitura «sul percorso»; decidere se il ventaglio vale il suo prezzo (decisione dell'utente).
2. L'attacco a creativo-2 con corpo largo 40 cm e Pd 0,7, e con due soggetti nella stessa ombra.
3. Un microfono come indizio «passi sì / passi no» per scegliere fra fronte e scia: idea non provata, mai per la sicurezza.

**Rifare** (in questa cartella; ogni lancio sotto 60 s): `PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 cono2.py 1.0 prosegue,rallenta,sosta,torna,svolta,lontano 100 0.0 AB` (fronte + scia; `ABC` con il ventaglio; `2.0` per il pannello largo; `-0.2` al posto di `0.0` per l'ombra stretta); `cono.py` per v1; `timeout 120 python3 terzo.py`; `timeout 60 python3 tabellone.py`. Semi fissati negli script.

**Fonte letta:** [NHC, definizione del cono](https://www.nhc.noaa.gov/aboutcone.shtml) («the area swept out by a set of circles… two-thirds of historical official forecast errors over a 5-year sample»). Il «cerchio di massimo allontanamento» e la verifica a posteriori dei meteorologi: non verificati sul testo.
