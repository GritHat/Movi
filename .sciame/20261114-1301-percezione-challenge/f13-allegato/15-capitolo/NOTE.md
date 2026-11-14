# NOTE — capitolo 5 (Occlusione), per chi unisce

Lavoro dalle 18:55:51 alle 19:10 circa del 14 novembre 2026 (`date -Is`). File: `capitolo.tex` (il capitolo), `prova.tex` (file di prova: preambolo + `\setcounter{section}{4}` + capitolo + bibliografia), `prova.pdf`, `CIFRE.md`, questo file; copie di `preambolo.tex` e `allegato.bib`.

## 0. In testa: regole violate, scostamenti, cose non fatte

- **Regola 3 (previsioni prima):** non ho scritto previsioni prima della sola prova che ho fatto (la compilazione). Esito della prova, detto dopo: compila.
- **Un comando negato.** Un mio comando che cancellava le immagini di controllo nella cartella temporanea (`rm -f …/pg/*.png`) è stato rifiutato dal sistema dei permessi. Non l'ho ripetuto né aggirato: ho solo rifatto le immagini senza cancellare niente. Nessun effetto sulla consegna.
- **File di rapporto.** L'ambiente chiede di non scrivere file di rapporto; la consegna chiede `CIFRE.md` e `NOTE.md`: ho seguito la consegna.
- **Il giudizio complessivo dell'integrazione non esiste** (`f12-integrazione/30-arbitro/` è vuota, controllato con `ls`): non ho potuto confrontare le frasi del capitolo con «la forma più forte che resta vera» né con un suo elenco di frasi da non scrivere. Ho usato l'elenco «Non si dice mai» di `SOLUZIONE_V3.md` §3.
- **Letti per intero:** contratto, preambolo, fascicolo 01, `PROVA_INSIEME.md`, `BLOCCO_CLASSIFICAZIONE.md`, `USO_DELLA_CLASSE.md`. **Letti in parte:** `SOLUZIONE_V3.md` (§1.3–§3, r. 100–313, e la tabella delle esclusioni), `VERDETTO_CONTINUITA.md` (fino al §3), `CONTROLLO_PROVE.md` (§0–§4), fascicolo 04 (simboli, §4, §6.2, §6.3), fascicolo 06 (§II.3), discordanze (parte del fascicolo 01), `ATTACCO_CLASSIFICAZIONE.md` (ricerca testuale). **Non letti:** fascicoli 02, 03, 05; `LIBERO_DELLA_CELLA.md`; i due file sull'identità su profondità simulata (esistono, controllato con `ls`); `ATTACCO_V3.md`; `SCHERMO_E_DEMO.md`; `PROFILI.md`; `CLASSIFICATORE.md`; i verdetti f4, f7, f9, f10.
- **Nessuna cifra ricalcolata:** tutte ritrovate per lettura nei file (vedi `CIFRE.md`). Indipendenza del mio controllo: nulla; condivido con le fonti testi, autori e modello.
- **Compilazione:** `xelatex`, `bibtex`, `xelatex` × 2 con `timeout 120 … -interaction=nonstopmode -halt-on-error`: 0 errori, 0 citazioni indefinite, 0 avvisi di BibTeX, 0 righe fuori margine. **Otto pagine di corpo esatte**; la bibliografia va a pagina 9. I riferimenti agli altri capitoli (`sec:map`, `sec:sti`, `sec:val`, `sec:cos`, `sec:lim`) restano «??» (14 occorrenze): atteso. Il margine è nullo: ogni aggiunta al capitolo porta a nove pagine.
- **Preambolo:** non mi è servito nessun pacchetto in più. Uso `\operatorname{dist}` (amsmath), `[H]` (float), `pattern` (libreria già caricata).

## 1. Punti in cui ho dovuto scegliere fra due fonti (da confermare)

1. **Chiusura dell'area d'avviso al riaggancio.** Il fascicolo 01 §4 definisce l'area d'avviso che «si chiude solo per riaggancio dell'identità o quando tutte le sue celle sono state viste libere», e la consegna chiede di dire che l'area realizzata «si chiude anche per riaggancio». La soluzione finale (§1.7) dice il contrario: «NIENTE toglie l'avviso se non lo sguardo: non il riaggancio…», e dopo un riaggancio l'area resta come «possibile presenza residua». **Ho seguito la soluzione finale** (è il sistema descritto) e ho presentato la chiusura per riaggancio come «variante esaminata», con il suo controesempio (secondo soggetto). Di conseguenza:
   - nella Definizione dell'area d'avviso non c'è la chiusura per riaggancio;
   - nella dimostrazione del punto (c) della proposizione sull'annidamento ho sostituito la frase del fascicolo sulla porta del riaggancio («può solo impedire una chiusura») con «il riaggancio, che usa la regione nella sua porta, non chiude l'avviso»;
   - nel punto (d) ho scritto «alla chiusura della traccia» invece che «alla chiusura dell'avviso».
   Se chi unisce preferisce la forma del fascicolo, vanno cambiati questi tre punti e il paragrafo «Differenza fra Π e W».
