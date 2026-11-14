# Schermo, segnali e copione della demo — `sciame-interfacce`, f12 (05-schermo), 14 novembre 2026

Sigle: **VN**, **V7**, **V8**, **V9** i verdetti di f4, f7, f8, f9; **AS** l'attacco alla specializzazione; in f8, **Vis** `06-visualizzatore/CONSEGNA.md`, **St** `15-statistica/ANALISI.md`, **M** `13-soluzione/MODIFICHE_CONTINUITA.md`; **[int.]** conto o prova mia (`risultati_schermo.txt`). Il verdetto di f10 non esiste (`ls`): ciò che cito da f10 è **preliminare**.

## 0. In testa

**Tutto resta simulazione, conto o progetto. Nessuna persona ha guardato lo schermo, ascoltato un suono o letto il tabellone: ogni «si legge» qui sotto è non verificato.**

**Prova nuova [int.]:** il codice dello statistico di f8, copiato, con una geometria `E` e una banda di passo in più (due righe; lancio di controllo uguale al suo file). 400 semi nuovi, `sd-1`, soggetto puntiforme, maschera esatta, senza c1–c8; un codice, un autore.
1. **«Con un'ombra larga la zona è stretta fino a 3 s» (V8 §6.6) non vale alla scala della demo.** T e L hanno il soggetto a 4 m e la portata a 6 m (`gen.h`). Con il pannello largo 2 m a 1,9 m, l'attore a 2,3 m, la portata di 3 m e il passo a 0,8–1,0 m/s: zona al 55 % dell'ombra a 1 s e all'87 % a 2 s; 84 passaggi su 400 scartati per meno di 4 misure prima dell'ombra (546 su 2000 sul percorso); dentro la zona, sul percorso, 1128 su 1275 = 0,885 [0,866; 0,901] a 2 s e 0,864 [0,843; 0,883] a 3 s, sotto il livello dichiarato. Stato proposto: **controesempio in simulazione** alla scelta «pannello da 2 m».
2. **K-111, «0,45 s di vista per lato» conta solo il campo.** Con la portata di 3 m il corpo è in vista per intero 0,12–0,27 s per lato a 1,0 m/s: 2–4 fotogrammi a 15 Hz, contro i 4 della condizione 6 di VN. *Conto in pianta.*
3. **Pannello da 1 m a 0,45–0,55 m/s:** 0 scartati su 2000; zona al 52 % dell'ombra a 1 s, tutta l'ombra a 2 s; dentro la zona 0,996 / 0,984 / 0,968 a 1 / 2 / 3 s (limiti inferiori 0,992 / 0,978 / 0,960); 0 passaggi con un vuoto. **Sostenuto dai dati in simulazione.**

**Incoerenze fra i verdetti.** `interfacce-K1`: M §2.7 mette una croce in «previsto ampio», c8 la toglie, V8 §6.1 promette «un segno e una zona»: propongo la targhetta del §1. `interfacce-K2`: fra 2 e 3 s V8 §4.8 scrive «almeno 8 su 10», V8 §6.2 «almeno 85 su 100»: propongo ovunque la seconda.

**Scostamenti.** Previsioni scritte alle 17:50:39, dopo la lettura dei verdetti e conti a mente: P-int-4(b) e la soglia in parole di P-int-6 **smentite**; le altre reggono. Letture parziali e file non letti: elenco in `PREVISIONI.md`. Regole violate: nessuna che io sappia.

## 1. Lo schermo

**Disposizione.** In alto, su tutta la larghezza, la riga fissa della sorgente (§4). A sinistra la pianta dall'alto, sensore in basso, archi a 1, 2 e 3 m. A destra, dall'alto: la banda del livello; una riga per traccia; il tabellone (§3); le ultime cinque righe del registro. Al piede: «età del dato 0,07 s · ritardo: non misurato · calcolo 1,1 ms per ciclo».

**Regole generali.** Ogni distinzione sta nella forma, nella trama e nella parola; il colore, se c'è, ripete soltanto, e non è mai verde (V9, S5). Tratti di almeno 1,5 px (Vis). Un decimale; scritte che cambiano al più 2 volte al secondo (V9; il 2 è mio). L'età è misurata, mai «0 ms».

