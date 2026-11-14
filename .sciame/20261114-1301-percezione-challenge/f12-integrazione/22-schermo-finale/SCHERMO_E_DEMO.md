# Schermo, segnali e copione della demo, versione finale — `sciame-interfacce`, f12 (22-schermo-finale), 14 novembre 2026

Sigle (cartelle di `f12-integrazione/`): **V3** `01-soluzione`; **PI** `02-prova-insieme`; **LC** `03-libero`; **PIA** `04-piano`; **ID** `06-identita`; **ATT** `10-attacco`; **COM** `11-completezza`; **RIF** `12-piano-rifatto`; **STA** `13-statistica`; **VD** il verdetto dei dati; **DIS** `f13-allegato/DISCORDANZE_DEI_FASCICOLI.md`; **[int.]** conto mio (`conti_finali.py`). Sostituisce `05-schermo/`.

## 0. In testa

**Tutto resta simulazione, conto o progetto: nessuna cifra è promossa. Nessuna persona ha guardato lo schermo, ascoltato un suono o letto il tabellone: ogni «si legge» è non verificato.** Prove nuove mie: solo conti [int.].

**Cambi di stato rispetto a `05-schermo`.** (1) «Pannello da 1 m: dentro la zona 0,996 / 0,984 / 0,968» valeva col soggetto puntiforme: **smentita col corpo esteso** (PI: 942 su 1045 a 1 s, limite 0,882; 0,875 su cinque celle, STA). In demo resta «almeno 87 su 100 a 1 s», poi nessun livello. (2) L'avviso che finirebbe soltanto guardando: **controesempio** (ATT P5, P7): a ostacolo fermo guardando non finisce mai; nella V3 scritta finisce per riaggancio, cioè per identità. (3) La dicitura del livello più basso coi suoi 2,7 m: scartata da V3, oltre il tetto di 2,6 m: tolta. (4) Identità al ritorno: **smentita su profondità realistica** (VD: 0 passaggi su 90) **e in correzione**; ID è consegnata (29–30 su 30 in un dominio stretto, correzione scelta dopo i dati); **controprova non ancora consegnata** (`ls`, 18:32): preliminare.

**Aperto, mostrato come interruttore nella riga fissa:** l'avviso al ritorno (resta o si chiude: decide l'utente; intanto vale «resta», priorità 2 del contratto). **Non verificato:** che la V3 finale (`20-finale/`, alle 18:32 senza il documento) accolga le correzioni di ATT e COM su cui poggio.

**Scostamenti.** Previsioni Q1–Q8 non cieche (18:24: dopo gli ingressi, prima di conti e stesura). **Q7 smentita: il limite di quattro pagine non è rispettato** (misure in `PREVISIONI.md`); le altre reggono. Letti per intero: contratto, `05-schermo`, ATT, COM, STA, RIF, VD, DIS; in parte V3, PIA, PI, LC, ID; non riaperti gli altri verdetti, l'audit e f6 (citati tramite V3 e COM). Regole violate: il limite di lunghezza.

## 1. Lo schermo

**Disposizione.** In alto la riga fissa. A sinistra la pianta dall'alto, sensore in basso, archi a 1, 2 e 3 m, 17 settori. A destra: livello per settore, una riga per traccia, tabellone (§3), ultime cinque righe del registro. Al piede: «età del dato 0,07 s · ritardo: non misurato · calcolo x ms per ciclo · gruppi in conferma: n».

