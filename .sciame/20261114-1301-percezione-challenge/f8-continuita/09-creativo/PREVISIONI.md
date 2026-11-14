# Previsioni — sciame-creativo, f8 (continuità visiva), corsia B

Scritte alle **2026-11-14T15:20:14+01:00** (`date -Is`), PRIMA di scrivere e lanciare `cono.py` e `tabellone.py`.
A quest'ora ho letto: la traccia, il contratto f8, gli addendum, `SOLUZIONE_V2.md`, `VERDETTO.md`, `TORNEO_parte2.md`, `TORNEO_parte3.md`, la consegna del creativo di f1, e il codice di `scena_parte3.py` e `torneo_parte2.py` (solo i generatori). Nessuna prova mia ancora eseguita.

## Impianto della prova (fissato prima)

- Scena e traiettorie di prova: COPIA di `vis()`, `truth()` e `KF` di `f2/04-torneo/scena_parte3.py` (autore: avversario, non io): sensore in (0,0), campo ±43,5°, portata 6 m, pannello a 2 m largo 1 m (e 2 m), pedone puntiforme a 4 m, 1,0–1,5 m/s, 15 Hz, rumore 5 cm, Pd 0,9. Comportamenti dell'avversario: prosegue, sosta (2–4 s), torna, lontano (esce dal lato lontano). Due comportamenti aggiunti da me (dichiarati miei): rallenta (×0,3–0,5), svolta (45–90°).
- Dati di «taratura» (la libreria degli analoghi): COPIA di `g1()` di `f2/04-torneo/torneo_parte2.py` (autore: avversario; miscela 60/15/10/15 prosegue/sosta/torna/svolta, manovra a istante uniforme in 6 s). Generatore diverso da quello della prova: niente «lontano», niente «rallenta», soste di 0,5–3 s, virate graduali.
- Predittore in prova (creativo-2, «cono degli analoghi sfoltito alle bocche»): 400 membri della libreria trapiantati sul punto e sulla velocità d'ingresso del Kalman; un membro che cade in una cella vista libera oltre una fascia di 0,2 m pesa ×0,1 a ogni ciclo; sfondo «allagamento» = celle non viste raggiungibili a 2,5 m/s passando solo per celle non viste, con massa a priori ε = 0,05 (fissata ora, non tarata); regioni al 50 % e al 90 % = celle (0,25 m) più dense; se la regione ha bisogno dello sfondo lo prende tutto («diffuso»). Fantasma = membro più vicino alla mediana pesata, con passo limitato a 2,5 m/s.
- Confronti: fermo all'ultima posizione; velocità costante (il Kalman del nucleo, q = 0,2); regola del nucleo (cerchio al 95 % ritagliato, mostrato finché copre meno di metà dell'ombra, poi «perso»).
- Misure solo nei cicli in cui il soggetto non è visibile. 100 passaggi per comportamento, seme 20261114.

## Previsioni

**P-creativo-1 (continuità).** Il nucleo emette una stima (posizione + regione) in meno del 50 % dei cicli senza osservazione nei passaggi con sosta e in meno del 40 % in quelli «lontano». Il cono emette nel 100 % (per costruzione: non è un dato); la quota in regime informativo (regione al 90 % non diffusa e sotto metà dell'ombra) è ≥ 60 % dei cicli nascosti sulla sosta. **Smentita:** quota informativa del cono < quota del nucleo + 15 punti sulla sosta.

**P-creativo-2 (taratura per comportamento).** Regione al 90 %: copertura ≥ 85 % per prosegue, rallenta, sosta; ≥ 80 % per torna; ≥ 75 % per svolta; ≥ 80 % per «lontano» (grazie allo sfondo). **Smentita:** una cella comportamento × tempo (1, 2, 3, 4, 5 s) con n ≥ 30 sotto il 75 %. Regione al 50 %: copertura aggregata fra 35 % e 70 % a ogni tempo; mi aspetto «lontano» sotto (20–50 %) e sosta sopra a 3–5 s: se è così la regione al 50 % NON è tarata per comportamento e lo scrivo. Area della regione al 90 %: sotto il 60 % dell'ombra fino a 1 s; in regime diffuso (tutta l'ombra raggiungibile) a 3 s nei passaggi con sosta in più di metà dei casi.

**P-creativo-2b (braccio che deve fallire).** Con ε = 0 (nessuno sfondo) la copertura al 90 % di «lontano» a 3 s scende sotto il 60 % (riproduce il 22–41 % delle particelle del torneo). Se non scende, lo sfondo non serve e la prova è cieca su quel punto.

