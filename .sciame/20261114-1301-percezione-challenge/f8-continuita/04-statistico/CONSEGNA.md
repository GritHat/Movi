Canarino: sciame-canarino-20c82ebff50dded3

# Come si valuta la precisione della previsione — `sciame-statistico`, f8, corsia A

## 0. Scostamenti e regole violate

- **Scrittura fuori cartella:** lo strumento di lettura in rete ha salvato da solo un PDF (Gneiting e Raftery) sotto `~/.claude/projects/…/tool-results/`. L'ho solo letto (pagine 359 e 367–370).
- **Previsioni non cieche:** P13 e P14 sono scritte dopo aver visto le prime uscite; `h9_cieco.py` e la riga (d) della prova conforme non hanno previsione. **Mie previsioni smentite:** P1 in una clausola (0,90 contro 0,95 chiede 203 passaggi, non 220–320), P6 in una (rapporto 1,38, non ≥ 1,5), P14 a 1 s (0,848 < 0,85). Un'etichetta di stampa sbagliata è stata corretta e il lancio rifatto: nessun numero cambia.
- **Letture parziali:** di `SPECIALIZZAZIONE.md`, `MOTO_PROPRIO.md`, `PIANO_MISURE.md`, della consegna Kalman di f1 e della proposta ho letto solo le righe citate; non ho letto `AUDIT.md`, `CONTROPROVE.md`, `MISURE.md`. Lunghezza al limite delle tre pagine.
- **Che cosa condividono le mie prove con l'oggetto:** il filtro `Ax` e i generatori `g1`, `g2` sono quelli del torneo (`f2/04-torneo/torneo_parte2.py`, importato in sola lettura): le mie cifre **ripetono** il torneo con altri semi, non lo confermano in modo indipendente. Mie sono le misure, le miscele e la «capsula», disegnata conoscendo le classi di `g1`. **Niente geometria:** nessuna ombra, nessun ritaglio, nessun «esce dal lato lontano», nessun «rallenta». Tutto è simulazione.
- Per rifare: `sh rifai.sh` (sette lanci, il più lungo 8 s; un secondo lancio ha ridato uscite identiche). Previsioni ed esiti: `PREVISIONI.md`.

## 1. Risposta a Q3, per le parti che mi competono

| Parte | Esito | Prova |
|---|---|---|
| Nucleo, controllo 1 (continuità) | **non rispettato** | la stima è emessa per 0,40–0,53 s su 1,07–1,13 s di buio: il 35–50 % (`MISURE_V2.md`, P4); circa il 10 % in sosta e il 20 % per chi torna (`v2_C6.txt`). Rapporti di mediane: derivati, non misurati |
| Nucleo, controllo 2 (efficacia) | **in parte** | batte «fermo» sulla miscela (mediana 0,50 contro 2,48 m a 2 s), ma il suo punto **è** la linea di base a velocità costante, e per chi torna è peggiore di «fermo» da 2 s (1,78 contro 1,29 m). Nessun file lo misurava (P2) |
| Nucleo, controllo 3 (taratura) | **non rispettato** | §2, critiche 1–3 |
| Nucleo, controllo 4 (incertezza controllata) | **non rispettato come visualizzazione** | il raggio al 90 % è 0,81 / 1,91 / 3,29 / 6,72 m a 1 / 2 / 3 / 5 s (`out_misure.txt`); il nucleo lo limita spegnendo l'area, non cambiando segno |
| Criteri di accettazione (H9) | **non rispettato** | critica 4 |
| Sensore in moto | **in parte** | il requisito «copertura ≥ 0,90 (da 0,92)» (`MOTO_PROPRIO.md`, riga 64) parte dalla media che nasconde 0,56 |
| Specializzazione | **non rispettato** | «la durata del previsto non ha un valore proposto»; per le classi veloci «si riduce a un istante» (`SPECIALIZZAZIONE.md`, riga 83) |
| Documento per l'utente (v0.5) | **rispettato come dichiarazione, non come contenuto** | dice che il punto è in revisione (`proposta_sciame.tex`, riga 94); non riporta nessuna cifra di precisione della previsione |

## 2. Critiche, con la prova e con il modo di misurare

