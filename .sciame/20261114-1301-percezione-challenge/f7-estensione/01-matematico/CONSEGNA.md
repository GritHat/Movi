Canarino: sciame-canarino-55f6adcfa718b00e

# Formalizzazione matematica della mappa a strati — `sciame-matematico`, f7, corsia A

Lavoro dalle 2026-11-14T15:05:02+01:00. File: `PREVISIONI.md` (tre tornate, ciascuna con l'ora prima del lancio), `verifica_strati.py` (Python puro, semi fissi), `risultati.txt` (15:18), `risultati_dopo.txt` (15:19), `risultati_braccio.txt` (15:21). Rifare, in questa cartella: `PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 verifica_strati.py` (18 s), poi con l'argomento `F` (24 s) e `G` (11 s).

## 1. Scostamenti, previsioni smentite, regole

- **Smentite.** P4: la regola proposta dichiara libero lo 0,1 % (v_max 2,5 m/s) e il 3,2 % (1,4 m/s) del visto libero, contro il 10–30 % e il 25–50 % previsti. P5: con il 5 % di buchi per passo angolare tiene il 13,7 %, non ≥ 70 % (con buchi per cella, seconda tornata: 84,9 % e 74,3 %). P3, seconda metà, alla lettera: falsi liberi a latenza zero in 29 corse su 96 (29 su 48 con i buchi, 0 su 48 senza). P7, una clausola: senza margine sbagliano 114 e 162 scene su 200, non ≥ 90 %. P8: a f = 0,20 il 90,5 %, non > 95 %. **Reggono** P1, P2, P6, P9, D1–D5, G1, G2.
- **Scostamenti.** La prova numerica è una **sezione piana (2D)**: i teoremi non dipendono dalla dimensione, ma nessun numero qui è misurato in 3D. La «regola nucleo-simile» è una mia lettura del nucleo, non il suo codice. Prima del lancio registrato c'è stato un lancio di prova con 2 mondi; lo script è stato esteso due volte dopo (funzioni `sim_F`, `sim_G`): i primi due lanci rifatti con lo script finale (15:23) sono identici, salvo il tempo. Le modifiche dello script e due correzioni di cifre in questo file sono state fatte con comandi Python senza `timeout` (meno di 1 s l'uno). Lunghezza: circa 2500 parole, al limite delle tre pagine o poco oltre. Non ho letto `MISURE*.md`, `CONTROPROVE.md`, `AUDIT.md` né `f6-specializzazione/01` e `03`: del nucleo conosco `SOLUZIONE_V2.md`, `VERDETTO.md`, `MOTO_PROPRIO.md`. Le due fonti in rete le ha riassunte un modello ausiliario: le cifre vanno ricontrollate sulla pagina.
- **Regole violate:** nessuna che io sappia. **Indipendenza:** script e dimostrazioni condividono autore, modello e ipotesi; il controllo vale per errori d'algebra e di codice, non per il sensore vero.

## 2. Critiche, ciascuna con la prova

