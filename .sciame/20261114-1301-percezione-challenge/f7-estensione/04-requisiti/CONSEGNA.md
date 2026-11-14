Canarino: sciame-canarino-55f6adcfa718b00e

# Conciliazione con la traccia e registro di eventi — `sciame-requisiti`, f7, corsia A (Q2)

## 1. Scostamenti e regole violate

- **B1 è smentita, e l'ho riletta dopo.** La seconda lettura (`eventi.py 2`) è scritta dopo il primo lancio: è una diagnosi, non un «regge». Fra i due lanci c'è un conteggio di diagnosi senza previsione.
- **I conteggi A non sono previsioni:** `PREVISIONI.md` (15:05:58; aggiunte 15:09:10) è nato a testi già letti. A3 è caduta comunque (`uncrewed`: 4 volte, non almeno 5).
- **Indipendenza.** Generatore, estrattore e oracolo di `eventi.py` sono miei: è un **controllo della logica**, non un dato sul nucleo né sul sensore. Il «nucleo» dello script è una mia riduzione di B5, con un soggetto puntiforme.
- **Non fatto:** nessuna pagina in rete; non letti `MOTO_PROPRIO.md`, `MISURE*.md`, `CONTROPROVE.md`. **Lunghezza:** composto, il file supera le tre pagine di poco meno di mezza pagina (misure in fondo).
- Rimandi: `T` = `regole_challenge.md`; `V2` = `SOLUZIONE_V2.md`; `tex` = `proposta/proposta_sciame.tex`; `SP`, `ATT`, `AUD`, `VER` = specializzazione, attacco, audit, verdetto. Cifre «mie»: `timeout 120 python3 -I eventi.py` (meno di 1 s), in `risultati_eventi_lancio1.txt` e `risultati_eventi_lettura2.txt` (`risultati_eventi.txt` è il primo lancio rifatto dopo le modifiche allo script: stesse cifre).

## 2. Critiche

**A `promptMare.txt`.**

1. **Il suo criterio guarda un ambito che la traccia non ha, e tace quelli che ha.** `UAV` o `drone`: 12 volte; `monitoraggio`, `attività`, `ispezione`, `accessibilità`, `disabilità`: 0. In `T`, `uncrewed`, `drone`, `UAV`, `veicol`, `volo`, `3D`, `voxel`: 0 (`grep`). La domanda finale (riga 467) chiede un beneficio «per applicazioni UAV»: è ambito in più, e il contratto l'ha già tolto.
2. **I «vincoli di latenza, memoria e costo della challenge» (riga 467) non esistono.** `T` dice solo «bassa latenza ed efficienza elaborativa»; 15 cicli/s e 150 ms sono soglie dello sciame, e una soglia di memoria non c'è: va fissata prima delle misure.
3. **Due voci del §14 non sono benefici rispetto al nucleo:** «meno memoria di una volumetrica densa» e «prestazioni compatibili» confrontano voxel sparso e voxel denso, non voxel e griglia (2610 celle contro 72 000 a 10 cm nella regione 6 × 4 × 3 m; conto mio). Il criterio 1 del contratto le eredita: contino come condizioni.
4. **La regione di prova (6 m) esce dalla portata del nucleo** (V2, B1: griglia fino a 3 m): il confronto va fatto entro 3 m.
5. **«Drone in hovering simulato» (riga 223) è sbagliato sui file:** SP §2 esclude il volo stazionario; il criterio dell'IMU di V2 lo darebbe «affidabilità persa».

**Al nucleo e ai documenti già dati.**

