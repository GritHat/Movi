# Rivalutazione dei risultati col criterio dell'addendum 14 (f19, `sciame-arbitro`)

2026-11-15, dalle 04:36 (`date -Is`). Previsioni P1–P5 scritte prima, alle 04:36:14, in `PREVISIONI.md`. Riconto con
codice mio: `riconto_f19.py` → `riconto_f19_esito.json`. Rilegge i record per passaggio di
`f15-lunga-portata/60-fase2c/01-correzioni/` (`passaggi_v3.jsonl`, `riprova_passaggi_v3.jsonl`) e ricalcola i Wilson
al 95 % di tutte le cifre citate. Tabella completa, 35 righe: `risultati_classificati.json`.
**Tutto è simulazione dalle schede, conto, o traiettoria pubblica con occlusione simulata. Nessun sensore fisico,
niente è «validato». Le etichette sono messe a mano. Solo osservazione e avviso.**
**Indipendenza:** condivido con gli autori i record, le definizioni dei campi e il modello linguistico. Controllo
l'aggregazione, non la misura.

## 0. In testa

- **Previsioni.** Reggono tutte e cinque.
  - P1: ogni k/n e ogni Wilson dei cinque verdetti torna entro 0,001.
  - P2: E1 51/60 ha limite inferiore 0,739, quindi è INCORAGGIANTE.
  - P3: nel corto raggio nessun LIMITE diventa SOLIDO.
  - P4: gli aerei in volo restano LIMITE.
  - P5: le affermazioni presentabili sono 15.
- **Cambi di stato.** Il criterio nuovo cambia la classe di presentazione, non i fatti. Ciò che i verdetti chiamavano
  «smentito contro la soglia» e che è vicino al sicuro, con un meccanismo noto, ora è **INCORAGGIANTE**: E1 entro 2 s,
  A1 min fuori avviso, A4, S2, le precisioni del corto raggio, l'identità H-502.
- **Fatto nuovo, ricontato da me.** La curva del ritardo di E1 si può presentare come «perdita di tempo» esatta sul
  campione:
  - entro 1,0 s: 0/60;
  - entro 1,5 s: 23/60 [0,271; 0,510];
  - entro 2,0 s: 51/60 [0,739; 0,919];
  - entro 2,5 s: 60/60 [0,940; 1].

  Il ritardo massimo è 2,3 s. È minore dei 4,0 s in cui, nel modello dei frammenti, il primo pezzo può toccare terra.
  Quel modello ha valori non verificati (REGOLE_E_SCENARI_EVENTI, riga 156). La soglia dei 2,5 s l'ho notata dopo:
  non è una previsione.
- **Il caso centrale nuovo oggi non è provato.** Nessuno scenario simula collisione, detriti o esplosione **in volo
  ad alta velocità**:
  - E1 è fra due multirotori a 8 e 6,7 m/s, a 80 m di quota;
  - E2 è un aereo **a terra**, in corsa di decollo a 40 m/s;
  - gli aerei in volo (70–210 m/s) hanno solo il conto della tempestività (LIMITE) e le traiettorie ADS-B senza eventi.

  Per mostrarlo come «simulazione» servono scenari nuovi (§ 4). Fino ad allora è «Schematic».
- **Regole.** Ho scritto solo in `f19-volo/01-rivalutazione/`. Niente rete, git, sudo o cancellazioni. Un processo
  alla volta. **Non riletti:** il codice del nucleo v3, `compara.json` (le cifre delle traiettorie vengono da
  VERDETTO_FASE2, che le aveva ricontate), il prototipo f16/10.

## 1. Corto raggio (camera di profondità, persone)