1. **La formula di §4 di `promptMare.txt` è il filtro di Bayes di un mondo fermo.** Ha il passo di correzione e nessun passo di previsione: è questa la causa del «problema obbligatorio». *Prova:* su 24 mondi × 300 fotogrammi (2–4 oggetti fino a 2,5 m/s) dichiara libere 138 230 celle-fotogramma che risultano occupate quando l'uscita è in uso, in 24 corse su 24; a sensore coperto per 2 s tiene «libere» almeno 235 celle per tutto il tempo (`risultati.txt`, A).
2. **Lo stato (L, τ, q, ν) è ridondante e insufficiente.** ν si ricalcola a ogni fotogramma dall'immagine di profondità: memorizzarlo crea il dato vecchio; q scala l'incremento e non è uno stato. Un solo τ non basta. *Prova a mano:* celle j e k; j è vista libera solo nei fotogrammi pari, k solo nei dispari; un oggetto sta in j nei dispari e in k nei pari. Ogni cella ha «età ≤ 1 fotogramma» e l'oggetto non è mai visto: l'età per cella non certifica niente senza la condizione sull'intorno (T1).
3. **«Sparsa» contro «non allocato = sconosciuto».** Per T3 ogni voxel dichiarabile libero deve essere allocato: l'allocazione cresce con il **volume** visto libero, non con le superfici. *Conto:* la piramide vista (87° × 58°, 3 m) è 18,9 m³, il 26 % della scatola 6 × 4 × 3 m: 18 937 voxel da 10 cm, 151 494 da 5 cm, contro 72 000 e 576 000 della griglia densa (`risultati.txt`, E). Il guadagno massimo è 3,8 volte, prima del costo dell'indice; a 2 byte per voxel la densa pesa 144 kB e 1,15 MB (conto, non misura).
4. **La credenza sul libero non ha un uso positivo ammesso** (T2, §5). Il predicato di sicurezza la può leggere solo come veto.
5. **Il filtro bayesiano rende il vetro un «libero» stabile.** Con i parametri di OctoMap (0,7 e 0,4; saturazione 0,1192 e 0,971) la deriva media è negativa se la superficie ritorna in meno di f* = 0,323 dei fotogrammi. *Prova:* p < 0,5 nel 99,9 % dei fotogrammi a f = 0,05 e nel 90,5 % a f = 0,20 (C). Il vetro resta non risolto.
6. **Inerzia.** Da saturata libera a p > 0,5 servono 3 colpi (0,2 s a 15 Hz); da saturata occupata a p < 0,5, 9 passaggi (0,6 s) (C). *Prova:* a latenza zero la griglia bayesiana ha 95 928 celle-fotogramma «libere» e occupate; 82 620 anche escludendo le celle colpite nel fotogramma. «Occupato osservato» deve venire dal fotogramma corrente, mai da L.
7. **Nucleo, invariante 1.** La regola nucleo-simile dà 45 829 falsi liberi in finestra (24 corse su 24) e 0 a latenza zero senza buchi: il difetto è la latenza senza margine, cioè la questione K-015 del verdetto, qui contata. La fascia di 0,40 m copre 1,85 m/s con h = 0,217 s (E), ma il nucleo la applica solo attorno allo strato 1, non a ogni bordo del non osservato.
8. **§6, filtro 3D.** Il rango di osservabilità è 6 solo se la quota del centro è misurata; con il gruppo tagliato dal campo verticale è 4. Un oggetto in caduta esce dalla regione al 95 % del modello a velocità costante dopo 0,169 s; per coprirlo a 0,5 s servirebbe q = 4,62 m²/s³, 23 volte quello del nucleo (D).
9. **§8, nebbia come buchi.** I buchi non sono il caso difficile (D4: la ricorsione tiene il 74–85 % con il 5 % di buchi per cella); lo è la profondità valida e sbagliata, che viola H1. Non provato.

## 3. Parti di `promptMare.txt` per il mio campo

**Utili:** i tre strati di §2 e §4, che reggono se corretti come in §5; §5, con la risposta «l'ombra si ricava per proiezione sull'immagine di profondità e non si memorizza»; §7, fermare l'integrazione se la posa non è affidabile (T6 dà la soglia); le prove 1, 2, 3, 5, 6, 9 di §10; il criterio di §14. **Inutili qui:** CSR e COO, che sono formati statici (un inserimento riscrive gli indici); il capitolato di §13. **Sbagliate o da correggere:** la formula di §4 senza passo di previsione (critica 1); l'ipotesi «sparsa a blocchi» come risparmio di memoria a questa scala (critica 3); il filtro a 6 stati come estensione naturale (critica 8).

## 4. Stati proposti

| Enunciato | Stato |
|---|---|
| T1, T3–T6 (§5) | **dimostrato** nel modello H1–H5; controllo numerico in 2D: 0 falsi liberi in 368 corse da 300 fotogrammi e 0 celle occupate fuori da Π nelle 296 in cui l'ho contato; il braccio con velocità doppia fallisce in 23 e 21 corse su 24 (`risultati_braccio.txt`) |
| T2 (minimalità di Π) | **dimostrato per oggetti puntiformi**, a schizzo; con una taglia minima degli oggetti è **congettura** che Π si possa restringere |
| «Una griglia bayesiana statica non dà falsi liberi» | **smentito** (critiche 1 e 6) |
| «La mappa sparsa risparmia memoria rispetto alla densa» sulla regione 6 × 4 × 3 m | **non risolto**: limite teorico 3,8 volte; decide la misura del gruppo strutture dati |
| «La regola Π lascia libero dichiarabile utile a passo d'uomo» | **smentito nel modello**: 0,2 % a 2,5 m/s e 5,1 % a 1,4 m/s (0,1 % e 3,2 % nel primo lancio, altri semi); 31,8 % a 0,9 e 60,7 % a 0,4 (scena dinamica, `risultati_dopo.txt`); in scena vuota 10,9 / 31,2 / 61,5 / 79,8 % |
| H1 sulla camera vera; vetro; beneficio in 3D | **non risolto**: nessuna profondità vera, nessuna prova in 3D |