**Unità e misure (valgono per tutto ciò che segue).** L'unità è **il passaggio** (un'occlusione di una traccia confermata), con un solo valore per fascia d'orizzonte. Misure: (a) **copertura** a livello p: quota dei passaggi in cui la posizione (in simulazione) o la prima misura (sull'hardware) cade nella regione dichiarata, con l'intervallo di Wilson; (b) **diagramma di affidabilità**: la copertura osservata almeno ai livelli 50 e 90 %; (c) **nitidezza**: area della regione mostrata, in m² e in quota dell'ombra; (d) **punteggio proprio**: CRPS per componenti, in metri (forma chiusa per la gaussiana; per un punto vale l'errore assoluto, quindi confronta anche le linee di base), come abilità rispetto a «fermo con dispersione tarata»; punteggio d'energia per regioni a campioni, punteggio dell'intervallo per le sole regioni; (e) **errore del punto**: mediana e 90° percentile, appaiato con le linee di base. Tutto per fascia d'orizzonte **e** per comportamento.

Il cerchio del nucleo (q = 0,2) su `g1`, 1500 passaggi per classe (`out_misure.txt`; Wilson per classe entro ± 0,025):

| Buio | Raggio 90 %, area | Copertura al 90 %: miscela · prosegue · sosta · torna · svolta | Al 50 %, miscela | Errore del punto, mediana / 90° (fermo) | Abilità CRPS: miscela · torna |
|---|---|---|---|---|---|
| 1 s | 0,81 m, 2,0 m² | 0,915 · 1,000 · 0,867 · **0,603** · 0,829 | **0,798** | 0,24 / 0,74 m (1,30 / 1,75) | +0,69 · +0,04 |
| 2 s | 1,91 m, 11,4 m² | 0,903 · 1,000 · 0,863 · **0,536** · 0,801 | **0,788** | 0,50 / 1,88 m (2,48 / 3,39) | +0,60 · **−0,38** |
| 3 s | 3,29 m, 34,0 m² | 0,919 · 1,000 · 0,943 · **0,531** · 0,831 | **0,799** | 0,77 / 2,97 m (3,70 / 5,03) | +0,56 · **−0,64** |
| 5 s | 6,72 m, 141,7 m² | 0,942 · 1,000 · 1,000 · **0,579** · 0,897 | 0,851 | 1,40 / 4,98 m (6,04 / 8,35) | +0,53 · **−0,74** |

1. **La copertura «0,89–0,93» è una proprietà della miscela, non del predittore.** Con le coperture per classe del torneo a 2 s (1,000 / 0,955 / 0,561 / 0,839, `risultati_A_parte2.txt`) la media vale 0,996 per una squadra che cammina dritta (90/10/0/0), 0,925 per la miscela del torneo, 0,887 per un giurato (50/20/20/10), 0,785 se ci sono solo manovre (`out_tabelle.txt`). Il «giusto» nasce da due errori di segno opposto: 1,000 dove ne basterebbero 0,90, 0,54 su chi torna (nel nucleo con C6: 0,47–0,50, Wilson [0,42; 0,55], `v2_C6.txt`).
2. **Al 50 % la regione contiene il 79 %.** Nessun file aveva un secondo livello: la taratura era letta in un solo punto del diagramma. E resta sotto il nominale: ricalcolando da quei conteggi, il limite superiore di Wilson sta sotto 0,95 in 7 celle su 7 (P4).
3. **Taratura e prova non erano separate.** q = 0,2 è stato scelto fra 0,1, 0,2 e 0,5 sugli stessi tre generatori su cui si riporta la copertura (`TORNEO.md`, K-003). Cambiando generatore senza ritarare, una soglia conforme tarata su `g1` dà su `g2` 0,864–0,888 invece di 0,90 (`out_incrociata.txt`).
4. **Il criterio H9 non può fallire per il comportamento coperto peggio.** Con 21 prosegue, 5 soste e 4 ritorni, i due stadi (≥ 28 su 30; altrimenti ≥ 52 su 60) danno «regge» con probabilità **1,000** se chi torna è coperto al 50 %, e ancora 1,000 se non è coperto mai: 26 su 30, poi 52 su 60 (`h9_cieco.py`, conto esatto; ridà l'86,5 % e il 14,2 % del metrologo). Notato dopo, senza previsione.
5. **Il controllo 3 del contratto, letto come «copertura vicina a p in ogni comportamento», non è soddisfacibile.** Il comportamento nel buio non è noto quando si prevede: è condizionare sull'esito (già sulle grandezze note la copertura condizionata esatta è impossibile senza ipotesi: Barber e altri). Va letto come **pavimento**: almeno p in ogni comportamento dichiarato. Il prezzo è misurato: un disco che copra al 90 % tutte e quattro le classi è 3,5–4,8 volte l'area del cerchio a 2 s (`out_conforme.txt`, c).
6. **I fotogrammi non sono campioni.** Correlazione intraclasse 0,21 a 1 s e 0,51 a 3 s: 15 fotogrammi ne valgono 3,9 e 45 ne valgono 1,9; contandoli, l'errore tipo esce 2,0 e 4,9 volte troppo piccolo (`out_fotogrammi.txt`).
7. **Trenta occlusioni non distinguono 0,90 da 0,80.** Servono 89 passaggi per cella (203 per distinguere 0,90 da 0,95; potenza 0,80, alfa 0,05, binomiale esatta). Con 30 la potenza è 0,39 e 27 su 30 dice «fra 0,74 e 0,97». Con 12 celle giudicate insieme (z = 2,87), 90 su 100 dice «fra 0,78 e 0,96».
8. **La previsione conforme garantisce solo sotto scambiabilità.** Riprodotto qui in simulazione: con n passaggi di taratura la copertura realizzata segue Beta(k, n+1−k), k = ⌈0,9·(n+1)⌉; 5° percentile 0,803 con n = 30 (teoria 0,805), 0,851 con n = 100 (0,848). Per stare sopra 0,85 con probabilità 0,95 servono 68 passaggi; sotto 9 la soglia è infinita. **Si rompe** se il giurato cammina diversamente: tarata sulla squadra, sul giurato copre 0,72 / 0,66 / 0,64 a 1 / 2 / 3 s. Una soglia unica per tutti gli orizzonti dà fra 0,873 e 0,935: serve una soglia per fascia. Condizionare sul comportamento visto prima dell'occlusione: **non verificato** (in `g1` la manovra non dipende dal tratto visibile).
9. **Con una sola camera, durante il buio la verità non esiste.** Sul pannello vero si misura solo alla ricomparsa, dove orizzonte e comportamento sono confusi (1,1 s chi prosegue, 2,2 s chi torna, 5,1 s chi sosta).

## 3. Stati proposti

| Enunciato | Stato |
|---|---|
| «Il cerchio del filtro è tarato» | **smentito** per comportamento e al livello 50 %; **sostenuto dai dati** solo come media su miscele simili a 60/15/10/15, in simulazione |
| Il nucleo rispetta i controlli 1, 3 e 4 | **smentito** (il 1 per derivazione dai file) |
| H9 come accettazione della precisione | **smentito** (calcolo esatto) |
| Garanzia conforme in campione finito | **dimostrata** nel modello scambiabile (letteratura: letto solo il riassunto) e **sostenuta** dalla mia simulazione; fuori da quel modello **smentita** (0,66 sul giurato) |
| Massimo sulle classi: ≥ 0,90 su ogni miscela delle classi tarate | **dimostrato** (combinazione convessa) se le classi di prova sono quelle tarate; **sostenuto** su `g1` (0,89–0,91). Il trasferimento a un altro generatore è **smentito** sotto 1 s (su `g2`, con manovra: 0,848 a 1 s, 0,738 a 0,5 s) |
| Copertura su persone e camera vere; con la geometria dell'ombra; chi esce dal lato lontano | **non risolto**: decide il protocollo del §5 e P15 |

## 4. Proposte per Q4

**`statistico-1` — il livello dichiarato è un pavimento per comportamento, ottenuto per taratura conforme.** Sopra qualunque predittore, la regione «90» è {s ≤ ŝ}: s è un punteggio fissato prima (nella prova: il minimo fra distanza/raggio del filtro e il punteggio di una capsula lungo l'asse del moto, che copre chi prosegue, sosta o torna); ŝ è, per fascia d'orizzonte, il **massimo sulle classi prescritte** del quantile conforme, con 30–50 passaggi di taratura per classe diversi da quelli di prova. La regione si ritaglia poi sul non osservato e si dichiara «almeno 90 % per ciascun comportamento tarato», con la cifra realizzata a schermo.
- *Prima → dopo* (`out_unione.txt`, `out_incrociata.txt`): classe peggiore 0,60 / 0,54 / 0,53 → **0,89 / 0,90 / 0,91** a 1 / 2 / 3 s; «giurato» 0,88 / 0,86 / 0,88 → 0,98; su `g2`, senza ritarare, con manovra nel buio 0,66 / 0,79 / 0,83 → 0,85 / 0,92 / 0,93. *Prezzo:* area 2,6 / 2,3 / 1,8 volte il cerchio, prima del ritaglio.
- *Vincoli:* nessun modello appreso; un ordinamento fuori linea e un confronto per ciclo; non toglie mai un avviso. Non copre comportamenti non tarati né manovre più brusche di quelle tarate. Con 50 passaggi per classe il 5° percentile della classe peggiore è 0,82–0,85.
- *Chi:* validazione o avversario, con `scena_parte3.py`. *Falsificatore (5 minuti), P15 scritta prima:* tarata su `g1` e provata su `g3` con l'ombra, «torna» ≥ 0,85 in ogni fascia da 0,75 s (oggi 0,06 / 0,09 / 0,34 / 0,79); smentita sotto 0,80.

**`statistico-2` — una scheda di valutazione fissata prima, e un criterio stratificato al posto di H9.** Si scrivono prima: celle, livelli, soglie, numerosità, semi. Tre insiemi (sviluppo, taratura, prova toccata una volta); almeno due generatori non scritti dall'autore del predittore, taratura su uno e prova sull'altro, con miscele diverse; linee di base: fermo, velocità costante (il nucleo di oggi), fermo con dispersione tarata, disco raggiungibile ritagliato; un braccio che deve fallire (q = 0,01: 0,71–0,74 nel torneo). Soglie proposte:

| Controllo | Misura, per passaggio | Soglia | Oggi |
|---|---|---|---|
| 1 | passaggi con un ciclo senza stima prima della ricomparsa o di una chiusura dichiarata | 0 su 300 per comportamento (limite 1 %) | stima per il 10–50 % del buio |
| 2 | errore del punto e abilità CRPS, per fascia e comportamento | mediana ≤ 0,5 m (un corpo) fino a 2 s; mai oltre 1,2 volte la migliore linea di base; abilità > 0 in ogni cella | 0,50 m; torna 1,38 volte e −0,38 |
| 3 | copertura «90» per cella (n ≥ 400, ± 0,03); «50» sulla miscela | ≥ 0,85 in ogni cella; «50» fra 0,40 e 0,60; area ≤ 3 volte il cerchio di oggi | 0,53–0,60; 0,79 |
| 4 | area su celle viste libere; cicli oltre la soglia in cui la stima resta, con altro segno; passaggi in cui il ritaglio toglie il vero | 0; 100 %; 0, con il braccio «ombra a −20 cm» che deve fallire | per costruzione; 0 %; non misurato |

Sull'hardware: 30 passaggi **per comportamento**, giudicati ciascuno: ≥ 28 regge, ≤ 23 smentita, altrimenti altri 30. *Guadagno:* con chi torna coperto al 50 % la smentita esce nel 99,9 % dei casi (H9: mai); una taratura vera di 0,90 è smentita per errore nel 2,6 %. *Vincolo:* «regge» esce solo nel 41 % dei casi a 0,90 vero e nell'81 % a 0,95. *Chi:* metrologo. *Falsificatore (5 minuti):* la scheda sul simulatore del nucleo, 30 passaggi per classe per 200 ripetizioni; atteso «smentita» su «torna» in almeno il 95 %.

## 5. Protocollo per l'hardware, e che cosa si potrà dichiarare

1. **Occlusione virtuale** per taratura e copertura: camminate in piena vista, mascherate a programma dietro un cuneo finto. Dà la verità a ogni ciclo e a ogni orizzonte; l'unità resta la camminata. Non rappresenta l'occlusione parziale (C6): per quella, il pannello vero alla ricomparsa.
2. **Numeri:** taratura 4 comportamenti × 30 (meglio 50), prova 4 × 30 con almeno un camminatore fuori dalla taratura: 240 camminate, circa 80 minuti in due (stima mia, non misurata).
3. **Che cosa si dichiara:** per comportamento, 27 su 30 → «fra 0,74 e 0,97»; «almeno 0,80» solo con 28 su 30; sull'insieme, 108 su 120 → «fra 0,83 e 0,94». Mai «tarato al 90 %». Un contatore dal vivo («regione al 90 %: dentro k su n») mostra alla giuria la precisione realizzata.

## 6. Dopo

Eseguire P15; far passare ogni predittore delle altre corsie per la stessa scheda (`misure_f8.py`, funzione `riga`), con semi congelati; aggiungere geometria, ritaglio e «esce dal lato lontano». L'adattamento in linea della soglia (Gibbs e Candès) è **non verificato** qui.

**Fonti.** Gneiting e Raftery 2007, eq. 21, 22, 43 (lette): https://sites.stat.washington.edu/raftery/Research/PDF/Gneiting2007jasa.pdf. Solo il riassunto: https://arxiv.org/abs/2107.07511, https://arxiv.org/abs/1903.04684, https://arxiv.org/abs/2106.00170.
