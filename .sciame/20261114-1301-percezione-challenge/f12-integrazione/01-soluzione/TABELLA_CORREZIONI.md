# Tabella delle correzioni obbligate → dove stanno nella versione 3 — f12, `01-soluzione` (`sciame-scene-dinamiche`)

14 novembre 2026. «§» rimanda a `SOLUZIONE_V3.md` nella stessa cartella; «I#» agli invarianti del suo §2. Fonti e sigle come nel §0 di quel documento. **Esclusa** = non entra nel prototipo, con il motivo. **Altro ruolo** = è del piano o del documento di due pagine di questo passo: qui la riga dice solo che non è persa. **[prel.]** = viene da f10: profondità simulata dalle schede tecniche o tracce pubbliche, mai un sensore della squadra. Il verdetto di f10 (**V10**, `f10-dati/23-verdetto/VERDETTO_DATI.md`) era assente alle 17:50, è comparso alle 17:52 e l'ho letto alle 18:02: i §7 e §8 lo seguono. Lo stato di ogni riga è quello del verdetto citato: nessuna è «validata».

## 1. Verdetto del nucleo (VN): le nove condizioni, più la decima di V8

| Sigla | Che cosa chiede | Dove nella versione 3 |
|---|---|---|
| VN-1 | filtri della camera spenti; autoverifica all'avvio (mano sul sensore, pixel validi sotto il 10 % in 3 fotogrammi), altrimenti non parte | §1.1; I13. [prel.] necessità sostenuta in simulazione (989–995 celle «libero» con i filtri accesi) |
| VN-2 | fascia a formula, oppure velocità massima coperta dichiarata (circa 1,4 m/s); soglie in secondi | §1.7 (formula e «fino a 1,4 m/s»); §1 convenzioni (secondi); §7; K-015 nel §5. V8: limite inferiore di 0,3 m/s → §1.6, §7 |
| VN-3 | pannello alto almeno 1,5 m e largo 1 m, attore a non più di 2,3 m, una sola persona dietro | §7 «geometria della demo», con **1,7 m** (V7 corregge 1,5); §5 (chiuse) |
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
| AU-9 | l'avvio presume una scena vuota e ferma | §1.1 (taratura a scena vuota; posa dal metro; non parte oltre 1°) |
| AU-10 | banda stereo senza dato accanto all'ombra (5–9,5 cm), errore non simmetrico | K-215 nel §5 (errore della maschera al bordo, primo sensore); [prel.] nessuna asimmetria a 424 pixel |
| AU-11 | soglia di 0,07 m e campo della scheda; pixel minimi per «occupato» non scritti | §1.1 (stampa di risoluzione e campo); §1.2 (almeno 3 pixel); `sd-K4` |
| AU-12 | le costanti nascondono pedone, sala, sensore fermo, pavimento | §3 (quattro regole su nove; due profili); §1.9; §7 |
| AU §2 | che cosa un lettore può credere dimostrato e non lo è; la riga per il giurato | §0; §3 («non si dice mai»); §7 («da dire per primi»). La «prova scelta dal giurato»: **altro ruolo** (demo) |

## 3. Verdetto f7 (V7): mappa voxel e traccia

