# Previsioni di `sciame-interfacce` (f9, S5 e uscita di S8)

Scritte alle **2026-11-14T15:41:47+01:00** (`date -Is`), dopo la lettura del contratto, dell'addendum, della preproposta, del nucleo (versione 2), del verdetto e del sorgente v0.5; **prima** di ogni script e di ogni ricerca in rete. Gli esiti sono in fondo, aggiunti dopo.

Che cosa condivido con ciò che controllo: il modello linguistico e la specifica (la preproposta e il nucleo); gli script sono miei, quindi generatore e giudice hanno lo stesso autore: valgono come conti, non come misure indipendenti. Nessuna persona, nessuno schermo vero, nessun suono riprodotto.

| # | Enunciato | Misura | Soglia di smentita |
|---|---|---|---|
| int-P1 | Il colore da solo non distingue i tre stati in bianco e nero: fra i tre colori di stato del documento v0.5 (`ok` 1E7A4C, `warn` A8620A, `todo` 6B7280) e in una terna «semaforo» qualunque (verde 2E7D32, ambra FFB300, rosso C62828) c'è almeno una coppia con rapporto di contrasto di luminanza sotto 3:1 (soglia WCAG 1.4.11 per gli oggetti grafici), e almeno una sotto 1,5:1 | luminanza relativa sRGB e rapporto (L1+0,05)/(L2+0,05), in grigio e con le matrici di Machado per protanopia, deuteranopia, tritanopia | smentita se in tutte e due le terne ogni coppia sta a 3:1 o più, in grigio e nelle tre simulazioni |
| int-P2 | Con il filtro del nucleo (velocità quasi costante, q = 0,2 m²/s³, 15 cicli al secondo) e senza ritaglio, nel formato «±X.XX m» l'ultima cifra cambia in almeno il 90 % dei cicli fra 0,3 e 2 s di occlusione; l'etichetta a tre campi cambia almeno 10 volte al secondo | conto dei cicli in cui la stringa formattata differisce dalla precedente | smentita se l'ultima cifra cambia in meno del 50 % dei cicli |
| int-P3 | «±σ» in due dimensioni contiene il soggetto in meno della metà dei casi (atteso 39 %); alla tolleranza d'esempio della preproposta (σ_eff ≤ 0,8 m) il raggio al 95 % supera la larghezza del pannello della demo (1 m) | formula della gaussiana isotropa in 2D, r_p = σ·√(−2 ln(1−p)) | smentita se la quota a 1σ è ≥ 50 % o se il raggio al 95 % è ≤ 1 m |
| int-P4 | Dopo il ritaglio sull'ombra della demo (pannello di 1 m a 1,8 m, griglia fino a 3 m) lo scarto σ_eff della massa stesa su tutto il cuneo resta sotto 0,8 m: la soglia d'esempio non fa mai scattare «perso», e il numero dopo «±» misura il pannello, non la conoscenza | scarto quadratico di una distribuzione uniforme sul cuneo, per asse e radiale, con e senza la fascia di 0,40 m | smentita se lo scarto radiale del cuneo senza fascia è ≥ 0,8 m |
| int-P5 | Le misure di taratura chieste dall'attacco 5 (30 passaggi veri, oppure 400 simulati) non sostengono il secondo decimale: l'intervallo di Wilson al 95 % sulla copertura si traduce in almeno ±10 % sul raggio con 30 passaggi (cioè ±8 cm su 0,8 m) | intervallo di Wilson su 27/30 e 360/400; raggio corrispondente | smentita se l'incertezza sul raggio è sotto 0,5 cm su 0,8 m |
| int-P6 | A leggibilità da sala (carattere alto 20 minuti d'arco per l'ultimo giurato a 6 m, schermo proiettato largo 2 m e 1920 punti: ipotesi mie) l'etichetta obbligatoria (circa 40 caratteri) è larga più del doppio dell'ombra del pannello disegnata in mappa, e tre etichette non stanno nella larghezza dello schermo | geometria | smentita se tre etichette stanno in metà della larghezza |
| int-P7 | Con tre oggetti nascosti e un canale sonoro seriale (segnale di 0,3 s più 0,1 s di pausa), la coda per oggetto fa partire almeno il 15 % dei segnali oltre 300 ms dopo l'evento (soglia R5); una regola per settore con priorità e scarto dei segnali scaduti scende sotto il 5 % senza dire stati scaduti | simulazione a eventi, seme fissato: 3 oggetti, ingressi in una finestra di 2 s, occlusioni di 0,7–2,0 s (i numeri della preproposta), 20 000 scene | smentita se la coda per oggetto resta sotto il 5 % (la regola non serve), oppure se la regola per settore resta al 15 % o più |

