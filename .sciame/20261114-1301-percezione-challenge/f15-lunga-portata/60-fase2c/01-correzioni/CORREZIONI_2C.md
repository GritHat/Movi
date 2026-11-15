# Correzioni rapide al caso centrale (fase 2c, 01-correzioni)

`sciame-tracciamento`, 2026-11-15, dalle 03:03 alle 03:33 (`date -Is`). Previsioni e soglie scritte prima, alle 03:06,
in `PREVISIONI.md`, con il seme delle scene. **Tutto è simulazione dalle schede: nessun sensore fisico, niente è
«validato».** Etichette a mano. Solo osservazione e avviso. Frequenze per passaggio (un record per passaggio), Wilson
al 95 %, ricontate da `analizza_2c.py` → `analizza_2c_esito.json`.

## 0. In testa: cambi di stato e regole

- **K-613 letterale (solo la finestra W_c legata alla v_max vera): la previsione del coordinatore è smentita**,
  163/171 come col v2. La mia previsione contraria, scritta prima, regge. **v3 completo (finestra + ritenuta del
  ritorno): 0/171 [0; 0,022], regge** (soglia ≤ 2/171).
- **X5 (cp_X5b) chiuso nel predefinito del prototipo:** 0 «libero» su 6. Resta aperto quando una scena dichiara la
  mappa: 5 su 6 «libero» dietro l'edificio non in pianta. La validazione-3 non è chiamata.
- **E1, impronta: regge.** Mediana 4,5 km, 0/60 ≥ 10 km. Ma l'ispezione non ha tolto un solo punto (0/60): la
  riduzione viene tutta da t_a.
- **E1 entro 2 s: resta smentito**, 51/60. La separazione falsa prima dell'urto (passaggio 31) è tolta: 0/60.
- **`prova_tutto.sh`: esito 0** in 698 s. Le 20 scene lunghe hanno girato col v3.
- **Regole.**
  - Ho scritto nel prototipo (permesso dalla consegna), con una copia di prima: `movi/lungo.py.prima_2c`,
    `movi/__main__.py.prima_2c`, `prova_tutto.sh.prima_2c` (non modificato), `uscite/video/INDICE.md.prima_2c`.
  - Ho rigenerato due volte, sovrascrivendole, le mie cartelle `uscite/video/*_v3`. Il primo giro aveva un
    `NameError` nella maschera; il suo esito è in `genera_video_v3_esito_giro1.txt`.
  - Ho fatto un `mv -n` di un mio file d'esito.
  - `prova_tutto` riscrive `uscite/lp_*`, come sempre. Niente `rm`.
  - Per circa 10 minuti hanno girato insieme `prova_tutto` (fino a 3 scene) e le scene video (1): ho stimato al
    più 6 processi Python, senza contarli in modo continuo (**non verificato**).
  - La regola dell'età minima della traccia d'origine (3 s) l'ho aggiunta **dopo** il pilota sul passaggio 31, che
    il verdetto già nominava.

## 1. Che cosa ho cambiato (codice)

**Nucleo `movi_lp_v3.py`** (copia del v2, con interruttori di modulo):
```python
FINESTRA_INVILUPPO = True   # K-613: W_c = min(t_cumulo, lato / v_vera), v_vera = max v_max delle classi ammesse;
                            # il lato conta anche l'elevazione (dist * del)
T_RITENUTA_S = 5.0          # ritorno (o alone) nella cella o nelle 26 vicine negli ultimi 5 s -> mai «libero»
...
bv = self._vicinato_max(blocco); out = np.where(t - bv <= T_RITENUTA_S, 0.0, out)
```
Perché serve la ritenuta: con passate correlate (n_eff = 1) basta **una** passata mancata, subito dopo un ritorno,
per dare «libero» sulla cella del drone. Col pannello, che fa una passata ogni 0,1 s, succede quasi in ogni
passaggio. La lunghezza della finestra qui non conta: la classe vincolante era già `multirotore_veloce` (45 m/s).

**Eventi `eventi_v3.py`:**
- avversario-1: traccia d'origine vista da ≤ 2 s e nata da ≥ 3 s; t_a ≥ (primo ritorno nuovo − un giro − 2 s), e un
  contatto lungo non sposta più t_a (prima di 14 s, quindi r0 = ½·25·14² m);
- duplicati: un contatto di ≥ 4 s con |Δv| < 3 m/s non fa coppia d'origine;
- avversario-2: impronta campionata (24 × 48 punti). Un punto esce solo se, dopo t_a + T_c, una griglia affidabile e
  non accecata lo dice «libero» per ogni classe e per il frammento minimo;
- avviso ai mezzi: sull'impronta **residua**;
- mappa degli scenari E (senza ostacoli) dichiarata con `EVENTI_MAPPA_CERT=1`, che è un'ipotesi.

**Prototipo:**
- `--nucleo v3` è predefinito; v1 e v2 restano. Le copie stanno in `riuso/lunga_portata_v3/` (`PROVENIENZA.md` con
  gli sha256).
- Col v3 la mappa **non** è dichiarata per predefinito. La dichiara solo `"mappa_certificata": true` della scena, o
  `MOVI_MAPPA_CERTIFICATA=1`, e la dichiarazione è scritta nell'intestazione.
- `_maschera_v3`: nel registro, una cella «libero» dentro un avviso o dentro i detriti diventa «non_osservato», e il
  numero va in `celle.libere_tolte_dentro_avviso`.
- Prima della prima pianta, i conteggi = n² «non_osservato».

