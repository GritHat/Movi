# Fascicolo: rilevamento, associazione e stima dello stato

<!-- PARTE I: entra nell'allegato. PARTE II: per chi compone, non entra nell'allegato. -->

# PARTE I — Contenuto per l'allegato

**Simboli aggiunti alla notazione comune.** $n_{\min}$: punti minimi perché una cella sia «occupata»; $\mathbf{c}_k$: centro di un gruppo al fotogramma $k$; $\sigma_t(d)$, $\sigma_c$: rumore trasversale e rumore del centro; $\kappa$: correlazione fra gli errori di due punti; $m$: fotogrammi mediati; $k_s$: soglia in scarti tipo; $\delta$, $w$: spostamento vero e finestra; $\sigma_\delta$: scarto tipo della differenza di due medie; $P_{fa}$, $P_d$: falso allarme e rilevamento della regola «mobile»; $p_d$: probabilità di rilevare il gruppo in un fotogramma; $\sigma_p(\tau_{occ})$: scarto tipo per asse della posizione prevista; $r_\alpha$: raggio del cerchio al livello $\alpha$; $\sigma_a$: scarto tipo dell'accelerazione stimata; $\mathcal{M}$: matrice di osservabilità; $\beta$, $n_c$, $p$: falsi per cella e per ciclo, celle della porta, probabilità di un falso in porta; $q_{\mathrm{eff}}$: densità che riproduce l'errore mediano; $\Phi$ e $Q(\cdot) = 1 - \Phi(\cdot)$ con argomento scalare: ripartizione e coda della normale standard.

**Livello di prova.** Tutti i risultati vengono da dimostrazioni, calcoli, simulazioni o elaborazioni di dati pubblici; nessuno da un sensore fisico. I livelli sono: *dimostrato* (nel modello dichiarato), *verificato per calcolo*, *verificato in simulazione* (con $N$ e intervallo di Wilson al 95 %), *misurato su dati pubblici*, *non verificato sperimentalmente*.

## 1. Dalla mappa ai gruppi

**Definizione 1 (cella occupata).** Una cella $(\varphi, \rho)$ della mappa polare ($1^\circ \times 0{,}1$ m, $\rho \le 3$ m) è «occupata osservata» se contiene almeno $n_{\min}$ punti di profondità con quota $y \in [0{,}07;\, 2]$ m ed è il primo ritorno lungo il suo azimut. Il valore di riferimento è $n_{\min} = 3$.

**Definizione 2 (gruppo).** Un gruppo è una componente connessa di celle occupate, con vicinanza a otto celle negli indici $(\varphi, \rho)$. Il suo centro $\mathbf{c}$ è la media delle coordinate $(x, z)$ dei suoi punti; la larghezza è la corda sottesa dalla sua estensione in azimut alla distanza del centro. Un gruppo è «tagliato» quando confina con celle in ombra di un gruppo più vicino alla camera: il centro della parte visibile non è il centro dell'oggetto, quindi un gruppo tagliato non aggiorna il filtro e non entra nella regola «mobile».

**Rumore del centro in funzione della distanza.** Per una camera stereo la profondità è $d = f b / \text{disparità}$, quindi un errore di disparità $\sigma_d$ dà

$$\sigma_z(d) = \frac{d^2}{f\,b}\,\sigma_d .$$

Con $\sigma_d = 0{,}08$ px e crescita quadratica con la distanza \cite{realsense-bkm-taratura}, e con i valori assunti $f = 424$ px e $b = 0{,}05$ m, si ottiene $\sigma_z = 1{,}51 / 3{,}40 / 6{,}04$ cm a $2 / 3 / 4$ m (curva *nominale*). Come analisi di sensibilità si usano due curve più severe, anch'esse quadratiche: $4\,(d/2)^2$ cm (*pessimista*: $4 / 9 / 16$ cm) e $5\,(d/2)^2$ cm (*severa*: $5 / 11{,}25 / 20$ cm). In direzione trasversale il centro è quantizzato sulla cella di $1^\circ$; un errore uniforme sulla cella dà $\sigma_t(d) = d\,(\pi/180)/\sqrt{12}$, cioè $1{,}01 / 1{,}51 / 2{,}02$ cm. La covarianza di misura è

$$R(d) = \sigma_z^2(d)\,\mathbf{u}_r\mathbf{u}_r^{\top} + \sigma_t^2(d)\,\mathbf{u}_t\mathbf{u}_t^{\top},$$

con $\mathbf{u}_r$ versore dalla camera al centro e $\mathbf{u}_t$ il suo ortogonale sul suolo.

**Lemma 1 (rumore del centro e numero di punti).** Se gli $n$ punti di un gruppo hanno errori di varianza $\sigma^2$ e correlazione a coppie $\kappa \in [0, 1]$, la varianza della loro media è $\sigma_c^2 = \sigma^2\,[(1-\kappa)/n + \kappa]$.

*Dimostrazione.* $\mathrm{Var}\big(\tfrac1n\sum_i e_i\big) = \tfrac{1}{n^2}\,[\,n\sigma^2 + n(n-1)\kappa\sigma^2\,]$. $\square$

Quindi $\sigma/\sqrt{n} \le \sigma_c \le \sigma$. Una sagoma di $0{,}4 \times 1{,}7$ m a 2 m, a 424 pixel di larghezza ($f \approx 223$ px), occupa circa $8{,}5 \cdot 10^3$ pixel: con errori indipendenti il centro avrebbe $0{,}016$ cm. Il progetto adotta l'estremo prudente $\sigma_c = \sigma_z(d)$ ($\kappa = 1$). Il valore reale di $\sigma_c$ è **non verificato sperimentalmente**: in profondità simulata con un modello realistico del sensore, per una persona ferma (sagoma rigida, 20 semi), il rumore radiale mediano è $0{,}36 / 0{,}99 / 1{,}25$ cm a $2 / 3 / 4$ m (massimi $7{,}0 / 5{,}6 / 10{,}4$); l'unico dato da una sequenza pubblica reale (altro sensore della stessa famiglia, una persona che cammina, 288 fotogrammi, senza verità di riferimento) è $5{,}8$–$6{,}8$ cm sotto 3 m. I due valori stanno ai lati opposti della curva nominale.

## 2. La regola «mobile»

**Definizione 3.** Sia $\bar{\mathbf{c}}_k = (\mathbf{c}_k + \mathbf{c}_{k-1} + \mathbf{c}_{k-2})/3$ la media di $m = 3$ centri consecutivi non tagliati. Al fotogramma $k$ si confronta $\bar{\mathbf{c}}_k$ con la media più vecchia disponibile $\bar{\mathbf{c}}_j$, con $k - j \le 1/\Delta$ (finestra che cresce fino a 1 s) e $k - j \ge m$ (medie disgiunte). Il gruppo è «mobile» se, lungo l'asse radiale o lungo quello trasversale,

$$|\bar c_k - \bar c_j| > k_s\,\sigma\,\sqrt{2/m}, \qquad k_s = 5,$$

con $\sigma = \sigma_z(d)$ o $\sigma_t(d)$ alla maggiore delle distanze ai due capi. Scritta sullo scarto tipo $\sigma/\sqrt{m}$ della media di tre fotogrammi, la soglia è $5\,(\sigma/\sqrt m)\,\sqrt2$.

**Proposizione 1 (soglia e falso allarme).** Per un oggetto fermo con errori gaussiani indipendenti fra i fotogrammi, di scarto tipo $\sigma$ lungo un asse, la differenza di due medie disgiunte di $m$ fotogrammi è $\mathcal{N}(0, \sigma_\delta^2)$ con $\sigma_\delta = \sigma\sqrt{2/m}$. La soglia vale $k_s\sigma_\delta$ e la probabilità di falso allarme per prova e per asse è $P_{fa} = 2\,Q(k_s)$.

