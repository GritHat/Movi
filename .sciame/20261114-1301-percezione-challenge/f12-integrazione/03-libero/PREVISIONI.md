# PREVISIONI — «libero» della cella (K-107, controllo C-D) — sciame-nuvole-punti, f12

Scritte alle **2026-11-14T17:50:30+01:00**, prima di scrivere il banco (`banco_libero.py`) e prima di ogni lancio. Non cieche: ho letto
V7 (§0, §1, §3, §7), `14-attacco/av10.py`, `av1.py`, `sim.py` e i loro risultati, `15-verifica/VERIFICA_DECISIONE.md`
e `vq3c.c` (modello dei buchi, regola dei settori, impronta). Gli esiti si aggiungono in coda, senza toccare questa parte.

## Banco (dichiarato prima)

Camera ideale a foro 320 x 240, 87 x 58 gradi, a 1,2 m, 15 gradi in basso, profondità lungo l'asse ottico, rumore k z^2
(k = 0,004 e 0,0100), margine m(z) = 0,03 + 3 k z^2; griglia 87 x 30 (1 grado x 0,1 m). Scene: le 8 di `av10.py` x 2 valori
di k (= le 16 combinazioni di A) + due mie: corpo che non rimanda segnale (0,45 x 0,25 x 1,75 m a 2 m, da `av1.py`) e la
scatola da 10 cm spostata a 2,6-2,9 m (pochi pixel per cella). Buchi: nessuno, sparsi 5 % e 30 % (per pixel), a chiazze
5 % e 30 % (blocchi 20 x 20 pixel, come `vq3c.c`). Errore d'inclinazione: 0, ±0,5, ±1 grado (camera vera a 15 + e, regola
che crede 15). Tutte le regole leggono il SOLO fotogramma corrente. 30 fotogrammi per condizione, semi fissi.
Candidate: **SC** stato(centro a 0,10 m); **RP** ripiego stato(centro a 0,20 m), senza griglia; **V17** quota verificata
(non occupata, non oltre il primo ritorno, stato a 0,20 m; q_v letta su 0,2/0,6/1,0/1,4/1,8 m); **V18-1** e **V18-m**
impronta del suolo con almeno 1 pixel o almeno metà dell'impronta (non occupata, non in ombra).

## Soglie (contratto C-D; valgono per tutte le candidate)

- **S1, sicurezza.** 0 celle «libere» col centro dentro la pianta di un corpo appoggiato al suolo, 0 col suolo del centro
  nascosto da un corpo, 0 (per V17) con q_v non sotto la base di un ostacolo sospeso; su tutte le scene, tutti i buchi,
  errore d'inclinazione fra -0,5 e +0,5 gradi. A ±1 grado si misura e si dichiara (la premessa del nucleo è «assetto
  noto a meno di 1 grado»: è il bordo del dominio).
- **S2, uscita.** Stanza vuota, 5 % di buchi sparsi, errore 0: mediana per settore (5 gradi, da 1,3 m, direzione
  peggiore, settori aperti) della distanza libera **non sotto 2,7 m**, per ciascuno dei due valori di k.
- In più, misurati senza soglia: resa del libero vero, cambi di stato per cella al secondo (15 fotogrammi al secondo),
  tempo per fotogramma (Python con numpy, un filo, questa macchina).

## Previsioni (smentita = la cifra esce dall'intervallo)

- P1. SC: almeno una cella libera dentro la scatola da 10 cm o sotto vincolo S1 violato (smentita: 0 ovunque). S2: sotto 2,0 m.
- P2. RP: S1 violata sulla scatola da 10 cm (centro a 0,20 m sopra la scatola: almeno 10 celle per fotogramma); S2 sotto 2,0 m.
- P3. V17: S1 regge (0) fra -0,5 e +0,5 gradi; S2 **cade**: mediana fra 1,3 e 2,0 m col 5 % sparso (nove pixel validi: 0,95^9 = 0,63).
- P4. V18-1: S1 regge (0) fra -0,5 e +0,5 gradi; S2 regge: mediana 2,9-3,0 m col 5 % sparso; col 30 % sparso resa >= 70 %;
  con chiazze al 30 % mediana fra 1,3 e 2,0 m e cambi fra 3 e 6 al secondo.
- P5. V18-m: S1 regge; col 30 % sparso resa sotto il 60 %; S2 regge (>= 2,7 m).
- P6. A -1 grado (camera che guarda più in alto di quanto crede) almeno una regola con la griglia dà celle libere
  dentro la scatola da 10 cm; a +1 grado nessuna violazione ma resa del libero oltre 2,4 m sotto il 50 %.
- P7. Scatola da 10 cm a 2,6-2,9 m col 30 % di buchi sparsi: V18-1 dà almeno una cella libera dentro la pianta (pochi
  pixel per cella: la soglia «3 pixel» non scatta); V17 no (smentita di P7: 0 per V18-1).
