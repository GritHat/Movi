# Fascicolo «enunciati e dimostrazioni»

<!-- PARTE I: entra nell'allegato. PARTE II: solo per chi compone, non entra. -->

# PARTE I — Contenuto per l'allegato

## 1. Notazione, definizioni e ipotesi

Oltre alla notazione comune si usano: $X$ la regione del suolo coperta dalla mappa; $B(r)$ il disco chiuso di raggio $r$; $A\oplus B(r)=\{x: \mathrm{dist}(x,A)\le r\}$ la dilatazione di $A$; $\hat\Omega$ l'ombra stimata e $\varepsilon_\Omega$ l'errore del suo bordo; $w$ la larghezza della fascia di guardia; $W(t)$ l'area d'avviso di «possibile presenza»; $a$ l'età del dato più vecchio usato da un'uscita; $\varepsilon_p(\rho)=\varepsilon_t+\rho\,\delta_\theta$ il margine di posa (errore di traslazione $\varepsilon_t$, errore angolare $\delta_\theta$ in radianti); $c(t)$ il centro del soggetto; $M$ la massa e $u(t)$ la forza (per non confonderle con le matrici del filtro); $G$ una misura di probabilità sul suolo, $S$ l'insieme delle celle ammesse, $E_p$ una regione con $G(E_p)\ge p$.

**Stati della cella.** A ogni fotogramma ogni cella di $X$ ha uno e un solo stato: *libero* (appartiene a $O(t)$: il suolo della cella è visto alla quota attesa da pixel validi del fotogramma $t$ e nessun ritorno sopra il suolo cade nella cella), *occupato osservato* (primo ritorno sopra il suolo), *in ombra* (appartiene a $\Omega(t)$: sta oltre un primo ritorno lungo il raggio), *non osservato* (fuori campo, oltre portata, pixel non valido). I quattro stati formano una partizione di $X$.

**Ipotesi.** Gli enunciati dichiarano quali usano.

1. *Profondità valida = giusta.* Un pixel valido con profondità $d$ garantisce che il raggio è privo di superfici fino a $d$ (meno la tolleranza di misura).
2. *Superfici che rimandano segnale.* Ogni superficie nel campo e in portata produce un pixel valido; un soggetto fuori dall'ombra, in campo e in portata, è rilevato entro un tempo $a$.
3. *Camera ferma, posa nota entro una tolleranza.* L'errore di posa sposta un punto a distanza $\rho$ di al più $\varepsilon_p(\rho)$.
4. *Velocità limitata.* Ogni punto di ogni oggetto si muove con continuità a velocità $\le v_{\max}$.
5. *Pavimento piano.*
6. *Un solo soggetto per ombra.*

Tutti i risultati numerici di questo capitolo sono dimostrazioni, conti o simulazioni: nessuno è stato ottenuto su un sensore fisico.

## 2. Sicurezza del «libero»

**Proposizione 1 (sicurezza del «libero»).** Sia la regola: *lo stato «libero» è scritto solo dalla funzione che legge il fotogramma corrente, e solo per le celle di $O(t)$*. Allora: (a) nessuna cella in ombra, fuori campo, oltre portata o con pixel non validi nel fotogramma $t$ è dichiarata libera al fotogramma $t$; (b) sotto le ipotesi 1, 3 (con $\varepsilon_p=0$) e 5, se una cella è dichiarata libera al fotogramma $t$, all'istante d'acquisizione nessuna superficie interseca i raggi che ne raggiungono il suolo.

*Dimostrazione.* (a) Per definizione $O(t)$ contiene solo celle il cui suolo è colpito da pixel validi del fotogramma $t$; gli stati sono una partizione, quindi una cella in ombra o non osservata non sta in $O(t)$, e nessun'altra funzione scrive «libero». (b) Un pixel valido che restituisce il suolo alla quota attesa ha profondità $d$ pari alla distanza del suolo lungo il raggio (ipotesi 5 e posa esatta); per l'ipotesi 1 il raggio è vuoto fino a $d$. $\square$

*Livello di prova:* (a) dimostrato per costruzione; (b) dimostrato nel modello delle ipotesi 1, 3, 5; non verificato sperimentalmente.

