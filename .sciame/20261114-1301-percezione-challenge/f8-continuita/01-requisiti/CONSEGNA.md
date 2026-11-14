Canarino: sciame-canarino-20c82ebff50dded3

# Continuità visiva: requisiti e audit — `sciame-requisiti`, f8, corsia A

**In testa: scostamenti e regole violate.** (1) Lo strumento di lettura in rete ha salvato da solo un PDF fuori dalla mia cartella (`~/.claude/projects/-home-fede-Scrivania-ed-GitHub-Movi-Hackthon/…/tool-results/webfetch-1794665945489-9828vn.pdf`): non l'ho aperto, e la fonte che cercavo (regole di punteggio proprie) resta **non verificata**. (2) P7 e il conto D stanno nello stesso comando: l'ordine è previsione, poi lancio, ma l'ora è la stessa (15:18:50). (3) Letti per intero: contratto f8, traccia, addendum, `SOLUZIONE_V2.md` (V2), `VERDETTO.md`, `SPECIALIZZAZIONE.md`, `MOTO_PROPRIO.md`, `TORNEO_parte2.md` e `parte3.md`, `proposta_sciame.tex` (v0.5; non il PDF). Solo con `grep`: `MISURE*.md`, `AUDIT.md`, `ATTACCO_SPECIALIZZAZIONE.md`, la consegna del ricercatore. Nessun simulatore altrui rieseguito. (4) **Indipendenza:** il mio conto (`conto_requisiti.py`, Python puro, senza numeri casuali, 2 s; `risultati_conto.txt`) condivide con V2 la specifica (q = 0,2, 15 Hz, la regola) e il modello linguistico, non il codice; corpo puntiforme, niente C6, niente rilevamenti mancati. (5) **Previsioni** (`PREVISIONI.md`, scritte alle 15:14:50, prima di leggere le parti): P1, P4, P5 reggono; P2 **smentita a metà** (l'analisi del moto ha un requisito sulla copertura, Q5); P3 regge sui file, **superata di poco nel mio conto** con rumore di 1,5 cm (67–72 % contro la soglia del 60 %); P6 **smentita alla lettera** (due blocchi sono compatibili senza modifiche); P7 regge in (a) e (b), **mista** in (c).

## 1. Risposta a Q3: no, il nucleo non rispetta l'imperativo

Rispetta la continuità **dell'avviso** (strato 1) e **dell'identità**; non quella **del movimento mostrato**. Prova: `MISURE_V2.md`, riga P4 (demo, «prosegue»): buio 1,07–1,13 s, «previsto» 0,40–0,53 s, poi «perso», che è assorbente. La stima esce quindi nel **35–50 %** dei cicli senza osservazione in demo e nell'8–10 % in sosta («perso» 4,6–4,8 s); con 3 e 5 s di buio sarebbe il 13–18 % e l'8–11 % [conto C: estrapolazione, la durata del «previsto» non dipende dal buio]. A schermo il segno sparisce e ricompare 0,72 m più avanti [(1,07 − 0,47) s · 1,2 m/s]. Nessuna misura dice quanto è precisa la previsione per tempo e per comportamento (§3).

**Legame con la traccia.** «Continuità percettiva» ha tre letture: dell'avviso, dell'identità, della stima del movimento. Il contratto originale (R3) e il verdetto hanno misurato le prime due; l'utente chiede la terza, e la traccia mette il vincolo: «senza rinunciare alla sicurezza delle indicazioni».

## 2. L'imperativo, parola per parola (ogni soglia è un'ipotesi da tarare)