**P-creativo-3 (efficacia).** Errore mediano del fantasma, media a pesi uguali sui sei comportamenti, a 2 s e a 3 s: minore sia di «fermo» sia di «velocità costante». **Smentita:** il fantasma perde contro una delle due a 2 s o a 3 s nell'aggregato. Per comportamento mi aspetto che perda contro la migliore delle due (velocità costante su prosegue, fermo su torna) ma di meno di 0,5 m.

**P-creativo-4 (regolarità e salto).** Passo del fantasma ≤ 0,167 m per ciclo (per costruzione). Passi all'indietro (> 2 cm contro la direzione d'ingresso) in meno del 5 % dei cicli nei passaggi «prosegue». Salto fra fantasma e prima misura alla ricomparsa: mediana ≤ 0,4 m per prosegue; prima misura entro 0,45 m da una cella della regione al 90 % in ≥ 85 % delle ricomparse (tutti i comportamenti insieme). **Smentita:** una delle tre soglie mancata.

**P-creativo-5 (costo).** Passo completo (membri, sfoltimento, regioni, fantasma) in Python puro: mediana < 10 ms per ciclo (un ciclo a 15 Hz dura 66,7 ms). **Smentita:** > 20 ms.

**P-creativo-6 (tabellone, creativo-1).** Conto binomiale esatto: con 30 occlusioni (virtuali o vere) e soglia «≥ 24 su 30 dentro la regione al 90 %», un sistema tarato (0,90) passa con probabilità ≥ 0,95 e uno mal tarato (0,70) con probabilità ≤ 0,20. **Smentita:** uno dei due numeri fuori.

**P-creativo-7 (pannello virtuale contro vero).** Ripesando le coperture per comportamento del lancio principale: con la miscela «in vista» (90 % prosegue, 5 % rallenta, 5 % svolta) la copertura al 50 % misurata dal pannello virtuale supera di almeno 10 punti quella della miscela «dietro il pannello vero» della demo (40 % prosegue, 30 % sosta, 15 % torna, 15 % lontano) ad almeno uno dei tempi 2–4 s: cioè il pannello virtuale è ottimista se la gente dietro un pannello vero si comporta in modo diverso. **Smentita:** differenza sotto 10 punti a tutti i tempi (allora il limite dichiarato è meno grave del previsto). Le due miscele sono mie ipotesi, non dati.

---

# Esiti della versione registrata (v1, «miscela con sfondo»), lanciata alle 15:24:45–15:25:18

Prima del lancio pieno ho fatto una prova di fumo (8 passaggi per prosegue, sosta, lontano, stessi semi): ne ho visto i numeri, ma non ho cambiato una riga del codice fra la prova di fumo e il lancio registrato. File: `esito_v1_w1.txt`, `esito_v1_w2.txt`, `esito_v1_w1_eps0.txt`.

- **P-creativo-1: SMENTITA** sul pannello da 1 m. Nucleo: stima mostrata nel 39,3 % dei cicli nascosti sulla sosta e nel 34,9 % su «lontano» (queste due parti reggono). Cono informativo sulla sosta: 39,2 %, non ≥ nucleo + 15 punti. (Sul pannello da 2 m: 59,5 % contro 28,2 %.)
- **P-creativo-2: SMENTITA.** Regione al 90 % a 1 s: sosta 71 %, torna 69 %, svolta 68 %, lontano 64 % (soglia 75 %). La regione al 50 % non è tarata per comportamento (a 2 s: torna 3 %, svolta 4 %, lontano 9 %). Da 2 s in poi la regione al 90 % è «diffusa» nel 66–100 % dei casi: copre, ma è tutta l'ombra raggiungibile.
- **P-creativo-2b: REGGE** (braccio che deve fallire): con ε = 0 «lontano» a 3 s è coperto nell'1 % e la sosta nel 27 %.
- **P-creativo-3: REGGE nell'aggregato** (2 s: fantasma 1,18 m, velocità costante 1,76, fermo 1,38; 3 s: 1,44 / 2,84 / 1,63; medie delle mediane sui cinque comportamenti ancora nascosti), **smentita nella parte per comportamento**: su «torna» a 2 s perde di 1,13 m contro «fermo» (1,50 contro 0,37).
- **P-creativo-4: REGGE** sulle tre soglie (passi indietro 0,1 % su prosegue; salto mediano 0,32 m; prima misura entro la regione 387 su 430 = 90 %), ma «torna» da solo è al 59 %.
- **P-creativo-5: REGGE** (mediana 0,22 ms, p95 0,31 ms).

