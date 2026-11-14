# Controllo finale delle dimostrazioni — allegato tecnico corretto

Letti per intero, nel testo com'è ORA: capitoli 2, 3, 4, 5, conclusioni, sommario; del capitolo 6 le righe 1–150 e la riga 170; dei capitoli 1, 7, 8, dei simboli e dell'appendice A le righe con enunciati, marche \prova{D} e richiami. Programma: `controllo.py` (Python puro), uscita `controllo.txt`. Previsioni scritte prima: `PREVISIONI.md` (19:57).

## 1. Esito, cambi di stato, previsioni, regole

- **Enunciati controllati nei capitoli 2–8: 67** (cap. 2: 12; cap. 3: 13; cap. 4: 10; cap. 5: 17; cap. 6: 10; cap. 7: 3; cap. 8: 2). **Tornano: 62. Non torna: 1. Tornano con una condizione in più: 4.** Conclusioni e sommario, 8 voci: 5 tornano, 2 con una condizione in più, 1 non torna. In più, **11 richiami** fuori capitolo non coerenti con l'enunciato d'origine (R3: 2; R4: 1; R5: 5; R7, R8, R9: 1 ciascuno) e 2 da adeguare per R1.
- **Cambio di stato proposto.** `prop:occ-contenimento`: da «dimostrato» a **smentito nella forma scritta** (controesempio senza errore di posa: la striscia del margine di lettura), **dimostrato** per la lettura per punto esatta (margine nullo). La correzione precedente («oggetto più alto del margine di lettura») non basta: l'altezza dell'oggetto non conta.
- **Le 17 correzioni della verifica precedente** (che coprivano le sue 20 voci) risultano applicate nel testo: stato una per una nel §2bis. Una non bastava (la 1: R1), una è rimasta a metà (`t_a` nei simboli e in appendice A: R3), una ha introdotto un rinvio sbagliato (la 8, cap. 6: R4).
- **Previsioni.** P1 regge (6 voci, soglia 3). **P2 smentita a metà**: sulla griglia astratta regge (0 differenze su 65 536 e 32 768 successioni; con errore di posa di una cella la posizione vera è fuori in 447 istanti su 447; 0 con il libero eroso), ma sotto le ipotesi del testo corretto, che legge il suolo con il margine, c'è una violazione senza errore di posa. P3 regge. P4 regge (la forma di $\Reg_{0,9}$ dipende dalla classe ed entra nella porta del riaggancio). P5 regge: 0 discordanze numeriche (unico scarto: $r_{0,95}$ a 3 s, 3,635, stampato 3,64: arrotondamento).
- **Regole.** Scritture solo in questa cartella; niente git, sudo, rete; allegato non toccato. `numpy` non è installato: programma riscritto in Python puro dopo un primo lancio fallito (nessun risultato perso). **Indipendenza:** codice mio; condivido con l'allegato il testo, il modello e il tipo di lettore. Nessun simulatore rilanciato: le cifre \prova{S} non sono ricontrollate.

## 2. Correzioni residue

### R1 — Contenimento: falso con il margine di lettura (cap. 5, `prop:occ-contenimento`, dimostrazione e capoverso seguente; richiami in cap. 1 e 9)

**Com'è ora.** «…ogni punto del suolo su cui poggia, al fotogramma $t$, un oggetto più alto del margine di lettura \eqref{eq:map-margine} (punto \emph{occupato}) appartiene a $\Pres(t)$» e, nella dimostrazione, «il raggio che legge il suolo in un punto è privo di superfici fino al suolo, a meno del margine di lettura, quindi un punto occupato non è letto come suolo».

**Che cosa non torna.** Il raggio diretto a un punto $x$ dell'impronta che sta a distanza $\delta$ (in pianta) dietro la faccia vista dell'oggetto incontra la faccia alla profondità $z_0(1-\delta/\rho)$. Se $\delta\le\rho\,m(z_0)/z_0$ la lettura dista da $z_0$ meno di $m$: il pixel «legge il suolo», $x\in\Oss(t)$, e $x$ esce da $\Pres(t)$ già al primo fotogramma ($\Pres=X\setminus\Oss$). L'altezza dell'oggetto non entra. Nel tempo la striscia non si richiude: resta quella della distanza più lontana da cui l'oggetto è stato visto.

