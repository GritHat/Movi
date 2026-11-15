# MoVi · voce guida inglese (`sciame-comunicazione`, f17-video/40-voce)

Dalle 01:53:55 alle 02:13 del 2026-11-15 (`date -Is`). Fonti: `PIANO_VIDEO.md` (letto per intero), `voce_{en,it}_v2.txt`,
`VERDETTO_FASE2.md` (§1–§9), `STRUMENTI.md` §3, il registro `prototipo/uscite/lp_E1/registro.jsonl` (riga 1).
`prototipo/uscite/video/` **non esiste** alle 01:54: nessun registro del video usato, la voce non ne dipende.

## 0. In testa: cambi di stato e regole

- **Scritture:** solo in `video/` e qui. `video/progetto/cifre.json` esisteva già (v6 di un altro ruolo, letta da
  `strumenti/monta_v6.py`): prima l'ho copiato in `progetto/versioni/cifre.20261115-v6-prima-della-voce.json`, poi l'ho
  riscritto **compatibile** (stessi campi `en`/`it`/`stato`, più `voce_en`/`voce_it`/`voce_senza_*`, `righe_schermo`,
  `pronuncia`). Una copia in più senza uso: `video/voce/testi/voce_en_v3.modello.txt.bak`. Nessun file cancellato,
  niente git, niente sudo, niente rete; Kokoro e ASR uno alla volta, con `timeout`.
- **Previsioni:** non ne ho scritte prima delle prove (regola 3 non rispettata per mancanza di tempo). Quella del piano
  (circa 146 s a 129 parole al minuto, pause escluse) è compatibile con la misura: 158,8 s con le pause.
- **Indipendenza:** il controllo d'intelligibilità (faster-whisper `small`) non condivide il modello con Kokoro, ma
  condivide il testo di riferimento. Nessun ascolto umano.

## 1. Le cifre (in `cifre.json`, unica fonte; voce, schermo e sottotitoli da lì)

| Chiave | Detto (EN) | Stato | Fonte (verdetto) |
|---|---|---|---|
| STATO-1 | «Event rules are not yet in the prototype.» | sostenuto: `regole_accese = [correzioni_f12]` in lp_E1 | §4; registro lp_E1 |
| L-46 | «Almost half the values are assumed.» (46 %) | verificato come limite | §7 n. 1 |
| L-VOLO | «For aircraft in flight, warnings are not yet in time.» | limite (N/X) | §1 n. 1, §7 n. 2 |
| A1 | «…a drone hidden behind a building was announced in time in two hundred passes out of two hundred.» | S, Pd ipotetica | §6 n. 1 |
| CIFRA-V2 | «Zero passes out of six hundred lost that warning.» | S (regola prudente) | §6 n. 5 |
| E1-X | «Our weak point: …contact was declared within two seconds in one run out of sixteen.» | X, detto come limite | §6 n. 12 |
| E2-C | «…MoVi marks them unreliable, in thirty-two runs out of thirty-two.» | S, non indipendente | §6 n. 8 |
| A2, A4, A7, E2-X | solo a schermo (scene 3, 7, 4, 6) | S / S / S / X | §6 n. 2, 4, 7, 12 |
| tolte | S2 (da non dire: «rileva droni a 3 km»), S3, S3b, S7, V3 (non nel verdetto), V1 (smentita), S1 (aerei in volo senza il limite accanto inganna) | — | §6, §8 |

Scelte da far confermare all'arbitro: **(a)** V2 riempita con l'affermazione n. 5, non con la misura E1–E4 del piano
§3.2 (che il verdetto non dà); **(b)** la frase di STATO-1 riscritta, perché «the full chain has not yet run end to end»
contraddirebbe il §6 n. 10 (il prototipo gira a lunga portata su 20 scene); **(c)** i due limiti degli eventi detti
**nella scena in cui si vedono**, non solo nella 7.

## 2. Il testo detto (EN, 330 parole; `video/voce/voce_guida_en_v4.txt`)

Cambi rispetto alla v2, oltre alle cifre: scena 2 senza «MoVi declares what it has not observed» (taglio 1 del piano);
scena 5 senza «Then they touch» (taglio 3) e senza «The operator is warned: a person is underneath» (funzione non nel
verdetto: Q30); scena 6 senza «Downstream: possible debris, unverified» (taglio 2) e con la variante «during taxi» (E2
ha `aereo_rullaggio`); scena 7 asciugata («Everything is simulated…», «Classes…», «Total delay: not measured»); scena 9
«A project by SDMs», perché all'ASR «No output is a command. By SDMs» diventava «a command by SDMS».
Pronuncia solo nel testo dato a Kokoro (`cifre.json` → `pronuncia`): `MoVi → Mowvee` (fonemi `mˈəʊviː`; «MoVi» dava
`mˈəʊ vˈaɪ`), `SDMs → S D M S`. Numeri in lettere. Termini vietati: 0 (controllo automatico in `voce_util.py`).

