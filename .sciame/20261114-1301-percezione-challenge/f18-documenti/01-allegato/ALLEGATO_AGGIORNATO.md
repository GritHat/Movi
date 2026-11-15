# Allegato tecnico aggiornato: veicoli veloci (copia v2)

`sciame-redattore`, 15-11-2026, dalle 03:03 alle 03:16 circa (`date -Is`). Previsioni scritte prima, alle 03:03, in
`PREVISIONI.md`. Copia: `allegato_tecnico_v2/` (PDF `allegato_tecnico_v2/allegato_tecnico.pdf`, 83 pagine contro 71).
L'originale in `allegato_tecnico/` non l'ho toccato. Tutto è simulazione dalle schede, conto o traiettorie pubbliche:
niente è «validato».

## 0. In testa: esiti, regole e stato della 2c

- **Previsioni.** P1–P5 reggono. Compilazione (xelatex, bibtex, xelatex, xelatex): 0 errori, 0 citazioni o riferimenti
  indefiniti, 0 avvisi di bibtex, nessun «Overfull» (i tre che c'erano, da 15 a 34 pt, li ho corretti). Il PDF passa
  da 71 a 83 pagine.
- **Parole vietate** (`strumenti/controlla_parole.py`, esito in `controllo_parole_v2.txt`). Il programma toglie i
  commenti e cerca 37 espressioni: sciame, ruoli, fasi, verdetti, sigle K/X/H/F, nomi di scenario come E1 o A1,
  `.md`, «validato», «in tempo reale», il lessico d'ingaggio, «bersaglio», v1/v2, riprova, nucleo e altre. Trova 26
  occorrenze nella v2 e le **stesse 26 nell'originale**. Sono usi tecnici che c'erano già: «bersaglio bianco» di una
  scheda, «nucleo» di CPU, «in tempo reale» detto di lavori altrui, «famiglia» di camere. Il testo nuovo ne ha 0.
  Restano visibili i nomi dei file di scena del prototipo (`lp_A1`) nei comandi dell'appendice B, perché la consegna
  chiede quei comandi.
- **Fase 2c.** Alle 03:14 `60-fase2c/02-verdetto/VERDETTO_2C.md` non esiste (c'è solo `01-correzioni`). Le cifre
  vengono quindi da VERDETTO_2B. Le frasi che la 2c può cambiare portano il commento LaTeX `% 2C` (8 punti): il
  «libero» col pannello, la collisione e le scene, nel cap. 9 nuovo, nel sommario, nella tabella di sintesi, nei
  limiti, nelle conclusioni e nell'appendice B.
- **Regole.** Ho scritto solo in `f18-documenti/01-allegato/` e non ho cancellato niente. I file che ho modificato
  sono nella mia copia, e accanto a ciascuno c'è una copia `_prima` (`*_prima.tex`, `allegato.bib_prima`). Le
  immagini di controllo sono in `pagine_v2/`. Non ho usato rete, git o sudo, e ho lanciato un processo alla volta.
  `allegato.bib` porta in testa «generata da programma: non modificare a mano»: le 16 voci nuove le ho aggiunte a
  mano in fondo, dichiarandolo in un commento. Se il bib si rigenera, vanno aggiunte al generatore.

## 1. Che cosa ho aggiunto e cambiato

| File | Modifica |
|---|---|
| `capitoli/10_lunga_portata.tex` (nuovo; nel PDF è il cap. 9, prima delle conclusioni) | scala e distanza d'avviso (tab. per scenario); sensori dalle schede (tab. con le ipotesi); «libero» per classe con Pd cumulata, Prop. «n_eff = 1 è prudente» (D), mappa come ingresso di sicurezza, classi escluse; inseguimento multisensore; insieme di possibile presenza (Prop. di contenimento, D) e spegnimento prudente (564/2400 contro 0/600); traiettorie pubbliche (tab. delle fonti; tab. per mezzo); eventi e visibilità degradata (regole, Prop. sul volume dei detriti, D nel modello; nube, abbagliamento, meteo con tab.); prove del caso centrale (tab. con N e Wilson); aerei in volo come limite; smentiti come limiti; riquadro di validità |
| `allegato_tecnico.tex` | `\input` del capitolo nuovo; titolo «…, dal corto raggio ai veicoli veloci» |
| `00_sommario.tex` | un paragrafo sulla seconda scala, il caso centrale, le cifre e i limiti |
| `01_introduzione.tex` | le due scale e il caso centrale; contributo 8; 8 righe nella tabella di sintesi; «Dominio a lunga portata» nel riquadro; ambiti d'uso (il secondo uso resta a corto raggio); struttura |
| `08_limiti.tex` | § «Limiti a lunga portata» (L1–L6) |
| `09_conclusioni.tex` | paragrafo «Ai veicoli veloci» |
| `A_parametri.tex` | tab. dei parametri a lunga portata (21 righe) |
| `B_riproducibilita.tex` | comandi del prototipo, durate, costo per ciclo |
| `allegato.bib` | 16 voci: IRIS, SCANTER 5000, AT128, Tele-15, EchoGuard, 14 CFR 91.227 e 89.310, Johnson e Stopping sight distance (Wikipedia, dichiarate secondarie), adsb.lol, Zenodo 18916312, TrajAir, il drone CMU, ALFA, NGSIM (doi 10.21949/1504477), Digitraffic |

## 2. Cifre e fonti (cartelle sotto `f15-lunga-portata/`)

- **Distanze d'avviso** 806 / 147 (277) / 3900 / 126 (60) / 67 (24) / 261 (798) m: `03-scenari/SCENARI_E_REQUISITI.md` § 1.
- **Sensori; 57 ipotesi su 124 campi; R(σ); Swerling; 62 %:** `02-sensori/SENSORI_LUNGA_PORTATA.md` § 2 e § 7,
  `parametri_lunga_portata.json` (EchoGuard).
- **«Libero» 2360 → 877 m; 0,263 contro 0,010:** `04-moto/MODELLI_E_REGOLE.md` § 1, `50-fase2b/01-nucleo/NUCLEO_V2.md`
  § 1, `20-attacco/ATTACCO_LP.md` (riga X4).
- **Inseguimento: 39,9 contro 4,4 m, 40/40; 0/40 [0; 0,088]; 60 000 traiettorie; 675 m:** `04-moto` § 2–3.
- **Inviluppo 210 e 45 m/s, 25 m/s²; scatto a 60 m/s fuori a 8 s; mappa:** `NUCLEO_V2.md` § 1–2 e VERDETTO_2B § 1.
- **564/2400 [0,218; 0,252] e 0/600 [0; 0,006]:** VERDETTO_FASE2 § 1.3. **0/200 senza regione:** VERDETTO_2B § 1.
- **Traiettorie** (tab. per mezzo; 105/722, 167/730, 8–11 aerei su 43; treni 61/405, 18 su 19):
  `21-statistica/CONTROLLO_LP.md` § 2.1 e VERDETTO_FASE2 § 2. **ALFA 0,656, virate 0,74 e 0,72 (per tratto):**
  `12-traiettorie/PROVE_SU_TRAIETTORIE.md` § 1. **Fonti dei dati:** `01-dati/PROVENIENZA.md`, `DATI_PUBBLICI.md`.
- **Eventi** (regole, volume, 0 su 1 131 692 e 0 su 646 957, meteo): `40-eventi/02-regole/REGOLE_E_SCENARI_EVENTI.md`
  § 2–3. **Collisione** 49/60 e 24/30, 0,9973, 36/60 ≥ 10 km, 42 e 74 km, 1/60 a −12,5 s; **avaria** 60/60, 90/90,
  3,5 km; **fumo** 0/120 e 0/60; **passaggio ravvicinato** 0/300 e 0/30: VERDETTO_2B § 1–2. **4,2·10⁸, 1080 cicli,
  460/460:** VERDETTO_FASE2 § 2 e § 6. **5,3 s, falsi avvisi 3,8–1594 all'ora, costo 11/46/340 ms:**
  `11-prove/PROVE_LUNGA_PORTATA.md` § 3.7–3.9.
- **Caso centrale** (200/200, 100/100, 12/200, 9/100, 22 e 34 su 200, 50/200, 0/200 «libero», 95/100 e 9/100;
  auto 200/200, treni 186/200): VERDETTO_2B § 1–2 e VERDETTO_FASE2 § 2. **163/171, 85/85, 0/171 con 8 falsi;
  3410 > 877 m; 7,57 km:** VERDETTO_2B § 1, VERDETTO_FASE2 § 1.
- **228/228; 665 s; 35 min; 66 s; 88 s; 34,5 s:** VERDETTO_FASE2 § 3.3 e § 8, VERDETTO_2B § 2,
  `10-riprova/prova_tutto_esito.txt`, le intestazioni dei rapporti 12-traiettorie, 40-eventi/02-regole e 04-moto.
- **Wilson:** li ho ricalcolati tutti con il mio codice (29 valori di k/n) e coincidono con le fonti. Gli
  intervalli bootstrap per mezzo li ho ripresi senza ricalcolarli.

## 3. Dubbi di contenuto per l'autore

1. Varie cifre sono state ottenute con l'inviluppo precedente (90 m/s): rullaggio col solo radar, auto, treni,
   460/460, nebbia, 228/228, 0/300. Nel testo le ho marcate «con l'inviluppo precedente», senza dire perché fossero
   state misurate così.
2. Il commento `% 2C` va tolto, o le cifre vanno allineate, quando esce VERDETTO_2C.
3. Ho descritto l'«avaria: mezzo avvisato a ≥ 140 m in 60/60, ma 0/60 dal bordo dell'impronta» rileggendo
   VERDETTO_2B § 1. La forma esatta della seconda misura è **non verificata**.
4. Il titolo della pagina NGSIM l'ho preso com'è in `PROVENIENZA.md`. Per autori e titoli delle altre voci ho usato
   solo ciò che riportano `01-dati` e `02-sensori`: gli autori sono dati per cognome, con «and others» dove manca il
   resto.
