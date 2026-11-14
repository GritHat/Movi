# Fascicolo: metodo di valutazione e risultati sperimentali

<!-- Due parti. La PARTE I entra nell'allegato; la PARTE II è per chi compone l'allegato e non vi entra. -->

# PARTE I — Contenuto per l'allegato

## Simboli aggiunti alla notazione comune

Oltre alla notazione comune ($\Delta$, $\tau_{occ}$, $O(t)$, $\Omega(t)$, $\Pi(t)$, $\mathcal R_\alpha(t)$, $q$, $N$) si usano: $k$ numero di eventi contati su $N$ prove; $\hat p = k/N$; $z$ quantile normale ($z = 1{,}960$ al 95 % a due code); $[\ell^-, \ell^+]$ intervallo di Wilson; $m$ numero di celle (combinazioni di condizioni) giudicate insieme; $n_c$ numerosità dell'insieme di taratura; $P_D$ probabilità di rilevamento per fotogramma; $e_\Omega$ errore con segno del bordo dell'ombra stimata (negativo: ombra stimata più stretta della vera); $\rho$ correlazione fra passaggi della stessa persona; $G_1, G_2, G_3$ le tre disposizioni di prova (ombra stimata di 1,36 m², 7,82 m² e 14,70 m²; $G_1$ ha un pannello largo 1 m, $G_3$ uno largo 2 m).

Ogni risultato porta il **livello di prova** — *dimostrato* nel modello dichiarato; *verificato per calcolo*; *verificato in simulazione* con $N$ e intervallo; *misurato su dati pubblici*; *non verificato sperimentalmente* — e il **tipo di dato**: (I) modello ideale del sensore: posizioni al suolo con rumore gaussiano, nessuna immagine di profondità; (II) profondità simulata dai parametri delle schede tecniche di tre camere a stereo attivo; (III) dati pubblici. **Nessun risultato di questo capitolo è stato ottenuto su un sensore fisico**: tutte le prove sono simulazioni, calcoli, o elaborazioni di dati pubblici.

## 1. Le misure

L'unità statistica è il **passaggio**: una persona attraversa il campo, scompare dietro un ostacolo fermo e (di norma) ricompare. Un passaggio è *valido* se la traccia ha ricevuto almeno 4 misure prima di scomparire. I fotogrammi di uno stesso passaggio non sono indipendenti: gli intervalli si calcolano sui passaggi, salvo dove è detto.

**Definizione 1 (continuità).** (a) *Per ciclo*: quota dei cicli senza osservazione del soggetto in cui il sistema emette una regione $\mathcal R_\alpha(t) \neq \emptyset$; denominatore: i cicli senza osservazione dei passaggi validi. (b) *Per passaggio*: quota dei passaggi con almeno un *vuoto*, cioè almeno un ciclo senza osservazione e senza regione; denominatore: i passaggi validi.

