# Misure delle prove A e B — H-012, f4 (`sciame-validazione`)

**In testa.** Eseguito fra le 14:24 e le 14:35 del 14 novembre 2026 (`date -Is`). Simulatore scritto da capo in Python puro (`sim_h012.py`), seme base 5101, 400 passaggi per cella come da progetto: con zero fallimenti il limite superiore al 95 % è 0,75 % per cella. Tutto è **simulazione a sensore fermo**: niente è provato su hardware.

**Cambi di stato che propongo.** (1) A1 **regge** solo con la lettura «ombra più celle non osservate contigue»; con la lettura «sola ombra dilatata» è **smentita**. (2) A7 **regge** solo se il rilascio per osservazione non guarda la posizione prevista; con la prova del raggio sulla posizione prevista è **smentita**. (3) A3 è **smentita** su «prosegue» nella geometria della demo con il pannello da 0,5 m. (4) K-007 **non risolta**: la decide la curva di rumore vera. (5) Lo strato 2 è quasi sempre già spento alla riemersione (K-004).

**Scostamenti dal progetto congelato.**
- Il progetto non diceva la probabilità di rilevamento né la curva di rumore per A: uso Pd = 1 e la curva nominale; la curva pessimista e Pd = 0,9 sono corse in più.
- La portata della griglia in T (6 m) non era scritta: la fisso ora; dà i 7,82 m² d'ombra del torneo.
- Geometria D con l'attore a 3 m **non simulata**: sulla linea a 3 m ogni punto dista almeno 3 m, cioè la portata della griglia. Per aritmetica: zero misure.
- Il filtro tratta i due assi separati (R diagonale approssimata). A6 è calcolata sui passaggi singoli accoppiati, senza occlusione reciproca.
- Due correzioni al codice dopo il primo lancio (un doppio conteggio nella sensibilità, contatori aggiunti): ho rifatto tutto; i file `out_*.txt` vengono dal codice finale.
- **Notati dopo** (file `extra.py`, fuori dal progetto): la causa del risultato A3 in D; i falsi «mobile» nel primo secondo di una traccia ferma.
- Con Pd = 0,9 le misure A3–A4 **non valgono**: un mancato rilevamento vicino all'ombra viene contato come riemersione. Uso quella corsa solo per A1.

## Prova A

Letture eseguite. Celle contigue: (i) sola ombra dilatata; (ii) ombra dilatata più non osservate contigue (fuori portata, fuori campo). Rilascio: (R-a) una cella esce se «libero» per 3 fotogrammi oltre la fascia, cioè mai con il pannello fermo; (R-b) prova del raggio sulla posizione prevista. Metà dell'ombra: (d1) area dell'ombra in portata; (d2) larghezza dell'ombra alla distanza del pedone.