**Riga fissa** (bianco su nero, mai coperta, ripetuta in ogni riga esportata). *Sorgente*, una di quattro: «DATI SIMULATI · profondità simulata da scheda (D435i, 424×240, rumore nominale) · sequenza [nome]»; «SCENA A MANO, senza rumore»; «REGISTRAZIONE DI ALTRI · THÖR, cattura del moto: non è una camera di profondità · occlusione creata a programma»; «CAMERA IN SALA · [modello] · fotogramma 18 204», solo se il contatore del sensore avanza (camera altrove: «REGISTRAZIONE NOSTRA · [modello] · ore 9:40»). *Configurazione*: «camera ferma 1,2 m, 15° in basso · celle 1° × 0,1 m fino a 3 m · filtri della camera spenti · controllo all'avvio superato alle 14:02». *Nel tronco* (RIF §6; ciò che manca è scritto): «libero nel fotogramma SÌ · avviso al ritorno RESTA · zona prevista SÌ (sd-0) · avviso senza traccia NO · identità al ritorno IN CORREZIONE · sensore non in salute SÌ».

**Regole generali.** Ogni distinzione sta in forma, trama e parola; il colore ripete soltanto e non è mai verde. Tratti di almeno 1,5 px. Un decimale; scritte che cambiano al più 2 volte al secondo. L'età è misurata, mai «0 ms». Nessuna uscita è un comando; nessuna funzione d'ingaggio o di puntamento.

**I segni: uno per ogni stato della V3, nessuno in più** (`stati_v3.txt`: 19 su 19).

| Stato (V3) | Segno in bianco e nero | Parole esatte | Finisce quando |
|---|---|---|---|
| C1 libero (§1.2) | bianco | «visto libero ora» | manca il dato nel fotogramma: nessuna memoria |
| C2 occupato | nero pieno | «occupato (visto)» | non è più visto |
| C3 in ombra | righe oblique rade | «in ombra: non visto» | il suolo è rivisto |
| C4 non osservato | puntini | «non osservato» | mai per memoria |
| A1 possibile presenza (§1.7) | quadrettato fitto, bordo spesso: cuneo più 0,40 m | «POSSIBILE PRESENZA · da 4 s» | celle viste libere 3 fotogrammi di fila; dietro un ostacolo fermo mai (ATT P7); al ritorno: X1 |
| A2 avviso senza traccia (c7) | come A1 | «POSSIBILE PRESENZA · senza traccia · da n s» | come A1; esiste solo se la riga fissa dice SÌ |
| A3 ramo C2 (§1.5) | come A1, entro 0,40 m dal bordo del campo o dal vuoto vicino | «POSSIBILE PRESENZA · fuori campo o sotto il sensore · da n s» | la zona è rivista |
| T0 tentativa | contorno sottile sulle celle nere, senza nome | al piede: «gruppi in conferma: n» | confermata o scartata |
| T1 osservato | disco pieno, scia piena; solo con una misura intera nel ciclo | «P1 VISTO · 2,1 m» | manca la misura |
| T2 visto in parte (c4, c6) | contorno pieno del gruppo tagliato, senza freccia, **insieme** alla zona di T4 | «P1 VISTO IN PARTE» | torna intero o sparisce; l'età di T4 conta dall'ultima misura intera |
| T3 non confermato | disco vuoto a punti sull'ultima misura | «P1 NON CONFERMATO · ultima misura da 0,13 s» | dopo 0,2 s: registro «non più rilevato» |
| T4 previsto (§1.6) | anello vuoto; zona a righe fitte, bordo tratteggiato; scia tratteggiata | «P1 PREVISTO · [livello] · larga 0,8 m · non visto da 1,2 s» | mai finché è pendente: diventa T5 e non torna indietro |
| T5 previsto ampio | tutto il non visto libero dell'ombra a righe rade, bordo a punti; nessun punto | «P1 PREVISTO AMPIO · dietro l'ostacolo o fuori area · da 3,4 s» | solo per una chiusura X1–X5 |
| N non ricomparso | riga sotto T5 | «non ricomparso da 6 s (dedotto): fermo dietro, o passato dal lato non visibile» | chiusura |
| X1 riagganciata (§1.8) | disco pieno; segmento fra punto previsto e prima misura intera per 0,5 s | «P1 RICOMPARSO · identità presunta · scarto 28 cm» | con RESTA, A1 rimane: «P1 ricomparso · ombra non riguardata da 12 s»; con SI CHIUDE, A1 sparisce |
| X2 identità ambigua | disco «P2?»; T5 di P1 e A1 restano | «P2 · identità ambigua» | l'ombra è vista libera |
| X3 ombra vista libera | T5 e A1 spariscono cella per cella | registro: «ombra vista libera · OSSERVATO» | — |
| X4 affidabilità persa (§1.9) | cornice spessa, pianta a puntini, parola grande; ogni traccia viva diventa T5 | «AFFIDABILITÀ PERSA · sensore coperto · ultimo dato valido da 2 s»; «P1 PREVISTO AMPIO · non aggiornata · sensore non affidabile» | al ritorno zone e avviso dilatati, sul «non visto libero» (ATT 4); ogni riaggancio è X2 |
| X5 fuori dall'area osservata | T5 fermo al bordo; A1 resta | «P1 · fuori dall'area osservata (dedotto)» | come A1 |