**Prova.** `controllo.txt` §B. Persona alta 1,7 m, faccia a 2,30 m, punto a 5 cm dentro l'impronta: lettura 2,525 m contro $z_0=2{,}580$ m, scarto 5,5 cm < $m=11{,}0$ cm. Striscia $\rho\,m/z_0$ sull'asse: 10,9 cm a 2,5 m e 14,4 cm a 3 m con $k=0{,}004$; 23,2 e 31,7 cm con $k=0{,}0100$. Oggetto in avvicinamento da 2,6 m, 8 fotogrammi: impronta fuori da $\Pres$ fino a 12,0 cm dalla faccia; con margine nullo 0 punti. La parte sulla posa richiama il Lemma, che vale solo per lo spostamento in pianta: va detto nell'enunciato.

**Testo corretto** (enunciato):

```latex
\begin{proposizione}[Contenimento]\label{prop:occ-contenimento}
Sia $\Oss(t)$ l'insieme dei punti del suolo il cui raggio, nel fotogramma $t$, è letto da un pixel valido alla profondità attesa del suolo (lettura per punto \emph{esatta}: margine di lettura nullo nella \eqref{eq:map-margine}). Sotto le ipotesi (i), (iv) e (v), a posa esatta ($\varepsilon_p=0$), ogni punto interno all'impronta al suolo di un oggetto al fotogramma $t$ (punto \emph{occupato}) appartiene a $\Pres(t)$. In particolare la posizione di un soggetto entrato in un'ombra appartiene a $\Pres(t)$ per ogni $t$ fino alla riosservazione, senza alcuna ipotesi sul numero dei soggetti né sull'esistenza di una traccia. Con posa nota entro $\varepsilon_p$ (ipotesi (iii), intesa come spostamento nel piano del suolo, come nel Lemma~\ref{lem:map-posa}) l'enunciato vale nel riferimento stimato; nel riferimento vero vale se nella \eqref{eq:occ-presenza} a $\Oss(t)$ si sostituisce l'insieme dei punti $x$ il cui disco di raggio $\varepsilon_p$ è contenuto nel libero stimato $\hat{\Oss}(t)$. \prova{D}
\end{proposizione}
```

Nella dimostrazione, al posto della frase «Per (i) e (v) il raggio che legge il suolo … $x\notin\Oss(t)$.»:

```latex
Per (i) e (v) un raggio letto alla profondità attesa del suolo è privo di superfici fino al suolo; il raggio diretto a un punto interno all'impronta incontra invece l'oggetto prima del suolo, quindi un punto occupato non è letto come suolo: $x\notin\Oss(t)$.
```

Al posto del capoverso «Per la regola della cella … \prova{S}.»:

```latex
Con il margine di lettura $m>0$ della \eqref{eq:map-margine} il passo «un punto occupato non è letto come suolo» cade su una striscia dell'impronta. Il raggio diretto a un punto che sta dietro la faccia vista dell'oggetto, a distanza $\delta$ in pianta, incontra la faccia alla profondità $z_0\,(1-\delta/\rho)$: se $\delta\le\rho\,m(z_0)/z_0$ la lettura dista da $z_0$ meno del margine e il punto è letto come suolo, qualunque sia l'altezza dell'oggetto. Sull'asse del campo, con $h=1{,}2\unita{m}$, $\theta=15^\circ$ e $k=0{,}004$, la striscia è larga $11\unita{cm}$ a $2{,}5\unita{m}$ e $14\unita{cm}$ a $3\unita{m}$; con $k=0{,}0100$, $23$ e $32\unita{cm}$ \prova{C}. La Proposizione è quindi dimostrata per la lettura per punto esatta \prova{D}; con il margine di lettura la parte dell'impronta più vicina alla camera può uscire da $\Pres$, e il contenimento dell'intera impronta non è dimostrato. Nemmeno per la regola della cella (Definizione~\ref{def:map-libero}) il passo è dimostrato: una cella può essere «libero» con meno di metà dell'impronta coperta da un oggetto. Con il margine di lettura e con la mappa a celle il contenimento poggia sulla verifica in simulazione del \S\ref{sec:map-banco} \prova{S}.
```