| # | Soglia e previsione del responsabile | Esito (N = 400 per cella) | Verdetto |
|---|---|---|---|
| A1 | un nascosto fuori dallo strato 1; previsto 100 % | **Lettura (ii):** 0 fotogrammi fuori in 48 celle (T e D, 19 200 passaggi); limite 0,75 % per cella. Anche con curva pessimista e con Pd = 0,9. **Lettura (i):** fuori in 400 passaggi su 400 in ogni cella «lontano» (il soggetto esce dalla portata restando in ombra). **Mio falsificatore N2:** 0 in tutte le celle | (ii) **regge**; (i) **smentita** |
| A1, sensibilità (mia) | — | T, pannello 1 m, 1200 passaggi per riga. Corpo 40 cm: errore −20 cm 0 fuori; −30 cm 107 (8,9 %); −40 cm 1075 (89,6 %). Corpo 60 cm: −20 cm 0; −30 cm 399 (33,3 %). Errori positivi fino a +50 cm: 0 | il margine oltre i −20 cm ipotizzati è **meno di 10 cm** |
| A2 (a) | > 0 % nei termini del sistema | non misurata: zero per costruzione | controllo, non prova |
| A2 (b) | una cella davvero visibile oltre 0,60 m dal bordo vero | a −20 e 0 cm: 0 m² (massimo 0,40 m). A +20 cm: 0,171 m² in T-1 m (massimo 0,67 m), 0,041 in T-2 m, 0,010 in D-0,5 m, 0 in D-1 m. Viene dal mio modello d'errore, che sposta i bordi di un angolo: oltre la linea del pedone l'errore supera i 20 cm | **smentita alla lettera**, per al più 7 cm; con errore costante sarebbe zero per costruzione |
| A2, costo (mia) | — | quota dello strato 1 su suolo davvero visibile: 14–41 % in T (2,2–5,3 m²), **37–68 % in D** (1,1–2,3 m²). Celle nascoste fuori dallo strato 1: 0 m² in 12 casi su 12 | descrittiva |
| A3, definizione del responsabile | < 85 % su «prosegue» o sulla miscela 60/15/10/15; previsto 0,86–0,94 «prosegue», 0,50–0,70 «torna» | **T:** prosegue 95,8–100 %; sosta 96,0–100 %; torna 90,2–92,2 % (82,8–84,8 % con la curva pessimista). **D, pannello 1 m:** 97,0–100 %. **D, pannello 0,5 m: prosegue 14,2–16,5 %**; sosta e torna 100 %. Errore tipo ≤ 1,8 punti. Con tolleranza 0,20 m, a −20 cm: 0 % ovunque | T **regge**; D-0,5 m **smentita** |
| A3, definizione mia (contenuta e strato 2 ancora mostrato) | — | T: 0–6,2 % con d1, 0 % con d2; D: 0–1,5 % | **smentita** ovunque |
| A4 | descrittiva; previsto 30–70 % (pannello 1 m), 0–10 % (2 m) | «prosegue», strato 2 ancora mostrato: T-1 m 2,2–6,2 % (d1), 0 % (d2); T-2 m 0 %; D-0,5 m 28–72 % (d1), 0–7 % (d2). Buio medio in T-1 m: 1,9 s, non 1,70 | fuori dalla fascia prevista per 1 m; dentro per 2 m |
| A5 | < 95 %; previsto ≥ 95 % | 100 % in ogni cella con riemersione; limite inferiore 99,25 % | **regge** |
| A6 | > 0 scambi muti; «ambigua» nel 60–100 % | 0 scambi muti su 6400 riemersioni; «ambigua» dichiarata nel 94,5–100 % | **regge**, ma per costruzione della regola |
| A7 | oltre 10,2 s, o un rilascio per osservazione a soggetto nascosto | **R-a:** nessuna durata oltre 10,00 s; «lontano» 400 su 400 a T_g; nessun rilascio per osservazione. In «torna» con pannello 2 m, 3 passaggi su 1200 riemergono dopo T_g, ad avviso già caduto. **R-b:** rilascio a soggetto nascosto in sosta 92,5–99,5 % (T) e 80–97 % (D); torna 35–55 % (T); lontano 92–100 %; prosegue 0–8,5 % | R-a **regge** (per costruzione); R-b **smentita** |

**Causa del 14–17 % (notata dopo, controllata).** Con il corpo largo la misura è il centro della parte visibile: mentre il corpo entra nell'ombra il centro misurato rallenta, il filtro abbassa la velocità, e alla riemersione la misura sta davanti alla previsione. Sostituendo la misura con il centro vero del corpo, sugli stessi semi: 100 % (`out_EXTRA.txt`). L'effetto pesa quando il buio è corto (0,65 s) e il corpo è vicino (a 2,5 m resta rilevabile con un terzo del corpo visibile). Dipende dalla mia regola di rilevamento a 3 colonne: su hardware può essere più piccolo o più grande.

**«Torna» non è confrontabile col torneo.** Le mie rampe a 1 m/s² allungano il buio a 2,9–5 s e il cerchio cresce: da qui il 90–92 % contro il 56–66 % del torneo.

## Prova B

Tre curve di rumore: nominale (1,5 / 3,4 / 6,0 cm a 2 / 3 / 4 m), pessimista (4 / 9 / 16 cm), del torneo (5 / 11 / 20 cm). «Visto» = prima etichetta entro 1 s più un fotogramma dalla prima misura; stessi semi per le due regole.

| # | Soglia e previsione del responsabile | Mia previsione | Esito | Verdetto |
|---|---|---|---|---|
| B1 | falsi sul muro a 4 m > 10 %; previsto ≤ 2 % | ≤ 0,1 % con R giusto; 1–5 % con σ creduto la metà; > 10 % con un terzo | R giusto: spostamento 0 su 12 000 finestre (limite 0,025 %), χ² 0,000 % dei fotogrammi, con tutte le curve. σ creduto la metà: 2,3–2,7 % con una valutazione per finestra, ma **31 %** delle finestre con almeno un'etichetta falsa fra le 15 scorrevoli. Un terzo: 18 % e 95 %. χ² uguale | **regge**; le mie tre reggono contando una valutazione per finestra (il conteggio non l'avevo scritto) |
| B2 | di traverso a 2 e 3 m < 90 %; previsto ≥ 95 % | — | 100 % per le due regole e le tre curve (N = 2000; limite inferiore 99,85 %) | **regge** |
| B3 | in avvicinamento a 2 m < 90 %; spostamento regge (90–99 %), **χ² smentita (70–80 %)** | spostamento ≥ 95 % con le tre curve | spostamento 100 / 100 / 100 %; **χ² 100 / 100 / 99,0 %** | spostamento **regge**; χ² **regge**: la previsione del responsabile sulla χ² è smentita |
| B4 | nessuna soglia; previsto 30–80 % a 3 m, < 30 % a 4 m per tutte e due | da 3 m regge con la nominale, < 30 % con le altre; da 4 m solo con la nominale, 70–95 % | **Da 3 m:** nominale 100 / 100 %; pessimista spostamento 10,8 %, χ² 56,7 %; torneo 0,1 % e 45,2 %. **Da 4 m:** nominale 98,5 % e 81,4 %; pessimista 0,0 % e 27,0 %; torneo 0,0 % e 22,4 % | la mia regge a 3 m; a 4 m è **smentita** (98,5 % sta sopra la fascia). «Nessuna regola vede oltre 3 m» è smentita con la curva nominale |

