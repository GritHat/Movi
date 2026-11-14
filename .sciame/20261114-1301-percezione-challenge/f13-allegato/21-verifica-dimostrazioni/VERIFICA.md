# Verifica avversaria dell'allegato tecnico — parte «dimostrazioni»

**Esito.**
- Voci controllate: **63** (proposizioni, lemmi, corollari, osservazioni, controesempi e passi marcati D dei capitoli 2–9: cap. 2: 12; cap. 3: 10; cap. 4: 9; cap. 5: 16; cap. 6: 8; cap. 7: 3; cap. 1, 8, 9: 5).
- Tornano senza modifiche: **43** (enunciato, dimostrazione e cifre rifatte con `controlli.py`).
- Non tornano: **20** — 9 con un enunciato o un passo **falso o non sostenuto** (correzioni 1–8 e la tabella della 11), 9 **imprecise** (correzioni 9, 10, 12–16, il punto (c) nella 5, il rumore del centro nella 17), 2 di **forma** (17).

**Cambi di stato, previsioni, regole.** Previsioni scritte prima dei calcoli in `PREVISIONI.md` (19:32:33; primo lancio 19:33:49). Reggono PV1, PV3–PV8, PV10. **PV2 smentita a metà:** il mio primo conteggio del controesempio di velocità dà 30 288 su 65 536, non 17 696; la differenza è la convenzione (io contavo la violazione a un fotogramma qualsiasi, il fascicolo solo all'ultimo); il secondo conteggio, aggiunto *dopo* e quindi non cieco, dà 17 696. PV9: tutto torna tranne $z_{60}$ (3,341, l'allegato stampa 3,342). Nessuna regola violata: scritture solo in questa cartella, niente git, niente rete; l'allegato non è stato toccato. **Indipendenza:** i miei controlli condividono con l'allegato il modello, le ipotesi e il testo delle regole; il codice è mio (Python puro, 2 s). Non ho rilanciato alcun simulatore: delle cifre di simulazione ho rifatto solo gli intervalli.

