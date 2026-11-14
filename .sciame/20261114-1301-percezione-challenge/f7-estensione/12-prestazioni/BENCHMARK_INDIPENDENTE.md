# Banco indipendente delle rappresentazioni — `sciame-prestazioni`, estensione f7, fase f4

14 novembre 2026, 16:07–16:44. Accanto: `PREVISIONI.md` (16:10:02, prima del codice), `banco.c`, gli script, `risultati*.txt`, `tabelle*.txt`, `confronto_core.txt`. **Rifare:** `sh compila.sh && sh lancia.sh 2 risultati.txt` (11 minuti; un processo alla volta, ognuno sotto `timeout 120`), poi `sh lancia.sh 2 risultati_colbit.txt 300 colbit`, `sh lancia.sh 9 risultati_core_lento.txt 300 breve`, `python3 -I tabella.py tutti.txt`.

## 0. In testa: cambi di stato e scostamenti

1. **F-102 va riscritto.** La scena «vuota» dei «736 blocchi su 1 200 e 116 su 160» è una stanza chiusa: pareti a 8 m e a ±6 m, soffitto a 4 m, profondità valida fino a 10 m (`06-tempo-reale/banco.c`, righe 59, 88–90, 100), quindi ogni raggio torna e scava. Col **solo pavimento** i blocchi sono **357 e 76**. «Lo sparso non paga» resta sostenuto dai dati, con cifre diverse.
2. **F-103, «tutti i raggi a 5 cm stanno oltre il ciclo»: smentito per la matrice densa su un core veloce** (p95 49,1 e 45,9 ms in due lanci); regge su un core lento (67,4 ms) e per hash e octree.
3. **Octree con potatura (V-008, «non risolto»): smentito come risparmio.** Il picco dei nodi è almeno il 99 % del non potato in 20 configurazioni su 20, e la memoria da riservare sale del 6 %.
4. **Costo discorde delle fasce (V-004): spiegato** (§3). **K-101 resta non spiegata**; un contributo c'è: il tipo di core vale 1,49 volte, e uno dei banchi non fissa il core.

**Scostamenti.** (a) Previsioni non cieche: il triage, letto prima, riporta alcuni numeri degli autori. (b) La variante «colonne di bit» è aggiunta **dopo** il primo giro, visto che le mie fasce costavano 1,6 volte la densa e quelle di un autore 0,6; gli altri otto eseguibili sono rimasti identici (`bin_prima.sha256`). (c) Il giro principale è un solo comando da 11 minuti. (d) Macchina non libera: carico medio 1,7–3,3, altri agenti al 100 % sui core 1–3. (e) Lette tre righe di `03-nuvole-punti`, fuori dai miei ingressi. (f) Scena vuota con tutti i raggi: 60 fotogrammi; core lento e ripetizione: 100. (g) CSR e COO non misurate; nessuna misura sui falsi «libero».

## 1. Impianto

Portatile, **non la scheda di bordo**: AMD Ryzen AI 9 HX 370, 4 core fino a 5,16 GHz (0–3) e 8 fino a 3,29 GHz (4–11), letti da `cpuinfo_max_freq`; Linux 7.3.4, regolatore `performance`, gcc 16.2.1 `-O2`, un filo fissato con `taskset` (core 2; ripetizione sul core 0; core lento 9), pagine da 4 kB. Camera simulata 640 × 480, 87° × 58°, a 1,2 m, inclinata di 15°, profondità valida fino a 6 m, rumore 0,0025·z², 1,2 % di buchi; un raggio senza ritorno non scrive niente. Regione 6 × 4 × 3 m: 72 000 voxel a 10 cm, 576 000 a 5 cm, **4 byte per voxel**. Passo 1, 2, 4, 8 = 307 200, 76 800, 19 200, 4 800 pixel letti. Scene da 300 fotogrammi: vuota (solo pavimento), rada (persona, cassa, pannello), densa (parete di fondo, tre scaffali, venti oggetti), carico (rada, poi 200 oggetti dal fotogramma 150). **Il tempo comprende** deproiezione, lancio dei raggi, scritture, potatura; **non** la generazione dell'immagine. **Indipendenza:** condivido con gli autori consegna, macchina e geometria del nucleo; non il codice (scritto e lanciato prima di leggere il loro) né le scene. Le mie strutture voxel condividono il lancio dei raggi: le somme di controllo uguali (densa = hash = octree in 12 configurazioni su 12; colonne di bit = densa in 8 su 8) coprono solo i difetti delle strutture.