**Il livello nell'etichetta di T4** si legge dalla configurazione, per predittore e geometria (COM, correzione 6). Oggi: *sd-1, ostacolo largo 2 m*: «almeno 9 su 10 qui dentro» fino a 2 s, «almeno 85 su 100» fra 2 e 3 s (V3 §1.6 scrive «8 su 10», più debole: ne va scelta una); *sd-1, pannello della demo*: «almeno 87 su 100» fino a 1 s, poi T5 (a 2 s il segno è già «ampio» nel 92 % degli istanti, PI); *sd-0, o qualunque predittore su profondità simulata o vera*: **nessuna cifra**, «livello non misurato qui» (sd-0 tiene 0,90 solo in 37 celle su 45; sulla profondità la zona di f8 non è mai stata misurata: V3 §1.6). Chi entra nell'ombra da fermo va subito in T5 (ATT, correzione 9).

**Livello per settore** (uno solo, il più alto: V3 §1.10): «ATTENZIONE» (cornice spessa: mobile in avvicinamento, poi occupato a d m); «ZONA NON VERIFICATA» (a righe: possibile presenza, previsto, ombra, buco); «SUOLO VISTO LIBERO DA 1,3 m A d m», d al più 2,6 m; «SCONOSCIUTO» se d = 1,3 m: lo dicono per geometria 8 settori laterali su 17 (LC §3). Fuori scala: «AFFIDABILITÀ PERSA». L'ordine fra «zona non verificata» e un mobile in avvicinamento è aperto (K-306).

**Schermata d'avvio.** «Non misuro: il suolo a meno di 1,24 m davanti e di 1,7 m ai lati; oltre 3 m; il vetro e ciò che non rimanda segnale (un palo scuro può risultare libero); sotto un ostacolo sospeso il suolo resta "visto libero"; oggetti bassi vicini (0,35 m a 0,5–0,8 m); barre più sottili di 2 cm; la testa di una persona di 1,70 m a meno di 2,0 m. Dietro un ostacolo più basso di 1,65 m perdo chi è ancora in vista. Seguo una persona sola per ostacolo: se ne esce un'altra, la scambio.» Sotto, il **controllo all'avvio**, quattro righe con l'esito: filtri spenti; inclinazione entro 0,5° dalla taratura; un oggetto di 10 cm a 2,5 m esce «occupato»; pavimento vuoto 30 s, 0 tracce confermate. Se cade la terza non parte; se cade la quarta parte con «avviso senza traccia NO» e «rumore oltre il dominio provato». Fonti: VD (F-404, F-405, F-410, F-413), ATT (P2–P4), COM (B13). Con due valori (DIS): 1,24 m col campo di 58°, 1,22 m con la focale di 424 px; ai lati 1,71–1,73 m o 1,69 m.

**Registro**, una riga per evento con «come lo so»: `14:02:07 · P1 · scomparso dietro l'ostacolo · DEDOTTO`; `P1 · ricomparso · identità presunta · OSSERVATO · scarto 28 cm`. Mai una sosta o un'uscita affermata.