Stati proposti (li assegna l'arbitro): Prop. contenimento, fascia, annidamento (b), etichetta, sicurezza (a) → **smentite nella forma scritta, dimostrate nella forma corretta qui sotto**; tutto il resto resta com'è marcato.

---

## Correzioni — A. Falso o non sostenuto

### 1. Contenimento con errore di posa (cap. 5, `prop:occ-contenimento`, e di riflesso `cor:occ-libero-adesso`)

**Che cosa non torna.** L'enunciato dichiara l'ipotesi (iii) con $\varepsilon_p>0$ e conclude «ogni punto occupato appartiene a $\Pres(t)$». Il passo «per (i) un punto occupato non è visto libero: $x\notin\Oss(t)$» vale solo a posa esatta: con posa stimata l'oggetto che sta in $x$ compare in $x'\neq x$, e la coordinata $x$ può stare in $\hat\Oss(t)$. Il termine $\varepsilon_p$ nella dilatazione non ripara, perché la sottrazione viene dopo.

**Prova.** Controesempio minimo, una dimensione: riferimento stimato spostato di una cella; un oggetto fermo in $x$; il sensore vede libero tutto tranne $x+1$. Allora $\Pres(t)=\{x+1\}$ e $x\notin\Pres(t)$. `controlli.txt` §A2 (tutte le traiettorie a passo ≤ 1 su 7 celle e 3 fotogrammi): posizione vera fuori da $\Pres$ in **132 istanti su 132** con la ricorsione dell'allegato; **0 su 132** se a $\Oss$ si sostituisce il suo eroso di $\varepsilon_p$ (cifre mie, non da inserire).

**Testo corretto** (enunciato; assorbe anche la correzione 2):

```latex
\begin{proposizione}[Contenimento]\label{prop:occ-contenimento}
Sia $\Oss(t)$ l'insieme dei punti del suolo il cui raggio è letto come suolo da un pixel valido del fotogramma $t$ (lettura per punto). Sotto le ipotesi (i), (iv) e (v), a posa esatta ($\varepsilon_p=0$), ogni punto del suolo su cui poggia, al fotogramma $t$, un oggetto più alto del margine di lettura \eqref{eq:map-margine} (punto \emph{occupato}) appartiene a $\Pres(t)$. In particolare la posizione di un soggetto entrato in un'ombra appartiene a $\Pres(t)$ per ogni $t$ fino alla riosservazione, senza alcuna ipotesi sul numero dei soggetti né sull'esistenza di una traccia. Con posa nota entro $\varepsilon_p$ (ipotesi (iii)) l'enunciato vale nel riferimento stimato; nel riferimento vero vale se nella \eqref{eq:occ-presenza} a $\Oss(t)$ si sostituisce l'insieme dei punti $x$ il cui disco di raggio $\varepsilon_p$ è contenuto nel libero stimato $\hat{\Oss}(t)$ (Lemma~\ref{lem:map-posa}). \prova{D}
\end{proposizione}
\begin{proof}
Per induzione su $t$. Base: $\Pres(0)=X$. Passo: sia $x$ occupato al tempo $t$. Per (iv) il punto materiale che sta in $x$ si trovava al tempo $t-\Delta$ in un punto $y$ con $|x-y|\le\vmax\Delta$; $y$ era occupato, quindi $y\in\Pres(t-\Delta)$ per ipotesi induttiva, e $x\in\dilata(\Pres(t-\Delta),\vmax\Delta)$. Per (i) e (v) il raggio che legge il suolo in un punto è privo di superfici fino al suolo, a meno del margine di lettura, quindi un punto occupato non è letto come suolo: $x\notin\Oss(t)$. Con posa stimata l'oggetto compare in $x'$ con $|x-x'|\le\varepsilon_p$ e $x'\notin\hat{\Oss}(t)$; se il disco di centro $x$ e raggio $\varepsilon_p$ fosse contenuto in $\hat{\Oss}(t)$ si avrebbe $x'\in\hat{\Oss}(t)$: dunque $x$ non appartiene all'insieme sottratto.
\end{proof}
```

Nel corollario aggiungere in testa «Sotto le ipotesi della Proposizione~\ref{prop:occ-contenimento},». In cap. 1 (tabella di sintesi, riga «Contenimento in $\Pres(t)$») e in cap. 9 (secondo punto) sostituire «posa entro tolleranza» con «posa esatta, o libero eroso del margine di posa; suolo piano; lettura per punto».

### 2. Contenimento e mappa a celle: il passo usa una proprietà che il cap. 3 dichiara non dimostrata (cap. 5, stessa proposizione; composizione con `def:map-libero`)

**Che cosa non torna.** Nel cap. 5 $\Oss(t)$ è «quello del §3», cioè la regola della cella (metà impronta più cella di guardia). Per quella regola «un punto occupato non è visto libero» non segue da (i): l'Osservazione `oss:map-nondice` (ii) dice essa stessa che «la sicurezza della cella intera è verificata in simulazione, non dimostrata». Inoltre l'enunciato non elenca (v), che la dimostrazione di `prop:map-sicurezza` (b) usa.

**Prova.** Controesempio minimo dentro (i), (iii), (iv): cella con $n(c)=12$ pixel; un oggetto sottile dà 2 pixel validi a quota fra 0,07 e 2,0 m (meno dei 3 richiesti per «occupato»); gli altri 10 leggono il suolo ($10\ge 6$), le vicine sono lette: la cella è «libero» e contiene un punto occupato, che esce da $\Pres$. Tutte le ipotesi dell'enunciato sono rispettate.

**Testo corretto.** L'enunciato della correzione 1 (lettura per punto, ipotesi (v)). Dopo la dimostrazione aggiungere:

```latex
Per la regola della cella (Definizione~\ref{def:map-libero}) il passo «un punto occupato non è letto come suolo» non è dimostrato: una cella può essere «libero» con meno di metà dell'impronta coperta da un oggetto. La Proposizione è quindi dimostrata per la lettura per punto \prova{D}; con la mappa a celle il contenimento poggia sulla verifica in simulazione del \S\ref{sec:map-banco} \prova{S}.
```

### 3. Sicurezza del «libero», parte (a) (cap. 3, `prop:map-sicurezza`; cap. 8, tabella degli enunciati, riga 2)

**Che cosa non torna.** «Nessuna cella … con pixel non validi nel fotogramma $t$ è dichiarata libera» è falso con la Definizione `def:map-libero`: una cella è letta se legge il suolo **almeno metà** dell'impronta. Lo dice anche `cex:map-muto` («protegge solo dove i pixel … risultano non validi su più di metà dell'impronta»). Nella riga 2 del cap. 8 «Buco … mai libero» ha lo stesso difetto, e porta come condizioni della parte (a) le ipotesi della parte (b).