## 2. Misure (core 2)

**Memoria usata, byte (percentuale della densa), tutti i raggi.** Hash: blocchi 8³ più la tabella. Octree: 8 byte per nodo.

| | 10 cm, vuota | 10 cm, densa | 5 cm, vuota | 5 cm, densa |
|---|---|---|---|---|
| Matrice densa | 288 000 | 288 000 | 2 304 000 | 2 304 000 |
| Hash 8³ | 159 744 (55 %) | 241 664 (84 %) | 763 904 (33 %) | 1 515 520 (66 %) |
| Octree | 163 264 (57 %) | 377 856 (131 %) | 1 004 672 (44 %) | 2 691 008 (117 %) |

A dimensione fissa: polare del nucleo 10 788 B (più 1,5 MB di tabelle per pixel), colonne di bit 28 800 e 115 200 B, tre fasce 48 000 e 192 000 B, lettura nell'immagine 2 457 600 B. **Memoria residente** in più, 5 cm: densa 1 144 kB (vuota) e 2 328 kB (densa), hash 1 048 e 1 780 kB. Le pagine mai toccate della densa non vengono materializzate: nella scena vuota lo scarto vero è 96 kB.

**Aggiornamento, scena densa, ms: media / p95 / p99 / massimo.** Raggi validi 16 557 (passo 4) e 264 709 (tutti); passi di raggio 0,77 e 1,56 milioni, poi 12,4 e 24,9 milioni; densa 1,8–2,7 ns per passo.

| | 10 cm, passo 4 | 5 cm, passo 4 | 10 cm, tutti | 5 cm, tutti |
|---|---|---|---|---|
| Polare, 3 m | 0,03 / 0,04 / 0,04 / 0,05 | uguale | 0,42 / 0,55 / 0,57 / 0,57 | 0,37 / 0,40 / 0,43 / 0,53 |
| Immagine (V-002) | 0,51 / 0,52 / 0,55 / 0,57 | uguale | 0,74 / 0,88 / 0,89 / 0,89 | 0,51 / 0,53 / 0,58 / 0,62 |
| Colonne di bit | 1,30 / 1,34 / 1,38 / 1,44 | 2,47 / 2,55 / 2,60 / 2,66 | 19,5 / 20,0 / 21,3 / 22,4 | 37,4 / 38,4 / 39,0 / 40,8 |
| Tre fasce (S10) | 3,29 / 3,37 / 4,80 / 4,91 | 6,23 / 6,41 / 6,47 / 6,51 | 44,5 / 45,7 / 67,1 / 73,4 | 85,5 / 97,6 / 146 / 151 |
| Matrice densa | 2,03 / 2,08 / 2,14 / 2,25 | 4,21 / 4,35 / 4,71 / 5,38 | 22,4 / 22,8 / 33,3 / 33,4 | 44,5 / 49,1 / 52,1 / 58,3 |
| Hash 8³ | 3,02 / 3,12 / 3,16 / 3,23 | 6,71 / 7,45 / 14,4 / 16,9 | 32,6 / 47,9 / 49,0 / 62,2 | 72,4 / 76,4 / 77,6 / 78,0 |
| Octree | 5,02 / 5,39 / 6,55 / 6,88 | 11,2 / 12,1 / 12,3 / 12,3 | 72,2 / 75,7 / 76,8 / 77,6 | 161 / 171 / 216 / 267 |

