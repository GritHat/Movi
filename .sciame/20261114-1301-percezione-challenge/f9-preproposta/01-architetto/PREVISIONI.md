# Previsioni — `sciame-architetto`, f9, strategia S1 (selettore della configurazione)

Scritte alle **2026-11-14T15:41:31+01:00** (`date -Is`), dopo aver letto contratto, addendum, preproposta per intero,
`SOLUZIONE_V2.md`, `VERDETTO.md`, `AUDIT.md`, `FONTI_VERIFICATE.md`, `f1/985ccd9bca46/CONSEGNA.md` e il sorgente v0.5,
e **prima** di scrivere o lanciare qualunque script. Nessuna prova eseguita finora.

Avvertenza: di P1 e P3b conosco già il verso da un conto a mente fatto leggendo i file; valgono come conti, non come
prove riuscite. P2, P3a e P5 non le ho calcolate.

## P1 — «1,1 m» è una distanza dal sensore, non un'altezza (conto)

- **Misura:** con camera a 1,2 m, inclinata di 15° verso il basso, campo verticale 58° (B1 del nucleo): distanza da cui
  si vede il suolo; distanza sotto cui un ostacolo alto 15 cm è fuori campo; distanza oltre cui si vede un oggetto a
  1,8 m di quota.
- **Previsione:** 1,24 m, 1,09 m, 2,41 m (entro 1 cm): i tre numeri del nucleo sono limiti del campo visivo. Cambiando
  la sola rappresentazione (griglia sul piano → voxel) restano identici, perché dipendono da quota, inclinazione e campo.
- **Smentita:** uno dei tre numeri differisce di oltre 2 cm; oppure il conto mostra che il limite dipende dalla
  struttura dati.

## P2 — Oscillazione del selettore (simulazione, attacco 3 visto dall'architettura)

- **Modello:** ciclo a 15 Hz; costo per ciclo T = costo della configurazione corrente + rumore; il selettore valuta
  ogni 1 s la media degli ultimi 15 cicli con la tabella della preproposta (T > 55 ms → degrada; T < 45 ms → risale).
  Scenario A (strutturale): configurazione piena 60 ms, ridotta 40 ms, rumore σ = 2 ms. Scenario B (attacco 3): piena
  55 ms con carico esterno sinusoidale ±6 ms di periodo 4 s, ridotta 12 ms in meno.
- **Bracci:** (a) tabella nuda; (b) tabella + isteresi temporale di 2,5 s (quella che propone la preproposta);
  (c) degrado immediato, risalita solo dopo sosta e con costo **previsto** (misurato ridotto + delta del modulo);
  (d) degrado a scatto, senza risalita automatica (versione minima).
- **Previsione:** nello scenario A il braccio (a) cambia ≥ 20 volte al minuto; il braccio (b) continua a oscillare
  **senza fine**, fra 10 e 24 cambi al minuto (24 = 60/2,5), e sta in una configurazione fuori bilancio (> 55 ms) per
  il 35–65 % del tempo; i bracci (c) e (d) fanno al più 1 cambio in 10 minuti. Nello scenario B: (a) ≥ 10 cambi al
  minuto, (b) ≥ 5, (c) e (d) ≤ 1 in 10 minuti.
- **Smentita:** nello scenario A il braccio (b) fa ≤ 2 cambi al minuto (allora l'isteresi temporale basta e la mia
  critica cade); oppure (c) o (d) fanno più di 1 cambio in 10 minuti.
- **Braccio che deve fallire:** (a) nello scenario A; se non oscilla, il modello è cieco.

## P3 — Il degrado della mappa può far nascere un «libero» (conto e simulazione)

- **P3a, griglia più grossa.** Griglia polare 1° × 0,1 m (87°, 1,24–3 m) con un pannello largo 1 m a 1,8 m, la sua
  ombra, e l'1 % di raggi senza dato (seme fissato). Si passa a 2° × 0,2 m in due modi: (i) la regola di B2 applicata
  alla lettera alla cella grossa («suolo visto e nessun ostacolo» = almeno un raggio della cella vede il suolo, nessuno
  vede un ostacolo); (ii) aggregazione prudente (la cella grossa è «libero» solo se lo sono tutte le celle fini che
  contiene). **Misura:** celle fini «in ombra» o «non osservato» che finiscono dentro una cella grossa «libero».
  **Previsione:** (i) > 0, fra 50 e 2000 celle fini su circa 15 000; (ii) esattamente 0 (controllo dell'invariante,
  non dato). **Smentita:** (i) dà 0 (allora la regola alla lettera è già prudente); (ii) dà > 0 (errore mio).
  **Braccio che deve fallire:** (i).