## 3. Misure (bm_george, en-gb; `video/voce/uscite/`)

| Versione | Voce | Parole/min | Picco | Saturi | Silenzi > 1 s | Montaggio con le durate del piano | Con le durate proposte |
|---|---|---|---|---|---|---|---|
| **1.0 (scelta)**, `en_v4_1.0` | 158,77 s | 125 | −2,9 dBFS | 0 | 0 | 178,8 s (fuori da Q1) | **172,8 s** |
| 0,95, `en_v3_0.95` (testo a 331 parole) | 164,12 s | 121 | −3,0 dBFS | 0 | 0 | 180,5 s | 174,8 s (al limite) |

Testa 0,19 s, coda 0,25 s, pausa interna massima 0,94 s (le 8 pause di scena), −19,9 LUFS. ASR su 1.0: 14/335
differenze, tutte di grafia (cifre, «Movi», «labeled») salvo una vera («Our weak point» → «A weak point»).
**Scelgo 1.0:** la differenza di passo è piccola (125 contro 121 parole al minuto), e solo 1.0 entra in 165–175 con
margine. La chiarezza «a orecchio» è **non verificata** (nessun ascolto).

Tempi per scena (1.0, voce in s → scena = max(piano, 0,4 + voce + 0,6)): 1: 11,3 · 2: 18,6 · 3: 12,7 · 4: 18,0 ·
5: 19,6 · 6: 16,8 · **7: 35,2** · 8: 7,6 · 9: 12,3. Tempi di ogni frase (44) in `voce_guida_en_v4.wav.tempi.json`,
con la grafia vera e il campo `scena`; un WAV per scena in `uscite/en_v4_1.0/voce_en_scenaN.wav`.

**Proposta di durate (per videomaker e arbitro):** 12,5 · **22** · 16 · 21 · 22 · 20 · **36,5** · **10** · 13,5 = 173,5 s.
La scena 2 cede 5 s alla 7 (che il piano non taglia mai) e la 8 un secondo. Senza questo, il totale esce a 178,8 s.

## 4. Italiano (im_nicola, prova sull'intero testo, non solo su due scene)

- `it_v4_1.0`: con le pause dell'inglese il modello lascia circa 0,3–0,45 s di coda per frase: 35 silenzi > 0,6 s,
  8 > 1 s; montaggio 184,6 s, scena 7 +4,1 s sull'inglese. **Corretto nello script**: per `it`, pause 0,05/0,45.
- `it_v5_1.0` (348 parole, 4 tagli in più): voce 152,5 s, pause 0,41 s di mediana, 0 silenzi > 1 s, saturi 0. Con le
  durate proposte l'italiano entra in ogni scena (7: 35,4 s contro 36,5). **Sfora Q2**: 348 parole contro 340.
- ASR italiano: 42/348 differenze; da sentire **«mai vuoto» → «ma i vuoto»**, «Per gli aerei» → «In via aere»,
  «i limiti» → «il limiter». Rischio vero di malinteso sulla frase centrale: non risolto.

## 5. Critiche e rischi (da passare a chi monta)

1. Scene 5 e 6 mostrano eventi «dedotti», ma il §6 n. 12 li dà come punto debole: la voce ora lo dice; a schermo la riga
   `WARNING TO OPERATOR · UNVERIFIED ZONE ON VEHICLE PATH` va sostituita da E2-X (0 su 32), e `PERSON IN FOOTPRINT` va
   tolta se nessun registro la dà.
2. `monta_v6.py` non legge ancora `righe_schermo` né i campi `voce_*`: finché non lo fa, le righe tolte restano
   magenta e `--finale` rifiuta (è il comportamento giusto).
3. «Warnings would come too late» (scena 4) e «reliability is lost» non hanno una cifra nel verdetto: sono stati del
   registro R3c, che **non esiste** ancora.
4. La pronuncia voluta di «SDMs» e di «MoVi» resta da confermare dalla squadra.

## 6. Che cosa propongo dopo

1. L'arbitro conferma (a), (b), (c) del §1 e le durate del §3; poi `rimonta.py --voce-en video/voce/voce_guida_en_v4.wav
   --testo-en video/voce/voce_guida_en_v4.txt`.
2. Un ascolto umano di `voce_guida_en_v4.wav` (5 minuti), sulle tre frasi delle cifre.
3. Per l'italiano: 8 parole in meno e «mai vuoto» riscritto («mai dato per vuoto»?), poi `genera_voce.sh it`.
4. Alla fine della fase 2b: si cambia solo `cifre.json`, poi `video/voce/genera_voce.sh en` e `… it`.