Le quattro larghezze sono **cifre mie**, non presenti nei file: se non si vogliono cifre nuove, togliere la frase «Sull'asse del campo … \prova{C}.» (la formula resta).

Richiami: `01_introduzione.tex`, riga «Contenimento in $\Pres(t)$…»: «lettura per punto» → «lettura per punto esatta (margine di lettura nullo)», e «con la mappa a celle il contenimento poggia sulla simulazione» → «con il margine di lettura e con la mappa a celle il contenimento poggia sulla simulazione». `09_conclusioni.tex`, secondo punto: «su suolo piano e con la lettura per punto; con la mappa a celle il contenimento poggia» → «su suolo piano e con la lettura per punto esatta, senza margine di lettura; con il margine e con la mappa a celle il contenimento poggia».

### R2 — Fascia di guardia: l'ipotesi (ii) va letta per il centro, e «rilevato» non è «riportato come osservato» (cap. 5, `ip:occ-modello` (ii), `prop:occ-fascia`)

**Che cosa non torna.** La dimostrazione passa da «$c(t')\notin\Omb$ per tutto $[t-t_a,t]$» a «il soggetto è fuori dall'ombra da più di $t_a$». Vale solo se «fuori dall'ombra» significa «con il centro fuori»: un corpo di raggio $r_c$ con il centro appena fuori è ancora in parte nascosto, e nel sistema descritto dà un gruppo tagliato («visto in parte», non «osservato»). Inoltre la notazione definisce $t_a$ con «riportato come osservato», l'ipotesi (ii) e la dimostrazione dicono «rilevato». Con $P_D<1$ nessun $t_a$ finito è un limite certo.

**Prova.** `controllo.txt` §C: con (ii) per il centro, 0 uscite su 200 000 fuori da $W$; con (ii) per il corpo intero ($r_c=0{,}225$ m), 48 866 su 200 000. Conferma entro due cicli con $P_D=0{,}9$: 0,81 (cap. 4, già nel testo).

**Testo corretto.** In `ip:occ-modello` (ii): «è rilevato entro un tempo $t_a$» → «è riportato come osservato entro un tempo $t_a$». Nell'enunciato:

```latex
Sotto le ipotesi (ii) e (iv), con la (ii) intesa per il centro (un soggetto con il centro fuori da $\Omb$, in campo e in portata, è riportato come osservato entro $t_a$), se
```
```latex
Per contenere l'intero corpo di raggio $r_c$ si aggiunge $r_c$ al secondo membro; se la (ii) vale solo quando tutto il corpo è fuori dall'ombra, se ne aggiunge un altro. \prova{D}
```

Nella dimostrazione: «nel quale il soggetto non è rilevato» → «che non lo riporta come osservato»; «e non è rilevato in $t$» → «e non è riportato come osservato in $t$»; «e sarebbe rilevato» → «e sarebbe riportato come osservato». Dopo «è un valore assunto \prova{N}» aggiungere:

```latex
Con $P_D<1$ nessun tempo finito è un limite certo: per una traccia nuova la conferma entro due cicli ha probabilità $0{,}81$ con $P_D=0{,}9$ (\S\ref{sec:sti-porta}).
```

### R3 — $t_a$ definito in due modi (`00_simboli.tex` r. 27; `A_parametri.tex` r. 45)

La correzione è stata applicata nel cap. 5 e non altrove. Simboli: «età del dato più vecchio usato da un'uscita» →

```latex
$t_a$ & tempo entro cui un soggetto fuori dall'ombra, in campo e in portata, è riportato come osservato\\
```

Appendice A: «con età $0{,}133\unita{s}$» → «con $t_a=0{,}133\unita{s}$ (assunto)».

### R4 — Lo zero di «soggetto nascosto fuori da $W$» non viene dalla Proposizione della fascia (`06_valutazione.tex` r. 132)

**Com'è ora.** «Lo zero della prima riga è dimostrato solo nelle ipotesi della Proposizione~\ref{prop:occ-fascia} (bordo dell'ombra esatto, ingresso riconosciuto, un solo soggetto per ombra, ostacolo fermo); altrove è un conteggio.»

