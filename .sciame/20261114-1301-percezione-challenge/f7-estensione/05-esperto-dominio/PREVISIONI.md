# Previsioni — sciame-esperto-dominio, f7, corsia A

Scritte alle 2026-11-14T15:06:07+01:00 (`date -Is`), **prima** di ogni ricerca in rete, di ogni calcolo e di ogni misura di questa consegna. A quell'ora avevo letto solo: la traccia, il contratto dell'estensione, `promptMare.txt`, gli addendum, `SOLUZIONE_V2.md` e il mio `QUADRO_DOMINIO.md` di f6. Le cifre qui sotto vengono dalla memoria o da conti a mente: sono previsioni, non dati.

## P1 — Mappe volumetriche: licenze e trattamento dello «sconosciuto» (ricerca in rete)
- OctoMap: octree, licenza BSD; il nodo assente è «sconosciuto», distinto da «libero».
- Voxblox: blocchi di voxel su tabella hash, TSDF, licenza BSD; il voxel non allocato (o con peso zero) è «sconosciuto».
- UFOMap: octree con i tre stati espliciti (sconosciuto, libero, occupato); licenza BSD.
- OpenVDB: albero a fattori di ramificazione fissi; licenza MPL 2.0 (dubbio: passaggio ad Apache 2.0 con le versioni recenti).
- Bonxai: struttura alla VDB, solo intestazioni, licenza MPL 2.0.
- nvblox: GPU (CUDA), licenza Apache 2.0: fuori dai vincoli (niente GPU).
- **Smentita:** una licenza diversa da quella scritta; oppure una di queste librerie che tratta il non allocato come «libero» in modo predefinito.

## P2 — Sicurezza industriale (ricerca in rete)
- La sorveglianza di velocità e separazione (ISO/TS 15066, ora in ISO 10218-2:2025) ragiona su una distanza minima di protezione, non su voxel probabilistici.
- Almeno un sistema 3D di sicurezza certificato documenta che i volumi **occlusi o non visti si trattano come occupati** (ricordo: Veo Robotics FreeMove).
- **Smentita:** nessuna fonte apribile lo dice; oppure un sistema certificato tratta il non visto come libero.

## P3 — Nebbia, fumo, polvere su stereo attivo (ricerca in rete)
- Mi aspetto fonti che documentano **due** effetti: perdita di misure valide (buchi) **e** ritorni falsi più vicini del vero (retrodiffusione del proiettore, calo di contrasto). Quindi un azzeramento casuale delle misure modella solo il primo.
- **Smentita:** le fonti dicono che l'unico effetto è la perdita di misure, senza ritorni falsi né distorsione della profondità.
- **Non risolta** se non trovo nessuna fonte sullo stereo attivo (solo LiDAR o ToF).

## P4 — Limite di osservabilità (calcolo)
Camera 848×480, campo orizzontale 87° → focale di circa 447 px. Impronta di un pixel: z/f.
- Previsione: impronta di circa 6,7 mm a 3 m e 13,4 mm a 6 m; con il criterio «almeno 5 pixel di lato» la dimensione minima è 3–4 cm a 3 m e 6–7 cm a 6 m.
- Velocità massima seguibile per un oggetto che attraversa il campo a 3 m, chiedendo 5 fotogrammi consecutivi in campo: fra 15 e 25 m/s a 15 fotogrammi al secondo, il doppio a 30. Il limite vero del nucleo è più basso: la porta di associazione tarata su 2,5 m/s.
- Un frammento di 1 cm a 3 m: sotto il limite → «non osservabile».
- **Smentita:** dimensione minima a 3 m fuori da 2–5 cm; velocità a 15 fotogrammi al secondo fuori da 10–30 m/s.

## P5 — Ombra di un ostacolo più basso del sensore (calcolo)
Sensore a 1,2 m; ostacolo alto a alla distanza d: l'ombra al suolo finisce a d·h/(h−a).
- Previsione: scatola da 0,5 m a 1,5 m → l'ombra al suolo finisce a circa 2,6 m (non al bordo dei 3 m); dietro, una persona di 1,7 m resta visibile dalla vita in su. Il cuneo del nucleo è quindi prudente in eccesso (non pericoloso): è il beneficio più netto di una mappa in quota.
- **Smentita:** l'ombra calcolata arriva a 3 m o oltre per ostacoli di 0,3–0,6 m posti fra 1,3 e 2 m.

## P6 — Costo di una griglia 3D **densa** sulla regione 6 × 4 × 3 m (misura su CPU, C, un processo, ≤ 2 minuti)
- Voxel: 576 000 a 5 cm, 72 000 a 10 cm. Con 4 byte per voxel: 2,3 MB e 0,29 MB. Previsione: la memoria densa è così piccola che «sparso» non dà un beneficio di memoria utile a questa scala.
- Lancio dei raggi (attraversamento voxel per voxel), 212×120 = 25 440 raggi (un pixel su 4 per lato), scena vuota (caso peggiore: ogni raggio arriva a fine portata): previsione mediana < 10 ms e 95° percentile < 20 ms a 5 cm; a piena risoluzione (407 040 raggi) fra 50 e 150 ms, cioè **oltre** i 66 ms di un ciclo a 15 Hz.
- **Smentita:** mediana a 25 440 raggi > 66 ms; oppure piena risoluzione sotto 30 ms (allora la decimazione non serve).
- Indipendenza: programma, scena e misura sono miei; è una scena sintetica, non il prototipo né il sensore.