## 2. Il canale sonoro (secondo profilo: avviso di presenza per una persona non vedente ferma)

Segnali di 0,3 s, uno per cambio di stato; la frase «direzione, distanza, stato» solo a stato stabile. Precedenza: (1) affidabilità persa, ripetuta finché dura; (2) visto in avvicinamento; (3) scomparso dietro l'ostacolo; (4) previsto ampio, poi non ricomparso; (5) ricomparso; (6) identità ambigua; (7) la frase. All'avvio, a voce: la sorgente e «il silenzio non vuol dire che non c'è nessuno». Nel minimo resta almeno il suono 1 (RIF). **Non si promette:** niente per chi cammina; una posizione dal suono; che i segnali si distinguano; un ritardo (stimato 155 o 131 ms secondo la cifra del sensore, DIS; non misurato). Se il programma si ferma il canale tace: il battito continuo è «dopo l'hackathon».

## 3. Il tabellone

```
PRECISIONE MISURATA · DATI SIMULATI, verità del simulatore · sequenze mai usate per tarare
(con una camera: «MISURATA QUI · occlusione virtuale · CAMERA IN SALA»)
passaggi con un vuoto dopo l'ingresso nell'ombra (soglia 0)      k su n
istanti nascosti fuori dall'avviso (soglia 0) · su «libero»      k su n · k su n
celle «libero» con un ostacolo sotto (soglia 0)                  k su n
dentro la zona · 1 s · ancora nascosta, nell'area osservata      k su n  fra .. e .. su 100  larga .. m
dentro la zona · 2 s                                             k su n  fra .. e .. su 100  larga .. m
«previsto ampio» (a parte, non fa punteggio)                     k su n istanti
identità al ritorno · pannello dato per «mobile»                 k su n · k su n
calcolo per ciclo su questa macchina                             media .. ms · massimo .. ms
n fissato prima: 100 passaggi · nessun azzeramento · una riga di registro per passaggio
```

**Come si legge** [int.]. 27 su 30 dice «fra 74 e 97 su 100»; 30 su 30 «almeno 89 su 100», non «sempre». Con 100 passaggi «più di 8 su 10» si scrive solo con almeno 87 dentro (binomiale esatta, una coda: 0,047; con 86: 0,080); «almeno 9 su 10» chiede 96 su 100 e riesce solo se il vero è 0,97 o più (STA §5). Sotto 30 passaggi solo il conto. La larghezza sta accanto: una zona enorme è sempre giusta. **Cifre di oggi sulla profondità simulata** (VD, parametri del nucleo), che il tabellone stampa finché le correzioni non entrano: identità 0 su 90; pannello «mobile» 79 su 90; centro nascosto nell'avviso 2939 fotogrammi su 3038, mai su «libero»; persona nella zona 36 passaggi su 46 (83 su 90 con la soglia di 40 punti a 424×240: DIS); «libero» nell'ombra vera 0 su 2,9 milioni di controlli a posa esatta. Pedoni veri (THÖR, 9 persone, cattura del moto; filtro con q = 0,2, non il predittore mostrato): 0,977 / 1,000 / 1,000 a 1 / 2 / 3 s (col secondo codice 0,982 / 0,995 / 1,000: DIS).

## 4. La demo

**Il caso più probabile all'ora 14: solo registrazioni e dati simulati** (PIA §6). Si mostra **il tronco com'è al gelo dell'ora 12** (RIF): la riga fissa nomina i pioli entrati, la scaletta non cambia. Sequenze di `f10-dati/11-simulatore` (D435i nominale): `pavimento_vuoto`; `pannello_a05` (passa a 0,5 m/s); `pannello_b` (sosta di 3 s dietro); `pannello_c` (torna indietro: solo 4); `sensore_coperto`. **Hanno il pannello di 1 × 1,6 m a 1,8 m e la persona a 2,3 m:** in 10 passaggi su 90 la testa spunta (VD); in prova generale si scelgono quelle in cui non spunta, e lo si dice. Il giurato sceglie il numero della sequenza fra quelle mai usate per tarare.