**Altri numeri.** Con il 2 % di misure anomale e R giusto: spostamento 2,9–6,1 % di finestre false (35–62 % con le scorrevoli); χ² 2,4–8,3 % dei fotogrammi. Oggetto fermo appena visto (notato dopo, N = 4000): spostamento 0 etichette false nel primo secondo; χ² 0,15–2,3 %. Nel mio simulatore il rumore cala mentre il pedone si avvicina; se nel torneo restava fisso non l'ho verificato, e può spiegare il 75,4 % di là contro il 99 % di qui.

**Esito su K-007: non risolta.** Alla distanza dichiarata (2 m) passano tutte e due le regole: la prova non le separa. Oltre, decide la curva di rumore: con la nominale lo spostamento è migliore (98,5 % contro 81,4 % da 4 m); con le due pessimiste la χ² è migliore, ma nessuna arriva al 90 % (da 3 m: 45–57 % contro 0–11 %). Lo spostamento è a soglia netta: tutto o niente attorno a 5·σ·√2 metri al secondo. Sui falsi allarmi le due regole sono pari, salvo lo 0,2–2,3 % della χ² sulle tracce appena nate. «Vince lo spostamento» non è sostenuto. La decide la misura su hardware del rumore del centro di una persona a 2–4 m.

**`validazione-1` (media di 3 fotogrammi ai due capi): regge di misura.** Velocità minima vista al 90 %, in avvicinamento da 2 m (N = 2000 per velocità): 0,380 → 0,278 m/s con la curva del torneo, 0,301 → 0,229 con la pessimista, 0,138 → 0,095 con la nominale. Guadagno 1,31–1,46 restando dentro la finestra di 1 s; 1,48–1,58 con la finestra allungata a 1,2 s. La soglia di smentita era 1,3: passa per poco, e sta sotto l'1,7 che avevo previsto. Da 3 m con la curva pessimista porta il «visto» dal 10,8 % al 95,0 %. Costo: con il 2 % di misure anomale i falsi sul muro salgono a 5,7–14,9 %.

## Che cosa il simulatore condivide con la soluzione, e quindi non può escludere

Condivide: la specifica (ombra come intervallo angolare, errore d'ombra come spostamento dei bordi, quattro stati, fascia di 0,40 m, q, soglie χ², v_max, T_g), il modello linguistico che ha scritto soluzione e simulatore, il rumore gaussiano bianco, il pavimento piano, un pannello fermo, un sensore fermo, nessun rilevamento falso. Non condivide codice, semi, traiettorie, forma del corpo e curva di rumore con i simulatori del torneo.

Non può escludere:
- un errore vero della maschera d'ombra oltre i 20–30 cm, dove lo strato 1 smette di contenere;
- rilevamenti falsi al bordo del pannello, quindi «osservato» falsi e riagganci falsi;
- rumore correlato o con code, che cambia i falsi «mobile» (già al 31 % delle finestre con σ sbagliato di due volte);
- una regola di rilevamento diversa dalle 3 colonne, che sposta il risultato di A3 in D nei due versi;
- occlusore mobile, seconda persona mai vista che esce dall'ombra, sensore indossato;
- A1, A2 (a), A6 e A7 con R-a sono vere per costruzione: qui provano solo che il codice applica la regola.

## Per rifare tutto

```
sh /home/fede/Scrivania/ed/GitHub/Movi-Hackthon/.sciame/20261114-1301-percezione-challenge/f4/H-012/03-validazione/rifai.sh
```

Tredici lanci in sequenza, ciascuno sotto `timeout 120`; il più lungo dura 11 s, il totale circa 50 s su una CPU. Risultati in `out_*.txt` nella stessa cartella; per A la riga di ogni cella riporta i conteggi grezzi.

**Dopo.** Il responsabile fissa nel testo la lettura (ii) e il rilascio R-a, e dice che cosa esce nei mancati rilevamenti in campo aperto (con Pd = 0,9 sono 2–5 fotogrammi per passaggio, `out_A_T_w1_pd09.txt`). Per la demo: pannello da almeno 1 m, oppure prova su hardware di dieci passaggi dietro quello da 0,5 m prima di mostrarlo.