| # | Frase per la giuria (forma più forte che resta vera) | Classe | Intervallo · base | Limite → miglioria |
|---|---|---|---|---|
| CR-1 | «Ciò che non è osservato non è mai dichiarato libero.» | **SOLIDO**, dimostrato | dimostrazione condizionata: posa entro 0,5°, ostacolo che rimanda segnale | vetro, ostacolo sospeso → radar a corto raggio in fusione; IMU per la posa |
| CR-2 | «In simulazione nessuna cella "libera" sopra un ostacolo in 300 condizioni, due volte.» | **SOLIDO** | errori [0; 0,013] | cede a 1° d'inclinazione → stima della posa a ogni fotogramma |
| CR-3 | «Una persona nascosta ha sempre una zona sullo schermo: 0 interruzioni su 23 402 passaggi.» | **SOLIDO**, per costruzione e simulato | [0; 0,0002]; sensore ideale; prototipo su profondità 0/5820 cicli | manca la prova sul sensore |
| CR-6 | «Su profondità simulata la persona nascosta non è mai uscita dall'avviso (0 su 4324 fotogrammi; 0 su 3608 e 0 su 2360 nelle repliche).» | **SOLIDO** | [0; 0,001] | oltre 3 m è fuori griglia → LiDAR di portata maggiore |
| CR-4 | «Con un ostacolo largo 2 m la persona è nella zona in almeno 92 casi su 100 a 2 s e 90 su 100 a 3 s.» | **INCORAGGIANTE** | limiti peggiori 0,921 e 0,899 | chi svolta 0,57–0,86 → modello a più regimi (dritto, svolta, fermo) |
| CR-5 | «Col pannello da 1 m: almeno 88 su 100 a 1 s.» | **INCORAGGIANTE** | 942/1045 [0,882; 0,918] | oltre 1 s nessuna cifra → come CR-4 |
| CR-7 | «Entro i 3 m la zona contiene la persona: 59/59 a 2 s, 30/30 a 3 s.» | **INCORAGGIANTE** | [0,939; 1]; [0,886; 1] | sui passaggi interi 59/84 [0,60; 0,79]: esce dai 3 m → portata maggiore |
| CR-8 | «Il nome al ritorno, sempre "presunto", è giusto in 176 casi su 180 nel caso semplice.» | **INCORAGGIANTE** | [0,944; 0,991] | fuori dominio 0/10; un estraneo prende il nome 19/20 → re-identificazione dall'aspetto (l'avviso già non ne dipende) |
| CR-9 | «Persa prima dell'ombra: 24 casi su 23 402.» | **SOLIDO** come tasso, con c7 accesa | [0,0007; 0,0015] | 928 con c7 spenta → c7 dopo la prova d'ingresso |
| CR-10 | — | **LIMITE** | tolto il pannello l'avviso resta acceso, 10/10 | correzione del rilascio (K-505) |
| CR-11 | «Con 3 m di portata l'avviso è tempestivo fino a 1,44 m/s.» | **SOLIDO**, calcolato | reazione di 1 s come ipotesi | veicoli no → lunga portata |
| CL-1 | «Il classificatore è richiesto: qui le etichette le mettiamo a mano.» | **NON PROVATO** | — | modello per classe; la regola di sicurezza non lo usa |

## 2. Lunga portata: droni e aerei (più preciso)

Configurazioni e sensori come nei verdetti: radar per droni, pannello, EO e Remote ID; radar di superficie, LiDAR e
ADS-B.

