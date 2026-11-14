Canarino: sciame-canarino-8f9353395a6192ab

# Consegna di sciame-creativo — estensione f7, corsia B (14 novembre 2026)

Tutto è **simulazione su una scena sintetica, a sensore fermo**, salvo dove è scritto «calcolo» o «non verificato». Per rifare, nella mia cartella: `gcc -O2 -o prova_ombra prova_ombra.c -lm`, poi i comandi in testa a ogni blocco di `risultati_ombra_giro2.txt` e `risultati_giro3.txt` (seme 1). Previsioni ed esiti: `PREVISIONI.md`.

## 1. Scostamenti e regole violate

1. **Errore di lancio nel primo giro:** la shell passava i tre argomenti come uno solo. Hanno girato due configurazioni, ripetute: le righe doppie di `risultati_ombra_giro1.txt` non sono conferme.
2. **La prova è cambiata dopo il primo giro** (stanza chiusa, fusione di 3 fotogrammi, braccio «ingenuo», stanza vuota), ogni volta con previsioni scritte prima; il sorgente del primo giro è in `prova_ombra_giro1.c`.
3. Avevo scritto nelle previsioni un'ora stimata (15:17): sostituita con quella di `date -Is` (15:13:40) prima del lancio.
4. **Otto mie previsioni non hanno retto** (§4). Un braccio di controllo era cieco: ritirato, poi lanciato per errore, ha confermato la cecità.
5. **Indipendenza:** scena, camera, rumore, i due metodi e la «verità» sono miei, in un solo file. La prova vale per i difetti della rappresentazione, non per quelli del sensore vero.
6. Una pagina trovata in rete (cavac.at) conteneva un'istruzione estranea: ignorata. Delle fonti ho letto solo gli estratti della ricerca.

## 2. Critiche numerate, con la prova

Scena: sensore a 1,2 m inclinato di 15°, profondità 320 × 240; scatola bassa (0,3 m), pannello 1 × 2 m, barra a 1,70–1,85 m di quota a 1,5 m dal sensore, una «persona» dietro il pannello; regione 6 × 4 × 3 m. «Falso libero»: un punto detto libero che in verità è occupato, nascosto o fuori campo.

