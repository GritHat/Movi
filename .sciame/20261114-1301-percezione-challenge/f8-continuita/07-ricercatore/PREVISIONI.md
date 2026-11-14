# PREVISIONI — sciame-ricercatore, f8 (continuità visiva), corsia A

Scritte alle **2026-11-14T15:14:49+01:00** (`date -Is`), PRIMA di ogni ricerca in rete e di ogni calcolo di questa
estensione. Che cosa avevo già visto: il contratto f8, la traccia, gli addendum, `SOLUZIONE_V2.md`, `VERDETTO.md`,
la mia consegna f1 (`f1/3fff79e9c3ea/`), `FONTI_VERIFICATE.md` di f3, e le righe di `TORNEO.md` con le coperture
(0,89–0,93; torna 0,56–0,66; particelle 98–100 %; lato lontano 22–41 %). Nessuna pagina in rete aperta oggi per f8.
Ciò che so a memoria su questi temi (limite di conoscenza: metà 2026) è un pregiudizio dichiarato, non una prova.

## Sulla letteratura (la prova è la fonte aperta)

- **P1 — taratura dei predittori appresi.** Misura: numero di fonti primarie aperte che riportano una misura di
  taratura (copertura, diagramma di affidabilità, ECE, NLL per orizzonte) per predittori di traiettorie di pedoni o
  veicoli. Attesa: ne trovo almeno 2, e dicono che i predittori appresi, senza ritaratura, sono mal tarati (di
  norma troppo sicuri). **Smentita se:** ne trovo 0, oppure le fonti aperte dicono che sono già tarati senza
  correzione.
- **P2 — previsione conforme sulle traiettorie.** Attesa: esistono almeno 2 lavori primari (2021–2026) che applicano
  la previsione conforme a traiettorie con più passi; la garanzia è marginale e vale sotto scambiabilità; nelle
  prove sugli stessi dati la copertura empirica sta entro 5 punti dal nominale. **Smentita se:** non ne trovo, o la
  copertura riportata in distribuzione sta più di 5 punti sotto il nominale.
- **P3 — il modello appreso aggiunge qualcosa di provato?** Attesa: NON trovo nessuna fonte primaria che mostri,
  insieme, (a) un predittore appreso che gira su CPU ad almeno 15 Hz, (b) errore più basso della velocità costante
  o del Kalman su occlusioni di 0,5–3 s di pedoni, (c) una misura di taratura migliore. **Smentita se:** trovo una
  fonte con le tre cose. (Una fonte con la sola (b) su GPU sposta la risposta a «promettente, non provato qui».)
- **P4 — verità di riferimento durante l'occlusione.** Attesa: trovo almeno 2 insiemi di dati con la posizione vera
  durante l'occlusione (attesi: TAO-Amodal, un insieme sintetico), e trovo che il banco TAP-Vid NON valuta la
  posizione dei punti quando sono occlusi (valuta solo il segnale «occluso»). **Smentita se:** meno di 2 insiemi, o
  TAP-Vid valuta la posizione in occlusione.
- **P5 — traccia «in coasting» nel controllo del traffico aereo.** Attesa: nello standard ASTERIX categoria 062
  (tracce di sistema, EUROCONTROL) esistono (a) un bit che dichiara la traccia estrapolata/in coasting e (b) un
  campo con l'accuratezza stimata della traccia. **Smentita se:** la specifica aperta non li contiene.
- **P6 — errori d'interpretazione.** Attesa: per gli operatori vedenti trovo almeno 1 studio primario con numeri
  sugli errori di lettura di una regione d'incertezza (atteso: il «cono» degli uragani letto come dimensione
  della tempesta); per le persone non vedenti trovo al più 1 studio su una previsione continua con incertezza
  comunicata (attesa: lacuna). **Smentita se:** nessuno studio per i vedenti, oppure 2 o più studi controllati per
  i non vedenti.

## Sul falsificatore di `ricercatore-1` (lo eseguo io, se resta tempo; altrimenti resta scritto)