| # | Frase per la giuria | Classe | Intervallo · base | Limite → miglioria |
|---|---|---|---|---|
| LP-1 | «Un drone a 15–21 m/s che sparisce dietro un edificio è annunciato in tempo all'operatore (servono 806 m, confermato a circa 950 m) in 200 passaggi simulati su 200, in due configurazioni, e in 100 su 100 con semi nuovi.» | **SOLIDO** | [0,981; 1] ×2; [0,963; 1]. Pd ipotesi | in alta solo 22/200 passaggi hanno una fase nascosta → Pd e sezione radar misurate |
| LP-2 | «Col nucleo v3 MoVi non ha mai detto "libero" dove c'era il drone: 0 passaggi su 171, con la mappa del sito dichiarata completa.» | **SOLIDO**, con l'ipotesi della mappa | [0; 0,022] | con la mappa sbagliata 5/6 «libero» falso [0,44; 0,97] → la mappa si verifica col LiDAR prima di dichiararla (validazione-3) |
| LP-3 | «Quando il drone rallenta o si ferma, l'avviso lo contiene in 188 passaggi su 200.» | **INCORAGGIANTE** | [0,898; 0,965]; 6 «ferma», 6 «rallenta» | ricentramento su un falso ritorno (K-606, non verificato) → modello a più regimi che non si ricentra |
| LP-12 | «Il limite di velocità copre i droni fino a 45 m/s e gli aerei fino a 210 m/s; passate correlate contate come una.» | **SOLIDO** per costruzione; valori ipotesi | casi costruiti | a 60 m/s il drone esce a 8 s → inviluppo per classe dalle schede (FPV) |
| LP-9 | «Con i sensori di bordo (radar 4D, LiDAR, EO) l'avviso è in tempo in 95 passaggi su 100.» | **INCORAGGIANTE** | [0,888; 0,978] (v2) | 9/100 fuori avviso: il Doppler perde il lento → soglia Doppler per classe e fusione con l'EO |
| LP-14 | «I droni sotto 250 g: "zona non verificata", mai "libero"; annunciati in tempo in 29 su 29.» | esclusione **SOLIDO** per costruzione; tempestività **INCORAGGIANTE** | [0,883; 1] | — |
| LP-13 | «Un radar d'aeroporto non vede un drone sotto la copertura: MoVi non lo chiama mai "libero" (0/200).» | **SOLIDO** per costruzione | [0; 0,019] | tempestività non misurata → radar per droni in fusione |
| LP-8 | «Su 98 voli reali di un multirotore la zona lo contiene almeno 9 volte su 10 fino a 10 s.» | **INCORAGGIANTE**, dati pubblici | un esemplare | ala fissa circa 0,6 a 10 s (LIMITE) → più esemplari; moto in virata coordinata |
| LP-4 | «Aereo in rullaggio dietro un hangar, con radar di superficie, LiDAR e ADS-B: avviso in tempo in 200 passaggi su 200, mai fuori, mai "libero".» | **SOLIDO** (nucleo v2) | [0,981; 1] | v3 non rimisurato; 34/200 con fase nascosta |
| LP-5 | «Col solo radar, 50 su 200: un sensore solo non basta.» | **LIMITE**, argomento per la fusione | [0,195; 0,314] | — |
| LP-7 | «Su 43 aerei reali (ADS-B), dopo 2–30 s senza vederli, la zona conteneva l'aereo in circa 9 casi su 10.» | **INCORAGGIANTE**, dati pubblici | 0,93–0,95; bootstrap per mezzo ≥ 0,87 | con v_max 90 m/s l'avviso perdeva 8–11 aerei su 43; con 210 **non rimisurato** → rifare per fase di volo |
| LP-6 | «Per gli aerei in volo (fino a 210 m/s) l'avviso al sito non arriva in tempo, e MoVi lo scrive.» | **LIMITE**, calcolato | servono 3410 m (16 s a 210 m/s); il «libero» arriva a circa 0,88 km | radar primario o multilaterazione a decine di km, fusi con l'ADS-B; un ricevente con altri tempi di reazione |
| LP-10 | auto 200/200; treni 186/200 | auto **SOLIDO** [0,981; 1]; treni **INCORAGGIANTE** [0,886; 0,958] | — | treni su traiettorie reali: fuori avviso in 18 su 19 (LIMITE) → vincolo di binario; verità ripulita |
| LP-11 | «L'avviso si spegne solo guardando tutta la zona: 0 su 600; la regola ingenua lo spegneva in 564 su 2400.» | **SOLIDO** | [0; 0,006]; [0,218; 0,252] | — |

## 3. Eventi improvvisi e perdita di confidenza