## 2. Risultati

| Misura (soglia scritta prima) | v2 (VERDETTO_2B) | v3 | Stato |
|---|---|---|---|
| A1 alta, «libero» sul drone non C0 (≤ 2/171; smentita ≥ 10) | 163/171 | **0/171** [0; 0,022]; 0/19 494 istanti. Letterale: 163/171 | v3 regge; K-613 letterale smentita |
| A1 alta / min tempestivi (≥ 190/200) | 200 / 200 | 200/200 e 200/200 [0,981; 1] | regge |
| A1 min fuori avviso (< 19/200) | 12/200 | 12/200 [0,035; 0,102] (6 «ferma», 6 «rallenta») | invariato: K-606 aperto |
| cp_X5b nel prototipo, predefinito (0 «libero» su 6) | 5/6 | **0/6** (stato 3); con la mappa dichiarata 5/6 | regge solo nel predefinito |
| E1 evento (n = 60) | 49/60 entro 2 s | 60/60; entro 2 s **51/60** [0,739; 0,919]; ritardo 1,2–1,8–2,3 s | smentita (< 57/60) |
| E1 prima dell'urto (0) | 1/60 | **0/60** [0; 0,06] | regge (regola notata dopo) |
| E1 impronta, mediana ≤ 5 km; smentita se ≥ 10 km in ≥ 10/60 | 42 km; 36/60 | R_imp 4,3 km; **residua 4,5 km** (3,1–5,3); **0/60** ≥ 10 km | regge |
| E1 punti tolti dall'ispezione | — | **0/60** passaggi. T_c mediano 213 s contro 32 s di passaggio | l'ispezione è vuota |
| E1 «libero» su un frammento (0) | 0/60 per costruzione | 0/60, ma 0/28 512 punti «libero» nell'impronta | ancora vuoto |
| E2 (n = 30): evento, camere entro 3 cicli | 60/60 | 30/30, 30/30 [0,886; 1] | regge (innesco ottimista) |
| E2 avviso al mezzo ⇔ il mezzo entra davvero nell'impronta (≥ 29/30) | — | 30/30, ma entra in 30/30: non discrimina; tracce avvisate, mediana 96 | regge senza valore discriminante |
| E5, 5 m (0/30 falsi) | 0/30 | 0/30 [0; 0,114] | regge |
| Scene video _v3, validatore della controprova (0) | `lp_A1`: 56 | **0 su 8 scene**, convalida 0 errori su 8 | regge |
| `prova_tutto.sh` (0) | 0 | **0**, 698 s | regge |

**Scene.** `lp_A1_v3` è il passaggio 90 e `lp_E1_v3` il 30, tutti e due scelti a caso. `lp_A1_v3` non ha una fase
nascosta: è il caso tipico, perché solo 22 passaggi su 200 la hanno. Ha 11 293 celle-fotogramma «libero», quindi la
prova non è vuota, e 7 celle tolte dalla maschera. In `lp_E1_v3` l'evento arriva a **2,2 s**, con un'impronta di
5,0 km.

`lp_A2`, `lp_A3` e le scene E non hanno nessuna cella «libero», né col v2 né col v3: lì il validatore controlla il
vuoto. `lp_A1_ingenua_v3` col v3 non fa più da contrasto: resta `lp_A1_ingenua` (v1). Righe nuove in
`prototipo/uscite/video/INDICE.md`.

## 3. Stati proposti

- «Con la ritenuta, il "libero" sul drone in A1 sito è 0/171»: **sostenuto dai dati**, simulazione con la mappa
  dichiarata.
- «K-613 = legare la finestra W_c alla v_max»: **smentito** come rimedio da solo.
- X5: **chiuso nel predefinito del prototipo**, **non risolto** con la mappa dichiarata. La prova che lo deciderebbe
  è la validazione-3 col ritorno dello sfondo nel simulatore.
- E1, impronta ≤ 5 km: **sostenuto**. «L'impronta si riduce guardando»: **non risolto** (la prova è vuota). E1
  entro 2 s: **smentito** (51/60).

## 4. Da non dire

- «validato»;
- «il v3 elimina il "libero" falso» senza dire «mappa dichiarata, simulazione»;
- «l'impronta si restringe con l'ispezione»;
- «avvisa solo i mezzi in pericolo» (in E2 avvisa 96 tracce);
- «E1 entro 2 s»;
- `lp_A1_ingenua_v3` come contrasto.

## 5. Che cosa propongo dopo

1. **Il prezzo della ritenuta.** Contare i falsi confermati e le chiusure tardive su A1, A2 e A3 col v3. Previsione:
   falsi confermati di mediana ≤ 1. Smentita se ≥ 3.
2. **L'ispezione dell'impronta.** Darle un significato vuol dire usare T_c per punto (dal volume V(τ)) invece del T_c
   globale, e un sensore che veda il frammento minimo a terra. Oggi Pd ≥ 0,99 per 1,96·10⁻⁴ m² non c'è in nessuna
   cella.
3. **La mappa.** Chiamare la validazione-3 (`sfondo_atteso`/`sfondo_misurato`) dal simulatore e rifare cp_X5b con la
   mappa dichiarata.
4. **A1 min, 12/200 fuori avviso (K-606).** Seguire il centro dell'avviso ciclo per ciclo.

**Indipendenza.** Stesso autore, stesso simulatore e stessi semi per il codice e la misura. Il validatore video è
della controprova (sciame-avversario), ma condivide il registro. Vale solo per i difetti dell'integrazione.
