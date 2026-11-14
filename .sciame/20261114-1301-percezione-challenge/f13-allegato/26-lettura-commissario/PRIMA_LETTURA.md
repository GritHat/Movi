# Prima lettura a freddo del PDF (sciame-lettore, f13)

Scritta alle 19:32 del 14 novembre 2026 (`date -Is`: 2026-11-14T19:32:14+01:00), dopo aver letto solo
`20-unione/allegato_tecnico.pdf` (pdftotext -layout, 69 pagine, più le pagine 6-9, 10, 24, 35, 40, 53 come immagine) e
il registro di LaTeX per i difetti di forma. Nessun altro file aperto prima: né il contratto, né NOTE.md, né SCELTE.md,
né i fascicoli. I conti di controllo fatti finora sono a mano, sul solo testo del PDF.

## 1. Che cosa ho capito (dieci righe)

Una camera di profondità ferma guarda il suolo fino a 3 m. A ogni fotogramma il suolo è diviso in celle polari con
quattro stati; «libero» è scritto solo se il fotogramma corrente legge il suolo in metà dei pixel della cella e delle
otto vicine. I punti sopra il suolo fanno gruppi, un filtro di Kalman a velocità quasi costante li segue. Quando una
persona seguita sparisce dietro un ostacolo, il sistema accende un'area d'avviso (ombra più 0,40 m) che non si spegne a
tempo, e mostra una regione di previsione fatta con 400 percorsi campione, con un livello «almeno 9 su 10 fino a 2 s».
Davvero provato: teoremi nel modello (mai «libero» dove non si vede; contenimento; fascia), molti conti di geometria,
simulazioni con un sensore ideale (posizioni con rumore gaussiano) per continuità e copertura, simulazioni su
profondità sintetica per identità e gruppi, e un filtro provato su traiettorie pubbliche. Mai un sensore vero. Il
sistema descritto non è mai stato eseguito tutto insieme: la regione persistente gira solo sul sensore ideale, la
catena su profondità sintetica ha ancora uno stato «perso»; il classificatore non esiste; la fascia di 0,40 m copre
1,13 m/s, meno del passo d'uomo.

## 2. Voti (da 1 a 10)

- Chiarezza del problema: 8. Introduzione, figura 1 e riquadro dei limiti dicono subito che cosa si fa e che cosa no.
- Correttezza e rigore: 7. I conti che ho rifatto tornano quasi tutti; ma α è usato in tre sensi, Π e W sono scambiati
  nel capitolo 6, e alcune frasi di sintesi sono più forti delle proposizioni che citano.
- Onestà sui limiti: 9. Raramente si vede un documento che scrive i propri zeri mancati; a tratti però i limiti sono
  così tanti che non si capisce quale sia il sistema finale.
- Riproducibilità: 5. Formule e parametri ci sono; mancano le scene, le disposizioni G1-G3, il generatore di
  camminate, il simulatore «da scheda», i semi e qualunque rimando a programmi o dati.
- Completezza: 8. Copre tutto; pecca semmai per eccesso (alternative scartate, prove di varianti precedenti).

## 3. Dove mi sono fermato

Simboli e termini
1. α: nella tavola dei simboli e nella tabella 1 il livello è 1 − α (= 0,90); in §4.4, §5.5 (α = 0,9, R_0,9), §7.5 e
   appendice A (α = 0,90) α è il livello; in §6.3 α è il livello di significatività di una prova (0,05); in §6.4 è di
   nuovo il complemento.
2. Π e W: §5 dice che Π è il riferimento teorico e W l'area d'avviso; la Definizione 6.1(e) scrive «area d'avviso Π(t)»
   e la tabella 23 «Soggetto nascosto fuori da Π». §7.5 dice che il sistema «mantiene Π(t)».
3. «suolo» in due sensi: il terreno, e (Prop. 6.8 «Suolo per comportamento peggiore», §5.5 «se scatta il suolo»,
   tabella 19 «regione persistente con suolo», Def. 5.9 «(suolo)») una soglia minima di ripiego. Alla prima lettura
   «se scatta il suolo» non si capisce.
4. «cella»: cella della mappa e, da tabella 20 in poi, combinazione (disposizione, comportamento, τocc). La
   definizione del secondo senso è in §6.1, dopo l'uso in §5.6. La tabella 2 dice «combinazioni».
5. «tenuta» (tabella 18, §8.7, appendice A) non è definita: si intuisce che sia ∆, il ciclo in cui l'uscita resta in
   uso.