| # | Frase per la giuria | Classe | Intervallo · base | Limite → miglioria |
|---|---|---|---|---|
| EV-1 | «Dopo una collisione fra due droni MoVi ha dedotto l'evento in tutti i 60 passaggi simulati, in 1,2–2,3 s: entro 2 s in 51 su 60.» | **INCORAGGIANTE** | 51/60 [0,739; 0,919]; tipo giusto 50/60 [0,720; 0,907]; evento 60/60 [0,940; 1]. Base: fusione e separazione di tracce, confermate su più cicli | droni lenti; 2/60 dati come «separazione» → rivisita più rapida (EO e termica ad alto frame rate, radar a scansione elettronica), per ridurre i cicli di conferma. Che il ritardo scali col periodo è un'**ipotesi** |
| EV-2 | «Nessun falso evento con due droni a 5 m che non si toccano (0 su 300).» | **SOLIDO** | [0; 0,013] (v1); 0/30 v3 | «prima dell'urto» 0/60 [0; 0,060] con una regola scritta dopo: INCORAGGIANTE |
| EV-3 | «La zona dei detriti ha raggio di circa 4,5 km, mai oltre 5,3 km in 60 passaggi; MoVi non vi dice mai "libero".» | raggio **INCORAGGIANTE**; nessun «libero» **SOLIDO** per costruzione | 0/60 ≥ 10 km [0; 0,060]; frammenti dentro V 0,9973 contro ≥ 0,999 | la zona non si riduce guardando (0/60) → modello balistico della caduta: zona che si restringe nel tempo e chiusura per punto (T_c) |
| EV-4 | «Avaria con fiammata di un aereo in decollo a 40 m/s: evento in 0,2–0,3 s; camere dichiarate non affidabili entro 3 cicli in 90 su 90.» | **INCORAGGIANTE** | [0,886; 1]; [0,959; 1]. La saturazione è presa dal punto vero: innesco ottimista | l'avviso al mezzo non discrimina (circa 96 tracce) → saturazione rilevata dal segnale; impronta orientata lungo la pista |
| EV-5/6 | «Nebbia e pioggia accorciano la portata dichiarata; fumo e detriti in pista non hanno dato falsi eventi (0 su 120).» | **SOLIDO** | E4 [0; 0,031]. E3 per costruzione, non indipendente | — |
| EV-7 | collisione, detriti o esplosione **in volo** a 70–210 m/s, droni oltre 21 m/s | **NON PROVATO** | nessuno scenario | scenari E6–E8 (§ 4) |
| CF-1 | perdita di confidenza nel tempo | **INCORAGGIANTE** dove misurata; forma chiusa **NON PROVATA** | aerei 0,93–0,95 da 2 a 30 s; multirotore ≥ 0,9 fino a 10 s; corto raggio 0,92 a 2 s e 0,90 a 3 s; ala fissa circa 0,6 a 10 s | una curva per orizzonte, da un solo modello (inviluppo più rumore), con Wilson per passaggio, verificata sui dati (compito di `03-confidenza`) |

## 4. Che cosa propongo dopo, per il caso centrale

Le proposte sono ipotesi da provare, con la soglia scritta prima.

1. **E6, urto fra droni veloci in volo** (25–45 m/s, a 80–150 m di quota), riusando lo strato eventi v3.
   - Previsione: evento dedotto entro 2 s in ≥ 45/60.
   - Smentita: < 40/60, oppure un solo «libero» su un frammento.
2. **E7, avaria di un motore in salita** (aereo a 70–90 m/s, sotto i 300 m, coperto da radar e ADS-B), con i detriti
   lungo la traiettoria.
   - Previsione: «affidabilità persa» e evento entro 2 s in ≥ 27/30.
   - Smentita: < 24/30.
3. **E8, drone nel corridoio di finale di un aereo a 70 m/s**.
   - Previsione: «zona non verificata per i multirotori» in ogni ciclo e 0 «libero».
   - Smentita: un «libero».

   Tempestività: per conto si deve dire che non c'è, come in LP-6.
4. **LP-7 rifatto con v_max 210 m/s**, sui 43 aerei.
   - Previsione: avviso fuori in ≤ 2 aerei su 43.
   - Smentita: ≥ 5.
5. **Hardware.** L'unità dedicata accorcia il **calcolo**, non i cicli di conferma né la rivisita del sensore. Nel
   ritardo di E1 (1,2–2,3 s) il termine dominante è quello dei cicli: va dichiarato. È un'ipotesi, da verificare col
   periodo di rivisita come variabile.