Enunciato in prova: «un raggio tarato in modo conforme **per tempo senza osservazione** sui residui di un
predittore a velocità costante dà la copertura nominale in media, ma non per comportamento».
Prova: Python puro, semi fissati, al più 2 minuti. Generatore mio (dichiarato: NON indipendente da me; indipendente
dal filtro del nucleo), miscela prosegue / rallenta / si ferma / torna indietro / svolta; taratura su un insieme,
prova su un altro con semi diversi; livello 90 %; tempi senza osservazione 0,5, 1, 2, 3, 5 s.
- **P7a.** Copertura marginale sull'insieme di prova a ogni tempo: fra 0,88 e 0,92. **Smentita se:** fuori da
  0,87–0,93 in almeno un tempo.
- **P7b.** Copertura di «torna indietro» a 2 s con il raggio marginale: sotto 0,75. **Smentita se:** ≥ 0,80
  (allora la taratura marginale basterebbe e la mia critica cade).
- **P7c.** Con il quantile preso sul comportamento peggiore (taratura a gruppi, «Mondrian»), ogni comportamento
  è coperto ad almeno 0,88, e il raggio a 2 s cresce di almeno il 30 % rispetto al marginale. **Smentita se:** un
  comportamento resta sotto 0,87, o la crescita è sotto il 30 %.
- **P7d.** Cambio di miscela fra taratura e prova (torna indietro dal 10 % al 30 %): la copertura marginale del
  raggio marginale scende sotto 0,87 a 2 s; quella del raggio «comportamento peggiore» resta ≥ 0,88.
  **Smentita se:** una delle due non accade.
Esiti possibili: regge, smentita, non risolta (se lo script non gira nei due minuti).

---

# ESITI (scritti alle 2026-11-14T15:20:47+01:00, DOPO le ricerche e DOPO il lancio; le previsioni sopra non sono state toccate)

Sigle delle fonti: vedi `FONTI.md`. Lancio: `timeout 120 python3 -I conforme_orizzonte.py > risultati_conforme.txt`
(partito alle 2026-11-14T15:19:48+01:00, 4,9 s, uscita 0).

| Previsione | Esito | Prova |
|---|---|---|
| P1 taratura dei predittori appresi | **regge, con una correzione** | 2 fonti aperte con una misura (S1: Trajectron++ affidabilità media 64,9 %, minima 30,9 % su ETH/UCY; «None of the tested models can achieve suitable Reliability scores»; S2: la perdita NLL «is prone to predict over- or under-confident distributions»). Correzione: le fonti dicono «troppo o troppo poco sicuri», non solo «troppo sicuri» |
| P2 previsione conforme sulle traiettorie | **regge** | 3 lavori aperti (S4, S5, S6); garanzia sotto estrazioni indipendenti dalla stessa distribuzione (S4, ipotesi 2); copertura empirica 498 su 500 (99,6 %) al nominale 95 %: 4,6 punti SOPRA, per il limite d'unione sui passi |
| P3 il modello appreso aggiunge qualcosa di provato | **regge come assenza di prova** (ricerca non esaustiva: 17 interrogazioni) | nessuna fonte con (a)+(b)+(c). Contro, in parte: sui veicoli in autostrada l'appreso batte il Kalman a velocità costante (S9: RMSE 0,67 contro 0,75 m a 1 s; 6,26 contro 6,70 a 5 s; NLL migliore), senza occlusione e senza CPU; sui pedoni S7 e S8 danno la velocità costante alla pari; S10: il Kalman batte i predittori appresi «up to 34% of cases» anche su moto non lineare |
| P4 verità di riferimento durante l'occlusione | **regge** | S11 (sintetico con «ground truth annotations for invisible objects»), S12 (TAO-Amodal), S13 (MOT17: rapporto di visibilità per ogni riquadro vero), S14 (TCOW); S15: TAP-Vid valuta la posizione «only for frames where the point is visible» |
| P5 coasting in ASTERIX 062 | **regge** | S16: bit CST in I062/080; I062/500 «Estimated Accuracies»; I062/290 età degli aggiornamenti. Letto su una copia strutturata della specifica (edizione 1.18), non sul PDF ufficiale |
| P6 errori d'interpretazione | **regge** | vedenti: S19 (N = 179: «la tempesta cresce» 0,70 col cono contro 0,39 con le traiettorie, d = 0,66). Non vedenti: 0 studi con un'incertezza comunicata (S20: 6 persone, estrapolazione lineare a 5 s, nessuna incertezza in uscita; S21: nessun numero sugli utenti) |
| P7a copertura marginale 0,88–0,92 | **regge** | 0,907 / 0,906 / 0,903 / 0,900 / 0,897 a 0,5 / 1 / 2 / 3 / 5 s (N = 40 000, ± 0,003) |
| P7b «torna indietro» a 2 s sotto 0,75 col raggio marginale | **regge** | 0,455 (a 3 s 0,307; a 5 s 0,267) |
| P7c raggio «comportamento peggiore»: tutti ≥ 0,88, raggio a 2 s +30 % | **regge, di poco** | minimo 0,885 (torna, 5 s; taratura su circa 400 casi per gruppo); raggio a 2 s 2,92 m contro 1,85 (× 1,58) |
| P7d miscela spostata (torna dal 10 al 30 %) | **regge** | a 2 s: marginale 0,796; peggiore 0,972 |

