# Previsioni — `sciame-pianificatore`, f9, strategia S12

Scritte alle **2026-11-14T15:42:06+01:00** (`date -Is`), dopo aver letto contratto, addendum, preproposta, `SOLUZIONE_V2.md`, `AUDIT.md`, `VERDETTO.md`, `proposta_sciame.tex`, e **prima** di scrivere o lanciare `piano_mc.py`.

## Che cosa avevo già in mano quando le ho scritte (non sono previsioni)

- La tabella a tre punti dei moduli (ottimista / probabile / pessimista, in ore-persona) l'ho fissata a mano prima dello script: è una **stima mia**, non una misura. La somma «probabile» dei moduli aggiunti dal taglio a 24 ore, fatta a mano, dà circa 39 ore-persona; il totale del taglio a 24 ore con integrazione circa 96. Questi due numeri sono conti, non previsioni.
- Il cammino critico a mano del taglio a 24 ore (durate probabili, persone illimitate): circa 38 ore di lavoro in fila.

## La prova

Simulazione Monte Carlo del calendario (`piano_mc.py`, Python puro, seme fissato): grafo dei compiti con dipendenze, durate triangolari (O, P, Pess) moltiplicate per un fattore di velocità k (k = 1: valgono le stime dello sciame; k < 1: la squadra va più svelta), N persone, una sola camera (i compiti con la camera non si sovrappongono), ore utili di lavoro W(D) meno le ore di chiusura (prove generali, video di ripiego, presentazione). Misura: P(sta) = quota delle estrazioni in cui tutto finisce entro le ore utili; k* = il k più grande con P(sta) ≥ 80 %.

Piani a confronto: **PRE24** (il «taglio minimo garantito a 24 ore» della preproposta, con la mia organizzazione a corsie: è già un favore), **MIN** (il mio piano minimo: nucleo ridotto + previsione continua a una ipotesi + sua taratura ridotta), **MED** (MIN + seconda ipotesi con i pesi + livelli).

## Previsioni, con la soglia di smentita

- **PR1.** A k = 1 e D = 24 ore, P(sta) di PRE24 è **sotto l'1 %** con 3, 4 e 5 persone. Smentita se ≥ 10 % per qualche N.
- **PR2.** k* di PRE24 con 5 persone e 24 ore sta fra **0,25 e 0,40** (la squadra dovrebbe andare da 2,5 a 4 volte più svelta delle stime). Smentita se k* ≥ 0,50.
- **PR3.** Per MIN a 24 ore, k* con 4 persone sta fra **0,45 e 0,65**; la quinta persona lo sposta di meno di 0,05 (comanda il cammino critico, non il numero di mani). Smentita se la quinta persona dà ≥ 0,10.
- **PR4.** Per MIN a 24 ore, passare da 3 a 4 persone alza k* di almeno 0,05. Smentita altrimenti.
- **PR5.** A 48 ore e k = 1: MIN con 4 persone sta con P ≥ 80 %; PRE24 con 5 persone sta con P fra il 20 e il 70 %. Smentita fuori da questi intervalli.
- **PR6.** Sensore assente (ripiego su registrazioni o profondità sintetica) contro sensore posseduto: k* di MIN cambia di meno di 0,05; il costo vero non è in ore ma nei requisiti che non si possono più misurare (latenza, perdita di affidabilità, «prima prova sul sensore vero»). Smentita se la differenza è ≥ 0,10.

## Che cosa la prova condivide con ciò che controlla

Le stime a tre punti, il grafo e il simulatore hanno lo stesso autore (io) e lo stesso modello linguistico dello sciame che ha stimato le 54 ore-persona. La prova può quindi smentire solo **l'aritmetica del piano** (somme, cammino critico, effetto del numero di persone), non le stime: quelle le decide la prima tappa di controllo all'hackathon (tempo vero dei primi compiti contro il tempo stimato).

---

# Secondo blocco — scritto alle 2026-11-14T15:45:13+01:00, dopo il primo lancio (`risultati_v1.txt`) e prima del secondo

## Esito del primo lancio (15:44:06–15:44:13, `piano_mc_v1.py` → `risultati_v1.txt`)

- PR1 **regge** (0,0 % con 3, 4 e 5 persone).
- PR2 **non smentita, ma fuori dall'intervallo**: k* = 0,24 (previsto 0,25–0,40; soglia di smentita 0,50).
- PR3 **smentita nell'intervallo** (k* = 0,36 con 4 persone, previsto 0,45–0,65: ero ottimista); **regge** sulla quinta persona (0,36 → 0,36).
- PR4 **smentita**: da 3 a 4 persone k* passa da 0,35 a 0,36 (previsto almeno +0,05).
- PR5 **smentita** due volte: MIN a 48 ore con 4 persone sta nello 0,7 % dei casi (previsto ≥ 80 %); PRE24 a 48 ore con 5 persone nello 0,0 % (previsto 20–70 %).
- PR6 **regge sulla soglia, al limite**: differenza di k* 0,05 a 24 ore, 0,06 a 36, 0,08 a 48 (previsto < 0,05; soglia di smentita 0,10).

## Che cosa ho notato DOPO il primo lancio (non era scritto prima)

1. L'ordine «parte il compito con il cammino residuo più lungo» lascia per ultima l'uscita con i dati finti (gradino 1 completo a 9,8 ore di lavoro con 4 persone, a 16,7 con 3): è il contrario dell'ordine che protegge la demo. Il modello v1 non descrive il piano che propongo.
2. Con una sola camera, taratura e accettazione in fila dopo la prova dal vivo allungano la coda: nel piano vero si registra **una volta** e si analizza in parallelo sulle registrazioni.
3. La media di una triangolare (O, P, 2P) è 1,2 P: per questo la fine mediana (32–33 ore) supera il cammino critico «probabile» (23–27 ore). Le mie previsioni ragionavano sulle durate probabili.