**Che cosa ho capito (dopo, non prima):** (1) fra l'ingresso e l'uscita nominale nessuna evidenza distingue chi prosegue da chi si è fermato: una regione che segue solo il fronte perde chi resta indietro; (2) scommettere su una miscela di comportamenti (la libreria dice 60 % prosegue) rende la regione «sicura di sé e sbagliata» per i comportamenti rari.

# Versione 2 («scenari»: l'unione delle regioni per scenario) — previsioni scritte alle 2026-11-14T15:25:55+01:00, PRIMA di scrivere `cono2.py`

**Disegno, nato DOPO aver visto gli esiti di v1.** Niente miscela e niente ε. Tre scenari, ciascuno con il suo insieme di membri, costruiti dalla sola classe «prosegue» della libreria g1 con trasformazioni: **A fronte** (200 membri: prosegue); **B scia** (200: lo stesso percorso, congelato a un istante uniforme fra l'ingresso e la propria uscita dall'ombra: copre chi rallenta, si ferma, torna sui suoi passi); **C ventaglio** (400: virata istantanea di ±45–90°, l'intervallo della libreria, a un istante uniforme fra l'ingresso e la propria uscita). Sfoltimento come prima (fascia 0,2 m, ×0,1 per ciclo in una cella vista libera). Regione al livello p = UNIONE delle regioni più dense al livello p di ciascuno scenario (ogni membro pesa ½ sulla sua cella da 0,25 m e ⅛ sulle quattro vicine non libere). Fantasma = membro più vicino alla mediana pesata con la convenzione 0,6 / 0,25 / 0,15 (solo per il disegno, non per la regione). Area contata solo dentro campo e portata; «informativa» = area della regione al 90 % sotto metà dell'ombra in portata. Limite dichiarato: conosco il generatore di prova (l'ho letto prima); l'intervallo della virata è quello della libreria, non quello della prova («lontano» vira di 80–100°).