6. «non confermato» (§5.3, tabella 35) è lo stato di una traccia confermata rimasta senza misura: il nome dice il
   contrario.
7. La stessa cosa con quattro nomi: «gruppi a celle forti» (§4.2), «gruppi dalle celle forti» (tab. 28-29),
   «raggruppamento per picco» (tab. 38, §8.8, app. A), «gruppi e riaggancio modificati» (tab. 3, §9). Idem «marca
   tagliato» (tab. 27) e «bordo di profondità riconosciuto» (tab. 20); «traccia pendente» (§4.9) e «traccia in
   previsione» (§5); T_w (§4.2) e W (§8.9) per la finestra di 0,867 s; «parametri di partenza», «catena di partenza»,
   «parametri di base», «regola di partenza».
8. k: coefficiente del rumore (§2, §3), passo di sottocampionamento (§7), numero di eventi (§6), indice di statistica
   d'ordine, moltiplicatore di σ. z: coordinata in avanti e, in (11), profondità attesa z0(p). W: area d'avviso,
   larghezza dell'immagine (§7.1), finestra (§8.9). c: cella, centro, byte per voxel.
9. Segno dell'errore d'inclinazione: in §2.5 il caso pericoloso è +1°, in §3.5 (Controesempio 3.9) e §6.6 è −1°; in
   §8.8 punto 7 compaiono tutti e due nella stessa riga. La convenzione non è detta.
10. Risoluzione: tabella 4 a 848 × 480 e 30 fotogrammi al secondo; prove da scheda a 424 × 240; regola del «libero» a
    320 × 240; costo a 640 × 480; il ciclo è a 15 Hz. Che il ciclo usi un fotogramma su due si legge solo
    nell'appendice A.

Passaggi saltati
11. §4.2: «le prove sono al più 13 per asse» e «finestra massima T_w = 13∆»: la Definizione 4.3 ammette k − j fino a
    1/∆ = 15. Da dove viene 13?
12. Tabella 14, colonna «Prova singola»: con le formule della Proposizione 4.4, T_w = 0,867 s e σ a 3 m ottengo 0,816
    (pessimista) e 0,389 (severa), non 0,853 e 0,371. Non so rifare la colonna.
13. Osservazione 3.7(iii): «un margine di 0,33 m (per 1,4 m/s)» con finestra d'uso 0,20 s: 1,4 × 0,20 = 0,28. Quale
    tempo dà 0,33?
14. Lemma 3.8: «114 su 200 e 162 su 200»: quali sono i due casi?
15. §5.5: «3 lisciature» (di che cosa, con quale nucleo), «raggio da tabella» (quale tabella), «400 percorsi
    registrati» (registrati da chi: sembrano registrazioni reali, poi §6.5 fa capire che vengono dal simulatore);
    appendice A: «almeno 200 percorsi, due persone, tre andature» sembra un'altra libreria.
16. Tabella 18: da dove viene l'età del dato 0,133 s («3 fotogrammi») se la regola del «libero» ha memoria zero? E la
    latenza è 0,150 s nella prima riga, 0,155 nelle altre.
17. §8.9: «la conferma su tre fotogrammi vale solo sotto 0,375 m/s» senza conto.
18. §5.6 lettura (6): «lo "0 su 11,9 milioni di istanti" non è una misura del sistema» cita una cifra che compare solo
    dopo, in tabella 23.
19. Osservazione 5.14: il «criterio a due stadi su 30 passaggi» non è presentato: di chi è, perché lo si discute?

Cifre senza termine di paragone o non riconciliate
20. «Nascosto fuori dall'avviso» su profondità simulata: 0 su 4324 e 0 su 3608 (tab. 2, §9); 0 e 0 su 3921 e 3922 (tab.
    23); 0 su 336, 169 e 2360 (tab. 38); 0 su 264 (§6.6). Sono prove diverse? Nessuna riga le mette insieme.
21. 2 907 032 celle·fotogramma: «131 sequenze» (tab. 2, tab. 23) o «135 sequenze» (§3.6)?
22. Tabella 3, «Ostacoli fermi»: «cassa alta 1 m a 1,68 m, 84 fotogrammi su 84; scatola a 2,0 m, 10 su 10»: nel
    capitolo 6 (tab. 29) trovo 190 su 190 e nessuna cassa. Il requisito «5 prove su 5 fra 1,1 e 3 m» della tabella 1
    non ha un esito.