*Dimostrazione.* Ogni media ha varianza $\sigma^2/m$; le due medie sono indipendenti perché disgiunte; la differenza ha varianza $2\sigma^2/m$ e media nulla. $\square$

Con $m = 3$: $\sigma_\delta = 0{,}8165\,\sigma$, soglia $4{,}08\,\sigma$, $P_{fa} = 2Q(5) = 5{,}7 \cdot 10^{-7}$. Nel primo secondo di una traccia a 15 Hz le prove sono al più 13 per asse: per la disuguaglianza dell'unione la probabilità di almeno un'etichetta falsa è $\le 2 \cdot 13 \cdot 5{,}7 \cdot 10^{-7} = 1{,}5 \cdot 10^{-5}$. A 2 m con la curva nominale la soglia vale $6{,}2$ cm in radiale e $4{,}1$ cm in trasversale.

**Proposizione 2 (rilevamento).** Per un oggetto con componente di velocità $v$ lungo un asse, nella finestra $w = (k-j)\Delta$ lo spostamento è $\delta = v\,w$ e, con rumore uguale ai due capi,

$$P_d = \Phi\!\left(\frac{\delta}{\sigma_\delta} - k_s\right) + \Phi\!\left(-\frac{\delta}{\sigma_\delta} - k_s\right).$$

La velocità rilevata con probabilità $0{,}5$ nella prova singola è $v_{0,5} = k_s\,\sigma\sqrt{2/m}\,/\,w$; con probabilità $0{,}9$ è $v_{0,9} = (k_s + 1{,}2816)\,\sigma\sqrt{2/m}\,/\,w$.

*Dimostrazione.* La differenza delle medie è $\mathcal{N}(\delta, \sigma_\delta^2)$; $P_d$ è la massa oltre $\pm k_s\sigma_\delta$. Il secondo termine è trascurabile; $P_d = 0{,}5$ quando $\delta = k_s\sigma_\delta$, e $P_d = 0{,}9$ quando $\delta/\sigma_\delta - k_s = 1{,}2816$. $\square$

A 15 Hz la finestra massima con medie disgiunte entro il primo secondo è $w = 13\Delta = 0{,}867$ s. In radiale, $v_{0,5}$ / $v_{0,9}$ valgono $0{,}071 / 0{,}089$ m/s a 2 m e $0{,}160 / 0{,}201$ a 3 m con la curva nominale, $0{,}188 / 0{,}237$ e $0{,}424 / 0{,}533$ con la pessimista, $0{,}236 / 0{,}296$ e $0{,}530 / 0{,}666$ con la severa; in trasversale $0{,}047 / 0{,}060$ a 2 m e $0{,}071 / 0{,}089$ a 3 m (*verificato per calcolo*). Un pedone a $0{,}5$ m/s in avvicinamento da 3 m sta quindi sopra la soglia con la curva nominale, vicino con la pessimista, sotto con la severa: la simulazione della regola completa lo conferma.

**Tabella 1.** Regola «mobile», oggetto a $0{,}5$ m/s: quota di tracce etichettate entro 1 s (*verificato in simulazione*: centro puntiforme, rumore gaussiano indipendente e noto, 15 Hz).

| Caso | Simulazione d'origine, $N = 2000$ | Ricalcolo indipendente, $N = 20\,000$ | Prova singola (Prop. 2) |
|---|---|---|---|
| da 2 m, di traverso o in avvicinamento, tre curve | 100 % in sei casi su sei ($\ge 99{,}81$ %) | 100 % ($\ge 99{,}98$ %) | 1,000 |
| da 3 m in avvicinamento, nominale | 100 % | 100 % | 1,000 |
| da 3 m in avvicinamento, pessimista | 85,9 % (84,3–87,3) | 86,2 % (85,7–86,7) | 0,853 |
| da 3 m in avvicinamento, severa | 26,6 % (24,7–28,6) | 26,9 % (26,3–27,5) | 0,371 |
| oggetto fermo: tracce con un'etichetta falsa nel primo secondo | 0 su 4000 in ciascuno dei sei casi ($\le 0{,}10$ %) | 1 su 120 000 | $\le 1{,}5 \cdot 10^{-5}$ |

Con la curva severa la prova singola sovrastima, perché la regola usa la maggiore delle distanze *misurate*, che il rumore gonfia.

**Condizioni di validità.** (i) Rumore noto: se quello creduto è la metà del vero la soglia scende a $2{,}5\,\sigma_\delta$, il falso allarme per prova sale a $1{,}2$ % e, in simulazione, il $10{,}9$ % delle tracce ferme riceve un'etichetta falsa nel primo secondo ($N = 20\,000$, curva pessimista, 2 m). (ii) Errori indipendenti fra i fotogrammi, senza valori aberranti. (iii) Il centro cambia solo per il rumore di misura, non perché cambia l'insieme delle celle del gruppo.

