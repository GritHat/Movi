# NOTE al capitolo 2 (Sensore e geometria d'osservazione) — per chi unisce

Lavoro svolto il 14-11-2026 dalle 18:55 alle 19:12 circa (`date -Is`). File consegnati in questa cartella: `capitolo.tex` (corpo del capitolo), `CIFRE.md`, `NOTE.md`; di servizio: `prova.tex`, `prova.pdf`, `prova.txt`, `allegato.bib` (copia), `img/`, i `.log`.

## 0. Cambi di stato, regole, scostamenti

- **Nessun cambio di stato** di enunciati: il capitolo è composizione del fascicolo 02 (parte I, §0–§6 e §10) con le correzioni della sua parte II.
- **Previsioni:** nessuna registrata, perché non ho fatto prove nuove; il solo controllo è il ricalcolo in forma chiusa di circa 150 cifre (colonna «rifatta» di `CIFRE.md`): tutte tornano con il fascicolo. **Indipendenza:** il ricalcolo condivide con il fascicolo le formule e i parametri di scheda; vale contro errori di trascrizione, non contro un errore di formula o di lettura delle schede. Non rifatti: il 20,5 % (integrazione numerica), i conteggi di simulazione del §2.5, i valori letti dalle schede.
- **Un comando negato dalla sessione** (una modifica al mio file fatta con un programma, insieme a una cancellazione di immagini di servizio): rifatta con lo strumento di modifica, senza aggirare il divieto. Per questo in `img/` restano immagini di più passate.
- Nessuna scrittura fuori da `f13-allegato/12-capitolo/`; niente git, sudo, rete. Nessuna prova su sensore fisico è lasciata intendere: le diciture sono «verificato per calcolo», «su profondità simulata dalle schede tecniche», «non verificato sperimentalmente».
- **Compilazione:** XeLaTeX, BibTeX, XeLaTeX due volte: 0 errori, 0 citazioni indefinite; restano indefiniti solo i rimandi ad altri capitoli (`sec:map`, `sec:occ`, `sec:lim`). **Il corpo del capitolo occupa poco meno di sei pagine** (finisce a circa due terzi della pagina 6, dove comincia la bibliografia di prova; il limite era sette). Nessun pacchetto in più.

## 1. Che cosa ho lasciato fuori, e perché

1. **Requisiti sulla posa per il sensore in moto** (fascicolo 02, Prop. 9 e Tab. 7; forma chiusa p(δ), 0,88°, ritardi, inclinazione, regione di previsione): vanno nel capitolo 8, per consegna. Qui c'è solo la formula dell'errore di quota (`eq:geo-posa`) e il rimando.
2. **Fascia di guardia e distanza di separazione** (fascicolo 02, §7: Prop. 10, Tab. 8 e 9): capitolo 5. Nella figura in pianta la fascia è disegnata con larghezza simbolica $g$ e la didascalia rimanda a `sec:occ`.
3. **Bilancio di latenza** (fascicolo 02, §8, Tab. 10): capitolo 8.
4. **Cifre senza sostegno nella mappa «affermazione → chiave»**, tolte invece di lasciarle con una citazione non coperta:
   - rumore laterale al bordo destro (4,1 cm): la mappa di `ahn2019` riporta solo 4,3 cm al bordo sinistro;
   - portata di 0,8 m al buio su grigio al 17 % (VL53L7CX);
   - «il costruttore dichiara che tre sensori coprono 180° × 60°»: scritto come conto (3 × 60°), non come dichiarazione;
   - campi diagonali (90° e 65°);
   - «solo lo stato 5 del bersaglio è valido al 100 %» (`st-um3038`): la mappa sostiene un'altra frase (primo campione dopo «nessun bersaglio»: fiducia sotto il 50 %), che ho usato al suo posto per la ragione (c);
   - scarto tipo per zona 3,7 cm da «±5 % letto a 2,7 σ»: il fascicolo 02 stesso dice che il ±5 % non è fra i dati verificati.
5. **«Settore tagliato dalla retta, 19,0 %»** (terza variante della frazione del disco): è solo nella parte II del fascicolo; nel capitolo restano il 20,0 % e il 20,5 %.
6. **Controesempi più recenti sull'errore di posa** della soluzione finale (scatola di 10 cm a 2,6–2,9 m «libera» in 146–150 fotogrammi su 300 a −1°; tolleranza di posa all'avvio sotto 0,5°): appartengono ai capitoli 3 e 8; qui ci sono solo i riscontri del fascicolo 02.

## 2. Dove il capitolo dipende da altri

- `\S\ref{sec:map}`: lo stato «libero» come affermazione sul suolo e fino a $y_{\max}(z)$; la proprietà «mai libero su un ostacolo» vale a posa nota (§2.2 e §2.5).
- `\S\ref{sec:occ}`: larghezza $g$ della fascia di guardia (figura in pianta e riquadro finale).
- `\S\ref{sec:lim}`: requisiti in moto, bilancio di latenza, tolleranza di posa all'avvio.
- Parametri che devono coincidere con l'appendice A: $h=1{,}2$ m, $\theta=15^\circ$, portata 3 m, $y_s=0{,}07$ m, cella 1° × 0,1 m, flusso 848 × 480 a 30 fotogrammi al secondo.
- Etichette che altri capitoli possono voler citare: `eq:geo-zmin`, `eq:geo-ombra`, `eq:geo-amin`, `eq:geo-durata`, `eq:geo-banda`, `eq:geo-sigmaz`, `eq:geo-posa`, `eq:geo-suolo-falso`, `tab:geo-profili`, `tab:geo-verticale`, `tab:geo-amin`, `tab:geo-durata`, `tab:geo-rumore`, `tab:geo-tof`, `fig:geo-sezione`, `fig:geo-pianta`, `fig:geo-tof`, `prop:geo-disco`, `cor:geo-suolo`.
- Il capitolo 4 usa $\sigma_z(d)=k\,d^2$ per la soglia della regola «mobile»: la forma con $\sqrt{2/3}$ e l'asse trasversale $\rho\cdot1^\circ/\sqrt{12}$ (discordanza 9 della geometria) non è toccata qui.

