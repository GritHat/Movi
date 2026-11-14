# Previsioni — sciame-ottimizzazione, estensione f7, corsia A

Scritte alle **2026-11-14T15:09:45+01:00** (`date -Is`), prima di scrivere il banco di prova `banco.c` e prima di ogni lancio.
Nessuna misura esiste ancora: ciò che segue viene da conti a mano.

## Il banco (dichiarato prima)

- Regione d'interesse 6 × 4 × 3 m (x avanti 0–6, y −2…+2, z 0–3), sensore fermo in (0, 0, 1,2 m), inclinato di 15° verso il basso, campo 87° × 58°.
- Voxel di 8 byte: log-odds a 16 bit, qualità 8 bit, osservabilità 8 bit, marca di tempo 32 bit (lo stato (L, τ, q, ν) di `promptMare.txt` §4).
- Raggi per fotogramma: 19 200 (160 × 120, sottocampionato 4 ×), 76 800 (320 × 240), 307 200 (640 × 480, pieno).
- Scene sintetiche, seme fisso: «rada» (suolo, parete di fondo, 2 mobili) e «densa» (suolo, tre pareti, 24 scatole ferme a quote diverse, 6 mobili). Rumore 0,00375·z² m, 2 % di pixel non validi. 300 fotogrammi.
- Un solo thread, `gcc -O2`, fissato su un nucleo con `taskset`. Il tempo di generazione della profondità è escluso.
- Strutture: A densa (con indice ad anello) e A' densa senza anello; B hash di blocchi 8³ (con e senza memoria dell'ultimo blocco, `calloc` per blocco oppure arena); C octree a indici senza potatura; D polare sul piano + colonna di bit di quota per cella; E polare sul piano del nucleo (3 m e 6 m); F vettore ordinato tipo CSR/COO (solo 10 cm).

## Conti (non sono previsioni)

- Voxel teorici: 60 × 40 × 30 = **72 000** a 10 cm; 120 × 80 × 60 = **576 000** a 5 cm.
- Byte densi a 8 byte per voxel: **576 000 B (0,55 MiB)** a 10 cm; **4 608 000 B (4,39 MiB)** a 5 cm.
- Blocchi 8³ nella regione: 8 × 5 × 4 = 160 a 10 cm; 15 × 10 × 8 = 1 200 a 5 cm.
- Griglia polare del nucleo, 1° × 0,1 m: 30 celle radiali fino a 3 m, 60 fino a 6 m.

## Previsioni (misura, soglia di smentita)

**P1 — la sparsità non paga a questa scala.** Memoria usata dalla hash di blocchi (blocchi + tabella + indici), scena rada: ≥ 50 % della densa a tutte e due le risoluzioni (attesa: 70–90 % a 10 cm, 55–75 % a 5 cm). Motivo: per poter dire «libero» bisogna allocare il voxel libero, e il tronco di vista copre circa metà della regione. **Smentita se** la hash usa < 50 % della densa nella scena rada. Corollario atteso: la scena «rada» alloca PIÙ blocchi della «densa».

**P2 — latenza d'aggiornamento con lancio dei raggi, 19 200 raggi.** Media: densa 1–6 ms a 10 cm e 2–12 ms a 5 cm; hash (con memoria dell'ultimo blocco) fra 1,3 e 3 volte la densa; octree fra 3 e 10 volte la densa. **Smentita se** un rapporto esce dall'intervallo o la densa esce dall'intervallo assoluto.

**P3 — la linea di base costa molto meno.** Griglia polare E (3 m e 6 m), 19 200 raggi: media < 0,5 ms; la densa a 10 cm è almeno 5 volte più lenta della polare. **Smentita se** la polare supera 0,5 ms o il rapporto è < 5.

**P4 — 15 cicli al secondo.** A 19 200 raggi tutte le strutture A, B, C hanno 95° percentile e massimo dell'aggiornamento sotto 66,7 ms. A 307 200 raggi e 5 cm: octree e hash hanno il 95° percentile sopra 66,7 ms; la densa sta fra 30 e 120 ms (incerto da che parte della soglia). **Smentita se** qualcuna di queste tre frasi è falsa.

**P5 — primo fotogramma.** La hash con `calloc` per blocco ha il primo fotogramma ≥ 2 volte la propria media (raffica di allocazioni); la densa ≤ 2 volte. **Smentita se** non è così.

**P6 — interrogazione per settori (9 settori, fascia di quota 0,1–2,0 m).** Media: densa < 0,3 ms a 10 cm e < 2 ms a 5 cm; hash 1,5–4 volte la densa; polare E < 0,05 ms. **Smentita se** fuori.

**P7 — equivalenza.** Stesso seme e stessa configurazione: la somma di controllo dello stato di tutti i voxel è identica per densa, hash, octree e vettore ordinato. **Smentita se** differisce (allora c'è un difetto nel banco, da trovare prima di usare i numeri).

**P8 — CSR/COO.** Vettore ordinato con ricerca binaria e inserimento, 10 cm, 19 200 raggi: primo fotogramma > 100 ms; a regime ≥ 5 volte la densa. **Smentita se** il primo fotogramma è < 66,7 ms e il regime è < 2 volte la densa.

**P9 — ibrido D.** Polare + colonne di bit (60 livelli da 5 cm, fino a 6 m): aggiornamento ≤ 0,5 volte la densa a 5 cm con gli stessi raggi; memoria ≤ 10 % della densa a 5 cm. **Smentita se** D è più lenta della metà della densa o usa > 461 kB.

**P10 — ombra esplicita.** Se si marcano i voxel in ombra allocandoli, nella scena densa la hash usa una memoria entro ± 15 % di quella della scena rada (l'ombra riempie ciò che l'occlusione risparmiava). **Smentita se** la differenza supera il 15 %.

**P11 — scorrimento.** Spostare la finestra di un voxel lungo x: densa ad anello < 0,05 ms a 5 cm (azzera una fetta di 80 × 60 voxel). **Smentita se** ≥ 0,05 ms.

## Che cosa condivide il controllo con ciò che controlla

Il banco, le scene e le previsioni hanno lo stesso autore e lo stesso modello; le strutture A, B, C, F condividono il codice del lancio dei raggi (la somma di controllo vede solo i difetti della struttura, non quelli del lancio). Scene sintetiche, sensore fermo, un solo calcolatore (portatile, non la scheda di bordo).

## Aggiunta, scritta alle 2026-11-14T15:23:18+01:00 (dopo i lotti 1–9 in C, prima di scrivere e lanciare `dda_python.py`)

**P12 — il lancio dei raggi voxel in Python puro non sta nel ciclo.** Il nucleo dichiara la griglia «20 ms a 640×480 in Python puro» (SOLUZIONE_V2, B2): se il prototipo resta in Python senza numpy, quanto costa lo stesso lancio dei raggi denso? Misura: un porting riga per riga del ciclo Amanatides–Woo su lista piatta, 10 cm, 19 200 raggi, scena di solo suolo e parete di fondo, Python 3.14, 5 fotogrammi. Attesa: 0,5–2 s per fotogramma (circa 950 000 passi a 0,5–2 µs l'uno). **Smentita se** la mediana è < 66,7 ms per fotogramma (allora starebbe nei 15 cicli al secondo).
