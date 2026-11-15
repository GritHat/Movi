# Previsioni e soglie (sciame-validazione, f15/10-simulatore e 11-prove)

Scritte il **2026-11-15T00:20:40+01:00** (`date -Is`), PRIMA di scrivere il simulatore e di eseguire qualunque prova.
Tutto è simulazione dalle schede: nessuna prova su un sensore fisico. Esiti possibili: regge, smentita, non risolta.
Le soglie valgono per scenario e configurazione («min» = sensore unico o minimo; «alta» = multisensore).
Intervalli: Wilson al 95 % sulle frequenze.

## Simulatore (verifica contro il suo modello)
- **V1 Pd.** Per ogni sensore a portata, Pd empirica per fascia di distanza (≥ 2000 prove per fascia) dentro
  l'intervallo di Wilson al 95 % del valore di modello in almeno il 90 % delle fasce. Smentita se meno.
- **V2 rumore.** Deviazione standard empirica in distanza e angolo entro ±10 % della sigma dichiarata (n ≥ 2000).
- **V3 falsi allarmi.** Numero di falsi ritorni per passata: media empirica dentro l'intervallo di Poisson al 95 %
  della media di modello.
- **V4 geometria.** Linea di vista: 0 rilevamenti generati per punti dietro un ostacolo più alto della retta, 0 oltre
  l'orizzonte radar, 0 sotto la quota minima del radar che ne ha una, 0 fuori campo.
- **V5 cooperativi.** Assente: 0 messaggi; intermittente: quota di messaggi pari alla quota di tempo acceso ±5 punti.
- **V6 semi.** Tutti i passaggi hanno semi distinti (SeedSequence con chiave scenario, configurazione, indice), e
  nessuna coppia di passaggi produce la stessa prima estrazione.

## Prove del nucleo (movi_lp.py, non modificato)
- **P1 tempestività.** Config. alta: distanza di traccia confermata ≥ d_richiesta in ≥ 90 % dei passaggi in A1, A2,
  A4, S1, S2. A3 (drone a 2,5 km, d_richiesta 3932 m): 0 % per costruzione dello scenario (parte già dentro).
  Config. min: prevedo < 90 % almeno in A3 (radar d'aeroporto senza copertura sotto 200 m).
- **P2 continuità.** Cicli con oggetto nascosto e traccia confermata prima dell'ombra, senza «possibile presenza»
  in uscita: 0 in tutti gli scenari e configurazioni.
- **P3 precisione.** Copertura della zona dichiarata a 2, 5, 10, 20 s dall'ultima osservazione: comportamento
  nominale ≥ 0,90 (limite inferiore di Wilson ≥ 0,85) dove una zona è dichiarata. Prevedo che cada (< 0,90) per
  «si ferma», «torna indietro» o «vira» ad almeno un orizzonte ≥ 5 s in almeno uno scenario.
- **P4 sicurezza, avviso.** Istanti con oggetto nascosto fuori dall'insieme di possibile presenza: 0.
- **P5 sicurezza, libero.** Istanti in cui la cella dell'oggetto vero è «libera» (stato_fuso): 0 per ogni oggetto con
  sezione radar ≥ quella della classe più piccola ammessa. Prevedo > 0 per la variante «drone C0» (1,6·10⁻⁴ m²,
  sotto lo 0,01 m² della classe): è il limite noto della regola, non una sua violazione.
- **P6 falsi avvisi.** Tracce confermate senza oggetto vero: ≤ 1 per ora simulata (limite superiore al 95 %) nella
  config. con radar di sorveglianza.
- **P7 identità.** Scambi d'identità fra due oggetti (A2, E5): passaggi con scambio ≤ 5 % (limite superiore di Wilson).
- **P8 perdita di un sensore.** Affidabilità persa dichiarata entro 3 periodi del sensore nel 100 % dei casi.
- **P9 costo.** Mediana del costo per ciclo del nucleo < 50 ms in Python su questa macchina.
- **P10 rifai.sh** completo in < 15 minuti con al più 8 processi.

## Eventi E1–E5 (misure di scenari_eventi.json)
- **E-a** E1: evento dichiarato entro 2,0 s dal vero in ≥ 95 % dei passaggi; frammenti dentro il volume V ≥ 0,999
  dei campioni (frammento, istante); celle «libere» dentro l'impronta prima dell'ispezione: 0.
- **E-b** E2: affidabilità persa delle camere entro 3 cicli; celle libere dentro impronta e pista a valle: 0; avviso
  al mezzo prima di 140 m dall'impronta nel 100 %.
- **E-c** E3: portata utile dichiarata uguale al conto entro 5 %; celle libere oltre la portata utile: 0; «avviso non
  tempestivo» dichiarato al primo ciclo quando R_utile < d_avv; tracce perse senza avviso: 0.
- **E-d** E4: tracce perse senza avviso dentro la nube: 0; eventi dichiarati: 0.
- **E-e** E5: falsi eventi 0 su 1000 a 5 m di separazione (limite superiore 0,4 %); prevedo che l'innesco scatti a
  separazioni ≤ 1 m (non risolto finché non misurato).

## Annotate dopo (separate da quanto sopra)
(vedi PROVE_LUNGA_PORTATA.md, § «notato dopo»)
