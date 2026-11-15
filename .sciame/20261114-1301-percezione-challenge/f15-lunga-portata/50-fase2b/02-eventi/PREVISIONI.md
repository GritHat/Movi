# Previsioni e soglie, scritte prima delle misure (eventi_v2)

`sciame-scene-dinamiche`, scritto alle **2026-11-15T01:55:56+01:00** (`date -Is`), prima di aver scritto e fatto
girare `eventi_v2.py`. Tutto è simulazione (simulatore f15 `10-simulatore`), niente è «validato». Le frequenze sono
per passaggio, con Wilson al 95 %. Le soglie sono quelle della consegna degli scenari (`scenari_eventi.json`,
campo `misure`); dove la consegna non dà un numero di passaggi, la soglia è sul limite di Wilson come scritto qui.

Notato prima di scrivere il codice, guardando gli esemplari della prova vecchia (`10-simulatore/esemplari/E*_alta_0.json`):
i frammenti esistono nella verità **prima** dell'evento, fermi nel punto d'urto, e i sensori li vedono (E1: 1–5
ritorni «fr» a ciclo fra 12 e 15 s). È un difetto del simulatore vecchio. In v2 i frammenti prima dell'evento sono
spostati fuori dalla portata di ogni sensore. Il radar IRIS vede i frammenti dopo l'urto (15 a 16 s, 40 a 17 s
nell'esemplare); il radar di superficie di E2 ne vede 20–29 a scansione da 17 s.

| # | Misura (per passaggio) | Soglia: regge se | Smentita se | Previsione |
|---|---|---|---|---|
| P1 | E1, ritardo dell'evento dal vero (60 passaggi, «alta») | ≥ 0,95 entro 2,0 s, cioè limite inferiore di Wilson ≥ 0,90 con 60/60 o 59/60 | < 57/60 entro 2,0 s | **regge** con la conferma da due sensori (radar + EO); senza camera (solo radar, 1 s di giro) il ritardo è ≥ 2 giri: al limite |
| P2 | E1, quota (frammento, istante) dentro V | ≥ 0,999 | < 0,999 | **regge** ora che t_a è prudente (inizio del contatto o t_b − 2 s − 1 giro) |
| P3 | E1, falso «libero» su un frammento dentro l'impronta (istanti, nucleo + strato v2) | 0 | ≥ 1 | regge |
| P4 | E1, avviso alla persona sul piazzale entro 2,0 s | come P1 | come P1 | uguale a P1 (la persona è dentro l'impronta) |
| P5 | E2, evento dichiarato entro 2,0 s (60 passaggi) | ≥ 57/60 | < 57/60 | **regge** con l'innesco nuovo «fiammata sulla traccia» (abbagliamento colocato con una traccia confermata) |
| P6 | E2, avviso a mezzo1 mentre la sua distanza dall'impronta è ≥ 140 m | ≥ 57/60 | < 57/60 | **regge** |
| P7 | E2, frammenti dentro V | ≥ 0,999 | < 0,999 | regge, con riserva: dv 60 nella verità contro 100 nell'inviluppo |
| P8 | E4, falsi eventi (60 passaggi, «alta») | 0/60 | ≥ 1/60 | **regge** con il grappolo (≥ 2 ritorni nuovi nello stesso giro) |
| P9 | E5, falsi eventi a 5 m (300 passaggi) | 0/300 (Wilson sup. ≤ 0,0126) | ≥ 1/300 | **regge** |
| P10 | E2, camere dichiarate non affidabili entro 3 cicli | 60/60 | < 60/60 | regge (stessa regola di prima) |

Limiti dichiarati prima: lo strato eventi v2 è scritto da me e misurato dal mio stesso programma sullo stesso
simulatore (non indipendente: condivide simulatore, scenari, autore). La nube (EV-B) è presa dalla verità dello
scenario e non stimata dallo sfondo: è ottimista. Nessun sensore di E1–E2 ha una griglia oscurata dalla nube (sono
radar): EV-B è realizzata ma non esercitata da queste misure.