| Sigla | Che cosa chiede | Dove nella versione 3 |
|---|---|---|
| V7-a | il «libero» della cella va riscritto (K-107) | §1.2 (V-018, ripiego a 0,20 m); K-107 nel §5 |
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
| V7 §1, tabella | «libero» senza memoria (V-018; ripiego `stato` a 0,20 m) | §1.2; I1 |
| V7 §1, tabella | affidabilità persa contata sui pixel validi | §1.9 |
| V7 §1, tabella | `stato(p)` per la previsione, letta a 0,20 m | §1.2 (ripiego e maschera del «non visto libero»), §1.6 |
| V7 §1, tabella | registro degli eventi con «come lo so» | §1.11; I14 |
| V7 §1, tabella | V-017, V-016, V-019, T-008: serve il secondo autore; 4 ore | §4 (4 ore, se confermate); T-008 anche in §1.11 |
| V7 §2 | struttura a tre assi (applicazione, portatore, uscita) | §1 (sotto lo schema); §3 |
| V7 §2 | ambito: il testo riscritto dall'attacco (A7 §3.8) | **altro ruolo** (documento di due pagine); la coda «provato solo al calcolatore…» è nel §7 |
| V7 §2 | veicolo senza equipaggio = valore dell'asse «portatore», sempre con «fermo» o «non provato» | §3, tabella dei profili |
| V7 §2 | S11 riformulata: `SOSTA_IN_OMBRA` diventa «non ricomparso da n s (dedotto)» | §1.11; §6 (da rinominare nel codice) |
| V7 §2 | coperte solo a parole: «oggetti», «ispezione», «aerospaziali», «Intelligenza Artificiale», «bassa latenza» | §3 («non si dice mai»); §1.10 (latenza non risolta) |
| V7 §2 | demo: pannello alto almeno 1,7 m, a 1,7–1,9 m, attore a 2,3 m; K-111 | §7; K-111 nel §5 |
| V7 §3 | K-102 (il cuneo nasconde chi si vede dietro un ostacolo basso), K-105 («liberi» occupati entro 0,20 s: mai «via libera», onesto fino a 1,4 m/s) | §7; I12; §1.7 |
| V7 §3 | K-106, K-107, K-109, K-110, K-111 aperte; K-108 (ore) | §5; K-108: **altro ruolo** (piano) |
| V7 §4 | contratto d'uscita e quattro regole identiche su nove | §3 |
| V7 §4 | i due profili differiscono in canale d'uscita e reazione alla perdita (C5); nome del secondo (C6); frase della prova (C1); limite (C8); vuoto vicino (C2); 1,4 m/s (C4); pannello a non meno di 1,7 m di distanza (C3) e alto 1,7 m | §3; §1.5; §1.7; §7 |
| V7 §4 | elenco di ciò che resta «non provato» | §3 (tabella), §7 |
| V7 §5, §6 | quattordici affermazioni convergenti; affermazioni da non fare | §3, §7; **altro ruolo** per il documento |
| V7 §7 | prossima prova: V-017 e V-018 sullo stesso banco; poi la stanza ferma per 60 s | K-107, K-106 nel §5 (criterio C-D) |
| A7 §3.1 | regola del «libero» con almeno 3 pixel e quota letta | §1.2 |
| A7 §3.2 | frase d'uscita con q letta; «senza una parete entro la portata la quota verificata scende a 0,6 m» | §1.2 (la quota entra solo con V-017, nelle 4 ore: il limite va scritto allora) |
| A7 §3.3 | sensore non in salute; rilascio «oltre la fascia» | §1.9; §1.7 |
| A7 §3.4 | C2 nello pseudocodice | §1.5 |
| A7 §3.5 | assetto entro 1°; controllo del piano | §1.1, §1.9 |
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
| c1 | riaggancio: prima misura non tagliata entro 0,40 m da R90 e 0,75 m dall'ombra d'ingresso | §1.8, **condizionata** alla prova contro l'estraneo; K-218, K-219 |
| c2 | le pendenti ambigue diventano un solo avviso e non bloccano il riaggancio | §1.7, §1.8; `sd-K3` per «le azzera l'operatore» |
| c3 | «gruppo tagliato» definito sull'immagine | §1.3 (col sensore; fino ad allora la cifra vale «con la maschera esatta»: K-215) |
| c4 | entrata dopo due cicli senza misura; subito se il gruppo è tagliato | §1.5; K-220 |
| c5 | sotto 0,3 m/s d'ingresso subito «ampio» | §1.6 («fermo negli ultimi 2 s»: non provata, non adottata) |
| c6 | il gruppo tagliato a contorno pieno, «visto in parte», senza velocità | §1.3; §1.10 |
| c7 | traccia chiusa o non confermata entro 0,75 m da un'ombra accende l'avviso | §1.5 (non provata) |
| c8 | soglia di «ampio» sulle sole celle d'ombra; in «ampio» niente croce | §1.6; §1.10 |
| c9 | libreria di almeno 200 percorsi; «sul percorso» = rotta entro 3 °/s | §1.6 (parametro); §1.12; K-221. Raffinamento |
| c10 | evidenza negativa solo su celle libere negli ultimi 3 fotogrammi; in moto «ampio» | **esclusa**: dopo l'hackathon (§4) |
| statistico-3 | un denominatore («nascosti dentro l'area osservata») e la regola di Wilson | §1.12 |
| statistico-4 | il tabellone conta la persona dentro la regione a 1 e a 2 s | §1.12 |
| statistico-5 | «almeno 9 su 10» fino a 2 s, «almeno 8 su 10» fino a 3 s, poi «ampio» | §1.6; §1.10 (etichetta) |
| statistico-6 | libreria da almeno due persone a tre andature | §1.6, §1.12 (registrazione nelle 14 ore, prova nelle 4) |
| statistico-7 | riparare il seme del generatore prima di ogni nuovo lancio del banco | §6 (avvertenza); §4 (dopo, salvo nuovi lanci) |
| V8 §4.1 | c7 per prima (sicurezza) | §1.5 |
| V8 §4.2 | c1, e prima la prova contro l'estraneo | §1.8; K-219 |
| V8 §4.3 | c2 | §1.7, §1.8 |
| V8 §4.4 | c4 | §1.5 |
| V8 §4.5 | c3; finché manca, «con la maschera esatta» | §1.3; §1.6 (stato); §7 |
| V8 §4.6 | c5 | §1.6 |
| V8 §4.7 | c6 e c8 | §1.3, §1.6, §1.10 |
| V8 §4.8 | le tre righe dello statistico | §1.6, §1.12 |
| V8 §4.9 | la chiusura «fuori dall'area osservata» non toglie l'avviso | §1.7; `sd-K6` |
| V8 §4.10 | nel raffinamento c9 e statistico-6; dopo c10 e statistico-7 | §1.6, §1.12; §4 |
| V8 §4 | manca la prova d'insieme | §0; criterio C-C: **altro ruolo** |
| V8 §5 | sd-0 o sd-1 (decisione dell'utente); sd-0 per primo | §1.6 |
| V8 §5 | della preproposta (C-EST): S3 e S4 non entrano; di S5 entrano contorno pieno solo con una misura, inviluppo tratteggiato ritagliato, età | §4; §1.10 |
| V8 §5 | ciò che non si può dichiarare | §3 («non si dice mai») |
| V8 §3 | K-202, K-214, K-215, K-218, K-219, K-220, K-221 aperte; K-016 non riparata | §5; §7 |
| V8 §6 | otto affermazioni per la giuria | §7 (forma più forte e «dove cede») |
| V8 §7 | prossima prova: c1–c5 e c7 insieme, semi nuovi, estraneo, corpo esteso a −10 cm | **altro ruolo** (C-C); esiti attesi nel §5 |

## 5. Verdetto f9 (V9): preproposta esterna

| Sigla | Verdetto | Dove nella versione 3 |
|---|---|---|
| S1 | forma minima approvata (controllo all'avvio, configurazione dichiarata, mappa fissa); forma completa **respinta** | §1.1; I11; completa: **esclusa**, §4 |
| S2 | approvata con correzioni: età dichiarata; compensazione solo sull'uscita | §1.10 (età nelle 14 ore; compensazione nelle 4, mai in ombra); I3; §4 |
| S3 | approvata solo come informazione, una ipotesi; seconda ipotesi solo se batte l'orologio | §1.6 (una ipotesi); «non riemerso» in §1.11; seconda ipotesi: **esclusa**, §4; `sd-K1` |
| S4 | (a) ritaglio sul visto libero con fascia: approvata; (b) pesi a ogni ciclo e (c) soglia 0,8 m: **respinte** | (a) §1.6, I4; (b), (c): **escluse**, §4 |
| S5 | disegno approvato (trama e parola prima del colore; l'area non sparisce; un decimale; mai verde); etichetta «± \| conf» **respinta** | §1.10; etichetta: **esclusa**, §4 |
| S6 | formule approvate come etichetta; «probabilità d'intrusione» **respinta** | §1.10 (4 ore); **esclusa**, §4 |
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

## 7. Misure di f10 che toccano un parametro — tutte [prel.], ricontate da V10 salvo dove V10 dice «lette e non ricontate»

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

## 8. Verdetto f10 (V10): difetti F-401…F-413, condizioni, contraddizioni

V10 chiama i difetti «ingressi obbligati per la soluzione integrata» e le loro correzioni «non provate»: la versione 3 registra ogni difetto dove tocca una regola, e non adotta una correzione non provata.

| Sigla | Che cosa dice | Dove nella versione 3 |
|---|---|---|
| F-401 | la persona si fonde col pannello (90 passaggi su 90); correzione: soglia proporzionale, non provata | §1.3 (stato); `sd-K4`; §4 (coda): non adottata |
| F-402 | il riaggancio accetta gruppi tagliati e l'occlusore stesso | §1.8: candidato = misura non tagliata (c1); escludere l'occlusore è proposta non provata |
| F-403 | fantasmi del pavimento: «una sola traccia pendente» non è mai vera | §1.8 (stato); §1.1 (prima misura col sensore) |
| F-404 | con la posa sbagliata di 1° un ostacolo basso è «libero» | §1.1 (non parte oltre 1°; prova d'ingresso); §7 |
| F-405 | un ostacolo che non rimanda profondità è «libero» | §1.2 (controesempi); §7: limite dichiarato, come il vetro |
| F-406 | i filtri del costruttore tengono vivo il «libero» | §1.1 (condizione 1) |
| F-407 | «libero» per memoria su una cella che era occupata | I1: nessuna memoria; §6 (la catena f10 va corretta) |
| F-408 | dopo un riaggancio tagliato il filtro non si aggiorna (5,00 m) | §1.8 (il riaggancio parte da una misura non tagliata); §4 (coda); §6 |
| F-409 | al riaggancio l'avviso si spegne anche se nell'ombra resta qualcuno; q non si tara sulle innovazioni alla ricomparsa | §1.7 (controesempio K-016); §4 (coda); §1.4 (regola su q) |
| F-410 | ostacolo sospeso vicino: non visto, e sotto è «libero» (97,5 %) | §7; `sd-K2` (per questo la frase dice «suolo») |
| F-411 | la regione del filtro non informa; la velocità costante sbaglia su chi si ferma | §1.4 (il cerchio non è la precisione); §1.6 (predittore di f8); q = 0,1: §4 (coda) |
| F-412 | le soglie di pixel sono assolute | §1.2 (parametro); `sd-K4` |
| F-413 | il vuoto vicino è una striscia: a ±44° il suolo si vede da 1,69 m | §1.1 (zona valutata = celle che ricevono suolo all'avvio) |
| V10, cambi di stato | identità «100 %» smentita su profondità realistica; muro «mobile» smentita; q corretto verso 0,05–0,1; K-014 sostenuta a posa esatta | §0; §1.8, §1.3, §1.4, §1.2; §7 |
| V10, condizioni 1–9 | 1 confermata necessaria; 3 corretta (1,5 m non basta; proposta 1,8 m); 4 stretta (posa entro 1°); 5 non basta; 6 «una traccia pendente» falsa su profondità realistica; 7 più F-404, F-405, F-410; 9 dicitura nuova | §1.1; §7 (geometria: almeno 1,7 m, 1,8 m se c'è; dicitura); §1.3; §1.8; §7 |
| V10 K-401…K-407 | K-401 copertura per passaggio (83 su 90); K-402 dominio stretto; K-403 soglia = rapporto coi pixel; K-404 bordo d'ombra; K-405 rumore a due gruppi; K-406 fantasmi = margine fra 5 e 7 cm; K-407 simulatore ottimistico sui buchi | K-401: §1.12 (si conta per passaggio); K-402: §1.2, §7; K-403: `sd-K4`; K-404: K-215 nel §5; K-405: §1.3; K-406: §1.1 (posa); K-407: §6, §7 |
| V10 §5 | sei affermazioni per la giuria; «da non dire» | §7; §3 («non si dice mai») |
| V10 §6 | prova senza sensore (F-401, F-402 a 424 e 848 pixel); tre prime misure col sensore | §1.8 (criterio); `sd-K4`; §7 |
| V10, decisioni dell'utente | telefono e inventario; dati con occlusioni lunghe; che cosa promettere sull'identità e su q | **altro ruolo** (piano e documento); q: §1.4 |
