# PREVISIONI — sciame-creativo, f1, corsia B

Scritte PRIMA di ogni prova. Ora di registrazione (date -Is): 2026-11-14T13:11:50+01:00

Strumento delle prove: una simulazione numerica in Python puro (senza numpy), 1D lungo un corridoio, su CPU, sotto i 60 s. Classe 2.
Indipendenza dichiarata: simulazione, filtro e previsioni hanno lo stesso autore (io) e lo stesso modello linguistico; la «verità» simulata usa però un modello del moto DIVERSO da quello del filtro (rallentamenti e soste tirati da una distribuzione che il filtro non conosce). Nessun dato reale, nessuna persona: le prove dicono se il meccanismo è coerente, non se funziona sul sensore vero né se una persona lo percepisce.

## P-creativo-2a (evidenza negativa, «sottomarino perduto») — bersaglio che si FERMA dietro l'occlusore
- Scena: bersaglio a 1,2 m/s lungo x; occlusore che nasconde x in [3, 5] m; il bersaglio entra e si ferma a x = 4 m. Misure a 15 Hz, sigma 0,05 m, solo fuori dall'ombra, Pd = 0,9.
- Misura: quota di massa di probabilità della posizione che, 3 s dopo l'ingresso nell'ombra, cade in celle che il sensore sta osservando LIBERE (cioè «previsto» messo dove si vede che non c'è niente).
- Previsione: (A) Kalman a velocità costante in coasting: quota >= 80 %. (B) filtro a particelle con modello fermo/in moto e aggiornamento per mancato rilevamento: quota <= 10 % e massa nell'ombra >= 90 %.
- Soglia di smentita: (A) < 50 % (il difetto che l'idea cura non esiste) oppure (B) > 25 % (la cura non funziona).

## P-creativo-2b / P-creativo-3 (la «buca dichiarata») — bersaglio che ATTRAVERSA
- Scena: 400 passaggi; velocità d'ingresso 0,8–1,6 m/s; dietro l'occlusore, con probabilità 0,3 rallenta del 0–40 %, con probabilità 0,1 sosta 0–3 s (distribuzione ignota al filtro).
- Misura: copertura dell'intervallo al 90 % dell'istante di riemersione, sigillato dal filtro B al momento dell'ingresso nell'ombra.
- Previsione: copertura fra 75 % e 97 %. Per confronto, l'intervallo al 90 % del Kalman CV (A): copertura < 75 % (troppo ottimista, perché ignora soste e rallentamenti).
- Soglia di smentita: copertura di B < 70 % (la scommessa sigillata farebbe brutta figura davanti alla giuria) oppure A >= B (l'idea non aggiunge niente al Kalman).

## P-creativo-4 (attenzione a bilancio, «ronzio terminale» del pipistrello)
- Scena: 6 bersagli in 1D con velocità a passeggiata casuale; a ogni passo si può misurare UN solo bersaglio (bilancio di sensore/calcolo); uno dei sei è in rotta verso l'utente.
- Misura: errore quadratico medio di posizione sul bersaglio più minaccioso (tempo al contatto minimo) negli ultimi 2 s prima del contatto, su 300 scene.
- Previsione: la politica «guarda dove varianza / tempo al contatto è massima» riduce l'errore di almeno il 30 % rispetto al giro a turno.
- Soglia di smentita: riduzione < 10 %.
- In più (controllo di fonte): la scheda tecnica del ToF multizona VL53L5CX dichiara 4x4 zone fino a 60 Hz e 8x8 fino a 15 Hz. Smentita: valori diversi nella scheda ST.

## P-creativo-1 (tre timbri e battito, segnalamento ferroviario a sicurezza intrinseca) — NON eseguibile da me (servono persone e audio)
- Prova prevista (5 minuti, da fare alla squadra): 3 persone bendate, 60 s di addestramento, 20 stimoli casuali fra «osservato» (clic nitidi), «previsto» (stesso ritmo, suono sfocato) e «sconosciuto» (battito sospeso + ronzio grave).
- Previsione: riconoscimento >= 90 % (54 su 60). Soglia di smentita: < 80 % (48 su 60).
- Prova del cane da guardia: sospeso il processo di percezione (SIGSTOP), il battito tace entro 2 periodi (<= 1 s con periodo 0,5 s). Smentita: il battito continua (il «libero» sopravvive al guasto).
- Stato atteso alla consegna: non risolto, non verificato.

## P-creativo-3bis (finestra tarata sulle prove generali, «taratura del meteorologo») — aggiunta DOPO aver visto l'esito di 2b/3
Ora di registrazione (date -Is): 2026-11-14T13:14:26+01:00. Nota: questa previsione nasce da ciò che ho notato dopo la prima prova (la finestra del filtro B copre il 100 % ma è larga 6,3 s: inutile come scommessa; quella del Kalman è stretta ma copre il 69 %). È scritta prima di eseguire sim2.py.
- Scena: stessa «verità» di 2b; 100 passaggi di taratura e 300 di prova. Finestra = quantili empirici 5 %–95 % del rapporto (tempo vero di riemersione) / (tempo nominale = larghezza dell'ombra / velocità stimata all'ingresso), misurati sui 100 passaggi di taratura.
- Previsione: copertura sui 300 passaggi di prova fra 85 % e 95 %; larghezza mediana della finestra <= 2,5 s.
- Soglia di smentita: copertura < 80 % oppure larghezza mediana > 4 s.
- Limite dichiarato: taratura e prova vengono dalla stessa distribuzione simulata; nella realtà la distribuzione delle prove generali può non essere quella della demo.

---
# ESITI (scritti DOPO le prove; ora di registrazione: 2026-11-14T13:17:23+01:00)
Prove: sim.py eseguito fra 13:13:26 e 13:13:30; sim2.py concluso alle 13:14:26. Uscite integrali in esito_sim.txt ed esito_sim2.txt.

| Previsione | Misura | Esito |
|---|---|---|
| P-creativo-2a (A >= 80 %; B <= 10 % e ombra >= 90 %) | a 3 s: A = 100,0 %; B = 0,11 % in celle libere, 99,89 % nell'ombra | regge |
| P-creativo-2b/3 (B fra 75 % e 97 %; A < 75 %) | B = 100,0 %, larghezza mediana 6,27 s, 27 finestre aperte su 400; A = 69,3 %, 0,40 s | A regge; B smentita in alto (fuori banda), soglia di smentita < 70 % non scattata |
| P-creativo-3bis (85–95 %; <= 2,5 s) | 91,7 %; 1,24 s | regge |
| P-creativo-4 (riduzione >= 30 %) | 48,4 % (0,060 -> 0,031 m) | regge |
| P-creativo-4, scheda VL53L5CX (4x4 a 60 Hz, 8x8 a 15 Hz) | confermato solo dal riassunto di una ricerca sul manuale ST UM2884; pagina ST in timeout | non risolta (non verificata sul testo) |
| P-creativo-1 (persone bendate; cane da guardia) | non eseguita | non risolta |

Notato dopo, non previsto:
- in 2a il filtro B' (stesso modello fermo/in moto, senza aggiornamento per mancato rilevamento) lascia il 90,1 % della massa in celle osservate libere a 3 s: l'ingrediente che conta è l'evidenza negativa;
- in 4 la politica a priorità peggiora l'errore sugli altri bersagli del 158 % (0,059 -> 0,151 m);
- la finestra larga di B viene dalla coda delle soste del suo modello (circa il 12 % delle particelle si ferma in 25 passi e riparte in media dopo 6,7 s): spiegazione mia, non provata con un'ablazione.
