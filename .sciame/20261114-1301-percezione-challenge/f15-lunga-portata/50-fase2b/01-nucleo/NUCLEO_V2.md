# Nucleo a lunga portata v2: correzioni 1–5 (fase 2b, 01-nucleo)

`sciame-tracciamento`, 2026-11-15, dalle 01:53 alle 02:10 (`date -Is`). Previsioni scritte prima, in `PREVISIONI.md`:
01:55:46 per le prove unitarie, 02:02:09 e 02:05 per i piloti. **Tutto è conto o simulazione dalle schede, niente è
«validato».** Solo osservazione e avviso. Interprete: `f10-dati/ambiente/venv/bin/python -I -B`.

**File** (tutti in questa cartella; `movi_lp.py` e `regole_lunga_portata.json` di 04-moto restano dove sono, intatti):
`movi_lp_v2.py` (nato da `cp -n` di movi_lp.py, poi corretto), `regole_lunga_portata_v2.json` (generato dal JSON v1),
`prove_v2.py` → `prove_v2_esito.json` (0,1 s) e, con `--compat`, `prove_v2_compat_esito.json` (7,9 s),
`pilota_A1.py` → `pilota_A1{,_v1,_cert}_esito.json`, `confronta_un_passaggio.py`, `conta_liberi.py`, `PREVISIONI.md`.

## 0. In testa

- **Cambi di stato, per il modello del nucleo.** «L'avviso contiene il mezzo» nei casi X1 e X2: da **smentito** a
  **regge sul caso costruito**. «Il libero non contiene oggetti di classe ammessa» contro X4, X5, la cella vicina e il
  Doppler: da **smentito** a **regge sui casi costruiti**, e nel pilota A1 il «libero» sull'oggetto passa da 7/40
  passaggi [0,087; 0,32] a **0/40 [0; 0,088]**. Validazione-1: ora è **nel nucleo**, non solo nel chiamante.
- **Regole violate:** nessuna, che io sappia. Non ho cancellato né sovrascritto file di altri, non ho usato git né la
  rete, e ho tenuto al più 8 processi (i piloti, circa 100 s ciascuno). Ho corretto con `sed -i` un mio file di prova.
- **Il prototipo non usa ancora v2.** `prove_lp` e `prototipo/riuso` importano il nucleo da `04-moto` attraverso
  `movi_lp_import.py`. Passare a v2 è una riga in quel ponte, oppure `sys.modules["movi_lp_import"]` come fa
  `prove_v2.py --compat`. Quella riga non l'ho cambiata, perché la cartella non è mia.

## 1. Le correzioni, la regola e il punto del codice

1. **Inviluppo per scenario.** È il peggio fra le classi ammesse dallo scenario, nel JSON v2.
   - `aereo_linea_avvicinamento.v_max` passa da 90 a 210 m/s. Il nome resta, perché lo usa `prove_lp`.
   - Classe nuova `multirotore_veloce`: 45 m/s, 25 m/s². È un'**ipotesi** dell'attacco X1, senza fonte.
   - Scenario nuovo **`sito_droni_rullaggio`** (il caso centrale): multirotori, ala fissa e aerei in rullaggio. Gli
     aerei in volo sono esclusi e dichiarati.
   - `aeroporto_e_droni` tiene gli aerei in volo come **limite dichiarato**.
   - `tempestivita()` confronta per ogni ricevente la distanza d'avviso con la portata del «libero» (n_eff). Il
     risultato entra in `Inseguitore.dichiarazione` e in ogni uscita come `avviso_non_tempestivo_per`.
2. **Passate correlate.** La Pd cumulata è `1 - (1-Pd)^n_eff`, con `n_eff = 1 + (n-1)(1-ρ)`. ρ è della classe, e il
   predefinito è 1, quindi n_eff = 1.
   - La regola è prudente per qualunque correlazione: E[(1-Pd)^n] ≤ E[1-Pd].
   - Fra sensori dello **stesso tipo** `stato_fuso` prende il migliore, non il prodotto, perché l'aspetto può essere
     correlato (**ipotesi**). Il prodotto vale solo fra tipi diversi.
   - `Sensore.portata(..., rho=)` dà 877 m per 0,01 m² sul radar segnaposto, contro i 2360 m di v1.
