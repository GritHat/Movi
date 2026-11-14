# Stato — sciame-ottimizzazione, f7, corsia A

- 15:09:45 previsioni scritte (`PREVISIONI.md`), prima del codice.
- 15:11 `banco.c` compilato, prova di fumo a 20 fotogrammi; tolta `floorf` dalla struttura D (dichiarato).
- 15:13 lotto 1 sul nucleo 2: conteso da un altro agente → `risultati_1_contaminato_cpu2.txt`; rifatto sul nucleo 1.
- 15:16–15:23 lotti 2–10 eseguiti, uno alla volta, ciascuno sotto i due minuti.
- 15:22 aggiunta P12 (Python puro) prima del lotto 10.
- CONSEGNA.md scritta. Stato: **consegnato**.
- Esiti delle previsioni: P1 regge; P2 smentita in parte (hash 1,16–1,34 ×, octree 2,5–2,9 ×: meno del previsto); P3 regge; P4 regge; P5 smentita; P6 regge salvo hash a 10 cm (1,43 ×); P7 regge (17 configurazioni); P8 regge sulla soglia (primo fotogramma 63 ms, previsto > 100); P9 regge dopo la correzione di `floorf`; P10 regge (0 % di differenza); P11 regge (massimo 0,014 ms); P12 regge sulla soglia (154 ms), attesa sbagliata.
