Canarino: sciame-canarino-8f9353395a6192ab

# Revisione avversariale della mappa voxel (`sciame-rovesciatore`, f7, corsia B)

**Esito in tre righe.** La terza dimensione serve: il «libero» del nucleo è un'affermazione sul suolo, non sulla colonna sopra il suolo. La mappa voxel probabilistica e sparsa, invece, non serve alla prima dimostrazione: con il sensore fermo tutto ciò che di sicuro sa dire si legge nell'immagine di profondità corrente, a un costo da 57 a 540 volte più basso (sulla zona del nucleo, fino a 3 m), e la memoria del «libero» non ha un uso ammesso dalle regole del nucleo. Non sono riuscito a smontare tre cose: il beneficio della lettura 3D, il costo quasi nullo della struttura sparsa, l'utilità di una mappa su una piattaforma in moto con la posa nota.

## 1. Scostamenti e regole violate

- **Programma cambiato dopo aver visto i primi esiti.** Nella prima esecuzione (`rovescia_prima.c`, `risultati_analisi_prima.txt`) le superfici della scena cadevano sui bordi dei voxel e sporcavano due conteggi (materia dentro i «liberi», effetto della posa). Ho spostato l'origine della griglia di 1–2 cm e rilanciato (`risultati_analisi.txt`). Aggiunti dopo, senza previsione: la parete a 4 m, la divisione per causa dei voxel misti, δ = 0,1°.
- **Previsioni P7, P8, P9 scritte dopo P1–P6**, ciascuna prima della propria prova (ore in `PREVISIONI.md`: 15:08:04, 15:17:06, 15:18:15).
- **Tempi su una macchina condivisa** con altri agenti (carico medio 3–4). La prima serie (`risultati_tempi.txt`) è bimodale e fino a due volte più lenta; uso la seconda (`risultati_tempi_2.txt`), stabile. L'attraversamento dei raggi è scritto in modo diretto, non ottimizzato, a un thread.
- **Non letti:** `MISURE*.md`, `CONTROPROVE.md`, `AUDIT.md`, `SPECIALIZZAZIONE.md`, `QUADRO_DOMINIO.md`, i PDF. Nessuna fonte in rete: «ritorno valido fino a 6 m» è un'ipotesi mia sul sensore, **non verificata**.
- **Indipendenza.** Le prove condividono con ciò che controllano: l'autore, la camera ideale (niente rumore, niente pixel misti, niente vetro), la scena sintetica. La regola «libero» del nucleo l'ho riscritta io da `SOLUZIONE_V2.md` (blocco B2), non è il codice della validazione. Vale per la geometria e per l'ordine di grandezza dei costi su questa CPU.
- Delle dieci prove di falsificazione ho misurato solo la 6 e la 10; le altre sono discusse per lettura.
- **Lunghezza:** circa tre pagine (il conteggio è in `stato.md`).

**Rifare:** `sh rifai.sh` nella cartella (quattro lanci, ciascuno sotto i due minuti, scena deterministica).

## 2. Critiche, ciascuna con la prova

Scena: camera a 1,2 m inclinata di 15°, 87° × 58°, 640 × 480 raggi; regione 4 × 6 × 3 m; pannello da 1 m a 1,83 m, scatola alta 0,20 m, barra a quota 1,75–1,90 m, oggetto in volo; parete di fondo a 5,5 m, a 4 m o assente; scena «peggiore» = stanza vuota.

**1. Con il sensore fermo la mappa è una copia a bassa risoluzione dell'immagine di profondità.** Lo stato di un punto dello spazio (libero osservato, superficie, in ombra, senza ritorno valido, fuori campo) si ottiene proiettandolo nell'immagine e confrontando la distanza: una lettura, nessuna mappa. A 5 cm i voxel «liberi» sono 113 718 attraversando i raggi, 105 003 leggendo il centro, 96 767 chiedendo tutti i 64 sottopunti (`risultati_analisi.txt`). La mappa aggiunge solo ciò che il fotogramma corrente non contiene: la memoria.