6. **Il primo ambito non è mai detto con le parole della traccia.** In `tex`: `monitoraggio`, `attività`, `ispezion`, `industri`, `aerospa` = 0; `uncrewed` 4, `sentinella` 2, `autopilot` 4. V2 §7: «il monitoraggio di attività non è coperto». AUD §2: è «la scelta rovesciata».
7. **Una frase del PDF v0.3 è falsa sui file:** «un drone in volo stazionario simulato dal treppiede» (`tex`, riga 158) contro SP §2.
8. **«Oppure».** `T` chiede una applicazione; due sono una scelta dell'utente, e nel profilo assistivo niente è provato oltre il nucleo comune (ATT S4). **«Ispezione»** non è una funzione del nucleo: niente valuta lo stato di un oggetto.
9. **[dopo] V2 non dice che cosa diventano le tracce vive quando l'affidabilità cade** (B5: solo «buco → affidabilità persa»). Nella mia riduzione, che le chiude, se il sensore è coperto 2 s mentre il soggetto entra nell'ombra, in 8 scene su 40 (3 su 40 con rilevamento 0,9) il soggetto resta nascosto in portata per almeno 1 s con affidabilità buona e **nessuna «possibile presenza»**. Tocca il quarto principio del contratto; non è un «libero» falso.
10. **[dopo] Un registro rende visibili i falsi allarmi del nucleo.** Con un rilevamento mancato su dieci, una «scomparsa» spuria (soggetto in vista, nella fascia) esce nel 58 % delle scene senza conferma e nel 12,5 % con 3 fotogrammi di conferma (B7 prevedeva ≤ 5 %: smentita). VER dà 12,8–14,3 % di strati accesi a vuoto: serve la regola di K-018.

## 3. `promptMare.txt`, lato requisiti

- **Utile.** §1 e §10 (principi, dieci prove): criteri d'accettazione di R4, R6, R8. §4, «storia contro garanzia corrente»: l'invariante 1 detto come requisito. §5 e §14, occlusioni e quote: servono alla traccia **senza UAV**, perché in un ambiente industriale l'occlusore più basso del sensore (cassa, bancale) è il caso comune, e lì il cuneo del nucleo è falso (AUD 5). Il requisito è «ombra corretta dietro un occlusore basso»: lo può soddisfare anche l'alternativa D. §8-A e §8-C per R6 e R7; §9; §11.
- **Inutile per la traccia:** §6 (stato a sei componenti), §7 (trasformazioni sensore–drone), «trasferibilità a UAV» nel §14, §12, §13. **Sbagliato:** critiche 2, 4, 5. **Da riformulare:** §8-B, «detriti» → «oggetto piccolo a terra»; sotto 0,07 m di quota il nucleo non lo vede: limite da scrivere.

## 4. Stati proposti

