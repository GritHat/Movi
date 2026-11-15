# DATI PUBBLICI per aerei, droni, auto e treni (sciame-dati, f15/01-dati)

**In testa.** Niente qui è misurato da un sensore del progetto e niente è «validato»: sono traiettorie pubbliche convertite. **Tutte e quattro le classi hanno dati reali** (nessuna resta «solo simulazione dalle schede» per il MOTO); **le rilevazioni reali di sensori mancano per tutte** (nessun `rilevazioni_<sensore>.csv`: restano simulate dalle schede). Regole: nessuna violata che io sappia. Da segnalare: l'orologio della macchina dice 15 novembre 2026 (00:01-00:16), la consegna dice 14; 749 MB scaricati su 6 GB; scaricamento in 13 minuti (00:01:41-00:14:49); 16 minuti in tutto. Previsioni scritte prima (00:01): `PREVISIONI.md`, 4 reggono, 1 smentita in parte, 1 smentita.

## 1. Che cosa c'è (704 scene, 0 errori di formato: `convertitori/verifica.py`)

| classe | tipo (etichetta a mano dalla fonte) | fonte, licenza | tratti | passo | verità offerta |
|---|---|---|---|---|---|
| aerei | rullaggio 19, decollo 15, avvicinamento 9, sorvolo 6, elicottero 4 | adsb.lol, cattura dal vivo attorno ad Atlanta, 12 min; ODbL 1.0 | 53 | 3,1-5,1 s | posizione ADS-B (GNSS di bordo), NON elaborata |
| aerei | avvicinamento 40, decollo 40 (sotto 3000 m) | Zenodo 18916312 (LHR-ZRH, da OpenSky); CC BY 4.0 | 80 | 1 s | ADS-B già filtrato e interpolato a spline dalla fonte |
| aerei | aviazione generale in circuito | TrajAir (CMU), CC BY 4.0 | 60 | 1 s | ADS-B elaborato dalla fonte; asse x lungo la pista |
| droni | multirotore (DJI Matrice 100) | CMU KiltHub 12683453, CC BY 4.0 | 196 | 0,12 s | GNSS/INS di bordo (±2 m orizz., ±5 m vert. dal README) |
| droni | ala fissa senza pilota (Carbon Z T-28) | ALFA (CMU), CC BY 4.0 | 47 | 0,24 s | GNSS dell'autopilota; molte sequenze con guasto indotto |
| auto | auto 154, camion 2, moto 1 | NGSIM US-101 (US DOT), CC BY-SA 3.0 | 157 | 0,1 s | posizione da telecamere dall'alto (rumorosa, nota) |
| treni | treno passeggeri in linea | Fintraffic digitraffic, 12-11-2026, CC BY 4.0 | 111 | 3,0 s | GPS di bordo; quota assente (z = 0) |

Pagine, dimensioni, sha256, che cosa ho cercato e scartato: `PROVENIENZA.md`. Ogni scena è `traiettorie/<classe>/<nome>/{scena.json, verita.csv}`, un oggetto per scena; 33 MB in tutto.

## 2. Velocità, accelerazioni, virate misurate sui dati (`statistiche.json`)

Velocità = modulo 3D derivato dalle posizioni; accelerazione = derivata del modulo; virata = derivata della rotta. Finestra di derivazione dichiarata per fonte (1 s auto e multirotori, 2 s ala fissa, 5 s aerei, 10 s rullaggio, 15 s treni): **i percentili alti dipendono dalla finestra**.

| tipo (fonte) | tratti / campioni | v mediana | v p95 | v max | \|a\| mediana | \|a\| p95 | virata mediana | virata p95 |
|---|---|---|---|---|---|---|---|---|
| | | m/s | m/s | m/s | m/s² | m/s² | °/s | °/s |
| aereo in avvicinamento (dal vivo) | 9 / 565 | 88,8 | 132,7 | 144,4 | 0,27 | 1,27 | 0,08 | 3,21 |
| aereo in decollo (dal vivo) | 15 / 945 | 83,0 | 179,7 | 193,1 | 0,20 | 1,97 | 0,12 | 3,16 |
| aereo in rullaggio (dal vivo) | 19 / 866 | 2,76 | 12,9 | 16,0 | 0,04 | 0,26 | 0,31 | 5,82 |
| elicottero (dal vivo) | 4 / 258 | 47,9 | 61,3 | 65,0 | 0,18 | 1,13 | 0,19 | 4,06 |
| aereo in avvicinamento (Zenodo) | 40 / 21 572 | 99,4 | 158,0 | 195,3 | 0,81 | 2,69 | 0,08 | 1,86 |
| aereo in decollo (Zenodo) | 40 / 15 420 | 133,7 | 163,9 | 204,6 | 0,89 | 3,27 | 0,08 | 2,21 |
| aviazione generale (TrajAir) | 60 / 21 374 | 38,7 | 56,8 | 137,8 | 0,48 | 2,17 | 0,36 | 4,70 |
| multirotore | 196 / 247 601 | 2,71 | 9,74 | 14,3 | 0,14 | 2,13 | 0,46 | 16,6 |
| ala fissa senza pilota | 47 / 20 239 | 16,9 | 21,4 | 28,2 | 0,32 | 1,29 | 4,53 | 24,5 |
| auto (autostrada urbana congestionata) | 154 / 90 175 | 10,6 | 17,1 | 27,8 | 0,36 | 1,44 | 0,29 | 2,59 |
| treno in linea | 111 / 17 551 | 14,6 | 43,5 | 73,9 | 0,10 | 0,59 | 0,11 | 1,13 |

**Confronto con i profili ipotizzati** (`classi.json` di f14; frazione dei tratti il cui massimo supera `v_max` del profilo, Wilson 95 %):