- **CV-1, «continuità visiva».** Per ogni traccia confermata entrata in un'ombra, **a ogni ciclo** fino al riaggancio o a una chiusura dichiarata escono il punto più probabile, le regioni al 50 % e al 90 % e l'età dall'ultima osservazione. Chiusure ammesse, elenco chiuso: riaggancio; ombra vista libera cella per cella; affidabilità persa. *Misura:* quota dei cicli con stima = 100 %, vuoto ≤ 1 ciclo (0,067 s). *In demo:* contatore «cicli stimati / cicli senza osservazione».
- **CV-2, «predizioni efficaci».** Errore del punto più probabile a 0,5, 1, 2, 3 e 5 s senza osservazione. *Soglia:* mediana non peggiore di «fermo all'ultima posizione» e di «velocità costante» sulla miscela, e non oltre +10 % su nessun comportamento; ≤ 0,5 m a 1 s (il conto A dà σ 0,30–0,40 m per asse, cioè mediana radiale 0,35–0,47 m). *In demo:* curva errore–tempo dalle registrazioni (`requisiti-1`).
- **CV-3, «valutazione realistica della precisione».** Copertura vera delle regioni al 50 e al 90 %, per tempo **e** per ciascuno dei sei comportamenti del contratto, con generatore non dell'autore e taratura su dati diversi. *Soglia:* entro ±5 punti sulla miscela e non sotto p − 10 in ogni cella, con N ≥ 400 (semiampiezza 4,9 e 2,9 punti [conto]); sempre insieme all'area mediana della regione. *In demo:* tabellone «ricomparso dentro la regione al 90 %: k su n».
- **CV-4, «visualizzazione continua del movimento».** Il punto mostrato avanza di non più di v_max·Δt per ciclo (0,17 m a 2,5 m/s), non inverte il verso senza un'evidenza, e al riaggancio il salto sta nella regione al 90 % in almeno l'85 % dei casi. *In demo:* scia tratteggiata che si raccorda alla traccia vista.
- **CV-5, «incertezza controllata».** Dichiarata (il livello p a schermo); limitata (regione dentro le celle non osservate più la fascia; 0 celle su «libero»); con soglia: grado **«saturo»** quando la regione al 90 % copre almeno l'80 % dell'ombra, detto e mostrato con un altro segno, non tolto. *Misura:* quota dei cicli saturi, riportata.
- **CV-6, «a prescindere dal sistema».** Soglie senza unità (quote, coperture, rapporti) e la stessa prova su ogni profilo, che dichiara v_max, frequenza, rumore e incremento di posa. Passo del predittore dentro i 67 ms, misurato.

## 3. Audit parte per parte

