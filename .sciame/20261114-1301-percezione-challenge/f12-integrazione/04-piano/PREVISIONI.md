# PREVISIONI — sciame-pianificatore, f12, 04-piano

Scritte alle 2026-11-14T17:50:44+01:00 (`date -Is`), dopo aver letto contratto, verdetti e consegne di f10, **prima** di lanciare
qualunque prova o simulazione mia. Gli esiti si aggiungono in fondo, con l'ora.

## A. Prove sul materiale da riusare (decidono le stime di rilettura)

- **R-1.** `10-catena/prove.py` rilanciato da me passa 25 prove su 25 in meno di 30 s. *Smentita:* una prova fallita,
  un errore d'importazione, o più di 30 s.
- **R-2.** `f8-continuita/13-soluzione/comp.c` si compila con `gcc -O2` senza errori (eseguibile scritto nella mia
  cartella) in meno di 30 s. *Smentita:* un errore di compilazione.
- **R-3.** `f7-estensione/04-requisiti/eventi.py` gira con `python3 -I` in meno di 120 s ed esce con 0.
  *Smentita:* codice d'uscita diverso da 0 o tempo scaduto.

## B. Simulazione delle durate (`piano_mc.py`, 20 000 estrazioni per caso, seme 20261114)

Misura: P(MD) = quota di estrazioni in cui la prova generale del minimo dimostrabile (continuità e sicurezza comprese)
finisce entro l'ora 14,0 d'orologio. Le stime a tre punti sono mie, scritte nel programma prima del primo lancio.

- **S-1.** Piano di riferimento (5 persone, nessun sensore, compito più lungo a una persona): 0,45 ≤ P(MD) ≤ 0,80.
  *Smentita:* fuori dall'intervallo.
- **S-2.** Con 4 persone P(MD) < 0,35 (V8 §5 dice «non ci sta» sul bilancio delle ore-persona, senza riuso).
  *Smentita:* P(MD) ≥ 0,35.
- **S-3.** Dividere fra due il compito più lungo (B3, le regole della continuità) alza P(MD) di almeno 0,08 con
  5 persone. *Smentita:* guadagno sotto 0,08.
- **S-4.** Ciò che muove di più la fine è il fattore comune di squadra (correlazione di rango più alta con l'ora di
  fine), e fra i compiti B3; l'indice di criticità più alto è della catena di P2 (B1 → B2 → B3 → J1).
  *Smentita:* un altro fattore o un altro compito in testa.
- **S-5.** Il ramo «arriva una camera» abbassa P(MD) di meno di 0,05 rispetto a «non arriva niente», perché la prima
  ora di misure sta fuori dal minimo e si abbandona all'ora 11. *Smentita:* calo di 0,05 o più.
- **S-6.** Il nocciolo non tagliabile (senza la corsa sulle sequenze pubbliche, con la robustezza A4 e le correzioni J2
  a tempo chiuso) chiude entro l'ora 14 con P ≥ 0,85 a 5 persone. *Smentita:* P < 0,85.

Ciò che noto dopo i lanci va sotto «Dopo», separato.

## Esiti del primo lancio (aggiunti alle 2026-11-14T17:56:30+01:00)

- **R-1 regge:** 25 prove su 25, 4,69 s, uscita 0 (`prova_R1_catena.txt`). **R-2 regge:** `gcc` esce con 0, nessun
  errore (`prova_R2_comp.txt`; il tempo non è misurato: manca `bc`, è sotto il tetto di 60 s). **R-3 regge:** uscita 0
  (`prova_R3_eventi.txt`).
- **S-1 smentita:** RIF-5 dà P(MD) = 0,016 [0,014; 0,018], non 0,45–0,80; mediana della fine all'ora 21,1.
  Il mio conto a mano usava le durate probabili (13,2 ore sul percorso più lungo) e nessuna pausa: la media di una
  triangolare asimmetrica sta 1,2 volte sopra la moda e le pause tolgono il 12 %.
