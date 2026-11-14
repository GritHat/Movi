# Previsioni del rovesciatore (f7, corsia B) — scritte PRIMA di ogni prova

Ora di scrittura: 2026-11-14T15:08:04+01:00 (`date -Is`). Nessun programma è ancora stato scritto né lanciato.
Macchina: AMD Ryzen AI 9 HX 370, L2 da 1 MiB per nucleo, un solo thread per le misure.

Scena comune (sintetica, senza rumore): camera a 1,2 m, inclinata di 15° in basso, 87° × 58°, 640 × 480 raggi,
ritorno valido fra 0,4 e 6 m; regione 4 (larghezza) × 6 (profondità) × 3 (altezza) m; pavimento, parete di fondo a
5,5 m (variante: senza parete), pannello da 1 m a circa 1,8 m, scatola alta 0,32 m, barra a quota 1,75–1,90 m a 2 m,
piccolo oggetto in volo. Scena «peggiore»: stanza vuota con la sola parete di fondo (tutti i raggi lunghi).

## Conti a mano fatti prima (non sono misure)

- Voxel teorici: 10 cm → 40 × 60 × 30 = 72 000; 5 cm → 80 × 120 × 60 = 576 000. A 1 byte: 72 kB e 576 kB; con lo
  stato di promptMare §4 (L float32, τ uint32, q uint8, ν uint8 = 10 byte, 12 con l'allineamento): 864 kB e 6,9 MB.
- Volume del tronco di vista dentro la regione, con parete a circa 6 m: circa 40 m³ su 72, cioè circa il 56 %.
- Colonna 0,07–2,0 m sopra una cella a distanza r: il tetto del campo è 1,2 + r·tan 14° (1,51 / 1,70 / 1,95 m a
  1,24 / 2 / 3 m); senza parete, un punto a quota h < 1,2 è «visto attraverso» solo se il raggio tocca il suolo
  entro 6 m: h ≤ 1,2·(1 − r/5,88), cioè 0,95 / 0,79 / 0,59 m.

## Previsioni

**P1 — «sparso = efficiente».** Se lo spazio libero osservato si memorizza (come serve per distinguerlo dallo
sconosciuto), i blocchi 8×8×8 allocati a 5 cm sono fra il 50 e il 70 % dei 1200 blocchi della regione nella scena
demo, e di più nella scena peggiore; il risparmio di memoria sul denso è sotto 2,5 volte. Se si memorizza solo
l'occupato: 10–25 % dei blocchi, 1,5–4 % dei voxel.
*Smentita:* con il libero memorizzato, meno del 25 % dei blocchi allocati nella scena demo.

**P2 — «denso è banale».** Il costo è l'attraversamento dei raggi, non la memoria. Griglia densa, 307 200 raggi, un
thread: 10 cm → 20–70 ms a fotogramma; 5 cm → 40–150 ms (la soglia di 66,7 ms dei 15 cicli al secondo è a rischio
nella scena peggiore). Con blocchi indicizzati da una tabella hash (con memoria dell'ultimo blocco) il tempo è
1,3–4 volte quello denso.
*Smentita di «denso è banale»:* denso a 5 cm oltre 66,7 ms nella scena peggiore anche con un raggio su quattro
(320 × 240). *Smentita di «sparso è solo complicazione»:* hash più veloce del denso, oppure memoria sotto un terzo
del denso con il libero memorizzato.

**P3 — «la mappa aggiunge falsi liberi di discretizzazione».** Fra i voxel che l'attraversamento dei raggi etichetta
«libero» (attraversato da almeno un raggio valido, mai colpito), quelli con almeno un sotto-punto su 64 NON
osservato libero (in ombra, fuori campo, ritorno non valido) sono il 5–20 % a 10 cm e il 3–12 % a 5 cm; quelli che
intersecano materia vera della scena sono più di zero (0,05–1 % a 10 cm).
*Smentita:* quota mista sotto l'1 % a 10 cm, oppure zero voxel «libero» con materia a entrambe le risoluzioni.

**P4 — il «libero» del nucleo è un'affermazione sul suolo, non sulla colonna.** Nelle celle che la regola del nucleo
dà «libero» fra 1,24 e 3 m, la quota della colonna 0,07–2,0 m attraversata da un raggio con ritorno valido più
lontano è: con la parete di fondo a 5,5 m, in media 80–95 %; senza parete (ritorni validi fino a 6 m), in media
30–50 %, con minimo sotto il 30 % a 3 m. La cella sotto la barra a quota 1,75–1,90 m (a 2 m) esce «libero» nel
nucleo e «non osservato» a quella quota nell'interrogazione 3D.
*Smentita:* media ≥ 95 % senza parete, oppure la cella sotto la barra non è «libero» per la regola del nucleo.

**P5 — «senza posa la mappa che accumula è più pericolosa».** Integrando un fotogramma con un errore d'imbardata δ
non compensato, i voxel che contengono materia vera e ricevono solo evidenza di «libero» crescono, rispetto a δ = 0,
di almeno 3 volte a δ = 1° e di almeno 5 volte a δ = 2° (5 cm). I voxel colpiti al fotogramma 1 (δ = 0) che al
fotogramma 2 (δ = 1°) ricevono solo evidenza di «libero» sono più di 500.
*Smentita:* aumento sotto 1,5 volte a 1°.

**P6 — l'alternativa senza mappa costa poco.** L'interrogazione di visibilità per fasce di quota sulla griglia polare
(87° × 18 anelli × 39 quote da 5 cm = circa 61 000 letture dell'immagine di profondità) costa meno di 2 ms a
fotogramma, e la sua memoria è la sola immagine di profondità (640 × 480 × 4 byte = 1,2 MB, o 614 kB a 16 bit).
*Smentita:* oltre 10 ms.

## Che cosa condividono le prove con ciò che controllano

Lo stesso autore (io), lo stesso modello di camera ideale (foro stenopeico, niente rumore, niente pixel misti ai
bordi, niente vetro), la stessa scena. Valgono per la geometria e per l'ordine di grandezza dei costi su questa CPU,
non per un sensore vero. P4 dipende dall'ipotesi «oltre 6 m il ritorno non è valido»: sul sensore vero non
verificato.

## Aggiunta, scritta alle 2026-11-14T15:17:06+01:00, dopo le prove P1–P6 e PRIMA della prova P7

(Le prove P1–P6 sono già state lanciate: i loro esiti sono in `risultati_analisi_prima.txt`, `risultati_analisi.txt`,
`risultati_tempi.txt`, `risultati_tempi_2.txt`. Questa previsione nasce da ciò che ho visto lì: il costo sta
nell'attraversamento dei raggi, circa 7 ns a voxel visitato.)

**P7 — memoria del solo occupato, senza attraversare i raggi.** Inserire nella griglia densa a 5 cm i soli punti
d'arrivo dei raggi validi (un byte di stato e un'età per voxel, 307 200 pixel, un thread) costa meno di 5 ms a
fotogramma nella scena demo e nella peggiore; il controllo «questo voxel occupato ricordato è ora visto attraverso?»
(una lettura dell'immagine di profondità per ciascun voxel occupato) costa meno di 1 ms.
*Smentita:* inserimento oltre 20 ms, oppure controllo oltre 5 ms.

## Seconda aggiunta, scritta alle 2026-11-14T15:18:15+01:00, dopo P7 e PRIMA delle prove P8 e P9 (i falsificatori delle due proposte)

Conto a mano fatto prima: il tetto del campo a 3 m è 1,2 + 0,249·3 = 1,95 m, sotto i 2,0 m: nessuna cella entro 3 m
può avere la colonna 0,07–2,0 m tutta osservata. Il falsificatore usa quindi la colonna fino a 1,5 m.

**P8 — falsificatore di rovesciatore-1 (la lettura per fasce dice qualcosa o dice sempre «non osservato»?).** Fra
le celle che il nucleo dà «libero» fra 1,3 e 3 m, quelle con la colonna 0,07–1,5 m tutta osservata-libera (150
campioni da 1 cm al centro della cella) sono: con la parete a 4 m almeno il 60 %; con la parete a 5,5 m fra il 30 e
il 60 %; senza parete meno del 30 %. *Smentita della proposta:* meno del 20 % con la parete a 4 m (la lettura
direbbe «non osservato» quasi ovunque e non aggiungerebbe niente al messaggio).

**P9 — falsificatore di rovesciatore-2 (la regola di rilascio dell'occupato ricordato).** Nello stesso fotogramma
in cui sono stati inseriti, i voxel occupati che risultano «visti attraverso» sono 189 su 5950 se si guarda il solo
centro (già misurato in P7: la regola col solo centro è smentita); chiedendo che TUTTI i 64 sottopunti siano
osservati-liberi sono al più 5 su 5950 nella scena demo e al più 5 nella peggiore. *Smentita:* più di 30.