**Con una camera in sala** (solo dopo il controllo all'avvio e dieci passaggi riusciti di fila): camera ferma a 1,2 m, 15° in basso; pannello **alto 1,8 m, largo 1 m, a 1,7–1,8 m**; attore sulla linea a **2,3 m**, cioè 0,5–0,6 m dietro il pannello (a 0,3 m l'identità corretta cade: 0 e 1 su 10, ID); passo **0,5 m/s**; una sola persona; al chiuso. Conti [int.]: ombra sulla linea 1,28–1,35 m; nascosto per intero 1,7–1,8 s; il pannello copre fino a 1,97 m di statura; il campo a 2,3 m arriva a 1,77 m: un attore più alto ha la testa tagliata. La fascia di 0,40 m copre 1,4 m/s nel conto dei file e 1,13 m/s in quello a tre termini del fascicolo (0,56 con 20 cm d'errore di bordo: DIS): a 0,5 m/s reggono tutti.

**Al ritorno**, secondo il tronco: *identità entrata* → X1, e il quadrettato resta con «ombra non riguardata»; *non entrata* → X2, la zona di P1 e l'avviso restano. **La frase vera:** «qui la previsione localizza per circa un secondo, poi dice che la persona è ancora dietro».

| Atto | Si vede (stati del §1) | Requisito della traccia · blocco V3 · riga del tabellone |
|---|---|---|
| 1 Pavimento vuoto | C1 solo dove il suolo è letto, C4 altrove, lati «sconosciuto»; schermata d'avvio | distinguere l'osservato dall'incerto · §1.1–§1.2 · celle «libero» con ostacolo sotto |
| 2 Passa dietro | T1 → T2 con T4 → T5 → X1 oppure X2; A1 sotto; registro | elementi mobili, interruzioni della visibilità, continuità percettiva · §1.5–§1.8 · vuoti; dentro la zona |
| 3 Si ferma e torna | T5, N; nessun timer spegne A1 | sicurezza delle indicazioni · §1.6–§1.7 · nascosti fuori dall'avviso |
| 4 Sensore coperto | X4, suono 1; al ritorno X2 | segnalare la perdita di affidabilità · §1.9 · — |
| 5 Tabellone | le righe del §3 | valutazione realistica della precisione; efficienza elaborativa · §1.12 · tutte |

Fuori dai 5 minuti, se c'è tempo o una camera: ostacolo fermo; prova scelta dal giurato (occlusione virtuale, o tratti THÖR **solo se quella riga è nel tronco**: PIA la taglia per settima); persona bendata **ferma** accanto al treppiede, con «per chi cammina non è provato niente». Tagli: atto 1, poi 3 accorciato; mai apertura, 2, 4, 5, chiusura.

## 5. Che cosa è cambiato rispetto a `05-schermo`

1. Segni nuovi per T0, T3, A3 e A2; tolte quattro uscite che la V3 non produce: la vecchia dicitura del livello basso coi 2,7 m, due livelli insieme, «dedotto, sensore non affidabile», la targhetta sulla pianta (COM §3).
2. Livello della zona per predittore e geometria: in demo «87 su 100 a 1 s», su profondità nessuna cifra (PI, STA).
3. Avviso «resta» o «si chiude» nella riga fissa; identità «presunta» (ATT 1; ID §5; F-409).
4. Schermata d'avvio coi limiti di VD e controllo all'avvio a quattro righe, con 0,5° (ATT 3 e 6).
5. Riga fissa: quattro sorgenti e i pioli del tronco (RIF §6).
6. Tabellone: un solo n (100), righe a soglia zero per prime, costo come riga, cifre di oggi (STA §5; COM B12).
7. Una scaletta sola, i cinque passi di PIA §9; la variante senza camera è il caso principale.
8. Geometria: pannello alto 1,8 m a 1,7–1,8 m, attore almeno 0,5 m dietro (VD, ID).
9. Elenco «da non dire» con le frasi di VD, COM (A14–A17) e ATT (W1–W5).

## 6. Da non dire → che cosa dire (elenco unico)

- «validato», «certificato», «garantito», «tarato», «validato su dati veri», «sul sensore» → «provato su profondità simulata dalle schede tecniche e su tracce pubbliche di persone; mai su un sensore nostro».
- «continuità garantita», «prevede dove sarà», localizzare «per tutta l'occlusione» → «finché è nascosta lo schermo mostra un segno e una zona; qui localizza per circa 1 s, poi dice che è ancora dietro; cede se la perde prima dell'ostacolo».
- «90 %» o «9 su 10» senza dominio; una cifra oltre 3 s, per chi svolta, per chi parte da fermo, col pannello da 1 m oltre 1 s; «l'ellisse al 95 % è coerente» → «in simulazione, con un ostacolo largo 2 m, sensore fermo e una persona alla volta che prosegue, rallenta, si ferma o torna, la persona nascosta sta nella zona in almeno 9 casi su 10 fino a 2 secondi e in almeno 85 su 100 fino a 3, finché resta nascosta; bordo dell'ombra noto esattamente; non misurato su un sensore».
- «100 % degli istanti dentro l'avviso», «zero casi su 218 000 passaggi» → «in simulazione meno di 1 passaggio su 1000 resta senza avviso con 9 rilevamenti su 10, fino a 5 su 1000 con 7 su 10; vuoti dopo l'ingresso nell'ombra: meno di 6,4 su 10 000».
- «l'avviso finisce solo guardando», «la previsione non tocca l'avviso» → «la previsione può accendere l'avviso, mai spegnerlo; l'avviso resta finché quell'ombra non è vista libera, e dietro un ostacolo fermo non si spegne» (con SI CHIUDE: «finisce quando la persona ricompare; se dalla stessa ombra esce un'altra persona, cade a torto»).
- «identità mantenuta al 100 %», «segue chi passa dietro un ostacolo» e basta, «soglia 40» senza la risoluzione → «il nome al ritorno è presunto; su profondità simulata realistica oggi regge 0 volte su 90; la correzione è in prova».
- «via libera», «nessun ostacolo osservato fino a d», «mai dato per libero» senza condizioni, «2,7 m» → «suolo visto libero da 1,3 m a d metri»; «dice libero solo dove in quel fotogramma legge il suolo: in simulazione, a camera ferma e inclinazione nota entro mezzo grado, 300 condizioni senza un errore; un ostacolo che non rimanda segnale, o sospeso, sfugge».
- «30 prove bastano», «± X,XX m», «confidenza Z %», «errore di 0,2 m a 1 s» → «27 su 30 dice: fra 74 e 97 su 100»; «la zona ha contenuto la persona k volte su n, larga tanto».
- «la perdita di affidabilità è dichiarata» senza condizioni → «segnala sensore coperto, fotogrammi fermi, inclinazione cambiata; su una camera vera non è provato».
- «riconosce la sosta», «si è fermato dietro il pannello», «è uscito» → «non ricomparso da n s (dedotto)». «bassa latenza», «15 Hz» → «ritardo non misurato; calcolo x ms per ciclo su questa macchina; 6 ms di media su scene simulate, 81 ms su una registrazione vera affollata».
- «dal vivo» prima che giri → la sorgente della riga fissa. «mappa 3D», «voxel», «copre gli ostacoli bassi», «360°», «il vetro è risolto» → «mappa a celle del suolo fino a 3 m; non vede il vetro».
- «ACAS», «TA/RA», «anti-bird strike», «detect and avoid», «indice di minaccia», «NOMINAL / HOLD / FAIL-SAFE», «preallarme laterale» → i nomi del §1; «avvicinamento diretto». «drone», «UAV», «in volo» → «camera ferma; un veicolo senza equipaggio è un modo di portarla: provato solo da fermo e a 1,2 m».
- «orientamento» per chi cammina, «dispositivo medico», «conforme a», una distanza di separazione da norma (norme non lette: DIS) → «avviso di presenza per una persona non vedente ferma; nessuna prova con persone».
- «ispezione», «Intelligenza Artificiale», «massa e accelerazione stimate» → «un registro di eventi, osservati o dedotti»; «regole scritte, nessun modello appreso»; «posizione e velocità».
- «la preproposta è stata adottata», «in cinque ci sta», «minimo chiuso» → «ne teniamo le regole di disegno»; «mostriamo il programma com'è, e la riga in alto dice che cosa c'è dentro».