**Prova.** Cella con 12 pixel, 5 non validi, 7 che leggono il suolo, vicine lette: «libero» per la Definizione, contro la lettera di (a).

**Testo corretto** (cap. 3, punto (a)):

```latex
\item nessuna cella in ombra, occupata, fuori campo o oltre portata è dichiarata libera al fotogramma $t$, e nemmeno una cella in cui meno di metà dei pixel dell'impronta legge il suolo (in particolare, con più di metà dei pixel non validi) o che ha una cella vicina in questa condizione;
```

Cap. 8, riga 2: «Fuori campo, oltre portata, suolo non visibile vicino, ombra, impronta letta per meno di metà (buchi compresi), sensore non in salute: mai «libero» & \prova{D} per costruzione, senza ipotesi sul sensore. Vale per ciò che non è visto; non afferma che ciò che è «libero» sia libero».

### 4. Conclusioni, primo punto (cap. 9, «Che cosa è dimostrato»)

**Che cosa non torna.** «Una cella dichiarata «libero» è priva di superfici fino al suolo, se … la posa è nota entro la tolleranza» è più forte di `prop:map-sicurezza` (b), che vale a posa **esatta** e per i **raggi dei pixel che leggono il suolo**, non per la cella (`oss:map-nondice`, ii). Scritto sotto \prova{D} è un enunciato non dimostrato.

**Testo corretto:**

```latex
\item Nessuna cella in ombra, fuori campo, oltre portata o letta per meno di metà dell'impronta è dichiarata «libero» (per costruzione); e, se la profondità valida è corretta, la posa è esatta e il suolo è piano, i raggi dei pixel che leggono il suolo di una cella «libero» sono privi di superfici fino al suolo, a meno del margine di lettura (Proposizione~\ref{prop:map-sicurezza}). La sicurezza della cella intera e la tenuta con un errore d'inclinazione entro $0{,}5^\circ$ sono verificate in simulazione, non dimostrate \prova{S}. Fuori da queste ipotesi l'enunciato cade: i controesempi sono il vetro, l'ostacolo che non rimanda segnale e l'errore d'inclinazione di $1^\circ$ (\S\ref{sec:map-controesempi}).
```

### 5. Annidamento, punto (b): «gli stessi eventi osservato» (cap. 5, `prop:occ-annidamento`)

**Che cosa non torna.** Il predittore entra nell'identità attraverso la porta del riaggancio («riagganciata se la misura è entro $w$ da $\Reg_{0,9}$», stesso capitolo; `SOLUZIONE_V3.md` r. 202). Due predittori con $\Reg_{0,9}$ diverse danno, alla ricomparsa, in un caso la traccia vecchia «osservato» nel ciclo stesso, nell'altro «identità ambigua» con una traccia nuova, che è «osservato» solo dopo la conferma. La dimostrazione dice «gli insiemi $C_\alpha$ compaiono solo in $\Reg_\alpha$ e nel punto mostrato» e contraddice il punto (c), che nomina la porta del riaggancio. Il fascicolo (parte I, §4, dim. (c)) riconosce questa dipendenza.