**P-creativo-8 (taratura per comportamento, v2).** Regione al 90 %: copertura ≥ 85 % per prosegue, rallenta, sosta, torna a ogni tempo con n ≥ 30; ≥ 75 % per svolta; ≥ 60 % per «lontano» (fuori dall'intervallo della libreria: mi aspetto 60–85 %). Regione al 50 %: ≥ 45 % per prosegue, rallenta, sosta, torna. **Smentita:** una cella con n ≥ 30 sotto la sua soglia.

**P-creativo-9 (incertezza controllata, v2).** Area della regione al 90 % dentro campo e portata: ≤ 35 % dell'ombra a 1 s; ≤ 80 % a 3 s. Quota informativa dei cicli nascosti sulla sosta ≥ 60 % (pannello da 1 m), cioè almeno 20 punti sopra il nucleo (39,3 %). **Smentita:** una delle tre soglie mancata.

**P-creativo-10 (prezzo del ventaglio, braccio che deve fallire).** Senza lo scenario C la regione al 90 % a 3 s scende sotto il 40 % dell'ombra, e «lontano» a 3 s è coperto in meno del 30 %. **Smentita:** «lontano» ≥ 30 % senza C (allora il ventaglio non serve).

**P-creativo-11 (efficacia e ricomparsa, v2).** Errore mediano del fantasma, media sui comportamenti ancora nascosti, a 2 s e a 3 s: sotto entrambe le linee di base. Alla ricomparsa, ultimo ciclo nascosto dentro la regione al 90 %: ≥ 85 % per ogni comportamento con n ≥ 30 (in v1 «torna» era al 45 %). **Smentita:** una delle due.

**P-creativo-12 (costo, v2).** 800 membri: mediana < 10 ms per ciclo in Python puro. **Smentita:** > 20 ms.

---

# Esiti della versione 2 (scritti alle 2026-11-14T15:37:04+01:00, dopo i lanci delle 15:27–15:35)

Prima del lancio registrato: un errore corretto nella virata dello scenario C (la rotazione leggeva la lista già sovrascritta) e una prova di fumo di 3 passaggi «prosegue»; nessun numero di v2 visto prima della correzione. Il codice dei lanci registrati è `cono2_registrato.py`; `cono2.py` aggiunge solo opzioni esplorative e una colonna (uscite predefinite identiche: `diff` vuoto sulle prime 150 colonne).

- **P-creativo-8: SMENTITA in tre punti, regge sul resto** (`esito_v2_w1.txt`). Regione al 90 %: prosegue, rallenta, sosta, torna 98–100 % a ogni tempo (regge). Svolta 94 % a 2 s, 78 % a 3 s, poi **42 % e 32 %** a 4 e 5 s; «lontano» 85 / 72 / **57 / 36 / 19 %** a 1–5 s. Regione al 50 %: sosta a 5 s **24 %** (n = 33).
- **P-creativo-9: SMENTITA.** Area al 90 % a 1 s: **46–47 %** dell'ombra (soglia 35 %); a 3 s 55–66 % (regge); quota informativa sulla sosta **48,8 %** contro il 38,0 % del nucleo (+10,8 punti, non +20).
- **P-creativo-10: REGGE** (`esito_v2_w1_senzaC.txt`). Senza ventaglio: area al 90 % a 3 s 34–38 %; «lontano» a 3 s coperto nel 3 %.
- **P-creativo-11: REGGE.** Errore mediano, media sui comportamenti ancora nascosti: a 2 s fantasma 0,98 m, velocità costante 1,67, fermo 1,41; a 3 s 1,45 / 3,04 / 1,68. Ultimo ciclo nascosto dentro la regione al 90 %: 98–100 % per i cinque comportamenti che ricompaiono.
- **P-creativo-12: REGGE.** Mediana 1,06 ms, p95 2,15 ms, massimo 3,03 ms; creazione all'ingresso 15,3 ms (massimo 30,2 ms).
- **P-creativo-6: REGGE** (`esito_tabellone.txt`): 0,974 e 0,160. Notato dopo: con 30 prove un sistema a 0,80 passa nel 60,7 %; con 60 prove e soglia 51 passa nel 21,3 %.
- **P-creativo-7: SMENTITA** (`esito_tabellone.txt`): differenze +5,8 / −1,9 / +1,6 punti a 2, 3, 4 s (soglia +10). La previsione era mal posta: fra chi è ancora nascosto dopo 2 s chi prosegue non c'è più, e il segno dipende dalle due miscele, che sono mie ipotesi.

## Notato dopo (non registrato prima; esplorativo)

1. Il braccio «senza ventaglio» (fronte + scia) è la configurazione più utile: chi resta sul percorso è coperto nel 99–100 % con il 12 / 25 / 37 / 34 / 31 / 29 % dell'ombra a 0,5–5 s; informativa nel 97–100 % dei cicli nascosti; chi lascia il percorso è coperto nello 0–21 % da 2 s.
2. Pannello da 2 m (`esito_v2_w2*.txt`): fronte + scia ≥ 96 % sul percorso, area 6 / 13 / 37 / 51 / 50 / 47 %, informativa nel 74–87 % (nucleo 28–48 %).
3. Ombra stimata più stretta di 20 cm (`esito_v2_w1_senzaC_ombra-20.txt`): sul percorso ≥ 98 % nelle celle con n ≥ 30.
4. Contando «fuori area» come coperto quando la regione tocca il bordo della portata (colonna aggiunta, `esito_v2_w1_uscita.txt`): «lontano» 85 / 85 / 100 / 100 / 100 %, svolta 94 / 84 / 68 / 67 % a 2–5 s.
5. Ventaglio largo 30–135° (`esito_v2_w1_ventaglio_largo.txt`): «lontano» 98 / 92 / 93 / 74 % a 1–4 s, ma area 50 / 97–98 / 76–86 % dell'ombra.
6. Fantasma sullo scenario più probabile invece che sulla mediana della miscela (`esito_v2_w1_senzaC_map.txt`): salto mediano alla ricomparsa su «prosegue» 0,32 m contro 0,43 (velocità costante 0,28).

# Falsificatore del terzo generatore (creativo-2) — previsione scritta alle 2026-11-14T15:39:21+01:00, prima di scrivere `terzo.py`

Traiettorie: COPIA di `traiettoria()` del rovesciatore (in `f2/04-torneo/torneo_parte2.py`; pannello da 1,5 m, manovra fra −1,2 e 1,2 m, soste di 2–6 s, 60/25/15 prosegue/sosta/torna), con la sola aggiunta della manovra forzata e del passo a 15 Hz. Predittore: fronte + scia (`AB`), invariato. 100 passaggi per comportamento.
**P-creativo-13.** Regione al 90 %: ogni cella comportamento × tempo con n ≥ 30 al 90 % o più. **Smentita:** una cella sotto l'85 %. Fra 85 e 90 %: non risolta.
**Esito (lancio delle 15:39, `esito_terzo.txt`): REGGE.** Le 12 celle con n ≥ 30 stanno fra il 96 % e il 100 % (minimo: torna a 0,5 s, 96 %, n = 98). Notato dopo: informativa nell'89–97 % dei cicli nascosti (nucleo 31–63 %); area al 90 % fra l'8 % e il 44 % dell'ombra in quelle celle.