3. **Mappa come ingresso di sicurezza.** Una cella illuminata conta come guardata solo se la linea di vista è
   certificata, in uno di due modi:
   - (a) la mappa è dichiarata completa: `mappa_certificata` vale True, oppure è una maschera di rilievo;
   - (b) sul raggio era atteso un ritorno dello sfondo oltre la cella (`sfondo_atteso[az, el]`), ed è stato misurato
     alla distanza attesa entro 2 m (`passata(..., sfondo_misurato=)`).

   I casi dello sfondo:
   - se lo sfondo atteso **manca**, il raggio non è certificato;
   - se lo sfondo è **più vicino** dell'atteso, c'è un ostacolo non in mappa: le celle oltre vanno «in ombra» e il
     caso si annota in `ostacoli_nuovi`.

   Il predefinito è **non certificato** (`MAPPA_CERTIFICATA_PREDEFINITA = False`), quindi senza certificazione non
   c'è nessun «libero». Il cielo non ha sfondo: lì vale solo (a).
4. **Classi.** `dichiara_punto()` dice «libero per ⟨classi ammesse⟩», e sempre «zona non verificata per ⟨classe⟩» per
   le `classi_escluse` dello scenario:
   - `strada`: pedone, due ruote, multirotore, C0;
   - `aeroporto` e `sito`: C0;
   - `sito`: anche gli aerei in volo.
5. **Validazione-1 e 2 nel nucleo.**
   - **Validazione-1.** `mancato()` conta l'evidenza d'assenza di una traccia confermata solo se
     `avviso_spegnibile()` è vero. Ora quella funzione è **esatta sulle celle**, non più a 32 punti a caso: serve una
     griglia affidabile che contenga tutta la sfera, e tutte le celle che la toccano devono essere «libere» dopo la
     perdita (centro entro raggio + mezza diagonale).
   - **Validazione-2.** Ogni ritorno toglie il «libero» alle celle entro 3σ del sensore, più una cella (`t_alone`).
     Un sensore con `v_rad_min` (filtro Doppler) non dà mai «libero». Il suo silenzio non conta se
     |v_r| − 3σ_v ≤ v_rad_min.
   - **L'interfaccia resta la stessa.** Ci sono solo argomenti nuovi, con nome e predefinito. `n_punti` e `rng` di
     `avviso_spegnibile` restano ma sono ignorati.

## 2. Prove ed esiti

Ogni prova è un caso costruito, quindi dice se il difetto esiste o no, non con che frequenza. Il tempo totale è
0,1 s (P8 regge).

| Prova (prev.) | v1 | v2 | Esito |
|---|---|---|---|
| X1 scatto 20–25 m/s² fino a 45 m/s; X2 205 m/s (P1) | fuori a τ = 3, 5, 8 s | dentro a ogni τ, in 3 scenari | regge |
| X3 operatore di sito (P2) | «sì», 1490 m < 2360 m | aeroporto 3410 m > 877 m: **dichiarato non tempestivo**; sito 770 m ≤ 877 m: tempestivo | regge |
| X4 passate correlate (P3) | «libero» a 2250 m | non osservato a 2250 m, «libero» a 700 m | regge, **ma con punti cambiati dopo** (sotto) |
| X5 edificio ignoto (P4) | «libero» | non certificato: non osservato; sfondo a 400 m invece di 1500: in ombra e annotato; sfondo mancante: non osservato; sfondo come atteso: «libero» | regge |
| X6 classi escluse (P5) | solo «libero» | «libero per auto_…», «zona non verificata per pedone…» (9360 celle libere non verificate per il pedone); aeroporto: C0 | regge |
| Validazione-1 (P6) | chiusa con mezzo insieme guardato | non chiusa; chiusa quando è guardato tutto | regge |
| Validazione-2 (P7) | cella dell'oggetto «libera», con il ritorno a 2 celle; Doppler: 3960 celle libere | non osservato; Doppler: 0 libere, traccia non chiusa | regge |
| Compatibilità (P9) | — | un passaggio A1 di `prove_lp` gira con v2 (7,9 s) | regge |