**Che cosa non torna.** Le condizioni fra parentesi non sono le ipotesi di quella Proposizione ((ii), (iv), condizione \eqref{eq:occ-fascia}); e la sua condizione copre 1,13 m/s, mentre le prove hanno velocità d'ingresso fino a 1,8 m/s (stesso capitolo, condizioni comuni). Lo zero segue invece da $W\supseteq\hat\Omb=\Omb$, come dicono il cap. 5 (lettura 6) e la tabella del cap. 1 («per costruzione»). Non ho verificato come il programma di prova definisce «nascosto».

```latex
Lo zero della prima riga vale per costruzione dove l'ingresso è riconosciuto, l'ostacolo è fermo e l'ombra stimata coincide con la vera: allora $W(t)=\dilata(\hat\Omb,w)\supseteq\Omb$ (Definizione~\ref{def:occ-avviso}) e il centro di un soggetto nascosto sta in $\Omb$; altrove è un conteggio. Non è un'applicazione della Proposizione~\ref{prop:occ-fascia}, che riguarda il soggetto uscito dall'ombra e non ancora riportato come osservato, e la cui condizione \eqref{eq:occ-fascia} copre $1{,}13\unita{m/s}$, meno delle velocità d'ingresso di queste prove (fino a $1{,}8\unita{m/s}$).
```

### R5 — Etichetta di classe: la proposizione è vera come condizionale, i richiami dicono di più (cap. 5 `prop:occ-etichetta`; cap. 4 r. 76 e 79; cap. 8 r. 174 e 219; cap. 9 r. 31)

**Esito della rifattura.** Sotto (1), (2), (3) la dimostrazione è completa: $W_e(t_0)\supseteq W_0(t_0)$, $L_e(t)\subseteq L_0(t)$, induzione (`controllo.txt` §I: 0 violazioni su 220 000 passi, ombra mobile compresa). **Per il sistema descritto** nei cap. 4, 5, 8: la (1) vale; la (3) è una regola non eseguita (fascia fissa a 0,40 m: l'etichetta non entra affatto nell'avviso); la (2) non vale, e il cap. 5 lo dice. Resta vero: nessun «libero» da un'etichetta; per ogni ingresso riconosciuto in entrambe le esecuzioni l'area con etichette contiene quella senza. **Non è vero** che «la sicurezza delle indicazioni non dipende dall'etichetta». Controesempio con le sole regole del cap. 5: il soggetto esce dall'ombra di un primo ostacolo; con l'etichetta la regione ha un'altra forma, la misura cade oltre $w$ da $\Reg_{0,9}$, l'esito è «identità ambigua» e nasce una traccia nuova; se questa entra nell'ombra di un secondo ostacolo prima di avere 4 fotogrammi di misura, l'ingresso non scatta e lì non c'è avviso; senza etichetta la traccia riagganciata lo fa scattare. Il controesempio è costruito sulle regole scritte, non eseguito. Il cap. 4 scrive inoltre «non entra … nella porta», contro la nota del cap. 5.

**Seconda imprecisione.** «i rilasci con etichette sono un sottoinsieme di quelli senza» è vero per l'insieme $L(t)$, falso per le celle tolte da $W$: una cella dell'anello fra le due fasce si rilascia solo nell'esecuzione con etichette (§I: 6 776 passi su 220 000).

**Testo corretto.** Cap. 5, conclusione dell'enunciato: «i rilasci con etichette sono un sottoinsieme di quelli senza» → «l'insieme di rilascio $L(t)$ con etichette è contenuto in quello senza». Cap. 4, riquadro (r. 76) e cap. 9 (r. 31), al posto di «La sicurezza delle indicazioni non dipende dall'etichetta.»:

