# Previsioni — sciame-esperto-dominio, f9 (S6, S7, S8)

Scritte alle 2026-11-14T15:40:31+01:00 (`date -Is`), PRIMA di ogni ricerca in rete e di ogni conto o simulazione di questa consegna.
Prima di scriverle ho letto solo: il contratto f9, gli addendum, la preproposta per intero, la traccia, SOLUZIONE_V2.md, il sorgente v0.5 e il mio quadro di dominio f6 (QUADRO_DOMINIO.md). Le previsioni vengono dalla mia memoria del campo: per questo ognuna ha la sua smentita.

| # | Previsione | Misura | Soglia di smentita |
|---|---|---|---|
| esp9-P1 | «ABAR» NON è il nome consolidato di un sistema aeroportuale contro gli urti con volatili: i termini del campo sono «avian radar», gestione del rischio fauna, BASH | ricerca in rete su fonti primarie (FAA, ICAO, EASA, SKYbrary, costruttori) | smentita se una fonte primaria usa «ABAR» come nome di un sistema o di una classe di sistemi per il rischio volatili |
| esp9-P2 | Nel TCAS II l'avviso di traffico (TA) non autorizza manovre (solo ricerca visiva e preparazione); l'avviso di risoluzione (RA) è un'indicazione di manovra verticale che il pilota esegue subito, anche contro il controllore. Soglie di tempo: TA circa 20–48 s, RA circa 15–35 s dal massimo avvicinamento | SKYbrary / FAA / EUROCONTROL | smentita se la fonte dà al TA una manovra, o tempi di RA sotto 5 s o sopra 60 s |
| esp9-P3 | Le luci di stato della pista (RWSL) sono automatiche, rosse, guidate dalla sorveglianza; lo spegnimento NON è un'autorizzazione. «Runway Hold» non è il nome di un sistema; «TA / HOLD / RA» non è una scala di alcun sistema reale (mescola bordo e terra) | FAA / SKYbrary | smentita se una fonte dice che le luci spente equivalgono a un'autorizzazione, o se esiste una scala «TA/HOLD/RA» |
| esp9-P4 | I radar per volatili lavorano a chilometri, danno consapevolezza a chi gestisce la fauna e non comandi né avvisi in tempo reale standardizzati ai piloti | FAA AC 150/5220-25, SKYbrary | smentita se la fonte descrive avvisi di risoluzione automatici ai piloti come funzione standard |
| esp9-P5 | La distanza protettiva della sorveglianza di velocità e separazione (ISO/TS 15066) ha la forma S = S_h + S_r + S_s + C + Z_d + Z_r: contiene già il tempo di reazione (latenza) e due termini d'incertezza di posizione | fonte che riporti la formula | smentita se la formula non ha termini d'incertezza o di tempo di reazione |
| esp9-P6 | Con i numeri del nucleo (v persona 1,6 m/s, latenza 0,155 s) e una reazione umana di 1 s, la distanza protettiva per un sistema che «chiede a una persona» supera 2 m (cioè oltre due terzi della portata di 3 m); con arresto automatico in 0,3 s scende sotto 1,5 m | conto a mano con le costanti della norma verificate | smentita se il primo valore è < 1,5 m o il secondo > 2 m |
| esp9-P7 | S8 alla lettera («attesa se una cella del corridoio è non osservata»): con un corridoio che parte dal sensore (0–3 m) l'attesa è accesa nel 100 % dei cicli a scena vuota; con il corridoio dentro la zona 1,24–3 m e buchi indipendenti (suolo valido 0,95 per fotogramma, regola dei 3 fotogrammi del nucleo) l'attesa scatta comunque in più dell'1 % dei cicli a scena vuota, cioè più di 9 falsi al minuto a 15 Hz | simulazione Monte Carlo in Python, seme fisso | smentita se nel secondo caso i cicli in attesa sono < 0,1 % |
| esp9-P8 | S7 non porta informazione nuova rispetto a S6: velocità angolare del rilevamento = d_CPA·|v|/r² (stessa grandezza r×v). Inoltre il rilevamento va preso dal punto protetto, non dal sensore: un oggetto diretto al varco a 1 m di lato dal sensore ha rilevamento NON costante visto dal sensore | identità algebrica + verifica numerica su 10 000 stati casuali; un controesempio numerico | smentita se lo scarto relativo massimo dell'identità supera 1e-9, o se nel controesempio la velocità angolare vista dal sensore resta < 2°/s |
| esp9-P9 | «P_intrusione ≈ 0 ⇒ nominale» soffre della diluizione della probabilità: su rotta di collisione esatta (d_CPA = 0), con il rumore di processo del nucleo (q = 0,2 m²/s³) e volume protetto di raggio 0,5 m, la P_intrusione calcolata a 2 s dal massimo avvicinamento resta sotto 0,30; e CRESCENDO il rumore di misura la P cala (il dato peggiore sembra più sicuro) | conto in forma chiusa + Monte Carlo, seme fisso | smentita se P(2 s) ≥ 0,5, o se P non cala al crescere del rumore |
| esp9-P10 | Costo di calcolo di S6+S7 per traccia: < 0,05 ms in Python puro (trascurabile rispetto ai 66,6 ms del ciclo) | misura con timeit su CPU | smentita se > 1 ms per traccia |

