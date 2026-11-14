# Previsioni — `sciame-esperto-dominio`, f11, sezione E

Scritte alle 2026-11-14T16:12:15+01:00 (`date -Is`), dopo la lettura dei file dello sciame e **prima** di riaprire in rete le fonti. Non si ritoccano: gli esiti stanno in fondo.

Misura: per ciascuna delle otto pagine qui sotto, apro il link citato nei file dello sciame e cerco la frase o il dato citato. Esiti: **regge** (la pagina si apre e il dato c'è), **smentita** (la pagina si apre e il dato è diverso o manca), **non risolta** (la pagina non si apre o lo strumento non mostra il passo).

| # | Fonte (link nei file dello sciame) | Dato atteso | Previsione | Soglia di smentita |
|---|---|---|---|---|
| E1 | comunicato della società sull'ordine del 21-10-2026 (`f6…/QUADRO_DOMINIO.md`, S2) | «1,7 milioni», «sistemi uncrewed», controllata CTMAVIO | regge | importo, data o oggetto diversi |
| E2 | PX4, prevenzione delle collisioni (S18) | «If there is no sensor data in a particular direction, velocity in that direction is restricted to 0» | regge | frase assente o di senso opposto |
| E3 | PX4, messaggio ObstacleDistance (S23, in f6 solo da motore di ricerca) | `UINT16_MAX` = sconosciuto; `max_distance + 1` = nessun ostacolo | regge | significati diversi |
| E4 | ASTERIX cat. 062, copia strutturata (S31) | bit CST «…(coasting)», bit CNF confermata o provvisoria | regge | definizione diversa |
| E5 | Marvel e Norcross, PMC5117641 (f7 S9, f9 F7) | formula della distanza protettiva con T_R, T_S, C, Z_S, Z_R | regge | termini diversi |
| E6 | The Robot Report, visione 3D e sicurezza (f7 S8) | «empty…, occupied, or unknown»; il non visto «treated as occupied» | regge, ma fonte di parte (autrice del costruttore) | frase assente |
| E7 | regolamento (UE) 2017/745, art. 2 punto 1 (copia su legislation.gov.uk) | «compensation for, an injury or disability» | regge | testo diverso |
| E8 | pagina di IATA sui danni a terra (f7 S14) | «nearly $10 billion by 2035»; 40 %; 42 % | regge almeno su due cifre | due cifre su tre diverse |

Previsione d'insieme: almeno 6 su 8 reggono; almeno una resta «non risolta» perché la pagina respinge i lettori automatici. Mi smentisce: meno di 5 «regge», oppure una sola «smentita» su E1, E2 o E4 (sono le tre che danno credito al nucleo).

Indipendenza: le pagine le legge lo strumento di lettura, che riassume con un modello ausiliario; condivido con i ruoli di f6, f7 e f9 lo strumento e il modello linguistico. Il controllo vale per «la pagina esiste e contiene il dato», non per la correttezza del dato nel dominio.

## Aggiunta, scritta alle 2026-11-14T16:13:30+01:00 (`date -Is`), prima di aprire queste altre quattro pagine

(Correzione dichiarata: nel titolo avevo scritto «16:17 circa» senza riportare l'ora letta; l'ora di `date -Is` era 16:13:30. Le quattro righe non sono state toccate.)

| # | Fonte | Dato atteso | Previsione | Soglia di smentita |
|---|---|---|---|---|
| E9 | Teleborsa, ingresso nel capitale di NIDO (f6 S7) | 20 % con opzione per il controllo; drone con stazione di ricovero; ispezione e sorveglianza | regge | quota o oggetto diversi |
| E10 | Websim, Task Force X (f6 S8) | partecipazione a un'iniziativa NATO con NIDO e CTM Avio; sorveglianza e protezione di infrastrutture | regge | assente |
| E11 | COLREG, regola 7 (f9 F5) | rischio se il rilevamento «does not appreciably change»; rischio possibile anche con cambio evidente «at close range» | regge | testo diverso |
| E12 | riproduzione dell'AIM 2-1-6, luci di stato della pista (f9 F6) | «does not substitute for or convey an ATC clearance»; «When the THLs extinguish, this is not clearance» | regge o non risolta (sito di terzi) | frasi assenti |

## Esiti

Prove fatte fra le 16:12 e le 16:15 del 14 novembre 2026, con lo strumento di lettura (che riassume: le frasi fra «» restano da ricontrollare sul testo grezzo dal curatore).

| # | Esito | Che cosa ho trovato |
|---|---|---|
| E1 | **regge su data, importo e oggetto; mancata sulla controllata** | Pagina della società aperta: titolo «Primo ordine da cliente estero da 1,7 milioni di euro per sistemi uncrewed», 21-10-2026, «circa 1,7 milioni di euro». Alla domanda diretta lo strumento risponde che «CTMAVIO», «CTM Avio» e «controllata» **non compaiono** nella pagina. La frase «la controllata CTMAVIO ha ottenuto il primo ordine estero» è nell'articolo di stampa (soldionline, aperto oggi). |
| E2 | **regge** | «velocity in that direction is restricted to 0»; avviso oltre 0,5 s; «HOLD mode» dopo 5 s; «treated as uncovered»; 4 m/s, 10 Hz, 0,1–0,5 s. |
| E3 | **regge** | «A value of max_distance +1 means no obstacle is present. A value of UINT16_MAX for unknown/not used.» In f6 era solo un risultato di ricerca: ora è pagina aperta. |
| E4 | **regge** | CST = 1: «Age of the last received track update is higher than system dependent threshold (coasting)»; CNF: «Confirmed track» / «Tentative track»; I062/290 «System Track Update Ages»; I062/500 «Estimated Accuracies». Letti i primi 100 000 caratteri su 102 356. Resta una copia strutturata, non il PDF ufficiale. |
| E5 | **regge, con una precisazione notata dopo** | Marvel e Norcross, Robotics and Computer-Integrated Manufacturing 44, 144–155 (in linea 2016, fascicolo 2017), DOI 10.1016/j.rcim.2016.08.001. Equazione 3, forma lineare, con i termini attesi. **Dopo:** l'articolo usa v_H = 1600 mm/s ma nota che ISO 13855 dà 2000 mm/s come massimo (1600 ammessi oltre 500 mm di separazione) e raccomanda 2000. |
| E6 | **regge nel senso, parole diverse** | Clara Vu (direttrice tecnica di Veo Robotics), 1° luglio 2020. Oggi: «classified as unknown and treated as occupied until the system can determine it to be otherwise»; il file di f7 riporta «treated as occupied for SSM purposes». |
| E7 | **regge** | «diagnosis, monitoring, treatment, alleviation of, or compensation for, an injury or disability». Copia su legislation.gov.uk, non EUR-Lex. |
| E8 | **regge** (tre cifre su tre) | IATA, 6 dicembre 2022: «nearly $10 billion by 2035»; «40% of total incidents»; «42% (IATA estimate)». |
| E9 | **regge** | Teleborsa, 9 giugno 2026: 20 %, diritto di salire al 51 % entro 24 mesi; drone H815, stazione, calcolo a bordo, oltre la linea di vista, supervisione remota; ispezione, monitoraggio di condotte e reti, sorveglianza perimetrale, duplice uso. |
| E10 | **regge** | Websim, 10 luglio 2026: Task Force X, Torre Veneri; NIDO e GMSPAZIO «partecipate», CTM Avio «partner industriale»; «la sorveglianza continua e la protezione delle infrastrutture critiche». |
| E11 | **regge** | Regola 7(d)(i) e (ii), come citate in f9. |
| E12 | **regge** | «does not substitute for or convey an ATC clearance»; «When the THLs extinguish, this is not clearance to begin a takeoff roll»; «Two aircraft, or a surface vehicle and an aircraft, are required…». Sito di terzi, non faa.gov. |

**Previsione d'insieme:** «almeno 6 su 8 reggono»: **regge** (7 piene e 1 con una parte mancata). «Almeno una resta non risolta perché la pagina respinge i lettori automatici»: **smentita** (12 pagine su 12 si sono aperte). Nessuna smentita su E2 ed E4; su E1 cade solo l'attribuzione della controllata alla pagina della società.

**Consultazioni senza previsione** (solo dati bibliografici, fatte dopo): arXiv 1706.08565 = Balch, Martin, Ferson, «Satellite conjunction analysis and the false confidence theorem», Proc. R. Soc. A 475, 20180565 (2019); arXiv 2608.01855 = Mandaokar e Rinner, «RADAR Perception for Dynamic Obstacle Avoidance onboard small-scale Quadrotor UAVs», v1 del 3 agosto 2026, v2 del 6 novembre 2026 (il riassunto dà errori medi fino a 0,15 / 0,93 / 0,87 m su x / y / z: f6 scriveva «errori laterali fino a 0,9 m»).

**Conto mio, notato dopo (non una previsione):** con v_H = 2,0 m/s al posto di 1,6 la distanza protettiva di `f9-preproposta/06-esperto-dominio/prove/risultati_p8_p9_p10.txt` (P6) passa da 2,80 a 3,26 m (richiesta a una persona) e da 1,68 a 1,86 m (arresto automatico): 2,0·1,155 + 0,95 e 2,0·0,455 + 0,95.