- P8. Tempo: ogni regola sotto 5 ms a fotogramma in numpy (griglia compresa); V18 non più lenta di V17.
- P9. Fotogrammi di f10 (modello del sensore e uno vero): V18-1 dà più celle libere di V17 in ogni fotogramma; nessuna
  soglia (non c'è verità sul libero).

## Esiti del lancio 1 (banco_libero.py 30; file `*_lancio1.*`; 15 000 fotogrammi, 500 condizioni)

- P1 **regge** (SC: 10 714 celle col suolo nascosto date per libere nelle 16 combinazioni; S2 1,3 m). P2 **regge** (RP: 15 648 dentro un corpo; S2 1,3 m).
- P3 **smentita su S1**: V17 dà 770 celle dentro un corpo e 835 col suolo nascosto, tutte coi buchi a chiazze (la chiazza toglie i pixel
  che testimoniano l'ostacolo; il punto a 0,20 m guarda oltre). S2 cade come previsto (1,3 m).
- P4 **smentita su S1**: V18-1 dà 533 celle dentro (20 oltre 5 cm) nelle 16 combinazioni, e 900 fotogrammi su 900 col corpo muto. S2 regge (3,0 m).
- P5 **smentita su S1 di poco**: V18-m 6 celle (3 oltre 5 cm) in 6 fotogrammi su 7 200, tutte sulla scatola da 10 cm col 30 % di buchi; S2 regge.
- P6 regge a -1 grado (tutte cadono); **smentita a +1** per V17 e V18-1 (cadono anche li'). P7 regge in parte (V18-1 3 celle; ma cade anche V17 con le chiazze).
- P8 regge (V17 1,16 ms; V18 0,87 ms; mediana). Nessuna candidata passa S1 alla lettera.

## Previsioni del lancio 2 — varianti PRUDENTI (scritte alle 2026-11-14T17:55:23+01:00, DOPO aver visto il lancio 1: non cieche)

Il contratto chiede, se nessuna passa, «la regola piu' prudente che non viola la sicurezza». Provo solo combinazioni dei pezzi
gia' sul banco (nessun meccanismo nuovo), sullo stesso banco e poi su semi nuovi:
- **PR1** = V17 e V18-m insieme (suolo letto E colonna letta a 0,20 m).
- **PR2** = V18-m, e nessuna cella occupata fra le 8 vicine.
- **PR3** = V18 con TUTTA l'impronta valida e sul suolo.
- **PR4** = V18-m erosa di una cella: libera solo se anche le 8 vicine sono libere per V18-m (le vicine senza impronta non contano).
Previsioni: PR1 S1 = 0 fra -0,5 e +0,5, ma S2 cade (1,3 m col 5 % sparso). PR2: S1 non 0 (restano i bordi del corpo muto e la
scatola lontana), S2 regge. PR3: S1 = 0 nelle 16 combinazioni, S2 cade (sotto 2,0 m). PR4: S1 = 0 nelle 16 combinazioni e sul
corpo muto; S2 regge a k = 0,004 (>= 2,7 m) e cade a k = 0,0100; resa col 30 % sparso sotto il 40 %.
Soglia di smentita: la cifra indicata. A ±1 grado nessuna promessa.

## Esiti del lancio 2 (scritti alle 2026-11-14T17:59:43+01:00; file `riepilogo_banco.txt` = semi del lancio 1, `riepilogo_banco_semi2.txt` = semi nuovi)

Le cinque regole del lancio 1 ridanno righe identiche (`diff` vuoto fra `risultati_banco.txt` e `risultati_banco_lancio1.txt`).
- PR1: S1 **regge** nelle 16 combinazioni (0 e 0), **cade** sulla scatola lontana (79 e 74 celle); S2 cade come previsto (1,3 m).
- PR2: **regge** la previsione «S1 non 0» (corpo muto 404 e 414 celle; 1 cella nelle 16 combinazioni coi semi nuovi); S2 regge (3,0 m).
- PR3: S1 0 coi primi semi, **1 cella** coi nuovi (smentita); S2 cade (1,3 m).
- PR4: S1 **regge**: 0 celle in 9 000 + 9 000 fotogrammi (tutte le 10 scene, 2 k, 5 buchi, errore 0 e ±0,5). S2: previsto «cade a
  k = 0,0100», **smentita in bene** (3,0 m a entrambi i k). Resa col 30 % sparso: previsto sotto il 40 %, **smentita in bene** (62,6 e 62,4 %).
  A -1 grado cade sulla scatola da 10 cm a 2,6-2,9 m (150 e 145 fotogrammi su 300); a ±1 nelle 16 combinazioni 0.
- P9 (fotogrammi di f10): **smentita** in 3 sequenze su 4: V17 da' piu' celle di V18-1 (pavimento vuoto 596 contro 522; cassa 1 064
  contro 962; TUM 70 contro 4); solo sul pavimento lucido V18-1 ne da' di piu' (173 contro 120).
Notato dopo, non previsto: sul modello del sensore al livello limite il 21 % dei pixel validi dell'impronta legge fuori da m(z)
(`diagnosi_f10.txt`); sul fotogramma vero il 37 % legge piu' vicino del suolo atteso.
