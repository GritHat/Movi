# Tabella delle correzioni obbligate → dove stanno nella versione 3 FINALE — f12, `20-finale` (`sciame-scene-dinamiche`)

14 novembre 2026. «§» rimanda a `SOLUZIONE_V3.md` **di questa cartella** (versione finale); «I#» agli invarianti del suo §2. La numerazione dei blocchi (§1.1–§1.12) e dei paragrafi §2–§7 è la stessa della prima stesura: le righe dei §1–§8 qui sotto sono quelle della prima stesura, con la terza colonna riscritta dove la regola è cambiata (31 righe, elenco in `fai_tabella.py`); le altre le ho lasciate com'erano e **non le ho ricontrollate una per una**. I §9–§14 sono nuovi: una riga per ogni correzione delle quattro critiche di f12 e per gli esiti delle prove nuove, con **applicata** o **non applicata** e il motivo. **Esclusa** = non entra nel prototipo, con il motivo. **Altro ruolo** = è del piano o dello schermo finali. **[prel.]** = f10 col verdetto VD; **[f12]** = prova di questo passo, non vagliata dall'arbitro. Nessuna riga è «validata».

## 1. Verdetto del nucleo (VN): le nove condizioni, più la decima di V8

| Sigla | Che cosa chiede | Dove nella versione 3 |
|---|---|---|
| VN-1 | filtri della camera spenti; autoverifica all'avvio (mano sul sensore, pixel validi sotto il 10 % in 3 fotogrammi), altrimenti non parte | §1.1; I13. [prel.] necessità sostenuta in simulazione (989–995 celle «libero» con i filtri accesi) |
| VN-2 | fascia a formula, oppure velocità massima coperta dichiarata (circa 1,4 m/s); soglie in secondi | §1.7: una sola fascia w = 0,40 m; copre 1,13 m/s col conto a tre termini (0,56 con 20 cm d'errore di bordo), 1,4 m/s solo con età e latenza; §1 convenzioni (secondi); K-015 nel §5 |
| VN-3 | pannello alto almeno 1,5 m e largo 1 m, attore a non più di 2,3 m, una sola persona dietro | §7 «geometria della demo»: pannello alto **1,8 m** (VD), largo 1 m, attore a 2,3 m, una sola persona |
| VN-4 | profilo «sensore fermo» dichiarato; nessuna soglia in moto; il criterio dell'IMU è del profilo | §0; §1.9 (parametro IMU «solo profilo fermo»); §3; §7 |
| VN-5 | N-C6 obbligata, con il suo costo | §1.3; costo e conflitti: K-110, K-218 nel §5 |
| VN-6 | garanzia solo per chi è stato visto almeno 4 fotogrammi, con una traccia pendente e l'occlusore fermo | §1.5 (parametro), §1.7, §7; V8: vale anche per la previsione → §1.6, §7 |
| VN-7 | limiti scritti: rilevamenti mancati vicino all'ombra, secondo soggetto, vetro, ostacoli bassi sotto 1,09 m, sole | §7 (allungati come chiede V8) |
| VN-8 | la regola per l'ombra propria fissata prima del codice (K-018) | §1.5 («occlusore che NON è il gruppo della traccia»); scritta, eseguita solo nella catena f10 [prel.] |
| VN-9 | dicitura «provato solo in simulazione, a sensore fermo»; mai «via libera» | §0; §3; §7; I12. V8 aggiunge «soggetto puntiforme salvo le controprove» → §1.6, §7 |
| VN-10 (V8 §3) | un solo livello dichiarato, con il dominio e con «previsto ampio» | §1.6; §7 |
| VN §0 | invariante 1: la riga «0,33 m, meno della fascia» è smentita | §2 (coda): la riga cade; I1 non ha più memoria |
| VN §0 | R8 diviso in due enunciati («mai libero» / garanzia dell'avviso) | I1–I2 e I7, con stati distinti |
| VN §5 | dieci affermazioni convergenti | §3 (contratto), §7; la 5 («la previsione vale mezzo secondo») è **sostituita** da V8 → §1.5, §1.6 |
| VN §6 | prossima prova sull'hardware: autoverifica dei filtri, celle per stato su 150 fotogrammi, «libero» dentro l'ombra vera | §1.1; controlli di I1 nel §2; K-014 nel §5 |

## 2. Audit delle ipotesi nascoste (AU)

| Sigla | Che cosa rileva | Dove nella versione 3 |
|---|---|---|
| AU-1 | i filtri della camera trasformano un buco in un dato | §1.1 (filtri spenti, autoverifica) |
| AU-2 | «libero» mai calcolato da una profondità; i quattro stati non coprono tutti i ritorni | §1.2 («non osservato» = tutto il resto); controllo di I1; [prel.] la catena f10 lo calcola (25 prove a mano) |
| AU-3 | l'età del «libero» ignora la latenza | §2 coda; I1 senza memoria; fascia a formula in §1.7 |
| AU-4 | ogni traccia sta a meno di 0,40 m dalla propria ombra | §1.5 (ombra di un occlusore diverso dal gruppo della traccia); una persona che ne nasconde un'altra = occlusore mobile: limite nel §7 |
| AU-5 | l'ombra vale solo se il pannello è più alto del campo; l'occlusore basso è il caso comune | §7 (geometria: 1,7 m; «dietro un ostacolo più basso di 1,65 m perde chi è in vista»); K-110 |
| AU-6 | buchi del suolo non indipendenti: celle sempre non valide | §1.10 (il buco ferma d e dà «zona non verificata», non scavalca «attenzione»); K-106, K-307 |
| AU-7 | soglie in fotogrammi e tempi perfetti; falsi «affidabilità persa» all'1 % di salti | §1 convenzioni (secondi); §1.9 (soglia da rifissare dopo 60 s di conteggio) |
| AU-8 | la catena dei blocchi è seriale; ordine che protegge la demo; ripieghi | **altro ruolo** (piano); i ripieghi sono citati in §1.3 e §1.4 |
| AU-9 | l'avvio presume una scena vuota e ferma | §1.1 (taratura a scena vuota; posa entro 0,5°; due prove d'ingresso) |
| AU-10 | banda stereo senza dato accanto all'ombra (5–9,5 cm), errore non simmetrico | K-215 nel §5 (errore della maschera al bordo, primo sensore); [prel.] nessuna asimmetria a 424 pixel |
| AU-11 | soglia di 0,07 m e campo della scheda; pixel minimi per «occupato» non scritti | §1.1 (stampa di risoluzione e campo); §1.2 (almeno 3 pixel); `sd-K4` |
| AU-12 | le costanti nascondono pedone, sala, sensore fermo, pavimento | §3 (quattro regole su nove; due profili); §1.9; §7 |
| AU §2 | che cosa un lettore può credere dimostrato e non lo è; la riga per il giurato | §0; §3 («non si dice mai»); §7 («da dire per primi»). La «prova scelta dal giurato»: **altro ruolo** (demo) |

## 3. Verdetto f7 (V7): mappa voxel e traccia

| Sigla | Che cosa chiede | Dove nella versione 3 |
|---|---|---|
| V7-a | il «libero» della cella va riscritto (K-107) | §1.2: `nuvole-1` (esito di C-D, LC); K-107 nel §5: decisa in simulazione, aperta sul vero |
| V7-b | l'uscita dice «suolo visto libero fino a d»; una quota solo se letta | §1.2, §1.10; `sd-K2` |
| V7-c | sensore non in salute: il ramo non finisce muto; tracce in previsione marcate; al ritorno regione dilatata e riaggancio ambiguo | §1.9; I13; `sd-K5` (= K-109) |
| V7-d | la correzione C2 (traccia che sparisce nel vuoto vicino) nello pseudocodice | §1.5 |
| V7-e | controllo dell'inclinazione nella salute (V-020) | §1.1 (avvio), §1.9 (in esercizio) |
| V7-f | casse fuori dalla linea dell'attore; dietro un ostacolo più basso di circa 1,65 m il sistema perde chi è in vista, e lo si dichiara | §7 |
| V7-g | la prova 9 regge per la lettura del fotogramma, non per la griglia con memoria | §1.2 (nessuna memoria); §1.9 (griglia tutta «non osservato») |
| V7-h | «provato» si legga «sostenuto dai dati, simulazione, un autore» | §0 e ogni riga «Stato» del §1 |
| V7 §1 | NO alla mappa voxel nelle 14 + 4 ore | **esclusa**: §4 |
| V7 §1 | NO alle tre fasce (S10) come sostituto e al passaggio automatico | **esclusa**: §4; resta il principio (§1.2) |
| V7 §1, tabella | griglia polare: occupato e ombra del fotogramma vincono | §1.2 |
| V7 §1, tabella | «libero» senza memoria (V-018; ripiego `stato` a 0,20 m) | §1.2 (`nuvole-1`; il ripiego `stato` a 0,20 m è caduto: LC, AT P1); I1 |
| V7 §1, tabella | affidabilità persa contata sui pixel validi | §1.9 |
| V7 §1, tabella | `stato(p)` per la previsione, letta a 0,20 m | §1.6: il ritaglio usa la maschera di §1.2, la stessa delle celle (LC §3); la lettura per punto a 0,20 m da sola è caduta |
| V7 §1, tabella | registro degli eventi con «come lo so» | §1.11; I14 |
| V7 §1, tabella | V-017, V-016, V-019, T-008: serve il secondo autore; 4 ore | §4: V-017 fuori dalle 14 ore (controesempio coi buchi a chiazze, LC); V-016, V-019, T-008: 4 ore, se confermate |
| V7 §2 | struttura a tre assi (applicazione, portatore, uscita) | §1 (sotto lo schema); §3 |
| V7 §2 | ambito: il testo riscritto dall'attacco (A7 §3.8) | **altro ruolo** (documento di due pagine); la coda «provato solo al calcolatore…» è nel §7 |
| V7 §2 | veicolo senza equipaggio = valore dell'asse «portatore», sempre con «fermo» o «non provato» | §3, tabella dei profili |
| V7 §2 | S11 riformulata: `SOSTA_IN_OMBRA` diventa «non ricomparso da n s (dedotto)» | §1.11; §6 (da rinominare nel codice) |
| V7 §2 | coperte solo a parole: «oggetti», «ispezione», «aerospaziali», «Intelligenza Artificiale», «bassa latenza» | §3 («non si dice mai»); §1.10 (latenza non risolta) |
| V7 §2 | demo: pannello alto almeno 1,7 m, a 1,7–1,9 m, attore a 2,3 m; K-111 | §7 (1,8 m, a 1,8 m, attore a 2,3 m); K-111 nel §5 |
| V7 §3 | K-102 (il cuneo nasconde chi si vede dietro un ostacolo basso), K-105 («liberi» occupati entro 0,20 s: mai «via libera», onesto fino a 1,4 m/s) | §7; I12; §1.7 |
| V7 §3 | K-106, K-107, K-109, K-110, K-111 aperte; K-108 (ore) | §5; K-108: **altro ruolo** (piano) |
| V7 §4 | contratto d'uscita e quattro regole identiche su nove | §3 |
| V7 §4 | i due profili differiscono in canale d'uscita e reazione alla perdita (C5); nome del secondo (C6); frase della prova (C1); limite (C8); vuoto vicino (C2); 1,4 m/s (C4); pannello a non meno di 1,7 m di distanza (C3) e alto 1,7 m | §3; §1.5; §1.7; §7 |
| V7 §4 | elenco di ciò che resta «non provato» | §3 (tabella), §7 |
| V7 §5, §6 | quattordici affermazioni convergenti; affermazioni da non fare | §3, §7; **altro ruolo** per il documento |
| V7 §7 | prossima prova: V-017 e V-018 sullo stesso banco; poi la stanza ferma per 60 s | eseguita in questo passo: LC (C-D). Esito in §1.2; K-107, K-106 nel §5 |
| A7 §3.1 | regola del «libero» con almeno 3 pixel e quota letta | §1.2 (3 pixel per «occupato»); la quota letta esce con V-017 (§4) |
| A7 §3.2 | frase d'uscita con q letta; «senza una parete entro la portata la quota verificata scende a 0,6 m» | §1.2 (la quota entra solo con V-017, nelle 4 ore: il limite va scritto allora) |
| A7 §3.3 | sensore non in salute; rilascio «oltre la fascia» | §1.9; §1.7 (rilascio oltre w dall'ombra corrente dell'occlusore) |
| A7 §3.4 | C2 nello pseudocodice | §1.5 |
| A7 §3.5 | assetto entro 1°; controllo del piano | §1.1, §1.9: **0,5°**, non 1° (controesempio a 1°: AT P2, LC, CO B13) |
| A7 §3.6 | ostacolo basso: casse fuori dalla linea; limite dichiarato | §7 |
| A7 §3.7 | ore: accettazione ridotta o registro nelle 4 ore | **altro ruolo** (piano) |
| A7 §3.8 | testo dell'ambito | **altro ruolo** (documento) |
| A7 §3.9 | S10: motivi (ii) e (iii) tolti; resta il principio | §4 |
| A7 §3.10 | «suolo visto libero fino a d» non oltre la portata meno 0,40 m | §1.10; I12 |

## 4. Verdetto f8 (V8): continuità visiva

| Sigla | Che cosa chiede | Dove nella versione 3 |
|---|---|---|
| M1 | riga d'ingresso riscritta; la previsione accende l'avviso e non lo toglie | §1.5; §1.7 |
| M2 | «perso» → «previsto ampio»; chiusure motivate, elenco chiuso; R100 = strato 1; maschere a ogni ciclo | §1.5; §1.7; §1.2 (maschera a ogni ciclo) |
| M3 | interfaccia «insieme di celle», sd-0, pavimento, punto ibrido | §1.6 |
| M4 | sd-1 («fronte + scia») dietro la stessa interfaccia | §1.6 |
| M5 | disegno nuovo (disco, anello, regione tratteggiata, indicatore, scarto alla ricomparsa), contatore | §1.10; §1.8 (scarto); la croce in «ampio» cade per c8 |
| M6 | occlusione virtuale, registro per ciclo, scheda per comportamento e per tempo | §1.12 |
| M7 | porta sul riaggancio: oltre 0,40 m da R90 non riaggancia | §1.8 |
| M8 | rumore misurato in R, libreria dei percorsi, scheda sul sensore | §1.12; §1.3, §1.4 (parametri) |
| M §2.8 | misure di accettazione nuove (0 cicli senza regione; R90 per comportamento; punto; disco pieno; costo) | controlli di I3, I4, I10 nel §2; §1.12; stato in §1.6 |
| M §2.9 | demo riscritta (atti 4, 5, 5 bis col pannello virtuale) | **altro ruolo** (piano e demo); il pannello virtuale è §1.12; K-111 |
| M §2.10 | invarianti 3, 4, 6, 8, 9 riscritti e 10 nuovo | §2: I3, I4, I6, I8, I9, I10 |
| M §3 | «a prescindere dal sistema»: interfaccia identica; in moto tutto da riprovare | §1.6 (interfaccia unica); §7 |
| c1 | riaggancio: prima misura non tagliata entro 0,40 m da R90 e 0,75 m dall'ombra d'ingresso | §1.8: **entra insieme a F-409**, col limite «un soggetto per ombra»; da sola cade contro l'estraneo (PI riga d); K-218, K-219, K-016 nel §5 |
| c2 | le pendenti ambigue diventano un solo avviso e non bloccano il riaggancio | §1.7 (un avviso con contatore), §1.8 («la più recente», identità presunta); `sd-K3`, `sd-K7`, `logico-K1` nel §5 |
| c3 | «gruppo tagliato» definito sull'immagine | §1.3 (col sensore; fino ad allora la cifra vale «con la maschera esatta»: K-215) |
| c4 | entrata dopo due cicli senza misura; subito se il gruppo è tagliato | §1.5; K-220 |
| c5 | sotto 0,3 m/s d'ingresso subito «ampio» | §1.6: 0,3 m/s **e** «sotto 0,3 m/s negli ultimi 2 s → ampio» (PI), coi due denominatori (AT P12) |
| c6 | il gruppo tagliato a contorno pieno, «visto in parte», senza velocità | §1.3; §1.10 |
| c7 | traccia chiusa o non confermata entro 0,75 m da un'ombra accende l'avviso | §1.5: sostenuta in simulazione ideale (PI: 928 → 24 su 23 402); **dietro la prova d'ingresso del rumore** (AT P11) |
| c8 | soglia di «ampio» sulle sole celle d'ombra; in «ampio» niente croce | §1.6; §1.10 |
| c9 | libreria di almeno 200 percorsi; «sul percorso» = rotta entro 3 °/s | §1.6 (parametro); §1.12; K-221. Raffinamento |
| c10 | evidenza negativa solo su celle libere negli ultimi 3 fotogrammi; in moto «ampio» | **esclusa**: dopo l'hackathon (§4) |
| statistico-3 | un denominatore («nascosti dentro l'area osservata») e la regola di Wilson | §1.12 |
| statistico-4 | il tabellone conta la persona dentro la regione a 1 e a 2 s | §1.12 |
| statistico-5 | «almeno 9 su 10» fino a 2 s, «almeno 8 su 10» fino a 3 s, poi «ampio» | §1.6: «almeno 9 su 10» fino a 2 s, «almeno 85 su 100» fra 2 e 3 s (una sola scritta: CO A8), solo con sd-1 e ostacolo largo 2 m |
| statistico-6 | libreria da almeno due persone a tre andature | §1.6, §1.12 (registrazione nelle 14 ore, prova nelle 4) |
| statistico-7 | riparare il seme del generatore prima di ogni nuovo lancio del banco | §6 (avvertenza); §4 (dopo, salvo nuovi lanci) |
| V8 §4.1 | c7 per prima (sicurezza) | §1.5 |
| V8 §4.2 | c1, e prima la prova contro l'estraneo | §1.8: prova eseguita (PI): c1 cade contro l'estraneo; entra con F-409 |
| V8 §4.3 | c2 | §1.7, §1.8 |
| V8 §4.4 | c4 | §1.5 |
| V8 §4.5 | c3; finché manca, «con la maschera esatta» | §1.3; §1.6 (stato); §7 |
| V8 §4.6 | c5 | §1.6 |
| V8 §4.7 | c6 e c8 | §1.3, §1.6, §1.10 |
| V8 §4.8 | le tre righe dello statistico | §1.6, §1.12 |
| V8 §4.9 | la chiusura «fuori dall'area osservata» non toglie l'avviso | §1.5, §1.7: sostenuta in simulazione (PI riga e2); `sd-K6` chiusa |
| V8 §4.10 | nel raffinamento c9 e statistico-6; dopo c10 e statistico-7 | §1.6, §1.12; §4 |
| V8 §4 | manca la prova d'insieme | eseguita in questo passo: PI (C-C), controllata da ST; esiti in §1.5–§1.8, §7 |
| V8 §5 | sd-0 o sd-1 (decisione dell'utente); sd-0 per primo | §1.6 |
| V8 §5 | della preproposta (C-EST): S3 e S4 non entrano; di S5 entrano contorno pieno solo con una misura, inviluppo tratteggiato ritagliato, età | §4; §1.10 |
| V8 §5 | ciò che non si può dichiarare | §3 («non si dice mai») |
| V8 §3 | K-202, K-214, K-215, K-218, K-219, K-220, K-221 aperte; K-016 non riparata | §5; §7 |
| V8 §6 | otto affermazioni per la giuria | §7 (forma più forte e «dove cede») |
| V8 §7 | prossima prova: c1–c5 e c7 insieme, semi nuovi, estraneo, corpo esteso a −10 cm | eseguita: PI. Esiti: continuità regge; precisione regge in T e L, cade col pannello da 1 m; estraneo: cade; K-215 senza c3: cade |

## 5. Verdetto f9 (V9): preproposta esterna

| Sigla | Verdetto | Dove nella versione 3 |
|---|---|---|
| S1 | forma minima approvata (controllo all'avvio, configurazione dichiarata, mappa fissa); forma completa **respinta** | §1.1; I11; completa: **esclusa**, §4 |
| S2 | approvata con correzioni: età dichiarata; compensazione solo sull'uscita | §1.10 (età nelle 14 ore; compensazione nelle 4, mai in ombra); I3; §4 |
| S3 | approvata solo come informazione, una ipotesi; seconda ipotesi solo se batte l'orologio | §1.6 (una ipotesi); «non riemerso» in §1.11; seconda ipotesi: **esclusa**, §4; `sd-K1` |
| S4 | (a) ritaglio sul visto libero con fascia: approvata; (b) pesi a ogni ciclo e (c) soglia 0,8 m: **respinte** | (a) §1.6, I4; (b), (c): **escluse**, §4 |
| S5 | disegno approvato (trama e parola prima del colore; l'area non sparisce; un decimale; mai verde); etichetta «± \| conf» **respinta** | §1.10; etichetta: **esclusa**, §4 |
| S6 | formule approvate come etichetta; «probabilità d'intrusione» **respinta** | §1.10 (4 ore, sola etichetta, riferita al punto protetto, con la guardia per l'oggetto fermo); K-305 nel §5; «probabilità d'intrusione»: **esclusa**, §4 |
| S7 | **respinta** come modulo; resta l'etichetta «avvicinamento diretto» | §4; §1.10 |
| S8 | com'è scritta **respinta**; riscritta approvata (nomi che dichiarano; affidabilità persa fuori scala) | §1.10; §4; K-306…K-308 |
| S9 | «preallarme» **respinto**; canale di sola prossimità da provare sull'hardware | **esclusa**: §4 (dopo) |
| S10 | regola corretta approvata; «chiude il buco sotto 1,1 m» e passaggio automatico **respinti** | §1.1 (frase d'avvio sulle quote non viste), §1.2 (principio); §4 |
| S11 | approvata con correzioni: ogni evento osservato o dedotto, «non riemerso» | §1.11; I14 |
| S12 | «taglio garantito» **respinto**; piano a tappe approvato | §4; **altro ruolo** (piano) |
| V9 §5.1–§5.9 | ciò che entra nella soluzione integrata | 1 → §1.1; 2 → §1.6, I4; 3 → §1.6 e `sd-K1`; 4 → §1.10; 5 → §1.10; 6 → §1.10; 7 → §1.11; 8 → altro ruolo; 9 → §1.10, §1.1 |
| V9 §4 | letture sbagliate: «sotto 1,1 m» è una distanza | §7 («di distanza dal sensore») |
| V9 §4, §6 | parole che promettono troppo; «da non dire» | §3 |
| V9, decisione 3 | la presa visione dell'operatore | `sd-K3` (decisione dell'utente) |
| V9 K-301…K-308 | contraddizioni | K-301: non entra (solo forma minima); K-302, K-303, K-304: §5 (chiuse dall'adozione di V8); K-305: 4 ore, etichetta; K-306…K-308: §5 |

## 6. Attacco alla specializzazione (AS): C1–C8

| Sigla | Che cosa chiede | Dove nella versione 3 |
|---|---|---|
| C1 | la frase «una prova» con una persona sola, rilevamento senza errori, e dove cede | §3 (coda), aggiornata con V7 e V8; §7 |
| C2 | il soggetto nel vuoto vicino: niente «nessun ostacolo» sui settori finché non è rivisto; limite scritto | §1.5; §1.10; §7 |
| C3 | pannello a non meno di 1,7 m | §7 (geometria della demo) |
| C4 | fascia a formula; d non oltre la portata meno v_max·(età + latenza); «fino a 1,4 m/s, di corsa no», classe «persona» | §1.7; §1.10; I12; §7 |
| C5 | «adattabile»: identici il contratto e quattro regole su nove; i profili differiscono in canale e reazione | §3 |
| C6 | profilo assistivo = «avviso di presenza per una persona non vedente ferma», non «orientamento» | §3 |
| C7 | piano del suolo: porta riferita alla taratura da fermo, 1° a 3 m, altrimenti affidabilità persa; velocità propria ≤ 0,37 m/s per la memoria del «libero» | §1.1, §1.9; la seconda parte decade: non c'è più memoria (I1) e niente è dichiarato in moto |
| C8 | il limite per tutti i giurati: al chiuso o all'ombra, 3 m, camera a 1,2 m; messaggio per l'autopilota non simulato | §3 (tabella); §7 |
| AS §3 | ciò che resta «non provato», comprese le correzioni C1–C8 stesse | §3, §7; stati nelle righe del §1 |

## 7. Misure di f10 che toccano un parametro — tutte [prel.], ricontate da VD salvo dove VD dice «lette e non ricontate»

| Parametro o regola | Che cosa dice f10 | Dove annotato |
|---|---|---|
| Filtri della camera | accesi, col sensore coperto: 989–995 celle «libero» per altri 3 fotogrammi | §1.1 |
| Posa | 1° d'errore: ostacolo di 10 cm a 2,55 m «libero»; stima dai primi fotogrammi sbagliata di 5° su una sequenza vera | §1.1; §7 |
| Pixel minimi per «occupato» | soglie assolute dipendono dalla risoluzione (40 a 424×240 ≈ 160 a 848×480) | §1.2; `sd-K4` |
| «Libero» nell'ombra vera (K-014) | 0 su 2 907 032 celle·fotogramma a posa esatta, tre geometrie | §1.2; §5 |
| Gruppi | la persona si fonde col pannello in 90 passaggi su 90; pannello «mobile» in 79 su 90 | §1.3; §7 |
| σ del centro | simulato 0,3 / 0,8 / 1,2 cm di mediana, bimodale a 2 m; vero descrittivo 5,8–6,8 cm | §1.3 |
| q del filtro | 0,2 prudente su pedoni veri; calibrato fra 0,05 e 0,1 | §1.4 |
| Avviso | centro nascosto nell'avviso in 2939 fotogrammi su 3038 (nucleo); due persone e occlusore mobile: 25 e 21 fotogrammi fuori | §1.7 |
| Riaggancio | prende un fantasma dello spigolo a soggetto nascosto; proposta `validazione-7` | §1.8 |
| Errore del bordo d'ombra | da +2 a +15 cm verso il largo, al nominale, un solo spigolo | K-215 nel §5 |
| Altezza del pannello | servono 1,61 m (conto della catena) | coerente con 1,7 m: §7 |
| Zona valutata | il vuoto vicino è una striscia, non un anello (a ±44° il suolo si vede da 1,69 m) | §1.1 (celle con suolo contate all'avvio) |
| Criterio «28 su 30» | limite inferiore 78,7 %: non mostra il 90 % | §1.12 |
| Costo | 1–6 ms a 424×240 su scene pulite; 81 ms su una scena vera con 254 tracce | §7 |
| Correzioni proposte, non provate | `validazione-6` / `avversario-2` (soglia proporzionale), `avversario-3` (avviso che resta al riaggancio), `validazione-9` / `avversario-1` (prova d'ingresso) | §4 (coda), §1.1 |

## 8. Verdetto f10 (VD): difetti F-401…F-413, condizioni, contraddizioni

VD chiama i difetti «ingressi obbligati per la soluzione integrata» e le loro correzioni «non provate»: la versione 3 registra ogni difetto dove tocca una regola, e non adotta una correzione non provata.

| Sigla | Che cosa dice | Dove nella versione 3 |
|---|---|---|
| F-401 | la persona si fonde col pannello (90 passaggi su 90); correzione: soglia proporzionale, non provata | §1.3: soglia per cella **esclusa** (smentita in ID: 98 e 91 celle «libero» in ombra); gruppi per picco dietro interruttore; §4; `sd-K4` |
| F-402 | il riaggancio accetta gruppi tagliati e l'occlusore stesso | §1.8: rifiuto dei tagliati (c1), del bordo del campo e dell'occlusore (interruttore `riaggancio_f402`) |
| F-403 | fantasmi del pavimento: «una sola traccia pendente» non è mai vera | §1.1: prova d'ingresso del rumore (0 gruppi in 30 s); `logico-K1` nel §5; §1.3 (stato) |
| F-404 | con la posa sbagliata di 1° un ostacolo basso è «libero» | §1.1: posa entro 0,5° **e** prova d'ingresso (10 cm a 2,5 m «occupato») come cancello; I13; §7 |
| F-405 | un ostacolo che non rimanda profondità è «libero» | §1.2 (controesempi); §7: limite dichiarato, come il vetro |
| F-406 | i filtri del costruttore tengono vivo il «libero» | §1.1 (condizione 1) |
| F-407 | «libero» per memoria su una cella che era occupata | I1: nessuna memoria; §6 (la catena f10 va corretta) |
| F-408 | dopo un riaggancio tagliato il filtro non si aggiorna (5,00 m) | §1.4, §1.8: il filtro riparte dalla misura con R + (larghezza/2)² (ID: 5,00 → 0,17 m, N = 1) |
| F-409 | al riaggancio l'avviso si spegne anche se nell'ombra resta qualcuno; q non si tara sulle innovazioni alla ricomparsa | §1.7: **adottata**: l'avviso resta al riaggancio (priorità 2; costo: non si spegne dietro un occlusore fermo); §1.4 (regola su q) |
| F-410 | ostacolo sospeso vicino: non visto, e sotto è «libero» (97,5 %) | §7; `sd-K2` (per questo la frase dice «suolo») |
| F-411 | la regione del filtro non informa; la velocità costante sbaglia su chi si ferma | §1.4 (il cerchio non è la precisione); §1.6 (predittore di f8); q = 0,1: §4 (coda) |
| F-412 | le soglie di pixel sono assolute | §1.3: rapporto col picco al posto della soglia assoluta, sui soli gruppi (interruttore); `sd-K4` |
| F-413 | il vuoto vicino è una striscia: a ±44° il suolo si vede da 1,69 m | §1.1 (zona valutata = celle che ricevono suolo all'avvio) |
| VD, cambi di stato | identità «100 %» smentita su profondità realistica; muro «mobile» smentita; q corretto verso 0,05–0,1; K-014 sostenuta a posa esatta | §0; §1.8, §1.3, §1.4, §1.2; §7 |
| VD, condizioni 1–9 | 1 confermata necessaria; 3 corretta (1,5 m non basta; proposta 1,8 m); 4 stretta (posa entro 1°); 5 non basta; 6 «una traccia pendente» falsa su profondità realistica; 7 più F-404, F-405, F-410; 9 dicitura nuova | §1.1 (1, 4: posa entro 0,5°); §7 (3: pannello 1,8 m; 7: limiti; 9: dicitura); §1.3 (5); §1.8 e `logico-K1` (6) |
| VD K-401…K-407 | K-401 copertura per passaggio (83 su 90); K-402 dominio stretto; K-403 soglia = rapporto coi pixel; K-404 bordo d'ombra; K-405 rumore a due gruppi; K-406 fantasmi = margine fra 5 e 7 cm; K-407 simulatore ottimistico sui buchi | K-401: §1.12 (si conta per passaggio); K-402: §1.2, §7; K-403: `sd-K4`; K-404: K-215 nel §5; K-405: §1.3; K-406: §1.1 (posa); K-407: §6, §7 |
| VD §5 | sei affermazioni per la giuria; «da non dire» | §7; §3 («non si dice mai») |
| VD §6 | prova senza sensore (F-401, F-402 a 424 e 848 pixel); tre prime misure col sensore | prova senza sensore: **eseguita** (ID): il criterio con le correzioni dei ruoli cade; passa una variante scelta dopo i dati, senza controprova: §1.3, §1.8. Tre misure col sensore: §7 |
| VD, decisioni dell'utente | telefono e inventario; dati con occlusioni lunghe; che cosa promettere sull'identità e su q | **altro ruolo** (piano e documento); q: §1.4 |

## 9. Attacco alla versione 3 (AT): le dodici correzioni obbligate

| Sigla | Che cosa chiede (controesempio) | Esito | Dove |
|---|---|---|---|
| AT-1 | l'avviso non deve cadere per sola identità (P5: 0,475–0,717 e 0,911–0,991) | **applicata**: F-409 adottata, costo dichiarato (140 su 140) | §1.7, §1.8, I5, I7, §7 |
| AT-2 | «libero» = `nuvole-1`, senza ripiego (P1) | **applicata** | §1.2, I1, §4 |
| AT-3 | inclinazione 0,5°, più la prova d'ingresso (P2) | **applicata** | §1.1, §1.9, I13 |
| AT-4 | «∩ non visto libero» al ritorno del sensore (P10) | **applicata** | §1.9 |
| AT-5 | una sola dicitura del livello più basso (P3, P4, F-410) | **applicata** nelle regole; lo schermo è di un altro ruolo | §1.10, I12, §3, §4 |
| AT-6 | c7 solo dopo «0 tracce in 30 s a pavimento vuoto» (P11) | **applicata**: interruttore; scoperti dichiarati (3,97 % senza) | §1.1, §1.5 |
| AT-7 | via il «100 %»: 29 su 95 399 e 15 su 2 000 (P8) | **applicata** | §1.7, §2 (coda), §7 |
| AT-8 | in demo «88 su 100 a 1 s, poi è dietro» (W4) | **applicata**, con la cifra di ST: 87 su 100 | §1.6, §3, §7 |
| AT-9 | c5 nella forma «fermo negli ultimi 2 s», due denominatori (P12) | **applicata** | §1.6, §7 |
| AT-10 | una sola fascia (P9) | **applicata**: w = 0,40 m come simbolo; la formula non è il parametro | §1.7, §1 convenzioni |
| AT-11 | §1.4 contro §1.8 con due pendenti (sessione 47 su 47) | **applicata**: «la più recente», identità presunta, un soggetto per ombra; `sd-K7` | §1.4, §1.8, §5 |
| AT-12 | le 8 righe della catena f10 nell'elenco «da correggere» | **applicata** | §6 |
| AT W1–W5 | cinque frasi lette come garanzia | **applicate** (W1 → AT-7; W2 → I7 col limite; W3 → AT-5; W4 → AT-8; W5 → via «fra 0,3 e 1,8 m/s» dal dominio) | §7, §2, §3 |
| AT R1, R2 | chi entra già tagliato; ombre dopo un'affidabilità persa (a ragionamento) | **non applicate come regole**: limiti dichiarati; servono i due casi sul banco di PI | §1.5, §1.7, §9 |
| AT R3 | «suolo visto libero fino a d» non esce mai sotto 1,24 m | **applicata**: «da 1,3 m a d m» | §1.10 |

## 10. Completezza e coerenza (CO): le undici correzioni obbligate

| Sigla | Che cosa chiede | Esito | Dove |
|---|---|---|---|
| CO-1 | «libero» riscritto con l'esito di C-D; intanto zero pixel a quota d'ostacolo (B5) | **applicata** la prima metà; **non applicata** la seconda (non è la regola provata; serve il banco con la variante); incoerenza B5 tolta dal testo | §1.2, §9 |
| CO-2 | posa «sotto 1°» più prova d'ingresso, o limite dichiarato (A3, A4, B13); 1,24 m al centro e 1,69 m ai bordi (A5) | **applicata**, più stretta: 0,5°; bordi 1,71–1,73 m (58°) o 1,69 m (424 px) | §1.1, §7 |
| CO-3 | esito del cancello su c1; K-219, K-016 con la prova; `sd-K4`; nuovo caso di K-014; niente scelto dopo i dati senza controprova | **applicata**; l'ultima parte **a metà**: i gruppi per picco entrano spenti, dietro interruttore | §1.3, §1.8, §5, §9 |
| CO-4 | (2) e (4) non chiudono la traccia; pendente ambigua, contatore, chi lo azzera (B1) | **applicata**: eventi, non chiusure; `sd-K3`: l'operatore ferma solo il suono | §1.5, §1.7, §1.9 |
| CO-5 | `logico-K1`; K-003, K-216, K-305, K-404, K-406; prova per K-016, K-214, K-108 | **applicata** | §5 |
| CO-6 | livello per predittore e geometria; una scritta fra 2 e 3 s; frase della prova (A6–A9) | **applicata** | §1.6, §3 |
| CO-7 | forma e parola per tentativa, «non confermato», ramo C2; «visto in parte» con la regione; origine dell'età; una soglia di conferma (B3, B4) | **applicata**: tabella degli stati; due soglie dichiarate per due cose | §1.4, §1.5 |
| CO-8 | da dove si misura «oltre la fascia»; R100 si dilata con R90; fascia come simbolo (B6, B7, B11) | **applicata** | §1.7, §1.9, I4 |
| CO-9 | 15 frasi «da non dire»; «nessuna funzione d'ingaggio o di puntamento»; mappa R1–R8; S6; pesi di sd-1 (A1, A2, A13–A17, B8) | **applicata** | §1, §3, §1.10, §1.6 |
| CO-10 | schermo: dicitura, d ≤ 2,6 m, un livello per settore, stringa del sensore, limiti di VD, pannello 1,8 m, predittore nella riga fissa (B9, B10) | **applicata** nelle regole; lo schermo finale è di un **altro ruolo** (`22-schermo-finale`) | §1.10, §1.5, §7 |
| CO-11 | piano: compiti, misure di VD §6, identità nel minimo o «in correzione», criterio di B3b, un n del tabellone (B12) | **non applicata** qui: è del piano finale (`21-piano-finale`); fissati qui il criterio di B3b (I7) e il tabellone a 100 passaggi | §1.12, I7, §9 |
| CO B8, B10 | il decimo si moltiplica? un livello per settore? | **applicate**: si moltiplica a ogni ciclo (`comp.c` 238, 298); un livello, il più alto | §1.6, §1.10 |
| CO B12 | tre valori di n del tabellone | **applicata**: 100 passaggi, due soglie (ST §5) | §1.12 |

## 11. Piano rifatto (PR): le otto correzioni

| Sigla | Che cosa chiede | Esito | Dove |
|---|---|---|---|
| PR-1 | scala con gelo all'ora 12; ordine d'ingresso; interruttori nominati sullo schermo | **applicata** per l'ordine e gli interruttori; il calendario è del piano | §1, §1.10, §4 |
| PR-2 | F-401/402/408/409 nella forma sui gruppi, mai la soglia per cella, con due cancelli a ogni fusione | **applicata**, dietro interruttore, in attesa della controprova | §1.3, §1.8, §6, §11 riga 10 |
| PR-3 | B3b riscritto: l'avviso resta finché le celle non sono viste libere | **applicata** | §1.7, I7 |
| PR-4 | B3a diviso fra due persone | **non applicata** qui: è del piano finale | §9 |
| PR-5 | tabellone sul tronco dall'ora 7–8; riga THÖR del predittore mostrato | **non applicata** qui: è del piano; qui la regola del tabellone | §1.12, §9 |
| PR-6 | la prova d'ingresso della posa precede ogni fotogramma vero | **applicata** | §1.1 |
| PR-7 | la latenza come riga del tabellone | **non applicata** qui: è del piano; la latenza resta «non risolta» | §1.10, §9 |
| PR-8 | ambiente preparato prima; origine della sequenza sullo schermo | **applicata** la seconda parte; la prima è del piano | §1, §1.10 |

## 12. Controllo statistico (ST)

| Sigla | Che cosa chiede | Esito | Dove |
|---|---|---|---|
| ST-1 | «0 vuoti»: «meno di 6,4 su 10 000», non 1,7 | **applicata** | §1.6, §7 |
| ST-2 | col pannello da 1 m «almeno 87 su 100» a 1 s | **applicata** | §1.6, §3, §7 |
| ST-3 | `nuvole-1`: «verificato sull'insieme dichiarato», non una frequenza | **applicata** | §1.2, I1 |
| ST-4 | semi riusati fra i lanci: 70 400 camminatori distinti al più | **applicata** nelle cifre | §1.6 |
| ST-5 | un solo totale sotto «tutti i lanci» | **applicata**: 217 861 lanciati, 23 402 per il limite | §1.6 |
| ST-6 | «finché resta nascosta» e «bordo noto» nella frase | **applicata** | §1.6, §3, §7 |
| ST-7 | secondo autore per `nuvole-1` su scene non sue | **non applicata**: serve un banco scritto da zero | §5 (K-107), §9 |
| ST §4 | che cosa non si può scrivere | **applicata** | §3 («non si dice mai») |
| ST §5 | quante prove dal vivo | **applicata** | §1.12 |
| ST §2 | segnale non spiegato su chi svolta | **non applicata**: serve un rilancio col corpo puntiforme | §5, §9 |

## 13. Esiti delle prove nuove (PI, LC, ID) [f12]

| Sigla | Esito | Dove |
|---|---|---|
| PI a1 | 0 vuoti su 23 402: regge | §1.6, I10 |
| PI a2 | scoperti: 24 su 23 402 con c7 (cade lo «0») | §1.5, §7 |
| PI b | precisione: regge con ostacolo largo 2 m; cade col pannello da 1 m | §1.6, §3, §7 |
| PI c | K-215: cade senza c3; con c3 solo se il bordo è visto a ogni ciclo | §1.6, §5 |
| PI d | estraneo: c1 cade (0,913–0,995) | §1.7, §1.8, §5 |
| PI e1, e2 | R100 per costruzione; chiusura (5) lascia l'avviso | §1.5, §1.7 |
| PI f, g | identità sul percorso 0,968–0,998; costo in C | §1.8, §7 |
| LC | `nuvole-1`; V-017 e «un pixel» cadute; 0,5°; 2,2 m al limite | §1.2, §4, §5 |
| ID | criterio di VD §6 caduto con le proposte; gruppi per picco in dominio stretto; F-409 a 0 fotogrammi fuori; K-014 a 848 px | §1.3, §1.7, §1.8, §5 |
| Controprova di ID | **non consegnata** alle 18:26 e alla chiusura (`ls`) | §0 |

## 14. Discordanze dei fascicoli (DF)

| Voce | Che cosa cambia | Esito | Dove |
|---|---|---|---|
| stima D1; geometria 9 | soglia «mobile» 5·σ·√(2/m), m = 3 | **applicata** | §1.3 |
| dimostrazioni D1; stima D2 | 99,25 % e 99,85 % sono limiti unilaterali; Wilson 99,05 % e 99,81 % | **applicata** | §1.8, §1.3 |
| geometria 3 | testa a 1,70 m vista da 2,01 m | **applicata** | §7 |
| geometria 1, 2 | suolo ai bordi 1,71–1,73 m (58°) o 1,69 m (424 px) | **applicata**: entrambe con la condizione; la scelta della focale **non applicata** (§9) | §1.1 |
| costo 2 | rese con conferma su tre fotogrammi e a un fotogramma | **applicata** | §1.2 |
| dimostrazioni D3 | «la previsione non tocca l'avviso» è falsa alla lettera | **applicata**: monotonia; con F-409 l'area realizzata non si chiude per riaggancio | §1.7, §2 (coda) |
| dimostrazioni D4 | fascia: 1,13 m/s (0,56) coi tre termini | **applicata** (derivazione scritta e riconosciuta) | §1.7 |
| valutazione 3 | «83 su 90» è della soglia 40; di partenza 36 su 46 | **applicata** | §1.6 |
| costo (rilancio) | previsione in Python 15,9 ms al 95° percentile | **applicata**: entrambe le cifre | §6 |
| bibliografia; consegna | norme sulla distanza non lette: C = 0,85 m non citabile | **applicata** | §3 |
| stima D6; valutazione 8 | THÖR, due codici | **applicata** | §1.4 |
| costo 5, 6 | vetro 654 su 800 a 2,0 m; 254 tracce confermate, non insieme | **applicata** | §1.2, §7 |
| dimostrazioni D5, D6, D8, D9 | Fisher esattamente 0; ordine della catena; «mai libero» in due enunciati; la fascia ottenuta con un peso | **applicata** | I9, §1.4, I2, I4 |
| geometria 8 | latenza 155 ms o circa 131 ms | **applicata** | §1.10 |
| valutazione 1 | denominatore della copertura di V8 | **non applicata**: la cifra di V8 non è più usata | §9 |
| altre (geometria 4–7, 10; stima D3–D5, D7; valutazione 4–7; costo 1, 3, 4, 7, 8; bibliografia D1–D8) | cifre che questo documento non usa | non toccate | — |