23. Tabella 3 «uscita osservato con il soggetto nascosto in 8 passaggi su 90, poi 1 su 140»; §4.9 «riagganci a persona
    ancora nascosta da 11 e 6 a 1 e 1 su 140». Stessa grandezza?
24. §4.2 «pannello mobile in 0 passaggi su 140 (130 e 94 con i gruppi della Definizione 4.2)»: 130 e 94 su quanti?
25. §8.8 punto 9: 1568 + 2983 = 4551, il totale scritto è 4552; 1584 + 2968 = 4552, il totale scritto è 4553.
26. §7.4: «9 dei circa 25 tipi della tassonomia del §4», ma la tabella 15 ha 15 tipi; «carrozzina» non compare nel §4.
27. Tabella 20 e tabella 27 danno numeri diversi per condizioni che sembrano le stesse (bordo riconosciuto: 0,998 e
    1,000 contro 0,996…0,928; chi parte da fermo: 0,146/0,049/0,043 contro 0,11/0,16/0,26).
28. Tabella 26: 2400 passaggi per comportamento in G2 e G3 e 4000 in G1 fanno 44 000; il totale dichiarato è 23 402.

Capitoli che presuppongono altro
29. Due definizioni di «occupato»: Def. 3.1(i) (tre pixel fra 0,07 e 2,0 m) e Def. 4.2 (in più «è il primo ritorno
    lungo il suo azimut»).
30. Due regole di riaggancio: §4.9 (condizioni a-f, fascia 0,40 o 0,75 m) e §5.5 (entro w da R_0,9 ed entro 0,75 m).
31. R_α definita due volte: Def. 5.9 (celle più dense della libreria) e §6.4 (posizioni con punteggio sotto la soglia).
    §6.4 non dice che descrive un metodo non adottato.
32. Appendice A: «raggruppamento per picco (opzionale)», «avviso senza traccia (opzionale)». Le cifre di testa (24 su
    23 402; 176 su 180) dipendono da regole opzionali: fanno parte del sistema o no?

Frasi che mi fanno credere più del dimostrato
33. Sommario e §9: «0 interruzioni su 23 402 passaggi». In 928 di quei passaggi (24 con la regola opzionale) la
    traccia è chiusa prima dell'ombra e la regione non c'è mai: lo zero è condizionato all'ingresso.
34. §9, primo punto: «una cella dichiarata libero è priva di superfici fino al suolo, se ... la posa è nota entro la
    tolleranza». La Proposizione 3.6(b) vale a posa esatta (ε_p = 0) e solo per i raggi dei pixel che leggono il
    suolo, non per la cella (Oss. 3.7 ii).
35. §9: chi svolta o esce lontano «fra 0,57 e 0,86»: è la serie migliore (corpo esteso); l'altra serie dà 0,13–0,70
    (tab. 2, tab. 27).
36. §6.6 dopo la tabella 28: «con il modello ideale, l'avviso viene rilasciato insieme all'identità» sembra descrivere
    il sistema adottato; §5.6 dice che è la variante scartata.
37. §7.5: «per ciò che non è mai stato visto mantiene un insieme di possibile presenza Π(t)»; §5.2 e §5.4 dicono che
    un'ombra in cui non è entrata alcuna traccia non porta avviso.
38. §9: «(Proposizione 4.7) [C]» per l'accelerazione: la 4.7 è la massa.

## 4. Le cinque domande agli autori

1. Qual è, esattamente, il sistema che dichiarate? Quali regole «opzionali» ne fanno parte, e quale singola
   esecuzione le contiene tutte? Mi pare nessuna.
2. La fascia di 0,40 m copre 1,13 m/s, ma le prove usano ingressi fino a 1,8 m/s e la classe «persona a piedi» ha
   v_max 2,5 m/s: su quale base l'area d'avviso è detta sicura per una persona che cammina?
3. Il livello «almeno 9 su 10» è misurato con libreria e passaggi dello stesso generatore e con il bordo dell'ombra
   esatto; con il bordo stimato cade a 0,30–0,46. Che cosa dichiarerete davanti al sensore?
4. Perché la continuità non è stata eseguita su profondità simulata, dove la catena ha ancora lo stato «perso»?
5. Il simulatore «da scheda» produce il 7,8 % di pixel senza dato contro 24–34 % delle registrazioni: quali risultati
   del tipo (II) sopravvivono al 30 % (la resa del «libero» scende al 45–63 %)?

## 5. Che cosa manca per rifare i conti principali

