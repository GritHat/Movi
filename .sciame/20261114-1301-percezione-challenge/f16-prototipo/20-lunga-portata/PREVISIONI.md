# Previsioni del modo a lunga portata del prototipo (f16/20-lunga-portata)

Scritte da `sciame-sviluppatore` alle 2026-11-15T01:23:37+01:00, PRIMA di ogni prova. Tutto è simulazione.

| # | Misura | Soglia (regge se) | Smentita se |
|---|---|---|---|
| L1 | Cicli del registro del prototipo contro `esemplari/<scen>_alta_0_<chiamante>.json` (A1–A4, S1, S2, due chiamanti) e `E1…E5_alta_0.json`: stesse parole, posizioni, raggi, zone, sensori persi | 17 file su 17 identici campo per campo (tolleranza 0) | un campo diverso in un ciclo |
| L2 | Principi sul registro (`movi convalida`): avviso tolto senza guardare; «libero» con affidabilità persa | 0 errori su ogni scena del modo prudente | ≥ 1 errore in una scena prudente |
| L3 | Le etichette a mano non cambiano l'avviso: raggio della possibile presenza con etichette e senza | identico in ogni ciclo | un raggio diverso |
| L4 | Una scena (A1, alta) da `esegui` a filmato | < 120 s | ≥ 120 s |
| L5 | Nel modo interfaccia si vedono cicli con l'oggetto nascosto e nessuna regione (P2 di PROVE) e la convalida li segnala come «avviso tolto senza guardare» in almeno uno di A1, S1 | ≥ 1 segnalazione | 0 segnalazioni ovunque |

Ipotesi: il passaggio 0 nella configurazione alta è deterministico (semi SeedSequence(20261115, …)); la vista in pianta
calcolata dentro `uscite()` non cambia lo stato del nucleo (le cache di `pd_cumulata` sono funzioni pure).