```latex
Un'etichetta non produce un «libero» e, per ogni ingresso in un'ombra riconosciuto, non riduce l'area d'avviso (Proposizione~\ref{prop:occ-etichetta}); può cambiare l'esito di un riaggancio, e quindi gli ingressi successivi (\S\ref{sec:occ-classe}).
```

Cap. 8 (r. 174), al posto di «La sicurezza delle indicazioni non dipende dall'etichetta (invarianti 5 e 15).»:

```latex
Un'etichetta non produce un «libero» e non toglie né restringe un avviso acceso (invarianti 5 e 15); può cambiare l'esito di un riaggancio, e quindi gli ingressi successivi (\S\ref{sec:occ-classe}).
```

Cap. 4 (r. 79): «non entra nel costo d'associazione né nella porta;» →

```latex
non entra nel costo d'associazione né nella porta di validazione; entra invece, attraverso la forma della regione di previsione, nella porta del riaggancio (\S\ref{sec:occ-classe});
```

Cap. 8 (r. 219): «avviso con etichette non più stretto» → «per ogni ingresso riconosciuto in entrambe le esecuzioni, avviso con etichette non più stretto».

### R6 — Regione di ripiego: la Definizione e il testo dicono due insiemi diversi (cap. 5, `def:occ-regione`, «Passaggio a previsto ampio», figura)