**2. L'attraversamento dei raggi crea «liberi» che contengono volume non osservato.** Fra i voxel etichettati «libero», quelli con almeno un sottopunto su 64 non osservato sono il **28,1 %** a 10 cm e il **14,9 %** a 5 cm; quelli non osservati per più di metà sono 2229 e 8746; quelli con dentro un pezzo d'ombra 1073 (7,2 %) e 4265 (3,8 %); quelli che intersecano materia vera 6 e 62 (0 e 52 nella prima esecuzione). È il principio «una zona non osservata non è mai libera», violato alla scala del voxel. Il meccanismo dei voxel con materia non l'ho isolato.

**3. Il costo è l'attraversamento, non la struttura dati.** Circa 7,3 ns a voxel visitato. A piena risoluzione: 72 ms (10 cm) e 141 ms (5 cm) a fotogramma nella scena demo, 90 e 176 ms nella peggiore: sopra i 66,7 ms dei 15 cicli al secondo. Con un raggio su quattro: 19 / 36 ms e 23 / 44 ms (griglia densa; p95 entro 2 ms dalla media). Il nucleo dichiara già la latenza non risolta, con circa 155 ms di media contro un limite di 150 (`SOLUZIONE_V2.md`, §7, R7): ogni millisecondo aggiunto nel percorso critico la peggiora.

**4. «Sparso = efficiente» è un falso problema, in entrambi i versi.** Voxel teorici: 72 000 a 10 cm, 576 000 a 5 cm. Griglia densa: 72 e 576 kB a un byte; 864 kB e 6,9 MB con lo stato di promptMare §4 (12 byte). La tabella hash di blocchi 8³ risparmia da 1,3 a 4,9 volte (2,4 MB contro 6,9 nella scena demo a 5 cm) e costa in tempo dal 3 al 13 % in più. Nessuna delle due cifre è un vincolo su un portatile. Il dilemma vero: se il libero osservato si memorizza, i blocchi allocati sono il 33–52 % (5 cm, con parete) e la struttura è poco sparsa; se non si memorizza (10–14 % dei blocchi, 1,0–1,9 % dei voxel), il libero va letto dall'immagine, cioè dalla critica 1.

**5. La credenza bayesiana sul «libero» non ha un uso ammesso.** Per gli invarianti 1 e 5 del nucleo, «libero» esiste solo se visto negli ultimi 3 fotogrammi e nessun timer lo produce: un log-odds negativo più vecchio di 0,13 s non può uscire come «libero». L'unico uso che resta è frenare un'occupazione nuova, cioè la prova di falsificazione 5. Conto con parametri miei, d'uso comune e non verificati (+0,85 al colpo, −0,4 all'attraversamento, limiti −2 e 3,5): un voxel a −2 torna sopra zero dopo 3 colpi, cioè 0,2 s a 15 Hz, su un requisito di 0,3 s (R5). **Deduzione dai testi, non misura.**

**6. Senza posa la mappa che accumula sbaglia nel verso pericoloso.** Integrando un fotogramma con un errore d'imbardata non compensato di 0 / 0,1 / 0,5 / 1 / 2°, i voxel colpiti al fotogramma prima che ricevono solo evidenza di «libero» sono 0 / 3 / 32 / 228 / 1339 (5 cm), e i «liberi» con materia vera 62 / 62 / 75 / 273 / 1378. La griglia per fotogramma non accumula e non ha questo difetto, per costruzione (lo dice anche `MOTO_PROPRIO.md`, §1).

**7. Critica al nucleo: il suo «libero» copre il suolo, non il corpo.** Nelle 948 celle che la regola del nucleo dà «libero» fra 1,3 e 3 m, la parte della colonna 0,07–2,0 m attraversata da un raggio con ritorno valido più lontano è in media il **72,9 %** con la parete a 4 m, il **54,2 %** a 5,5 m, il **41,2 %** senza parete (25,2 % a 2,9 m). Il resto è assenza di rilevamento, che l'invariante 6 del nucleo vieta di contare. Per conto: il tetto del campo a 3 m è 1,95 m, quindi nessuna cella ha la colonna intera osservata. La cella sotto la barra in quota è «LIBERO» nel nucleo; la lettura 3D a 1,80 m dà «fuori campo». Dietro la scatola bassa l'ombra vera sul suolo è lunga 3 celle, il nucleo ne dichiara 8 fino al bordo; 135 celle «in ombra» su 541 hanno il suolo visto. La frase «il cuneo arriva sempre al bordo della portata» (blocco B5) è **smentita** per ostacoli più bassi del sensore o sospesi.