Rapporti sulle medie (18 configurazioni): hash 1,39–1,76 volte la densa; octree 2,2–3,9; potatura 0,99–1,23 volte l'octree; colonne di bit 0,46–0,89. **Rumore:** sul core 0 le medie stanno a 0,95–1,08 volte quelle del core 2 (45 configurazioni su 48), i massimi no (octree a 5 cm: 267 contro 164 ms): oltre il p95 il massimo è dell'ambiente. **Core lento:** 1,49 volte (mediana di 48); a 5 cm con tutti i raggi, media / p95 / massimo: densa 65,2 / 67,4 / 67,6 ms, colonne di bit 55,8 / 57,5 / 57,7, hash 106 / 109 / 109, octree 235 / 247 / 321. Nessun picco al primo fotogramma. **Python 3.14 puro**, 19 200 raggi a 10 cm: densa **102 ms**, polare 1,6 ms.

**Interrogazione, 18 settori da 5°** (quote 0,1–2 m, fino a 6 m), µs, media / p95 / massimo, a 10 e a 5 cm: polare 3,6 / 3,8 / 7,3; colonne di bit 4,9 / 5,4 / 6,2 e 14 / 16 / 16; tre fasce 16 / 18 / 25 e 58 / 61 / 89; densa 38 / 40 / 52 e 261 / 281 / 447; hash 62 / 64 / 73 e 433 / 493 / 1 640; octree 219 / 236 / 331 e 1 883 / 1 963 / 2 989; immagine 636 / 652 / 700 per 108 000 punti (5,9 ns l'uno).

**Carico improvviso (da 3 a 200 oggetti in un fotogramma), passo 4.** Quel fotogramma costa 1,07–1,22 volte la mediana di prima in tutte le strutture con i raggi (densa a 5 cm: 2,69 → 2,95 ms; hash 4,09 → 4,46, blocchi 314 → 397 → 543 a fine corsa; octree 7,47 → 8,09, nodi 110 161 → 127 745 → 216 809); massimo dopo il carico 13,2 ms. **Dopo, il tempo sale del 9–15 %, non scende:** senza parete di fondo gli oggetti in aria creano ritorni dove non ce n'erano. Il lavoro resta limitato da raggi × (nx + ny + nz).

## 3. Confronto con gli autori

| Grandezza | Autori | Qui | Causa dello scarto | Esito |
|---|---|---|---|---|
| Memoria densa | 576 000 e 4 608 000 B | la metà | voxel da 8 byte contro 4 | **spiegata** |
| Blocchi hash, «vuota» | 736 e 116 | 357 e 76 | stanza chiusa (§0); con la mia parete di fondo: 724 e 116 | **spiegata** |
| Densa, 5 cm, tutti i raggi | 88,9 ms (tempo reale); 76,2 ms (ottimizzazione: 1,71, sotto il fattore due) | 44,5 ms | il loro «core veloce = 4» (`rifai.sh`) è un core da 3,29 GHz: 1,49 ×; 33,3 milioni di passi contro 24,9: 1,34 ×. Sul core lento misuro 2,64 ns per passo, loro 2,67 | **spiegata** |
| Fasce | 121–123 ms contro 1,66 ms | 0,65–116 ms | 407 040 raggi contro 19 200 (21 ×); due strutture in un solo tempo (2 ×); resto 1,7. Il codice vale un altro 2,5 × (le mie due varianti) | **spiegata** |
| Hash e octree sulla densa; polare; interrogazione; Python puro | 1,39–1,71 e 2,5–2,9; 0,39–0,50 ms; 39 e 290 µs; 154 ms | 1,39–1,76 e 2,2–3,9; 0,37–0,42 ms; 38 e 261 µs; 102 ms | entro 1,5 | concordi |
| Passi a 4,9–7,7 ns (K-101, altri tre ruoli) | — | 1,7–4,1 ns | banchi non rifatti | **non spiegata** |

## 4. Conclusioni

1. **La sparsità riduce la memoria?** In byte allocati sì, con i blocchi: al 33 % (5 cm) e al 55 % (10 cm) col solo pavimento, al 66 % e all'84 % con scaffali e parete. In assoluto **al più 1,54 MB**; in memoria residente 96 kB nella scena vuota. L'octree ne usa **di più** (117–131 % nella scena densa). Una hash che conserva solo l'occupato scende all'11–27 % (245 760 B a 5 cm), ma risale al 55–76 % nella scena densa senza rimozione. **Sostenuto dai dati**, su scene sintetiche.
2. **E il tempo?** Peggiora: hash 1,39–1,76 volte, octree 2,2–3,9 nell'aggiornamento; 1,2–1,8 e 5–12 nell'interrogazione. Il costo segue raggi × passi, non la struttura.
3. **15 cicli al secondo (66,7 ms) e p95 ≤ 150 ms, solo mappa e interrogazione, su questo portatile.** A passo 4 li rispettano **tutte**, a 10 e a 5 cm: p95 peggiore 12,8 ms (20,4 sul core lento). Con tutti i raggi a 10 cm, sul p95: sì tutte quelle della tabella tranne l'octree (75,7 ms). Con tutti i raggi a 5 cm: sì polare, immagine, colonne di bit (38,4) e densa sul core veloce (49,1), che sul core lento manca il ciclo di 0,7 ms; **no** hash (76,4), tre fasce (97,6), octree (171, oltre anche i 150 ms). In **Python puro** la densa manca il ciclo già a 19 200 raggi. Il resto della catena non è qui: R7 resta **non risolto**; scheda di bordo e sensore vero **non verificati**.
4. **S10.** Il costo non la sostiene come «sostituto su CPU»: in C la densa a passo 4 costa 2–4 ms (3–7 sul core lento), da 7 a 20 volte sotto la soglia di 45 ms; in Python puro la supera (102 ms). Il passaggio automatico lo deciderebbe il linguaggio, non la scheda grafica. La forma economica delle fasce è la colonna di bit: 0,5–0,9 volte il tempo della densa, 57 righe di C, stessa uscita per settori.

| Scelta | Costo misurato | Continuità visiva | Quando |
|---|---|---|---|
| Griglia polare (V-001) | 0,03–0,6 ms | non tocca: lascia il ciclo alla previsione | **indispensabile nelle 14 ore** |
| Lettura nell'immagine (V-002) | 0,5 ms più 5,9 ns per punto; 30 righe | **aiuta**: chiedere «il sensore ora vede attraverso?» su 1 000 punti dell'area prevista costa 6 µs | **14 ore**, se il torneo la conferma |
| Colonne di bit (V-003, V-004, S10) | 1,3–2,5 ms a passo 4; 29–115 kB | aiuta se dà la quota a cui l'ombra finisce | **4 ore di raffinamento** |
| Matrice densa (V-006) | 2–4 ms a passo 4; 45–67 ms con tutti i raggi | non tocca a passo 4; **ostacola** con tutti i raggi: 66,7 ms di ritardo sono 9 cm a 1,4 m/s (calcolo) | **dopo l'hackathon** |
| Hash, octree; passaggio automatico di S10 | più lenti; risparmio ≤ 1,54 MB | non aiutano | **dopo**; no a questa scala |
| S11 e registro degli eventi (Q2) | **non misurato** | — | fuori dal mio banco |

**Previsioni (14 voci, esiti in `PREVISIONI.md`).** Cinque reggono (P1, P2b, P7, P8, P12); nove sono smentite del tutto o in parte: quasi sempre il costo è più basso dell'atteso (densa due volte più veloce, octree 2,2–3,9 volte e non 3–8, potatura quasi gratuita nel tempo ma inutile nel picco); P9 e P13 erano sbagliate nel merito (il tempo sale dopo il carico; il solo occupato arriva al 55 %, non al 25).

**Che cosa propongo dopo.** Rifare `sh lancia.sh <core> x.txt 300 breve` (4 minuti) sulla macchina della demo: è la sola misura che decide il punto 3. Misurare il ciclo nel linguaggio del prototipo con le librerie vere (qui numpy manca): **non misurato**, e pesa più della scelta della struttura.