La Definizione dà $W(t)\setminus\Oss(t)$ («dell'ombra e della sua fascia»); due capoversi dopo «la regione è tutta la maschera dell'ombra», e la didascalia «tutto il non visto libero dell'ombra»; la descrizione di progetto dice «tutta la maschera dentro il cuneo». I punti (a) e (d) valgono per entrambe, ma (a) «per ogni $t$» chiede che la regione stia in $W(t)$. Quale valga nel programma: **non verificato**. Testo che rende coerenti le tre frasi e conserva (a) e (d):

```latex
$\Reg_\alpha(t)=C_\alpha(t)\cap W(t)$ per $\alpha<1$; se questo insieme è vuoto, e in ogni altro caso di «previsto ampio», $\Reg_\alpha(t)=\bigl(\hat\Omb(t)\setminus\Oss(t)\bigr)\cap W(t)$, cioè tutto il non visto libero dell'ombra (\emph{regione di ripiego}). Si pone $\Reg_1(t)=W(t)$.
```
```latex
(d) $\hat\Omb\cap\Oss(t)=\emptyset$ per definizione d'ombra e, con l'ostacolo fermo e l'ombra stimata costante, $\hat\Omb\subseteq W(t_0)=W(t)$; quindi la regione di ripiego è $\hat\Omb\neq\emptyset$.
```

### R7 — Riquadro del cap. 3: la parte (b) è dimostrata a posa esatta, non «entro 0,5°» (`03_mappa.tex`, ultimo riquadro)

«parte (b) dimostrata nel modello;» sta sotto «inclinazione nota entro $0{,}5^\circ$», ma `prop:map-sicurezza` (b) chiede $\varepsilon_p=0$ (le conclusioni lo dicono giusto). →

```latex
parte (b) dimostrata nel modello a posa esatta; con errore d'inclinazione entro $0{,}5^\circ$ la tenuta è verificata in simulazione, non dimostrata;
```

### R8 — Conclusioni, terzo punto: manca l'ipotesi (ii) (`09_conclusioni.tex` r. 9)

«l'ostacolo è fermo e il soggetto resta nel campo e in portata» →

```latex
l'ostacolo è fermo, il soggetto rimanda segnale, resta nel campo e in portata ed è riportato come osservato entro $t_a$ da quando il suo centro è fuori dall'ombra
```

### R9 — Tabella di sintesi del cap. 1, prima riga \prova{D} (`01_introduzione.tex` r. 89)

«per l'inverso:» promette più della parte (b). → «per l'inverso, limitato ai raggi dei pixel che leggono il suolo e a meno del margine di lettura:».

## 2bis. Le correzioni precedenti, una per una

| N. | Oggetto | Stato nel testo corretto |
|---|---|---|
| 1 | contenimento con errore di posa | applicata; la parte sulla posa torna (447 su 447 fuori senza erosione, 0 con erosione); la clausola «più alto del margine di lettura» non ripara il margine: **R1** |
| 2 | contenimento e mappa a celle | applicata; il capoverso va esteso al margine (R1) |
| 3 | sicurezza del «libero», parte (a) | applicata bene; cap. 8 riga 2 coerente |
| 4 | conclusioni, primo punto | applicata bene |
| 5 | annidamento (b), (c) | applicata bene; enunciato e dimostrazione coerenti |
| 6 | fascia: campo e portata; simbolo $t_a$ | ipotesi applicata bene; resta la lettura di (ii) (**R2**) e $t_a$ nei simboli e in appendice (**R3**) |
| 7 | etichetta: premessa (2) | applicata bene nel cap. 5; i richiami no (**R5**) |
| 8 | $\Pres$ al posto di $W$ | applicata (cap. 6 e schema del cap. 1); il rinvio alla Proposizione della fascia è sbagliato (**R4**) |
| 9 | sicurezza (b), margine | applicata bene |
| 10 | Lemma del margine di posa | applicata bene; va richiamata nel contenimento (R1) |
| 11 | tabella della fascia | applicata bene (riga 1 con la latenza dichiarata; riga 2 «meno di 1,4») |
| 12 | criterio stratificato | applicata bene |
| 13 | «in tutte le celle» | applicata; la clausola «ed è costruito con $z_m$» è ridondante ma non falsa |
| 14 | struttura sparsa | applicata bene |
| 15 | minimalità di $\Pres$ | applicata bene |
| 16 | $L(t)\cap W(t_0)=\emptyset$ | applicata bene |
| 17 | forma e livelli (6 punti) | applicati; il riquadro del cap. 3 non era fra questi (**R7**) |

## 3. Elenco degli enunciati

T = torna; C = torna con una condizione in più; N = non torna. Fra parentesi il livello dichiarato, giusto salvo dove detto.

**Cap. 2.** `oss:geo-focale` (C) T · `prop:geo-campo` (D) T, equivalenza rifatta nei due versi · `cor:geo-suolo` T (1,2426; 0,9166; 0,2947) · `cor:geo-basso` T · `cor:geo-tetto` T · `prop:geo-disco` (C) T (5,661 e 5,785 m²) · `prop:geo-ombra` (D) T · `prop:geo-amin` (D) T · `prop:geo-durata` (D) T · `prop:geo-banda` (D) T · `prop:geo-rumore` (D) T · `prop:geo-posa` (D) T.

**Cap. 3.** `def:map-stati`, `def:map-libero` T · `prop:map-sicurezza` (a) (D) T, coerente con la regola di metà impronta · (b) (D) T · `oss:map-nondice` T · `lem:map-posa` (D) T, cifre 2,6 / 8,2 / 15,5 cm e 0,69° / 0,57° · `cex:map-inclinazione`, `cex:map-vetro`, `cex:map-muto` T (coerenti con (a) e con il Lemma) · `oss:map-fermo` T · `cex:map-memoria` (C) T · `prop:map-logodds` (C/S) T · lettura di un punto (D) T. Riquadro finale: R7.

**Cap. 4.** `prop:sti-ordine` (D) T · rumore del centro fra $\sigma/\sqrt n$ e $\sigma$ (D) T con le condizioni aggiunte · `prop:sti-mobile` (D) T ($5{,}73\cdot10^{-7}$; $1{,}49\cdot10^{-5}$) · `ctr:sti-misti` (S) T, non rieseguito · `prop:sti-crescita` (D) T: composizione esatta su 200 coppie razionali; tabella riprodotta (0,156 / 0,344 / 0,848 / 1,485; 1,147 s e 1,945 s) · `prop:sti-massa` (D) T: rango 1, determinante 0 esatto; rango 3 su 4 con $p_0,v_0$ · differenza seconda (D) T (66,1 / 16,5 / 7,3; 0,714 con 16 campioni) · porta (D) T (9,210) · `prop:sti-conferma` (D) T, formula confermata per enumerazione · copertura attesa $\mathrm{Bin}(N,\alpha)$ (D) T (188–205; $8{,}1\cdot10^{-6}$; $2{,}5\cdot10^{-6}$; 0,012). Riquadro e «Interfaccia»: R5.

**Cap. 5.** `ip:occ-modello` C (R2: (ii)) · `def:occ-presenza` T · **`prop:occ-contenimento` N (R1)** · `cor:occ-libero-adesso` T, eredita R1 · `prop:occ-monotonia` (D) T, minimalità compresa · `ce:occ-velocita` (C) T (8 su 64; 17 696 all'ultimo fotogramma, 30 288 a uno qualsiasi) · `def:occ-avviso` T · `prop:occ-fascia` (D) C (R2) · tabella della fascia (C) T (1,846; 1,389; 1,128; 0,564) · `def:occ-regione` C (R6) · `prop:occ-annidamento` (a), (b), (c), (d) (D) T; correzione della porta del riaggancio applicata bene; (a) e (d) con R6 · `prop:occ-ritaglio` (D) T (0 violazioni su 19 455; uguaglianza in 19 455 su 19 455) · `oss:occ-sigma` (D) T · `oss:occ-intrusione` (D) T · `oss:occ-criterio` (C) T (0,99928; 0,02583) · `prop:occ-etichetta` (D) C (R5): livello giusto per il condizionale, non per il sistema · dominio per classe (C) T (tutte le righe di $d_{\mathrm{serve}}$ e della fascia; 1,442 e 7,11 m/s).

**Cap. 6.** `def:val-misure` T ($W$ al posto di $\Pres$: applicata) · esempio di Wilson T · `prop:val-zero` (D) T · `prop:val-celle` (D) T ($z_{60}=3{,}341$: applicata) · `oss:val-unita` T · `prop:val-marginale` (D) T · `prop:val-beta` (D) T (0,805; 0,848; 68; 110; 9) · `oss:val-nonvale` T · `prop:val-suolo` (D) T · `lem:val-semi` (D) T. Testo sulla prima riga della tabella di sicurezza: R4.

**Cap. 7.** `lem:cos-voxel` (C) T · `lem:cos-passi` (D) T · `lem:cos-sparsa` (C) T (18,94 m³; 26,3 %; verso della disuguaglianza corretto).

**Cap. 8.** Tabella degli invarianti, righe 2, 4, 5, 9, 10, 15: T (5 e 15 lette come proprietà di una sola esecuzione) · formula della regola «mobile» in moto (D) T (3,036 e 2,183). Righe 174 e 219: R5.

**Conclusioni e sommario.** Punto 1 T · punto 2 C (R1) · punto 3 C (R8) · punto 4 T · punti 5 e 6 T · «Il classificatore» N (R5) · sommario T («nelle ipotesi dichiarate»).

## 4. Che cosa non ho controllato

- Le cifre di simulazione e ogni simulatore; la conformità dei programmi alle regole (in particolare: quale insieme usa il programma per «nascosto» in R4 e quale regione di ripiego in R6).
- Il capitolo 6 dalla riga 151 in poi (tavole dei risultati) salvo la riga 170; i capitoli 1, 7, 8 e le appendici fuori dalle righe indicate; il PDF; la bibliografia.
- La compilazione dei frammenti dentro l'allegato: li ho compilati da soli con il preambolo (`prova_frammenti.tex`, vedi `controllo.txt` in coda), con i riferimenti incrociati non risolti.
- Se con il margine di lettura valga una forma più debole del contenimento (impronta contenuta in $\Pres$ dilatato della striscia): **non risolto**; lo deciderebbe una dimostrazione per induzione con il raggio di dilatazione aumentato, oppure un controesempio su una sezione piana con oggetti che ruotano.

## 5. Che cosa propongo dopo

Applicare R1–R5 (toccano ciò che l'allegato chiama «dimostrato»); R6–R9 sono di coerenza. Chi applica R1 decide se tenere le quattro larghezze della striscia, che sono cifre nuove.
