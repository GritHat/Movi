# Fascicolo — Geometria d'osservazione e modello del sensore

# PARTE I — Contenuto per l'allegato

Tutti i risultati di questo capitolo sono dimostrazioni in un modello dichiarato, calcoli, letture di schede dei costruttori, misure pubblicate da terzi o simulazioni. Nessuna grandezza è stata misurata su un sensore fisico: dove un risultato dipende dal sensore reale, lo si dice come limite di validità.

## 0. Simboli aggiunti alla notazione comune

$T_h=\tan(\mathrm{FOV}_h/2)$, $T_v=\tan(\mathrm{FOV}_v/2)$; $\beta_-=\theta+\mathrm{FOV}_v/2$ e $\beta_+=\mathrm{FOV}_v/2-\theta$ (angoli del bordo basso e del bordo alto del campo rispetto all'orizzontale); $(u,v)$ coordinate d'immagine normalizzate ($v$ verso il basso); $a$ altezza di un ostacolo; $s$ statura di una persona; $z_o$, $z_p$ coordinate in avanti dell'ostacolo e della persona; $L$ larghezza di un pannello, $w$ larghezza del corpo, $v$ velocità di passaggio, $T_{\mathrm{tot}}$ durata dell'occlusione totale; $d_{\mathrm{bordo}}$, $d_{\mathrm{sfondo}}$ profondità di un bordo occludente e dello sfondo; $k=\sigma_d/(f\,b)$ coefficiente del rumore di profondità; $\delta\theta$ errore d'inclinazione, $\delta\psi$ errore d'imbardata relativa, $\omega$ velocità angolare; $\kappa$ moltiplicatore di soglia della regola di mobilità, $W$ la sua finestra; $y_s$ soglia di quota che separa suolo e ostacolo; $g$ larghezza della fascia di guardia, $\tau_{\text{età}}$ età massima di una cella «libero», $e_{\mathrm{ombra}}$ errore del bordo d'ombra; $S_{\mathrm{sep}}$ distanza di separazione, $v_H$ velocità d'avvicinamento, $T_R$, $T_S$ tempi di risposta e d'arresto, $C$, $Z_S$ termini additivi; $Q(\cdot)$ coda della gaussiana standard.

## 1. Modello della camera

**Definizione 1 (camera).** La camera è un foro stenopeico senza distorsione, con centro $C=(0,h,0)$, asse ottico $\mathbf e_d=(0,-\sin\theta,\cos\theta)$, asse d'immagine verso il basso $\mathbf e_v=(0,-\cos\theta,-\sin\theta)$ e verso destra $\mathbf e_u=(1,0,0)$. Un punto $P=(x,y,z)$ ha profondità $d=(P-C)\cdot\mathbf e_d=(h-y)\sin\theta+z\cos\theta$ e coordinate normalizzate $u=x/d$, $v=[(h-y)\cos\theta-z\sin\theta]/d$. È nel campo se $d>0$, $|u|\le T_h$, $|v|\le T_v$. Il pixel è $(c_x+f\,u,\;c_y+f\,v)$. Posa di riferimento: $h=1{,}2$ m, $\theta=15^\circ$.

**Tabella 1 — Profili di sensore considerati** (valori dichiarati dai costruttori nelle rispettive schede, flusso 848 × 480 a 30 fotogrammi al secondo; nessun valore è misurato su un esemplare).

| | RealSense D455 | RealSense D435i | Orbbec Gemini 335 |
|---|---|---|---|
| $\mathrm{FOV}_h\times\mathrm{FOV}_v$ della profondità | 87° × 58° | 87° × 58° | 90° × 60° (90° × 65° a 1280 × 800) |
| Base $b$ | 95 mm | 50 mm | 50 mm |
| Focale $f$ usata nei conti di rumore | 424 px | 424 px | 410,7 px |
| Distanza minima; fascia ideale | 0,35 m; 0,6–6 m | 0,195 m; 0,3–3 m | 0,18 m; 0,3–3 m |
| $\sigma_d$ nominale / limite | 0,08 / 0,20 px | 0,08 / 0,21 px | 0,082 / 0,154 px |
| Tolleranza dichiarata sul campo | ±3° | ±3° | ±3° |

**Osservazione 1 (focale e campo).** Nel foro stenopeico $f=(W/2)/T_h$: con 848 px, 87° danno 446,8 px e 58° (480 px) danno 433,0 px; $f=424$ px corrisponde a 90° × 59,0°. I 424 px sono il valore con cui il costruttore traccia la curva di rumore (campo dell'imager di 90°), gli 87° × 58° sono il campo utile della profondità. In questo capitolo la geometria del campo usa gli angoli dichiarati (87° × 58°), il rumore usa $f\,b$ con $f=424$ px; lo scarto fra le due scelte è il 5 % sulle grandezze laterali e 2 cm su $z_{\min}$ (1,22 m con 59,0° contro 1,24 m). I parametri intrinseci veri si leggono dall'esemplare. *Livello: verificato per calcolo.*

## 2. Dove il suolo è visibile

**Proposizione 1 (campo in coordinate del suolo).** Nel modello della Definizione 1, con $\beta_\pm\in(0,90^\circ)$, un punto $P=(x,y,z)$ con $z>0$ è nel campo se e solo se
$$h-z\tan\beta_-\;\le\;y\;\le\;h+z\tan\beta_+\qquad\text{e}\qquad |x|\le T_h\,[(h-y)\sin\theta+z\cos\theta].$$

*Dimostrazione.* Sia $\beta=\operatorname{atan}\!\big((h-y)/z\big)$ la depressione del punto vista dal centro. Dividendo numeratore e denominatore di $v$ per $z\cos\theta$ si ha $v=(\tan\beta-\tan\theta)/(1+\tan\beta\tan\theta)=\tan(\beta-\theta)$. Quindi $|v|\le T_v\iff\theta-\mathrm{FOV}_v/2\le\beta\le\theta+\mathrm{FOV}_v/2$, cioè $-\tan\beta_+\le(h-y)/z\le\tan\beta_-$, che è la prima condizione; in questo intervallo $d>0$. La seconda è $|u|\le T_h$ con $d$ della Definizione 1. $\square$

I due bordi verticali del campo sono dunque due **piani** che dipendono solo da $z$, non dall'azimut. Con $\beta_-=44^\circ$ e $\beta_+=14^\circ$:

**Corollario 1 (suolo).** Il suolo ($y=0$) è nel campo per $z\ge z_{\min}=h/\tan\beta_-=1{,}2/\tan44^\circ=1{,}243$ m e $|x|\le T_h(z\cos\theta+h\sin\theta)=0{,}917\,z+0{,}295$ m. Il confine vicino è la **retta** $z=z_{\min}$: la zona cieca vicina è una striscia, non un anello. In coordinate polari $\rho_{\min}(\varphi)=z_{\min}/\cos\varphi$: 1,24 m sull'asse, 1,43 m a 30°, 1,71 m a 43,5°; lo spigolo del campo tocca il suolo a $x=\pm1{,}43$ m, cioè $\varphi=\pm49{,}1^\circ$, $\rho=1{,}90$ m. Con $f=424$ px ($\mathrm{FOV}_v=59{,}0^\circ$) si ha $z_{\min}=1{,}221$ m e 1,70 m a 44°.

**Corollario 2 (ostacolo basso).** La cima di un ostacolo alto $a<h$ è nel campo solo per $z\ge(h-a)/\tan\beta_-$: 1,087 m per $a=0{,}15$ m, 1,139 m per 0,10 m. Sotto questa distanza l'ostacolo è interamente fuori campo.

**Corollario 3 (tetto del campo).** La quota massima visibile è $y_{\max}(z)=h+z\tan\beta_+=1{,}2+0{,}249\,z$; una quota $y>h$ è vista solo per $z\ge(y-h)/\tan\beta_+$.

**Tabella 2 — Limiti verticali del campo** ($h=1{,}2$ m, $\theta=15^\circ$).

| $z$ (m) | 1,24 | 1,7 | 1,9 | 2,0 | 2,3 | 3,0 | | quota (m) | 1,60 | 1,70 | 1,80 | 1,90 | 2,00 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $y_{\max}$ (m) | 1,51 | 1,62 | 1,67 | 1,70 | 1,77 | 1,95 | | vista da $z\ge$ (m) | 1,60 | 2,01 | 2,41 | 2,81 | 3,21 |

Conseguenza: entro 3 m la colonna da 0 a 2 m di quota non è mai osservata per intero; una testa a 1,70 m non è vista sotto 2,01 m e un ostacolo sospeso a 1,80 m sotto 2,41 m. Lo stato «libero» è quindi un'affermazione sul suolo e sul volume fino a $y_{\max}(z)$, non sulla colonna intera.

| Profilo ($\mathrm{FOV}_v$) | $z_{\min}$ suolo | $z$ per $a=0{,}15$ m | $\tan\beta_+$ | quota 1,80 m vista da |
|---|---|---|---|---|
| D455, D435i (58°) | 1,243 m | 1,087 m | 0,249 | 2,41 m |
| Gemini 335 (60°) | 1,200 m | 1,050 m | 0,268 | 2,24 m |
| Gemini 335 (65°) | 1,100 m | 0,962 m | 0,315 | 1,90 m |

*Sensibilità di $z_{\min}$:* da 1,18 a 1,31 m per $\mathrm{FOV}_v=58^\circ\pm3^\circ$; da 1,20 a 1,29 m per $\theta=15^\circ\pm1^\circ$. *Livello: dimostrato nel modello del foro stenopeico; valori verificati per calcolo e con un lancio di raggi su 848 × 480 pixel (minimo di $z$ al suolo 1,245 m ai centri dei pixel, uguale su tutte le colonne). Condizioni: suolo piano, posa nota, assenza di distorsione. Controesempio fuori dalle ipotesi: su una rampa o con la camera più inclinata i limiti si spostano secondo il §5.*

**Proposizione 2 (frazione del disco coperta).** Sia $D$ il disco di raggio 3 m centrato sulla proiezione della camera (28,27 m²). (i) Approssimando la regione vista con il settore d'anello di apertura $\mathrm{FOV}_h$ fra $\rho=z_{\min}$ e 3 m, l'area è $\tfrac12\mathrm{FOV}_h(3^2-z_{\min}^2)=5{,}66$ m², il **20,0 %** di $D$. (ii) Con la regione esatta del Corollario 1 intersecata con $D$ l'area è 5,79 m², il **20,5 %** (integrazione numerica su una griglia di 2 mm). *Livello: verificato per calcolo.* In entrambi i conti quattro quinti del disco non sono osservati dalla camera.

## 3. L'ombra

**Proposizione 3 (ombra sul suolo).** Un ostacolo opaco alto $a$ a distanza $\rho_o$ lungo una direzione $\varphi$ nasconde il suolo, in quella direzione, per $\rho_o<\rho<\rho_o\,h/(h-a)$ se $a<h$, e per ogni $\rho>\rho_o$ se $a\ge h$.

*Dimostrazione.* Nel piano verticale per il centro e la direzione $\varphi$, il raggio che sfiora la cima $(\rho_o,a)$ ha equazione $y=h-(h-a)\rho/\rho_o$ e tocca il suolo a $\rho=\rho_o h/(h-a)$; i punti del suolo più vicini hanno il raggio intercettato dall'ostacolo. Se $a\ge h$ il raggio non scende. $\square$

Esempi: $a=0{,}3$ m a 1,7 m: ombra fino a 2,27 m; $a=0{,}5$ m a 1,5 m: 2,57 m; $a=1{,}0$ m a 1,5 m: 9,0 m. In pianta l'ombra è il **cuneo** compreso fra gli azimut dei due bordi dell'ostacolo; per un ostacolo più basso della camera il cuneo è troncato alla distanza della Proposizione 3 e non arriva al bordo della portata. *Livello: dimostrato (ottica geometrica, ostacolo opaco, suolo piano).*

**Proposizione 4 (altezza che nasconde una persona).** Un pannello opaco a $z_o$, alto $a$, nasconde per intero dall'alto una persona di statura $s$ a $z_p>z_o$ se e solo se
$$a\;\ge\;a_{\min}=h+z_o\,\min\!\Big(\frac{s-h}{z_p},\;\tan\beta_+\Big).$$
Viceversa, sopra un pannello alto $a$ resta visibile a $z_p$ la fascia di quota fra $h+(a-h)z_p/z_o$ e $\min(s,\,y_{\max}(z_p))$.

*Dimostrazione.* Il raggio dal centro alla sommità $(z_p,s)$ passa a $z_o$ alla quota $h+(s-h)z_o/z_p$; se il pannello la raggiunge, ogni punto più basso della persona è nascosto, perché il suo raggio passa più in basso. Se $s>y_{\max}(z_p)$ la parte sopra il tetto del campo non è comunque vista e basta raggiungere il tetto a $z_o$, cioè $h+z_o\tan\beta_+$. $\square$

**Tabella 3 — $a_{\min}$ (m) per una persona a $z_p=2{,}3$ m.**

| $s$ \ $z_o$ | 1,15 m | 1,5 m | 1,7 m | 1,8 m | 1,9 m | 2,0 m |
|---|---|---|---|---|---|---|
| 1,60 m | 1,40 | 1,46 | 1,50 | 1,51 | 1,53 | 1,55 |
| 1,70 m | 1,45 | 1,53 | 1,57 | 1,59 | 1,61 | 1,63 |
| 1,75 m | 1,48 | 1,56 | 1,61 | 1,63 | 1,65 | 1,68 |
| ≥ 1,77 m (tetto del campo) | 1,49 | 1,57 | 1,62 | 1,65 | 1,67 | 1,70 |

Un pannello alto 1,5 m a 1,7–1,9 m dalla camera **non** nasconde una persona a 2,3 m: resta in vista ciò che supera 1,61 m (a 1,7 m) o 1,56 m (a 1,9 m), fino al tetto di 1,77 m. A 1,7–1,9 m servono fra 1,61 m (statura 1,75 m) e 1,67 m (qualunque statura); un pannello di **1,7 m** nasconde ogni statura fino a $z_o=2{,}0$ m (a margine nullo a 2,0 m, con 3–8 cm a 1,9–1,7 m), e 1,8 m dà da 10 a 18 cm di margine contro l'errore di posa e la tolleranza del campo. *Livello: dimostrato nel modello; verificato per calcolo. Limite: il pannello deve anche coprire in larghezza (Proposizione 5); la tolleranza di ±3° sul campo sposta il tetto di circa ±5 cm a 1,9 m.*

**Proposizione 5 (durata dell'occlusione totale).** Un pannello largo $L$ a $z_o$, parallelo al piano dell'immagine, proietta alla distanza $z_p$ un'ombra larga $L\,z_p/z_o$. Un corpo largo $w$ che la attraversa di traverso a velocità $v$ è nascosto per intero per
$$T_{\mathrm{tot}}=\frac{L\,z_p/z_o-w}{v}.$$

*Dimostrazione.* I raggi per i due bordi del pannello sono rette per l'origine in pianta: a $z_p$ distano $L z_p/z_o$ (triangoli simili). Il corpo è tutto nascosto finché entrambi i suoi estremi stanno nell'ombra, cioè lungo un tratto $L z_p/z_o-w$. $\square$

**Tabella 4 — $T_{\mathrm{tot}}$ (s), $z_p=2{,}3$ m, $w=0{,}45$ m.**

| $L$; $z_o$ | ombra (m) | tratto nascosto (m) | 1,4 m/s | 1,0 m/s | 0,5 m/s |
|---|---|---|---|---|---|
| 1 m; 1,7 m | 1,35 | 0,90 | 0,64 | 0,90 | 1,81 |
| 1 m; 1,9 m | 1,21 | 0,76 | 0,54 | 0,76 | 1,52 |
| 2 m; 1,7 m | 2,71 | 2,26 | 1,61 | 2,26 | 4,51 |
| 2 m; 1,9 m | 2,42 | 1,97 | 1,41 | 1,97 | 3,94 |

A passo normale (1,0–1,4 m/s) un pannello da 1 m dà 0,54–0,90 s di occlusione totale, uno da 2 m 1,4–2,3 s. *Livello: dimostrato in pianta; verificato per calcolo.*

**Proposizione 6 (banda senza dato accanto a un bordo).** In una coppia stereo con riferimento sull'imager sinistro e base $b$, accanto a un bordo verticale a profondità $d_{\mathrm{bordo}}$, dal lato sinistro, lo sfondo a profondità $d_{\mathrm{sfondo}}$ non ha disparità su una banda larga
$$\Delta x=b\,\frac{d_{\mathrm{sfondo}}-d_{\mathrm{bordo}}}{d_{\mathrm{bordo}}}\ \text{(sullo sfondo)},\qquad \Delta u=f\,b\Big(\frac1{d_{\mathrm{bordo}}}-\frac1{d_{\mathrm{sfondo}}}\Big)\ \text{(pixel)}.$$

*Dimostrazione.* In pianta, imager sinistro in $(0,0)$ e destro in $(b,0)$; l'ostacolo occupa $x\ge x_e$ alla profondità $d_{\mathrm{bordo}}$. Un punto $(x,d_{\mathrm{sfondo}})$ è visto dal sinistro se $x<x_e\,d_{\mathrm{sfondo}}/d_{\mathrm{bordo}}$; dal destro se il segmento da $(b,0)$ passa a sinistra del bordo, $b+(x-b)\,d_{\mathrm{bordo}}/d_{\mathrm{sfondo}}<x_e$, cioè $x<x_e d_{\mathrm{sfondo}}/d_{\mathrm{bordo}}-b(d_{\mathrm{sfondo}}-d_{\mathrm{bordo}})/d_{\mathrm{bordo}}$. La differenza dei due limiti è $\Delta x$; in pixel $\Delta u=f\Delta x/d_{\mathrm{sfondo}}$. $\square$

**Tabella 5 — Banda d'occlusione stereo.**

| bordo; sfondo | D455 | D435i | Gemini 335 |
|---|---|---|---|
| 1 m; 3 m | 19,0 cm = 27 px | 10,0 cm = 14 px | 10,0 cm = 14 px |
| 1,5 m; 3 m | 9,5 cm = 13 px | 5,0 cm = 7 px | 5,0 cm = 7 px |
| 2 m; 3 m | 4,8 cm = 7 px | 2,5 cm = 4 px | 2,5 cm = 3 px |

La banda è sistematica e da un lato solo; i bordi orizzontali non ne hanno. Per la stessa ragione manca il dato su una striscia di $f\,b/d$ pixel al bordo sinistro dell'immagine (20 px a 2 m con $b=95$ mm, 11 px con 50 mm). Chi ricompare dal lato della banda è misurato $\Delta x/v$ più tardi: 0,16 s a 1,2 m/s con 19 cm. *Livello: dimostrato (geometria epipolare ideale); verificato numericamente (0,1900 m). Una misura di terzi sulla D435 riporta un peggioramento sul bordo sinistro del bersaglio \cite{ahn2019}, coerente con il lato previsto; l'ampiezza su un esemplare reale non è verificata sperimentalmente, e i filtri di riempimento del costruttore, se attivi, la mascherano copiando lo sfondo.*

## 4. Rumore di profondità dello stereo

**Proposizione 7.** Se la disparità $\delta=f\,b/d$ è misurata con errore di scarto tipo $\sigma_d$ (pixel), al primo ordine
$$\sigma_z(d)=\frac{d^2}{f\,b}\,\sigma_d=k\,d^2 .$$

*Dimostrazione.* $d=f\,b/\delta\Rightarrow\partial d/\partial\delta=-f\,b/\delta^2=-d^2/(f\,b)$; propagazione lineare dell'errore. $\square$

Il costruttore indica $\sigma_d<0{,}1$ px per una camera ben tarata e traccia la curva di riferimento con 0,08 px \cite{realsense-bkm-taratura}: è il valore «nominale». Il valore «limite» si ricava dal massimo dichiarato in scheda: scarto quadratico ≤ 2 % a 4 m (D455, $k=0{,}02\cdot4/16=0{,}005$ m⁻¹), ≤ 2 % a 2 m (D435i, $k=0{,}010$ m⁻¹), ≤ 1,5 % a 2 m (Gemini 335, $k=0{,}0075$ m⁻¹); per la Gemini 335 il nominale ($k=0{,}004$ m⁻¹) è letto da un grafico di scheda.

**Tabella 6 — $\sigma_z$ (cm) e passo di quantizzazione.**

| Profilo ($f\,b$, px·m) | | 1 m | 2 m | 3 m | 4 m | $\sigma_z=5$ cm a |
|---|---|---|---|---|---|---|
| D455 (40,28) | nominale | 0,20 | 0,79 | 1,79 | 3,18 | 5,0 m |
| | limite | 0,50 | 2,00 | 4,50 | 8,00 | 3,2 m |
| D435i (21,20) | nominale | 0,38 | 1,51 | 3,40 | 6,04 | 3,6 m |
| | limite | 1,00 | 4,00 | 9,00 | 16,0 | 2,2 m |
| Gemini 335 (20,54) | nominale | 0,40 | 1,60 | 3,60 | 6,40 | 3,5 m |
| | limite | 0,75 | 3,00 | 6,75 | 12,0 | 2,6 m |
| Passo di quantizzazione (mm), disparità a 1/32 px | D455 | 0,8 | 3,1 | 7,0 | 12,4 | |
| | D435i | 1,5 | 5,9 | 13,3 | 23,6 | |

*Quantizzazione.* Un passo di disparità $q_\delta$ dà un passo di profondità $d^2 q_\delta/(f\,b)$ e uno scarto tipo $1/\sqrt{12}$ di quel passo (2,0 mm a 3 m per la D455, 3,8 mm per la D435i): inferiore al rumore nominale. Il valore $q_\delta=1/32$ px è un'ipotesi non confermata da una scheda.

*Confronto con una misura indipendente.* Su una D435 a 848 × 480, bersaglio bianco frontale fra 0,4 e 2,1 m, è stato misurato $\sigma_z=0{,}00106+0{,}00073\,d+0{,}00395\,d^2$ m \cite{ahn2019}: 1,83 cm a 2 m, cioè 1,21 volte il nominale (0,097 px equivalenti); a 3 m (3,9 cm) è un'estrapolazione.

*Limiti di validità.* I valori dichiarati valgono su bersaglio chiaro e frontale nella parte centrale del campo. Il rumore è correlato nello spazio, quindi la media su $N$ pixel non lo riduce come $\sqrt N$. Dal punto di montaggio il suolo è visto con incidenza $\operatorname{atan}(\rho/h)$ dalla normale: 46° a 1,24 m, 60° a $\rho=h\tan60^\circ=2{,}08$ m, 68° a 3 m; oltre 60° non esiste una misura del rumore sul suolo. *Livello: formula dimostrata; valori nominali e limite calcolati da dati di scheda; comportamento sul suolo radente, su tessuti scuri e su superfici lucide non verificato sperimentalmente.*

**Risoluzione e rumore laterali.** Un pixel copre $d/f$: con il campo dichiarato di 87° ($f=446{,}8$ px) 4,5 mm a 2 m e 6,7 mm a 3 m; un oggetto che debba coprire 5 pixel di lato è quindi osservabile a 3 m solo se è largo almeno **3,4 cm** (6,7 cm a 6 m), e un oggetto di 1 cm solo entro 0,89 m. Con $f=424$ px i valori crescono del 5 % (3,5 cm). Il rumore laterale misurato da terzi ai bordi di un bersaglio è 4,3 cm (bordo sinistro) e 4,1 cm (destro) al 90° percentile \cite{ahn2019}. La sfocatura da moto vale $v\,t_{\mathrm{esp}}$: 12 mm a 1,5 m/s con 8 ms, 45 mm con 30 ms. *Livello: verificato per calcolo; il criterio dei 5 pixel è una convenzione.*

## 5. Effetto di un errore di posa

**Proposizione 8 (errore di quota).** Se l'inclinazione creduta differisce dalla vera di $\delta\theta$, un punto del suolo a distanza $\rho$ sull'asse è ricostruito alla quota
$$\Delta y=\rho\sin\delta\theta+h(1-\cos\delta\theta)\;\approx\;\rho\,\delta\theta .$$

*Dimostrazione.* Rispetto al centro il punto è $(\rho,-h)$ nel piano verticale; una rotazione di $\delta\theta$ attorno all'asse trasversale porta la sua quota a $-h\cos\delta\theta+\rho\sin\delta\theta$; la differenza da $-h$ è $\Delta y$. $\square$

Con $\delta\theta=1^\circ$: 3,5 cm a 2 m, **4,9 cm a 2,8 m**, 5,2 cm a 3 m. Detta $y_s=0{,}07$ m la soglia di quota sopra cui un ritorno è «occupato»:
- con un errore che alza il suolo, il pavimento supera la soglia oltre $\rho\approx y_s/\delta\theta$: con 2° da 1,99 m in poi il suolo risulta occupato;
- con un errore che lo abbassa, un ostacolo alto $a$ scende sotto la soglia, e viene classificato suolo, quando $\rho\,\delta\theta>a-y_s$: per $a=0{,}10$ m bastano 0,86° a 2 m, 0,67° a 2,55 m, 0,57° a 3 m; per $a=0{,}15$ m servono 2,3° a 2 m.

*Riscontro in simulazione* (catena di elaborazione completa su profondità sintetica; primo caso su una scena senza rumore, secondo con il profilo nominale della D435i): un ostacolo di 10 cm a 2,55 m risulta «occupato» in 7 celle su 7 con errore nullo e «libero» in 7 su 7 con +1° (previsione: soglia a 0,67°); uno di 12 cm cambia stato fra 1,0° e 1,5° (previsione 1,12°), uno di 15 cm fra 1,5° e 2,0° (previsione 1,78°). Per una scatola di 15 cm a 2,0–2,15 m, i fotogrammi con almeno una cella dell'impronta «libero» sono 0 su 10 a 0°, 1 su 10 a 1°, 2 su 10 a 2°, 9 su 10 a 2,5° (intervallo di Wilson al 95 %: 0,60–0,98) e 10 su 10 a 3° (0,72–1); la soglia prevista è 2,1–2,3°. *Livello: formula dimostrata; soglie verificate in simulazione con le numerosità indicate (N = 7 celle, N = 10 fotogrammi: campioni piccoli). La proprietà «mai libero su un ostacolo» vale quindi solo a posa nota entro questi margini.*

**Sensore in moto.** I requisiti seguenti quantificano quanto errore di posa relativa tollera la regola che etichetta «mobile» un gruppo: differenza fra due medie di 3 fotogrammi i cui capi distano 13 fotogrammi ($W=13\Delta=0{,}867$ s a 15 Hz), confrontata per asse con $\kappa\sigma$, $\kappa=5\sqrt2/\sqrt3=4{,}08$, dove $\sigma$ è lo scarto tipo della misura per fotogramma ($\sigma_z(\rho)$ nominale sull'asse radiale; $\rho\cdot1^\circ/\sqrt{12}$ sul trasversale, per la cella di 1°).

**Proposizione 9 (falsi «mobile» da deriva di posa).** Se le misure di un gruppo fermo hanno errori indipendenti $\mathcal N(0,\sigma^2)$ e la posa non compensata sposta l'oggetto apparente di $\delta$ fra i due capi, la probabilità di un'etichetta falsa su quell'asse è
$$p(\delta)=Q\!\Big(5-\frac{\delta}{\sigma\sqrt{2/3}}\Big)+Q\!\Big(5+\frac{\delta}{\sigma\sqrt{2/3}}\Big),$$
e $p=10\,\%$ per $\delta=3{,}036\,\sigma$, $p=1\,\%$ per $\delta=2{,}183\,\sigma$.

*Dimostrazione.* La differenza di due medie indipendenti di 3 misure è $\mathcal N(\delta,\,2\sigma^2/3)$; la soglia $\kappa\sigma$ vale $\kappa/\sqrt{2/3}=5$ scarti tipo della differenza. Le due code danno $p(\delta)$; $Q^{-1}(0{,}10)=1{,}2816$ dà $\delta=(5-1{,}2816)\sqrt{2/3}\,\sigma$, e $Q^{-1}(0{,}01)=2{,}3263$ dà l'altro valore. $\square$

Controllo Monte Carlo indipendente ($N=2\cdot10^6$ valutazioni): 0,0999 (Wilson 95 %: 0,0995–0,1003) e 0,0100 (0,0098–0,0101).

**Tabella 7 — Requisiti sulla posa relativa** (soglia: 10 % di falsi salvo dove indicato; i valori a 10 e 30 m assumono un sensore a scansione con 3 cm di rumore radiale e sono fuori dalla portata della camera).

| Requisito | Derivazione | 2 m | 3 m | 10 m | 30 m |
|---|---|---|---|---|---|
| Imbardata relativa su $W=0{,}867$ s | $3{,}036\cdot1^\circ/\sqrt{12}$ | **0,88°** (1,01°/s) a ogni distanza; 0,63° (0,73°/s) per l'1 % | | | |
| Errore di velocità trasversale / radiale (cm/s) | $3{,}036\,\sigma/W$ | 3,5 / 5,3 | 5,3 / 11,9 | 17,7 / 10,5 | 53 / 10,5 |
| Ritardo posa–profondità $\tau$ | $\tau\,\Delta\omega\le0{,}88^\circ$ | gradino di 30°/s: 29 ms; oscillazione ±3° a 1 Hz: 74 ms; ±8° a 1 Hz: 28 ms; ±30° a 0,5 Hz: 5,9 ms (10 % di falsi in media su un periodo) | | | |
| Inclinazione rispetto al suolo (10 % di celle di suolo oltre $y_s$) | $\Delta y+\mathcal N(0,\sigma_y^2)>y_s$, $\sigma_y=\sigma_z h/\sqrt{\rho^2+h^2}$ | 1,70° | 1,03° | 0,37° | 0,13° |
| idem, con ±2,5 cm di oscillazione verticale | | 1,27° | 0,79° | 0,27° | 0,09° |
| Scostamento non modellato perché la regione di previsione copra ≥ 0,90 (da 0,92) | $\chi^2$ non centrale, 2 gradi di libertà: $e\le0{,}48\,\sigma$ | 9,7 cm a 0,67 s; 16 cm a 1 s; 41 cm a 2 s (su 1 s: 4,6° / 3,1° / 0,92° / 0,31°) | | | |
| Quota della fascia di guardia lasciata alla posa (0,10 m) | $0{,}10/\rho$ | 2,9° | 1,9° | 0,57° | 0,19° |
| idem, ritardo che la consuma a 30°/s | $0{,}10/(\rho\,\omega)$ | 95 ms | 64 ms | 19 ms | 6 ms |

Nella riga della regione di previsione $\sigma(t)=\sqrt{0{,}03^2+(0{,}21\,t)^2+q\,t^3/3}$ con $q=0{,}2$ m²/s³ (0,20 m a 0,67 s; 0,33 m a 1 s; 0,84 m a 2 s). La memoria dello stato «libero» su tre fotogrammi resta valida solo se la traslazione propria è sotto mezza cella radiale in due passi, cioè sotto 0,375 m/s. *Livello: dimostrato o calcolato in forma chiusa nel modello d'errore dichiarato (errori gaussiani indipendenti fra fotogrammi); nessuno di questi requisiti è verificato su una piattaforma in moto, e gli errori reali delle sorgenti di posa non sono noti. La proprietà «mai libero dove non è osservato» non dipende dalla posa relativa, perché è calcolata sul singolo fotogramma.*

## 6. Sensori a tempo di volo multizona e LiDAR a scansione su un piano

Il VL53L7CX ha un campo quadrato di 60° × 60° (90° in diagonale) su 8 × 8 zone, e il costruttore dichiara che tre sensori coprono 180° × 60° \cite{st-vl53l7cx}; il VL53L8CX ha 45° × 45° (65° in diagonale) \cite{st-vl53l8cx}. Una zona in 8 × 8 sottende 7,5° (5,625° per il VL53L8CX). A distanza $D$ il lato di una zona è $2D\tan(\text{passo}/2)$:

| | VL53L7CX | VL53L8CX |
|---|---|---|
| Lato di una zona a 2 m; diagonale | **26 cm**; 37 cm | 20 cm; 28 cm |
| Campo intero a 2 m | 2,31 m | 1,66 m |
| Tre sensori affiancati | 180° × 60° | 135° × 45° |
| Sensori necessari per 360° | 6 | 8 |
| Portata in 8 × 8 a 15 Hz, bersaglio bianco: buio / 5 klx | 2,0 m / 0,5 m | 4,0 m / 1,55 m |
| Persona larga 0,5 m a 4 m | 0,95 zone | 1,27 zone |

Tre sensori non danno dunque 360°. Per regola di progetto il canale a tempo di volo è solo un indicatore laterale di prossimità e **non genera mai lo stato «libero»**, per tre ragioni geometriche: (a) una zona restituisce una distanza per un cono largo 26 cm a 2 m, contro celle di 1° × 0,1 m (3,5 cm × 10 cm a 2 m): non distingue suolo visto alla quota attesa da un ostacolo basso; (b) da 1,2 m di altezza la distanza obliqua dal suolo è almeno 1,20 m e vale 2,33 m a $\rho=2$ m, oltre la portata con luce ambiente (0,5 m a 5 klx su bianco, 0,8 m al buio su grigio al 17 % \cite{st-vl53l7cx}); (c) una zona senza bersaglio valido significa «nessun dato», non «vuoto»: solo lo stato 5 del bersaglio è valido al 100 % \cite{st-um3038}. Come copertura, tre sensori da 60° fino a 2 m aggiungono $3\cdot\tfrac12\cdot\tfrac{\pi}{3}\cdot2^2=6{,}28$ m², il 22,2 % del disco di 3 m, al buio; con portata 0,5 m l'1,4 %. Lo scarto tipo per zona, se l'accuratezza dichiarata (±5 %) è letta a 2,7 σ, è l'1,85 %: 3,7 cm a 2 m.

Un LiDAR a scansione su un piano (passo 0,72° o 0,8°, 10 giri al secondo) vede solo ciò che interseca il piano alla quota di montaggio: non gradini, ostacoli bassi, tavoli od oggetti sospesi. Il passo fra due punti a 3 m è 3,8–4,2 cm: 12–13 punti su una persona larga 0,5 m a 3 m, meno di 2 su una gamba di 12 cm a 5 m. Ogni punto ha il proprio istante: a 30°/s il sensore ruota di 3° dentro un giro. *Livello: campi e portate letti dalle schede; il resto verificato per calcolo; interferenza ottica fra proiettore della camera e sensori a tempo di volo non verificata sperimentalmente.*

## 7. Fascia di guardia e distanza di separazione

**Proposizione 10 (fascia di guardia).** Sia una cella dichiarata «libero» sulla base di un'osservazione vecchia al più $\tau_{\text{età}}$, comunicata con latenza $\tau$, e sia $e_{\mathrm{ombra}}$ l'errore massimo di posizione del bordo d'ombra. Se ogni oggetto si muove a non più di $v_{\max}$, un oggetto che al momento dell'osservazione era nell'ombra dista dal bordo stimato, al momento in cui l'informazione è usata, al più
$$g=v_{\max}\,(\tau_{\text{età}}+\tau)+e_{\mathrm{ombra}} .$$

*Dimostrazione.* In un tempo $\tau_{\text{età}}+\tau$ lo spostamento è al più $v_{\max}(\tau_{\text{età}}+\tau)$ dal bordo vero, che dista al più $e_{\mathrm{ombra}}$ da quello stimato. $\square$

Con «libero» valido se visto in uno degli ultimi tre fotogrammi a 15 Hz, $\tau_{\text{età}}=2\Delta=0{,}133$ s; con $\tau=0{,}155$ s (§8) il tempo totale è 0,288 s.

**Tabella 8 — Termini della fascia (m).**

| $v_{\max}$ (m/s) | $v_{\max}\tau_{\text{età}}$ | $v_{\max}(\tau_{\text{età}}+\tau)$ | con $e_{\mathrm{ombra}}=0{,}20$ m |
|---|---|---|---|
| 1,0 | 0,13 | 0,29 | 0,49 |
| 1,4 | 0,19 | **0,40** | 0,60 |
| 2,0 | 0,27 | 0,58 | 0,78 |
| 2,5 | 0,33 | **0,72** | 0,92 |

Una fascia fissa di 0,40 m copre quindi $v_{\max}=0{,}40/0{,}288=1{,}39$ m/s a margine nullo se $e_{\mathrm{ombra}}=0$, e solo 0,69 m/s (0,35 m/s) se i termini si sommano con $e_{\mathrm{ombra}}=0{,}20$ m (0,30 m). A 2,5 m/s il solo termine di moto vale 0,72 m. *Livello: dimostrato (limite cinematico); i valori di $\tau$ e di $e_{\mathrm{ombra}}$ non sono misurati.*

**Confronto con la distanza di separazione della sicurezza industriale.** Nella sorveglianza di velocità e separazione la distanza protettiva somma lo spazio percorso dalla persona durante la risposta del sistema e l'arresto, più termini di intrusione e d'incertezza del sensore, con velocità d'avvicinamento di 1,6 m/s \cite{marvel2017}. Con il sensore fermo e nessun mezzo comandato i termini del mezzo si annullano e resta la forma $S_{\mathrm{sep}}=v_H\,(T_R+T_S)+C+Z_S$, cioè «velocità per tempo più costante». Parametri usati: $T_R=\tau=0{,}155$ s; $T_S=1{,}0$ s (reazione di una persona a un avviso) oppure 0,3 s (arresto automatico); $Z_S=0{,}10$ m; $C=0{,}85$ m (valore attribuito alla norma sul posizionamento dei ripari, non riscontrato sul testo).

**Tabella 9 — $S_{\mathrm{sep}}$ (m).**

| $v_H$ | $T_S=1{,}0$ s | $T_S=0{,}3$ s |
|---|---|---|
| 1,6 m/s | $1{,}6\cdot1{,}155+0{,}95=$ **2,80** | $1{,}6\cdot0{,}455+0{,}95=$ **1,68** |
| 2,0 m/s | $2{,}0\cdot1{,}155+0{,}95=$ **3,26** | $2{,}0\cdot0{,}455+0{,}95=$ **1,86** |

Con 3 m di portata, 1 s di reazione e 0,27 s di conferma la velocità coperta è $(3-0{,}95)/1{,}425=1{,}44$ m/s; a 2,0 m/s la distanza richiesta (3,26 m) supera la portata. Il sistema descritto avvisa e non comanda arresti: il confronto dà un ordine di grandezza e non è una dichiarazione di conformità. *Livello: verificato per calcolo con i parametri dichiarati.*

## 8. Bilancio di latenza

**Tabella 10 — Voci note, dall'evento alla scheda audio** (30 fotogrammi al secondo).

| Tratto | Valore medio | Natura del dato |
|---|---|---|
| Evento → inizio dell'esposizione | 16,7 ms (uniforme fra 0 e 33,3 ms) | calcolo |
| Esposizione → fotogramma disponibile all'applicazione | 95 ms | misura pubblicata dal costruttore su una D435 con il proprio banco (comprende calcolatore e schermo di prova): è una stima per eccesso del solo sensore; media, senza percentili |
| Fotogramma → comando d'uscita | 22 ms | misura su scene sintetiche con codice non ottimizzato |
| Campioni → scheda audio | 21,3 ms | un quanto di 1024 campioni a 48 kHz (valore predefinito del servizio audio) |
| **Somma delle medie** | **155 ms** | |

Mancano, perché senza dato, la sintesi vocale (nulla con suoni preregistrati) e il tratto dalla scheda al suono. La somma è una **media**: la sola prima voce la fa variare fra 138 e 172 ms, e se le altre fossero costanti il 95° percentile sarebbe 170 ms; un requisito espresso come 95° percentile ≤ 150 ms non è quindi soddisfatto dalle sole voci note. Alla stessa maniera si ottengono 99 ms a 60 fotogrammi al secondo e 88 ms a 90 (tratto del sensore 47 e 39 ms). Un secondo dato del costruttore per il tratto del sensore, un unico esempio di circa 71 ms, porterebbe la somma a circa 131 ms. *Livello: somma verificata per calcolo; nessuna voce è misurata sulla catena del prototipo e nessun percentile è disponibile.*

## 9. Figure da disegnare

**Figura A — Sezione verticale (piano $x=0$).** Assi $z$ (0–3,5 m) e $y$ (0–2,2 m); suolo; camera in $(0;\,1{,}2)$ con asse ottico inclinato di 15°; raggio basso a 44° sotto l'orizzontale fino al suolo in $z=1{,}243$ m; raggio alto a 14° sopra l'orizzontale (retta $y=1{,}2+0{,}249z$) con le quote 1,62 / 1,70 / 1,77 / 1,95 m a $z=$ 1,7 / 2,0 / 2,3 / 3,0 m; tratto di suolo cieco $0<z<1{,}243$ tratteggiato; ostacolo di 15 cm a $z=1{,}087$ m con la cima sul raggio basso; pannello a $z_o=1{,}8$ m alto 1,7 m; persona di 1,75 m a $z_p=2{,}3$ m; raggio radente alla cima del pannello; ostacolo basso ($a=0{,}5$ m a 1,5 m) con ombra sul suolo fino a 2,57 m; limite di portata a 3 m; quota della testa 1,70 m con il punto $z=2{,}01$ m.

**Figura B — Pianta.** Disco di 3 m; retta $z=1{,}243$ m (striscia cieca); bordi laterali $x=\pm(0{,}917z+0{,}295)$; arco $\rho_{\min}(\varphi)$ per confronto con l'anello; pannello largo $L$ a $z_o$ con il cuneo d'ombra fra i due raggi di bordo; larghezza dell'ombra $Lz_p/z_o$ a $z_p$; corpo largo $w$ e tratto «tutto nascosto»; fascia di guardia di larghezza $g$ attorno al cuneo; banda stereo $\Delta x$ sul lato sinistro del bordo; griglia polare 1° × 0,1 m accennata.

**Figura C — Copertura dei sensori a tempo di volo.** Pianta con il disco di 3 m, il settore della camera (87°, da 1,24 a 3 m), tre settori da 60° con raggio 2 m (buio) e 0,5 m (5 klx), i 180° coperti e i 180° scoperti; riquadro con la matrice 8 × 8 a 2 m (campo 2,31 m, zona 26 cm) e la sagoma di una persona larga 0,5 m.

## 10. Condizioni generali di validità

Foro stenopeico senza distorsione; suolo piano; posa $(h,\theta)$ nota e camera ferma (per il moto valgono i requisiti del §5); ostacoli opachi che restituiscono profondità (vetro, specchi, nero assorbente e pavimenti lucidi sono fuori dal modello); campi e basi come da scheda, con ±3° di tolleranza; rumore gaussiano in disparità. Tutte le cifre sono conti o simulazioni: la loro validità su un sensore reale non è verificata sperimentalmente.

---

# PARTE II — Provenienza e controlli (per il coordinatore; non entra nell'allegato)

Radice dei percorsi: `.sciame/20261114-1301-percezione-challenge/`. Ricalcoli: `f13-allegato/02-geometria/ricalcoli.py` (numpy 2.5.4, scipy 1.18.1, interprete di `f10-dati/03-infrastruttura/AMBIENTE.md` con `-I -B`), uscita `ricalcoli.txt` (196 righe), rifacimento `bash rifai.sh` (circa 3 s). Lavoro svolto dalle 17:59 alle 18:11 del 14-11-2026 (`date -Is`). La parte I è lunga circa 31 600 caratteri (otto pagine fitte, tabelle comprese): se va accorciata, le prime candidate sono la seconda tabella del §2 e le righe a 10 e 30 m della Tab. 7.

## II.0 Cambi di stato, scostamenti, regole

- **Discordanze trovate (10), elencate in II.2**: nessuna rovescia una conclusione; tre cambiano una cifra della consegna (testa a 1,70 m; requisiti in moto; frazione del disco esatta).
- **Previsioni:** non ne ho registrate prima dei conti (la consegna chiede ricalcoli di cifre già scritte, non prove nuove). Le attese implicite erano le cifre della consegna; dove non tornano è scritto.
- **Indipendenza:** i miei programmi non riusano codice d'origine; condividono con le fonti le formule (che ho riderivato) e i parametri di scheda (che NON ho riaperto sulle schede: li prendo da `parametri_sensori.json`). Vale per errori di conto e di interpolazione, non per errori di lettura delle schede.
- **Contenuto che non è pura estrazione** (da vagliare): la forma chiusa della Prop. 9 (nei file c'è solo il Monte Carlo); la regione esatta del Cor. 1 con i bordi laterali rettilinei; l'area esatta 20,5 %; il 95° percentile «a voci costanti» (170 ms); le tre ragioni (a)–(c) del §6 (nei file «mai libero» è una regola, motivata con portata e risoluzione, non con la distanza obliqua); la riga «≥ 1,78 m» della Tab. 3; la sensibilità di $z_{\min}$. Sono riderivazioni di conti presenti, non misure nuove.
- Nessuna scrittura fuori da `f13-allegato/02-geometria/`; niente git, sudo, rete.

## II.1 Provenienza ed esito del ricalcolo

| Parte I | File d'origine | Mio numero | Esito |
|---|---|---|---|
| Tab. 1 | `f10-dati/02-sensori/MODELLO_SENSORE.md` §1; `parametri_sensori.json` (`camere_profondita`) | — (trascritti) | parametri non riaperti sulle schede |
| Oss. 1 | `parametri_sensori.json`, provenienza di `fx` | 446,8 / 433,0 px; 90,0° × 59,0° | conto mio; vedi II.2-1 |
| $z_{\min}$ 1,24 m | `f3/H-012/04-avversario/ATTACCO.md` p. 3; `f4/H-012/01-avversario/CONTROPROVE.md` r. 15 (1,243); `f7-estensione/13-soluzione/conti.txt` | 1,2426 | torna |
| striscia; 1,69 m a ±44° | `f10-dati/10-catena/CATENA.md` r. 75 e `PREVISIONI.md` r. 64 (z = 1,22 m) | 1,713 m (58°, 43,5°); 1,727 (44°); 1,697 con f = 424 | **non torna con 58°**: II.2-2 |
| ostacolo 15 cm, 1,09 m | `CONTROPROVE.md` r. 15 (1,087); `conti.txt` | 1,0873 | torna |
| tetto 1,2 + 0,25 z; 2,41 m | `f7-estensione/13-soluzione/conti.txt`; `16-verdetto/conti_arbitro.txt` (PA7) | 0,2493; 1,624 / 1,674 / 1,699 / 1,773 / 1,948; 2,406; 3,209 | torna; II.2-3 per «1,70 m» |
| 20,0 % del disco | `f4/H-012/01-avversario/risultati_a12.txt` | 20,02 % (settore d'anello); 20,48 % (esatto) | torna il conto del file; II.2-4 |
| Prop. 3 esempi | `f7-estensione/13-soluzione/conti.txt` (PA2) | 2,27; 2,57; 9,00 | torna |
| Prop. 4, Tab. 3 | `conti.txt` (ultime 9 righe); `conti_arbitro.txt` (PA7); `f7-estensione/13-soluzione/DECISIONE.md` §0; `16-verdetto/VERDETTO_ESTENSIONE.md` r. 41 | 1,606 / 1,563; 1,607–1,674; 1,624 / 1,674 | torna |
| Prop. 5, Tab. 4 | `conti_arbitro.txt` (PA6); `VERDETTO_ESTENSIONE.md` r. 41 e 51 | 0,54–0,90; 1,41–2,26 | torna |
| Prop. 6, Tab. 5 | `MODELLO_SENSORE.md` §1 «Buchi» p. 2 e tabella; `controlla_parametri.py` | 19,0 cm / 26,9 px; 10,0 / 14,1; 10,0 / 13,7; bordo 20,1 e 10,6 px; 0,158 s | torna; dimostrazione mia (il file la dà come «C, geometria») |
| Prop. 7, Tab. 6 | `MODELLO_SENSORE.md` §1; `f3/H-012/02-validazione/VERIFICA.md` §4 «Rumore R(z)» | tutti i valori della tabella | torna (il file non dà la colonna a 1 m: aggiunta) |
| quantizzazione 7 e 13 mm | `MODELLO_SENSORE.md` §1 | 6,98; 13,27 (Gemini 13,70) | torna |
| misura di terzi 1,83 cm; 1,21 | `MODELLO_SENSORE.md` §1; `controlla_parametri.py` | 1,83; 1,21; 0,097 px | torna |
| incidenza 60° a 2,08 m; 68° | `MODELLO_SENSORE.md` §1 «Incidenza» | 2,078; 68,2° | torna |
| 5 px = 3,4 cm a 3 m | `f7-estensione/05-esperto-dominio/CONSEGNA.md` C6; `risultati_osservabilita.txt` | 3,36 cm (f = 446,8); 3,54 (f = 424) | torna con 87°; II.2-1 |
| Prop. 8; 1° a 2,8 m | cifra data dalla consegna (non ho trovato il paragrafo d'origine; coerente con `f7-estensione/14-attacco/PREVISIONI.md` r. 46) | 4,90 cm | torna |
| 2° → suolo «occupato» da 2 m | `f3/H-012/02-validazione/VERIFICA.md` r. 7 («assetto 2° → 2,0 m») | 1,985 m | torna |
| ostacolo di 10 cm → «suolo» | `f10-dati/22-avversario/ATTACCO_DATI.md` A1; grezzo `uscite/a1_posa.txt` (A1c, A1d) | soglie 0,67° / 1,12° / 1,78° a 2,55 m; 2,11–2,27° scatola | i conteggi sono ritrovati nel grezzo; le soglie previste cadono dentro gli intervalli osservati |
| regola di mobilità | `f6-specializzazione/02-slam/MOTO_PROPRIO.md` §0 e §3; `bilancio_posa.py` r. 1–50 | $\kappa$ = 4,0825; 1,179° | torna; II.2-9 |
| imbardata 0,87° su 0,87 s | `MOTO_PROPRIO.md` §3 (Q1); `risultati.txt` S1 | 0,8764° (1,011°/s) | torna |
| «≤ 0,7° per l'1 %» | idem | 0,630° sulla finestra (0,727°/s) | **non torna**: II.2-5 |
| velocità (Q2) | `risultati.txt` S1 | 3,5/5,3; 5,3/11,9; 17,7/10,5; 53/10,5 | **scarto 2–8 %**: II.2-6 |
| sincronia (Q3) | `risultati.txt` S3 | 29,2; 74,4; 27,7; 5,9 ms | scarto 1–6 % (file: 30; 73; 27; 5,6): II.2-6 |
| inclinazione (Q4) | `risultati.txt` S5 | 1,705 / 1,025 / 0,375 / 0,131; 1,268 / 0,789 / 0,265 / 0,089 | **a 10 m non torna** (file 0,32 e 0,24): II.2-6 |
| area prevista (Q5) | `risultati.txt` S6 | 0,482 σ; 9,7 / 16,1 / 40,6 cm | **scarto 5 %** (file 0,46 σ; 9 / 15 / 39): II.2-6 |
| fascia (Q6); 0,375 m/s | `risultati.txt` S7; `MOTO_PROPRIO.md` §1 | 2,86 / 1,91 / 0,57 / 0,19°; 95 / 64 / 19 / 6 ms; 0,375 | torna |
| §6 campi, portate | `MODELLO_SENSORE.md` §2–3; `f1/985ccd9bca46/CONSEGNA.md` §2; `f11-documentazione/sez-d/SEZIONE.md` §D.3 | 26,2 / 19,7 cm; 37,1 / 27,8; 2,31 / 1,66 m; 0,95 / 1,27 zone; 22,2 %; 1,4 %; 3,7 cm; 13,3 / 11,9 punti | torna (26 cm: valore già corretto in `f11-documentazione/verifica-1/VERIFICA.md` a1; `MODELLO_SENSORE.md` scrive ancora 13 e 10 cm: II.2-7) |
| Prop. 10, Tab. 8 | `f5/02-audit/AUDIT.md` p. 3; `f4/H-012/09-arbitro/VERDETTO.md` r. 62; `f6-specializzazione/03-avversario/ATTACCO_SPECIALIZZAZIONE.md` S3 | 0,288 s; 0,404; 0,721; 1,387 m/s; 0,69; 0,35 | torna |
| Tab. 9 | `f9-preproposta/06-esperto-dominio/CONSEGNA.md` §6; `f11-documentazione/sez-e/SEZIONE.md` r. 72 e 76 | 2,798; 1,678; 3,260; 1,860; 1,439 m/s | torna |
| Tab. 10 | `f3/H-012/02-validazione/VERIFICA.md` §3c | 155,0 ms | torna; II.2-8 |

## II.2 Discordanze fra file (e fra file e consegna)

1. **Focale e campo non sono coerenti.** $f=424$ px equivale a 90° × 59°, non a 87° × 58° (che danno 446,8 e 433,0 px). I file usano l'una o l'altra: «1 px = 4,7 mm a 2 m» (`MODELLO_SENSORE.md`, f = 424) contro «6,7 mm a 3 m» (`f7…/05-esperto-dominio`, f = 447). Per la Gemini 335, $f=410{,}7$ px a 848 px dà 91,8°, non 90°. Nella parte I ho dichiarato la scelta (Oss. 1). Da decidere una volta per l'allegato.
2. **$z_{\min}$: 1,24 m (f3, f4, f7; campo di 58°) contro 1,22 m (f10, catena simulata; coerente con f = 424 px, 59,0°).** Il «1,69 m a ±44°» della consegna viene da 1,22/cos 44° = 1,697 (troncato). Con 58° il valore è 1,73 m a 44° (1,71 a 43,5°). Nella parte I: formula e 1,71 m, più il caso f = 424.
3. **«La testa a 1,70 m sotto 2,41 m non è vista» (consegna) mescola due cifre:** nei file 2,41 m è la distanza per la quota **1,80 m** (`conti.txt`, `TORNEO.md`); per 1,70 m il conto dà **2,01 m**. Parte I: tabella con entrambe.
4. **20,0 % è il settore d'anello di 87° fra $\rho$ = 1,24 e 3 m** (`a09_a10_a12.py`), che ignora sia la striscia sia l'allargamento laterale del campo sul suolo; la regione esatta del foro stenopeico dà 20,5 % (il settore tagliato dalla retta, 19,0 %). Parte I: entrambe.
5. **Q1 all'1 %:** `MOTO_PROPRIO.md` scrive «≤ 0,7° per l'1 %»; `risultati.txt` dà 0,719 **°/s**, cioè 0,62° sulla finestra (forma chiusa: 0,630°, 0,727°/s). Il file confonde tasso e angolo.
6. **Q2–Q5: le soglie del file vengono da un'interpolazione lineare su griglie rade di curve ripide** (`incrocio()` in `bilancio_posa.py`), che sposta la soglia verso il basso. Forma chiusa: Q2 3,5/5,3 – 5,3/11,9 – 17,7/10,5 (file 3,4/5,2 – 5,2/11 – 17/10; a 30 m il file dice «oltre il massimo provato», il conto dà 53 cm/s); Q4 a 10 m 0,375° e 0,265° (file 0,32° e 0,24°), a 2 m 1,70° (file 1,68°); Q5 0,482 σ (file 0,46 σ: inoltre il suo campione dà 0,918 a scostamento nullo dove il valore esatto è 0,920). Q3: 29,2 / 74,4 / 27,7 / 5,9 ms contro 30 / 73 / 27 / 5,6 (il file campiona 15 o 30 fasi, io la media continua; per il gradino il file misura la frazione su una finestra di 2 s, io la singola valutazione). Nella parte I ho messo i valori in forma chiusa. Le conclusioni qualitative del file non cambiano.
7. **Lato della zona a 2 m:** `MODELLO_SENSORE.md` §2 scrive ancora 13 e 10 cm (mezza zona); corretto in f11 a 26 e 20 cm. Confermo 26,2 e 19,7 cm.
8. **Latenza del sensore: 95 ms (`VERIFICA.md` §3c) contro 70 ms nominale / 120 limite (`MODELLO_SENSORE.md` «Tempo»).** Fonti diverse; inoltre `RIFERIMENTI.md` classifica la fonte dei 95 ms «dato diverso» (misura il banco di prova, non il solo sensore; modi 848 × 100). Parte I: 155 ms con 95, e circa 131 ms con 71, dicendo che cosa è ciascuno. I «22 ms» sono 20,1 + 2,0 da due programmi diversi, non riletti da me nel grezzo.
9. **Regola di mobilità:** `SOLUZIONE_V2.md` B3 scrive soglia $5\sigma\sqrt2$; il codice usato nei conti di posa divide per $\sqrt3$ e usa sull'asse trasversale $\rho\cdot1^\circ/\sqrt{12}$ (lo segnala lo stesso `MOTO_PROPRIO.md` §0). Ho seguito il codice, come il file. Il fascicolo sul tracciamento deve usare la stessa forma.
10. **Campo della Gemini 335:** 90° × 60° a 848 × 480 (`parametri_sensori.json`, dalla scheda) contro 90° × 65° (`SOLUZIONE_V2.md` B1, pagina del prodotto, 1280 × 800). Parte I: entrambe, con le conseguenze geometriche.

## II.3 Citazioni

- **Usate** (stato «verificata» per il dato): `realsense-bkm-taratura` (σ_d < 0,1 e 0,08 px); `ahn2019` (formula di σ_z; 4,3 e 4,1 cm; lato della banda — per quest'ultimo l'elenco riporta la frase sul bordo sinistro del bersaglio, da ricontrollare che sostenga «lato sinistro del bordo»); `st-vl53l7cx` (60° × 60°, 90°, 180° × 60°, 2,0 m, 0,5 m a 5 klx, 0,8 m su grigio 17 %); `st-vl53l8cx` (45° × 45°, 65°); `st-um3038` (stato 5 = 100 %); `marvel2017` (concetto, 1,6 m/s; la formula **non** è stata riletta simbolo per simbolo: per questo nella parte I la descrivo a parole e non la cito come equazione della fonte).
- **Verificate ma senza chiave nel `.bib`** (frasi lasciate senza citazione; propongo di aggiungere le voci): `realsense-d455` (87° × 58°, 95 mm, < 2 % a 4 m), `realsense-d400-accuratezza` (≤ 2 % fino a 2 m / 4 m, riempimento ≥ 99 %), `realsense-taratura-profondita` (errore ∝ distanza², 848 px, 50 mm, 0,08), `orbbec-gemini-335` (50 mm, ≤ 1,5 % a 2 m, 90° × 65°), `slamtec-rplidar-c1` (0,72°, 5 kHz, 10 Hz), `pipewire-conf` (1024 / 48000), `realsense-filtri-post` (persistenza, riempimento).
- **Non usate perché non verificate per il dato:** `realsense-d400-scheda` (verificata, ma «base stereo e RMS non ricontrollati»); `orbbec-gemini-330-scheda` (verificati solo versione e lunghezza d'onda: campo a 848 × 480, intrinseci, grafico del rumore no); `iso-13855` (solo riassunto di ricerca: C = 0,85 m e il «2,0 m/s raccomandato» non verificati); `iso-ts-15066` (non raggiungibile); `realsense-alta-velocita-d435` («dato diverso», e senza chiave); `ldrobot-ld19-scheda` (aperta solo da chi la cita; 0,8° è derivato da 360°/450); `dxomark-rapporto-camera3d`. Portate del VL53L8CX in 8 × 8 al buio (4,0 m) e a 5 klx (1,55 m): la seconda è verificata, ma nella tabella non ho messo la citazione per riga; l'accuratezza ±5 % a 2,7 σ non è fra i dati verificati di nessuna voce.

## II.4 Che cosa l'integrazione in corso potrebbe cambiare

- **Fascia di guardia:** `f12-integrazione/01-soluzione/SOLUZIONE_V3.md` §1.7 scrive «fascia ≥ 0,20 m + mezza larghezza + v_max·(età + latenza)» e dichiara l'invariante sul «libero» **senza memoria** (`TABELLA_CORREZIONI.md` r. 19 e 30): cambierebbero $\tau_{\text{età}}$ (da 0,133 s a 0) e comparirebbe il termine di mezza larghezza del corpo; la Tab. 8 va allora rifatta con quei termini (il programma li ha come parametri).
- **Zona valutata:** la striscia al posto dell'anello è già recepita (`TABELLA_CORREZIONI.md` r. 186); il valore 1,22 o 1,24 m dipende dalla scelta II.2-1.
- **Regola di mobilità e soglia di quota:** se cambiano $\kappa$, la finestra o $y_s$, la Tab. 7 e il §5 scalano (forme chiuse nel programma).
- **Scena dimostrativa:** altezza e larghezza del pannello (`f12-integrazione/05-schermo/SCHERMO_E_DEMO.md` r. 112–119 usa già 1,5–1,8 s e 1,4–2,3 s): Tab. 3 e 4 restano valide come formule.

## II.5 Che cosa manca per completare l'area

- La scelta unica di $f$ e del campo (II.2-1), poi una passata sulle cifre laterali.
- Le sette voci da aggiungere al `.bib`, e una lettura di `iso-13855` (o la rinuncia a $C=0{,}85$ m e a 2,0 m/s).
- Il paragrafo d'origine di «1° a 2,8 m ≈ 5 cm»: non trovato nei file (il conto torna).
- Non ho riaperto le schede (campi, basi, portate): la tabella 1 è trascritta dal JSON, con la sua provenienza.
- Non ricalcolati perché fuori dal perimetro o privi di formula: «0,68 m² su 0,98 m² dell'anello cieco» coperti da un ToF puntato in basso (`risultati_a12.txt`; per di più riferito all'anello, non alla striscia); i falsi per sorgente di posa (`risultati.txt` S4, ipotesi sugli errori delle sorgenti); la soglia allargata con la σ di posa (S2).
- Le figure sono descritte, non disegnate.