**I segni** (aspetto in bianco e nero; quando compare → cambia → sparisce; parole esatte).
- **Suolo visto libero** — bianco. Cella letta libera in questo fotogramma (V7, correzione a); sparisce appena manca il dato. «visto libero ora».
- **Occupato** — nero pieno, finché è visto. «occupato (visto)». **In ombra** — righe oblique rade, dietro un occupato, finché il suolo non è rivisto. «in ombra: non visto». **Non osservato** — puntini: fuori campo, oltre 3 m, buco, sotto 1,24 m; mai tolto per memoria. «non osservato».
- **Possibile presenza** (cuneo più 0,40 m) — quadrettato fitto, bordo spesso. Compare quando la traccia entra nell'ombra (M1; c4, dopo due cicli senza misura; c7, traccia chiusa entro 0,75 m da un'ombra: non provata). Cresce solo l'età. **Sparisce solo guardando**, cella per cella: mai per un timer, per la previsione o per una conferma dell'operatore (decisione 3 di V9: all'utente). «POSSIBILE PRESENZA · da 4 s».
- **Oggetto visto** — disco pieno di taglia fissa, scia piena; solo con una misura nel ciclo. «P1 VISTO · 2,1 m».
- **Visto in parte** (c6, non provata) — contorno pieno delle celle del gruppo tagliato dal bordo dell'ombra, senza freccia: non è una misura. «VISTO IN PARTE».
- **Previsto** — anello vuoto di taglia fissa; zona a righe fitte con bordo tratteggiato, ritagliata su ombra più 0,20 m; scia tratteggiata. Compare al primo ciclo senza misura di una traccia entrata nell'ombra. La zona cresce, mai su suolo visto libero oltre la fascia. **Non sparisce finché la traccia è pendente:** diventa «ampio». «P1 PREVISTO · almeno 9 su 10 qui dentro · larga 0,8 m · non visto da 1,2 s»; fra 2 e 3 s «almeno 85 su 100».
- **Previsto ampio** — la zona è tutto il non visto dell'ombra, a righe rade, bordo a punti grossi; niente croce (c8); una targhetta «P1» fissa sul bordo vicino dell'ombra, che non è una posizione. Scatta quando la zona supera l'80 % delle celle d'ombra, oltre 3 s, con ingresso sotto 0,3 m/s (c5), con profondità o posa degradate. Sparisce solo per una chiusura dichiarata. «P1 PREVISTO AMPIO · dietro l'ostacolo o fuori area · da 3,4 s».
- **Ricomparsa** — disco pieno, più il segmento fra punto previsto e prima misura per 0,5 s; la scia resta tratteggiata. «P1 RICOMPARSO · scarto 28 cm».
- **Non ricomparso** — riga sotto la targhetta, passato il tempo d'uscita atteso. «non ricomparso da 6 s (dedotto): fermo dietro l'ostacolo oppure uscito dal lato non visibile».
- **Identità ambigua** — disco «P2?» per una misura fuori porta, o con più tracce pendenti nella stessa ombra (c2: un solo avviso); la zona di P1 resta finché non si guarda l'ombra. «P2 · identità ambigua».
- **Affidabilità persa** — cornice spessa, pianta a puntini, parola grande: nessun fotogramma nuovo, pixel validi sotto soglia, inclinazione cambiata (V7, c ed e). Le tracce restano come zone «dedotto, sensore non affidabile»; al ritorno le zone sono dilatate e ogni riaggancio è «identità ambigua». «AFFIDABILITÀ PERSA · sensore coperto · ultimo dato valido da 2 s».

**Chiusure dichiarate** di una traccia in ombra (M §2.5, elenco chiuso), scritte nel registro: riagganciata; identità ambigua; ombra vista libera; affidabilità persa (zona «non aggiornata»); fuori dall'area osservata (non toglie l'avviso: V8 §4.9, da provare). **Banda del livello** (V9, S8: dichiara, non comanda): «NESSUN OSTACOLO OSSERVATO FINO A 2,7 m» (cornice sottile); «ATTENZIONE» (cornice spessa: occupato o mobile nella zona valutata); «ZONA NON VERIFICATA» (a righe: possibile presenza o buchi); fuori scala «AFFIDABILITÀ PERSA» (bianco su nero). L'ordine fra «zona non verificata» e un mobile in avvicinamento è aperto (K-306): finché lo è, la banda li mostra tutti e due.

