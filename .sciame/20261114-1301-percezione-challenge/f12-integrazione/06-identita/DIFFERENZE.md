# DIFFERENZE — la copia `catena/` rispetto a `f10-dati/10-catena` (f12, 06-identita)

`catena_originale/` è la copia intatta di f10 (senza `uscite/`); `catena/` è quella corretta. **Ogni riga cambiata è
in `DIFFERENZE.diff`** (`diff -u -r catena_originale catena`: 7 file, 105 righe aggiunte o tolte); `rifai.sh`
ricostruisce `catena/` dall'originale più quel diff e controlla che coincida. La catena di f10 non è stata toccata.
Tutte le correzioni stanno dietro interruttori di `Parametri`, **spenti di norma**: a interruttori spenti la copia dà
le stesse cifre di f10 (0 su 90; 28 tracce sul pavimento vuoto; scatola 10 su 10: colonna «prima»).

| Interruttore (`parametri.py`) | Difetto | File e punto | Che cosa cambia |
|---|---|---|---|
| `soglia_proporzionale`, `alt_rif_cella_m` = 0,05, `area_rif_gruppo_m2` = 0,004 | F-401, F-412 (come proposto da validazione-6 e avversario-2) | `mappa.py` (`Mappa.__init__`, `aggiorna`), `geometria.py` (`fx`, `fy`, `ia_campo`), `gruppi.py` | «occupato» se i punti ≥ max(3, ⌈fx·fy·Δaz·h_rif/r⌉); un gruppo vale se ha ≥ fx·fy·A_rif/r² punti |
| `gruppi_per_picco`, `frazione_picco` = 0,30 | F-401, F-403 (**tracciamento-1**, nuova, scelta dopo i dati) | `gruppi.py` (`_forti`, `trova_gruppi`) | la mappa resta quella di f10; fanno gruppo solo le celle con punti ≥ max(ρ·picco della componente, soglia sui pixel attesi); stessa soglia di gruppo |
| `tagliato_su_componente` | **tracciamento-2** (nuova, provata e **smentita**: 0 su 10 a 2,1 m) | `gruppi.py` (`trova_gruppi`) | la marca «tagliato» scavalca fino a 2 celle deboli accanto al gruppo; spenta nella configurazione finale |
| `riaggancio_rifiuta_tagliati`, `riaggancio_rifiuta_occlusore` | F-402 (validazione-7) | `presenza.py` (`riaggancio_ammesso`), `gruppi.py` (`al_bordo`) | niente riaggancio a un gruppo tagliato da un'ombra, al bordo del campo (azimut o portata), o che dà il primo ritorno su un azimut del cuneo |
| `riparti_al_riaggancio` | F-408 (sviluppatore-1) | `inseguimento.py` (`_riaggancia`, `_misura`) | al riaggancio il filtro riparte dalla misura con R + (larghezza/2)²·I; le misure tagliate che seguono aggiornano con R gonfiato fino alla prima misura piena |
| `strato_resta` | F-409 (avversario-3) | `inseguimento.py` (`orfani`), `presenza.py` (`orfano`), `catena.py` | al riaggancio lo strato non finisce: resta nell'avviso e si rilascia cella per cella (vista libera 3 volte di fila); l'evento di riaggancio porta `identita: presunta` |

Aggiunte di servizio: `CicloMappa.ia_campo`, `.fxfy`, `.soglia_attesi`; `Gruppo.al_bordo`; `Traccia.appena_ripartito`.
Le 25 prove di f10 sulla copia: 23 passano, 2 falliscono **anche sull'originale copiato** perché cercano
`../03-infrastruttura` (P1, P14): non dipendono dalle correzioni (`risultati/prove_copia.txt`).

File miei: `prova.py` (banco: otto configurazioni per sequenza; usa `misura_passaggi.py` e `misura_ostacoli.py` di
f10 senza modificarli), `estraneo.py`, `p8_f408.py`, `riassumi.py`, `cifre.py`, `diagnosi.py`, `diag_celle.py`, `diag_z21.py`, `rifai.sh`, `PREVISIONI.md`.
Una prima stesura delle correzioni stava in uno script `applica_correzioni.py`, poi tolto: fa fede il diff.