**Che cosa la proposizione non dice.** (i) La garanzia riguarda il suolo e i raggi che lo raggiungono, non la colonna sopra la cella: un oggetto sospeso sopra i raggi lascia la cella «libero»; l'uscita corretta è «suolo visto libero», non «spazio libero». (ii) Vale all'istante d'acquisizione, non a quello d'uso (Corollario 1). In simulazione (150 fotogrammi, finestra d'uso di 0,20 s), 537 celle-fotogramma dichiarate libere su 88 418 risultano occupate entro la finestra; un margine di 0,33 m (per 1,4 m/s) attorno a ombra e non osservato porta gli errori a 0 ma conserva lo 0,4 % del libero, uno di 0,55 m (per 2,5 m/s) lo 0,0 %.

**Osservazione 1 (controesempio alla regola con memoria).** La regola «libero se il suolo è stato visto in almeno uno degli ultimi 3 fotogrammi» non soddisfa la Proposizione 1. Controesempio minimo, una cella e due fotogrammi: al fotogramma 1 il suolo è visto (pixel valido); al fotogramma 2 un corpo che non rimanda segnale entra nella cella e i pixel diventano non validi. La regola con memoria dichiara «libero» una cella occupata; la regola del solo fotogramma corrente dichiara «non osservato». La variante «l'occupato e l'ombra del fotogramma corrente prevalgono sulla memoria» corregge il caso del corpo che rimanda segnale, non questo. Età massima del dato ricordato: $2\Delta=0{,}133$ s a 15 Hz, cioè $v_{\max}\cdot 2\Delta = 0{,}33$ m a 2,5 m/s. *Livello di prova:* verificato per calcolo (caso minimo); verificato in simulazione con due programmi indipendenti: 1 186 punti del suolo sotto il corpo dati per liberi, con almeno un errore in 87 fotogrammi su 87; 58 fotogrammi su 90 con almeno un errore (0,64; Wilson 0,54–0,74). Il prezzo della regola senza memoria è la perdita di «libero» vero quando mancano misure, dal lato prudente.

**Lemma 1 (margine di posa).** Sotto l'ipotesi 3, se $B(x,\varepsilon_p(\rho))\subseteq \hat O(t)$, dove $\hat O$ è il libero calcolato con la posa stimata e $\rho$ la distanza di $x$, allora $x$ è libero nel riferimento vero.

*Dimostrazione.* La posa vera porta $x$ in un punto $x'$ con $|x-x'|\le\varepsilon_p(\rho)$, quindi $x'\in B(x,\varepsilon_p)\subseteq\hat O(t)$. $\square$

Valori a $\rho=3$ m: $\delta_\theta=0{,}5°\Rightarrow 3\cdot 0{,}00873 = 2{,}6$ cm; $\varepsilon_t=3$ cm, $\delta_\theta=1°\Rightarrow 3+5{,}2=8{,}2$ cm; $\varepsilon_t=5$ cm, $\delta_\theta=2°\Rightarrow 5+10{,}5=15{,}5$ cm. *Livello di prova:* dimostrato; verificato in simulazione (sezione piana, 200 scene per caso): senza margine, scene con almeno un falso «libero» 114 su 200 e 162 su 200; con un margine non inferiore a quello teorico 0 su 200; con 10 cm dove ne servono 15,5, 1 su 200.

**Fuori dalle ipotesi.** *Vetro e superfici che danno profondità valida ma sbagliata (cade l'ipotesi 1):* in simulazione, con una lastra trasparente di 1 × 2 m a 2,0 m dal sensore, la lettura del fotogramma corrente dà per liberi 654 punti della lastra su 800 (600 su 800 con la lastra a 1,5 m); il limite non è risolto da nessuna regola sulla mappa. *Errore di posa di 1° (cade l'ipotesi 3 senza il margine del Lemma 1):* a 3 m sono 5,2 cm, più di mezza cella.

## 3. Insieme di possibile presenza

**Definizione.** $\Pi(0)=X$ e, a ogni fotogramma,
$$\Pi(t)=\bigl[\Pi(t-\Delta)\oplus B(v_{\max}\Delta+\varepsilon_p)\bigr]\setminus O(t).$$
Sulla griglia la dilatazione si calcola per eccesso; ciò che è fuori dalla griglia o non è mai stato valutato appartiene a $\Pi$. È il passo di previsione di un filtro a insiemi con dinamica a velocità limitata, nella linea dei metodi che sovrastimano gli ostacoli nascosti con insiemi raggiungibili \cite{orzechowski2018}.

**Proposizione 2 (contenimento).** Sotto le ipotesi 1, 3 e 4, ogni punto occupato al fotogramma $t$ appartiene a $\Pi(t)$. In particolare la posizione di un soggetto entrato in un'ombra appartiene a $\Pi(t)$ per ogni $t$ fino alla riosservazione, senza alcuna ipotesi sul numero dei soggetti né sull'esistenza di una traccia.

*Dimostrazione.* Per induzione su $t$. Base: $\Pi(0)=X$. Passo: sia $x$ occupato al tempo $t$. Per l'ipotesi 4 il punto materiale che sta in $x$ si trovava al tempo $t-\Delta$ in un punto $y$ con $|x-y|\le v_{\max}\Delta$; $y$ era occupato, quindi $y\in\Pi(t-\Delta)$ per ipotesi induttiva; tenuto conto dell'errore di posa fra i due fotogrammi (ipotesi 3), $x\in\Pi(t-\Delta)\oplus B(v_{\max}\Delta+\varepsilon_p)$. Per l'ipotesi 1 un punto occupato non è visto libero, $x\notin O(t)$. Dunque $x\in\Pi(t)$. $\square$

**Corollario 1 («libero adesso»).** Se l'uscita del fotogramma $t$ è in uso in $[t+\tau,\,t+\tau+\Delta]$, una cella $V$ con $\mathrm{dist}(V,\Pi(t))>v_{\max}(\tau+\Delta)+\varepsilon_p$ è vuota in tutto $[t,\,t+\tau+\Delta]$. *Dimostrazione.* Ogni punto occupato in un istante $s$ dell'intervallo dista al più $v_{\max}(s-t)\le v_{\max}(\tau+\Delta)$ da un punto occupato al tempo $t$, che sta in $\Pi(t)$. $\square$

**Proposizione 3 (monotonia: nessun rilascio a tempo).** $\Pi(t)\supseteq\Pi(t-\Delta)\setminus O(t)$: un punto esce da $\Pi$ solo in un fotogramma in cui è osservato libero. Né un contatore di tempo, né la covarianza di un filtro, né la chiusura di una traccia riducono $\Pi$. Inoltre, per oggetti puntiformi e $\varepsilon_p=0$, $\Pi(t)$ è minimo: per ogni $x\in\Pi(t)$ esiste un mondo ammesso dalle ipotesi, coerente con tutti i fotogrammi, con un oggetto in $x$ al tempo $t$.

*Dimostrazione.* Poiché $0\in B(r)$, $A\subseteq A\oplus B(r)$; togliendo $O(t)$ ai due membri si ha l'inclusione, e nella ricorsione non compare altro termine sottrattivo. Minimalità, per induzione: se $x\in\Pi(t)$ allora $x\notin O(t)$ ed esiste $y\in\Pi(t-\Delta)$ con $|x-y|\le v_{\max}\Delta$; per ipotesi induttiva una traiettoria ammessa e coerente con i fotogrammi fino a $t-\Delta$ arriva in $y$; la si prolunga con il segmento da $y$ a $x$ percorso in $\Delta$ a velocità $\le v_{\max}$, che è coerente con il fotogramma $t$ perché $x\notin O(t)$. $\square$

Conseguenza della minimalità: ogni regola che dichiara libera una cella esclusa dal Corollario 1 sbaglia in almeno un mondo ammesso; una probabilità d'occupazione accumulata nel tempo può solo restringere il «libero», mai estenderlo.

*Livello di prova:* dimostrato nel modello (ipotesi 1, 3, 4; minimalità solo per oggetti puntiformi). Verificato per calcolo esaustivo su griglie in una dimensione (passo $\le$ 1 cella per fotogramma, tutte le successioni di insiemi osservati): 4 celle e 4 fotogrammi, 65 536 successioni; 5 celle e 3 fotogrammi, 32 768 successioni; in tutte l'insieme delle posizioni finali delle traiettorie coerenti coincide con $\Pi(t)$, nessuna violazione della monotonia, nessun «libero adesso» occupato. Verificato in simulazione su una sezione piana (2–4 oggetti, 300 fotogrammi per corsa):

| Regola | $v_{\max}$ dichiarata / vera (m/s) | Celle-fotogramma «libere» e occupate durante l'uso | Corse con almeno un errore |
|---|---|---|---|
| $\Pi$ con il Corollario 1 | 2,5 e 1,4 / uguale; misure mancanti 0 e 5 % | 0 | 0 su 96 (Wilson 0–0,038) |
| Suolo visto, senza margine | 2,5 / 2,5 | 45 829 | 24 su 24 |
| Probabilità d'occupazione statica (log-odds) | 2,5 / 2,5 | 138 230 | 24 su 24 |
| $\Pi$, velocità vera doppia | 0,9 / 1,8 | 1 172 | 23 su 24 (0,80–0,99) |
| $\Pi$, velocità vera doppia | 0,4 / 0,8 | 301 | 21 su 24 (0,69–0,96) |

**Fuori dalle ipotesi.** *Velocità doppia (cade l'ipotesi 4):* controesempio minimo con 3 celle e 2 fotogrammi: al primo sono viste libere le celle 1 e 2, quindi $\Pi=\{3\}$; al secondo non si vede nulla, $\Pi=\{2,3\}$; un oggetto che percorre due celle per fotogramma può essere nella cella 1 (8 successioni su 64 nel caso minimo; 17 696 su 65 536 con 4 celle). *Profondità valida e sbagliata (cade l'ipotesi 1):* la sottrazione di $O(t)$ toglie punti occupati; il contenimento non vale.

**Costo.** Il «libero adesso» garantito è quasi vuoto a passo d'uomo: nella stessa simulazione resta dichiarabile lo 0,1 % del suolo visto libero con $v_{\max}=2{,}5$ m/s e il 3,2 % con 1,4 m/s. Con il sensore frontale a 3 m di portata il raggio della massima sfera inscritta nel volume visto è $r_{\mathrm{in}}=0{,}98$ m e l'età utile massima di un «libero» è $r_{\mathrm{in}}/v_{\max}-(\tau+\Delta)$: con $\tau+\Delta=0{,}217$ s, 0,175 s a 2,5 m/s e 0,483 s a 1,4 m/s. Per questo l'uscita del sistema non afferma mai «via libera», ma «suolo visto libero fino a $d$» all'istante d'acquisizione.

## 4. Area d'avviso, regioni di previsione e loro annidamento

**Definizioni.** Quando una traccia confermata entra nell'ombra di un occlusore fermo, nasce l'area d'avviso $W(t_0)=\hat\Omega\oplus B(w)$, con $w=0{,}40$ m. A ogni fotogramma $W(t)=W(t-\Delta)\setminus L(t)$, dove $L(t)$ è l'insieme delle celle viste libere da 3 fotogrammi consecutivi e distanti più di $w$ dall'ombra corrente (con l'occlusore fermo $L(t)=\emptyset$ e $W(t)=W(t_0)$); l'avviso si chiude solo per riaggancio dell'identità o quando tutte le sue celle sono state viste libere. Il predittore produce a ogni ciclo un insieme di celle $C_\alpha(t)$; la regione mostrata al livello $\alpha<1$ è
$$\mathcal R_\alpha(t)=\bigl[C_\alpha(t)\cap W(t)\bigr]\setminus\bigl[O(t)\setminus(\hat\Omega\oplus B(w_p))\bigr],\qquad w_p=0{,}20\ \text{m},$$
e, se questo insieme è vuoto, $\mathcal R_\alpha(t)=W(t)\setminus O(t)$ con il segno «previsto ampio». Si pone $\mathcal R_1(t)=W(t)$.