**Testo corretto** (punto (b) e sua dimostrazione):

```latex
(b) Il predittore non scrive alcuno stato di cella e non può far emettere «osservato» in un ciclo senza misura: a parità di fotogrammi, due predittori diversi danno gli stessi stati delle celle. Gli eventi «osservato» coincidono fino al primo riaggancio; dopo possono differire per l'identità attribuita e per l'istante di conferma, perché la porta del riaggancio usa $\Reg_{0,9}$.
```
```latex
(b) Lo stato della cella è funzione dei soli fotogrammi di profondità; «osservato» richiede nel ciclo una misura dentro la porta di una traccia confermata; il predittore entra nell'attribuzione delle misure alle tracce solo attraverso la porta del riaggancio.
```

Nel punto (c) premettere «Per ogni ingresso in un'ombra, a parità di stato delle tracce in quell'istante,»: il confronto lungo una successione di occlusioni non è dimostrato, perché lo stato delle tracce (e la soglia dei 4 fotogrammi della regola d'ingresso) dipende dal riaggancio precedente.

### 6. Fascia di guardia: manca un'ipotesi (cap. 5, `prop:occ-fascia`)

**Che cosa non torna.** La dimostrazione applica (ii) al contrario: «non rilevato in $t$» implica che in $[t-t_a,t]$ il soggetto è stato nell'ombra **oppure fuori campo oppure oltre portata**. L'enunciato chiede campo e portata solo all'istante $s$.

**Prova.** Controesempio dentro tutte le ipotesi scritte: un soggetto entra dal bordo laterale del campo in un istante fra $t$ e $s$, a più di $w$ da $\hat\Omb$; al fotogramma $t$ è fuori campo e quindi non è rilevato, senza violare (ii) per alcun $t_a\ge0$; in $s$ è nel campo, l'uscita in uso non lo riporta, e $c(s)\notin W$. Il sistema tratta questo caso con un'altra regola («l'avviso resta sul non osservato entro $w$»), non con questa proposizione.

**Testo corretto** (conclusione dell'enunciato e secondo passo della dimostrazione):

```latex
allora in ogni istante $s$ in cui è in uso un'uscita, prodotta da un fotogramma $t$, che non riporta il soggetto come osservato, se il soggetto è rimasto nel campo e in portata per tutto $[t-t_a,\,s]$, si ha $c(s)\in W$.
```
```latex
Poiché il soggetto è nel campo e in portata in tutto $[t-t_a,t]$ e non è rilevato in $t$, per (ii) esiste $t'\in[t-t_a,t]$ con $c(t')\in\Omb$.
```

**Simbolo $t_a$, non risolto.** In §`sec:occ-ipotesi` $t_a$ è «l'età del dato più vecchio usato da un'uscita»; nell'ipotesi (ii) e nella dimostrazione è il tempo massimo di mancato rilevamento fuori dall'ombra (il fascicolo, D4, lo dichiara «mia lettura»). Con la regola adottata nel cap. 3 («memoria di 0 fotogrammi») la prima grandezza vale 0, mentre la tabella usa 0,133 s con la dicitura «età (3 fotogrammi)». Nessun file decide: tenere una sola definizione, quella di (ii) («tempo entro cui un soggetto fuori dall'ombra, in campo e in portata, è riportato come osservato»), e nella tabella scrivere «$t_a=0{,}133$ s (assunto: due cicli)» al posto di «età (3 fotogrammi)». La proposizione riguarda l'insieme $W$, non il fatto che l'avviso sia acceso (premessa: ingresso riconosciuto).

### 7. «Un'etichetta non riduce l'avviso»: la premessa (2) non vale per il sistema descritto (cap. 5, `prop:occ-etichetta`)

**Che cosa non torna.** Il passo «per (1) e (2) stati delle celle, tracce e ingressi coincidono» chiede che il riaggancio non dipenda dall'etichetta. Ma nello stesso paragrafo «la forma della regione dipende dal modello di moto della classe», e la porta del riaggancio usa $\Reg_{0,9}$ (`BLOCCO_CLASSIFICAZIONE.md` r. 97 esclude la classe dalla porta in modo diretto, r. 101 dà la libreria per classe; `SOLUZIONE_V3.md` r. 202). Due esecuzioni con etichette diverse possono quindi differire nelle tracce dopo un riaggancio, e una traccia nuova (meno di 4 fotogrammi) non fa scattare un ingresso che la traccia vecchia farebbe scattare. La parte sul «libero» è vera senza condizioni; la parte sull'area d'avviso è dimostrata solo per ingresso.

**Testo corretto** (premessa (2), conclusione, e una frase dopo la dimostrazione):

```latex
(2) associazione, porta, riaggancio e ciclo di vita non leggano l'etichetta né grandezze che ne dipendono (in particolare la porta del riaggancio usi una regione che non dipende dalla classe),
```
```latex
Allora le celle «libero» sono identiche; per ogni ingresso in un'ombra l'area d'avviso con etichette contiene, in ogni istante, quella senza etichette; i rilasci con etichette sono un sottoinsieme di quelli senza.
```
```latex
Nella costruzione descritta la forma di $\Reg_{0,9}$ dipende dalla classe e la porta del riaggancio usa $\Reg_{0,9}$: la premessa (2) non è soddisfatta alla lettera. L'identità delle celle «libero» vale comunque, per la sola (1); l'inclusione delle aree d'avviso vale per ogni ingresso riconosciuto in entrambe le esecuzioni, non per la successione degli ingressi.
```

### 8. $\Pres$ scritto al posto di $W$ (cap. 6, `def:val-misure` punto «Sicurezza» (i) e tabella `tab:val-sicurezza`, riga «Soggetto nascosto fuori da $\Pres$»; cap. 1, schema a blocchi, «$\Reg_\alpha(t)$ e $\Pres(t)$»)

**Che cosa non torna.** Il cap. 6 chiama $\Pres(t)$ l'area d'avviso e marca \prova{D} lo zero su 175 802 istanti. Il cap. 5 distingue i due insiemi: «$\Pres$ è il riferimento teorico; il sistema realizza l'area d'avviso $W$», che esiste solo dopo un ingresso riconosciuto. La Proposizione di contenimento (senza tracce) non si trasferisce a $W$; per $W$ vale la Proposizione sulla fascia, con le sue premesse. Il cap. 5, lettura (6), e il cap. 6, §semi («controllo sull'area d'avviso»), indicano che la misura è su $W$. Quale insieme usi il codice della prova non l'ho verificato.

**Testo corretto.** Cap. 6: «…il cui centro sta fuori dall'area d'avviso $W(t)$»; riga della tabella: «Soggetto nascosto fuori da $W$»; ultima colonna: «\prova{D} nelle ipotesi della Proposizione~\ref{prop:occ-fascia} (bordo dell'ombra esatto, ingresso riconosciuto), \prova{S}». Cap. 1, schema: «occlusione: $\Reg_\alpha(t)$ e $W(t)$».

---

## Correzioni — B. Impreciso

### 9. Sicurezza del «libero», parte (b): il margine di lettura è un'ipotesi tacita (cap. 3)

La dimostrazione parla di un pixel «che restituisce il suolo alla quota attesa»; la regola accetta $|D_t(p)-z_0(p)|\le m(z_0(p))$. La conclusione vera è più debole: il raggio è vuoto fino a $z_0-m$, non fino al suolo. Il punto del raggio a profondità $z_0-m$ sta a quota $h\,m(z_0)/z_0$: `controlli.txt` §K dà 4,8–5,7 cm con $k=0{,}004$ e 9,7–12,7 cm con $k=0{,}0100$ fra 2 e 3 m (cifre mie, non da inserire). **Testo corretto** di (b): «…nessuna superficie interseca i raggi dei pixel che ne leggono il suolo a profondità inferiore a $z_0(p)-m(z_0(p))$, meno la tolleranza di misura: non è esclusa una superficie più vicina al suolo del margine \eqref{eq:map-margine}.» Nella dimostrazione: «Un pixel che legge il suolo ha profondità non inferiore a $z_0(p)-m(z_0(p))$, e $z_0(p)$ è la distanza del suolo lungo il raggio (Ipotesi~\ref{ip:map-piano} e posa esatta); per l'Ipotesi~\ref{ip:map-valida} il raggio è vuoto fino a quella profondità.»

### 10. Lemma del margine di posa: vale per lo spostamento in pianta, non per l'inclinazione (cap. 3, `lem:map-posa`, `cex:map-inclinazione`)

La dimostrazione suppone che lo stato calcolato nel riferimento stimato sia giusto in quel riferimento e che l'errore sposti soltanto i punti. Un errore d'inclinazione altera la quota ricostruita (`prop:geo-posa`: $\rho\,\delta\theta=5{,}2$ cm a 3 m è un errore di **quota**) e quindi lo stato: `cex:map-inclinazione` mostra celle occupate dichiarate «libero», che nessun margine in pianta ripara. **Testo corretto** (inizio del lemma): «Sotto l'Ipotesi~\ref{ip:map-posa}, intesa come spostamento nel piano del suolo (traslazione e rotazione attorno alla verticale), e supposto corretto nel riferimento stimato lo stato calcolato,». Dopo i valori numerici: «Il margine non copre l'errore d'inclinazione, che agisce sulla quota ricostruita e quindi sullo stato: per esso vale il conto diretto che segue.» In `cex:map-inclinazione`: «Errore d'inclinazione oltre la tolleranza di $0{,}5^\circ$ del dominio (il Lemma~\ref{lem:map-posa} non lo copre).»

### 11. Tabella della fascia (cap. 5, `tab:occ-fascia`)

Riga 2: $0{,}40/0{,}288=1{,}39$ m/s e $1{,}4\cdot0{,}288=0{,}404$ m: 1,4 m/s **non** è coperto (mancano 4 mm); «1,4 (margine nullo)» arrotonda dal lato non prudente. Riga 1: usa $\tau=0{,}150$ s mentre le altre e il resto dell'allegato usano 0,155 s; con 0,155 s viene 1,80 m/s (`controlli.txt` §C; il valore 1,80 è nel fascicolo, D4). **Testo corretto:** riga 2, quinta colonna: «1,39 (a 1,4 m/s mancano 4 mm)» — cifra ricalcolata, non presente nei file: in alternativa «meno di 1,4»; riga 1: «0 & 0,155 & 0 & 0,222 & 1,80», oppure tenere 0,150 e 1,85 aggiungendo nella colonna di descrizione «con la latenza di 0,150 s». Nel testo dopo la tabella: «il passo d'uomo ($1{,}4$ m/s) non è coperto nemmeno trascurando la tenuta».

### 12. Criterio stratificato (cap. 5, `oss:occ-criterio`)

0,999 e 0,026 sono probabilità del **solo primo stadio** (`controlli.txt` §I: 0,9993 e 0,0258). Se il criterio stratificato ha un secondo stadio come quello non stratificato (52 su 60), una copertura di 0,90 è respinta in tutto con probabilità 0,138 (cifra mia). **Testo corretto:** «…una copertura di 0,5 è respinta al primo stadio con probabilità 0,999 e una di 0,90 è respinta per errore al primo stadio con probabilità 0,026.»

### 13. Dichiarazioni «in tutte le celle» con l'intervallo di Wilson (cap. 6, `prop:val-celle`)

La dimostrazione usa $P(E_j)\le0{,}05/m$: vale per intervalli con copertura effettiva non inferiore al nominale; quella di Wilson è approssimata (`controlli.txt` §G: al 95 % nominale, $N=100$, minimo 0,910 per $p=0{,}005$). **Testo corretto:** «Se si giudicano insieme $m$ celle e ogni intervallo ha copertura non inferiore a $1-0{,}05/m$, …». Dopo la dimostrazione: «Con l'intervallo di Wilson, la cui copertura è approssimata, il limite $0{,}05$ è a sua volta approssimato.» Valore: $z_{60}=3{,}341$ (stampato 3,342).

### 14. Limite del guadagno di una struttura sparsa (cap. 7, `lem:cos-sparsa`)

«Il sensore vede **al più** la piramide» dà memoria sparsa ≤ quella della piramide, quindi rapporto densa/sparsa **≥** 3,8, non «non supera». Il 3,8 è il caso peggiore, quello che conta per dimensionare. **Testo corretto:** «…cioè il 26,3 % dei 72 m³ della regione: nel caso peggiore, con tutta la piramide vista libera, il rapporto fra memoria densa e memoria sparsa è $72/18{,}9=3{,}8$, prima del costo dell'indice; è il guadagno su cui si può contare, perché con ostacoli in scena il volume visto libero è minore e il rapporto maggiore.»

### 15. Minimalità di $\Pres$ (cap. 5, `prop:occ-monotonia` e frase seguente)

(a) La Definizione calcola la dilatazione «per eccesso» sulla griglia: con l'eccesso $\Pres$ non è minimo. (b) Manca la base dell'induzione. (c) «Può solo restringere il «libero», mai estenderlo» non segue: segue che non può estenderlo senza errore. **Testo corretto:** nell'enunciato «per oggetti puntiformi, $\varepsilon_p=0$ e dilatazione esatta (senza l'eccesso di griglia)»; nella dimostrazione, prima di «se $x\in\Pres(t)$»: «Base: $\Pres(0)=X$ e nessun fotogramma vincola l'istante 0.»; nella frase seguente: «una probabilità d'occupazione accumulata nel tempo non può estendere il «libero» senza sbagliare in almeno un mondo ammesso».

### 16. Continuità, punto (d) (cap. 5, `def:occ-avviso` e `prop:occ-annidamento`)

«Con l'ostacolo fermo $L(t)=\emptyset$» è falso alla lettera ($L(t)$ contiene le celle libere lontane); vero è $L(t)\cap W(t_0)=\emptyset$, e richiede che l'ombra **stimata** sia la stessa a ogni ciclo. **Testo corretto:** «Con l'ostacolo fermo e l'ombra stimata costante nessuna cella di $W(t_0)$ dista più di $w$ dall'ombra corrente: $L(t)\cap W(t_0)=\emptyset$ e $W(t)=W(t_0)$.» In (d): «Con l'ostacolo fermo e l'ombra stimata costante, …».

### 17. Forma e livelli

- `ce:occ-velocita`: «17 696 su 65 536» è contato **all'ultimo fotogramma**; a un fotogramma qualsiasi sono 30 288 (`controlli.txt` §A, §M). Scrivere «(8 successioni su 64; 17 696 su 65 536 con 4 celle, contando la violazione all'ultimo fotogramma)».
- Cap. 4, rumore del centro: «sta fra $\sigma/\sqrt n$ e $\sigma$ \prova{D}» vale con errori di uguale varianza e **correlazioni non negative**: aggiungerlo.
- Cap. 5, §ciclo: «con 3 fotogrammi la traccia manca nel 27,1 %, con 4 nel 5,2 %» sono binomiali (\prova{C}, cap. 4), non simulazione: spostare la marca \prova{S} dopo il punto e virgola e mettere \prova{C} su queste due.
- `tab:occ-classi`, «trattore di piazzale»: $\vmax=8{,}3>7{,}1$ m/s, quindi «no; alla massima dopo il contatto», come per «persona di corsa». Non ho ricontato «10 classi alla massima» sulle 15.
- `tab:occ-classi`, persona a piedi: $d_{\mathrm{serve}}(2{,}5)=4{,}505$ m con $t_{\mathrm{conf}}=0{,}267$ e 4,504 con $4/15$: «4,51» e «4,50» sono entrambi arrotondamenti; la fonte (`BLOCCO_CLASSIFICAZIONE.md` r. 156) scrive 4,51: lasciare.
- `prop:occ-annidamento`: \prova{D} per (b), (c) è «per costruzione della regola descritta»; la conformità del codice alla regola non è verificata da nessuno dei file letti: dirlo nella frase dopo la dimostrazione.

---

## Che cosa torna (rifatto)

Cap. 2: campo in coordinate del suolo, tre corollari, disco (5,66 e 5,79 m²), ombra, altezza minima, durata, banda senza dato, rumore, errore di quota, focale: enunciati, dimostrazioni e cifre (`controlli.txt` §J). Cap. 3: griglia bayesiana (0,847; −2,000; 3 colpi), lettura per punto, controesempio della memoria, limiti di Wilson per 0 su 300, 10, 131. Cap. 4: ordine della catena (forma debole D6 del fascicolo: usata), regola «mobile» ($P_{fa}=5{,}7\cdot10^{-7}$; $v_{0,5}$, $v_{0,9}$), forma chiusa di $Q$ e tabella $\sigma_p(\tocc)$ (tutte le 12 celle; 1,15 s e 1,95 s), massa (determinante 0 esatto; rango 3 su 4 con $p_0,v_0$ ignoti), differenza seconda (66,1 / 16,5 / 7,3; minimi quadrati 0,71 con 16 campioni), porta (9,210), conferma (27,1 / 5,2 / 0,9 %; 0,147 s), copertura attesa $\mathrm{Bin}(N,\alpha)$. Cap. 5: monotonia; ricorsione esaustiva (0 differenze su 65 536 e 32 768); ritaglio (0 violazioni su 2 000; 0,7826; 0,375; forma debole D7: usata); $\pm\sigma$ (0,3935; 2,45); intrusione (64 ms); criterio non stratificato (1; 0,865; 0,142); righe 3–4 della fascia (1,13; 0,56); tabella per classe (fasce, $d_{\mathrm{serve}}$, 1,44 e 7,1 m/s); forma debole D3 (interferenza monotòna) e D9 (peso: \prova{S}, non per costruzione): usate. Cap. 6: zero su $N$, Wilson (826 su 879), marginale, Beta (0,805; 0,848; 68; 110; 9), suolo per comportamento peggiore, semi contigui. Cap. 7: voxel, blocchi, tetto dei passi (128; 258), piramide (18,9; 26,3 %). Cap. 8: 3,036 $\sigma$ e 2,183 $\sigma$; formule $T_{\mathrm{ant}}$ e $d_{\mathrm{serve}}$ (coerenza dei termini; 1,44 e 1,07 m/s).

## Che cosa non ho controllato

- Le cifre di simulazione contro i file grezzi (ho rifatto solo gli intervalli di Wilson a partire dai conteggi stampati) e ogni simulatore.
- La corrispondenza fra regole descritte e codice (in particolare: quale insieme usa la prova dei 175 802 istanti; se la porta del riaggancio usa davvero una regione che dipende dalla classe quando la fascia di scenario è accesa).
- Il PDF (ho letto i sorgenti `.tex`), la bibliografia e la mappa «affermazione → chiave», i criteri A-4 e A-6.
- Cap. 1 oltre le righe marcate D; cap. 7 oltre i tre lemmi; cap. 8 oltre la tabella degli enunciati, la formula del portatore e la formula di §moto; appendici A e B.
- Il conteggio «3 classi su 15 a velocità tipica, 10 alla massima» e i profili di classe.
- `VERDETTO_INTEGRAZIONE.md` e i verdetti precedenti: non letti per intero (solo ricerche mirate in `SOLUZIONE_V3.md` e `BLOCCO_CLASSIFICAZIONE.md`).

File accanto: `controlli.py`, `controlli.txt` (uscita), `PREVISIONI.md`, `CIFRE.md`.