- **P3b, da tre fasce di quota a mappa sul piano.** Con le fasce di S10 (0,15–0,60; 0,60–1,60; > 1,60 m, chiusa a
  2,0 m come il tetto del nucleo) e la regola «libero solo se tutte le fasce pertinenti sono osservate e libere»:
  **Previsione:** la fascia media è osservata per intero solo da circa 1,6 m; la fascia alta non è osservata per intero
  in nessun punto entro 3 m; passando alla mappa sul piano, l'anello 1,24–1,60 m (circa 0,7–0,8 m², 12–15 % della zona
  di valutazione) passa da «non libero» a «libero» per il solo cambio di configurazione. **Smentita:** l'anello è vuoto
  (la fascia media è osservata per intero già da 1,24 m).

## P4 — Costo di calcolo del selettore (misura su CPU)

- **Misura:** tempo di una valutazione della tabella (6 righe, media mobile su 15 cicli) in Python puro.
- **Previsione:** < 10 µs a valutazione; a 2 Hz meno dello 0,001 % di un ciclo da 66,7 ms. Il costo del selettore non è
  nel calcolo. **Smentita:** > 1 ms a valutazione.

## P5 — La tabella non è una funzione degli ingressi (enumerazione)

- **Misura:** si enumerano gli stati d'ingresso che la tabella nomina: T in {< 30, 30–45, 45–55, > 55 ms} × GPU {sì,
  no} × saturazione IR {sì, no} × interferenza {sì, no} × camera frontale {sana, guasta} × ToF laterali {sani, assenti}
  = 128 stati; per ciascuno si contano le righe che scattano (lettura «/» = «oppure» e lettura «/» = «e» per la riga 2).
- **Previsione:** in tutte e due le letture meno del 30 % degli stati fa scattare esattamente una riga; almeno il 10 %
  non ne fa scattare nessuna; almeno il 40 % ne fa scattare due o più. Le configurazioni nominabili (camera × modo dei
  ToF × mappa × rete) sono almeno 30, contro 6 righe.
- **Smentita:** almeno il 60 % degli stati fa scattare esattamente una riga (la tabella è quasi una funzione).

---

# Esiti (scritti alle 2026-11-14T15:45:54+01:00 da `date -Is`, dopo il lancio delle 15:44:02; file `risultati_s1.txt`)

Comando per rifare: `timeout 120 python3 -I prove_s1.py > risultati_s1.txt` (meno di 1 s; seme 20261114).

| # | Esito | Numeri |
|---|---|---|
| P1 | **regge** (conto di cui conoscevo il verso) | 1,243 m; 1,087 m; 2,406 m; montaggio verticale 0,735 m |
| P2, scenario A | **regge** | (a) 600 cambi in 10 min; (b) 200 cambi (20 al minuto), 49,7 % dei cicli oltre 55 ms; (c) 1; (d) 1 |
| P2, scenario B | **regge** per (a), (b), (d); **non risolta** per (c) | (a) 300; (b) 150; (d) 1; (c) 1 con risalita sotto 45 ms, ma 11 con 50 ms e 100 con 55 ms |
| P3a | **regge nel verso, smentita nel numero** | (i) 10 celle fini, non 50–2000; il denominatore è 1566 celle, non «circa 15 000» (errore mio di conto); (ii) 0 |
| P3b | **regge** (conto di cui conoscevo il verso) | fascia media intera da 1,604 m; fascia alta intera da 3,209 m (mai entro 3 m); anello 0,78 m², 13,8 % della zona |
| P4 | **regge** | 0,22 µs a valutazione (indicativo) |
| P5 | **smentita in parte**; la soglia di smentita (≥ 60 % con una sola riga) non è raggiunta | lettura «oppure»: nessuna riga 13,3 %, una sola 45,3 % (prevedevo < 30 %), due o più 41,4 %; lettura «e»: 39,8 %, 29,7 %, 30,5 % (prevedevo ≥ 40 %); 45 configurazioni nominabili contro 6 righe |

**Notato dopo, non previsto.**
- La soglia di risalita del braccio (c) non era nelle previsioni: l'ho fissata a 45 ms (la soglia «CPU scarica» della
  preproposta) scrivendo lo script, prima del lancio, e ho aggiunto la sensibilità a 50 e 55 ms. Con 50 e 55 ms il
  braccio (c) torna a oscillare: solo il braccio (d) regge per costruzione.
- Varianti di P3a aggiunte scrivendo lo script (dopo le previsioni, prima del lancio): con la griglia da 0,5 m, come in
  B1 del nucleo, le celle non viste sotto un «libero» sono 98 (87 sono l'anello cieco fra 1,1 e 1,2 m, che cade nella
  stessa cella grossa del primo suolo visto); 112 con l'1 % di celle morte; 87–109 spostando il pannello di lato in 21
  posizioni. Dipende dall'allineamento della griglia grossa.
- Con il profilo «bassa + media + alta» la regola di S10 non lascia nessuna cella «libero» entro 3 m.