**Proposizione 4 (annidamento e interferenza monotòna).** (a) $\mathcal R_\alpha(t)\subseteq\mathcal R_1(t)=W(t)\subseteq\hat\Omega\oplus B(w)$ per ogni $t$ e ogni $\alpha$, e $\mathcal R_\alpha(t)$ non contiene celle viste libere nel fotogramma corrente oltre la fascia $w_p$. (b) Il predittore non scrive alcuno stato di cella e non produce uscite «osservato»: a parità di fotogrammi, due predittori diversi danno gli stessi stati delle celle e gli stessi eventi «osservato». (c) L'area d'avviso con il predittore contiene quella senza: la previsione può accendere o mantenere l'avviso, mai toglierlo. (d) Con l'occlusore fermo, dall'ingresso nell'ombra alla chiusura dell'avviso, $\mathcal R_\alpha(t)\neq\emptyset$ a ogni ciclo.

*Dimostrazione.* (a) Entrambe le espressioni che definiscono $\mathcal R_\alpha$ sono sottoinsiemi di $W(t)$; $W(t)\subseteq W(t_0)$ perché la ricorsione solo sottrae; la seconda affermazione è la sottrazione scritta nella definizione. (b) Lo stato della cella è funzione dei soli fotogrammi di profondità; «osservato» è emesso se e solo se nel ciclo c'è una misura dentro la porta della traccia; gli insiemi $C_\alpha$ compaiono solo in $\mathcal R_\alpha$ e nel punto mostrato. (c) La condizione d'ingresso è la disgiunzione «ultima misura entro $w$ dall'ombra» oppure «punto previsto nell'ombra o entro $w$»: aggiungere un disgiunto non toglie ingressi. Il rilascio $L(t)$ non dipende dal predittore; la sola altra dipendenza è la porta sul riaggancio (un rilevamento a più di 0,40 m da $\mathcal R_{0,9}$ non riaggancia), che può solo impedire una chiusura. (d) $\hat\Omega\cap O(t)=\emptyset$ per definizione d'ombra e, con l'occlusore fermo, $\hat\Omega\subseteq W(t_0)=W(t)$; quindi $W(t)\setminus O(t)\supseteq\hat\Omega\neq\emptyset$. $\square$

L'enunciato «la previsione non interferisce con l'avviso» va quindi letto nella forma (c): l'interferenza esiste ed è monotòna, dal lato prudente. La continuità (d) è condizionata all'ingresso: se la traccia è chiusa prima che l'ingresso sia riconosciuto, non c'è né avviso né regione.