Geometria di G1, G2, G3 (posizioni di ostacolo, percorsi, portata); parametri del generatore di camminate e dei sette
comportamenti; le dieci scene della regola del «libero»; il modello del simulatore da scheda (pixel misti, pixel senza
dato); nucleo e griglia delle «lisciature»; la tabella dei raggi del predittore di ripiego; quali registrazioni
dell'insieme pubblico; i semi; dove stanno programmi e dati. L'appendice B dice che cosa si rifà «dal solo testo»: sono
i conti a mano, non le simulazioni.

## 6. Che cosa toglierei

Proposizione 4.1 (ordine della catena); Lemma 6.9 e metà di §6.5 (basta una frase); §5.7 (tre indicatori di varianti
scartate) e Oss. 5.14; il paragrafo «Lettura di un punto nell'immagine di profondità» in §3.7 (non è nel sistema);
§2.6 e la riga dei sensori laterali; metà della tabella 34. Le tabelle 2-3 ripetono le 19-30: tenerle, ma con le
stesse cifre. Il controesempio a +1° è raccontato quattro volte (§2.5, §3.3, §3.6, §8.8).

## 7. Più mani?

Sì. Capitolo 2: gradi scritti «87°», riferimenti «figura 2», «tabella 5» minuscoli, «Limiti di validità» in corsivo
nel testo. Capitoli 3-5: «58◦» in formula, «Tabella», «Figura» maiuscoli. Capitolo 6: «Che cosa il risultato non
dice», tipi (I)(II)(III) invece di «ideale» e «da scheda», Π al posto di W, «misure mancanti» al posto di «pixel non
validi», «maschera di verità» al posto di «maschera di riferimento». Capitolo 7: simboli propri (k, c, W, T). Capitolo
8: «raggruppamento per picco», «portatore». I nomi diversi sono al punto 7 del §3.

## 8. Forma

Nessuna riga fuori margine nel registro (0 «Overfull»). Tabelle 23-30 e 34 in corpo molto piccolo, leggibili ma
fitte. §8.1: «Con la geometria del capitolo 2 9 settori su 17» (due numeri attaccati). §3.7: «[C]; il secondo enunciato
[S]» dopo il punto. §4.8: «Consistenza del filtro.» è un titolo finito in mezzo al capoverso; idem «Livello di prova.»
in §8.3. §3.3: «(b) [D] nel modello delle tre ipotesi, [N].» monco. §8.9: «[D] (§2)» rimando spurio. Figura 3 e
tabella 7/8 affiancate: didascalie strette. Frontespizio: «Autori: [nome della squadra]» è un segnaposto.

## Previsioni scritte prima dei controlli sulle fonti (19:32)

- P1. Le potenze e le numerosità della tabella 22 e i percentili Beta di §6.4, rifatti da me, tornano entro
  l'arrotondamento. Smentita: uno scarto oltre un'unità sull'ultima cifra.
- P2. La colonna «Prova singola» della tabella 14 non si ottiene dalla Proposizione 4.4 con T_w = 0,867 s (attesi
  0,816 e 0,389). Smentita: il fascicolo della stima dà la formula e i parametri con cui 0,853 e 0,371 tornano.
- P3. I 2 907 032 celle·fotogramma sono su 135 sequenze, e 131 è il sottoinsieme a filtri spenti. Smentita: la fonte
  dice 131 per il conteggio.
- P4. La regola «avviso senza traccia entro 0,75 m» (da 928 a 24) è nella soluzione finale come regola adottata, non
  opzionale. Smentita: SOLUZIONE_V3 la dà come interruttore spento di norma.
- P5. NOTE.md e SCELTE.md conoscono già α, Π/W e i nomi dei gruppi. Smentita: non li nominano.

## Rettifiche aggiunte dopo (19:39), senza toccare il testo sopra

- In testa ho scritto di aver guardato come immagine «le pagine 6-9, 10, 24, 35, 40, 53»: le avevo prodotte, ma ne
  avevo guardate tre (pagine del PDF 8, 11 e 41, cioè le numerate 7, 10 e 40). Dopo ho guardato anche le pagine del
  PDF 12, 14 e 32 (figure 2, 3 e 6): leggibili. Punto nuovo nato lì: la figura 3 chiama g la larghezza della fascia di
  guardia, che nel resto del documento è w.
- Non avevo scritto la cosa più ovvia per chi ha quaranta minuti: 55 pagine di corpo non si leggono in quel tempo. Il
  contratto (letto dopo) ne chiede una trentina; NOTE.md lo dichiara già.