**Schermata d'avvio.** «Non misuro: a meno di 1,24 m di distanza dal sensore; oltre 3 m; fuori dal campo; il vetro; ciò che è più basso di 0,4–0,7 m e più vicino di 0,8–0,5 m. Dietro un ostacolo più basso del sensore perdo chi è ancora in vista. Seguo una persona sola per ostacolo.» Sotto, l'esito del controllo all'avvio (VN, condizione 1). **Registro**, una riga per evento con «come lo so» (V7 §2; logica non provata sul nucleo): `14:02:07 · P1 · scomparso dietro l'ostacolo · DEDOTTO`; `P1 · ricomparso · OSSERVATO · scarto 28 cm`.

## 2. Il canale sonoro (secondo profilo: avviso di presenza per una persona non vedente ferma)

Segnali di 0,3 s, uno per cambio di stato; la frase «direzione, distanza, stato» solo a stato stabile (correzione C11 del nucleo; M §2.7). Se due eventi cadono insieme suona il primo di questa lista (ordine del blocco B7 del nucleo fino al 4, il resto è mio; 2 contro 3 è K-306, aperta): (1) affidabilità persa, ripetuta finché dura; (2) oggetto visto in avvicinamento; (3) scomparso dietro l'ostacolo; (4) previsto ampio, poi non ricomparso; (5) ricomparso; (6) identità ambigua; (7) la frase. All'avvio, a voce: la sorgente dei dati (§4) e «il silenzio non vuol dire che non c'è nessuno».

**Non si promette:** niente per chi cammina (AS, C6); che il silenzio significhi assenza; una posizione precisa dal suono; che i segnali si distinguano (la prova con tre persone bendate, almeno 54 risposte giuste su 60, non è fatta); un ritardo sotto 150 ms (155 ms stimati, non misurati: VN); niente sull'anello cieco né su una seconda persona nella stessa ombra. **Limite:** se il programma o l'audio si fermano, il canale tace come quando non c'è niente; il battito continuo che lo coprirebbe è «dopo l'hackathon» (M: non verificato).

## 3. Il tabellone della precisione misurata sul posto

```
PRECISIONE MISURATA QUI · occlusione virtuale · CAMERA DAL VIVO
La persona era dentro la zona tratteggiata?    dentro    intervallo al 95 %   zona larga
 dopo 1 s non vista · prosegue                 27 su 30  fra 74 e 97 su 100   0,8 m
 dopo 2 s non vista · prosegue                  k su n   fra .. e .. su 100   .. m
 dopo 2 s non vista · si ferma o torna          k su n   fra .. e .. su 100   .. m
 «previsto ampio» (a parte, non fa punteggio)   k su n passaggi
 passaggi del giurato                           k su n   (sotto 10: solo il conto)