2. **Definizione della regione mostrata.** Il fascicolo 01 scrive la sottrazione esplicita delle celle viste libere oltre w_p; la sua nota D9 avverte che nel codice è un peso (× 0,1 a ciclo) e che lo «0 cicli» è misurato. Ho descritto il peso, tolto la sottrazione dalla definizione e dato la proprietà come «verificata in simulazione», non «per costruzione». Il pavimento è scritto W(t) \ O(t), come nel fascicolo (lettura del suo autore: D9).
3. **Fascia di guardia.** Tabella con quattro conti (vedi `CIFRE.md`). La riga «età e latenza, senza tenuta» riporta «1,4 (margine nullo)»: è la frase dei file, non una divisione mia.
4. **Latenza.** Nei file è 0,150, 0,155 o 0,222 s. Nel capitolo: 0,150 solo nella riga 1 della tabella (com'è nel fascicolo), 0,155 «stimata» altrove; nell'osservazione sulla probabilità d'intrusione ho scritto solo «meno della latenza», senza cifra. Da allineare al valore che dichiara il capitolo 8.
5. **«0 su 96 corse»:** il fascicolo 01 (II.1) segnala che un file d'origine dice «368 corse»; ho tenuto 96 come il fascicolo.

## 2. Che cosa ho scritto io e non sta alla lettera in un file

- **La dimostrazione della proposizione sull'etichetta** (§5.8). I file danno l'enunciato (invariante sull'etichetta in `BLOCCO_CLASSIFICAZIONE.md` §5) e lo stato «per costruzione»; le quattro righe di dimostrazione (monotonia della dilatazione nel raggio, rilascio più restrittivo, induzione) le ho scritte io. Le ipotesi (1)–(3) sono le regole del blocco. Non è contenuto nuovo nel senso dei risultati, ma **nessun secondo ruolo l'ha rifatta** (criterio A-1): da far rileggere.
- **La formula d_serve per destinatario fermo**, v·(t_conf + τ + T_r) + C: è la formula generale del blocco con v_ego = 0.
- **I nomi descrittivi** al posto delle sigle: «regola d'ingresso», «predittore principale» e «di ripiego», «variante esaminata», «prove brevi», «fascia di scenario», G_1–G_3 (questi ultimi dal fascicolo 04).
- **La figura** è schematica: ostacolo largo 2 m a 1,5 m, campo di 87°, portata 3 m, fascia 0,40 m in scala; posizioni di regione e punto disegnate a mano, non da una prova (la didascalia dice «pianta schematica»).

## 3. Dipendenze dagli altri capitoli

- **Capitolo 3 (`sec:map`):** stati della cella, definizione di O(t), proposizione di sicurezza del «libero». Le ipotesi (i)–(vi) del mio §5.1 sono le stesse sei del fascicolo 01 §1: se il capitolo 3 le enuncia già, qui basta un rimando e si recuperano circa dieci righe. Attenzione alla numerazione: io le cito come (i)…(vi).
- **Capitolo 4 (`sec:sti`):** conferma della traccia, porta, gruppo «tagliato», cifre dell'identità al ritorno, tabella dei profili di classe (15 classi), controllo di coerenza cinematica. La mia tabella del dominio ha 8 classi su 15 e ne riprende velocità tipica e massima: devono coincidere con la tabella del capitolo 4.
- **Capitolo 6 (`sec:val`):** tavole complete, definizioni delle misure, G_1–G_3, P_D, intervalli della tabella «prima e dopo», taratura per quantili. Io uso P_D e G_1–G_3 con una riga di definizione.
- **Capitolo 7 (`sec:cos`):** l'alternativa a due ipotesi di moto pesate (qui una frase, «38–100 % dei transiti»).
- **Capitolo 8 (`sec:lim`):** formula generale di d_serve e T_ant, profilo di chi porta il sensore, la dicitura «suolo visto libero fino a d», latenza. Simboli che uso e che devono coincidere: v_scen, w_scen, v_ego, t_conf, T_r, C, d_serve.
- **Appendice A:** parametri che cito: w = 0,40 m; w_p = 0,20 m; 4 fotogrammi; 2 cicli; 0,75 m; 3 fotogrammi per il rilascio; 400 percorsi (200 + 200); peso 0,1; 3 lisciature; 80 %; 0,3 m/s; 2 s; orizzonte 3 s; 8 cicli e 0,167 m per ciclo del punto.

## 4. Notazione: scelte da uniformare

- Dilatazione: uso `\dilata(A,r)` del preambolo e scrivo una volta l'equivalenza con A ⊕ B(r) (il fascicolo 01 usa ⊕).
- Area d'avviso: W(t); regione: `\Reg_\alpha`, con `\Reg_1 = W`. Ombra stimata: `\hat\Omb`; errore del bordo: ε_Ω.
- Nella proposizione sul ritaglio il livello si chiama α_S (il fascicolo lo chiama q, che nella notazione comune è la densità del rumore di processo).
- Fascia per ombra: w_Ω(t).

## 5. Lasciato fuori, e perché

- **La tabella completa della simulazione di Π** (cinque righe): data nel testo; la riga sulla probabilità d'occupazione statica (138 230 celle-fotogramma) è materia del capitolo 3.
- **Margine di posa, vetro, memoria fra fotogrammi** (fascicolo 01 §2): capitolo 3.
- **Massa e ordine della catena** (fascicolo 01 §5, §6): capitolo 4.
- **Identità al ritorno**: solo il meccanismo e il limite del secondo soggetto; le cifre (10 711 su 10 757 ecc., e quelle su profondità simulata) al capitolo 4 o 6.
- **Sette classi su quindici** della tabella del dominio (monopattino, auto in area di lavoro, aereo al traino, tram, treno in manovra, bicicletta, multirotore) e la colonna dell'ingombro: per spazio; stanno in `BLOCCO_CLASSIFICAZIONE.md` §6. Il multirotore è escluso anche perché la mappa del suolo non lo rappresenta.
- **Il profilo di chi porta il sensore** (tabella dei profili, T_ant): capitolo 8.
- **Il difetto del rilascio dopo la rimozione dell'ostacolo** è detto in una riga come «non verificato» (10 prove su 10), senza i dettagli (117 celle fra 2,3 e 3,0 m).
- **Costo di calcolo del predittore** (0,32–1,96 ms): capitolo 7.
- **Chiusura «fuori dall'area osservata»**: descritta; le cifre (25 su 194 861; 271 / 268 / 340) lasciate fuori per spazio.
- **Altre cifre dell'osservazione sul criterio** (0,865; 0,142): lasciate fuori per spazio.
- **`guibas1997`, `scholl1999`, `tokmakov2021`, `vanhoorick2023`, `hsieh2023`**: citabili ma non usate (lavori correlati: capitolo 7).

## 6. Citazioni usate (tutte in `allegato.bib`, tutte secondo la mappa del fascicolo 06, §II.3)

`khurana2021` (occlusione come previsione a breve termine) · `cao2023` (senza misure l'errore del filtro si accumula durante l'occlusione) · `orzechowski2018` (stato degli ostacoli nascosti sovrastimato) · `koschi2021` (previsione insiemistica dei partecipanti rilevati e potenzialmente nascosti) · `koch2007`, `wyffels2015` (informazione negativa nel seguimento: citazioni nominali, usate senza cifre) · `angelopoulos2021` (copertura marginale) · `barber2019` (copertura condizionata esatta impossibile senza ipotesi sulla distribuzione). Nessuna fonte fuori dalla bibliografia: **niente da aggiungere** per questo capitolo. L'intervallo di Wilson è nominato senza citazione (lo cita il capitolo 6).

## 7. Dubbi

- «Sezione bidimensionale» per la simulazione di Π: il fascicolo scrive «sezione piana»; ho evitato la parola «piano» ovunque (anche «suolo planare» per l'ipotesi v) per non urtare un controllo meccanico del criterio A-4. Se gli altri capitoli scrivono «pavimento piano», uniformare.
- La parola «persa» compare due volte, per descrivere la costruzione scartata («traccia dichiarata persa») e per dire che lo stato «perso» non esiste: voluto.
- «Tarata» compare per la soglia dei 4 fotogrammi e per la libreria: è l'origine del parametro, non una dichiarazione sul sensore.
- Le frasi sul classificatore («richiesto; non realizzato né valutato; simulato con etichette a mano; nessuna classe diversa da "persona a piedi" nella catena; la sicurezza non dipende dall'etichetta») sono nel §5.8; ho precisato che gli errori di etichetta sono stati provati solo su sequenze generate a caso e fuori dalla catena, perché nei file la modalità «errori iniettati» sulla catena non risulta eseguita.
