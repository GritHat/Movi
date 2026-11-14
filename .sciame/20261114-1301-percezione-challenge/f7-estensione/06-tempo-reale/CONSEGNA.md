Canarino: sciame-canarino-55f6adcfa718b00e

# Consegna — `sciame-tempo-reale`, estensione f7, corsia A: la mappa voxel sta nel tempo?

File, tutti in questa cartella: `banco.c` (micro-banco in C), `rifai.sh <parte>` (comando per rifare), `risultati_*.txt`, `PREVISIONI.md` (19 previsioni con l'ora, e gli esiti).

## 0. Scostamenti e regole violate

- **Dove valgono i tempi.** Un portatile (Ryzen AI 9 HX 370), un filo, gcc 16.2.1 `-O2`, core a **3,30 GHz** letti durante il lancio; profondità **sintetica** 640×480 (87°×58°, sensore a 1,2 m inclinato di 15°, rumore 0,00375·z²); regione 6×4×3 m; 8 byte per voxel; 240 fotogrammi per configurazione. **Non è la macchina di destinazione né il linguaggio del prototipo**: nessun tempo qui è una garanzia.
- **Previsioni smentite: 4 su 19.** P1 (voxel per raggio: 108 e 54, attesi 40–90 e 20–45); P8 per i blocchi (nessun picco d'allocazione); P14 (core «lento» uguale al «veloce»: giravano alla stessa frequenza); P15 (proiezione «lasca»: 45,6 % dei liberi, attesi ≥ 60 %). P13 e P17 reggono sulla soglia, con l'attesa numerica mancata.
- **Aggiunte dopo i primi risultati**, ciascuna con la previsione scritta prima del lancio: il metodo Q, il conteggio senza pavimento, il modo «vecchi», la lettura con contraddizione.
- I file `risultati_tempo`, `_lasca`, `_lento`, `_interf`, `_tetto` vengono da un binario precedente all'ultima modifica: la concordanza con il binario finale è sotto la tabella.
- Per leggere la frequenza ho lanciato due volte il banco in sottofondo a 4 s di distanza: «uno alla volta» è rispettato solo di misura.
- La pagina di ROS 2 sulla qualità del servizio è stata negata: ciò che dico sulle code è scelta di progetto, **non verificata** sulla fonte.
- Indipendenza: banco, scene, rumore e conteggi sono dello stesso autore; gli «0 per costruzione» sono controlli di coerenza, non dati.
- Lunghezza: circa 2 250 parole, al limite delle tre pagine.

## 1. Bilancio e critiche (a `promptMare.txt` e al nucleo)

Scena «vuota» (i raggi più lunghi: è il caso peggiore), ms per fotogramma, media / p95 / massimo. Periodo a 15 Hz: 66,7 ms.

| Metodo | 5 cm (576 000 voxel, 4,61 MB) | 10 cm (72 000, 0,58 MB) | Aggiornamenti per fotogramma |
|---|---|---|---|
| Griglia polare del nucleo, in C | 0,50 / 0,50 / 0,53 | — | 307 200 pixel → 2 610 celle |
| Raggi, matrice densa, tutti (k = 1) | **88,9 / 90,2 / 91,1** | 49,2 / 50,9 / 51,9 | 33,3 M e 16,5 M (108 e 54 voxel per raggio) |
| Raggi, uno ogni 2×2 pixel | 24,7 / 25,5 / 26,2 | 14,9 / 15,0 / 15,1 | 8,3 M e 4,1 M |
| Raggi, uno ogni 4×4 pixel | 8,1 / 8,7 / 9,2 | 5,5 / 5,6 / 5,6 | 2,1 M e 1,0 M |
| Raggi, blocchi 8³ con hash, k = 1 | 135,5 / 136,3 / 140,6 | 65,9 / 66,2 / 66,6 | come la matrice densa |
| Proiezione dei voxel sull'immagine (P) | 5,7 / 5,7 / 6,6 | 2,5 / 2,5 / 2,7 | 314 774 e 38 356 voxel provati |

Su 6 m senza ritaglio un raggio attraversa 120–208 voxel a 5 cm e 60–104 a 10 cm (calcolo). In 68 configurazioni il massimo non supera 1,35 volte la mediana. Rilanciate con il binario finale (`risultati_*_binario_finale.txt`), le righe della tabella cambiano al più del 6 % sul p95; su 58 configurazioni lo scarto mediano è 0,8 %, il massimo 18,6 % (raggi 8×8 a 5 cm).

1. **Il lancio di tutti i raggi non sta nel percorso critico.** A 5 cm il p95 è 90,2 ms, il 135 % del periodo; a 10 cm 50,9 ms, il 76 %. Costa 180 volte la griglia polare. Il costo non segue i voxel ma raggi × passi: 33,3 milioni di scritture per 324 139 voxel liberati, 103 visite a voxel. (`risultati_tempo.txt`)
2. **Decimare crea falsi «libero»; il sottocampionamento ammesso è uno solo.** Scena «tipica», 5 cm, per fotogramma, sui 6 648 voxel che contengono superficie vera sopra 0,10 m (`risultati_sicurezza.txt`): somma dei log-odds senza priorità, 3 707 liberi (55,8 %); un pixel ogni 4×4, 2 096 (31,5 %); tutti i raggi con priorità al colpo, 357, e 23 fermando lo scavo a Z − 3σ; **colpi a piena risoluzione, poi un raggio per blocco 4×4 fino al minimo del blocco − 3σ: 9,8 (0,15 %)**; proiezione: 0 su 36 fotogrammi. Passo ammesso: k ≤ lato·fx/Z_max, cioè 2 a 5 cm e 5 a 10 cm; oltre si perdono liberi, non sicurezza (a 5 cm, k = 4 tiene il 97,3 % dei liberi, k = 8 il 61 %). Neppure la regola migliore dei raggi dà zero: un raggio che sfiora un voxel lo libera tutto. La priorità al colpo è già la regola di OctoMap («occupied nodes have a preference over free ones», [OccupancyOcTreeBase.h](https://github.com/OctoMap/octomap/blob/devel/octomap/include/octomap/OccupancyOcTreeBase.h)); il §4 di `promptMare.txt` non la scrive.
3. **Lo sparso qui non paga.** Lo spazio visto libero va allocato (non allocato vuol dire «sconosciuto»): risultano allocati 736 blocchi su 1 200 (61 %) a 5 cm e 116 su 160 (72,5 %) a 10 cm. Memoria −35 % e −17,5 %, tempo +52 %. La formula M = O(B·b³·s) del §9 nasconde che B contiene il libero. Con il serbatoio al 50 % e senza precedenza ai colpi, nella scena «perturbazione» l'8,6 % dei voxel occupati osservati non entra in mappa (20 397 contro 22 305; `risultati_tetto.txt`): nessun falso libero, per costruzione, ma ostacoli visti che diventano «sconosciuto».
4. **Il log-odds letto come stato corrente è un falso «libero» (prove 2 e 5).** Quaranta scatole compaiono al fotogramma 60; conto i voxel «liberi» con il centro dentro una scatola (`risultati_vecchi.txt`, 5 cm). Lettura dal solo log-odds: 5 553 dopo 14 fotogrammi (il 33 % dei 16 851 voxel pieni), perché gli interni non vengono mai colpiti; 8 783 se la mappa è ferma. Lettura «visto libero nel fotogramma corrente»: 0 con la proiezione, 54 con i raggi 4×4. **Critica al nucleo:** la finestra di 3 fotogrammi dell'invariante 1, portata in 3D senza altro, dà 1 045 e 934 voxel nei due fotogrammi dopo la comparsa; con la clausola «un voxel contraddetto ora non è libero» dà 0. Nel nucleo la clausola c'è di fatto (oltre il primo ritorno la cella è subito «in ombra»): in 3D va scritta. Con i parametri di OctoMap ([fonte](https://github.com/OctoMap/octomap/blob/devel/octomap/src/AbstractOccupancyOcTree.cpp)) un voxel saturo «libero» cambia segno dopo 3 colpi, 0,2 s (calcolo).
5. **Prova 10: il caso peggiore è la scena vuota, non quella affollata.** Alla comparsa degli oggetti i raggi si accorciano: 70,0 ms contro una mediana di 82,6. La proiezione è costante: 5,5–5,7 ms di media nelle tre scene. Il tetto è geometrico. Ciò che cresce con gli oggetti è raggruppamento e associazione: **non misurato**.
6. **La regola rigida «un pixel non valido blocca il libero» crolla con buchi sparsi.** Con il 5 % di pixel non validi a caso la proiezione rigida lascia 2 voxel liberi (i raggi 133 984); quella lasca, che usa il minimo dei validi, 59 672. I buchi veri sono a chiazze: **non verificato** sul sensore.
7. **Il banco in ciclo chiuso sottostima, e non parla del prototipo.** La griglia polare costa 0,50 ms in ciclo chiuso e 0,80 / 0,84 / 1,42 al passo vero di 15 Hz (`risultati_interf.txt`). Il nucleo dichiara 20 ms in Python: un prototipo in Python **non è misurato**. R7 resta non risolto (155 ms noti contro 150: `f3/H-012/02-validazione/VERIFICA.md`, §3c).
8. **`promptMare.txt` non dice in quale orologio è τ, in che ordine si aggiorna, che cosa si scarta.** Il riferimento «p95 ≤ 150 ms» vale 2,25 periodi: come bilancio di uno stadio ammette una coda di due fotogrammi. Una marca a 16 bit in fotogrammi si riavvolge dopo 72,8 minuti (calcolo): serve un'epoca.

**I cinque comportamenti chiesti.**
- **(i) Tempo limitato.** Ordine fisso: colpi a piena risoluzione, poi i liberi con il passo che il tempo rimasto consente, poi niente. Ciò che non si fa conserva la marca vecchia e diventa «non osservato». Mai i liberi prima dei colpi, mai colpi decimati. Tracce e rilevamenti hanno un tetto; l'eccesso resta «occupato osservato» nella griglia, senza identità (**non verificato**).
- **(ii) Memoria.** Matrice densa preallocata, nessuna rimozione: a sensore fermo la prova 3 regge per costruzione. La possibile presenza **non vive nei voxel**: resta il cuneo geometrico del nucleo, in una tabella fissa. Con i blocchi (piattaforma in moto) si tolgono solo quelli senza occupati, i più lontani, e i colpi hanno la precedenza; se la tabella delle regioni è piena, le regioni si fondono e non si scartano (**non verificato**).
- **(iii) Dati vecchi.** Marca = contatore d'acquisizione del sensore; coda di un solo fotogramma, l'ultimo; un fotogramma più vecchio dell'ultimo integrato si scarta intero e si conta. Dentro il fotogramma: colpi → contraddizioni → liberi. «Libero» = marca del fotogramma corrente, o finestra senza contraddizione; l'età si calcola all'uscita, in secondi, latenza compresa. Il log-odds alimenta solo «occupato ricordato, con età».
- **(iv) Sensore coperto, posa.** Il controllo di salute va **prima** dell'integrazione, per fotogramma: una mappa con memoria conserverebbe i fotogrammi sbagliati che il nucleo impiega 0,13 s a dichiarare. Alla perdita: epoca + 1 (tutta la memoria torna «sconosciuto» in un'istruzione) e si degrada alla griglia del solo fotogramma. A 6 m, 0,5° valgono 5,2 cm, un voxel (calcolo). Senza assetto non si emette «libero». **Non verificato.**
- **(v) Ramo asincrono: sì.** Con i raggi che girano senza sosta su un altro core il p95 della griglia passa da 0,84 a 0,88 ms (1,03 sul filo gemello). La regola è la proposta 1.

## 2. `promptMare.txt` nel mio campo

- **Utili:** §9 (raggi, celle attraversate, casi peggiori, niente numeri senza misura); §10, prove 2, 3, 5, 9, 10; §4, «storia contro garanzia corrente» (misurato: 5 553); §7, non integrare con posa incerta; §11, riproduzione deterministica (due lanci, stessi conteggi).
- **Inutili qui:** CSR e COO (§3), formati per matrici ferme (deduzione, non misurata). Octree e hash come punto di partenza: a 72 m³ il denso sta in 4,61 MB; l'octree **non è misurato**.
- **Sbagliate o incomplete:** l'aggiornamento del §4 senza ordine né priorità (55,8 % di falsi sulla superficie); la formula della memoria del §9; il costo contato in voxel invece che in passi di raggio.

## 3. Stati proposti

| Enunciato | Stato |
|---|---|
| Tutti i raggi nel percorso critico a 15 Hz, 5 cm | **smentito** su questa macchina (p95 90,2 ms) |
| Aggiornamento voxel sotto 10 ms (proiezione, o raggi 4×4) | **sostenuto dai dati** qui; non verificato sulla destinazione |
| Decimare senza falsi liberi | **smentito** (2 096 per fotogramma) |
| Colpi pieni + minimo del blocco − 3σ | **sostenuto dai dati**: 0,15 %, non zero |
| Proiezione: zero falsi liberi | **sostenuto dai dati** (0 su 36 fotogrammi): non è una prova universale |
| Prove 2 e 5 | lettura dal log-odds **smentita**; marche con contraddizione **sostenute dai dati** con buchi sparsi; con buchi a chiazze **non risolto** |
| Prova 3 | per costruzione con matrice fissa; con blocchi e tetto **non risolto** |
| Prova 10 | **sostenuto dai dati** per la mappa; **non risolto** per raggruppamento e associazione |
| Prova 9, posa | **non verificato** |
| Lo sparso riduce la memoria | **sostenuto dai dati**: −35 % e −17,5 %, per +52 % di tempo |
| R7 (latenza) | resta **non risolto** |

## 4. Proposte

**`tempo-reale-1` — mappa voxel a senso unico, fuori dal percorso critico.** La sicurezza resta alla griglia del fotogramma. La mappa (matrice densa, proiezione, colpi prima, margine 3σ) gira in un ramo proprio sull'ultimo fotogramma e pubblica istantanee con marca d'acquisizione ed epoca, lette con uno scambio di puntatore e mai con un blocco. Può solo **aggiungere** avvisi («occupato ricordato», «ostacolo in quota», ombra 3D) con l'età: non produce «libero», non rilascia la possibile presenza, non abbassa un messaggio. Istantanea vecchia → «mappa in ritardo», e gli avvisi restano con l'età. *Guadagno:* niente nel percorso critico (+0,04 ms di p95 misurati). *Vincoli:* un core in più; ciò che la mappa aggiunge è «ricordato», mai «osservato». *Chi la prova:* validazione, avversario. *Falsificatore (5 min, non eseguito):* rifare `sh rifai.sh vecchi` con buchi a chiazze di 20×20 pixel sul 5 % dell'immagine. **Atteso, scritto ora:** lettura corrente 0; finestra con contraddizione ≤ 10 voxel per fotogramma; sopra 100 la finestra si toglie.

**`tempo-reale-2` — scala di degrado a scadenza.** È la regola (i), con i gradini misurati a 5 cm: 24,7 → 8,1 → 4,0 ms di media, oppure la proiezione a 5,7. Ogni gradino toglie solo «libero». *Guadagno:* scadenza tenuta, con tempi che non crescono con il numero di oggetti. *Vincoli:* orologio monotono e controllo del tempo fra le righe. *Chi la prova:* sistemista delle prestazioni. *Falsificatore (5 min, non eseguito):* interrompere lo scavo a righe alterne e contare i falsi sopra 0,10 m. **Atteso:** non più dei 118 su 12 fotogrammi dello scavo completo, liberi circa dimezzati; braccio che deve fallire: liberi prima dei colpi, con i colpi interrotti a metà, atteso oltre 1 000.

## 5. Che cosa propongo dopo

1. Rifare `rifai.sh` sulla macchina della demo e nel linguaggio del prototipo: finché manca, il sì alla mappa voxel è al più **condizionato**.
2. Misurare raggruppamento e associazione con 10, 50 e 200 oggetti: è la metà della prova 10 che manca.
3. Registrare 60 s dal sensore vero e contare i buchi a chiazze: decide fra regola rigida e lasca.