- **B1 sensore: in parte.** Il rumore è «da misurare» (V2, B1): senza, la precisione dichiarata non è realistica.
- **B2 griglia, B6 etichetta: rispettato.** Danno gli stati per limitare la regione; nulla da cambiare.
- **B3, regola C6: in parte.** Il gruppo tagliato dall'ombra non aggiorna il filtro: chi torna indietro è contenuto nel 47–50 % dei casi, da 99 % (`MISURE_V2.md`, P2c).
- **B4 filtro: in parte.** Copertura 0,89–0,93 al 95 % nominale sulla miscela, 0,56–0,66 per chi torna (`TORNEO_parte2.md`); un solo livello; senza vincoli il raggio al 95 % è 0,84 m a 1 s e 3,6 m a 3 s [conto A], oltre la griglia. Bene: q tarato su passaggi diversi da quelli di prova.
- **B5 ciclo di vita: non rispettato** (§1). Lo strato 1, invece, rispetta il criterio 5.
- **B7, B8: in parte.** Tre segni distinti (bene), ma nessun livello p, nessuna regione a due livelli, nessun segno per l'incertezza oltre soglia; la graduatoria «previsto > perso» va riscritta.
- **B9 e protocollo H0–H13: non rispettato.** Buio di 1,1 s: non mostra 2–5 s; nessuna prova misura la previsione; dietro il pannello manca la verità.
- **Invarianti 1–5 e 7: rispettato** (sono il criterio 5; il 4 è l'ultima frase del criterio 4). **6 e 9: da riscrivere.** Il 6 («mai sul punto previsto») vieta il rilascio, ed è giusto, ma letto largo vieta di restringere la regione con ciò che si vede; il 9 deve dire che la posizione prevista non è una «grandezza non osservabile». **8: da estendere** con l'età e il livello p. **Manca un decimo invariante** (CV-1).
- **Misure R1–R8: non rispettato in R3.** Misura l'identità, 28 su 30 (V2 §7 e riga M4). Nessuna quota dei cicli, nessun errore, nessuna copertura per tempo e comportamento, nessuna larghezza; la sola affine è «contiene alla riemersione» (un tempo, un livello). R4 e R8 sono compatibili; per R7 il costo del predittore non è misurato.
- **Regola «metà dell'ombra»: non rispettato.** Fissata, non misurata (K-004). Il cuneo è 1,01–1,53 m² (V2, C5; conto B) e il cerchio al 95 % a 1 s misura 2,2 m² [conto A, rumore di 5 cm]: la regola spegne **per costruzione** entro 0,67–0,87 s [conto B].
- **Verdetto: non rispettato nella promessa** (i fatti reggono): §5, punto 5; §3, R3; §6, decisione 3: «con 24 ore si taglia (etichetta, strato 2, ToF)».
- **Specializzazione: non rispettato.** §3.3: «la durata del previsto non ha un valore proposto… per le classi veloci si riduce a un istante»; allegato A: R3 «resta». L'attacco alla specializzazione non tocca mai la previsione.
- **Sensore in moto: in parte.** Q5 chiede copertura ≥ 0,90 con la covarianza dell'incremento di posa (9, 15, 39 cm a 0,67, 1, 2 s): solo fino a 2 s, e tutto non verificato.
- **Demo: non rispettato.** Atto 4: «probabile per un attimo»; atto 5: sosta in «perso».
- **Documento v0.5: in parte.** Dichiara l'obiettivo e ammette lo scarto (righe 60, 94). Restano: riga 112, «circa mezzo secondo» ancora convergente; riga 126, misura = identità; riga 184, «con 24 ore si tagliano… area prevista»; riga 157, l'atto 4 promette prima della prova; nessuna riga sulla previsione nella tabella dei profili.

## 4. Tensioni con la sicurezza, e come si sciolgono

1. **Mostrare una posizione senza farla sembrare vista.** Grammatica separata: visto = segno pieno; previsto = contorni delle due regioni, punto vuoto, età in secondi. L'invariante 3 resta. Misura: 0 fotogrammi in stile «osservato» a soggetto nascosto (R4), più tre osservatori ignari con almeno 54 risposte giuste su 60 (ipotesi).
2. **Niente previsione dove il sensore vede vuoto.** Il ritaglio non basta: in sosta il punto a velocità costante esce dall'ombra, e la regione al 50 % ritagliata è **vuota** a 2–3 s [conto D, notato dopo]. La regione va **condizionata** su ciò che si vede. L'evidenza negativa restringe solo la previsione, mai lo strato 1.
3. **Continuità contro «perso».** «Perso» smette di essere un'assenza e diventa il grado «saturo»: regione = tutta l'ombra, «può aver lasciato l'area». Lo strato 1 non cambia, e nessun timer entra.
4. **Tarata ma inutile.** «Tutta l'ombra» soddisfa sempre CV-1 e CV-3: per questo larghezza e quota dei cicli saturi sono misure obbligate.
5. **Uscita dal lato lontano.** Una regione sicura di sé e sbagliata (contenimento 22–41 %, `TORNEO_parte3.md`) viola CV-3: la regione deve comprendere l'uscita nel non osservato.

## 5. Critiche

1. La regola di fine del «previsto» confronta la regione con l'ombra, e alla scala della demo l'ombra è più piccola della regione onesta: spegne sempre (§3).
2. Il criterio 1 del contratto, da solo, si soddisfa con un'uscita priva d'informazione (tensione 4): va legato alla larghezza.
3. Sull'hardware la previsione **non è misurabile** con il protocollo attuale: dietro il pannello non c'è verità (→ `requisiti-1`).
4. Il piano taglia l'obiettivo principale: audit, punto 8 («se saltano… lo strato 2»); verdetto §6; documento, riga 184.
5. V2 dà due durate del «previsto»: 0,6–0,7 s (§1) e 0,40–0,53 s (`MISURE_V2.md`); il mio conto 0,67–0,87 s. Causa non verificata.
6. La taratura esistente ha un solo livello nominale, sul cerchio non ritagliato, senza «esce dal lato lontano» e senza larghezza.

## 6. Stati proposti

- «Il nucleo rispetta la continuità visiva»: **smentito** (misura altrui in simulazione; conto mio).
- «La continuità la porta lo strato 1»: regge per l'avviso; **smentito** per il movimento mostrato.
- «Filtro più ritaglio dà un'incertezza controllata»: **smentito** nel conto (regione vuota in sosta).
- «I principi di sicurezza sono compatibili con l'imperativo»: **non risolto**; lo sostiene la sola lettura, lo decide la modifica provata.
- Soglie CV-1…CV-6: **ipotesi**. Tutto è simulazione o conto, a sensore fermo.

## 7. Proposte per Q4

**`requisiti-1`, occlusione virtuale.** La previsione si accetta su registrazioni (o simulazioni) in cui il soggetto resta visibile e gli si negano i rilevamenti dentro un cuneo virtuale: la verità sono i rilevamenti negati. *Guadagno:* errore e copertura da 0,5 a 5 s per comportamento, su moto vero, senza seconda camera; riusa i 30 passaggi e le 20 soste già previsti. *Vincoli:* il cuneo virtuale entra nella griglia come «in ombra»; non riproduce il corpo tagliato dal bordo. *Chi:* validazione (`sim_v2.py`), poi il metrologo. *Falsificatore (≤ 5 min):* nel simulatore, «contiene alla riemersione» con pannello vero e virtuale, stessi semi, N = 2000. *Atteso, scritto prima:* scarto ≤ 5 punti con C6; oltre 15 senza C6 (braccio che deve fallire: `MISURE.md` dà 14–17 % contro 100 %). *Smentita:* oltre 5 punti con C6.

**`requisiti-2`, decimo invariante e «previsto» a due gradi.** «Ogni traccia pendente emette a ogni ciclo punto, regioni al 50 e al 90 % condizionate sul visto, età e grado (informativo o saturo)»; «perso» assorbente sparisce. *Guadagno:* quota dei cicli stimati dal 35–50 % (8–10 % in sosta) al 100 %. *Vincoli:* strato 1 intatto; vale solo se passa CV-3. *Chi:* le corsie del predittore, poi l'avversario. *Falsificatore, eseguito* (conto D; atteso in P7): con il solo cerchio del filtro i cicli saturi sono 0 % nel transito a 1,2 m/s, 46 % a 0,8 m/s, 31–83 % in 5 s di sosta. *Lettura:* nel transito il requisito non è vuoto; in sosta «filtro più ritaglio» non lo soddisfa.

## 8. Priorità, e che cosa fare dopo

**Deve esserci:** registrazione grezza e griglia; una traccia con il filtro; strato 1 (vincolo); predittore per tutta l'occlusione con regioni condizionate; schermo con la grammatica della previsione e i contatori; banco di misura con occlusione virtuale; «affidabilità persa» minima. **Si taglia o si rinvia:** etichetta B6 (4 ore, V2); sensori ToF; ungherese e seconda persona nell'atto 4; frasi in voce e prova con persone bendate; messaggio per settori; sesto atto in moto; pannello da 0,5 m; regola «mobile» fine. Le ore liberate oltre le 4 di B6 e il costo del lavoro nuovo sono **non verificati**. La mappa voxel la decide f7.

**Domande all'utente.** (a) «Visiva» vale solo per lo schermo o anche per il canale sonoro? (b) Quale livello e quale soglia per l'incertezza «controllata» (ipotesi: 50 e 90 %, saturo all'80 % dell'ombra)? (c) Fin quando: finché la traccia pende (ipotesi) o entro un orizzonte? (d) In conflitto, la sicurezza resta vincolo (ipotesi del coordinatore)? (e) Demo con un'ombra più larga, per mostrare almeno 2 s?

**Dopo:** validazione esegue il falsificatore di `requisiti-1`; il documento corregge le righe 112, 126, 184. **Rifare:** `cd f8-continuita/01-requisiti; PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 conto_requisiti.py > risultati_conto.txt`.