| dato | profilo | v_max profilo | tratti oltre | intervallo | lettura |
|---|---|---|---|---|---|
| rullaggio | `aereo_rullaggio` | 15,4 m/s | 2/19 | [0,03; 0,31] | profilo stretto: p95 12,9 m/s è sotto, il massimo 16,0 sopra; `a_max` 1,0 contro p95 misurato 0,24 (largo) |
| multirotore | `multirotore_lento` | 19,0 m/s | 0/196 | [0; 0,019] | regge su questo mezzo e questi voli (programmati a velocità fissa: non è il limite del mezzo) |
| auto | `auto_strada_urbana` | 13,9 m/s | 114/154 | [0,67; 0,80] | **contesto diverso** (autostrada): serve un profilo «auto in autostrada» |
| treno | `treno_banchina` | 16,7 m/s | 95/111 | [0,78; 0,91] | **contesto diverso** (linea): serve un profilo «treno in linea» |

Per avvicinamento, decollo, elicottero, aviazione generale, ala fissa senza pilota **non c'è un profilo** in `classi.json`: i valori sopra sono la proposta di partenza (sostenuta dai dati, non una scheda).

## 3. Critiche, ciascuna con la sua prova

1. **I dati degli aerei di linea sono di due qualità che non si mescolano.** La cattura dal vivo è grezza ma breve e rada (131 istantanee valide su 171 scritte e 190 chieste; 19 richieste scadute; 25 tracce scartate su 78 aerei). Zenodo è a 1 Hz ma lisciato a spline dalla fonte, e dà \|a\| p95 doppia (2,69 contro 1,27 m/s²): è un artefatto plausibile dell'interpolazione, **non risolto** (lo deciderebbe l'ADS-B grezzo degli stessi voli, che chiede credenziali).
2. **Controllo della derivazione** (condivide con i convertitori i dati e la proiezione, non la velocità della fonte): velocità derivata meno velocità al suolo trasmessa, aerei dal vivo: mediana 0,02 m/s, scarto assoluto mediano 0,43, p95 3,83 m/s su 2822 campioni. Treni contro la velocità della fonte: mediana 0,00, assoluto mediano 0,67, **p95 5,41 m/s** su 17 551 campioni. NGSIM: mediana della fonte 10,64 contro 10,61 derivata.
3. **Il GPS dei treni è sporco**: 51 096 doppioni di orario su 261 721 record e 9836 punti rimossi come salti (oltre 80 m/s dal punto precedente). Resta un massimo derivato di 73,9 m/s contro 56,1 della fonte: il massimo dei treni **non è affidabile**; mediana e p95 concordano con la fonte (p95 43,9).
4. **Il passo dei dati reali è lungo per le occlusioni brevi**: 3-5 s per aerei dal vivo e treni. A 89 m/s un aereo fa circa 300 m fra due campioni: per occlusioni sotto i 10 s la «verità» è un'interpolazione. Auto e droni (0,1-0,24 s) non hanno questo limite.
5. **Sottotipi sotto soglia**: rullaggio 19, avvicinamento grezzo 9, elicottero 4 tratti. I moti a terra etichettati (Zenodo 23548217) chiedono credenziali.
6. **La verità è di bordo, non esterna**: nessun insieme dà una posizione misurata da un secondo strumento indipendente. L'errore del GNSS (metri) è trascurabile a queste scale, non a 3 m.
7. **Quota del campo di Atlanta (313 m) a memoria, non verificata**: sposta solo lo zero di z nelle scene `atl_*`.

## 4. Stati proposti

- «Esistono traiettorie pubbliche reali, senza credenziali, per le quattro classi»: **verificato** sull'insieme scaricato oggi (704 scene).
- «I profili `auto_strada_urbana` e `treno_banchina` coprono i veicoli veloci»: **smentito** dai dati (contesto diverso, 74 % e 86 % dei tratti oltre `v_max`).
- «`multirotore_lento` copre i multirotori»: **sostenuto dai dati** per un solo mezzo; «`aereo_rullaggio`»: **non risolto** (19 tratti, 2 oltre).
- «Esistono rilevazioni multisensore pubbliche piccole per queste classi»: **non verificato** (non cercato a fondo nei tempi).

## 5. Proposte (sigla dati-)

- **dati-1, profili nuovi dai dati.** Aggiungere a `classi.json`: aereo in avvicinamento (v 89-99, p95 133-158 m/s), in decollo, elicottero, ala fissa senza pilota (v 17, virata p95 24 °/s), auto in autostrada, treno in linea, con `v_max` = massimo misurato più un margine dichiarato. Previsione: con i nuovi profili meno del 5 % dei tratti supera `v_max`. La smentisce una seconda giornata di cattura con più del 5 %.
- **dati-2, occlusioni tagliate sui tratti reali.** Lo scenario toglie la visibilità per una durata scelta e confronta la zona prevista con `verita.csv`. Previsione: l'ala fissa senza pilota (virata mediana 4,5 °/s) è il caso che allarga di più la zona per unità di tempo. La smentisce un errore a 5 s minore di quello degli aerei di linea in rapporto alla velocità.
- **dati-3, seconda cattura ADS-B** (30 minuti, due aeroporti, di giorno) per portare rullaggio e avvicinamento grezzi oltre 30 tratti: è `converti.py live` rifatto, costo zero.

## 6. Dopo

Chi fa gli scenari sostituisce il sensore segnaposto `rif` e ricalcola `vis_rif`; chi simula i sensori genera le `rilevazioni_<sensore>.csv` da queste verità. Rifare tutto: `python -I convertitori/converti.py <auto|droni|alfa|treni|trajair|live|zenodo|statistiche> <01-dati>`, poi `verifica.py`.
