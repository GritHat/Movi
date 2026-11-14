# PREVISIONI — sciame-sviluppatore, f16-prototipo/10-corto-raggio

Scritte alle 2026-11-15T00:15:23+01:00, PRIMA di scrivere il nucleo corto e di lanciare qualsiasi misura. Tutto è simulazione.

**Campione.** Passaggi nuovi generati col simulatore riusato (`riuso/11-simulatore`), semi mai usati: indici di
passaggio k = 100…129 (il catalogo usa k < 30; il seme del percorso e quello del rumore dipendono dal nome), 30 passaggi
per ciascun caso: a12 (attraversa a 1,2 m/s), a05 (0,5 m/s), b (si ferma 3 s dietro il pannello), c (torna indietro),
d (svolta dietro il pannello, si allontana e resta). Bracci: «base» (solo correzioni f12), «zona» (+ predittore_zona),
«zona+libero» (+ libero_dal_fotogramma). Il braccio dichiarato principale è «zona+libero».
«Nascosta» = `visibile: false` nella verità del simulatore. Frequenze con Wilson al 95 %.

| # | Misura | Previsione | Smentita se |
|---|---|---|---|
| sv-P1 | cicli a persona nascosta, DOPO l'evento d'ingresso in ombra, senza regione né avviso | 0 | ≥ 1 ciclo |
| sv-P2 | fotogrammi a persona nascosta senza alcun avviso (ritardo dell'ingresso compreso) | ≤ 10 % | stima puntuale > 10 % |
| sv-P3 | celle dichiarate «libero» il cui centro sta nell'ombra vera del pannello (codici 1 e 3), celle interne (le 8 vicine pure in ombra) | 0 | ≥ 1 cella; quelle di bordo si contano a parte |
| sv-P4 | persona vera dentro ciò che è mostrato (regione, o tutta l'ombra se «previsto ampio») a 1, 2, 3 s da quando è nascosta | ≥ 90 % a ogni orizzonte | limite superiore di Wilson < 90 % |
| sv-P4b | persona vera dentro la regione STRETTA (non ampia), quando c'è, a 1, 2, 3 s | ≥ 90 % (livello dichiarato) | limite superiore di Wilson < 90 % |
| sv-P5 | al ritorno (a12, a05, b): la traccia riprende l'identità come «presunta» (evento riaggancio) | ≥ 50 % dei passaggi; mai «certa» nel fotogramma del ritorno | < 50 % puntuale, o un solo «certa» al riaggancio |
| sv-P6 | tempo per ciclo del nucleo (catena + regole + registro, senza lettura/scrittura) | mediana ≤ 33 ms, p95 ≤ 66,7 ms (15 Hz) | p95 > 66,7 ms |
| sv-P7 | avvisi tolti senza guardare (controllo fra righe: sparisce senza evento di celle viste libere) | 0 | ≥ 1 |
| sv-P8 | cambiando il file delle etichette, avvisi, settori e celle restano identici riga per riga | 0 differenze | ≥ 1 |
| sv-P9 | pavimento vuoto: tracce confermate, avvisi | 0 e 0 | ≥ 1 |
| sv-P10 | sensore coperto (1,0–2,2 s): fotogrammi coperti dichiarati «affidabilità persa» dopo il ritardo di 0,2 s; nessuna cella «libero» in quei fotogrammi | tutti dopo 0,2 s; 0 celle | un fotogramma coperto oltre 0,27 s senza dichiarazione, o ≥ 1 cella |

Nota onesta scritta prima: sv-P5 è la più a rischio (l'architetto ha visto 0 riagganci su `pannello_a12__s00`, critica 4);
sv-P4b dipende da una libreria di percorsi rigenerata in Python (non quella del banco in C): se cade, lo si dice.