## 5. Proposte

### matematico-1 — strato Π di possibile presenza e «tempo di garanzia»

**Ipotesi.** H1: una profondità valida z garantisce vuota l'impronta del pixel fino a z − b (si usa il minimo sull'impronta). H2: ogni punto di ogni oggetto si muove con continuità a velocità ≤ v_max. H3: fotogrammi ogni Δ; l'uscita del fotogramma t è in uso in [t+λ, t+λ+Δ]; h = λ + Δ. H4: le dilatazioni sulla griglia sono per eccesso; un voxel non allocato o fuori griglia vale Π = 1. H5: l'errore di posa fra il riferimento in cui Π è memorizzato e il sensore sposta un punto a distanza r di al più m(r) = ε_t + r·δ.

**Stato del voxel (2 byte).** L_i, log-odds dell'occupazione, saturato; Π_i, un bit; a_i, età dell'ultimo attraversamento, in fotogrammi. Non allocato equivale a (L_0 = 0, Π = 1, a = ∞). La classe di visibilità (attraversato, colpito, in ombra, senza dato, fuori campo) si calcola a ogni fotogramma proiettando il voxel sull'immagine di profondità.

**Tre strati.**
- *Occupazione.* L_i ← sat(L_i + ℓ), con ℓ = +l_occ se colpito, −l_lib se attraversato, 0 negli altri casi: una misura mancante non aggiorna. Con L_0 = 0 il termine −L_0 di §4 cade. Valori anomali: minimo sull'impronta; l'avviso d'ostacolo chiede due colpi, la sicurezza no. Oggetti mobili: i voxel di un gruppo che ha una traccia «mobile» non ricevono +l_occ, altrimenti lasciano una scia; lo stato dinamico resta nella traccia. Un eventuale oblio porta L solo verso L_0. Con m(r) > a/2 l'integrazione si ferma e l'«occupato ricordato» si dilata di m.
- *Visibilità.* F(t) = voxel interamente attraversati da raggi validi nel fotogramma t.
- *Possibile presenza.* Π(0) = tutto; **Π(t) = [Π(t−Δ) ⊕ B(v_max·Δ + m)] ∖ F(t)**. È il passo di previsione che manca a §4: il supporto del filtro di Bayes con dinamica a velocità limitata.

**Predicato.** DL_i(t) ⇔ dist(V_i, Π(t)) > v_max·(λ+Δ) + m **e** a_i ≤ A_max **e** L_i < l_veto. La visibilità entra con F(t), la latenza con h, l'età con a_i e con la ricorsione, la credenza solo come veto. Versione graduata: tempo di garanzia T_i = dist(V_i, Π(t))/v_max − h.

**Teoremi nel modello.**
- **T1, correttezza.** Ogni punto occupato al fotogramma t sta in Π(t); un voxel con DL è vuoto in tutto [t, t+h]. Induzione: un punto occupato a t distava al più v_max·Δ da un punto occupato a t−Δ, che sta in Π(t−Δ), e per H1 non sta in F(t).
- **T2, minimalità.** Per ogni x in Π(t) esiste un mondo ammesso, coerente con tutte le immagini, con un oggetto puntiforme in x. Quindi ogni regola che dichiara libero un voxel fuori da DL sbaglia in qualche mondo: **la credenza sul libero non ha uso positivo**; in congiunzione può solo restringere.
- **T3, non allocato ⇒ sconosciuto.** Vale Π = 1, quindi non DL. Togliere un blocco non crea liberi e non cancella possibile presenza; l'etichetta dello strato 1 (identità, età) deve stare nella lista delle tracce, non nei blocchi.
- **T4, niente libero per decadimento.** Se i ∉ F(t) e i ∈ Π(t−Δ) allora i ∈ Π(t): nella ricorsione non compaiono timer, decadimento né perdita della traccia.
- **T5, il dato vecchio non prevale.** I voxel colpiti stanno in Π(t): tutto ciò che dista meno di v_max·h da un nuovo occlusore smette di essere DL nello stesso fotogramma; un'ombra profonda d è tutta in Π entro d/v_max, e con A_max entro A_max.
- **T6, posa.** Se B(x, m) ⊂ F̂ (libero stimato), allora x è libero davvero, perché la posa vera sposta x di meno di m. Margine: 2,6 cm a 3 m con δ = 0,5°, la soglia IMU del nucleo; 8,2 cm con 3 cm e 1°; 15,5 cm con 5 cm e 2°. *Controllo:* senza margine 114 e 162 scene su 200 con falsi liberi; con il margine 0 su 200; con 10 cm dove ne servono 15,5, 1 su 200 (B).

