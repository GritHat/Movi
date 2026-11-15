# Previsioni e soglie della riprova (fase 2b, 10-riprova)

`sciame-sviluppatore`, scritte alle **2026-11-15T02:18:09+01:00** (`date -Is`), prima di lanciare qualunque passaggio. Tutto è
simulazione dalle schede: niente è «validato». Frequenze per passaggio (un record per passaggio), Wilson al 95 %.
Chiamata **prudente** di prove_lp, nucleo **v2** (copia in prototipo/riuso/lunga_portata_v2), regole v2, mappa
**dichiarata completa** (il simulatore conosce tutti gli ostacoli: è un'ipotesi, dichiarata), senza regioni tarate
(come i piloti di 01-nucleo). Indici 0–199 appaiati con le prove f15. Famiglia: A1, A2 → `sito_droni_rullaggio`
(inviluppo dei droni e dei mezzi di terra); A3 → `aeroporto_e_droni` (aerei in volo a 210 m/s: limite dichiarato).

Soglie dalla «prossima prova» del verdetto (VERDETTO_FASE2 § 9):

| # | Misura | Regge se | Smentita se | Previsione |
|---|---|---|---|---|
| R1 | A1 alta, passaggi tempestivi (d_conf ≥ 806 m) | ≥ 190/200 | < 190/200 | regge (200/200 come v1) |
| R2 | A1 min, passaggi tempestivi | ≥ 190/200 | < 190/200 | regge |
| R3 | A1 min e alta, A2 alta: passaggi con almeno un ciclo nascosto **fuori dall'avviso** | 0 | ≥ 1 | 0 |
| R4 | stessi: passaggi con un ciclo nascosto senza regione né avviso | 0 | ≥ 1 | 0 |
| R5 | A1 alta (pannello): passaggi con un istante «libero» sull'oggetto | 0 | ≥ 1 | 0 (v1 prudente: 119/4902 istanti) |
| R6 | A2 alta, tempestivi (147 m) | ≥ 190/200 | < 190/200 | regge |
| R7 | A3 alta: conferme del drone sotto la copertura dal **solo** radar d'aeroporto, e celle «libere» per il drone nel suo volume | 0 conferme; uscita «zona non verificata per» | ≥ 1 «libero» sull'oggetto | regge (per costruzione: n_eff=1 e Pd del radar d'aeroporto) |
| R8 | A3: tempestività | non misurata (lo scenario parte a 2,5 km, ne servono 3,9: per costruzione) | — | — |
| R9 | costo: falsi confermati per passaggio (mediana) | solo misurato | — | cresce rispetto a v1 (pilota: 3 → 8) |

Eventi (dopo, «come nel file degli eventi», EVENTI_V2 § 2, nucleo v2 con EVENTI_NUCLEO=v2): soglie di EVENTI_V2:
E1 entro 2,0 s ≥ 57/60 (previsione: **smentita** come in v1 strato, ~51/60, il nucleo non cambia l'innesco);
E2 evento entro 2,0 s ≥ 57/60 (previsione regge, con l'ipotesi ottimista della fiammata); E2 camere non affidabili
entro 3 cicli 60/60; E4 falsi eventi 0 (previsione regge). E3 non è in eventi_v2: nei registri video gira con
eventi_lp e nucleo v2. Se il tempo non basta, n più piccolo, dichiarato **prima** del lancio qui sotto.

## Aggiunta (scritta alle 2026-11-15T02:24:32+01:00, dopo aver visto A1 alta e A1 min, prima della diagnosi)

**Notato dopo:** R5 smentita (A1 alta: 192/200 passaggi con un istante «libero» sull'oggetto, 1305/22 800 istanti) e
R3 smentita (A1 min: 12/200 passaggi con un ciclo fuori avviso). Ipotesi di causa, da decidere con una diagnosi
appaiata sugli stessi indici 0–199 di A1 (min e alta) con la famiglia **aeroporto_e_droni** (quella dei piloti di
01-nucleo, v_max 210) al posto di sito_droni_rullaggio. D1: se la causa è la finestra W_c più lunga e l'inviluppo più
stretto della famiglia «sito», con aeroporto_e_droni i passaggi con «libero» sull'oggetto scendono a ≤ 2/200 e i fuori
avviso a 0/200. Smentita di D1: ≥ 10/200 «libero» o ≥ 1 fuori avviso anche con aeroporto_e_droni.