- **Verificato:** la traccia non nomina uncrewed, volo, 3D (10 radici cercate in tutto `T`: 0).
- **Smentiti:** «il v0.3 dice il primo ambito con le parole della traccia» (0 occorrenze); «drone in volo stazionario simulato dal treppiede»; «il fuoco su UAV serve la traccia» (l'occlusore basso sì); «V2 copre il monitoraggio di attività» (suo §7); B1 (103 scene su 200 con un evento mancato).
- **Controllo della logica, in simulazione:** nel registro nessun «osservato» a soggetto nascosto e nessuna «uscita» senza misura (0 su 600 scene; braccio ingenuo fallito 200 su 200).
- **Sostenuto dai dati** (Python, questa macchina): il registro costa al più 0,27 ms su un ciclo di 66,7.
- **Non risolto:** le tracce vive alla perdita di affidabilità: manca la regola; decide la prova «sensore coperto mentre l'attore passa dietro il pannello».
- **«Sistema adattabile»:** regge nella forma di ATT C5; sull'hardware non verificato.

## 5. Proposte

### `requisiti-1` — Tre assi: applicazione, portatore, uscita

**Enunciato.** Il documento separa l'**applicazione** (le due della traccia), il **portatore del sensore** (supporto fisso, o piattaforma uncrewed ferma) e l'**uscita** (schermo e registro, o suoni). Il veicolo uncrewed è un valore del secondo asse, d'interesse per chi propone la sfida. «Adattabile» vuol dire: cambiando un asse, il contratto d'uscita resta lo stesso. Apertura (cinque righe, misurate):

> **Un sistema che sa che cosa non vede.** Una camera di profondità ferma **monitora attività e oggetti in un ambiente aerospaziale o industriale** (il varco di un hangar). È progettata per rilevare ostacoli ed elementi mobili, seguirli quando un ostacolo li nasconde e dire di ogni oggetto ed evento se è **osservato**, **previsto** o **sconosciuto**: ciò che non è osservato non è mai dato per libero, e la perdita di affidabilità è dichiarata. Con un'altra uscita, lo stesso nucleo serve all'**orientamento assistito di una persona non vedente** (oggi: avviso sonoro, a persona ferma). Il sensore sta su un supporto fisso o su una **piattaforma uncrewed ferma**. Stato: simulazione, sensore fermo; mai su una camera vera.

| Frase di `T` | Componente | Nella demo | Stato della prova |
|---|---|---|---|
| «trasformare immagini in informazioni»; «riconoscere… non basta» | profondità → griglia → tracce → registro; etichetta a lato | schermo; atto 3 | nessun fotogramma vero (VER §5); etichetta per lettura |
| «un ostacolo può nasconderlo»; «interruzioni della visibilità»; «continuità percettiva» | due strati, riaggancio | atto 4 | simulazione: identità 100 % (≥ 99,25 %), una persona, pannello fermo; con un secondo soggetto sbaglia sempre |
| «mentre la scena continua a cambiare» | seconda persona; registro | atto 4 | non provato (V2 §9) |
| «rilevare elementi mobili e ostacoli» | regola «mobile»; griglia a quattro stati | atti 2 e 3 | simulazione: 100 % entro 1 s a 2 m; ostacoli: conto fra 1,1 e 3 m |
| «distinguere le informazioni osservate da quelle incerte» | tre stati, anche su ogni evento | colori; colonna «stato» | per costruzione, in un verso |
| «feedback spaziali chiari e tempestivi» | regole; zona e ora nel registro | atti 2 e 3 | non verificato sull'hardware |
| «segnalando la perdita di affidabilità» | affidabilità persa | atto 5 | 0,13 s in simulazione; filtri della camera non provati |
| «monitoraggio di attività e oggetti in ambienti aerospaziali e industriali»; «osservazione e ispezione» | zone dichiarate e registro (`requisiti-2`) | registro in ogni atto; varco di hangar | V2: non coperto; registro: logica controllata; oggetti fermi non provati; 3 m, al chiuso; l'ispezione non è una funzione |
| «orientamento assistito di persone con disabilità visiva» | stesso nucleo, suoni | chiusura, persona bendata ferma | etichetta (ATT S4) |
| «bassa latenza ed efficienza elaborativa» | catena geometrica su CPU | contatore | non risolta: 155 ms contro 150 |
| «sicurezza delle indicazioni» | invarianti | atto 1; prova scelta dal giurato | per costruzione; mai su profondità vera; vetro smentito |

**Da rinominare** (righe di `tex`; anche titolo, §2 e §4 di SP).

- 47: «due ambiti d'uso: veicoli uncrewed (caso principale)» → «due applicazioni della traccia: monitoraggio di attività e oggetti in ambienti aerospaziali e industriali (caso principale) e orientamento assistito».
- 144: «Veicoli uncrewed» → «Monitoraggio (stazione ferma)». 151, 157: «sentinella uncrewed» → «stazione di osservazione di un varco». 158 → «una stazione ferma osserva il varco di un hangar».
- 146–150: autopilota e messaggio per settori → «sviluppo, mai simulato» (ATT §3); «camera sul veicolo; LiDAR o radar» → «supporto fisso a 1,2 m, o piattaforma uncrewed ferma alla stessa quota» (ATT S7); «indossata al petto» → «su treppiede, accanto alla persona ferma»; via la classe «piccolo drone» (SP §3.3).
- 160: «un autopilota non avanzerebbe» → «il registro dice: zona non osservata». 59: «quattro requisiti su otto» → «quattro richieste della traccia». 188: l'ordine per «sistemi uncrewed» resta una riga di contesto (fonte in `QUADRO_DOMINIO.md`, non riverificata da me).

**Guadagno:** criterio 5 del contratto. **Vincolo:** ogni frase con «uncrewed» contiene «ferma» o «non provato». **Chi la prova:** redattore e lettore critico. **Falsificatore (2 minuti), esito scritto prima:** nel nuovo sorgente `grep` trova «monitoraggio di attività e oggetti» nelle prime dieci righe, nessun «uncrewed» in testata e titoli, nessun «volo stazionario» (il v0.3 fallisce tutti e tre). Poi un lettore esterno, dopo 30 secondi sull'apertura, dice che cosa fa il sistema: la smentisce la risposta «un drone».

### `requisiti-2` — Un registro di eventi sopra gli stati

**Enunciato.** Un modulo legge solo gli stati delle tracce, le regioni di possibile presenza e l'affidabilità, e scrive righe «ora, evento, zona, stato»: ingresso, uscita, sosta, scomparsa dietro l'ostacolo, ricomparsa, permanenza non osservata, in zona non noto, affidabilità persa e ritrovata. **Regola unica:** un evento «osservato» nasce solo in un fotogramma con una misura; senza misura non c'è né «uscita» né «ingresso».

**Costo** (misurato): 99 righe di Python; 48 µs per fotogramma con 20 tracce e 8 zone, massimo 0,27 ms (0,4 % del ciclo). Lavoro: 3–4 ore-persona (stima, non verificata).

**Esiti** (cinque tipi di scena, 200 scene per braccio).

- **Reggono:** B2 (0 «osservato» a soggetto nascosto, 0 uscite false); B3 (l'estrattore ingenuo dà un'uscita falsa in 200 scene su 200: la prova non è cieca); B5; B6 (chi esce dalla portata restando in ombra non genera «uscita»: 40 su 40, 39 su 40 con rilevamento 0,9; resta «permanenza non osservata»); B8 con rilevamento certo (40 su 40).
- **B1 smentita.** 97 dei mancati sono l'uscita da una zona che finisce a 0,13 m dal bordo della portata: non si conferma in 3 fotogrammi, e il registro scrive «in zona non noto». Gli altri 6 sono ricomparse dopo il sensore coperto (critica 9). I ritardi reggono: al 95° percentile ≤ 0,27 s (0,33 s con rilevamento 0,9).
- **B4:** 0 violazioni; smentite le altre tre voci: 1 «scomparsa» spuria in campo aperto (prevista 0); chiusure spurie in 113 scene per un difetto del mio oracolo (1 su 200 nella seconda lettura); eventi mancati nel 52 % delle scene, 16 % nella seconda lettura (previsto ≤ 2 %; non diagnosticato).
- **[dopo]** 166 ingressi su 482 escono come «presente, ingresso non visto»: la traccia nasce già dentro la zona.

**Copre** «monitoraggio di attività» e mette lo stato su ogni informazione. **Vincoli.** Zone ad almeno v_max × 4 fotogrammi dal bordo del campo (0,37 m a 1,4 m/s); nessun modello appreso; il registro non nomina l'attività. **Demo:** una colonna «registro» a lato dello schermo; il giurato decide quando l'attore si ferma dietro il pannello e legge «permanenza non osservata da 5 s». **Chi la prova:** validazione, con un simulatore d'altro autore; poi una registrazione vera annotata a mano. **Falsificatore (1 minuto):** il comando del §1; atteso 0 violazioni e braccio ingenuo fallito; la smentisce una sola «uscita» a soggetto nascosto. **Non provato:** due soggetti nella stessa ombra; gli eventi sugli oggetti fermi, che chiedono lo stato delle celle per zona.

## 6. Dopo, e le ambiguità per gli organizzatori

Le scioglie chi organizza; all'utente resta se tenere la riga sull'ordine «uncrewed».

1. **«Oppure»:** una applicazione o due? Due sono un merito o una dispersione?
2. **«Attività»:** bastano eventi su zone e oggetti, o va nominata l'attività?
3. **Ambiente e scala:** una stazione fissa al chiuso, a 3 m, vale come modello in scala? Ci sono dati o hardware forniti?
4. **Soglie:** c'è un limite di latenza o un hardware di riferimento? La camera di profondità è ammessa fra le «immagini»?
5. Criteri e pesi della giuria; demo dal vivo o registrata.

Per lo sciame: fissare la soglia di memoria prima delle misure di Q1; scrivere e provare la regola per le tracce vive alla perdita di affidabilità; confrontare voxel e griglia sull'occlusore basso entro 3 m, il solo punto in cui Q1 serve la traccia.

**Misure di questo file.** L'apertura: 694 caratteri, **5 righe** composte con il preambolo di `tex` (xelatex, in una cartella temporanea). Il file: 2340 parole circa, cioè 3,0 pagine sul metro di 775 parole a pagina; composto con pandoc e xelatex (A4, corpo 10, margini 1,8 cm) fa **3 pagine e 25 righe**: su quel metro supera il limite di poco meno di mezza pagina, per la tabella.
