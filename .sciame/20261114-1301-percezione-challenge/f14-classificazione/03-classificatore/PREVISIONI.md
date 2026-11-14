# Previsioni di `sciame-ml` — f14, 03-classificatore

Scritte alle 2026-11-14T18:34:17+01:00 (`date -Is`), prima di aprire qualunque pagina in rete e prima di eseguire lo script. Lette prima: contratto f14, addendum 10, SOLUZIONE_V3 finale (§0, 1.6, 1.7, 1.10, §2, §3). Non cieche rispetto a quei testi né alla mia memoria delle fonti.

| # | Previsione | Misura | Soglia di smentita |
|---|---|---|---|
| ml-P1 | L'elenco delle 80 classi COCO contiene person, bicycle, car, motorcycle, airplane, bus, train, truck, boat; NON contiene forklift, tram, drone/UAV, scooter, wheelchair | lettura dell'elenco in una pagina aperta oggi | una delle nove manca, o una delle cinque c'è |
| ml-P2 | I pesi/codice della famiglia YOLO di Ultralytics sono AGPL-3.0; RF-DETR (codice e modelli piccoli) è Apache-2.0 | pagina del deposito aperta oggi | licenza diversa |
| ml-P3 | Esiste almeno un insieme pubblico con la classe «carrello elevatore» in magazzino (atteso: LOCO); non trovo in 2 ricerche un insieme pubblico affermato per i mezzi di piazzale aeroportuale | pagine aperte oggi | nessun insieme col carrello; oppure un insieme di piazzale affermato trovato subito |
| ml-P4 | Esistono fonti primarie per: taratura (Guo et al. 2017, arXiv 1706.04599), fuori distribuzione (Hendrycks e Gimpel, arXiv 1610.02136), scomposizione degli errori dei rilevatori (TIDE, arXiv 2008.08115), classificazione da cinematica (Ristic, Gordon, Bessell 2004) | pagine aperte oggi | una non si trova o dice altro |
| ml-P5 | Script `oracolo_degradato.py` (seme fisso, 10 000 tracce per braccio): con la regola «ingenua» (v_usata = v della classe etichettata) la quota di tracce con fascia più stretta della linea di base senza etichetta è > 0 con ogni matrice non identità; con la regola «solo allarga» (v_usata = max(v_base, v delle classi con probabilità ≥ ε)) è esattamente 0 con ogni matrice e ogni ritardo | conteggio | «solo allarga» > 0 in un braccio qualunque; oppure «ingenua» = 0 con una matrice con errori veloce→lento |
| ml-P6 | Con «solo allarga» la quota di tracce di classe veloce sotto-coperte rispetto alla loro velocità VERA resta > 0 quando l'etichetta sbaglia verso una classe lenta e v_base < v vera: la regola protegge la linea di base, non la classe | conteggio nello stesso script | quota = 0 |

Esiti: in fondo a CLASSIFICATORE.md.

## Esiti (scritti alle 2026-11-14T18:39:30+01:00, dopo le prove)

ml-P1 regge. ml-P2 regge per YOLO; smentita in parte per RF-DETR (Atto, Femto, Pico, XL, 2XL sotto PML 1.0). ml-P3: prima metà regge (LOCO), seconda smentita (Apron Dataset trovato alla prima ricerca). ml-P4 regge per l'esistenza delle fonti; il contenuto di Ristic et al. non è letto. ml-P5: «solo allarga = 0» regge (0 in 24 bracci); «ingenua > 0 con ogni matrice con errori» smentita nei 9 bracci con base 1,4 m/s. ml-P6 regge (160–1 004 su 10 000 nei 18 bracci con errori). Notato DOPO, non previsto: con base 4,0 m/s la regola ingenua restringe anche con etichette tutte giuste (5 928–5 984 su 10 000).
