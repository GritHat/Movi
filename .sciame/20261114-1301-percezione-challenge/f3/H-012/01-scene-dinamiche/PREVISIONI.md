# Previsioni per le prove A, B, C di f4 — H-012, `sciame-scene-dinamiche` (responsabile)

**Ora di scrittura:** 2026-11-14T14:00:30+01:00 (`date -Is`), prima di ogni prova di f4. Io non ho eseguito nessuna prova: queste previsioni vengono dal solo ragionamento sui file del torneo (`TORNEO.md`, `risultati_*_parte2.txt`, `risultati_*_parte3.txt`) e sulla selezione (§5). **Che cosa condivido con ciò che prevedo:** il modello linguistico, le schede, i numeri del torneo; nessun codice mio. I conti marcati **[resp.]** sono miei, a mano, non verificati.

decide: sì

Le prove A–C possono decidere il ramo **nel dominio simulato** (sensore fermo, pedone sintetico): A ha un falsificatore a un solo controesempio, B decide K-007, C è esaustiva sulle sei righe delle regole. Non decidono nulla di ciò che la selezione (§5) elenca come «non verificato fino all'hardware».

## Definizioni fissate prima (servono a leggere le soglie)

- **Parametri del ramo:** 15 Hz; q = 0,2 m²/s³; cerchio al 95 % (χ² = 5,991); fascia di guardia g = 0,40 m (0,20 di errore d'ombra + 0,20 di mezzo corpo, corpo 40 cm); rilascio per osservazione dopo ≥ 3 fotogrammi consecutivi; v_max = 2,5 m/s con margine 3σ√2 (come in `scena_parte3.py`, riga 160); tetto dell'avviso legato alla traccia T_g = 10 s (valore di H-015, mai attaccato).
- **Strato 1** = celle non osservate (in ombra, oltre portata, fuori campo, buco) contigue al punto d'ingresso della traccia, dilatate di g rispetto al bordo dell'ombra **stimata**.
- **«Nascosto»** = centro del corpo dentro l'ombra **vera**. Un corpo in parte visibile e non rilevato, con il centro fuori dall'ombra vera, si conta a parte.
- **«Celle viste libere oltre la fascia»**: (a) nei termini del sistema: celle che il sistema ha classificato «libero» nel fotogramma corrente a più di g dal bordo dell'ombra stimata; (b) contro la verità: celle davvero visibili a più di g + 0,20 = 0,60 m dal bordo dell'ombra vera. **Dichiaro prima:** con errore d'ombra di +20 cm lo strato 1 sta per forza su celle davvero visibili fino a 0,60 m dal bordo vero (0,20 + 0,40 [resp.]); chi misura «oltre 0,40 m dal bordo vero» troverà una striscia di 0,20 m, e non è un difetto nascosto: è l'incertezza dell'ombra, che g deve coprire nei due versi.
- **Strato 2 «contiene alla riemersione»**: la prima misura dopo il buio cade nel cerchio al 95 % E a non più di g dalla regione ritagliata calcolata al ciclo precedente (la misura cade per forza su una cella ora osservata: senza questa tolleranza il ritaglio la escluderebbe sempre).

## Prova A — la composizione come insieme

| # | Misura | Soglia di smentita | Esito atteso |
|---|---|---|---|
| A1 | quota di fotogrammi con soggetto nascosto dentro lo strato 1; 4 comportamenti × 2 ombre × errore −20 / 0 / +20 cm, corpo 40 cm | **un solo** nascosto fuori dallo strato 1 (soglia dell'arbitro: < 99 %) | **regge**: 100 % in tutte le celle. Rischio che vedo: a −20 cm, con «nascosto» letto come «non rilevato», il centro arriva a 0,40 m dall'ombra stimata, cioè sul filo di g: lì mi aspetto qualche caso fuori, e li conto a parte |
| A2 | quota dello strato 1 su celle viste libere oltre la fascia, definizioni (a) e (b) | (a) > 0 %; (b) una cella davvero visibile oltre 0,60 m dal bordo vero | **regge**: 0 % in (a), ma è per costruzione (vale come controllo dell'invariante, non come prova); 0 % in (b). Con la lettura «oltre 0,40 m dal bordo vero» a +20 cm: > 0 % (dichiarato sopra) |
| A3 | strato 2 ritagliato contiene alla riemersione, per comportamento | < 85 % su «prosegue», oppure < 85 % su una miscela tipo G1 (60 / 15 / 10 / 15) | **regge** su «prosegue» (0,86–0,94) e «sosta» (0,85–0,98); **sotto soglia** su «torna» (0,50–0,70: è il 56–66 % del torneo, il ritaglio non lo cura); «esce dal lato lontano» non riemerge in vista: va allo strato 1. Con pesi uguali fra i comportamenti mi aspetto 0,78–0,88 [resp.]: sul filo, e lo dichiaro |
| A4 | quota di transiti «prosegue» in cui lo strato 2 è ancora mostrato alla riemersione (regola «meno di metà dell'ombra») | nessuna soglia: misura descrittiva | pannello 1 m (transito 1,70 s): 30–70 %; pannello 2 m: 0–10 %. Cioè con l'ombra larga il ritorno avviene da «perso», attraverso lo strato 1 |
| A5 | identità alla prima ri-rilevazione, una sola traccia pendente nell'ombra (riaggancio dello strato 1, anche da «perso») | < 95 % | **regge**: ≥ 95 % (il disco del torneo dà 100 %) per chi riemerge in vista entro T_g |
| A6 | due bersagli: scambi d'identità senza segnale «identità ambigua» | > 0 scambi muti | **regge**: 0 muti; «ambigua» nel 60–100 % dei casi in cui tornano entrambi |
| A7 | durata del rilascio dello strato 1 | un caso oltre T_g + 3 fotogrammi = 10,2 s; oppure un rilascio per osservazione con il soggetto nascosto | **regge**: finita in tutti i casi. Chi riemerge: al riaggancio. Chi esce dal lato lontano: a T_g = 10 s, e le celle restano «non osservate», mai «libere». Rilasci per osservazione a soggetto nascosto: 0 % a 0 e +20 cm; a −20 cm 0 % (g supera l'errore), **non certo** |

## Prova B — R1 con rumore che cresce con la distanza (decide K-007)

Regola di default: spostamento su una finestra di 1 s oltre 5·σ(z)·√2, per asse, con R(z) da una scheda. Alternativa: χ² con R(z). **Distanza dichiarata per R1 in avvicinamento lento: 2 m.**

| # | Misura | Soglia di smentita | Esito atteso |
|---|---|---|---|
| B1 | falsi «mobile» sul muro fermo a 4 m, quota delle finestre | > 10 % | **regge** per tutte e due le regole con R(z): ≤ 2 % |
| B2 | pedone a 0,5 m/s **di traverso**, visto entro 1 s, a 2 e a 3 m | < 90 % | **regge**: ≥ 95 % (il rumore laterale è piccolo) |
| B3 | pedone a 0,5 m/s **in avvicinamento** a 2 m, visto entro 1 s | < 90 % | spostamento: **regge** (90–99 %; soglia 0,35 m contro 0,5 m percorsi [resp.]). χ²: **smentita** (70–80 %; il torneo dà 75,4 %) |
| B4 | lo stesso a 3 m e a 4 m | nessuna soglia: fissa il limite da dichiarare | 3 m: 30–80 % secondo la scheda usata (soglia 0,48–0,80 m [resp.] contro 0,5 m percorsi); 4 m: < 30 % per tutte e due. **Nessuna regola vede in 1 s chi si avvicina piano oltre 3 m: è il rapporto fra spostamento e rumore, non la regola** |

Esito atteso per K-007: vince lo spostamento su 1 s alla distanza dichiarata; oltre, la velocità minima vista si dichiara come 5·σ_r(z)·√2 al secondo. Se B3 cade anche per lo spostamento, R1 resta «non risolto» in avvicinamento e la demo mostra solo attraversamenti.

## Prova C — copertura e latenza, a mano

| # | Misura | Soglia di smentita | Esito atteso |
|---|---|---|---|
| C1 | R1–R8: ognuno con componente e misura di accettazione; lettura di «riconoscere» scritta | un requisito senza componente o senza misura; una frase prescrittiva delle regole scoperta | **regge**: 8 su 8 |
| C2 | bilancio della latenza con gli estremi nominati e una fonte per sensore e audio | manca la fonte per un tratto | **non risolta** sul tratto dal fotone al suono: per il sensore c'è solo una lettura incerta di un forum, non aperta; per l'audio nessuna fonte. Il tratto interno (marca di cattura → comando audio) resta una stima fino alla misura sul prototipo |

## Che cosa cambierebbe la decisione

A1 smentita → il ramo cade come garanzia (R8). A3 smentita su «prosegue» → lo strato 2 non informa: resta il solo strato 1 (H-009). B3 smentita per entrambe le regole → R1 solo di traverso. C2 non risolta → R7 dichiarato «non risolto», come chiede la selezione.