## 7. Il copione in una pagina (5 minuti; fra parentesi i tempi della demo da 3 minuti)

**Apertura · 25 s (20 s).** «Prototipo fatto in 14 ore. Oggi non c'è una camera: vedrete profondità simulata dalle schede tecniche di una camera vera. La riga in alto lo dice in ogni momento, insieme a ciò che è entrato nel programma e a ciò che manca. Vi diciamo prima dove cede.» (Con la camera: «Questa è una camera in sala, una sola installazione.»)

**1 · Pavimento vuoto · 35 s (tagliato: una frase nell'apertura, indicando i puntini).** «Bianco è solo il suolo che legge in questo fotogramma. I puntini sono ciò che non vede: non diventano mai liberi. Ai lati dice "sconosciuto".»

**2 · Passa dietro il pannello · 60 s, due passaggi (45 s, uno).** «Disco pieno: lo vede. Contorno: lo vede in parte. Anello e zona tratteggiata: non lo vede, e dice dove può essere e quanto è larga la zona. Dopo circa un secondo dice solo "è ancora dietro". Sotto, il quadrettato: possibile presenza.» Al ritorno, secondo la riga fissa: «Ricomparso: il nome è presunto» oppure «Qui il nome non regge ancora: lo segna ambiguo, e l'avviso resta.»

**3 · Si ferma dietro e torna · 50 s (35 s).** «Non ricomparso da 6 secondi: fermo dietro, oppure passato dal lato che non vediamo. Non lo sa, e lo scrive come dedotto. Nessun orologio spegne l'avviso.»

**4 · Sensore coperto · 30 s (20 s).** «Affidabilità persa: lo dice, lo suona, e toglie ciò che dava per visto. Al ritorno i nomi sono ambigui.»

**5 · Tabellone e costo · 70 s (40 s).** Si leggono le righe: le tre a soglia zero, poi «dentro k su n, cioè fra … e … su 100, zona larga …», poi identità e pannello «mobile» come sono, poi i millisecondi. «In simulazione, con un ostacolo largo, arriva a 9 su 10 fino a 2 secondi; con questo pannello a 87 su 100 a 1 secondo. Su profondità realistica il nome al ritorno oggi è a 0 su 90: è il primo difetto che correggiamo.»

**Chiusura · 30 s (20 s).** «Avete visto che il segno non sparisce mentre la persona è nascosta, che la zona dice quanto è larga, e che ciò che non è visto non è dato per libero. Non avete visto, perché non c'è: una camera nostra, una camera in moto, due persone dietro lo stesso ostacolo, il vetro, l'aperto, una prova con persone non vedenti.»

Somme [int.]: 300 s e 180 s. In prova generale si controlla che ogni scritta mostrata stia nel §1 e che nessuna frase del §6 sia detta.

## 8. Stati proposti e dopo

Corrispondenza stati–segni: **verificata per lettura** su V3 e COM §2 (19 su 19), da rifare sulla V3 finale. «87 su 100 a 1 s»: **sostenuta dai dati in simulazione**. Leggibilità di schermo, suoni e tabellone: **non provata**. Identità al ritorno: **smentita su profondità realistica, in correzione**. Dopo: dieci secondi con tre persone esterne su schermo e tabellone; l'utente decide «resta» o «si chiude». **Rifare:** `sh rifai.sh`.