**8. Critica al criterio.** «Meno memoria di una rappresentazione densa equivalente» e «prestazioni compatibili» (promptMare §14, contratto, criterio 1) non sono benefici rispetto al nucleo: il primo si confronta con un'alternativa che nessuno propone, il secondo è un vincolo. Un SÌ fondato solo su questi due sarebbe vuoto.

**9. Sulla traccia (Q2).** «Monitoraggio di attività e oggetti» descrive una stazione che osserva: il sensore fermo è il caso della traccia, non una limitazione di cui scusarsi. L'unico beneficio della mappa che resiste (punto 3 sotto) riguarda la piattaforma in moto, che la traccia non chiede.

**Dove non ho smontato l'ipotesi voxel.**
1. Rappresentare la visibilità in tre dimensioni è un beneficio vero (critica 7): corrisponde ai benefici 2 e 3 del criterio. Ho mostrato solo che non richiede una mappa memorizzata.
2. La struttura sparsa non costa quasi niente in tempo e risparmia memoria: la mia previsione «1,3–4 volte più lenta» è smentita.
3. Su una piattaforma in moto con posa affidabile, fondere più punti di vista richiede una mappa: l'immagine corrente non basta. Non l'ho attaccato con una misura.
4. La memoria dell'occupato (struttura fissa, oggetti usciti dal campo) richiede un contenitore volumetrico: la concedo in rovesciatore-2.

## 3. promptMare.txt: che cosa tengo, che cosa scarto