## Notato DOPO (non previsto: vale come osservazione, non come conferma)

1. Il raggio che copre al 90 % ogni comportamento è 0,64 m a 1 s, 2,92 m a 2 s, 5,82 m a 3 s, 12,2 m a 5 s: da 2 s in
   poi supera la griglia del nucleo (3 m). In campo aperto una regione tarata per comportamento è quasi tutto il
   raggiungibile: la limita solo ciò che il sensore vede.
2. Il cerchio nominale del Kalman con q = 0,2 (solo il termine q·τ³/3, livello 90 %) sul mio generatore: copre 0,999
   a 0,5 s (raggio 0,20 m contro 0,11 del conforme: largo quasi il doppio), 0,956 a 1 s, 0,851 a 2 s, 0,824 a 3 s; per
   «torna» 0,832 / 0,291 / 0,108 a 1 / 2 / 3 s. Stesso segno del torneo (torna 0,56–0,66 al 95 %), numeri diversi
   perché generatore e livello sono diversi.
3. «Fermo all'ultima posizione» batte la velocità costante per chi si ferma e per chi torna da 2 s in poi (a 2 s:
   1,04 contro 1,38 m e 0,74 contro 1,99 m); in media vince la velocità costante (0,75 contro 1,99 m a 2 s).
4. Al livello 50 % il raggio marginale a 2 s (0,45 m) copre l'83 % di chi prosegue e lo 0 % di chi si ferma, torna o
   svolta: un «nucleo al 50 %» a un solo modo è la regione di chi prosegue, non una regione al 50 % per tutti.

---

# Previsioni per i falsificatori delle due proposte (scritte alle 2026-11-14T15:23:11+01:00, prima della consegna; NON eseguiti da me)

- **P8 — falsificatore di `ricercatore-1`** (lo esegue un altro ruolo, con i generatori del torneo, non con il mio).
  Tabella dei raggi tarata su due generatori del torneo (G1, G2), provata sul terzo (G3), livello 90 %, tempi 0,5–3 s.
  Attesa: con il raggio «comportamento peggiore» ogni comportamento presente nella taratura è coperto ad almeno 0,85
  su G3; con il raggio marginale almeno un comportamento scende sotto 0,75 a 2 s. **Smentisce la proposta:** un
  comportamento di G3 sotto 0,80 con il raggio «comportamento peggiore» (allora la taratura a gruppi non si
  trasferisce fra generatori e serve altro). **Smentisce la mia critica 2:** tutti i comportamenti ≥ 0,85 già con il
  raggio marginale.
- **P9 — falsificatore di `ricercatore-2`** (controllo dello schema d'uscita su un registro di cicli in occlusione).
  Attesa sul nucleo com'è (versione 2), occlusione di 3 s: fra il 77 e l'87 % dei cicli senza osservazione non ha
  né posizione stimata né precisione dichiarata [conto mio: (3 − 0,7)/3 e (3 − 0,4)/3]. Attesa dopo la modifica:
  0 cicli senza i cinque campi, e 0 cicli con «osservato» senza misura. **Smentisce:** un solo ciclo senza campi dopo
  la modifica, o un solo ciclo «osservato» senza misura.