ultimo passaggio: DENTRO · scarto 28 cm · zona larga 0,8 m · non visto 1,7 s
n fissato prima: 50 per riga · taratura esclusa · nessun azzeramento
```

**Come si legge** (St §6; V8 §4.8; intervalli di Wilson ricontati [int.]). L'evento è «la persona era dentro la zona a 1 s e a 2 s», con l'occlusione virtuale: la persona resta in vista e fa da verità (M §2.3: mai eseguita). **27 su 30 dice «fra 74 e 97 su 100»**: è compatibile con 9 su 10 e non esclude 3 su 4. Per dire «almeno 8 su 10» servono 46 su 50 (limite 0,812; con 45 è 0,786). 30 su 30 dice «almeno 89 su 100», non «sempre». La larghezza sta sempre accanto al conto: una zona enorme è sempre giusta. I passaggi di una stessa persona si somigliano (St: 40 ne valgono circa 14): la cifra descrive queste persone in questa stanza.

## 4. La riga fissa: sorgente e configurazione

Sempre in alto, bianco su nero, mai coperta; uguale in ogni riga esportata del registro e in ogni schermata salvata (V9, S1). Tre sorgenti, parole esatte: «SORGENTE: DATI SIMULATI · sensore simulato da scheda (D435i, 424×240)»; «SORGENTE: REGISTRAZIONE PUBBLICA · THÖR, traiettorie da cattura del moto: non è una camera di profondità · occlusione creata a programma»; «SORGENTE: CAMERA DAL VIVO · [modello] · fotogramma 18 204», che compare solo se il contatore del sensore vero avanza. Segue la configurazione, scelta all'avvio e ferma in esercizio: «camera ferma 1,2 m, 15° in basso · mappa 1° × 0,1 m fino a 3 m · 15 Hz · filtri della camera spenti · previsione sd-1 · controllo all'avvio superato alle 14:02».

## 5 e 6. Il copione della demo, con il requisito della traccia per ogni atto

**Geometria fissa** (VN, condizione 3; V7 §2; AS, C3): camera ferma a 1,2 m da terra, 15° in basso; pannello **alto almeno 1,7 m**, a 1,7–1,9 m di distanza; attore sulla linea a 2,3 m; **una sola persona dietro il pannello**; casse fuori dalla linea dell'attore; al chiuso; passo non oltre 1,4 m/s.

**La larghezza (K-111): propongo il pannello da 1 m a passo lento; decide l'utente.**

| | **A. Pannello 1 m, passo 0,5 m/s** | **B. Pannello 2 m, passo 0,8–1,0 m/s** |
|---|---|---|
| Ombra sulla linea dell'attore | 1,2–1,35 m | 2,4–2,7 m |
| Corpo nascosto per intero | 1,5–1,8 s | 2,0–2,8 s |
| Corpo in vista per intero, per lato | 1,6–1,7 s | 0,12–0,27 s a 1,0 m/s |
| Passaggi senza le 4 misure prima dell'ombra | 0 su 2000 | 546 su 2000 |
| Zona su ombra a 1 / 2 / 3 s (prosegue) | 0,52 / tutta / tutta | 0,55 / 0,87 / 0,98 |
| Dentro la zona, sul percorso, a 1 / 2 / 3 s | 0,996 / 0,984 / 0,968 | 0,941 / 0,885 / 0,864 |

**Che cosa vede il giurato in A:** per quasi 1 s «visto in parte»; anello e zona che cresce fino a metà ombra in 1 s; fra 1 e 2 s «PREVISTO AMPIO» su tutta l'ombra; dopo circa 3 s senza misura torna il disco, con uno scarto di circa 0,5 m, che si mostra. **In B:** l'attore entra e sparisce quasi subito; in un passaggio su 4–5 nessun anello e nessuna zona; quando parte, la zona copre metà ombra a 1 s e quasi tutta a 2 s; all'uscita l'attore lascia l'area osservata dopo 0,5 m, e lo scarto si vede di rado (129 ricomparsi su 316).

Righe 1–3: conto in pianta [int.], coerente con V7; le altre e lo scarto: simulazione [int.]. Con il pannello da 1 m a passo normale (1,0–1,4 m/s) la zona è già l'84 % dell'ombra a 1 s e il corpo è nascosto 0,54–0,90 s: troppo poco. Il pannello da 2 m a 0,5 m/s tiene il livello (0,975 / 0,931 / 0,911) con la zona a 0,44 / 0,66 / 0,85 dell'ombra, ma perde 505 passaggi su 2000 prima dell'ombra e l'attore non ricompare nell'area osservata (1 su 341): non lo propongo. **La frase vera per A:** «in questa stanza la previsione localizza per circa un secondo, poi dice che la persona è ancora dietro» (V8 §6.6, c8). La zona stretta per 2–3 s esiste solo nelle simulazioni a 4 m con portata 6 m: si può mostrare come filmato, con la riga «DATI SIMULATI». Difetto visibile in A: il punto arretra in 84 passaggi su 400 (soglia di V8: 5 %).

**Apertura (30 s).** «Questo è un prototipo fatto in 14 ore. La riga in alto dice in ogni momento da dove vengono i dati. Le cifre di precisione che citiamo vengono da simulazioni, a camera ferma, con una persona sola. L'unica cifra misurata qui è quella del tabellone, e la leggiamo con il suo intervallo. Vi diciamo prima dove il sistema cede.»

**Gli atti** (in corsivo il requisito della traccia che ciascuno mostra).
1. **Ciò che non misuro (40 s).** Stanza vuota, un cartone copre mezzo campo: schermata d'avvio, «NESSUN OSTACOLO OSSERVATO FINO A 2,7 m», metà pianta a puntini. *«Distinguere le informazioni osservate da quelle incerte»; «sicurezza delle indicazioni».*
2. **Ostacolo fermo (30 s).** Una cassa oltre 1,24 m, fuori dalla linea: nero pieno, ombra a righe, «ATTENZIONE», distanza. *«Rilevare … ostacoli»; «feedback spaziali chiari».*
3. **Attraversamento (30 s).** L'attore attraversa in vista a 2,3 m: disco pieno, scia piena, età del dato. *«Rilevare elementi mobili»; «tempestivi».*
4. **Passa dietro il pannello (60 s, due passaggi, scelta A).** Visto in parte → previsto → previsto ampio → ricomparso con lo scarto; il registro scrive «DEDOTTO» e «OSSERVATO»; sotto resta la possibile presenza. *«Gestire interruzioni della visibilità»; «continuità percettiva».*
5. **Si ferma dietro e torna (60 s).** Nascosto 5–10 s: «non ricomparso da n s (dedotto)»; nessun timer spegne l'avviso; al ritorno, riaggancio. *Interruzioni; sicurezza delle indicazioni.*
6. **La prova che sceglie il giurato (90 s).** Pannello virtuale: il giurato cammina in vista dietro un cuneo cancellato a programma, e **prima** sceglie da un cartoncino: prosegue, si ferma, torna, svolta. Il tabellone conta nella sua riga. Detto prima: «se svolta, la zona la contiene in 3–7 casi su 10 a 2 s; lì la copre solo l'avviso» (V8 §2.1). *La «valutazione realistica» della precisione (obiettivo dell'utente).*
7. **Mano sul sensore (30 s).** Un giurato copre la camera quando vuole: «AFFIDABILITÀ PERSA · sensore coperto»; le tracce restano come zone; al ritorno «identità ambigua». *«Segnalando … la perdita di affidabilità».*
8. **Profilo sonoro (60 s).** Una persona bendata **ferma** accanto al treppiede, atti 3–5 in suoni (AS, C6); a voce: «per chi cammina non è provato niente». *L'applicazione alla disabilità visiva, nei limiti del §2.*
9. **Costo (20 s).** Al piede dello schermo: «calcolo x ms per ciclo» misurato in sala; «ritardo: non misurato», oppure la misura. *«Efficienza elaborativa»; latenza: la cifra, senza aggettivi.*

Circa 7,5 minuti (durata concessa: non verificata). Ordine dei tagli: 2, 8, 1, 3; mai apertura, 4, 6, 7, chiusura. L'atto 4 va con la camera vera solo dopo dieci passaggi riusciti di fila sull'hardware (criterio ripreso dal blocco B9 del nucleo). Motivo, **preliminare** (f10, `20-validazione`): sulla profondità simulata realistica la catena così com'è ha tenuto l'identità in 0 passaggi su 90 (41 su 45 con una soglia cambiata dopo) e ha detto «si muove» del pannello in 79 su 90.

**Variante «solo registrazioni».** Stessi atti, senza attore: 1–5 e 7 su sequenze del sensore simulato (f10, `11-simulatore`), riga «DATI SIMULATI»; 6 su traiettorie pubbliche di pedoni veri con l'occlusione creata a programma (THÖR: 9 persone, 219 tratti; **preliminare**), riga «REGISTRAZIONE PUBBLICA»: il giurato sceglie il numero della sequenza e il comportamento; 8 con i suoni sulle stesse sequenze. L'apertura diventa: «Oggi non c'è una camera: tutto ciò che vedrete è simulato o registrato da altri, e la riga in alto dice quale dei due.»

**Chiusura (30 s; si dice solo ciò che è successo in sala).** «Avete visto che il segno non sparisce mentre la persona è nascosta, che la zona dice quanto è larga, e che l'avviso resta finché non si guarda. Non avete visto, perché non c'è: una camera in moto, due persone dietro lo stesso ostacolo, il vetro, l'aperto, una prova con persone non vedenti. Oggi il tabellone dice: dentro k su n, cioè fra … e … su 100.»

## 7. Frasi da non dire → la frase vera (unione di VN §4, V7 §6, V8 §5 e §7, V9 §4 e §6, AS)

- «validato», «certificato», «garantito», «tarato», «provato» senza dire dove → «provato solo al calcolatore, una persona sola, al chiuso, fino a 3 m, camera ferma a 1,2 m».
- «continuità garantita», «prevede dove sarà», localizzare «per tutta l'occlusione» nella demo → «finché è nascosta lo schermo mostra un segno e una zona dove può essere; cede se la perde prima dell'ostacolo»; «qui localizza per circa 1 s, poi dice che è ancora dietro».
- «90 %» senza dominio, un livello al 50 %, una cifra oltre 3 s, in moto o indossato, «l'ellisse al 95 % è coerente» → la frase del §6.2 di V8, con «in simulazione, a camera ferma»; «qui vale il tabellone».
- «30 prove bastano» → «27 su 30 dice: fra 74 e 97 su 100». «± X,XX m», «confidenza Z %» → «non visto da 1,5 s · larga 0,8 m»; «la zona ha contenuto la persona k volte su n».
- «via libera», «mai dato per libero» senza condizioni → «nessun ostacolo osservato fino a d metri»; «è progettato per non dare per libero ciò che non vede in quell'istante».
- «la perdita di affidabilità è dichiarata» senza condizioni → «segnala sensore coperto, fotogrammi fermi, inclinazione cambiata; su una camera vera non è ancora provato».
- «segue chi passa dietro un ostacolo» e basta; che il riaggancio regga con due persone → «…dietro un ostacolo che lo nasconde per intero, una persona sola; se dalla stessa ombra esce un'altra persona, la scambia».
- «riconosce la sosta», «si è fermato dietro il pannello», «è uscito», «sosta in ombra» → «non ricomparso da n s (dedotto): fermo dietro l'ostacolo oppure uscito dal lato non visibile».
- «bassa latenza», «15 cicli al secondo con tutti i moduli» → «ritardo non ancora misurato, stimato 155 ms»; «calcolo x ms per ciclo, misurato qui». «dal vivo» prima che giri → la sorgente della riga fissa.
- «mappa 3D», «voxel», «copre gli ostacoli bassi», una «quota verificata» non letta, «360°», «il vetro è risolto» → «mappa a celle del suolo fino a 3 m; non misura a meno di 1,24 m di distanza; non vede il vetro».
- «ACAS», «TA/RA», «anti-bird strike», «detect and avoid», «indice di minaccia», «NOMINAL / HOLD / FAIL-SAFE», «preallarme laterale» → i quattro nomi del §1; «avvicinamento diretto»; «avviso di prossimità laterale».
- «drone», «UAV», «in volo», «in movimento» → «camera ferma; un veicolo senza equipaggio è un modo di portarla: provato solo da fermo e a 1,2 m».
- «orientamento» per chi cammina, «dispositivo medico», «conforme a» → «avviso di presenza per una persona non vedente ferma; nessuna prova con persone».
- «ispezione»; «Intelligenza Artificiale», se l'etichetta è tagliata; «massa e accelerazione stimate» → «un registro di eventi, osservati o dedotti»; «geometria e regole scritte, nessun modello appreso»; «stimiamo posizione e velocità».
- «la preproposta è stata adottata», «in cinque ci sta», «taglio garantito», il contratto della società come fatto → «ne teniamo le regole di disegno e gli attacchi»; «piano a tappe»; «riferito dall'utente».

## 8. Stati proposti e che cosa propongo dopo

Pannello da 2 m alla scala della demo: **controesempio in simulazione** (un codice, 400 semi); lo decide la prova d'insieme (C-C) rifatta sulla geometria `E` da un altro autore. Pannello da 1 m a passo lento: **sostenuto dai dati in simulazione**; sul sensore **non provato**. Dopo: dieci secondi con tre persone esterne su schermo e tabellone, anche stampati in bianco e nero (Vis §5: decide anche K1 e K2); i segnali con tre persone bendate; dopo l'hackathon, battito continuo e portata oltre 3 m per l'ombra larga. **Rifare:** `sh rifai.sh`.