Indipendenza: le previsioni P7–P10 le verifico con codice mio, sugli stessi numeri del nucleo (stessa specifica, stesso autore delle previsioni): valgono per errori di conto, non per errori di modello del sensore. P1–P5 le verifico su fonti esterne riassunte da un modello ausiliario (lo strumento di lettura): le citazioni fra «» vanno ricontrollate dal curatore.

## Esiti (scritti alle 2026-11-14T15:46+01:00, DOPO le prove; nessuna riga sopra è stata ritoccata)

| # | Esito | Prova |
|---|---|---|
| esp9-P1 | **smentita** | Un costruttore usa la sigla: DeTect, «MERLIN Aircraft-Birdstrike Avoidance Radar (ABAR)» (slide di J. Lewis, PDF aperto e letto come testo). Resta vero che non è un termine FAA/ICAO: la circolare FAA parla di «avian radar» |
| esp9-P2 | **regge** | Guida ACAS di EUROCONTROL, ed. 5.0 (PDF letto come testo): §6.1, §9.1.1, §9.2.1, tabella 16 |
| esp9-P3 | **regge**, con un limite | AIM 2-1-6 letto in una riproduzione di terzi (faa.gov risponde 403); Wikipedia aperta. «TA/HOLD/RA» non compare in nessuna fonte letta: è un'assenza su un campione, non una prova |
| esp9-P4 | **regge, precisata** | Il sistema MERLIN dà avvisi di rischio in tempo reale (LOW / MODERATE / SEVERE per zona) a controllori, gestori e, tramite loro, ai piloti; nessun comando di manovra. Non l'avevo previsto così esplicito |
| esp9-P5 | **regge** | Marvel e Norcross (PMC5117641, aperta): termini T_R, T_S, C, Z_S, Z_R |
| esp9-P6 | prima metà **regge** (2,80 m); seconda metà **mancata di 0,18 m** (1,68 m contro «< 1,5»), sotto la soglia di smentita (2 m). Senza il termine C: 1,95 e 0,83 m | `prove/risultati_p8_p9_p10.txt` |
| esp9-P7 | **regge** | 73,2 % di celle non osservabili nel corridoio 0–3 m (attesa permanente); a scena vuota con suolo valido 0,95: 5,72 % dei cicli, 44,8 ingressi in attesa al minuto. `prove/risultati_p7.txt` |
| esp9-P8 | **regge** | scarto 3,0e-16; controesempio 6,9–21,2 °/s visti dal sensore contro 0,0 dal punto protetto |
| esp9-P9 | **regge** | P(2 s) = 0,16–0,18 su rotta di collisione esatta; con rumore 0,20 m scende a 0,12 (a 1 s: da 0,75 a 0,45) |
| esp9-P10 | **regge** | 0,42 microsecondi per traccia (solo la formula, Python puro) |

Notato dopo, non previsto: (1) la regola S8 rimette il difetto che la correzione C3 del nucleo aveva tolto; (2) la guida ACAS dice che il TCAS stima il tempo al massimo avvicinamento nell'ipotesi peggiore (rotta di collisione), non con una probabilità; (3) COLREG 7(d)(ii): il rischio può esistere anche con rilevamento che cambia, a distanza ravvicinata; (4) il conto della distanza protettiva dà 1,44 m/s di velocità coperta, vicino all'1,4 m/s del verdetto, che però viene da un altro conto (fascia di 0,40 m): coincidenza non spiegata.

Comandi per rifare: `cd prove && timeout 120 python3 p7_corridoio.py` e `timeout 120 python3 p8_p9_p10.py` (semi fissi 20261114; Python 3.14, nessuna libreria esterna).