**Controesempio fuori dalle ipotesi (profondità simulata realistica).** Con immagini di profondità sintetiche che includono i *pixel misti* ai bordi delle sagome (profondità intermedie fra l'oggetto vicino e lo sfondo), un pannello fermo dietro cui passa una persona è etichettato «mobile» in 79 passaggi su 90 (Wilson 79,4–93,0 %). Cade la condizione (iii): quando le due sagome si toccano, i pixel misti riempiono celle «ponte» e i due gruppi diventano uno (90 passaggi su 90; in un caso esaminato, 100 celle e $1{,}42$ m di larghezza). Il centro del gruppo fuso si sposta di decine di centimetri, contro una soglia di $4$–$6$ cm: la prova legge come moto un cambio di segmentazione. Controlli: senza pixel misti la fusione passa da 10 casi su 10 a 1 su 10; con $n_{\min} = 40$ le etichette false scendono a 5 passaggi su 90 (2,4–12,4 %), ma una scatola alta 15 cm a 2 m è vista in 3 prove su 10 anziché 10 su 10. L'entità dei pixel misti è un'ipotesi del modello: l'effetto è **non verificato sperimentalmente**, in nessuno dei due versi.

## 3. Modello del moto e filtro

**Modello.** Lo stato è $\mathbf{x} = [p_x, p_z, v_x, v_z]^{\top}$. Per asse, $\dot p = v$, $\dot v = a(t)$, con $a$ rumore bianco di densità $q$ (m²/s³), indipendente fra gli assi. Campionando a passo $\Delta$:

$$F = \begin{bmatrix} I_2 & \Delta I_2 \\ 0 & I_2 \end{bmatrix}, \quad Q = q \begin{bmatrix} \tfrac{\Delta^3}{3} I_2 & \tfrac{\Delta^2}{2} I_2 \\ \tfrac{\Delta^2}{2} I_2 & \Delta I_2 \end{bmatrix}, \quad H = \begin{bmatrix} I_2 & 0 \end{bmatrix}, \quad R = R(d).$$

**Proposizione 3 (forma chiusa di $Q$).** Per asse, con $A = \begin{bmatrix} 0 & 1 \\ 0 & 0\end{bmatrix}$ e $G = [0, 1]^{\top}$, vale $Q(\Delta) = \int_0^{\Delta} e^{As} G\, q\, G^{\top} e^{A^{\top}s}\,ds = q \begin{bmatrix} \Delta^3/3 & \Delta^2/2 \\ \Delta^2/2 & \Delta \end{bmatrix}$, e $Q(\Delta_1 + \Delta_2) = F(\Delta_2)\,Q(\Delta_1)\,F(\Delta_2)^{\top} + Q(\Delta_2)$.

*Dimostrazione.* $A^2 = 0$, quindi $e^{As} = I + As$ e $e^{As}G = [s, 1]^{\top}$. L'integrando è $q \begin{bmatrix} s^2 & s \\ s & 1 \end{bmatrix}$; integrando termine a termine su $[0, \Delta]$ si ha la tesi. La seconda identità si verifica sostituendo: per l'elemento di posizione, $\Delta_1^3/3 + \Delta_1^2\Delta_2 + \Delta_1\Delta_2^2 + \Delta_2^3/3 = (\Delta_1 + \Delta_2)^3/3$, e analogamente per gli altri. $\square$

La seconda identità dice che la previsione su un tempo $\tau_{occ}$ non dipende dal numero di passi in cui è spezzata. Le due identità sono verificate anche numericamente.

**Equazioni e ordine degli aggiornamenti.** Predizione: $\hat{\mathbf{x}}^- = F\hat{\mathbf{x}}$, $P^- = FPF^{\top} + Q$. Innovazione: $\nu = \mathbf{z} - H\hat{\mathbf{x}}^-$, $S = HP^-H^{\top} + R$. Correzione: $K = P^-H^{\top}S^{-1}$, $\hat{\mathbf{x}} = \hat{\mathbf{x}}^- + K\nu$, $P = (I - KH)P^-(I - KH)^{\top} + KRK^{\top}$ (forma di Joseph, che conserva simmetria e positività). La correzione usa solo gruppi non tagliati che cadono nella porta (§5).

**Proposizione 4 (crescita senza misure).** Se all'ultima correzione la covarianza per asse è $\begin{bmatrix} P_{pp} & P_{pv} \\ P_{pv} & P_{vv} \end{bmatrix}$, dopo un tempo $\tau_{occ}$ senza misure

$$\sigma_p^2(\tau_{occ}) = P_{pp} + 2\,\tau_{occ}\,P_{pv} + \tau_{occ}^2\,P_{vv} + \frac{q\,\tau_{occ}^3}{3}.$$

*Dimostrazione.* Per la Proposizione 3, $P(\tau_{occ}) = F(\tau_{occ})\,P\,F(\tau_{occ})^{\top} + Q(\tau_{occ})$; l'elemento di posizione è la tesi. $\square$

Con covarianza isotropa la regione al livello $\alpha$ è un cerchio centrato in $\hat{\mathbf{p}}$ di raggio $r_\alpha = \sigma_p\sqrt{-2\ln(1-\alpha)}$, perché $\chi^2_2$ ha funzione di ripartizione $1 - e^{-x/2}$: $r_{0,50} = 1{,}177\,\sigma_p$, $r_{0,90} = 2{,}146\,\sigma_p$, $r_{0,95} = 2{,}448\,\sigma_p$.

**Tabella 2.** $\sigma_p(\tau_{occ})$ per asse, in metri (*verificato per calcolo*). «Solo processo» è $\sqrt{q\tau_{occ}^3/3}$; «a regime» parte dalla covarianza stazionaria del filtro a 15 Hz con rumore di misura di 5 cm per asse (per $q = 0{,}2$: $\sqrt{P_{pp}} = 3{,}3$ cm, $\sqrt{P_{vv}} = 0{,}205$ m/s).

| $q$ (m²/s³) | | 0,5 s | 1 s | 2 s | 3 s |
|---|---|---|---|---|---|
| 0,2 | solo processo | 0,091 | 0,258 | 0,730 | 1,342 |
| | a regime | 0,156 | 0,344 | 0,848 | 1,485 |
| | $r_{0,95}$ a regime | 0,38 | 0,84 | 2,08 | 3,64 |
| 0,1 | solo processo | 0,065 | 0,183 | 0,516 | 0,949 |
| | a regime | 0,121 | 0,257 | 0,618 | 1,072 |
| 0,05 | solo processo | 0,046 | 0,129 | 0,365 | 0,671 |
| | a regime | 0,096 | 0,194 | 0,453 | 0,777 |

Con $q = 0{,}2$ il raggio al 95 % supera 1 m dopo $1{,}15$ s, $1{,}5$ m dopo $1{,}57$ s e 2 m dopo $1{,}95$ s: oltre un paio di secondi la regione prevista copre gran parte di un'ombra larga uno o due metri e smette di localizzare. Che senza misure l'errore di un filtro di Kalman si accumuli è il punto di partenza anche dei metodi di inseguimento recenti \cite{cao2023}.

## 4. Perché l'accelerazione non si stima

**Lemma 2 (differenza seconda).** Con errori di posizione indipendenti di scarto tipo $\sigma_p$, la stima $\hat a_k = (p_{k+1} - 2p_k + p_{k-1})/\Delta^2$ ha scarto tipo $\sigma_a = \sqrt6\,\sigma_p/\Delta^2$.

*Dimostrazione.* $\mathrm{Var}(\hat a_k) = (1 + 4 + 1)\,\sigma_p^2/\Delta^4$. $\square$

Con $\sigma_p = 3$ cm (valore assunto: è la curva nominale a circa $2{,}8$ m) si ha $\sigma_a = 66{,}1$ m/s² a 30 Hz, $16{,}5$ a 15 Hz e $7{,}3$ a 10 Hz, contro un'accelerazione efficace di $0{,}67$ m/s² nel modello di pedone usato in simulazione: da uno a due ordini di grandezza sopra il segnale.

**Osservazione 1 (il limite non è algebrico).** Lo stato $[p, v, a]$ con misura della sola posizione ha matrice di osservabilità di rango 3 su 3: il limite è di precisione. Il limite dei minimi quadrati per un polinomio di secondo grado ($\sigma_p = 3$ cm, 30 Hz) dà $\sigma_a = 5{,}9 / 0{,}71 / 0{,}14$ m/s² su finestre di $0{,}2 / 0{,}5 / 1$ s: per scendere sotto 1 m/s² serve circa mezzo secondo di accelerazione *costante*, ipotesi non sostenibile per un pedone che manovra; e stimarla moltiplica per circa $3{,}8$ l'incertezza sulla velocità. *Verificato per calcolo.*

*Verificato in simulazione* (un solo modello di pedone che manovra, 15 Hz, rumore assunto di 5 cm, 1500 prove per caso): un filtro ad accelerazione costante sbaglia l'accelerazione di $0{,}82$ m/s² contro $0{,}67$ m/s² di valore efficace vero (peggio che supporla nulla) e, dopo 2 s senza misure, sbaglia la posizione di $2{,}29$ m contro $1{,}18$ m del modello a velocità quasi costante, con raggio al 95 % di $5{,}08$ contro $2{,}08$ m. Per questo lo stato del filtro si ferma a posizione e velocità.

**Proposizione 5 (osservabilità in tre dimensioni senza quota).** Per lo stato $[p_x, p_y, p_z, v_x, v_y, v_z]^{\top}$ a velocità costante, con misura di $(p_x, p_z)$ soltanto, la matrice di osservabilità $\mathcal{M} = [H^{\top}, (HF)^{\top}, \dots, (HF^5)^{\top}]^{\top}$ ha rango 4; il sottospazio non osservabile è generato da $p_y$ e $v_y$. Con la quota misurata il rango è 6.

*Dimostrazione.* $HF^i$ ha per righe $[\mathbf{e}_x^{\top},\, i\Delta\,\mathbf{e}_x^{\top}]$ e $[\mathbf{e}_z^{\top},\, i\Delta\,\mathbf{e}_z^{\top}]$. Le righe con $i = 0, 1$ generano $(\mathbf{e}_x, 0)$, $(\mathbf{e}_z, 0)$, $(0, \mathbf{e}_x)$, $(0, \mathbf{e}_z)$: quattro vettori indipendenti; le altre righe ne sono combinazioni. Le colonne di $p_y$ e $v_y$ sono nulle in ogni riga. Aggiungendo la riga di $p_y$ a $H$ si ottengono allo stesso modo sei vettori indipendenti. $\square$

*Verificato anche per calcolo numerico del rango* (4 su 6; 6 su 6; 4 su 4 per lo stato a quattro componenti). Conseguenza di progetto: quando il gruppo è tagliato dal campo verticale la quota del centro non è misurata, e quota e velocità verticale non compaiono in uscita.

## 5. Associazione, porta di validazione e conferma

**Porta.** Una misura $\mathbf{z}$ è candidata per una traccia se $\nu^{\top} S^{-1} \nu \le \gamma$. Se l'innovazione è gaussiana di covarianza $S$, la forma quadratica è $\chi^2_2$, con ripartizione $1 - e^{-x/2}$; la probabilità che la misura vera cada in porta è $P_G$ per $\gamma = -2\ln(1 - P_G)$. Con $P_G = 0{,}99$: $\gamma = 9{,}210$ (*dimostrato; verificato per calcolo*). L'area della porta, $\pi\gamma\sqrt{\det S}$, cresce con $\sigma_p^2$: senza misure si allarga, ed è ciò che rende possibili gli scambi d'identità (§8).

**Assegnamento.** Fra tracce e gruppi non tagliati si costruisce la matrice dei costi $c_{ij} = \nu_{ij}^{\top} S_i^{-1} \nu_{ij}$ se in porta, vietato altrimenti, e si sceglie l'assegnamento di costo totale minimo (algoritmo ungherese), prima per le tracce confermate e poi, sui gruppi rimasti, per quelle in attesa di conferma. Lo schema «rilevamento, filtro di Kalman, assegnamento ottimo» è quello degli inseguitori in linea più diffusi \cite{bewley2016}.

**Conferma.** Una traccia è confermata con 3 rilevamenti in 5 cicli consecutivi.

**Proposizione 6 (probabilità e ritardo di conferma).** Con rilevamenti indipendenti di probabilità $p_d$ per fotogramma, un oggetto visibile per $n \le 5$ fotogrammi è confermato con probabilità $\Pr[\mathrm{Bin}(n, p_d) \ge 3]$. Dal primo rilevamento, la conferma arriva al ciclo $+j$ ($j = 2, 3, 4$) con probabilità $(j-1)\,p_d^2\,(1-p_d)^{j-2}$.

*Dimostrazione.* La prima parte è la definizione. Per la seconda: al ciclo $+j$ deve cadere il terzo rilevamento, e fra i $j - 1$ cicli precedenti (dopo il primo rilevamento) ne deve cadere esattamente uno. $\square$

Con $p_d = 0{,}9$: non confermato il $27{,}1$ % degli oggetti visti per 3 fotogrammi, il $5{,}2$ % con 4, lo $0{,}9$ % con 5; le proprietà enunciate per le tracce confermate valgono quindi per chi è stato visto almeno 4 fotogrammi ($0{,}27$ s a 15 Hz). Ritardo dal primo rilevamento: $+2$ cicli ($0{,}133$ s) con probabilità $0{,}81$, $+3$ ($0{,}200$ s) con $0{,}162$, $+4$ ($0{,}267$ s) con $0{,}024$; in totale $0{,}9963$, media $0{,}147$ s. *Verificato per calcolo.*

**Proposizione 7 (traccia falsa).** Un falso rilevamento apra una traccia in attesa; se in ciascuno dei 4 cicli seguenti un falso cade nella sua porta con probabilità $p$, indipendentemente, la traccia falsa è confermata con probabilità $1 - (1-p)^4 - 4p(1-p)^3 = 6p^2 - 8p^3 + 3p^4$. Con frequenza di falsi $\beta$ per cella e per ciclo e una porta di $n_c$ celle, $p = 1 - (1-\beta)^{n_c}$.

*Dimostrazione.* Servono almeno 2 successi su 4 prove di Bernoulli; si sottraggono i casi con 0 e con 1 successo. $\square$

Per $p = 0{,}001 / 0{,}01 / 0{,}05 / 0{,}1$ la probabilità è $6{,}0 \cdot 10^{-6} / 5{,}9 \cdot 10^{-4} / 1{,}4 \cdot 10^{-2} / 5{,}2 \cdot 10^{-2}$; $\beta = 10^{-3}$ e $n_c = 30$ danno $p = 0{,}030$ e $5{,}0 \cdot 10^{-3}$. **Condizione di validità:** falsi indipendenti da un ciclo all'altro. Un falso sistematico (un ritorno spurio che persiste nella stessa cella) ha $p \to 1$ e supera la conferma: nella profondità simulata realistica i ritorni spuri sul pavimento a grande incidenza hanno prodotto da 7 a 66 tracce false per passaggio. Il valore di $\beta$ di un sensore reale è **non verificato sperimentalmente**.

## 6. Il valore di $q$

**Scelta iniziale** (*verificato in simulazione*, un solo modello di pedone: salti di velocità a istanti casuali con rilassamento, 15 Hz, rumore assunto 5 cm). $q = 0{,}2$ m²/s³ è il valore per cui la media della statistica d'innovazione è $1{,}95$ contro il valore atteso 2 (§9). Dopo un tratto senza misure, il cerchio al 95 % contiene la posizione vera nello $0{,}936 / 0{,}917 / 0{,}903 / 0{,}920$ dei casi a $0{,}5 / 1 / 2 / 3$ s (1500 prove per caso); con $q = 0{,}01$ la copertura a 2 s scende a $0{,}42$, con $q = 0{,}8$ sale a $0{,}997$ ma il raggio a 2 s passa da $2{,}08$ a $3{,}96$ m.

**Taratura su pedoni veri** (*misurato su dati pubblici*). Si usano le traiettorie dell'insieme pubblico THÖR (persone al chiuso, posizioni da cattura del moto): ricampionate a 15 Hz, con rumore gaussiano aggiunto di 2 cm, 1 s di filtro con misure e poi 3 s di sola previsione. Una registrazione dà 227 tratti di 9 persone (taratura), un'altra 219 tratti di 9 persone (prova). L'occlusione è artificiale: questi dati misurano solo il modello del moto, non il rilevamento, l'ombra o l'identità.

**Tabella 3.** Registrazione di prova, $N = 219$ tratti, 9 persone. Copertura della regione al 90 %, con il numero di tratti e l'intervallo di Wilson (che tratta i tratti come indipendenti).

| $q$ | a 1 s | a 2 s | a 3 s | $r_{0,95}$ a 1 / 2 / 3 s (m) | Errore mediano (m) |
|---|---|---|---|---|---|
| 0,2 | 0,977 (214; 0,948–0,990) | 1,000 (219; 0,983–1) | 1,000 (219; 0,983–1) | 0,75 / 1,96 / 3,49 | 0,21 / 0,49 / 0,81 |
| 0,1 | 0,945 (207; 0,907–0,968) | 0,945 | 0,945 | 0,55 / 1,41 / 2,50 | — |
| 0,05 | 0,795 (174; 0,736–0,843) | 0,804 (176; 0,746–0,851) | 0,831 (182; 0,776–0,875) | 0,41 / 1,02 / 1,80 | 0,19 / 0,44 / 0,72 |

«Fermo all'ultima posizione» ha errore mediano $0{,}91 / 1{,}79 / 2{,}62$ m. Una seconda elaborazione indipendente (altro codice, altra estrazione del rumore) dà $0{,}982 / 0{,}995 / 1{,}000$ per $q = 0{,}2$, $0{,}922 / 0{,}950 / 0{,}941$ per $0{,}1$ e $0{,}836 / 0{,}822 / 0{,}840$ per $0{,}05$; al variare del seme la copertura a 1 s con $q = 0{,}05$ sta fra $0{,}790$ e $0{,}836$. I tratti di una stessa persona non sono indipendenti: per persona la copertura con $q = 0{,}05$ va da $0{,}43$ a $1{,}00$, e l'intervallo ottenuto ricampionando le persone è $1{,}27$ volte quello sui tratti. La stessa regola di scelta sceglie $q = 0{,}05$ su una registrazione e $0{,}1$ sull'altra.

**Proposizione 8 (copertura attesa se il modello fosse esatto).** Se il moto vero seguisse il modello del §3 con lo stesso $q$ del filtro, l'errore di previsione sarebbe gaussiano di covarianza $P(\tau_{occ})$ e la regione al livello $\alpha$ conterrebbe la posizione vera con probabilità esattamente $\alpha$, a ogni $\tau_{occ}$. Su $N$ tratti indipendenti il numero dei contenuti sarebbe $\mathrm{Bin}(N, \alpha)$.

*Dimostrazione.* Con modello, rumori e condizione iniziale esatti e gaussiani, $P$ è la covarianza dell'errore del filtro di Kalman, che è gaussiano a media nulla; $\mathbf{e}^{\top}P^{-1}\mathbf{e} \sim \chi^2_2$ e la regione è l'insieme $\{\chi^2_2 \le -2\ln(1-\alpha)\}$. $\square$

*Controlli.* Simulando il moto con il modello stesso e lo stesso protocollo ($N = 20\,000$), la copertura al 90 % è $0{,}898 / 0{,}903 / 0{,}901$ a $1 / 2 / 3$ s e quella al 50 % è $0{,}502 / 0{,}501 / 0{,}502$; i raggi della Tabella 3 sono riprodotti al centimetro. Con $N = 219$ e $\alpha = 0{,}90$ si attendono $197{,}1 \pm 4{,}4$ tratti, intervallo centrale al 95 % da 188 a 205 ($0{,}858$–$0{,}936$). Con $q = 0{,}2$ se ne osservano 214: averne almeno tanti ha probabilità $8 \cdot 10^{-6}$ sotto il modello esatto, quindi **$q = 0{,}2$ copre troppo**, nel verso prudente. Con $q = 0{,}05$ se ne osservano 174: averne così pochi ha probabilità $2{,}5 \cdot 10^{-6}$, quindi copre troppo poco. I 207 con $q = 0{,}1$ stanno appena sopra l'intervallo (probabilità $0{,}012$). Il valore calibrato sta quindi **fra 0,05 e 0,1 m²/s³**. Lo conferma l'errore mediano: sotto il modello la mediana dell'errore è $1{,}177\,\sigma_p$, cioè $0{,}36 / 0{,}94 / 1{,}68$ m con $q = 0{,}2$, contro $0{,}21 / 0{,}49 / 0{,}81$ m osservati; la densità che riproduce le mediane osservate è $q_{\mathrm{eff}} = 0{,}058 / 0{,}050 / 0{,}044$.

**Lettura.** $q = 0{,}2$ è una scelta prudente, non una taratura: su pedoni veri in cammino la regione contiene quasi sempre il soggetto, ma a 3 s ha un raggio di $3{,}5$ m e informa poco. Che il punto previsto a velocità costante sia una base difficile da battere è noto: su traiettorie di pedoni riprese dall'alto, a $4{,}8$ s ha errore medio e finale di $0{,}39 / 0{,}83$ m contro $0{,}44 / 0{,}91$ m del miglior modello appreso deterministico considerato \cite{scholler2020}; quel confronto riguarda il punto, non la regione, e non comprende occlusioni.

## 7. Il cerchio di covarianza non è una dichiarazione di precisione durante un'occlusione

**Che cosa si osserva** (*verificato in simulazione*: soggetto puntiforme, 15 Hz, rumore di 5 cm, comportamenti generati da più simulatori scritti indipendentemente; $q = 0{,}2$).

- In media, al livello nominale 90 %, il cerchio contiene il soggetto nello $0{,}88$–$0{,}96$ dei casi fino a 5 s ($N = 6000$).
- Al livello nominale 50 % contiene lo $0{,}63$–$0{,}85$: per esempio $0{,}78 / 0{,}83 / 0{,}76 / 0{,}70 / 0{,}63$ a $0{,}5 / 1 / 2 / 3 / 5$ s ($N = 6000$) e $0{,}80 / 0{,}79 / 0{,}80 / 0{,}85$ a $1 / 2 / 3 / 5$ s in un secondo simulatore (1500 passaggi per comportamento).
- Per comportamento, al 90 %: chi prosegue $1{,}00$; chi si ferma $0{,}86$–$1{,}00$; chi svolta $0{,}72$–$0{,}90$; chi torna indietro, a 2 s, da $0{,}29$ a $0{,}77$ secondo il simulatore ($0{,}54$ in quello con 1500 passaggi).
- Il rapporto fra i quantili 90 % e 50 % dell'errore va da $1{,}8$ a $4{,}5$ secondo il simulatore e l'orizzonte; per una gaussiana è $\sqrt{\ln 10/\ln 2} = 1{,}82$.
- Se la regione viene mostrata solo finché copre meno di metà dell'ombra, a 2 s senza osservazione essa contiene chi prosegue nello $0{,}00$–$0{,}06$ dei passaggi (tre disposizioni, 400 passaggi ciascuna), perché a quel punto non viene più emessa: la regione esiste nel 19–38 % dei cicli senza osservazione.

**Spiegazione con il modello.** Il filtro assume un'accelerazione bianca: l'errore cresce con continuità, è gaussiano e ha una sola scala, $\sqrt{q\tau_{occ}^3/3}$. Il moto vero durante un'occlusione è una **miscela di comportamenti**: la gran parte prosegue, e allora l'errore è quasi solo quello di stima iniziale, molto più piccolo di $r_\alpha$; alcuni si fermano o tornano indietro, e allora l'errore è grande, sta lungo la traiettoria e dietro il punto previsto.

**Osservazione 2 (conto illustrativo).** Sia $v = 1{,}2$ m/s e la manovra istantanea, a un istante uniforme in $[0, \tau_{occ}]$. L'errore vale $v(\tau_{occ} - t_s)$ per chi si ferma in $t_s$ e $2v(\tau_{occ} - t_r)$ per chi inverte in $t_r$; un cerchio di raggio $r$ li contiene con probabilità $\min(1, r/(v\tau_{occ}))$ e $\min(1, r/(2v\tau_{occ}))$. Con i raggi a regime della Tabella 2 a 2 s ($r_{0,90} = 1{,}82$ m, $r_{0,50} = 1{,}00$ m): chi prosegue $1{,}00$; chi si ferma $0{,}76$ e $0{,}42$; chi torna $0{,}38$ e $0{,}21$. Con una miscela 70 / 18 / 12 la copertura complessiva è $0{,}88$ al «90 %» e $0{,}80$ al «50 %».

Il conto riproduce l'andamento osservato: il valore quasi giusto al 90 % in media nasce da **due errori di segno opposto** ($1{,}00$ dove basterebbe $0{,}90$, e meno di metà per chi torna); al 50 % la regione contiene circa l'80 %. Nessun valore di $q$ lo corregge, perché una gaussiana ha un solo parametro di scala e il rapporto fra i suoi quantili è fisso: alzare $q$ fino a coprire chi torna allarga la regione per tutti (un disco che copra al 90 % ogni comportamento ha da $3{,}5$ a $4{,}8$ volte l'area del cerchio a 2 s, in simulazione), e la copertura media dipende dalla composizione della popolazione (da $0{,}996$ per chi cammina sempre dritto a $0{,}785$ con sole manovre, a 2 s).

**Conseguenze.** (i) Il cerchio del filtro serve come porta di associazione e come centro della previsione, non come precisione dichiarata. (ii) Un livello dichiarato va misurato per fascia di $\tau_{occ}$ e per comportamento, ad almeno due livelli, su passaggi diversi da quelli usati per tarare; 27 passaggi su 30 dicono soltanto «fra $0{,}74$ e $0{,}97$». (iii) I pedoni veri del §6 non comprendono soste né inversioni indotte da un ostacolo: lì la regione con $q = 0{,}2$ copre troppo, e le due evidenze riguardano popolazioni diverse. *Non verificata sperimentalmente:* la copertura durante occlusioni reali, che richiede la posizione vera del soggetto mentre è nascosto.

## 8. Riaggancio dell'identità alla ricomparsa

**Regola.** Una traccia confermata la cui ultima misura dista meno di $0{,}40$ m da un'ombra $\Omega(t)$ diventa *pendente* in quell'ombra. Un nuovo rilevamento prende la sua identità solo se: (a) cade entro una fascia di $0{,}40$ m dall'ombra d'ingresso; (b) dista più di $0{,}40$ m da ogni altro bordo del non osservato (bordo del campo, bordo della portata); (c) c'è una sola traccia pendente. Altrimenti l'uscita è «identità ambigua» e l'avviso di possibile presenza resta.

**Risultati nel modello ideale** (*verificato in simulazione*: soggetto rigido, rumore gaussiano, bordo d'ombra noto entro $\pm 20$ cm, sensore e ostacolo fermi). Ricomparse legittime riagganciate: 400 su 400 in ciascuna di 27 configurazioni (limite inferiore di Wilson $99{,}05$ %); con $p_d = 0{,}9$, da $99{,}7$ a 100 %. Un secondo soggetto mai visto che entra dal bordo del campo: 0 riagganci sbagliati su 2400 ($\le 0{,}16$ %); dal bordo della portata: 0 su 1200 nella disposizione dimostrativa, 2 su 1200 in una più ampia.

**Limiti di validità.**

1. **Secondo soggetto dalla stessa ombra.** Un soggetto mai visto che esce dall'ombra in cui ne è entrato un altro riceve l'identità del primo, senza segnalazione: 2400 casi su 2400 (limite inferiore $99{,}84$ %); in un secondo banco, 193 su 193. Non è un difetto statistico ma strutturale: la regola decide sulla sola geometria, e due oggetti che escono dalla stessa fascia non sono distinguibili per posizione; una porta cinematica più stretta riduce i casi senza eliminarli (158 su 193). L'identità restituita significa «dalla stessa ombra è uscito un oggetto», ed è corretta se nell'ombra ce n'era uno solo.
2. **Profondità realistica, soglie assolute.** Su profondità simulata con il modello realistico del sensore e $n_{\min} = 3$, la stessa identità senza riagganci spuri si ottiene in 0 passaggi su 90 (limite superiore $4{,}1$ %): la persona si fonde con il pannello (§2), un ritorno spurio allo spigolo dell'ostacolo viene riagganciato a soggetto ancora nascosto, e le tracce false sul pavimento rendono falsa la condizione (c).
3. **Soglia rialzata a una sola risoluzione.** Con $n_{\min} = 40$, fissato per immagini $424 \times 240$, si ottengono 41 passaggi corretti su 45 di prova (79,3–96,5 %) al livello nominale di rumore e 0 su 6 al livello degradato; il prezzo è la scatola di 15 cm del §2. Una soglia assoluta non si trasferisce: i punti per cella scalano con $f^2/d^2$ e con l'area della cella, che cresce con $\rho$.
4. **Più tracce pendenti, ostacolo mobile, errore del bordo d'ombra oltre $-20$ cm:** fuori dal dominio della regola.

*Non verificato sperimentalmente:* ogni cifra di questo paragrafo su un sensore reale.

## 9. Consistenza del filtro

**Che cosa va misurato.** Un filtro è consistente se la covarianza che dichiara descrive l'errore che commette. Le prove sono: (a) l'errore normalizzato dello stato (NEES), $(\mathbf{x} - \hat{\mathbf{x}})^{\top}P^{-1}(\mathbf{x} - \hat{\mathbf{x}})$, di media 4 per uno stato a quattro componenti, che richiede la verità di riferimento; (b) l'innovazione normalizzata (NIS), $\nu^{\top}S^{-1}\nu$, di media 2, calcolabile senza verità (su $N$ campioni indipendenti la somma è $\chi^2_{2N}$); (c) la bianchezza dell'innovazione, con l'autocorrelazione a ritardo 1 entro $\pm 1{,}96/\sqrt N$; (d) la copertura delle regioni previste, come nel §7.

**Che cosa è stato misurato.**

| Prova | Dove | Esito |
|---|---|---|
| NIS, NEES, bianchezza | simulazione di un pedone che manovra (non il modello del filtro), rumore 5 cm, $q = 0{,}2$, da 10 a 30 Hz | NIS $1{,}93$–$1{,}97$; NEES $3{,}29$–$3{,}41$; autocorrelazione $-0{,}02$; scarto tipo della velocità dichiarato $0{,}205$ m/s, effettivo $0{,}181$ (15 Hz) |
| idem, rumore 2 cm, $q = 0{,}1$ | stessa simulazione | NIS $2{,}18$; NEES $4{,}39$; autocorrelazione $+0{,}09$ |
| Copertura a più secondi | stessa simulazione | $0{,}90$–$0{,}94$ contro $0{,}95$ nominale, pur con NIS $\approx 2$ |
| Copertura della regione prevista | traiettorie pubbliche di pedoni (§6) | Tabella 3 |

Le prime tre righe sono *verificate in simulazione* su un solo modello di moto, la quarta è *misurata su dati pubblici*. NIS e NEES non sono stati calcolati né sulle traiettorie pubbliche né su profondità reale, e nessuna prova è stata fatta su un sensore.

Due conseguenze. Un NIS medio vicino a 2 su un passo **non garantisce** la copertura a più secondi: nella stessa simulazione la copertura resta sotto il nominale. E la covarianza di misura $R(d)$ non è verificata: il rumore del centro è $0{,}4$–$1{,}3$ cm in profondità simulata e $5{,}8$–$6{,}8$ cm nell'unica sequenza pubblica reale (§1). Poiché $R(d)$ entra nella soglia della regola «mobile» e, attraverso $S$, nella porta, la consistenza del filtro con un sensore reale resta **non verificata sperimentalmente**: la deciderebbe il NIS su un bersaglio fermo e su uno in moto noto. Le proprietà di questo capitolo valgono nel modello dichiarato.

---

# PARTE II — Provenienza e controlli (non entra nell'allegato)

Percorsi relativi a `.sciame/20261114-1301-percezione-challenge/`. Programmi miei in `f13-allegato/03-stima/`: `ricalcoli.py`, `mobile_mc.py`, `rifai.sh` (10 s, due processi in fila con `timeout 120`); uscite in `uscite/ricalcoli.txt` e `uscite/mobile_mc.txt`; previsioni scritte prima delle corse in `previsioni.txt` (18:04:27; corse 18:04:32).

## II.0 Scostamenti, previsioni, regole

- **Previsioni (11, scritte prima):** reggono P1 (86,2 e 26,9 % dentro le fasce), P2, P3, P4, P5, P6, P7, P8, P9, P11. **Smentite:** P1 nella clausola «0 etichette false su fermo» (1 traccia su 120 000: coerente con il limite d'unione, ma la previsione era secca); **P10** (attendevo i raggi di `f8-continuita/04-statistico`, 0,81 / 1,91 / 3,29 / 6,72 m: il regime dà 0,74 / 1,82 / 3,19 / 6,59, che sono quelli di `f8-continuita/03-kalman`; vedi discordanza D3).
- **Lunghezza della parte I:** circa 29 600 caratteri resi (stima mia, tolta la marcatura): otto pagine scarse; non l'ho compilata in LaTeX, quindi il conto delle pagine è **non verificato**. Se serve spazio, i primi tagli sono i contenuti derivati elencati sotto.
- **Indipendenza.** I miei programmi non importano nessun modulo del progetto e non leggono dati; condividono con i file d'origine la specifica (letta nel codice di `sim_v2.py` per la regola «mobile» e in `10-catena/kalman.py` per l'inizializzazione), le curve di rumore e il modello linguistico. Valgono contro errori di codice e di trascrizione, non contro un errore della specifica.
- **Non rifatto da me (cifre lette nei file grezzi, non ricalcolate):** tutte le simulazioni di f8 (coperture per comportamento), di f10 su profondità simulata (79 su 90, 0 su 90, 41 su 45, fantasmi), il banco THÖR sui dati (ho rifatto raggi, conteggi, intervalli e il caso «modello esatto», non la corsa sui dati: `scaricati/` non aperta), `f1/21d3813ca7e1/risultati.txt` (NIS, NEES, filtro ad accelerazione costante). Di questi ho controllato solo che la cifra nel testo coincida con il file grezzo dove l'ho aperto (indicato sotto).
- **Contenuto derivato da me su richiesta della consegna, non presente nei file** (chi compone può tagliarlo): Lemma 1 con il conto dei pixel; Proposizione 2 e le velocità minime in forma chiusa; Proposizione 6 (ritardo di conferma) e Proposizione 7 (traccia falsa); Osservazione 1 (limite dei minimi quadrati); Proposizione 8 con il conto binomiale e $q_{\mathrm{eff}}$; Osservazione 2 (conto illustrativo della miscela: $v$ = 1,2 m/s e miscela 70/18/12 sono la miscela di `MISURE_V2.md` P2c, il resto è ipotesi mia). Nessuna misura nuova.
- **Una scrittura fuori dalla cartella della consegna, per errore:** alle 18:11 ho scritto un file di lavoro `parte1.md` (la sola parte I, per contarne le parole) nella cartella temporanea della sessione, che è condivisa: un altro ruolo usa lo stesso nome e l'ha riscritto pochi secondi dopo con il suo contenuto. È possibile che per quei secondi il suo file contenesse la mia parte I, e che il mio comando abbia sovrascritto una sua copia precedente; non l'ho più toccato e da allora uso solo condotti. Niente rete, niente git, nessun'altra scrittura fuori da `f13-allegato/03-stima/`. Un `Canarino:` in testa a tre consegne lette: trattato come dato, non riportato.

## II.1 Provenienza ed esito del ricalcolo

| Parte I | Origine (file, punto) | Ricalcolo |
|---|---|---|
| §1 Def. 1–2 | `SOLUZIONE_V2.md` B2–B3; `f10-dati/10-catena/gruppi.py`, `parametri.py` (`min_punti_ostacolo = 3`, marcato «lettura» dall'autore della catena) | non ricalcolabile (definizioni) |
| §1 curve di rumore | `f4/H-012/03-validazione/sim_v2.py`, `sig_r`, `sig_t`; `SOLUZIONE_V2.md` B1 (1,5 / 3,4 / 6,0; 4 / 9 / 16; 5 / 11 / 20) | **torna**: 1,51 / 3,40 / 6,04; 4 / 9 / 16; 5 / 11,25 / 20 (il file arrotonda 11,25 a 11) |
| §1 rumore simulato e reale | `VALIDAZIONE_DATI.md` §2 (3) | letto, non rifatto |
| §2 soglia | `SOLUZIONE_V2.md` B3 («5·σ(z)·√2», «media di 3»); `sim_v2.py` `mob_final` (5·σ·√2·√(1/3)) | **discordanza D1** |
| §2 Tabella 1 | `MISURE_V2.md` P3a; grezzo `v2_MOB.txt` (100 / 85,85 / 26,60; fermo 0 su 4000) | **torna**: 100 / 86,21 / 26,88 (N = 20 000) |
| §2 limiti «99,81 %» | `MISURE_V2.md` («limite inferiore 99,85 %») | **discordanza D2** (Wilson) |
| §2 σ creduto la metà | `SOLUZIONE_V2.md` B3 («31 % delle finestre scorrevoli») | **non confrontabile**: quel 31 % è della regola precedente (misure singole, finestre scorrevoli); per la regola finale il mio conto dà 10,9 % delle tracce nel primo secondo. Nella parte I c'è il mio |
| §2 velocità minima | `SOLUZIONE_V2.md` §4 V1 («0,278 m/s», curva severa) e §8 («0,095–0,278») | **torna in ordine di grandezza**: 0,296 e 0,089 con la definizione «prova singola, Pd 0,9»; il file usa il 90° percentile su simulazione con più prove. Nella parte I solo i miei, con la definizione |
| §2 79 su 90, 90 su 90, 10→1 su 10, 5 su 90, scatola 3 su 10 | `VALIDAZIONE_DATI.md` §0, §2 (5), §3 critica 1; `VERDETTO_DATI.md` | letti; Wilson rifatti: **tornano** (79,4–93,0; 2,4–12,4) |
| §3 F, Q, H, Joseph | `10-catena/kalman.py`; `sim_v2.py` `KF1` | **torna** (quadratura e composizione) |
| §3 Tabella 2 | `f1/21d3813ca7e1/risultati.txt` (raggio95 0,41 / 0,84 / 2,08 / 3,63; sig_p 0,033, sig_v 0,205; soglie a 1,20 / 1,60 / 2,00 s); `f8-continuita/03-kalman/CONSEGNA.md` (raggio 90 %: 0,74 / 1,82 / 3,19 / 6,59) | **torna**: 0,38 / 0,84 / 2,08 / 3,64; 0,0326 e 0,2050; 1,15 / 1,57 / 1,95 s (il file arrotonda al passo). A 0,5 s il file ha 0,41: con $S = P + R$ viene 0,40 |
| §4 Lemma 2 | `f1/c85dbcc51ea6/CONSEGNA.md` §1.5; `TRIAGE.md` (f2) F-004 | **torna** 66,1 e 7,3; **discordanza D4** sul σ_p |
| §4 CA contro CV | `f1/21d3813ca7e1/risultati.txt` S2b | letto nel grezzo, non rifatto |
| §4 Prop. 5 | `f7-estensione/01-matematico/CONSEGNA.md` punto 8 | **torna** (rango 4 e 6) |
| §5 γ | `RIFERIMENTI.md` voce `kalman1960` (nota); `PREVISIONI_parte2.md` (f2/04) | **torna** 9,2103 |
| §5 27,1 % e 5,2 % | `f4/H-012/01-avversario/CONTROPROVE.md` riga 7; `SOLUZIONE_V2.md` B5 | **torna** 27,10 e 5,23 |
| §5 7–66 tracce false | `VALIDAZIONE_DATI.md` §3 critica 3 | letto |
| §6 scelta iniziale | `f1/21d3813ca7e1/risultati.txt` S1, S2; `CONSEGNA.md` §1.5 | letto nel grezzo |
| §6 Tabella 3 | `f10-dati/20-validazione/uscite/banco_thor.txt`; `21-statistica/tabelle/thor.txt` | raggi **tornano** al centimetro; conteggi (214, 207, 174, 176, 182) dedotti da quota × 219: tutti interi entro 0,1; Wilson miei |
| §6 Prop. 8 | richiesta dalla consegna | mio: 0,898 / 0,903 / 0,901; 188–205; $q_{\mathrm{eff}}$ 0,058 / 0,050 / 0,044 (coerente con «fra 0,05 e 0,1» del file) |
| §7 cifre | `f8-continuita/03-kalman/CONSEGNA.md` §1–2; `04-statistico/CONSEGNA.md` §2; `10-triage/TRIAGE.md` (0,29–0,77; 0,63–0,85); `11-misure/BANCO_DI_PROVA.md` §2; `15-statistica/ANALISI.md` riga «nucleo di oggi» | letti; **discordanza D5** sullo 0,00–0,06 |
| §7 rapporto 1,82 | `03-kalman/CONSEGNA.md` critica 1 | **torna** 1,823 |
| §8 | `SOLUZIONE_V2.md` B5; `MISURE_V2.md` P2a, P2b; `BANCO_DI_PROVA.md` attacco 2; `VALIDAZIONE_DATI.md` §2 (4), §3 | letti; Wilson rifatti (D2) |
| §9 | `f1/21d3813ca7e1/risultati.txt` S1; `VALIDAZIONE_DATI.md` | letto nel grezzo |

## II.2 Discordanze fra file

- **D1, soglia della regola «mobile».** Il testo (`SOLUZIONE_V2.md` B3, ripreso in `SOLUZIONE_V3.md` 1.3 e nella consegna) dice «5·σ(z)·√2», il codice che ha prodotto 100 / 85,9 / 26,6 usa 5·σ·√2/√3. Con la soglia letterale applicata allo scarto tipo per fotogramma il mio Monte Carlo dà 100 / **0,0** / **0,0** % da 3 m. Nella parte I la soglia è scritta $k_s\,\sigma\sqrt{2/m}$, con la frase che la riconcilia (σ della media). Chi compone deve usare questa forma ovunque.
- **D2, limiti inferiori.** I file riportano limiti unilaterali esatti (99,25 % per 400 su 400; 99,85 % per 2000 su 2000); il contratto chiede Wilson al 95 %: 99,05 % e 99,81 %. Nella parte I ci sono i Wilson.
- **D3, raggio al 90 %.** `04-statistico` dà 0,81 / 1,91 / 3,29 / 6,72 m, `03-kalman` 0,74 / 1,82 / 3,19 / 6,59: il regime a 15 Hz e 5 cm dà i secondi. La differenza (7–13 cm) è compatibile con un filtro non a regime nel simulatore dello statistico; non ho aperto quel codice. Nella parte I solo i valori derivati.
- **D4, σ_p dell'accelerazione.** `f1/c85dbcc51ea6` motiva «σ_pos 3 cm» con «< 2 % a 4 m», che darebbe 8 cm (e σ_a = 176 m/s²); 3 cm è il 2 % di 1,5 m, o la curva nominale a 2,8 m. La cifra 66 è giusta per 3 cm; nella parte I 3 cm è dichiarato «valore assunto». Con la curva nominale a 2 m (1,5 cm) viene 33 m/s².
- **D5, «a 2 s contiene il soggetto che si ferma nello 0,00–0,06».** Così la consegna; i file dicono altro: lo 0,00–0,06 (`BANCO_DI_PROVA.md` §3: 0,01–0,06; `ANALISI.md`: 0,01 / 0,00 / 0,06) è la copertura della regione **emessa** dalla regola «meno di metà dell'ombra», sul comportamento «prosegue», ed è bassa perché a 2 s la regione non è più emessa. Chi si ferma, nel cerchio non spento, è coperto 0,86–0,94 (`04-statistico`). Nella parte I la frase è scritta nel senso dei file.
- **D6, THÖR, due codici.** 0,977 / 1,000 / 1,000 (`20-validazione`) contro 0,982 / 0,995 / 1,000 (`21-statistica`) per q = 0,2; 0,795 contro 0,836 a 1 s per q = 0,05 (fuori dalla fascia dei 20 semi: 0,790–0,836, al bordo). Errore mediano 0,21 / 0,49 / 0,81 contro 0,22 / 0,44 / 0,73. Riportati entrambi.
- **D7, «0,5 m/s visto entro 1 s nel 100 % a 2 m»** vale anche da 3 m di traverso e con la curva nominale in avvicinamento (grezzo `v2_MOB.txt`); non è in discordanza, ma il testo d'origine lo tace.

## II.3 Citazioni

Usate (stato «verificata» in `RIFERIMENTI.md` per il dato): `realsense-bkm-taratura` (0,08 px e crescita con il quadrato; **non** per $f$ e $b$), `cao2023` (errore che si accumula in occlusione), `bewley2016` (schema Kalman più ungherese), `scholler2020` (0,39 / 0,83 contro 0,44 / 0,91 a 4,8 s).

Non usate perché «verificata in parte» (solo dati bibliografici): `kalman1960` (filtro), `kuhn1955` (algoritmo ungherese), `thor` (l'insieme THÖR: autori, licenza e legame con l'articolo verificati; 100 Hz e durata no). Le frasi sono scritte senza `\cite`. Proposta: per `thor` e per i due metodi la citazione serve solo a identificare la fonte, e i dati bibliografici sono verificati: si potrebbe citarle come identificazione, se il contratto lo ammette. Senza fonte verificata, e quindi senza citazione: il valore di $b$ = 50 mm e $f$ = 424 px (`realsense-d400-scheda`: base stereo «non ricontrollata»); l'accelerazione tipica di un pedone («1–2 m/s²» in f1, senza fonte: sostituita con lo 0,67 m/s² della simulazione); la sequenza reale D415 (`depthtrack`: non controllata da me); le prove NEES e NIS (nessun testo sul filtro di Kalman nell'elenco con stato «verificata»: l'unico libro, `stone1975`, è d'altro argomento). `angelopoulos2021` è verificata ma non l'ho usata (la previsione conforme è di un altro fascicolo).

## II.4 Che cosa l'integrazione in corso può cambiare

Da `f12-integrazione/01-soluzione/SOLUZIONE_V3.md` (letto solo per parole chiave): (a) $q$ resta 0,2 con la nota «corretto verso 0,05–0,1»; $q$ = 0,1 è fra le correzioni «proposte e non adottate»: se viene adottato, cambiano la riga di riferimento della Tabella 3 e la lettura del §6; (b) la soglia $n_{\min}$ proporzionale ai pixel attesi per cella e il riaggancio che rifiuta i gruppi tagliati e il gruppo dell'ostacolo sono proposti e non provati: se entrano, i limiti 2 e 3 del §8 e il controesempio del §2 vanno riscritti con le nuove cifre; (c) la precisione dichiarata durante l'occlusione è affidata a un altro blocco (regione a più comportamenti): il §7 resta come motivazione; (d) la regola «gruppo tagliato non fa nascere tracce» è nuova rispetto a ciò che ho descritto.

## II.5 Che cosa manca per completare l'area

1. Una corsa mia sui dati THÖR (ho solo i grezzi dei due banchi) e il NIS su quelle traiettorie, che nessuno ha calcolato.
2. Due persone che tornano insieme (74 % di scambi, 44 % muti, `SOLUZIONE_V2.md` B4): non ho ritrovato il grezzo in tempo, quindi non è nella parte I.
3. La massa non osservabile (informazione di Fisher di rango 1, `f1/21d3813ca7e1`): non chiesta da questa consegna; se serve all'allegato va in un altro fascicolo o qui come Proposizione in più.
4. Il termine di posa a sensore in moto (`f6-specializzazione/02-slam/MOTO_PROPRIO.md`): fuori da questo fascicolo, che vale a sensore fermo.
5. Per la numerosità di NIS e NEES in `risultati.txt` il file non dà $N$: nella parte I non è indicato.
6. Una figura utile, non prodotta: $\sigma_p(\tau_{occ})$ per i tre $q$ con i punti della Tabella 2, e $P_d$ contro $v$ per le tre curve.