## 3. Scelte di notazione da uniformare

- Coordinate d'immagine normalizzate $(\xi,\eta)$ al posto di $(u,v)$ del fascicolo, per non scontrarsi con la velocità $v$; resta $\Delta u$ per la larghezza in pixel della banda stereo.
- Ampiezze del campo $\Phi_h$, $\Phi_v$ al posto della sigla FOV; centro della camera $\mathbf c$ (non $C$, che somiglia a una sigla di lavoro); passo di disparità $\epsilon_\delta$ (non $q_\delta$, per non scontrarsi con la densità $q$ del filtro).
- $L$, $w$, $v$, $a$, $s$, $z_o$, $z_p$, $y_s$, $k$ come nel fascicolo. Attenzione: $w$ qui è la larghezza del corpo e $L$ la larghezza del pannello; se il capitolo 5 usa $w$ per la fascia, uno dei due va rinominato.
- I livelli di prova sono dati con `\prova{D}`, `{C}`, `{S}`, `{N}`; nelle equazioni numerate il segno sta dentro l'equazione, con `\text{}`.

## 4. Dubbi

1. **Focale e campo** (discordanze 1–2 della geometria): ho tenuto la scelta del fascicolo, dichiarata una volta nell'Osservazione «Focale e campo» (geometria con 87° × 58°, rumore con $f=424$ px; $z_{\min}$ 1,24 m, e 1,22 m con 59,0°). Se l'allegato sceglie una sola focale, cambiano le cifre laterali del 5 % e $z_{\min}$ di 2 cm.
2. **Intervalli mancanti sulle frequenze del §2.5.** Il fascicolo dà Wilson solo per 9 su 10 e 10 su 10. Per le altre non ho scritto intervalli, perché non sono nei file. Se chi unisce li vuole (regola «ogni frequenza con il suo intervallo»), il conto è: 7 su 7 → 0,65–1; 0 su 10 → 0–0,28; 1 su 10 → 0,02–0,40; 2 su 10 → 0,06–0,51 (Wilson al 95 %, **calcolo mio, non presente nei file**, fatto con un programma di poche righe; la stessa formula ridà 0,60–0,98 e 0,72–1 del fascicolo).
3. **Lato della banda stereo e `ahn2019`.** Il fascicolo 02 (parte II, II.3) chiede di ricontrollare che la frase della fonte sul «bordo sinistro del bersaglio» sostenga «dal lato previsto». Ho scritto «cioè dal lato previsto»: se il controllo non è stato fatto, si tolga l'inciso.
4. **Gemini 335, intervallo ideale:** 0,3–3 m (fascicolo 02, dalla scheda della serie) e 0,26–3 m (mappa del fascicolo 06, dalla pagina del prodotto): riportati entrambi nella tabella dei profili.
5. **Valori di scheda senza citazione** nella tabella dei profili: distanze minime (0,35; 0,195; 0,18 m), $f=410{,}7$ px e 90° × 60° a 848 × 480 della Gemini 335, tolleranza ±3°, i $\sigma_d$ limite. La didascalia dice che sono letti dalle schede. Le voci `realsense-d400-scheda` e `orbbec-gemini-330-scheda` sono nel `.bib` ma la mappa le dà citabili solo per altri dati (proiettore a 850 nm): non le ho usate. **Da decidere:** verificare quei dati sulle schede e aggiornare la mappa, oppure lasciare i valori senza richiamo.
6. **Contenuto che il fascicolo 02 segnala come riderivazione propria** (parte II, II.0), entrato nel capitolo: la regione esatta con i bordi laterali rettilinei e il 20,5 %; la sensibilità di $z_{\min}$; la riga «≥ 1,77 m» della tabella di $a_{\min}$; le ragioni (a)–(c) sul tempo di volo. Sono conti, non misure; se «niente contenuto nuovo» le esclude, si tolgono senza toccare il resto.
7. **Bibliografia:** BibTeX avvisa «empty year» per otto voci (pagine dei costruttori senza anno) e tre righe della bibliografia escono dal margine (indirizzi lunghi nelle note). Non dipende dal capitolo: si risolve nel preambolo o nel `.bib`.
8. **La chiave `slamtec-rplidar-c1`** contiene «c1»: è l'unico riscontro del controllo automatico sulle sigle vietate, ed è dentro un `\cite`.
9. **Figure:** nella pianta la fascia di guardia e la banda stereo non sono in scala (detto in didascalia); il settore della camera nella figura dei sensori a tempo di volo è il settore d'anello schematico, non la regione esatta. Le figure e le tabelle usano `[htb]`: nel documento unito l'ordine dei galleggianti può cambiare. La tabella e la figura dei sensori a tempo di volo stanno affiancate in un solo ambiente `table` (la figura usa `\captionof{figure}`).

## 5. Fonti da aggiungere alla bibliografia

Nessuna fonte nuova è necessaria per questo capitolo. Mancano solo, nella mappa, i dati del punto 4.5 (già voci del `.bib`).