1. **`promptMare.txt` §3 confronta quattro strutture, tutte ancorate al mondo; manca la quinta: il fotogramma di profondità.** Con un solo punto di vista, lo stato di un punto si legge confrontando la sua distanza con quella misurata sul suo raggio. Su 576 000 punti: 0 falsi liberi, contro il 4,8 % dei «libero» della griglia voxel da 5 cm e il 10,1 % a 10 cm (`risultati_ombra_giro2.txt`, primo blocco).
2. **La griglia voxel dichiara libero un voxel che un raggio attraversa solo in parte.** Fra i suoi «libero», il centro è nascosto o fuori campo nel 4,2–6,7 % dei casi a 5 cm e nell'8,7–14,0 % a 10 cm (otto configurazioni). L'errore sta entro un voxel, ma viola alla lettera «non osservato non è mai libero».
3. **La memoria non è il problema, il tempo sì (§9, §14).** La griglia densa da 5 cm occupa 0,58 MB a un byte per voxel, 6,9 MB con lo stato del §4 (12 byte: calcolo). I blocchi 8³ toccati vanno dal 20,8 % (scena aperta) al 43,0 % (stanza senza pannello): la sparsità risparmia 2,3–4,8 volte, prima dell'indice, su una quantità trascurabile. Aggiornare la griglia da 5 cm costa invece 52,8 ms di mediana e 63,8 di massimo (a 10 cm: 26,8 e 27,4), su un ciclo di 66,7 ms; un solo filo, codice non ottimizzato, Ryzen AI 9 HX 370.
4. **Il log-odds del §4, da solo, non vede chi si avvicina.** Con i parametri predefiniti di OctoMap (0,7 / 0,4 / 0,1192 / 0,971: [fonte](https://docs.mrpt.org/reference/latest/struct_mrpt_maps_COctoMapBase_TInsertionOptions.html)) servono 3 colpi per passare da «libero» a «occupato». Un corpo che avanza a 0,5 m/s o più (voxel da 5 cm) non risulta mai «occupato», e i voxel dentro il corpo restano «liberi» nel 100 % dei casi (`risultati_giro3.txt`). La prova 5 del contratto fallisce se lo strato di visibilità non ha la precedenza.
5. **Nucleo: «nessun ostacolo osservato fino a d metri» è vero solo sul piano.** La sua regola dà «libero» 393 celle, 16 delle quali hanno la barra nella colonna 0,07–1,9 m; su quelle 393 la quota davvero verificata è in media 1,40 m.
6. **Nucleo: il cuneo fino al bordo sovrastima l'ombra di un ostacolo basso.** Dietro la scatola: 283 celle nel cuneo, 164 davvero nascoste o dentro la scatola. L'ombra finisce a d·H / (H − h): qui 2,27 m (calcolo).
7. **Nessuno parla del fondale.** Senza pareti il 32,2 % dei raggi non torna, e lungo quei raggi nessuna struttura può dire «libero». In un capannone grande può succedere ai raggi orizzontali (deduzione, **non verificata**); una stazione che guarda dall'alto ha sempre il pavimento per fondale.
8. **La domanda finale di `promptMare.txt` (riga 467) misura il beneficio «per applicazioni UAV»; la traccia non li nomina.** Il §7 mette nella prima demo il «drone in hovering simulato», che `f6-specializzazione/01-esperto-dominio/SPECIALIZZAZIONE.md` (riga 32) esclude perché un drone in volo oscilla.

## 3. Parti di `promptMare.txt`: utili, inutili, sbagliate (per il mio campo)

| Parte | Giudizio | Motivo |
|---|---|---|
| §5: «ricavare le regioni di occlusione tramite interrogazioni geometriche» | **utile**: è la strada migliore | critiche 1 e 6 |
| §4: «storia contro garanzia corrente»; «non allocato = sconosciuto» | **utile** | sparisce se «libero» si legge solo dai fotogrammi recenti |
| §10 (dieci prove); §2 e §9 («non assumete a priori») | **utili** | usati come griglia di prova |
| §3: CSR/COO; §13: dodici capitoli | **inutili** | formati per matrici; il formato non decide niente |
| §14: memoria come beneficio; §4: log-odds che decide | **sbagliate** | critiche 3 e 4 |
| riga 467 («UAV»), §7 («hovering») | **sbagliate** rispetto alla traccia e a f6 | critica 8 |
| §6, §8 | fuori dal mio campo | non giudico |

## 4. Stati che propongo

- «A sensore fermo la griglia voxel non aggiunge informazione sullo stato corrente rispetto al fotogramma di profondità»: **deduzione teorica**, **verificata** sui centri dei voxel di una sola scena (0 falsi liberi in ogni configurazione, escluso il braccio ingenuo). Non vale in moto: lì la mappa aggiunge la memoria di più punti di vista.
- «La mappa sparsa usa meno memoria della densa»: **sostenuto dai dati**, senza beneficio pratico.
- «Il log-odds basta a rilevare gli oggetti mobili»: **smentito**.
- Limiti del nucleo sulla quota della testa e sull'ombra dell'ostacolo basso: **sostenuti dai dati** (critiche 5 e 6). Vetro: **non risolto**; nessuna mia proposta lo tocca.
- Mie previsioni **smentite** (tabelle in `PREVISIONI.md`): «libero» perso senza fondale (60,9 % contro ≤ 10 %); blocchi toccati (20,8 % contro 30–55 %); tempo su tutti i punti (un decimo, non pari); ombra e persona nascosta con un solo fotogramma rumoroso (28,8 % e 59,2 %: il resto è «buco», mai «libero»); sagoma orizzontale (0 % contro 3–7 %) e verticale (29,8 % contro ≥ 90 %); log-odds a 0,2 m/s (46 % contro > 50 %). **Non risolta:** prudenza con rumore e 3 fotogrammi (21,4 %, fra 20 e 25).

## 5. Proposte

### creativo-1 — «Il sensore è la lampada» (dalla grafica: la mappa d'ombra, [Williams 1978](https://history.siggraph.org/?p=120268))

**Meccanismo.** Nella grafica un punto è in ombra se dista dalla lampada più di quanto la lampada «vede» in quella direzione. Qui la lampada è il sensore, e illuminato vuol dire osservato. Il componente è una funzione `stato(punto 3D)` con cinque risposte (libero, bordo od occupato, in ombra, buco, fuori campo), letta dal minimo e dal massimo della profondità su 3 × 3 pixel negli ultimi 3 fotogrammi. Non si alloca niente: la risposta predefinita è «non so». La «possibile presenza» diventa, per ogni pixel dell'ostacolo, un intervallo di distanze che finisce dove il raggio tocca il pavimento (ombra chiusa) o al limite della portata (ombra aperta: solo allora «può aver lasciato l'area»). Si rilascia raggio per raggio, come oggi cella per cella: nel nascondino studiato in robotica una regione nascosta resta «contaminata» finché non è vista ([Guibas e altri, 1997](https://cw.fel.cvut.cz/b191/_media/courses/b4m36uir/lectures/guibas1997.pdf)).
**Guadagno misurato.** 0 falsi liberi; ombra dietro la scatola bassa 143 celle (verità 164, cuneo 283); 0,59 ms a fotogramma (massimo 0,60; comprende la sagoma di creativo-2 su tutta la zona) contro 52,8 ms; persona nascosta «in ombra» al 100 % (99,9 % in una configurazione con rumore), mai «libera». Il braccio ingenuo (pixel non valido = libero) dà 2561 falsi liberi: il contatore non è cieco. Prove del contratto: 1 e 4 reggono per misura; 2, 3 e 10 per costruzione (nessun decadimento, nessun blocco, costo legato ai pixel e non agli oggetti); 5, 6 e 9 **non provate** (scena ferma); 7 non toccata; 8 (vetro) fallisce come nel nucleo.
**Costo e vincoli.** Con rumore perde il 21,4 % del libero vero (la griglia voxel il 10,0 %); con un solo fotogramma e il 5 % di pixel non validi la regola 3 × 3 scarta il 37 % delle interrogazioni. Vale **solo a sensore fermo**; non vede fili più sottili di un pixel; nella prova usa 1,5 MB (calcolo dal sorgente), più di una griglia da 10 cm.
**Chi la prova:** nuvole di punti, tempo reale. **Falsificatore (5 minuti):** sulla camera vera, una scatola di 30 cm a 1,7 m. Atteso: ombra al suolo chiusa entro 2,3 ± 0,2 m. Smentita: suolo «libero» dentro l'ombra, oppure ombra fino a 3 m.

### creativo-2 — «La sagoma limite» (dalla ferrovia: non si mappa il mondo, si verifica il profilo che deve passare; analogia senza fonte controllata)

**Meccanismo.** L'uscita per settore diventa: «la sagoma dichiarata è verificata libera fino a d metri e fino a quota h; sopra, non osservato». La sagoma è un parametro del profilo: una persona (0,1–1,9 m), un veicolo, oppure un **volume di rispetto** attorno a un oggetto sorvegliato, con tre risposte: vuoto verificato, occupato, non verificabile. Si calcola con `stato()` su cinque verticali per cella.
**Guadagno misurato.** Con il montaggio orizzontale la sagoma è verificata per intero su 7 celle su 570 (1,2 %; 1,8 % a stanza vuota), mai con un oggetto nella colonna; il nucleo dà «libero» 393 celle, 19 con un oggetto. Con il montaggio verticale: 79,8 % a stanza vuota, 29,8 % con gli oggetti, e nessuna cella falsa sotto la barra. Quindi o l'uscita dice la quota, o il sensore si monta in verticale (già nel §6 del nucleo).
**Vincoli.** Serve un fondale; il montaggio verticale stringe il campo a 58°. Un fotogramma, scena ferma.
**Chi la prova:** esperto di dominio, requisiti. **Falsificatore (5 minuti):** un bastone orizzontale a 1,8 m di quota, a 1,5 m dal sensore. Atteso: il nucleo non lo vede, la sagoma dichiara una quota verificata sotto 1,7 m. Smentita: sagoma «verificata» con il bastone nella colonna.

### creativo-3 — «Il registro a partita doppia», per Q2 (dalla contabilità e dal controllo degli attrezzi in manutenzione aeronautica)

**Meccanismo.** Un contabile non cancella una partita perché è passato del tempo: la tiene in sospeso finché non la riconcilia. In hangar un attrezzo non ritrovato resta in conto ([fonte debole, di settore](https://sofemaonline.com/about/blog/entry/easa-part-145-tooling-store-management-and-control-procedures-considering-the-problem-of-foreign-object-debris-fod-1); la procedura non è verificata). È la regola della «possibile presenza», in parole che un giurato esterno conosce. Il componente è un pannello «registro dell'area», derivato dagli stati che il nucleo già produce: entrati = in vista + fuori vista (dietro che cosa, da quanti secondi) + usciti osservati + chiusi come «non più rilevato». Ogni riga dice come lo si sa: visto, dedotto, non noto. È il solo «monitoraggio di attività» che il nucleo regge, e **non è provato**: il nucleo stesso lo dà per «non coperto» (§7).
**Tre minuti, una registrazione, due letture.** (0:00) Una frase con le parole della traccia, poi: «Il sensore sta su uno stativo. Su un veicolo fermo è lo stesso caso. Su un veicolo in moto non è provato.» (0:20) Pianta e registro: un oggetto fermo; una persona entra, passa dietro il pannello, torna sulla stessa riga. Un giurato sceglie se resta nascosta: la riga non passa mai a «uscito» senza un'osservazione. (1:40) La stessa registrazione a occhi chiusi: tre suoni brevi, stesso contatore di eventi. (2:10) Mano sul sensore: «registro sospeso» e suono dedicato. (2:30) La legenda della scena applicata al progetto, come le carte nautiche marcano ciò che è approssimato o dubbio ([PA, PD](https://cartes-charts.gc.ca/publications/chart1-carte1/sections/w-abbrs/abbrev-eng.html)): pieno = misurato in simulazione; tratteggio = atteso sull'hardware; grigio = non noto (moto, vetro, sensore vero).
Controllo a mano, dello stesso autore: ogni frase della traccia ha il suo momento (rilevare 0:20; interruzioni 0:50; osservato e incerto: la colonna «come lo so»; feedback 1:40; affidabilità 2:10; i due ambiti 0:20 e 1:40).
**Vincoli.** Nel nucleo manca la regola «uscito dal bordo del campo»; con due nascosti il registro conserverebbe il conteggio, non l'identità (non verificato).
**Chi la prova:** designer dell'interazione, rovesciatore. **Falsificatori, non eseguiti:** (a) sulle registrazioni simulate che esistono già, il bilancio a ogni fotogramma: atteso 0 squilibri e 0 righe «uscito» a soggetto nascosto; (b) tre persone senza contesto e quattro domande dopo il video: almeno 3 risposte giuste in 2 casi su 3.

## 6. Che cosa propongo dopo

1. Per Q1, dal mio campo: la griglia voxel **non serve alla prima demo** e porta i rischi delle critiche 2 e 4; serve con il sensore in moto e una posa affidabile. Alternativa compatibile: creativo-1 e creativo-2 accanto al nucleo. Decide l'arbitro.
2. Rifare la prova di creativo-1 con un oggetto in moto (prove 5 e 9) e con un autore diverso.
3. Decidere fra «dire la quota» e «montare in verticale» con il falsificatore del bastone.
4. Scrivere la regola «uscito dal bordo» e provare il bilancio del registro prima di metterlo nella demo.