*Livello di prova:* dimostrato per costruzione. Verificato in simulazione (sensore fermo, soggetto puntiforme, tre geometrie): passaggi con almeno un ciclo senza regione 0 su 2 716, 0 su 2 800, 0 su 2 798 (complessivamente 0 su 8 314; Wilson 0–0,0005); cicli di $\mathcal R_{0,9}$ su celle viste libere oltre la fascia: 0; istanti con il soggetto nascosto dentro $\mathcal R_1$: 10 883 su 10 883, 11 772 su 11 772, 13 236 su 13 236. La premessa di (d) cade in 9 passaggi su 2 800 (0,3 %; Wilson 0,2–0,6 %) con la regola d'ingresso completa e in 87 su 2 800 con la sola condizione sull'ultima misura.

**Fuori dalle ipotesi.** *Secondo soggetto nella stessa ombra (cade l'ipotesi 6):* la chiusura per riaggancio non è un'osservazione diretta del suolo; se nell'ombra c'è un secondo soggetto mai tracciato, il riaggancio del primo chiude l'avviso con il secondo ancora nascosto (le celle restano «in ombra», mai «libero»). In simulazione l'identità è attribuita al soggetto sbagliato e l'avviso rilasciato in 193 casi su 193 e in 347 su 357 (0,97; Wilson 0,95–0,98). L'insieme $\Pi$ del §3 non ha questo difetto, perché non dipende dalle tracce.

## 5. Non osservabilità della massa

**Proposizione 5.** Nel modello del punto materiale $M\ddot p(t)=u(t)$, con $u$ ignota, e misure di sola posizione $y_k=p(t_k)+n_k$, la massa $M$ non è identificabile: per ogni $\lambda>0$ le coppie $(M,u)$ e $(\lambda M,\lambda u)$ producono la stessa legge delle misure.

*Dimostrazione.* $\ddot p=u/M=(\lambda u)/(\lambda M)$: a parità di condizioni iniziali le due coppie danno la stessa traiettoria $p(\cdot)$ e quindi la stessa distribuzione di $(y_k)$; nessuno stimatore funzione delle misure può distinguere $M$ da $\lambda M$. Con forza costante in una dimensione, $p(t)=p_0+v_0t+\tfrac{u}{2M}t^2$ e il gradiente rispetto a $(u,M)$ è $\tfrac{t^2}{2}\,g$ con $g=(1/M,\,-u/M^2)^\top$; l'informazione di Fisher è $\sigma^{-2}\sum_k \tfrac{t_k^4}{4}\,gg^\top$, di rango 1, con direzione nulla $(u,M)^\top$. $\square$

*Livello di prova:* dimostrato nel modello dichiarato; verificato per calcolo in aritmetica razionale ($u=120$ N, $M=75$ kg, 30 misure a 15 Hz: determinante esattamente 0). *Fuori dall'ipotesi:* con forza nota e non proporzionale alla massa l'informazione su $M$ è positiva; in caduta libera $u=Mg$, $\ddot p=g$ e la massa resta non identificabile. Un sensore di profondità non misura forze: nel sistema la massa non compare; ciò che si osserva è l'ingombro.

## 6. Ordine della catena

**Proposizione 6.** Siano $Z_k=\{z_k^1,\dots,z_k^{n_k}\}$ i rilevamenti non etichettati del ciclo $k$ e, per ogni traccia $i$, il filtro con previsione $(\hat x_i^-,P_i^-)=(F\hat x_i,\;FP_iF^\top+Q)$ e aggiornamento funzione di $(\hat x_i^-,P_i^-,z)$ per una misura $z$ attribuita a $i$. Allora ogni esecuzione corretta rispetta l'ordine parziale: rilevamento e previsione $\to$ associazione $\to$ aggiornamento $\to$ decisione.

*Dimostrazione.* L'aggiornamento della traccia $i$ ha come argomento una misura della traccia $i$: richiede che $Z_k$ esista (rilevamento) e che sia fissata la corrispondenza fra tracce e misure (associazione). L'associazione usa la porta $\nu^\top S^{-1}\nu\le\gamma$ con $\nu=z-H\hat x_i^-$ e $S=HP_i^-H^\top+R$: richiede la previsione. La decisione legge stato e covarianza aggiornati. $\square$

La forma esatta è dunque: *il passo di aggiornamento consuma misure associate; il passo di previsione precede l'associazione*. Un filtro posto a monte del rilevamento può operare solo sui pixel di profondità, non sugli oggetti. È lo schema dei tracciatori per rilevamento, con filtro di Kalman e assegnazione ungherese a valle del rilevatore \cite{bewley2016}. Per la porta, in due dimensioni: $\gamma=-2\ln(1-P)$, cioè 5,991 al 95 % e 9,210 al 99 %. *Livello di prova:* dimostrato per costruzione (dipendenze fra i dati); non è un risultato sperimentale.

## 7. Livello di una regione ritagliata

**Proposizione 7.** Sia $G$ una misura di probabilità, $E_p$ con $G(E_p)\ge p$, $S$ con $G(S)>0$. Il livello della regione ritagliata $E_p\cap S$ rispetto alla distribuzione condizionata a $S$ è
$$q=\frac{G(E_p\cap S)}{G(S)}\;\ge\;1-\frac{1-p}{G(S)},$$
con uguaglianza se $S\supseteq X\setminus E_p$ e $G(E_p)=p$.

*Dimostrazione.* $G(E_p\cap S)=G(S)-G(S\setminus E_p)$ e $G(S\setminus E_p)\le G(X\setminus E_p)\le 1-p$; si divide per $G(S)$. Se $S\supseteq X\setminus E_p$ la prima disuguaglianza è un'uguaglianza. $\square$

Il risultato non richiede che $G$ sia gaussiana. Il limite è informativo solo se $G(S)>1-p$. Esempi: $p=0{,}95$, $G(S)=0{,}23\Rightarrow q\ge 1-0{,}05/0{,}23=0{,}78$; $G(S)=0{,}08\Rightarrow q\ge 0{,}375$. Ritagliare un cerchio «al 95 %» sulle celle ammesse senza rinormalizzare non conserva quindi il livello dichiarato: la regione va estratta dalla distribuzione rinormalizzata su $S$. *Livello di prova:* dimostrato; verificato per calcolo su 2 000 casi casuali (gaussiana discreta, $S$ semipiano): 0 violazioni.

## 8. Fascia di guardia

**Proposizione 8.** Sia l'occlusore fermo, $\Omega$ l'ombra vera e $\hat\Omega$ quella stimata, con $\Omega\subseteq\hat\Omega\oplus B(\varepsilon_\Omega)$; sia $W=\hat\Omega\oplus B(w)$. Sotto le ipotesi 2 e 4, se
$$w\;\ge\;\varepsilon_\Omega+v_{\max}\,(a+\tau+\Delta),$$
allora in ogni istante $s$ in cui il soggetto è nel campo e in portata ed è in uso un'uscita che non lo riporta come osservato, $c(s)\in W$. Per contenere l'intero corpo di raggio $r_c$ si aggiunge $r_c$ al secondo membro.

*Dimostrazione.* L'uscita in uso in $s$ viene da un fotogramma $t$ con $s\le t+\tau+\Delta$, nel quale il soggetto non è rilevato. Per l'ipotesi 2 esiste $t'\ge t-a$ con $c(t')\in\Omega$ (altrimenti il soggetto sarebbe fuori dall'ombra da più di $a$ e sarebbe rilevato). Per l'ipotesi 4, $|c(s)-c(t')|\le v_{\max}(a+\tau+\Delta)$; poiché $c(t')\in\hat\Omega\oplus B(\varepsilon_\Omega)$, $\mathrm{dist}(c(s),\hat\Omega)\le\varepsilon_\Omega+v_{\max}(a+\tau+\Delta)\le w$. $\square$

Con $w=0{,}40$ m e $\Delta=1/15$ s la velocità coperta $v_{\max}=(w-\varepsilon_\Omega)/(a+\tau+\Delta)$ vale:

| Età $a$ (s) | Latenza $\tau$ (s) | $\varepsilon_\Omega$ (m) | Tempo totale (s) | $v_{\max}$ coperta (m/s) |
|---|---|---|---|---|
| 0 (solo fotogramma corrente) | 0,150 | 0 | 0,217 | 1,85 |
| 0,133 (memoria di 3 fotogrammi) | 0,155 | 0 | 0,355 | 1,13 |
| 0,133 | 0,155 | 0,20 | 0,355 | 0,56 |

Senza il termine di tenuta $\Delta$ la seconda riga dà 0,288 s: $2{,}5\cdot 0{,}288=0{,}72$ m, oltre la fascia, e $1{,}4\cdot 0{,}288=0{,}40$ m, cioè margine nullo a passo d'uomo. La condizione è sufficiente, non necessaria: il caso peggiore è un soggetto che si allontana dall'ombra alla velocità massima senza essere rilevato per tutto il tempo $a$. *Livello di prova:* dimostrato nel modello (ipotesi 2 e 4, occlusore fermo); valori verificati per calcolo; la tenuta su un sensore fisico, dove $\varepsilon_\Omega$ e $a$ vanno misurati, non è verificata sperimentalmente. *Fuori dalle ipotesi:* occlusore mobile ($\Omega$ non costante); velocità doppia di quella dichiarata (la fascia necessaria raddoppia nel termine cinematico); soggetto che non rimanda segnale ($a$ non è limitato).

## 9. Tre indicatori che non misurano ciò che dichiarano

**Osservazione 2 (il «$\pm\sigma$» in due dimensioni).** Per $x\sim\mathcal N(\mu,\Sigma)$ in $\mathbb R^2$, $P\bigl((x-\mu)^\top\Sigma^{-1}(x-\mu)\le k^2\bigr)=1-e^{-k^2/2}$. *Dimostrazione:* con il cambio di variabile che rende $\Sigma$ l'identità e passando a variabili polari $(r,\vartheta)$, $\int_0^k r\,e^{-r^2/2}\,dr=1-e^{-k^2/2}$. $\square$ Per $k=1$ si ha $1-e^{-1/2}=0{,}393$: un'etichetta «posizione $\pm\sigma$» contiene il soggetto nel 39 % dei casi anche con un modello esatto (in una dimensione sarebbe il 68,3 %); il 95 % richiede $k=\sqrt{-2\ln 0{,}05}=2{,}45$. *Livello di prova:* dimostrato; verificato per calcolo (Monte Carlo, $N=2\cdot10^6$: 0,3932).

**Osservazione 3 (probabilità d'intrusione su una distribuzione ritagliata).** Sia $\pi_t$ la distribuzione di posizione di un soggetto nascosto, con supporto nelle celle non viste libere $S(t)=X\setminus O(t)$, e $V$ un volume protetto. Se $V\subseteq O(t)$, allora $P_{\mathrm{intr}}(t)=\pi_t(V)=0$ a ogni ciclo, qualunque sia la distanza del soggetto da $V$. *Dimostrazione:* $V\cap S(t)=\emptyset$. $\square$ Con il soggetto fermo nell'ombra a 9 cm da $V$, il tempo per entrarvi a 1,4 m/s è $0{,}09/1{,}4=64$ ms, meno della latenza (222 ms più un ciclo di 67 ms). L'indicatore dice «dov'è adesso secondo il modello», non «può entrare»: può solo abbassare un allarme, e non è usato come criterio. *Livello di prova:* dimostrato per costruzione; verificato in simulazione ($P=0$ a ogni istante provato fra 0 e 3 s).

**Osservazione 4 (criterio d'accettazione non stratificato).** Si consideri il criterio a due stadi su 30 passaggi (almeno 28 dentro: superato; al più 22: respinto; altrimenti altri 30 e almeno 52 su 60), con la composizione 21 «prosegue», 5 «sosta», 4 «torna». Se chi prosegue e chi sosta è sempre coperto e chi torna non lo è mai, i passaggi dentro sono $21+5=26$ con certezza; $23\le26\le27$ porta al secondo stadio, dove $26+26=52\ge52$: il criterio è superato con probabilità 1. *Livello di prova:* verificato per calcolo esatto (convoluzione di binomiali in aritmetica razionale): probabilità di superamento 1 anche con copertura 0,5 su chi torna; 0,865 con tutti i comportamenti a 0,90; 0,142 con tutti a 0,80. La precisione dichiarata va quindi verificata per comportamento: con 30 passaggi per comportamento (almeno 28 superato, al più 23 respinto), una copertura di 0,5 è respinta al primo stadio con probabilità 0,999 e una di 0,90 è respinta per errore con probabilità 0,026.

## 10. Quadro riassuntivo

| Enunciato | Ipotesi usate | Livello di prova | Dove cade |
|---|---|---|---|
| Prop. 1, sicurezza del «libero» | 1, 3, 5 | dimostrato; non verificato sperimentalmente | vetro; memoria fra fotogrammi; errore di posa senza margine |
| Lemma 1, margine di posa | 3 | dimostrato; simulazione, 200 scene per caso | errore oltre la tolleranza dichiarata |
| Prop. 2 e Cor. 1, contenimento e «libero adesso» | 1, 3, 4 | dimostrato; esaustivo su griglie piccole; simulazione, 96 corse | velocità oltre $v_{\max}$; profondità sbagliata |
| Prop. 3, monotonia e minimalità | 1, 4 (minimalità: oggetti puntiformi) | dimostrato; esaustivo su griglie piccole | — |
| Prop. 4, annidamento, continuità | ingresso riconosciuto; 6 per la chiusura | per costruzione; simulazione, 8 314 passaggi | ingresso mancato; secondo soggetto |
| Prop. 5, massa | forza ignota | dimostrato | forza nota non proporzionale a $M$ |
| Prop. 6, ordine della catena | — | per costruzione | — |
| Prop. 7, livello dopo il ritaglio | $G(S)>0$ | dimostrato; 2 000 casi | non informativo se $G(S)\le1-p$ |
| Prop. 8, fascia di guardia | 2, 4, occlusore fermo | dimostrato; valori per calcolo | $\varepsilon_\Omega$ o $a$ oltre il dichiarato |

---

# PARTE II — Provenienza e controlli (per chi compone; non entra nell'allegato)

Percorsi relativi a `.sciame/20261114-1301-percezione-challenge/`. Ricalcoli: `f13-allegato/01-dimostrazioni/ricalcoli.py` (Python puro, 5 s), uscita in `ricalcoli.txt`, si rifà con `sh rifai.sh`. Previsioni scritte prima del lancio: `PREVISIONI.md` (PF1–PF9, 2026-11-14T18:02:46+01:00).

## II.0 Cambi di stato, regole violate, scostamenti

- **Previsioni:** PF1–PF3, PF5–PF9 reggono. **PF4 regge sui valori analitici; il primo Monte Carlo (N = 400 000) dà 0,3916, scarto 0,0019, oltre la soglia di 0,001 che avevo scritto** (2,5 errori tipo). Ho aggiunto *dopo* un secondo lancio (N = 2 000 000: 0,3932, errore tipo 0,0003): non cieco. Nella parte I ho messo il secondo.
- **Indipendenza.** I miei controlli condividono con le fonti il modello e le ipotesi; il codice è mio e non importa niente dei file dello sciame. Il controllo esaustivo di Π è in una dimensione: copre errori d'algebra nella ricorsione, non la geometria del sensore. Le cifre di simulazione della parte I NON sono rifatte: sono **ritrovate** nei file grezzi indicati sotto (o, dove detto, solo nel documento che le riporta).
- **Scostamento dalla consegna:** non ho rilanciato i simulatori altrui; non ho letto per intero i verdetti (ricerca testuale mirata) né `PIANO_MISURE.md`, `AUDIT.md`, `MOTO_PROPRIO.md`, `f10-dati`. Nessun `stato.md` (lavoro breve). Scritture solo in `f13-allegato/01-dimostrazioni/`. Nessun git, nessuna rete.
- **Enunciati che ho indebolito o cambiato rispetto ai file** (decisione da confermare): vedi II.2, punti D1–D7.

## II.1 Provenienza, riga per riga

| Parte I | Fonte (file, paragrafo) | Mio ricalcolo |
|---|---|---|
| Prop. 1 (a), (b) | `f4/H-012/05-correzioni/SOLUZIONE_V2.md` §3 inv. 1, 2, 5; `f7-estensione/13-soluzione/DECISIONE.md` §1.3 (I1–I3); `f4/H-012/09-arbitro/VERDETTO.md` r. 11 (premesse); `f7-estensione/16-verdetto/VERDETTO_ESTENSIONE.md` r. 13 | dimostrazione riscritta; nessuna cifra |
| «suolo visto libero», non colonna | `VERDETTO_ESTENSIONE.md` r. 46 (K-104, 68 celle con una barra nella colonna) | non ricontato (cifra non usata nella parte I) |
| 537 celle-fotogramma su 88 418; 0,4 % col margine | `f7-estensione/11-torneo/risultati_k105.txt` r. 2 e 4 | ritrovato nel grezzo: torna |
| Oss. 1, caso minimo | `DECISIONE.md` §0 (2), §1.4 (1) | `ricalcoli.py` B: torna (memoria → libero con corpo che non rimanda; «occupato di ora vince» non basta) |
| 1 186 punti, 87 fotogrammi | `f7-estensione/11-torneo/risultati_a5c.txt` r. 3–4 | ritrovato: torna |
| 58 fotogrammi su 90 | `f7-estensione/15-verifica/risultati_vq3c_lancio1.txt` r. 62 (identico nei lanci 2 e 3) | ritrovato: torna; Wilson mio 0,54–0,74 |
| 0,33 m = 2,5 × 0,133 | `SOLUZIONE_V2.md` §3 inv. 1 | 0,333 m: torna |
| Lemma 1; 2,6 / 8,2 / 15,5 cm | `f7-estensione/01-matematico/CONSEGNA.md` §5 (T6); `risultati.txt` E | `ricalcoli.py` G: torna (con δ in radianti o con la tangente, uguale alla prima cifra decimale) |
| 114/200, 162/200, 0/200, 1/200 | `f7-estensione/01-matematico/risultati.txt` B | ritrovato: torna |
| Vetro 654 su 800 (2,0 m); 600 su 800 (1,5 m) | `f7-estensione/11-torneo/risultati_a8.txt` r. 18–20 e r. 5–7 | ritrovato: torna. Il verdetto riporta solo 654, senza la distanza |
| 1° = 5,2 cm a 3 m | `DECISIONE.md` §1.2 | 3·tan 1° = 5,24 cm: torna |
| Def. di Π, Prop. 2, Cor. 1, Prop. 3 | `f7-estensione/01-matematico/CONSEGNA.md` §5 (H1–H5, T1, T2, T4) | dimostrazioni riscritte per esteso (T2 nel file è «a schizzo»: qui completa per oggetti puntiformi); `ricalcoli.py` A: 0 differenze su 65 536 + 32 768 successioni |
| Tabella del §3 | `f7-estensione/01-matematico/risultati.txt` A (righe PI, nucleo, bayes) e `risultati_braccio.txt` | ritrovato: torna. **Nota:** nel grezzo ho contato 4 configurazioni × 24 corse = 96; la consegna del matematico dice «368 corse»: non le ho ricontate tutte, nella parte I c'è 96 |
| 0,1 % e 3,2 % del visto libero | `risultati.txt` A, colonna dich/F | ritrovato: torna (primo lancio; la consegna riporta anche 0,2 % e 5,1 % con altri semi) |
| ρ = 0,98 m; 0,175 s e 0,483 s | `risultati.txt` E | `ricalcoli.py` G: torna (con h = 0,2167 s). La consegna scrive 0,17 e 0,48 (h = 0,222) |
| Controesempio velocità doppia (3 celle) | mio, caso minimo del braccio «G» del matematico | `ricalcoli.py` A |
| Def. di W, 𝓡_α; Prop. 4 | `f8-continuita/13-soluzione/MODIFICHE_CONTINUITA.md` §2.1, 2.4, 2.5, 2.6, 2.10 (inv. 3, 4, 6, 10); `f8-continuita/16-verdetto/VERDETTO_CONTINUITA.md` r. 22, 25, 26, 112, 113; `SOLUZIONE_V2.md` B5 | dimostrazione riscritta; (c) riformulata (D3) |
| 0 su 2 716 / 2 800 / 2 798 | `f8-continuita/13-soluzione/ris/LETTURA.txt` r. 12, 103, 194 (riga del predittore adottato: passaggi 2 716 / 2 800 / 2 798, colonna «vuoto» 0, colonna «R90libCic» 0) | ritrovato nel grezzo: torna; Wilson mio su 8 314: 0–0,0005 |
| 10 883, 11 772, 13 236 | `LETTURA.txt` r. 56, 147, 214 | ritrovato: torna |
| 9 su 2 800; 87 su 2 800 | `MODIFICHE_CONTINUITA.md` §2.6; `VERDETTO_CONTINUITA.md` r. 22 | **solo dal documento**, grezzo non trovato con la ricerca fatta; Wilson mio 0,17–0,61 % |
| 193 su 193; 347 su 357 | `MODIFICHE_CONTINUITA.md` §4; `f8-continuita/16-verdetto/riconta_verdetto.txt` r. 99–100 (347/357 ricontato lì) | 347/357 ritrovato nel riconteggio; 193/193 solo dal documento; Wilson mio 0,949–0,985 |
| Prop. 5 | `f1/21d3813ca7e1/CONSEGNA.md` §1.2; `f2/03-triage/TRIAGE.md` F-002 | `ricalcoli.py` F: det = 0 esatto (D5) |
| Prop. 6 | `f1/21d3813ca7e1/CONSEGNA.md` §1.1; `TRIAGE.md` F-003 | dimostrazione riscritta; forma precisata (D6); γ = 5,991 e 9,210 ricalcolati |
| Prop. 7; 0,78 e 0,38 | `f8-continuita/05-inferenza/CONSEGNA.md` §2 critica 1 | `ricalcoli.py` C: 0,7826 e 0,3750; 0 violazioni su 2 000 casi (il file: 15 casi) |
| Prop. 8; tabella | `SOLUZIONE_V2.md` B5 e §5; `f4/H-012/09-arbitro/VERDETTO.md` r. 48 (0,72 m; margine zero a 1,4 m/s); `f7-estensione/01-matematico/risultati.txt` E (1,85 m/s) | `ricalcoli.py` G: 1,846; 0,72; 0,404; **1,13 e 0,56 sono miei** (D4) |
| Oss. 2 | `f9-preproposta/03-kalman/CONSEGNA.md` §5 | `ricalcoli.py` D: 0,3935; 2,4477 |
| Oss. 3; 64 ms; 222 ms | `f9-preproposta/12-avversario/CONSEGNA.md` r. 15 e 31; `risultati_p2.txt` r. 4–9 | P = 0,0000 ritrovato nel grezzo; 64 ms torna; i 222 ms sono presi dal file, non verificati |
| Oss. 4 | `f8-continuita/04-statistico/CONSEGNA.md` critica 4 e §4; `out_h9.txt`; `h9_cieco.py` | `ricalcoli.py` E (frazioni esatte): 1; 1; 0,484; 0,865; 0,142; stratificato 0,9993 e 0,0258: torna |

## II.2 Discordanze e punti in cui la forma dimostrabile è più debole di quella presentata

- **D1. «Limite inferiore 99,25 %» per 400 su 400** (`SOLUZIONE_V2.md` §1, verdetto del nucleo): è Clopper–Pearson unilaterale al 95 % ($0{,}05^{1/400}=0{,}9925$), non Wilson. Con Wilson bilaterale al 95 %, che è la notazione comune, è **0,9905**. Non l'ho usato nella parte I; chi lo usa deve dire quale intervallo è.
- **D2. Invariante 1 del nucleo, «0,33 m, meno della fascia»:** vero per la sola età (2Δ), ma con la latenza sono 0,72 m a 2,5 m/s (già nei file). Nella parte I la memoria è presentata come regola smentita (Oss. 1) e il conto completo sta nella Prop. 8.
- **D3. «La previsione non tocca l'avviso»** (`VERDETTO_CONTINUITA.md` r. 113): alla lettera è falsa, perché la regola d'ingresso e la porta sul riaggancio usano la previsione. La forma dimostrabile è la monotonia (Prop. 4 c). Inoltre **l'enunciato «Π non si riduce se non per osservazione diretta» vale per Π (Prop. 3) ma non per l'area d'avviso realizzata**, che si chiude anche per riaggancio: è lì che entra l'ipotesi «un solo soggetto per ombra».
- **D4. Fascia di guardia.** I file danno due conti diversi: h = τ + Δ senza età (1,85 m/s) ed età + latenza senza tenuta (0,288 s: 0,72 m; margine zero a 1,4 m/s). La condizione che so derivare ha tutti e tre i termini: con a = 0,133, τ = 0,155, Δ = 0,067 la velocità coperta è 1,13 m/s (0,56 con 20 cm d'errore di bordo). **Queste due cifre non sono nei file dello sciame**: sono l'applicazione della formula; se «niente contenuto nuovo» le esclude, si tolgano le righe 2–3 della tabella e resti la frase sul 0,288 s. Con τ = 0,155 invece di 0,150 la prima riga dà 1,80 m/s, non 1,85. La definizione di $a$ come tempo massimo di mancato rilevamento fuori dall'ombra è mia lettura: nei file $a$ è solo l'età del «libero» ricordato.
- **D5. Fisher, «det/traccia² = 5·10⁻¹⁷»** (`f1/21d3813ca7e1`): è lo zero in virgola mobile; il valore esatto è 0. Nella parte I: «determinante esattamente 0».
- **D6. Ordine della catena:** «il filtro viene dopo l'associazione» è esatto solo per l'aggiornamento; la previsione precede l'associazione. Forma corretta nella Prop. 6.
- **D7. Prop. 7:** il file la dà «nel modello gaussiano troncato»; vale per ogni misura di probabilità. Il file arrotonda 0,375 a 0,38.
- **D8. Prop. 1:** i file presentano «ciò che non è visto non è mai libero» come regola unica; la parte (b) («ciò che è dichiarato libero è libero») è un enunciato diverso, che vale solo sui raggi verso il suolo e solo all'acquisizione. Lo «0 falsi liberi profondi» delle simulazioni è per la lettura *sui punti*; sulla *cella* c'è un controesempio (`VERDETTO_ESTENSIONE.md` r. 5, punto 2), e la regola per cella è ancora in discussione (II.4).
- **D9.** Il pavimento della regione («tutto il non visto libero dell'ombra») l'ho formalizzato come $W(t)\setminus O(t)$: è una mia lettura di `MODIFICHE_CONTINUITA.md` §2.1; se il codice usa $\hat\Omega$ senza la fascia, (a) e (d) valgono lo stesso. Anche la sottrazione esplicita delle celle viste libere oltre $w_p$ nella definizione di $\mathcal R_\alpha$ è una mia formalizzazione dell'invariante 4: nel codice è ottenuta con un peso (un decimo a ciclo) e lo «0 cicli» è misurato, non garantito dalla sola regola del peso. Se l'allegato descrive il peso, il punto (a) sulla fascia va dato come «verificato in simulazione», non «per costruzione». Analogamente $L(t)$ («oltre la fascia» = a più di $w$ dall'ombra corrente) è la mia lettura di `SOLUZIONE_V2.md` B5, e (d) l'ho ristretta all'occlusore fermo.

## II.3 Citazioni

- Usate (stato «verificata» in `documentazione/RIFERIMENTI.md` per il dato usato): `orzechowski2018` (ostacoli nascosti sovrastimati con insiemi/intervalli di stato), `bewley2016` (Kalman e ungherese a valle del rilevatore).
- **Non usate perché non verificate per il dato:** `kalman1960` (verificata in parte: solo dati bibliografici) → la frase sul filtro è senza citazione; `clopper1934` (in parte); `kuhn1955` (in parte); `hornung2013` (in parte, testo non letto) e i parametri di OctoMap (la chiave `octomap` non è in `riferimenti.bib`) → non citati, e la riga «log-odds» della tabella non ne riporta i parametri. Per l'intervallo di Wilson **non c'è alcuna voce** nell'elenco: se l'allegato lo cita serve una voce nuova, verificata. Per la funzione di ripartizione della χ² a 2 gradi di libertà e per la non identificabilità non c'è fonte nell'elenco: sono dimostrate nel testo.

## II.4 Ciò che l'integrazione in corso (f12) può cambiare

- **La regola del «libero» per cella** (`f12-integrazione/03-libero/LIBERO_DELLA_CELLA.md`: «metà impronta con una cella di guardia»; K-107): la Prop. 1 è scritta sulla proprietà strutturale (solo fotogramma corrente, solo pixel validi) e resta vera; cambiano la definizione operativa di $O(t)$ e le cifre di resa. Se l'integrazione reintroduce una memoria condizionata (I3 di `DECISIONE.md`), la Prop. 1 (a) va riscritta.
- **Fasce:** $w=0{,}40$ m e $w_p=0{,}20$ m, la regola d'ingresso e la porta sul riaggancio (`f12-integrazione/06-identita`): se cambiano, cambiano la tabella della Prop. 8 e il punto (c) della Prop. 4.
- **Invarianti rinumerati** in `f12-integrazione/01-soluzione/SOLUZIONE_V3.md` §2 (letti solo per titoli): controllare che la Prop. 4 (d) corrisponda all'invariante di continuità finale e che «perso» non ricompaia.
- La latenza (0,150 / 0,155 / 0,222 s nei diversi file) non è unica: la Prop. 8 e l'Oss. 3 vanno allineate al valore che l'allegato dichiara.

## II.5 Che cosa manca per completare l'area

1. Una prova **in due dimensioni** e con corpo esteso della minimalità di Π (qui: dimostrazione per oggetti puntiformi, esaustivo solo in 1D).
2. Il riconteggio dal grezzo di: 9 e 87 su 2 800 (li ho solo in `MODIFICHE_CONTINUITA.md` e `f8-continuita/12-torneo/TORNEO.md` §2), 193 su 193, le «368 corse».
3. Una misura di $\varepsilon_\Omega$ e di $a$ sul sensore: senza, la Prop. 8 è un enunciato condizionale.
4. Nessuna prova formale per: occlusore mobile, sensore in moto, due soggetti per ombra (solo controesempi).
5. La Prop. 1 (b) non è mai stata esercitata su una profondità vera: nell'allegato resta «non verificato sperimentalmente».