**Risposta al punto 3.** Per T2 solo la credenza sull'occupato ha un uso: la memoria degli ostacoli fermi usciti di vista («occupato ricordato» con l'età, che dà un nome a una parte di Π), il filtro dei colpi spuri per gli avvisi, il veto. Alla sicurezza nel modello lo strato probabilistico non aggiunge niente. Il valore delle osservazioni passate sta nella ricorsione: con il 5 % di buchi per cella Π tiene l'84,9 % e il 74,3 % del dichiarabile, la regola a un solo fotogramma il 27,5 % e l'1,3 %. Quel valore però scade: con una camera frontale a 3 m l'età utile massima di un «libero» è 0,17 s a 2,5 m/s e 0,48 s a 1,4 m/s (E).

**Guadagno.** 0 falsi liberi nel modello contro 45 829 (nucleo-simile) e 138 230 (Bayes); K-015 e K-016 chiuse per costruzione, perché l'ombra è Π anche senza traccia. **Il guadagno non richiede i voxel:** Π si mette anche sulla griglia polare del nucleo. Il 3D toglie da H2 l'ipotesi «gli oggetti stanno sul piano» (deduzione, non misura). **Costo e vincoli.** Il libero garantito è quasi vuoto a passo d'uomo (§4): l'uscita utile è T_i, non un «libero» binario. Le leve sono h, la portata e una v_max dichiarata per profilo: per la conciliazione con la traccia, la v_max è il parametro che distingue una stazione fissa in ambiente industriale da un ausilio alla persona. La dilatazione quadrata è per eccesso fino a √2. **Chi la prova:** avversario e validazione nel loro simulatore, poi la camera. **Falsificatore (meno di 1 minuto):** `timeout 120 python3 verifica_strati.py A 24`; atteso 0 falsi liberi e 0 celle occupate fuori da Π; smentita con una sola cella.

### matematico-2 — filtro a 4 stati più intervallo di quota; 6 stati solo in volo

**Enunciato.** Per gli oggetti a terra resta [x, y, vx, vy] con l'attributo [z_min, z_max] del gruppo. Lo stato a 6 si usa solo per bersagli staccati dal suolo, con aggiornamento parziale: se il gruppo tocca il bordo verticale del campo, z e vz non si aggiornano e l'uscita dice «quota non osservabile». Nessuna previsione balistica dichiarata. **Guadagno:** nessuno stato non osservabile dichiarato stimato; la porta d'associazione non cresce da 5,991 a 7,815 (95 %); a 1 s senza misure la regione è 1,95 m² nel piano contro 3,04 m³. **Vincoli:** i bersagli in volo restano fuori dalla demo. **Chi:** esperto di scene dinamiche. **Falsificatore:** `python3 verifica_strati.py D`; attesi ranghi 4, 6, 4 e t* = 0,169 s; smentita con rango 6 senza la quota.

## 6. Dopo

1. Al gruppo strutture dati: misurare la griglia densa a 2 byte contro la sparsa, sapendo che il limite è 3,8 volte.
2. All'avversario: attaccare T1 con profondità valide e sbagliate (vetro, bordi) e con buchi a livello di pixel; serve una F(t) che tolleri buchi più stretti dell'oggetto minimo, che non ho provato.
3. All'arbitro: decidere se l'uscita «nessun ostacolo osservato fino a d metri» porta anche il tempo di garanzia.
4. Rifare il controllo in 3D con il simulatore della validazione.

**Fonti.** Parametri di OctoMap: https://github.com/OctoMap/octomap/blob/devel/octomap/src/AbstractOccupancyOcTree.cpp (aperta oggi). Stati nascosti sovrastimati con insiemi raggiungibili: Orzechowski, Meyer, Lauer, 2018, https://arxiv.org/abs/1807.01262 (aperta oggi; solo il riassunto). Che l'aggiornamento in log-odds presupponga una mappa ferma lo affermo a memoria: non verificato su una fonte oggi.