- **Utili:** §2, ultima frase («non assumete che lo sparso sia più efficiente»: giusta, misurata); §3, alternative A e D; §4, il «problema obbligatorio» storia contro garanzia corrente (è il nodo: critica 5); §5, la domanda se memorizzare i voxel in ombra o ricavarli con interrogazioni geometriche (risposta misurata: interrogazioni, 0,33 ms) e la possibile presenza come regione geometrica; §9, §10, §12, il divieto d'inventare misure.
- **Inutili per la prima dimostrazione:** octree e formati CSR/COO (§3: con 0,9–6,9 MB densi non c'è un problema di memoria da risolvere); lo stato a sei dimensioni per il veicolo in moto (§6); il formato in dodici capitoli (§13).
- **Sbagliate:** la domanda finale misura il beneficio «per applicazioni UAV», che la traccia non nomina; §14 ammette come beneficio la memoria rispetto al denso (critica 8); §4 dà per scontato che conservare la storia del libero abbia valore (critica 5).

## 4. Stati proposti

| Enunciato | Stato |
|---|---|
| La struttura sparsa è più lenta della densa | **smentito** (1,03–1,13 volte, otto configurazioni) |
| La struttura sparsa risparmia memoria sul denso | **sostenuto dai dati** (1,3–4,9 volte), non è un vincolo |
| L'aggiornamento a raggi a piena risoluzione sta nei 15 Hz | **smentito** su questa implementazione; **non risolto** in generale (lo decide un'implementazione ottimizzata misurata) |
| I «liberi» da raggi contengono volume non osservato | **sostenuto dai dati** (14,9–28,1 %) |
| Un errore di posa produce falsi liberi nella mappa che accumula (prova 6) | **sostenuto dai dati** nel modello |
| La credenza sul libero non ha un uso ammesso in uscita | deduzione dagli invarianti 1 e 5; **non verificato** con una prova |
| Il «libero» del nucleo vale per la colonna 0,07–2 m | **smentito** nel modello (41–73 %; dipende dall'ipotesi dei 6 m) |
| «Il cuneo arriva sempre al bordo della portata» | **smentito** per ostacoli bassi o sospesi |
| Trasferibilità a piattaforme in moto | **non risolto**: manca la posa; la decide la prova 6 con una posa stimata vera |

Previsioni: reggono P6, P7, P8, P4 (senza parete e barra). Smentite: P2 nella parte sulla tabella hash; P4 con la parete a 5,5 m (54,2 % contro 80–95 %: oltre 24° d'azimut la parete supera i 6 m); P5 nella parte «più di 500 a 1°» (228). Fuori intervallo senza che scatti la smentita scritta: P1 (33 % dei blocchi contro 50–70 %), P3 (28,1 % contro 5–20 %), P9 (15 voxel contro 5). I tempi di P2 superano l'intervallo previsto a piena risoluzione.

## 5. Proposte

**rovesciatore-1 — visibilità 3D senza mappa.** Per ogni cella della griglia polare del nucleo, fasce di quota da 5 cm fra 0,07 e 2,0 m, lette nell'immagine di profondità corrente. L'uscita «libero» diventa «libero fino a quota h»; sopra h è «non osservato».
- *Guadagno:* chiude la critica 7 (R2, R4, R8); ombre finite degli ostacoli bassi; un oggetto sospeso ha una fascia sua. Costo misurato: **0,33 ms** per 61 074 letture; memoria: la sola immagine (1,2 MB).
- *Prove di falsificazione:* 1, 2, 3, 5, 6, 10 superate per costruzione (niente allocazione, niente decadimento, niente blocchi, niente dati vecchi, niente posa, costo fisso); 9 per costruzione (sensore coperto = nessun ritorno valido ovunque); 4 e 7 restano quelle del nucleo; 8 (vetro) **non risolta**.
- *Che cosa perde:* ogni memoria oltre quella del nucleo; la fusione di più punti di vista.
- *Vincoli:* la parte fissa (tetto del campo) si dichiara una volta all'avvio, come l'anello cieco, per non saturare il messaggio.
- *Chi la prova:* validazione, sul simulatore del nucleo.
- *Falsificatore (P8, previsione scritta prima):* se meno del 20 % delle celle «libero» ha la colonna osservata fino a 1,5 m con la parete a 4 m, la lettura dice «non osservato» quasi ovunque e non serve. **Esito: regge** (83,1 %; 40,3 % a 5,5 m; 16,6 % senza parete: in uno spazio aperto la proposta avvisa quasi sempre, e va detto).

**rovesciatore-2 — memoria del solo occupato, densa, senza raggi.** Se si vuole una memoria volumetrica: griglia densa da 2 byte a voxel (stato ed età), in cui entrano solo i punti d'arrivo dei raggi validi. Il «libero» non si memorizza mai. Un occupato ricordato si rilascia solo se visto attraverso per 3 fotogrammi e mai per tempo; la possibile presenza resta la regione geometrica del nucleo.
- *Guadagno:* «occupato ricordato» in 3D con l'età a **1,17 ms** a fotogramma (contro 141–176 ms dell'attraversamento a 5 cm), più 0,04–0,07 ms di controllo; 1,15 MB. Nessun falso libero nuovo per costruzione; un errore di posa sposta un occupato (verso prudente).
- *Vincoli:* sensore fermo, o posa affidabile. Che la struttura fissa ricordata aiuti la regola «mobile» è un'ipotesi non provata.
- *Chi la prova:* scene dinamiche e avversario.
- *Falsificatore (P9):* voxel appena inseriti che la regola di rilascio dà per «visti attraverso» nello stesso fotogramma; attesi al più 5, smentita oltre 30. **Esito: non regge l'intervallo, la smentita non scatta** (15 su 5950 con 64 sottopunti; 189 guardando il solo centro, regola da scartare). Serve la clausola «mai rilasciare un voxel colpito negli ultimi 3 fotogrammi», **non provata**.

## 6. Che cosa propongo dopo

1. Risposta a Q1 dalla mia corsia: **SÌ CONDIZIONATO alla sola lettura 3D** (rovesciatore-1); **NO** alla mappa probabilistica sparsa nel percorso critico della prima dimostrazione; la memoria del solo occupato è facoltativa.
2. Alla validazione: rifare la critica 7 con il codice vero del nucleo e con la portata valida misurata sul sensore (la cifra dei 6 m decide il 41–73 %).
3. All'avversario: attaccare rovesciatore-1 con pixel misti ai bordi e buchi di profondità, che la mia camera ideale non ha.
4. Al redattore: «libero» nel documento per la giuria va scritto «suolo visto libero», finché la colonna non è letta.