Non sono previsioni (non hanno una prova oggi): che tre timbri si riconoscano a orecchio; che il battito non copra l'udito ambientale; che un giurato legga «conf Z %» come probabilità. Restano «non verificato», con la prova che le decide (cinque minuti, tre persone).

## Esiti (aggiunti dopo le prove)

Prove lanciate alle 2026-11-14T15:44:31+01:00 (`prove_interfacce.py` → `risultati_interfacce.txt`); la seconda, esplorativa e **non prevista**, alle 15:45:05 (`prove_interfacce_bis.py` → `risultati_interfacce_bis.txt`). Le fonti in rete sono state cercate dopo la scrittura delle previsioni.

| # | Esito | Numeri |
|---|---|---|
| int-P1 | **regge** | terna del documento: 1,12 / 1,10 / 1,02 : 1 in grigio; terna «semaforo»: verde/rosso 1,10:1 in grigio (1,13 in deuteranopia, 1,63 in protanopia), verde/ambra 2,86:1 |
| int-P2 | **regge** | «±X.XX» cambia in 26 cicli su 26 (tre livelli di rumore); «t_occ» in 17 su 26; l'etichetta 15,0 volte al secondo. Senza ritaglio: con il ritaglio il numero si ferma quando l'area satura l'ombra (non simulato) |
| int-P3 | **regge** | 39,3 % entro σ in 2D (68,3 % in 1D); raggio al 95 % con σ = 0,8 m: 1,96 m |
| int-P4 | **regge l'enunciato, va indebolita la conseguenza** | massa uniforme sul cuneo: scarto radiale 0,48–0,54 m (0,70–0,75 con la fascia, per eccesso). Notato dopo: «mai» è troppo: due grumi agli estremi del cuneo arrivano a metà del diametro, circa 0,85 m (conto a mano, non nello script). Vale quindi: la soglia d'esempio non scatta nello stato di massima ignoranza |
| int-P5 | **regge** | 27/30: copertura fra 74,4 e 96,5 %, raggio da 0,62 a 0,97 m su 0,80; 360/400: da 0,75 a 0,85 m |
| int-P6 | **regge** (con le mie ipotesi di sala) | a 6 m: etichetta larga 843–1159 punti, 2,3–3,2 volte l'ombra; tre etichette 2528–3476 punti su 1920. A 4 m e 16': 1685 punti (stanno, ma oltre metà schermo) |
| int-P7 | **prima metà regge, seconda metà smentita in un caso** | coda per oggetto, 3 oggetti: 20,2–20,4 % oltre 0,3 s (2 oggetti: 6,0 %; 1 oggetto: 0 %). Regola per settore: 1,5 % se i tre stanno nello stesso settore (regge), **10,7 % con tre settori a caso (smentita: la soglia era 5 %)**. Segnali a stato scaduto: 0,0 % in tutti i casi |

Notato dopo (esplorazione, non prevista): con l'ordine di priorità del nucleo (il visto prevale) e tre settori, 12,5 % oltre 0,3 s; con un segnale di 0,2 s più 0,05 s di pausa, 0,8 %; con la fusione dei settori in attesa in un solo segnale, 8,8 % (0,0 % con 0,2 s). Che un segnale di 0,2 s si riconosca non è verificato.

Costo del disegno (`costo_disegno.c` → `risultati_costo_disegno.txt`, misura senza previsione): campitura a righe più contorno tratteggiato su 1920×1080, 0,59 ms in media e 1,03 al massimo per quadro (C, un core, macchina condivisa); 18,3 ms se la maschera è ricalcolata punto per punto con `atan2`.