**Definizione 2 (copertura della regione).** Per un tempo trascorso dall'ultima osservazione $\tau_{occ} = \tau$ e un comportamento $b$, la copertura è
$$c(\tau, b) = \frac{\#\{\text{passaggi di tipo } b \text{ ancora nascosti a } \tau \text{ con il soggetto in } \mathcal R_\alpha\}}{\#\{\text{passaggi di tipo } b \text{ ancora nascosti a } \tau\}} .$$
Il denominatore comprende **tutti** i passaggi ancora nascosti, anche quelli in cui il soggetto è uscito dalla portata di 3 m senza essere rivisto: è la scelta prudente. Il denominatore alternativo («ancora nascosti *e* dentro l'area osservata») è il solo misurabile dal vivo con un'occlusione virtuale; dà valori uguali o maggiori e differisce in modo sensibile solo in $G_1$ (esempio: stessa cella, 461 su 513 contro 461 su 480). Il livello dichiarato è uno solo, $1-\alpha = 0{,}90$. Una *cella* è una terna (disposizione, comportamento, $\tau$), con $\tau \in \{0{,}5;\,1;\,2;\,3\}$ s. I comportamenti *sul percorso* sono cinque: prosegue, rallenta, si ferma, torna indietro, sosta lunga; *fuori dal percorso*: svolta, esce dal lato lontano.

**Definizione 3 (area relativa).** $|\mathcal R_\alpha(\tau)| / |\Omega|$, media sui passaggi ancora nascosti a $\tau$. Una copertura alta con area relativa vicina a 1 dice «è dietro l'ostacolo», non «dove».

**Definizione 4 (errore del punto).** Distanza euclidea al suolo fra il punto mostrato e la posizione vera a $\tau$; si riportano mediana e 90º percentile sui passaggi ancora nascosti.

**Definizione 5 (sicurezza).** (a) Quota degli istanti con il soggetto nascosto il cui centro sta fuori dall'area d'avviso $\Pi(t)$; denominatore: gli istanti campionati con il soggetto nascosto. (b) Numero di celle della mappa dichiarate «libero» e contenute per intero nell'ombra vera $\Omega(t)$; denominatore: celle interamente in ombra vera × fotogrammi (celle·fotogramma). La soglia per entrambe è zero.

**Definizione 6 (identità al ritorno).** Quota dei passaggi in cui, alla ricomparsa, la traccia ha lo stesso identificativo di prima e nessuna associazione intermedia a un altro oggetto; denominatore: i passaggi con ricomparsa.

**Definizione 7 (falsi «in movimento»).** Quota dei passaggi in cui un oggetto fermo riceve almeno un'etichetta «in movimento»; denominatore: i passaggi.

**Definizione 8 (costo per ciclo).** Tempo d'orologio di un ciclo della catena di elaborazione su un solo filo di CPU; si riportano media, 95º percentile, massimo e numero di cicli oltre il periodo $\Delta = 1/15$ s $= 66{,}7$ ms.

**Regola d'esito.** Una soglia $s$ su una quota è *rispettata* se $\ell^- > s$, *violata* se $\ell^+ < s$, altrimenti *non decisa*. Le soglie e le numerosità delle prove principali sono state fissate prima dei lanci; dove un parametro è stato scelto dopo aver visto i dati lo si dice nella riga.

## 2. Gli intervalli

**Intervallo di Wilson.** Per $k$ eventi su $N$ prove indipendenti, con $\hat p = k/N$,
$$\ell^\pm = \frac{\hat p + \dfrac{z^2}{2N} \pm z\sqrt{\dfrac{\hat p(1-\hat p)}{N} + \dfrac{z^2}{4N^2}}}{1 + \dfrac{z^2}{N}} .$$
*Esempio svolto* ($k = 826$, $N = 879$): $\hat p = 0{,}93970$; $z^2 = 3{,}8415$; $z^2/N = 0{,}004370$; centro $(0{,}93970 + 0{,}002185)/1{,}004370 = 0{,}93779$; radicando $0{,}93970\cdot0{,}06030/879 + 3{,}8415/(4\cdot 879^2) = 6{,}4464\cdot10^{-5} + 0{,}1243\cdot10^{-5} = 6{,}5707\cdot10^{-5}$; semiampiezza $1{,}960 \cdot 0{,}008106 / 1{,}004370 = 0{,}01582$; quindi $[0{,}9220;\ 0{,}9536]$.

**Proposizione 1 (zero eventi su $N$).** Se in $N$ prove indipendenti con probabilità d'evento $p$ si osservano 0 eventi, allora: (i) il limite superiore esatto a una coda al 95 % è $p^+ = 1 - 0{,}05^{1/N}$; (ii) $p^+ < 3/N$ (regola del tre); (iii) l'estremo superiore di Wilson a due code vale $z^2/(N+z^2) = 3{,}84/(N+3{,}84)$.

*Dimostrazione.* (i) La probabilità di 0 eventi è $(1-p)^N$, decrescente in $p$; i valori di $p$ non rifiutati al livello 0,05 sono quelli con $(1-p)^N \ge 0{,}05$, cioè $p \le 1 - 0{,}05^{1/N}$. (ii) $1 - 0{,}05^{1/N} = 1 - e^{-x}$ con $x = -\ln(0{,}05)/N = 2{,}9957/N$; poiché $1 - e^{-x} < x$ per $x>0$, $p^+ < 2{,}9957/N < 3/N$. (iii) Con $\hat p = 0$ il centro vale $\frac{z^2/2N}{1+z^2/N}$ e la semiampiezza $\frac{z\sqrt{z^2/4N^2}}{1+z^2/N}$, uguale al centro: $\ell^- = 0$ e $\ell^+ = \frac{z^2/N}{1+z^2/N} = \frac{z^2}{N+z^2}$. $\blacksquare$

*Valori* (verificati per calcolo): $N = 90$: 3,27 % esatto, 3,33 % regola del tre, 4,09 % Wilson; $N = 131$: 2,26 %, 2,29 %, 2,85 %; $N = 400$: 0,746 %, 0,750 %, 0,951 %; $N = 2716$: 0,110 %, 0,110 %, 0,141 %; $N = 24\,835$: 0,0121 %, 0,0121 %, 0,0155 %. Per simmetria, $N$ successi su $N$ danno il limite inferiore $1 - 3/N$ (a una coda) e $N/(N+z^2)$ (Wilson): con 400 su 400, 99,25 % e 99,05 %. Nelle tavole del §6 l'intervallo è sempre quello di Wilson a due code; il limite a una coda, più stretto, è citato dove serve.

**Proposizione 2 (dichiarazioni «in tutte le celle»).** Se si giudicano insieme $m$ celle e ciascun intervallo è costruito al livello $1 - 0{,}05/m$, cioè con $z_m = \Phi^{-1}\!\big(1 - \tfrac{0{,}05}{2m}\big)$, la probabilità che almeno un intervallo non contenga il proprio valore vero è al più 0,05, qualunque sia la dipendenza fra le celle.

*Dimostrazione.* Detto $E_j$ l'evento «l'intervallo $j$ non copre», $P(E_j) \le 0{,}05/m$ e $P(\bigcup_j E_j) \le \sum_j P(E_j) \le 0{,}05$ (disuguaglianza di Boole). $\blacksquare$

*Valori:* $z_{12} = 2{,}865$, $z_{15} = 2{,}935$, $z_{45} = 3{,}261$, $z_{60} = 3{,}342$. Con 90 su 100 l'intervallo passa da $[0{,}826; 0{,}945]$ ($m=1$) a $[0{,}782; 0{,}958]$ ($m = 12$). Per zero eventi in ciascuna di $m = 3$ disposizioni il limite a una coda diventa $1 - (0{,}05/3)^{1/N} \approx 4{,}09/N$.

**Osservazione 1 (unità d'analisi).** Un conteggio «0 su $M$» fatto su fotogrammi, istanti o celle·fotogramma non autorizza il limite $3/M$: le unità dello stesso passaggio o della stessa sequenza sono dipendenti. Il limite si calcola sul numero di passaggi o di sequenze; il conteggio fine resta come descrizione dell'estensione del controllo.

## 3. Numerosità e lettura di un tabellone «dentro $k$ su $n$»

**Prova esatta a una coda.** Per distinguere una copertura $p_0$ da una $p_1 > p_0$ si rifiuta $H_0\!: p = p_0$ quando $k \ge c$, con $c$ il minimo intero tale che $P(K \ge c \mid p_0) \le \alpha$, $K \sim \mathrm{Bin}(n, p_0)$; la potenza è $P(K \ge c \mid p_1)$. (Per $p_1 < p_0$ la regione di rifiuto è $k \le c$.) Poiché $c$ è intero, la potenza in funzione di $n$ è a dente di sega: si riportano il primo $n$ che raggiunge la potenza voluta e l'$n$ *stabile*, dal quale la raggiunge ogni $n$ maggiore.

| Confronto ($H_0$ contro alternativa) | $\alpha$, potenza | primo $n$ (soglia) | $n$ stabile |
|---|---|---|---|
| 0,90 contro 0,80 | 0,05; 0,80 | 78 ($k \le 65$) | **89** |
| 0,80 contro 0,90 | 0,05; 0,80 | 82 ($k \ge 72$) | 94 |
| 0,80 contro 0,90 | 0,10; 0,90 | 86 ($k \ge 74$) | 98 |
| 0,90 contro 0,85 | 0,05; 0,80 | 270 ($k \le 234$) | **299** |
| 0,85 contro 0,90 | 0,05; 0,80 | 281 ($k \ge 249$) | 304 |
| 0,90 contro 0,95 | 0,05; 0,80 | 179 ($k \ge 168$) | **203** |
| 0,95 contro 0,90 | 0,05; 0,80 | 169 ($k \le 155$) | 191 |

(Verificato per calcolo, binomiale esatta. L'approssimazione normale dà 83, 282 e 149.) Servono dunque circa **90 passaggi per cella** per distinguere 0,90 da 0,80, circa **300** per distinguerlo da 0,85 e circa **200** da 0,95. Con $n = 30$ la prova di $H_0\!: p = 0{,}90$ contro 0,80 rifiuta per $k \le 23$ (livello vero 0,026) e ha potenza 0,39: trenta passaggi non distinguono 0,90 da 0,80.

**Che cosa dice un conteggio dal vivo.** (Verificato per calcolo.)

| Osservato | Wilson 95 % | Esatto 95 % (a due code) | Lettura |
|---|---|---|---|
| 9 su 10 | 0,596–0,982 | 0,555–0,997 | compatibile sia con 0,60 sia con 0,98 |
| 27 su 30 | 0,744–0,965 | 0,735–0,979 | «fra 0,74 e 0,97»: non esclude 0,80 |
| 30 su 30 | 0,887–1 | 0,884–1 | «almeno 0,89», non «sempre» |
| 46 su 50 | 0,812–0,969 | 0,808–0,978 | minimo su 50 per dire «almeno 0,80» |
| 90 su 100 | 0,826–0,945 | 0,824–0,951 | |

Una regione che copre davvero solo 0,80 mostra «almeno 9 su 10» nel 37,6 % delle dimostrazioni da dieci passaggi; una che copre 0,90 lo mostra nel 73,6 %. Con copertura vera 0,90, «30 su 30» capita nel 4,2 % dei casi: un tabellone senza errori su trenta prove è più probabile con una regione troppo larga che con una tarata. La semiampiezza di Wilson scende a $\pm 0{,}10$ con 38 passaggi se la quota osservata è 0,90, con 51 se è 0,85 e con 93 nel caso peggiore ($\hat p = 0{,}5$); con 50 passaggi per riga si chiude entro $\pm 0{,}10$ con probabilità 0,88 se il valore vero è 0,90 (0,52 se è 0,85; con 60 passaggi, 0,89).

**Regole di lettura del tabellone.** (1) Si mostra «dentro $k$ su $n$» con l'intervallo, mai una percentuale sola; sotto $n = 10$ solo i conteggi. (2) L'evento contato è «la persona è dentro $\mathcal R_\alpha$ a $\tau_{occ} = 1$ s e a 2 s» (Definizione 2), non «la prima misura dopo la ricomparsa cade vicino al punto previsto»: le due grandezze divergono (in simulazione, con l'ombra stimata 20 cm più stretta e senza margine, la seconda segna 1216 su 1244 = 0,977 mentre la cella peggiore della prima vale 0,68). (3) I cicli in cui la regione coincide con quasi tutta l'ombra si contano a parte. (4) Il comportamento si dichiara prima della camminata; $n$ si fissa prima; nessun azzeramento; i passaggi usati per la taratura sono esclusi. (5) Passaggi della stessa persona si somigliano: con $m$ passaggi a testa e correlazione $\rho$ la numerosità efficace è $n/(1+(m-1)\rho)$; con $m = 10$ e $\rho = 0{,}2$, 40 passaggi ne valgono 14. La cifra descrive quelle persone e quell'installazione.

## 4. La taratura della regione per quantili

**Costruzione.** Per ogni fascia di $\tau_{occ}$ si calcola, su $n_c$ passaggi di taratura, un punteggio di non conformità $s_i$ (per esempio la distanza fra la posizione vera e il punto previsto a quel $\tau$) e si prende come soglia la statistica d'ordine $s_{(k)}$ con $k = \lceil (1-\alpha)(n_c+1) \rceil$; la regione $\mathcal R_\alpha$ è l'insieme delle posizioni con punteggio $\le s_{(k)}$. Se $k > n_c$ la soglia è infinita.

**Proposizione 3 (garanzia marginale sotto scambiabilità).** Se i punteggi $s_1, \dots, s_{n_c}, s_{n_c+1}$ (taratura più il passaggio nuovo) sono scambiabili, allora $P\big(s_{n_c+1} \le s_{(k)}\big) \ge 1 - \alpha$; se inoltre sono quasi certamente distinti, $P\big(s_{n_c+1} \le s_{(k)}\big) = k/(n_c+1) \le 1 - \alpha + 1/(n_c+1)$.

*Dimostrazione.* Per scambiabilità e assenza di parità, il rango di $s_{n_c+1}$ fra gli $n_c+1$ punteggi è uniforme su $\{1,\dots,n_c+1\}$. L'evento $s_{n_c+1} \le s_{(k)}$ (con $s_{(k)}$ calcolata sui soli $n_c$ di taratura) equivale a «il rango di $s_{n_c+1}$ è $\le k$», di probabilità $k/(n_c+1)$; e $\lceil (1-\alpha)(n_c+1)\rceil/(n_c+1) \in [1-\alpha,\ 1-\alpha+1/(n_c+1))$. Con parità l'uguaglianza diventa $\ge$. $\blacksquare$ La garanzia è la copertura *marginale* della previsione conforme a insieme separato \cite{angelopoulos2021}: è una media sulla popolazione da cui vengono taratura e prova.

**Proposizione 4 (copertura realizzata con una taratura data).** Se i punteggi sono indipendenti con la stessa distribuzione continua $F$, la copertura condizionata all'insieme di taratura, $C = F(s_{(k)})$, ha distribuzione $\mathrm{Beta}(k,\ n_c+1-k)$.

*Dimostrazione.* $U_i = F(s_i)$ sono uniformi indipendenti su $[0,1]$ e $F$ è monotona, quindi $F(s_{(k)}) = U_{(k)}$, la $k$-esima statistica d'ordine di $n_c$ uniformi, che è $\mathrm{Beta}(k, n_c+1-k)$. $\blacksquare$

*Valori* (verificati per calcolo, livello 0,90): con $n_c = 30$ ($k = 28$) il 5º percentile della copertura realizzata è 0,805; con $n_c = 100$ ($k = 91$) è 0,848; il primo $n_c$ per cui la copertura realizzata supera 0,85 con probabilità 0,95 è 68 (stabilmente da 110); sotto $n_c = 9$ si ha $k > n_c$ e la regione è tutto lo spazio. Una simulazione con 400 ripetizioni ha ridato 0,803 ($n_c = 30$) e 0,851 ($n_c = 100$).

**Osservazione 2 (dove la garanzia non vale).** La Proposizione 3 non dice nulla (a) sulla copertura *per comportamento*, perché una media $\sum_b w_b\, c_b \ge 1-\alpha$ non implica $c_b \ge 1-\alpha$ per ogni $b$; (b) su una popolazione diversa da quella della taratura, perché cade la scambiabilità. Controesempi in simulazione (modello ideale, tipo I):

| Condizione | Copertura della regione «al 90 %» |
|---|---|
| soglia unica per fascia di tempo, popolazione della taratura, nel complesso | 0,897–0,907 da 0,5 a 5 s |
| stessa soglia, solo chi torna indietro | **0,455** a 2 s; 0,307 a 3 s |
| taratura su una miscela 90/10/0/0 (prosegue / si ferma / torna / svolta), prova su 50/20/20/10 | 0,72 / **0,66** / 0,64 a 1 / 2 / 3 s |
| regione adottata (§6.3), camminatori meno regolari di quelli della taratura (variabilità di velocità 15 % anziché 6 %, di rotta 8° anziché 3°), disposizione $G_3$ | 323/342 = 0,944; 283/339 = 0,835 [0,792–0,871]; 226/282 = 0,801 [0,751–0,844] fino a 1 / 2 / 3 s |

**Proposizione 5 (pavimento per comportamento peggiore).** Se per ciascun comportamento $b$ di un insieme finito $B$ si tara una soglia $s^{(b)}$ con la costruzione sopra, e si adotta $s^\ast = \max_{b \in B} s^{(b)}$, allora per ogni $b \in B$ la copertura sul comportamento $b$ è almeno $1-\alpha$, sotto scambiabilità *dentro* ciascun comportamento.

*Dimostrazione.* La regione è monotona nella soglia: $\{s \le s^{(b)}\} \subseteq \{s \le s^\ast\}$; si applica la Proposizione 3 a ogni $b$. $\blacksquare$ Vale solo per i comportamenti di $B$ e per quella popolazione.

*Costo in area* (verificato in simulazione, tipo I). Un disco attorno alla previsione a velocità costante, con il raggio pari al massimo su quattro comportamenti, ha area 1,8 / 4,4 / 4,8 / 4,2 volte quella del cerchio al 90 % del filtro a 0,5 / 1 / 2 / 3 s. Nel sistema, il disco con il raggio massimo sui comportamenti sul percorso, ritagliato sull'ombra, occupa a 2 e 3 s una quota dell'ombra di 0,99 e 1,21 in $G_2$ e di 0,79 e 1,12 in $G_3$ (valori sopra 1: la regione comprende il margine attorno all'ombra); la regione adottata, costruita da una libreria di percorsi registrati (§6.3), ne occupa 0,24 e 0,31 in $G_2$ e 0,16 e 0,27 in $G_3$. Il pavimento dà la garanzia per comportamento al prezzo di una regione che dopo 2 s coincide con l'ombra.

## 5. L'indipendenza dei campioni: generatore e semi

Le simulazioni usano un generatore a incremento costante: stato $s \in \mathbb Z_{2^{64}}$, a ogni estrazione $s \leftarrow s + G \pmod{2^{64}}$ ($G$ costante dispari) e uscita $\mu(s)$, con $\mu$ una funzione di mescolamento biiettiva.

**Lemma 1 (semi contigui).** Se lo stato iniziale del seme $\sigma$ è $s_0(\sigma) = \sigma G + c \pmod{2^{64}}$, con $c$ indipendente da $\sigma$, allora la successione prodotta dal seme $\sigma+1$ è quella del seme $\sigma$ avanzata di un'estrazione: $x_i(\sigma+1) = x_{i+1}(\sigma)$ per ogni $i \ge 1$.

*Dimostrazione.* $s_0(\sigma+1) = s_0(\sigma) + G$. Lo stato dopo $i$ estrazioni è $s_0 + iG$, quindi $x_i(\sigma+1) = \mu(s_0(\sigma) + (i+1)G) = x_{i+1}(\sigma)$. $\blacksquare$

*Verifica per calcolo:* 1000 valori uguali su 1000 fra il flusso del seme 9001 e quello del seme 9000 avanzato di uno. *Riparazione:* $s_0(\sigma) = \mu(\sigma G + c)$; con essa le coincidenze sono 0 su 1000.

**Avvertenza di metodo.** Con lo schema del Lemma 1, i passaggi di un lancio a semi contigui condividono le stesse estrazioni spostate di un posto: non sono prove indipendenti. L'effetto misurato su dieci blocchi da 400 semi contigui ($G_1$): nella cella «prosegue» a 3 s la quota va da 0,726 a 0,977 fra i blocchi e la varianza fra blocchi è 6,0 volte quella binomiale; sulle 20 celle sul percorso fino a 3 s il rapporto vale in media 2,67 (1,62 con il denominatore «dentro l'area osservata»). Gli intervalli binomiali calcolati su quei lanci sono quindi **troppo stretti di un fattore fra $\sqrt{1{,}62} = 1{,}3$ e $\sqrt{6{,}0} = 2{,}5$**. Con i semi riparati il rapporto torna a 0,94. Le stime puntuali dei lanci originali restano dentro gli intervalli ricalcolati per blocchi.

**Cifre rifatte con semi riparati** (e taratura rifatta): continuità per passaggio (§6.2), copertura per comportamento e per tempo, numero di celle sopra soglia, area relativa (§6.3), prova con camminatori diversi (§4). **Non rifatte:** i conteggi del sistema prima della modifica a semi contigui (rifatti a parte: stessa conclusione), 71 671 dei 175 802 istanti del controllo sull'area d'avviso (§6.1), le prove fuori dal dominio (§6.3, eseguite con un altro programma e un altro schema di semi), e tutte le prove dei §6.4–6.8, che non usano quel generatore. In ogni prova la taratura e la verifica usano insiemi di semi disgiunti; il generatore delle traiettorie non è stato scritto dall'autore del predittore, ma **in nessuna prova la libreria di taratura viene da un generatore e i passaggi di verifica da un altro**.

## 6. Tavola dei risultati

Condizioni comuni del tipo (I), salvo diversa indicazione: sensore e ostacolo fermi; un soggetto puntiforme per ombra; velocità d'ingresso 0,3–1,8 m/s, rotta entro ±15°; rumore di misura gaussiano di 5 cm per asse, noto al filtro; $P_D = 0{,}9$; $\Delta = 1/15$ s; $q = 0{,}2$ m²/s³; maschera dell'ombra esatta; 400 passaggi per comportamento e per lancio. Condizioni comuni del tipo (II): profili di tre camere a stereo attivo (Intel RealSense D435i e D455, Orbbec Gemini 335) a 424×240, costruiti dai parametri delle schede tecniche a due livelli di rumore («nominale» e «limite»); salvo diversa indicazione profilo D435i al livello nominale, posa della camera nota esattamente. Intervalli: Wilson al 95 % a due code.

### 6.1 Sicurezza

| Misura | Condizioni | Valore | $N$ | Intervallo 95 % | Dato; livello |
|---|---|---|---|---|---|
| Soggetto nascosto fuori da $\Pi$ (Def. 5a) | $G_1,G_2,G_3$; 7 comportamenti; istanti a $\tau = 0{,}5$–5 s | 0 | 175 802 istanti; di cui 104 131 in 24 835 passaggi a semi indipendenti | per passaggio: 0–0,016 % | I; per costruzione ($\mathcal R_\alpha \subseteq \Pi$) e in simulazione |
| Passaggi in cui l'avviso manca | $P_D = 1$; $e_\Omega \in \{-0{,}2; 0; +0{,}2\}$ m; margine 0,40 m; 36 configurazioni | 0 | 14 400 | 0–0,027 % | I; simulazione |
| idem | $P_D = 0{,}9$; $e_\Omega = -0{,}2$ m | 13 (in 8 configurazioni su 12) | 4800 | 0,16–0,46 % | I; simulazione (controesempio) |
| idem | $P_D = 0{,}9$; $e_\Omega \in \{0; +0{,}2\}$ m | 0 | 9600 | 0–0,040 % | I; simulazione |
| Traccia chiusa prima dell'ombra (avviso non acceso) | $G_2$; $P_D = 0{,}7$; corpo esteso | 130 | 1581 | 7,0–9,7 % | I; simulazione (controesempio) |
| Celle «libero» dentro l'ombra vera (Def. 5b) | tre camere; 135 sequenze (4 con i filtri del costruttore accesi) | 0 | 2 907 032 celle·fotogramma; 131 sequenze senza filtri | per sequenza: 0–2,9 % | II; simulazione |
| Centro del soggetto nascosto in una cella «libero» | passaggi dietro un pannello, 3 disposizioni × 30 semi | 0 | 3038 fotogrammi; 90 passaggi | per passaggio: 0–4,1 % | II; simulazione |
| Centro del soggetto nascosto dentro $\Pi$ | idem | 2939 (i restanti 99: in ombra, senza avviso) | 3038 fotogrammi | 96,1–97,3 % (fotogrammi); passaggi con almeno un fotogramma senza avviso: 15 su 90, 10,4–25,7 % | II; simulazione |
| Secondo soggetto mai tracciato che esce dalla stessa ombra: riceve l'identità del primo | 2 disposizioni × 3 valori di $e_\Omega$ | 2400 | 2400 | 99,84–100 % | I; simulazione (controesempio) |

*Che cosa il risultato non dice.* Lo zero sulle celle «libero» vale a posa nota e per ostacoli che restituiscono profondità: nelle stesse simulazioni un errore di posa di 1°, un ostacolo senza ritorno (vetro, palo sottile) o i filtri del costruttore producono «libero» falsi. L'area d'avviso è garantita per un solo soggetto per ombra e per un ostacolo fermo; con due soggetti l'avviso viene rilasciato a torto.

### 6.2 Continuità

| Misura | Condizioni | Valore | $N$ | Intervallo 95 % | Dato; livello |
|---|---|---|---|---|---|
| Passaggi con almeno un vuoto, senza la regione persistente | $G_1 / G_2 / G_3$; 5 comportamenti sul percorso | 1958 / 1991 / 1999 | 1958 / 2000 / 2000 | 99,8–100 / 99,1–99,8 / 99,7–100 % (semi contigui: intervalli ottimistici) | I; simulazione |
| Cicli senza osservazione con una regione, senza la regione persistente (Def. 1a) | idem | 19,0 / 38,1 / 33,3 % | 105 301 / 118 875 / 139 132 cicli | non calcolato (cicli dipendenti) | I; simulazione |
| Passaggi con almeno un vuoto, con la regione persistente (Def. 1b) | $G_1 / G_2 / G_3$; 7 comportamenti; semi contigui | 0 / 0 / 0 | 2716 / 2800 / 2798 | — | I; simulazione |
| idem | semi indipendenti | 0 / 0 / 0 | 13 638 / 5600 / 5597 | 0–0,028 / 0–0,069 / 0–0,069 %; insieme: 0–0,016 % | I; per costruzione, data la premessa; simulazione |
| Cicli senza osservazione con una regione, con la regione persistente | idem | 100 % | 785 645 / 342 552 / 395 479 cicli | — | I; simulazione |

*Che cosa il risultato non dice.* La continuità è garantita per costruzione solo dopo che la traccia è entrata nell'ombra: se la traccia si chiude prima (130 passaggi su 1581 con $P_D = 0{,}7$ e corpo esteso) non c'è regione né avviso. Lo zero non riguarda l'identità al ritorno (§6.4) né una camera in moto.

### 6.3 Precisione della regione

**Nel dominio dichiarato** (sensore e ostacolo fermi; un soggetto per ombra, visto per almeno 4 fotogrammi; ingresso fra 0,3 e 1,8 m/s; comportamenti sul percorso; rumore noto; libreria di taratura dello stesso tipo di camminatore; maschera dell'ombra esatta). Regione adottata: 400 percorsi registrati trapiantati sul punto e sulla velocità d'ingresso, unione delle celle più dense fino al 90 %, con il pavimento «tutta l'ombra non vista libera». Copertura $c(\tau, b)$, Definizione 2, denominatore «tutti i nascosti»; semi indipendenti; tipo I; verificato in simulazione. Ogni cella riporta $G_1 / G_2 / G_3$.

| Comportamento | $\tau = 1$ s | $\tau = 2$ s | $\tau = 3$ s |
|---|---|---|---|
| prosegue | 0,980 / 0,995 / 0,990 | 0,940 / 0,964 / 0,960 | 0,899 / 0,968 / 0,924 |
| rallenta | 0,988 / 0,991 / 0,996 | 0,959 / 0,959 / 0,959 | 0,935 / 0,926 / 0,919 |
| si ferma | 0,985 / 0,991 / 0,989 | 0,965 / 0,977 / 0,959 | 0,956 / 0,968 / 0,939 |
| torna indietro | 0,985 / 0,993 / 0,987 | 0,972 / 0,969 / 0,956 | 0,977 / 0,976 / 0,935 |
| sosta lunga | 0,991 / 0,991 / 0,993 | 0,970 / 0,973 / 0,971 | 0,961 / 0,966 / 0,948 |
| $N$ per cella | 1872–1935 / 800 / 799–800 | 879–1844 / 529–783 / 774–800 | 513–1818 / 284–770 / 669–791 |
| area relativa (Def. 3) | 0,72 / 0,12 / 0,06 | 0,95 / 0,24 / 0,16 | 1,00 / 0,31 / 0,27 |

Semiampiezza degli intervalli $\le 0{,}03$ in ogni cella. Riepilogo per soglia:

| Enunciato | Valore | Cella peggiore | Livello |
|---|---|---|---|
| $\ell^- > 0{,}90$ in ogni cella fino a 2 s ($\tau = 0{,}5; 1; 2$ s) | **45 celle su 45** | $G_1$, prosegue, 2 s: 826/879 = 0,940 [0,922–0,954] | simulazione |
| lo stesso con la correzione per 45 celle ($z_{45} = 3{,}261$) | 45 su 45 | limite inferiore 0,908 | calcolo sui conteggi |
| $\ell^- > 0{,}85$ in ogni cella fino a 3 s | 60 celle su 60 | $G_1$, prosegue, 3 s: 461/513 = 0,899 [0,869–0,922] | simulazione |
| $\ell^- > 0{,}90$ a 3 s | 12 celle su 15; 3 non decise | 461/513; 437/472 = 0,926 [0,899–0,946]; 711/774 = 0,919 [0,897–0,936] | simulazione |
| disco col raggio massimo (ripiego): $\ell^- > 0{,}90$ fino a 2 s; $> 0{,}85$ fino a 3 s | 37 su 45; 60 su 60 | $G_2$, torna, 1 s: 715/800 = 0,894 [0,871–0,913] | simulazione |
| Errore mediano del punto mostrato (Def. 4), $G_2$, miscela di comportamenti | 0,18–0,19 / 0,37–0,39 / 0,54–0,60 m a 1 / 2 / 3 s; punto fermo all'ultima misura: 0,97–1,00 / 1,48–1,54 / 1,59–1,66 m | $N$ = 2400 / 2077–2115 / 1674–1734 | simulazione |

**Fuori dal dominio dichiarato** (controesempi; tipo I salvo l'ultima riga; verificati in simulazione).

| Che cosa cambia | Copertura a 1 / 2 / 3 s ($G_1 / G_2 / G_3$ dove indicato) | $N$ |
|---|---|---|
| chi svolta | 0,864 / 0,871 / 0,941; 0,567 / 0,541 / 0,698; 0,451 / 0,383 / 0,517 | 1911 / 800 / 798; 1578 / 667 / 792; 1504 / 538 / 735 |
| chi esce dal lato lontano | 0,771 / 0,839 / 0,920; 0,320 / 0,448 / 0,665; 0,131 / 0,262 / 0,466 | 1933 / 800 / 800; 1791 / 761 / 800; 1762 / 725 / 788 |
| oltre l'orizzonte: $\tau = 5$ s, $G_1$, prosegue | 174/221 = 0,787 [0,729–0,836] | 221 |
| camminatori meno regolari della taratura, $G_3$ | 0,944 / 0,835 / 0,801 (§4) | 342 / 339 / 282 |
| corpo esteso, $e_\Omega = -0{,}2$ m, $P_D = 0{,}7$, $G_2$, prosegue | 136/364 = 0,37 [0,33–0,42] a 1 s; 43/152 = 0,28 [0,22–0,36] a 2 s | 364; 152 |
| chi parte da fermo accanto al pannello, $G_2$ | 15/141 = 0,11; 21/134 = 0,16; 14/54 = 0,26 | 141; 134; 54 |
| profondità simulata da scheda (tipo II): il soggetto resta sempre nella regione | 36 passaggi su 46 con una previsione (su 90) = 0,78 [0,64–0,88]; con la soglia di punti adattata alla risoluzione: 83 su 90 = 0,92 [0,85–0,96] | 46; 90 |

*Che cosa il risultato non dice.* «Almeno 9 su 10 fino a 2 s» vale nel dominio dichiarato e per quel generatore di camminate; fuori (svolte, uscite laterali, bordo dell'ombra stimato male di 10–20 cm, partenza da fermi, popolazione diversa) la copertura scende fino a 0,1–0,8 e resta solo l'area d'avviso. In $G_1$ da 2 s la regione coincide con l'ombra (area relativa 0,95–1,00): lì la copertura non localizza. Nessuna cifra è dichiarata oltre 3 s, né per una camera in moto.

### 6.4 Identità al ritorno

| Misura (Def. 6) | Condizioni | Valore | $N$ | Intervallo 95 % | Dato; livello |
|---|---|---|---|---|---|
| Stessa identità | una persona, ostacolo fermo, $P_D = 1$; 27 configurazioni con ricomparsa | 400 su 400 in ciascuna (10 800 in tutto) | 400 per configurazione | per configurazione: 99,05–100 % (a una coda: $\ge$ 99,25 %) | I; simulazione |
| Stessa identità | profilo D435i, nominale; pannello, 3 disposizioni × 30 semi | **0** | 90 | 0–4,1 % | II; simulazione (smentisce la riga sopra) |
| Stessa identità, soglia minima di punti per cella portata da 3 a 40 | idem, soli semi di prova (la soglia è stata scelta sugli altri 45, dopo aver visto i dati) | 41 | 45 | 79,3–96,5 % | II; simulazione |
| Identità attribuita a un altro soggetto uscito dalla stessa ombra | §6.1 | 2400 | 2400 | 99,84–100 % | I; controesempio |

*Che cosa il risultato non dice.* Il 100 % del modello ideale non si trasferisce a una profondità realistica: lì la sagoma della persona si fonde con quella del pannello in 90 passaggi su 90. Il recupero a 41 su 45 dipende da una soglia legata alla risoluzione dell'immagine, scelta dopo i dati e provata a una sola risoluzione; non è una prestazione dichiarabile.

### 6.5 Elementi mobili e ostacoli

| Misura | Condizioni | Valore | $N$ | Intervallo 95 % | Dato; livello |
|---|---|---|---|---|---|
| Soggetto a 0,5 m/s etichettato «in movimento» entro 1 s | partenza da 2 m; tre curve di rumore; di traverso e in avvicinamento | 100 % | 2000 per cella | $\ge$ 99,81 % | I; simulazione |
| idem | partenza da 3 m, in avvicinamento, due curve di rumore peggiori | 85,85 %; 26,60 % | 2000 | $\pm$ 1,5; $\pm$ 1,9 punti | I; simulazione (limite) |
| Parete ferma etichettata «in movimento» mentre passa una persona (Def. 7) | con la regola che scarta le misure al bordo di un'ombra; senza | 0; 400 | 400 per curva di rumore | 0–0,95 %; 99,05–100 % | I; simulazione |
| Pannello fermo etichettato «in movimento» | profondità simulata; 3 disposizioni × 30 semi | **79** | 90 | 79,4–93,0 % | II; simulazione (smentisce la riga sopra) |
| idem, soglia di punti adattata | idem | 5 | 90 | 2,4–12,4 % | II; simulazione |
| Ostacolo fermo visto entro 15 cm dalla posizione vera | cassa alta 1 m a 1,68 m; scatola di 15 cm a 2,0 m | 84; 10 | 84; 10 fotogrammi (una sequenza ciascuno) | — | II; simulazione |
| idem, casi limite | scatola di 15 cm a 0,8 m; lastra di vetro; ostacolo sospeso a 2,0 m | 0; 0; 7 | 10 fotogrammi ciascuno | — | II; simulazione (limiti) |
| Tracce confermate su suolo vuoto in 30 fotogrammi | tre profili di camera, nominale; uno al livello limite | 28 / 0 / 26; 43 | 1 sequenza ciascuno | — | II; simulazione |

*Che cosa il risultato non dice.* Le righe sugli ostacoli contano fotogrammi di una sola sequenza: descrivono un caso, non una frequenza. Le soglie sui punti sono assolute e dipendono dalla risoluzione; le tracce spurie sul suolo vuoto misurano il margine fra la tolleranza del suolo e la soglia d'ostacolo, non un sensore.

### 6.6 Profondità simulata dalle schede tecniche di tre camere

| Misura | Condizioni | Valore | $N$ | Intervallo 95 % | Livello |
|---|---|---|---|---|---|
| Errore del bordo dell'ombra stimata | nominale; un pannello | da +2,0 a +14,6 cm; mediana +6,2 cm (verso il largo) | 115 sequenze | — | simulazione |
| Sequenze con tutto l'errore entro ±20 cm | nominale | 115 | 115 | 96,8–100 % | simulazione |
| idem | livello limite | 0 (errori da −65 a +73 cm) | 8 | 0–32,4 % | simulazione (limite) |
| Celle «libero» in ombra vera | soglia di punti a 40 (correzione del §6.4) | 2, più 45 al bordo | 2 907 032; 356 736 celle·fotogramma | — | simulazione (effetto collaterale) |

*Che cosa il risultato non dice.* Il simulatore è verificato contro il proprio modello, non contro una camera: i suoi parametri vengono dalle schede tecniche e, confrontato con registrazioni pubbliche, sottostima i pixel senza dato (7,8 % al livello limite contro 24–34 % osservati). Le cifre al livello nominale sono quindi ottimistiche e non sostituiscono una misura sul sensore.

### 6.7 Traiettorie pubbliche di pedoni

Tracciati di persone in cammino al chiuso, registrati con un sistema di cattura del moto (non con una camera di profondità); una registrazione per scegliere $q$ (227 tratti), un'altra per la prova (219 tratti, 9 persone). Si simula un'occlusione e si verifica se la posizione vera sta nella regione al 90 % del filtro a velocità quasi costante.

| Misura | Condizioni | Valore a 1 / 2 / 3 s | $N$ | Intervallo 95 % | Dato; livello |
|---|---|---|---|---|---|
| Copertura della regione al 90 % | $q = 0{,}2$ | 0,977 / 1,000 / 1,000 (214, 219, 219 su 219) | 219 tratti, 9 persone | 0,948–0,990 / 0,983–1 / 0,983–1 (tratti come indipendenti) | III; misurato su dati pubblici |
| idem | $q = 0{,}05$; $q = 0{,}01$ | 0,795 / 0,804 / 0,831; 0,534 / 0,521 / 0,516 | 219 | $\pm$ 0,05; $\pm$ 0,07 | III |
| idem, sulla registrazione di scelta | $q = 0{,}1$ | 0,943 / 0,960 / 0,987 | 227 | — | III |
| Errore mediano della previsione | $q = 0{,}2$ | 0,21 / 0,49 / 0,81 m | 219 | — | III |

*Che cosa il risultato non dice.* Il filtro parte da posizioni misurate con precisione millimetrica fino all'ultimo istante: la prova riguarda il modello di moto, non la catena su profondità. I tratti di una stessa persona sono correlati (da 7 a 42 tratti a testa): la numerosità efficace sta fra 9 e 219, e gli intervalli della tabella sono un limite ottimistico. Con $q = 0{,}2$ la regione copre più del livello dichiarato, cioè è più larga del necessario.

### 6.8 Costo

| Misura (Def. 8) | Condizioni | Valore | $N$ | Dato; livello |
|---|---|---|---|---|
| Ciclo della catena completa | 162 sequenze simulate a 424×240; un filo di una CPU da portatile | media **6,35 ms**; mediana 4,13; 95º percentile 18,6; massimo 105,0; 4 cicli oltre 66,7 ms | 9152 cicli | II; misurato |
| idem | una registrazione pubblica affollata (stereo attivo, 640×360), 254 tracce | media 81 ms; 95º percentile 152 ms | 320 cicli | III; misurato |
| Solo predittore della regione, in C | 10 / 60 / 120 tracce | mediana 0,51 / 2,53 / 4,83 ms; 95º percentile 0,62 / 2,89 / 5,44 ms | 1500 cicli | I; misurato |
| idem, in Python puro | 1 / 3 / 10 tracce | mediana 0,6 / 1,8 / 5,3 ms; 95º percentile 0,7 / 2,0 / 6,2 ms | 150–225 cicli | I; misurato |

*Che cosa il risultato non dice.* I tempi sono presi su un portatile condiviso con altri processi, non sulla scheda di bordo; non comprendono l'acquisizione né la latenza $\tau$ del sensore. Il costo cresce con il numero di tracce: con centinaia di tracce spurie il ciclo supera il periodo $\Delta$.

## 7. Limiti di validità comuni

Tutte le frequenze di questo capitolo sono condizionate al generatore che le ha prodotte: modello ideale del sensore (tipo I), profondità simulata da scheda tecnica a posa nota (tipo II), o traiettorie pubbliche prive di profondità (tipo III). La copertura della regione, l'errore del bordo dell'ombra, il rumore del centro, l'identità al ritorno e la latenza **non sono verificati sperimentalmente su un sensore**. Sul posto vale il conteggio «dentro $k$ su $n$» letto con le regole del §3: con le numerosità raggiungibili in una dimostrazione (10–50 passaggi per riga) esso può smentire una cifra, non confermarla al centesimo.

---

# PARTE II — Provenienza e controlli (per il coordinatore; non entra nell'allegato)

Radice dei percorsi: `.sciame/20261114-1301-percezione-challenge/`. Programmi miei in `f13-allegato/04-statistica/`: `riconta.py` (riconteggio dai file grezzi, sola lettura, nessun codice altrui importato) → `ricontato.txt`; `conti.py` (intervalli, numerosità, Beta, Fisher; usa scipy) → `conti.txt`; `rifai.sh` li rilancia (pochi secondi; interprete di `f10-dati/03-infrastruttura/AMBIENTE.md`, con `-I -B`). Ultimo esito: **31 righe «TORNA», 0 «NON TORNA»**.

## II.0 In testa: cambi di stato, scostamenti, regole violate

- **Un mio errore, corretto e lasciato a verbale.** Al primo lancio `riconta.py` dava «NON TORNA» su «regione 83 su 90»: avevo attribuito la cifra ai parametri di partenza. Nel file (`f10-dati/20-validazione/uscite/sim/misura_passaggi.json`) con i parametri di partenza le previsioni esistono solo in 46 passaggi su 90 e la verità resta nella regione in **36 su 46**; **83 su 90** sta nella variante a soglia 40 (`uscite/sim_p40/`). Il verdetto f10 (§«Cifre ricontate») scrive «regione 83 su 90» in fila con le cifre della variante di partenza (2939 su 3038, 99 senza avviso) senza dire la variante: **è un'ambiguità d'attribuzione, non un errore di conto**. Nella parte I ho messo entrambe, ciascuna con la sua condizione.
- **Previsioni** (in `PREVISIONI_E_STATO.txt`, scritte alle 18:01:06 dopo la lettura dei verdetti e prima dei miei programmi: non cieche rispetto ai testi). P1 (tutte le cifre tornano): **regge** (31 su 31, dopo la correzione qui sopra, che era mia). P2 (numerosità 80–95, 190–215, 300–420): **regge per l'$n$ stabile in un verso** (89 e 94; 203 e 191; 304), **smentita** per il primo $n$ (78–82; 169–179; 270–281) e per 299. P3 (9 su 10 è Clopper-Pearson, 27 su 30 è Wilson): **regge**. P4 (con Bonferroni restano almeno 40 celle su 45): **regge** (45 su 45, limite peggiore 0,908). P5 (semi contigui, 1000 su 1000): **regge**.
- **Notato dopo, non previsto:** la potenza esatta è a dente di sega, quindi «89» e «203» dei file sono l'$n$ *stabile*, non il primo $n$; lo stesso per «68 passaggi» della taratura conforme (primo $n$ 68, stabile 110).
- **Indipendenza dei miei controlli.** Condivido con gli autori il modello linguistico, la specifica e i file d'uscita; **non** ho rieseguito nessun simulatore: «ricontato» vuol dire somme e intervalli rifatti dalle righe grezze (TSV, json, jsonl, testo). Un difetto nei simulatori resta invisibile a questo controllo. Miei sono: il lettore dei file, le formule, lo splitmix64 del Lemma 1 (riscritto leggendo `f8-continuita/15-statistica/codice/gen.h`, righe 23–40).
- **Regole violate:** nessuna che io sappia (nessun git, sudo, rete; scritto solo in `f13-allegato/04-statistica/`). Ho creato `PREVISIONI_E_STATO.txt` al posto di uno `stato.md`.
- **Lunghezza:** la parte I è al limite delle dieci pagine (tabelle fitte).

## II.1 Provenienza e ricalcolo, voce per voce

| Parte I | File d'origine | Mio ricalcolo |
|---|---|---|
| §1 Def. 2, due denominatori; 461/513 e 461/480; 86/92–86/98; 101/105–101/119 | `f8-continuita/15-statistica/ANALISI.md` §0.2; `ris/semi_D_*.tsv`; `11-misure/risultati/prova_D_pd09.tsv`; `13-soluzione/ris/prova_D.tsv` | torna (`ricontato.txt` A5c, A5d); Fisher p = 0,519 (`conti.txt` §7; file: 0,52) |
| §2 Wilson, esempio 826/879 | formula in `15-statistica/riconta.py` riga 29 | torna: [0,9220–0,9536] |
| §2 Prop. 1; «limite 0,75 %» (0 su 400), «2,9 %» (0 su 131), «0–4,1 %» (0 su 90), «≤ 0,07 %» (0 su 5597) | `f4/H-012/03-validazione/MISURE_V2.md` riga 9; verdetto f10 §1; `ANALISI.md` §3 | torna, ma **con tre convenzioni diverse**: 0,75 % è 3/N a una coda; 2,9 % e 4,1 % sono Wilson a due code; 0,07 % è l'esatto a due code (0,066 %). Nella parte I: Wilson ovunque, una coda citata a parte |
| §2 Prop. 2; $z_{12} = 2{,}87$; 90 su 100 → 0,78–0,96 | `f8-continuita/04-statistico/CONSEGNA.md` riga 45 | torna (2,865; 0,782–0,958). $z_{45}$ e «45 su 45 con correzione» sono **un conto mio sui conteggi dei file** (chiesto dalla consegna), non una cifra dei file |
| §3 89 e 203; 86 con soglia 74; potenza 0,39 con 30 | `04-statistico/CONSEGNA.md` riga 45; `06-visualizzatore/risultati_tabellone.txt` (PV-2c) | torna come $n$ stabile con $H_0 = 0{,}90$ (89; 203) e come primo $n$ con i due errori a 0,10 (86, soglia 74); potenza 0,393. **299–304 per 0,85 è nuovo** (nessun file lo dà) |
| §3 9 su 10: 55,5–99,7 %; 27 su 30: 0,74–0,97; 37,6 %; 4,2 %; 38 / 51 / 93; 88 %; 46 su 50; 40 → 14 | `risultati_tabellone.txt` (PV-2a, 2b); `04-statistico/CONSEGNA.md` righe 45, 82; `15-statistica/ANALISI.md` §6 | torna. **Discordanza di metodo fra file:** 55,5–99,7 è l'esatto, 0,74–0,97 è Wilson (l'esatto di 27 su 30 è 73,5–97,9, com'è scritto nel tabellone). «Almeno 0,80 solo con 28 su 30» (CONSEGNA riga 82) vale solo col limite esatto a una coda (0,805); con Wilson ne servono 29 |
| §3 1216/1244 = 0,977 contro 0,68 | `ANALISI.md` §6 punto (2); `11-misure/BANCO_DI_PROVA.md` riga 48 | **non ricontato** (letto) |
| §4 Prop. 3 e citazione | `f8-continuita/03-kalman/CONSEGNA.md` riga 30; `04-statistico/CONSEGNA.md` righe 46, 56 | dimostrazione riscritta da me; citazione `angelopoulos2021`: in `RIFERIMENTI.md` «verificata … la condizione di scambiabilità è nel testo» |
| §4 Prop. 4; 0,805; 0,848; 68; soglia infinita sotto 9; 0,803 e 0,851 simulati | `04-statistico/out_conforme.txt` (a) | torna (`conti.txt` §6); i due valori simulati sono **letti** |
| §4 0,897–0,907; 0,455; 0,307 | `f8-continuita/07-ricercatore/CONSEGNA.md` riga 45; `risultati_conforme.txt` riga 28 | **letto nel file d'uscita, non rieseguito** (0,455 presente) |
| §4 0,72 / 0,66 / 0,64 | `04-statistico/out_conforme.txt` (b): 0,720 / 0,658 / 0,640 | **letto, non rieseguito** |
| §4 0,944 / 0,835 / 0,801 | `15-statistica/ris/semi_spostato_L_90000x400.tsv` | torna (A7): 323/342, 283/339, 226/282 (denominatore «dentro l'area osservata») |
| §4 Prop. 5 e aree 1,8 / 4,4 / 4,8 / 4,2 | `04-statistico/out_conforme.txt` (c), riga «disco su vel. costante, 4 classi» | dimostrazione mia; aree **lette** |
| §4 quote dell'ombra del ripiego e della regione adottata | `15-statistica/ris/semi_*.tsv`, campi `area90`, `ombra` | ricalcolate (A5): media pesata sui cinque comportamenti sul percorso. Il verdetto f8 §5 scrive «0,8–1,7» e «0,06–0,36»: usa un'altra pesatura («prosegue» soltanto); le mie sono 0,79–1,21 (a 2–3 s, $G_2$ e $G_3$; 1,55–1,61 in $G_1$) e 0,06–0,31 |
| §5 Lemma 1; 1000 su 1000; riparazione | `15-statistica/codice/gen.h` e `codice_semi/gen.h`; `ris/prova_semi.txt` | torna (A9), con un mio splitmix64 |
| §5 0,726–0,977; 2,67; 1,62; 6,0; 0,94; 1,3–2,5 | `ANALISI.md` §0.1; `ris/TABELLE_STATISTICO_tutti.txt` Tab 4b | torna (A8). **Precisazione:** nel testo d'origine «2,67» segue la frase sulla cella «prosegue a 3 s» e sembra riferirsi a quella; per quella cella il rapporto è 6,02; 2,67 è la **media sulle 20 celle** sul percorso fino a 3 s. Nella parte I è scritto così |
| §6.1 0 su 175 802 | verdetto f8 §2 (controllo 5); `16-verdetto/PREVISIONI.md` P-v-12 | torna (A6): 35 780 + 35 891 + 104 131. Sono istanti campionati a cinque valori di $\tau$, non tutti i cicli; i primi due addendi vengono da semi contigui |
| §6.1 0 su 14 400; 13 su 4800; 0 su 9600 | `f4/H-012/03-validazione/v2_R8.txt`, `v2_R8_pd09.txt` | torna (B1, B3) |
| §6.1 130 su 1581 | `f8-continuita/14-attacco/ris/tutto_T_e0_pd07.txt` | torna (A11) |
| §6.1 0 su 2 907 032; 135 = 131 + 4; 0 su 131 | `f10-dati/20-validazione/uscite/sim/misura_libero.json` | torna (C1). Il verdetto dice «3 forme d'ombra»; nei record i valori distinti di «celle tutte in ombra» sono 4 (8, 12, 342, 454): **non ho approfondito** (definizioni diverse di «forma») |
| §6.1 2939 su 3038; 99; 0 | `…/sim/misura_passaggi.json` | torna (C3); in più, per passaggio: 15 su 90 con almeno un fotogramma senza avviso (conto mio) |
| §6.1, §6.4 2400 su 2400 | `f4/…/v2_SECOND.txt` | torna (B4). Il «2 su 1200» del verdetto del nucleo: nel file le righe «portata» sommano 2 su 2400 (**denominatore discorde**, la cifra non è nella parte I) |
| §6.2 1958 / 1991 / 1999; 19 / 38 / 33 %; 0 su 2716 / 2800 / 2798; 0 su 13 638 / 5600 / 5597; 9715 / 3981 / 3997 | `11-misure/risultati/prova_*_pd09.tsv`; `13-soluzione/ris/prova_*.tsv`; `15-statistica/ris/semi_*.tsv` | torna (A1, A2, A3, A12, A12b) |
| §6.3 tabella per comportamento; 45 su 45; 826/879; 60 su 60; 12 su 15; 37 su 45; 174/221 | `15-statistica/ris/semi_*.tsv` (9 file) | torna (A4, A5, A5b) |
| §6.3 errore del punto | righe `M` di `13-soluzione/ris/prova_T.tsv` e `15-statistica/ris/semi_T_*.tsv` | **letto dalle righe riassuntive** (A12c), non ricalcolato dai passaggi. **Discordanza:** il verdetto f8 §2 dà per il punto fermo 0,97 / 1,53 / 1,64; i file danno 0,983 / 1,490 / 1,659 (semi contigui) e 0,97–1,00 / 1,48–1,54 / 1,59–1,65 (riparati). Nella parte I ho messo gli intervalli fra i lanci. I pesi della miscela non li ho controllati |
| §6.3 svolta, lato lontano | `semi_*.tsv` | torna (A5) |
| §6.3 136/364, 43/152 | `14-attacco/ris/tutto_T.txt` | torna (A11, seconda riga) |
| §6.3 15/141, 21/134, 14/54 | `14-attacco/ris/fermo_T*.txt` secondo `16-verdetto/riconta_verdetto.txt` n. 20 | **non ricontato da me** (letto dal riconteggio altrui) |
| §6.3 36 su 46; 83 su 90 | `f10-dati/…/sim/` e `sim_p40/misura_passaggi.json` | torna (C2), vedi II.0 |
| §6.4 400 su 400 in 27 configurazioni | `f4/…/v2_R8.txt` (riemersioni e quota riagganciata) | torna (B2): 27 righe con riemersioni, tutte al 100,0 %, 10 800 riemersioni. La quota è stampata in percentuale a un decimale: «400 su 400» è dedotto da 100,0 % × 400 |
| §6.4 0 su 90; 41 su 45; 80 su 90; fusione 90 su 90 | `f10-dati/…/sim*/misura_passaggi.json` | torna (C2). I nomi dei tre profili (D435i, D455, Gemini 335) vengono dal verdetto f10 §1: i parametri delle schede non li ho riletti |
| §6.5 «in movimento» 100 %; 85,85 %; 26,60 %; parete 0 e 400 su 400 | `f4/…/v2_MOB.txt`, `v2_WALLP.txt` | **letti** (percentuali stampate; conteggi dedotti); intervalli miei |
| §6.5 79 su 90; 5 su 90; 84 su 84; 10 su 10; 0, 0, 7 su 10; 28 / 0 / 26 / 43 | `misura_passaggi.json`; `misura_ostacoli.json`; `riassunto.json` dei quattro pavimenti vuoti | torna (C2, C5, C6) |
| §6.6 +2,0 / +6,2 / +14,6 cm; 115 su 115; 0 su 8; 2 più 45 | `…/sim/misura_ombra.json`; `sim_p40/misura_libero.json` | torna (C4, C1). «7,8 % contro 24–34 %»: **letto** dal verdetto f10 (K-407), non ricontato |
| §6.7 219 tratti, 9 persone; 0,977 / 1 / 1; 0,21 / 0,49 / 0,81; altre $q$ | `f10-dati/20-validazione/uscite/banco_thor.json`; `21-statistica/tabelle/thor.json` | **riletto dal riassunto** (C8), non ricalcolato dalle tracce; il ricalcolo indipendente già nei file dà 0,982 / 0,995 / 1,000. Conteggi 214 / 219 / 219 e intervalli sono miei |
| §6.8 6,35 ms ecc. | 162 file `fotogrammi.jsonl` in `…/uscite/sim/` | torna (C7): 9152 cicli, media 6,35, 95º 18,6, massimo 105,0, 4 oltre 66 ms; la mediana 4,13 è mia |
| §6.8 81 ms, 152 ms | `…/uscite/vere/RIEPILOGO.jsonl` (in `riconteggio.txt` C12: 81,47 e 151,95) | **letto**: non ricontabile (solo riepilogo) |
| §6.8 tempi del predittore | `f8-continuita/14-attacco/ris/tempo_C.txt`, `tempo_py.txt` | **letti** (A10), non rimisurati |

## II.2 Discordanze fra file (riassunto)

1. **Denominatore della copertura.** Il verdetto f8 (K-213) adotta «nascosti dentro l'area osservata»; la cifra di testa (826/879, limite 0,922) e la tabella per comportamento usano «tutti i nascosti». Ho dichiarato nella parte I «tutti» (prudente, coerente con la cifra di testa) e detto dell'altro. Con «dentro l'area osservata»: 45 su 45, cella peggiore $G_3$ «torna» a 2 s, 740/774, limite 0,939; a 3 s 13 celle su 15. **Scelta da confermare.**
2. **Tre convenzioni per «0 su N»** e **due per «k su n»** (II.1, righe §2 e §3).
3. **«Regione 83 su 90»**: variante a soglia 40, non di partenza (II.0).
4. **«2,67»**: media su 20 celle, non la cella citata accanto (II.1, §5).
5. **Errore del punto fermo**: 0,97 / 1,53 / 1,64 nel verdetto contro 0,98 / 1,49 / 1,66 nel file della soluzione.
6. **Aree relative**: 0,06–0,36 e 0,8–1,7 nel verdetto f8 (pesate su «prosegue») contro 0,06–0,31 e 0,79–1,21 (pesate sui cinque comportamenti; 1,55–1,61 in $G_1$).
7. **«2 su 1200»** (verdetto del nucleo) contro 2 su 2400 nel file.
8. **THÖR**: 0,977 / 1,000 / 1,000 (validazione) contro 0,982 / 0,995 / 1,000 (ricalcolo con un altro filtro): entrambe nei file; nella parte I la prima.

## II.3 Citazioni

- **Usata:** `angelopoulos2021` (stato «verificata», copertura marginale e scambiabilità nel testo).
- **Non usate perché non verificate per il dato o senza voce:** intervallo di Wilson (nessuna voce in `riferimenti.bib`: la formula è nella parte I senza citazione); `clopper1934` («verificata in parte», solo dati bibliografici, testo non letto); regola del tre (nessuna voce; dimostrata nella parte I); disuguaglianza di Boole/Bonferroni (nessuna voce); `thor` («verificata in parte»; inoltre gli insiemi di dati non sono in `riferimenti.bib`: il §6.7 descrive l'insieme senza nominarlo: **al curatore della bibliografia decidere come citarlo**); `depthtrack`, `tum-rgbd` (registrazioni pubbliche del §6.8 e §6.6: non in `.bib`; `tum-rgbd` verificata in parte); `gneiting2007` (verificata, ma il punteggio logaritmico usato nei file non è fra i dati verificati: non usata); generatore splitmix64 (nessuna voce).

## II.4 Che cosa l'integrazione in corso (f12) potrebbe cambiare

Non l'ho attesa né letta (solo l'elenco delle cartelle). Dai nomi (`02-prova-insieme`, `06-identita`, `03-libero`) e dalle correzioni chieste dai verdetti: (a) **§6.4 e §6.5**: una soglia di punti proporzionale ai pixel e il rifiuto dei gruppi tagliati cambierebbero 0 su 90, 41 su 45, 79 su 90, 5 su 90 e le 28 tracce sul suolo vuoto; (b) **§6.1 e §6.2**: la regola d'ingresso e il riaggancio riscritti cambierebbero 130 su 1581, i 99 fotogrammi senza avviso e il controesempio del secondo soggetto; (c) **§6.3**: una prova d'insieme delle correzioni su semi nuovi sostituirebbe le righe «fuori dal dominio»; (d) **§6.6**: i 2 più 45 «libero» con la soglia alta. Restano stabili: §2–§5 (metodo), la tabella nel dominio dichiarato del §6.3 (finché il predittore non cambia), §6.7, il metodo del §6.8.

## II.5 Che cosa manca per completare l'area

- La copertura a **semi riparati per le prove fuori dal dominio** fatte con l'altro programma: il verdetto f8 lo dice esente dal difetto dei semi (`16-verdetto/semi_altri.txt`); **non l'ho verificato**.
- Nessun intervallo **per gruppi** (per persona) sui 219 tratti pubblici: servirebbe un ricampionamento per persona dalle tracce (non fatto: avrei dovuto leggere i dati scaricati).
- Le cifre dell'estensione sulla mappa voxel (f7: 0 punti profondi dati per liberi, costi 0,03–0,6 ms della griglia polare) e delle strategie esterne (f9) **non sono nella tavola**: non le ho ricontate nel tempo dato; se servono nel capitolo vanno prese dai verdetti come «lette».
- Il rumore del centro con la distanza (verdetto f10, H-403: non decidibile) e la latenza: nessuna cifra dichiarabile; nella parte I stanno fra i limiti.
- Le condizioni di alcune righe del tipo (I) del nucleo (nomi delle due disposizioni, le «tre curve di rumore») sono descritte in modo generico: il fascicolo sul modello del sensore deve fornire i valori.