## P7 — Casi d'uso documentati (ricerca in rete)
- Mi aspetto fonti apribili per: (a) oggetti estranei su piste e piazzali (circolare FAA sui sistemi di rilevamento); (b) urti a terra in hangar e sul piazzale fra velivoli e mezzi; (c) aree condivise persone–mezzi o persone–robot.
- **Smentita:** per nessuno dei tre trovo una fonte primaria apribile.

## P8 — Quanto è davvero «sparsa» la regione frontale (aggiunta alle 2026-11-14T15:08:44+01:00, dopo le ricerche in rete e **prima** di scrivere ed eseguire qualunque programma)
Se «libero osservato» va memorizzato (principio: il non allocato è sconosciuto, mai libero), i voxel attraversati dai raggi vanno allocati tutti. Stima a mente del tronco di vista (87° × 58°, sensore a 1,2 m inclinato di 15°) dentro la scatola 6 × 4 × 3 m.
- Previsione: in una stanza vuota i voxel toccati in un fotogramma sono fra il 45 % e il 70 % della regione; quindi una struttura sparsa a blocchi risparmia al più circa un fattore 2 sulla memoria densa, prima dei costi della tabella hash.
- **Smentita:** quota toccata sotto il 25 % (allora lo sparso conviene) in stanza vuota.
- Con una parete a 2 m di fronte la quota scende (previsione: sotto il 25 %): lì lo sparso risparmia, ma su una memoria già di pochi megabyte.

## Esito di P1, P2, P3, P7 (scritto dopo le ricerche, alle 2026-11-14T15:08:44+01:00)
Vedi `CONSEGNA.md`. In breve: P1 regge salvo OpenVDB (ora Apache 2.0: il dubbio era scritto) e salvo due precisazioni notate dopo (OctoMap codifica lo sconosciuto in modo *implicito*; Bonxai non dà una semantica dello sconosciuto, restituisce un puntatore nullo); la licenza di nvblox non verificata (404 sul file). P2 regge. P3 **non risolta**: nessuna fonte trovata che misuri uno stereo attivo in nebbia o fumo. P7 regge per (a) e (b) con fonte secondaria o comunicato, (c) regge.

## Esiti dei calcoli e della misura (scritti alle 2026-11-14T15:15:22+01:00, dopo i lanci)
- **P4 regge:** impronta 6,7 mm a 3 m e 13,4 mm a 6 m; con 5 pixel 3,4 cm e 6,7 cm; attraversamento a 3 m, 15 fotogrammi al secondo: 17,1–21,4 m/s (`risultati_osservabilita.txt`).
- **P5 smentita in parte:** scatola da 0,5 m a 1,5 m → 2,57 m (regge); ma la stessa scatola a 2,0 m dà 3,43 m, cioè oltre i 3 m, dentro l'intervallo che avevo scritto come soglia di smentita. Il beneficio vale solo per ostacoli bassi **e** vicini.
- **P6 regge per la memoria e per la riga decimata, smentita in parte per la piena risoluzione:** 2,20 MB a 5 cm, 0,27 MB a 10 cm; 25 440 raggi a 5 cm: mediana 9,6–13,2 ms, 95° percentile 9,7–13,3 ms, massimo 15,5 ms; piena risoluzione a 5 cm: 148–199 ms (avevo scritto 50–150). **Notato dopo:** il caso peggiore non è la stanza vuota (solo il 55,8 % dei raggi ha un ritorno entro 6 m) ma la parete a 2 m (100 % di raggi validi).
- **P8 smentita:** voxel toccati 18,2–20,9 % in stanza vuota (avevo scritto 45–70 %), 8,5–9,5 % con la parete a 2 m. Causa: i raggi senza ritorno non aggiornano niente, e quasi metà dei raggi non ha ritorno. Lo sparso risparmierebbe quindi un fattore 5–12, ma su 2,2 MB.
- **Scostamento:** il primo lancio di `griglia_densa` (15:09:46) è stato fermato da `timeout 120` senza uscita (200 fotogrammi anche a piena risoluzione; uscita in coda nel buffer). Rilanciato alle 15:12:06 con 30 fotogrammi per le righe a piena risoluzione e `timeout 100`.

## P9 — Previsioni per i falsificatori delle due proposte (scritte alle 2026-11-14T15:15:22+01:00, prima che qualcuno li esegua)
- `esperto-dominio-1` (zone dichiarate): nella riproduzione dell'atto 4, 0 fotogrammi «vuota osservata» con la persona nascosta dentro la zona (smentita: 1 fotogramma). Braccio di utilità: una zona di 1 × 1 m in campo aperto fra 1,5 e 2,5 m (circa 280 celle) esce «vuota osservata» in circa il 96,6 % dei fotogrammi con suolo valido 0,95 (conto: (1 − 0,05³)^280), e scende al 75,6 % con 0,90 (smentita dell'utilità: sotto il 90 % a 0,95).
- `esperto-dominio-2` (griglia densa locale): sul portatile della squadra, `timeout 100 ./griglia_densa`: riga «parete a 2 m, 5 cm, 25 440 raggi» con 95° percentile ≤ 20 ms (smentita: > 66 ms). Scena con scatola da 0,5 m a 1,5 m: fra 2,57 e 3 m il 3D restituisce celle di suolo «libero osservato» che il cuneo dà «in ombra» (smentita: nessuna cella restituita, oppure un voxel mai attraversato che risulta libero).