**P3 come era scritta è in parte smentita.** Il «libero» a 800 m non c'è: la cella 800–900 m ha la vicina a 950 m,
oltre gli 877 m, e conta il minimo sulle 8 vicine. Anche v1 a 2300 m non dava «libero», per la vicina a 2400 m. Ho
spostato i punti a 700 m e a 2250 m **dopo** aver visto l'esito. Il difetto di v1 resta mostrato a 2250 m.

**Piloti nel simulatore.** A1 «alta», indici 0–39 appaiati, chiamata «interfaccia» (quella che rompeva), conteggi
per passaggio; previsioni P10–P14.

| Nucleo e mappa | Passaggi con «libero» sull'oggetto | Con un ciclo senza regione / fuori avviso | Tempestivi | Falsi confermati (mediana) |
|---|---|---|---|---|
| v1 | **7/40** [0,087; 0,32] (231 istanti su 4560) | 0/40 / 0/40 | 40/40 | 3 |
| v2, mappa non certificata | 0/40, **per costruzione** (nessuna cella libera) | 0/40 / 0/40 | 40/40 | 8 |
| v2, mappa dichiarata completa | **0/40 [0; 0,088]** (0/4560) | 0/40 / 0/40 | 40/40 [0,91; 1] | 8 |

Con la mappa completa le celle libere ci sono: per esempio 46 914 su 63 000 fino a 1044 m (`conta_liberi.py`). La
prova quindi non è vuota.

**P10 e P14 non sono decisive.** Solo 5 passaggi su 40 hanno una fase nascosta, e anche v1 qui fa 0/40: la smentita
564/2400 di v1 (9/200 in A1 alta) non si vede su questi indici.

## 3. Stati proposti

- **Sostenuto su casi costruiti, in simulazione:** X1, X2 e X3 dichiarati; X4, X5 e X6 chiusi o dichiarati;
  validazione-1 e 2 nel nucleo.
- **Sostenuto dai dati (pilota, n = 40):** «libero» sull'oggetto da 7/40 a 0/40 in A1 alta.
- **Non risolto:**
  - l'effetto su A2, A4, S1, S2 ed E1–E5;
  - i passaggi senza regione con l'interfaccia (servono n = 200 e passaggi con fase nascosta);
  - il costo in falsi avvisi tenuti accesi, che è cresciuto: mediana da 3 a 8, un solo indicatore e non ricontato.

## 4. Limiti e costi dichiarati

- **L'unione di più sensori non spegne un avviso**: serve una griglia che copra da sola tutto l'insieme. È prudente:
  gli avvisi restano accesi più a lungo.
- Con n_eff = 1 il «libero» del multirotore arriva a circa 0,88 km sul radar segnaposto, e a circa 1 km sul radar
  IRIS simulato.
- I radar 4D con Doppler non danno più «libero». In S1 resta solo il LiDAR: da misurare.
- Il predefinito «mappa non certificata» cambia il comportamento dei chiamanti che non dichiarano la mappa: nessun
  «libero». È voluto, e va detto.
- `mancato()` usa la sfera anche sul binario. È prudente.
- Sono ipotesi: ρ = 1, a_max = 25 m/s², 210 m/s, l'alone a 3σ, la tolleranza di 2 m sullo sfondo, «migliore fra
  sensori dello stesso tipo».
- Le correzioni 6–8 non sono toccate: disturbo strutturato, occlusioni vicino agli ostacoli, rivisita IRIS.

## 5. Dopo

1. Far puntare a v2 il ponte `movi_lp_import`, con decisione del coordinatore.
2. Rifare A1 e A2 «prudente» e «interfaccia» con n = 200, record per passaggio, nello scenario `sito_droni_rullaggio`
   e con la mappa dichiarata.
   - **Previsione:** 0 passaggi con «libero» sull'oggetto, 0 fuori avviso, A1 tempestivo ≥ 190/200.
   - **Smentita:** un solo passaggio fuori avviso, oppure A1 < 190/200.
3. Misurare il costo in falsi avvisi.
4. Rifare E1 ed E2, che questo lavoro non tocca.