## 5. Affermazioni presentabili (al più quindici)

Ogni frase ha la riga fissa «simulazione da schede · etichette a mano · nessun sensore fisico».

1. CR-1. Ciò che non è osservato non è mai dichiarato libero (dimostrazione condizionata).
2. CR-3 e CR-6. A corto raggio una persona nascosta ha sempre una zona sullo schermo e non è mai uscita dall'avviso
   (0 su 23 402 passaggi; 0 su 4324 fotogrammi su profondità simulata).
3. CR-4. Con un ostacolo largo 2 m la persona è nella zona in almeno 92 casi su 100 a 2 s.
4. LP-1. Un drone a 15–21 m/s nascosto da un edificio è annunciato in tempo in 200 passaggi su 200 [0,981; 1].
5. LP-2. Col nucleo v3 mai «libero» sul drone: 0 su 171, con la mappa dichiarata completa.
6. LP-3. Il drone che rallenta o si ferma resta nell'avviso in 188 passaggi su 200 [0,898; 0,965].
7. EV-1. Collisione fra droni dedotta in tutti i 60 passaggi, in 1,2–2,3 s; entro 2 s in 51 su 60 [0,739; 0,919].
8. EV-3. Zona dei detriti di circa 4,5 km (mai oltre 5,3 km), mai «libero» dove possono cadere i frammenti.
9. EV-2 ed EV-6. Nessun falso evento con droni a 5 m (0/300) né con fumo e detriti in pista (0/120).
10. EV-4. Fiammata in decollo: camere dichiarate non affidabili entro 3 cicli in 90 su 90 (innesco ottimista).
11. LP-7. Su 43 aerei reali (ADS-B), dopo 2–30 s senza vederli, la zona li conteneva in circa 9 casi su 10.
12. LP-4 e LP-5. Rullaggio con fusione di tre sensori: in tempo in 200 su 200; col solo radar in 50 su 200.
13. LP-6. Per gli aerei in volo fino a 210 m/s l'avviso al sito non è tempestivo, e MoVi lo scrive.
14. LP-11. L'avviso si spegne solo guardando tutta la zona: 0 su 600 contro 564 su 2400 della regola ingenua.
15. LP-13 e LP-14. Ciò che il sensore non può vedere (drone sotto la copertura, sotto 250 g) è «zona non
    verificata», mai «libero».

## 6. Da non dire (frasi false, non quelle incoraggianti)

- «validato», «testato su sensori» o su hardware, «in tempo reale», «certificabile», «detect and avoid», il lessico
  d'ingaggio o di contrasto.
- **«MoVi segue collisioni ed esplosioni in volo di aerei»** o di droni veloci: non c'è nessuno scenario (EV-7).
- «avviso tempestivo per gli aerei in volo» (LP-6).
- «sempre», o «entro 2 s» senza «in 51 su 60».
- «entro 2,5 s in tutti i casi» come previsione: la soglia è notata dopo, ed è sul campione.
- «mai "libero" ciò che non ha osservato» senza «con la mappa dichiarata», per la lunga portata.
- «la zona dei detriti si restringe guardando» (0/60).
- «avvisa solo chi è in pericolo» (circa 96 tracce).
- «rileva la fiammata» come capacità del sensore.
- «l'avviso contiene sempre il drone» (12/200).
- «l'hardware dedicato riduce il ritardo dell'evento di N volte»: il calcolo non è il termine dominante (ipotesi).
- le cifre del v3 per A2, A3 e A4, e l'aggancio con l'inviluppo a 210 m/s sulle traiettorie (non rimisurati).
- «122 droni», «zero falsi allarmi», «riconosce» o «classifica».
- «l'identità al ritorno è risolta» (dominio stretto; l'estraneo prende il nome).

**Decisione per il coordinatore (non dell'arbitro).** Mostrare nel video il volo ad alta velocità come «Simulation»
solo dopo E6–E8. Prima, come «Schematic», con la riga «scenario non ancora simulato».