- **S-2 regge** (0,003 con 4 persone), ma è poco informativa: anche con 5 non ci sta.
- **S-3 smentita:** dividere B3 dà +0,006 (0,016 → 0,022), non +0,08: dopo B3 restano in fila J1 → D3 → J2 → VID → PG.
- **S-4 regge in parte:** il fattore di squadra è in testa (Spearman +0,63); fra i compiti però in testa sono J2
  (+0,15), D3 (+0,12), J1 (+0,11), non B3; l'indice di criticità più alto, dopo K0 e PG, è di D3 (78 %) e J2 (66 %).
- **S-5 regge:** ramo A 0,016 contro 0,022 nel ramo C (calo 0,006).
- **S-6 smentita:** il nocciolo chiude entro l'ora 14 con P = 0,079, non ≥ 0,85.

## C. Piano rivisto DOPO il primo lancio (scritto alle 2026-11-14T17:56:30+01:00, prima di lanciarlo)

Il primo piano ha una coda in fila dopo l'integrazione (integrazione → tabellone → correzioni → video → prova
generale: 6,9 ore medie). Lo rifaccio **senza cambiare nessuna stima a tre punti dei compiti che restano**: cambia la
struttura. (a) Integrazione continua sulla catena che già gira (niente integrazione «tutta insieme» di 2 ore: una
prova d'insieme PI di 0,5–1–2 ore); (b) il tabellone gira dall'ora in cui D2 è chiuso, la corsa finale TAB è una
rilettura (0,5–1–2 ore); (c) correzioni e video non stanno più in fila: correzioni a tempo chiuso accanto a TAB, video
registrato durante la prova generale (0,75 ore, a tempo chiuso); (d) C3 diviso in C3a (P3) e C3b (P1); (e) A4 fuori
dal minimo (le cifre d'identità si dichiarano come trovate). Stime nuove, solo dei compiti nuovi: PI, TAB, C3a
0,5–1–2; C3b 1–1,5–3. Questo piano è **scelto dopo aver visto un esito**: va letto così.

- **S-7.** TC-5 (5 persone, nessun sensore): 0,15 ≤ P(MD) ≤ 0,45. *Smentita:* fuori dall'intervallo.
- **S-8.** TC-5 con i tagli scritti (A3 ridotto a 1,5 ore, niente C3b, niente D4, PI e TAB a tempo chiuso):
  P ≥ 0,60. *Smentita:* P < 0,60.
- **S-9.** TC con 4 persone: P(MD) < 0,10. Con B3 non diviso (TC-5-B3) P(MD) scende di almeno 0,05 rispetto a TC-5.
  *Smentita:* 4 persone ≥ 0,10; oppure calo sotto 0,05.

## Esiti del piano rivisto (aggiunti alle 2026-11-14T17:57:53+01:00)

- **S-7 regge:** TC-5 dà P(MD) = 0,294 [0,288; 0,300] (previsto 0,15–0,45).
- **S-8 smentita:** con i tagli scritti P = 0,460 [0,453; 0,467], non ≥ 0,60.
- **S-9 regge:** 4 persone 0,077 (< 0,10); con B3 a una persona 0,180 contro 0,294 (calo 0,114 ≥ 0,05).

## Dopo (notato dopo i lanci, non previsto)

- I punti di controllo che avevo scritto nel programma per le ore 2 e 5 erano troppo ambiziosi rispetto al mio stesso
  modello (P = 0,08 e 0,10): li ho ritarati sulle mediane (sezione 7f di `risultati_piano_mc.txt`), dopo aver visto 7d.
- La leva più forte non l'avevo prevista: «il riuso va male» (riletture × 2, correzioni × 1,5) toglie 0,41.
- Regola violata per errore: un `git status --short` in sola lettura dentro un comando di controllo (nessuna modifica).