## Modello v2 (modifiche dichiarate, a posteriori)

- Ordine a gradini: prima l'hardware (N1, A1), poi l'uscita con i dati finti, poi le due corsie (mappa vera; traccia, cuneo e previsione continua sul simulatore), poi l'innesto, poi dal vivo.
- Una sola sessione di registrazione (REG, con la camera), poi taratura e accettazione in parallelo sulle registrazioni.
- Tappe misurate una per una (uscita; mappa vera; continuità sul simulatore; catena vera; dal vivo; fine), non più cumulative.
- Stime a tre punti dei compiti: **invariate**.

## Previsioni per il secondo lancio

- **PR7.** MIN, 4 persone, sensore posseduto, k = 1: la tappa «uscita con dati finti» ha mediana ≤ 5 ore di lavoro (9,8 nel v1). Smentita se > 6.
- **PR8.** La sessione unica di registrazione abbassa la fine mediana di MIN (4 persone, posseduto) di 2–5 ore (da 31,8 a 27–30). Smentita se meno di 1 ora.
- **PR9.** Anche nel v2, MIN a 24 ore con 4 persone ha k* ≤ 0,45: la conclusione «il piano minimo non sta in 24 ore alle stime dello sciame» sopravvive. Smentita se k* ≥ 0,60.
- **PR10.** A 24 ore, 4 persone, sensore posseduto: la tappa «continuità sul simulatore» ha k* fra 0,55 e 0,80 (a k = 1 non si raggiunge); «uscita» e «mappa vera» hanno k* ≥ 0,9. Smentita fuori da questi intervalli.

---

# Terzo blocco — scritto alle 2026-11-14T15:46:58+01:00, dopo il secondo lancio (`risultati_v2.txt`, 15:46:07–15:46:15) e prima dell'ablazione

## Esito del secondo lancio

- PR7 **smentita**: «uscita con dati finti» a 8,0 ore di lavoro (mediana, 4 persone), non ≤ 5. Causa: è una catena (interfacce → schermo → disegno della previsione: 1 + 3 + 2,5 ore probabili, per 1,2), non un problema di mani.
- PR8 **smentita, ma confusa**: la fine mediana di MIN resta 31,9 ore (31,8 nel v1). Il v2 cambia insieme l'ordine e la sessione di registrazione: i due effetti non sono separati. Li separa l'ablazione qui sotto.
- PR9 **regge**: k* = 0,36 (4 persone, 24 ore).
- PR10 **smentita di poco** sulla continuità (k* = 0,53, previsto 0,55–0,80); **regge** su «uscita» (1,41) e, al limite, su «mappa vera» (0,90).

## Notato dopo (non scritto prima)

L'ordine «prima tutta l'uscita» fa partire tardi la corsia più lunga, quella della continuità (traccia → cuneo → previsione: 13 ore probabili in fila): con 4 persone la continuità sul simulatore arriva a 21,2 ore di lavoro.

## Ablazione (`ablazione.py` → `risultati_ablazione.txt`): tre ordini sullo stesso grafo v2, piano MIN, sensore posseduto

(a) «rango» (ordine del v1); (b) «gradini» (v2); (c) «due corsie dall'ora 1»: una persona fissa sulla corsia della continuità (N4r, N5, C1 nella stessa classe dell'uscita).

- **PR8bis.** Con l'ordine (a) e il grafo v2, la fine mediana di MIN con 4 persone è fra 27 e 30 ore (effetto isolato della sessione unica: 2–5 ore in meno rispetto a 31,8). Smentita se > 30,8.
- **PR11.** Con l'ordine (c) e 4 persone: «continuità sul simulatore» a ≤ 18 ore di lavoro (mediana; 21,2 con i gradini) e «uscita» a ≤ 9,5 (8,0 con i gradini). Smentita se la continuità guadagna meno di 2 ore o l'uscita perde più di 2,5.

---

# Quarto blocco — esito dell'ablazione, scritto alle 2026-11-14T15:51:01+01:00

Lancio di `ablazione.py` dalle 15:46:58 alle 15:47:09 → `risultati_ablazione.txt`.

- PR8bis **regge**: ordine (a) sul grafo v2, MIN con 4 persone, fine mediana 29,3 ore (31,8 nel v1): la sessione unica di registrazione vale circa 2,5 ore.
- PR11 **regge**: ordine (c), 4 persone: «continuità sul simulatore» a 17,0 ore (21,3 con i gradini: 4,3 ore guadagnate), «uscita» a 9,1 (7,9 con i gradini: 1,2 perse).

Conta esatta aggiunta dopo, senza previsione (`conta_pre24.py` → `risultati_conta_pre24.txt`, 15:50): il taglio a 24 ore della preproposta sta in 0 estrazioni su 4000 in tutte le 27 celle del modello v2; il rapporto massimo fra ore disponibili e ore necessarie a 48 ore è 0,65–0,75.

Bilancio delle 12 previsioni: reggono PR1, PR9, PR8bis, PR11; reggono sulla soglia ma fuori dall'intervallo previsto PR2 e PR6; smentite PR3 (nell'intervallo; regge sulla quinta persona), PR4, PR5, PR7, PR10 (di poco, sulla continuità); PR8 confusa da due modifiche insieme, separata da PR8bis.
