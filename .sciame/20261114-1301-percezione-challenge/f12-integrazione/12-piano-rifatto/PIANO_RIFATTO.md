# PIANO_RIFATTO — il piano 14 + 4 rifatto con ipotesi diverse (`sciame-rovesciatore`, f12, secondo ruolo di C-E)

Lavoro dalle 18:09 alle 18:21 del 14 novembre 2026 (`date -Is`); circa 2 600 parole, in gran parte tabelle: al limite delle tre pagine, e lo dichiaro. Cartella `f12-integrazione/12-piano-rifatto/`: `PREVISIONI.md` (18:09:23, prima di aprire il piano), `rifai_mc.py` → `risultati_rifai_mc.txt` (più i due lanci precedenti), `mediane_alt.py` → `mediane_alt.txt`, `prove_riuso.txt`. Si rifà con `timeout 300 ../../f10-dati/ambiente/venv/bin/python -I -B rifai_mc.py` (circa 2 s). **Tutte le durate sono stime, non misure; tutto è simulazione; niente è «validato».**

## 0. In testa: cambi di stato, regole violate

- **«Il minimo dimostrabile (MD) chiude entro l'ora 14» (piano §10: 0,29–0,46): con ipotesi più dure è da 0,37 a 0,001.** Stato proposto: **non provato, e smentito come obiettivo di calendario** in ogni modello mio con stime mie (al più 0,26). Va sostituito da una scala di cose che entrano nel tronco (§5).
- **Continuità e sicurezza non sono tutte sul percorso protetto del piano**: quattro punti le toccano di nascosto (§4). Il piano non nomina nessun F-401…F-413 (`grep -c "F-40" PIANO_14_4.md` = 0): è stato scritto prima di VD.
- **Prova sull'identità:** `06-identita/IDENTITA_SU_PROFONDITA.md` consegnata alle 18:18, letti §0–§2; **la controprova non è ancora consegnata** (alle 18:20 la cartella `07-controprova-identita/` esiste, `CONTROPROVA_IDENTITA.md` no): ciò che ne uso resta «preliminare, senza controprova».
- **Mie previsioni (8):** rov-P1 **smentita** (previsto 0,35–0,70; uscito 0,001 duro, 0,013 con le stime del piano); rov-P5 **smentita** (il rovesciamento A alla lettera vale +0,001…+0,076, non +0,10); rov-P2, P3, P4, P6, P7, P8 **reggono**.
- **Regole violate e scostamenti.** (a) Primo lancio di `prove.py` con l'uscita mascherata da `tail` e senza `-I`: rifatto (R1 bis). (b) Il calendario alternativo è stato **ridisegnato due volte dopo aver visto i numeri** (chi chiude lo scheletro; tolto il cancello dell'ora 5): va letto come scelto dopo; le sezioni 4–7 del programma sono nate dopo il primo lancio. (c) `mediane_alt.py` gira senza `-I` (importa il modulo accanto). (d) Non letti per intero: VN, V7, V8, V9, audit, f6, `SOLUZIONE_V3.md`; di `PROVA_INSIEME.md` §0–§1; `piano_mc.py` non letto (apposta). Letti per intero: contratto, piano, VD. Niente git, sudo, rete. *Indipendenza:* con il piano condivido il grafo dei compiti, le sue stime (nelle righe dette «del piano»), il modello linguistico; non il programma né le ipotesi.

## 1. All'indietro dall'ora 14 e dall'ora 18

| Ora | Che cosa deve esistere (risalendo dalla giuria) | Che cosa dice il piano (sue mediane) | Giudizio |
|---|---|---|---|
| 14 | la demo scorsa due volte e registrata; tabella firmata. Quindi prova generale **dalle 13:15** | PG 13,5–14,25: **la mediana del piano stesso manca l'ora 14 di un quarto d'ora** | non regge |
| 11–12 | tutto ciò che si mostra è nel tronco, e il tabellone è già corso **almeno una volta** su quel tronco (serve un giro di correzioni) | prima corsa di tutto insieme (PI) 11,1–12,05; TAB 12,3–13,5: nessun giro di correzione | non regge |
| 8 | scheletro di punta a punta (catena → file per fotogramma → schermo → tabellone) con «libero» corretto e una regione disegnata | B2 chiude a 5,8, ma lo schermo la disegna a 9 e il primo tabellone è all'ora 9 | un'ora tardi |
| 5 | una sequenza simulata scorre sullo schermo **dalla catena di f10 così com'è**; il tabellone base stampa le cifre di oggi (0 su 90) | C1 all'ora 5, D2 all'ora 9: niente di punta a punta prima delle 9–12 | manca |
| 2 | ambiente su 5 macchine; formato per fotogramma gelato (= `fotogrammi.jsonl` di f10); le quattro scene della demo scelte; macchina della demo provata | K0 a 1,0 con formato | regge, se K0 è preparato prima |
| 18 ← 17:15 ← 16 | consegna ← prova generale 2 ← gelo finale: fra 14 e 16 entrano al più due pioli | uguale | regge |

## 2. Simulazione rifatta (20 000 estrazioni per riga; Wilson al 95 % entro ± 0,007; tre semi: 0,001 / 0,001 / 0,001)

**Ipotesi dichiarate.** Stesso grafo del §3 del piano. *Stime mie*: più larghe dove c'è codice altrui da capire (B1 1/2/4; B2 1,5/3/6; B3a e B3b 2/3,5/7; D2 3/5/9; PI 1/2/4; K0 0,5/1/2,5). *Modello duro*: sottostima comune × 1,10; fattore di squadra σ 0,20 e di persona σ 0,25; ore utili su ore d'orologio 0,62–0,74–0,85 (pasti 1 h, 5 min l'ora, punto di squadra di 10 min ogni 2 h: 10,7 su 14 = 0,76); dopo l'ora 10 × 0,90; la rilettura non passa alla prima nel 30 % dei compiti di riuso (+0,5–2 h); +0,1–0,6 h a ogni compito che dipende dal lavoro di un altro; una persona ferma 2 h con probabilità 0,5; il sensore che arriva distrae P5 per 0,5–1,5 h (0,5) anche se è inutilizzabile; macchina della demo lenta, scoperta in prova (0,3; +0,5–2 h). *Medio*: a metà (0,70–0,80–0,90; 20 %; 0,3; 0,3; 0,2). *Leggero*: come il piano.

| Caso | Leggero | Medio | Duro |
|---|---|---|---|
| Piano con i tagli, **stime del piano** | **0,370** [0,363; 0,376], mediana 14,9 h (il piano dice 0,46 e 14,25) | 0,081; 18,1 h | **0,013**; 23,0 h |
| Piano con i tagli, stime mie | 0,055; 19,0 h | 0,007; 22,8 h | **0,001** [0,001; 0,002]; 29,0 h |
| Piano + F-401/402/408/409 sul percorso (F4) + THÖR ridotto | 0,021; 20,2 h | 0,002; 24,3 h | 0,000; 30,9 h |
| Calendario alternativo, con cancello all'ora 5 | 0,097; 16,7 h | 0,014; 19,5 h | 0,002; 24,5 h |
| **Calendario alternativo (§5), senza cancello** | **0,262**; 15,7 h | 0,056; 19,0 h | 0,007; 24,3 h |

Taratura del programma: minimo intero, stime e modello del piano: 0,294 (piano 0,29); continuità e sicurezza nel tronco alle ore 12 / 14 / 16: 0,69 / 0,89 / 0,96 (piano 0,70 / 0,88 / 0,96). Con i tagli do 0,37 contro 0,46: differenza non indagata (non ho letto il suo programma). Una persona ferma 2 h di sicuro: 0,001 (duro).

**Che cosa decide.** Sul leggero, una ipotesi alla volta (stime mie, base 0,055): ore utili 0,74 → 0,007; sottostima × 1,10 → 0,018; attrito fra persone → 0,023; rilettura → 0,031; persona ferma, sensore, macchina lenta, stanchezza → 0,043–0,046. **Il sensore non decide; decidono le mie stime (0,37 → 0,055) e le ore utili.** **Compito che decide: PI, la prima corsa di tutto insieme** (sul percorso critico 0,97; correlazione di rango fra durata e fine +0,68), poi la fila di P2: B2 (0,69; +0,64), B1 (0,69; +0,58), B3a (+0,66). Con stime mie P2 da solo ha in fila K0 + B1 + B2 + B3a + PI: 13,7 ore di lavoro medie, 15,7 con la tabella e la prova generale.

## 3. Le stime «di riuso» verificate sul posto (`prove_riuso.txt`)

| Riuso | Misura mia | «Un'ora di rilettura» è credibile? |
|---|---|---|
| Catena f10 | 1 868 righe (1 327 in 11 file, 541 di prove); **25 prove su 25 in 4,6 s** nella struttura di f10; **copiata senza `03-infrastruttura` accanto: 2 errori su 25** (P1, P14). Ambiente 730 MB legato a `/usr/bin/python3.14` di questa macchina; sequenze 1,8 GB | A1 (571 righe in 1 h): **sì**. K0 «25 verdi su ogni macchina» in 0,75 h: **non verificato** su altre macchine; va preparato prima dell'ora 0 |
| Predittori in C (`comp.c`) | compila (gcc -O2 -Wall); senza `taratura.txt` nella cartella non parte; 635 righe ma **49 984 byte: 79 caratteri per riga, massimo 542** (come 1 250 righe normali) | B1 (questo più 487 righe Python in 1,5 h = 748 righe l'ora): **no**. Propongo 1/2/4 e la lettura divisa: P2 solo `step_sd`, P5 il Python |
| Registro `eventi.py` | 418 righe, uscita 0 in 0,7 s | sì (ed è il primo taglio) |
| Correzione dell'identità (`06-identita`) | diff di 100–105 righe in 7 file (95 aggiunte e 5 tolte contate da me alle 18:09), dietro interruttori spenti; consegnata alle 18:18 | credibile in 0,5/1/2,5 h **se la controprova regge: non verificato** |

## 4. Continuità e sicurezza sul percorso protetto: quattro tagli nascosti

1. **Il taglio 8 lascia fuori dal minimo l'identità su profondità realistica** (A4*). Senza F-401/402/408 la scena 2 della demo cade al riaggancio (VD: 0 su 90; filtro fino a 5,00 m dalla verità). E la correzione F-401 **come scritta in VD tocca la sicurezza**: 98 e 91 celle·fotogramma «libero» nell'ombra vera (IDENTITA §0, preliminare); passa la variante sui gruppi (29–30 su 30 alle due risoluzioni), solo nella geometria del catalogo (a 0,3 m dal pannello: 0 e 1 su 10).
2. **B3b «mai tagliato» ha un criterio che la prova d'insieme ha fatto cadere**: con l'estraneo l'avviso è rilasciato senza aver visto il soggetto in 3027 su 3041, 3493 su 3616, 3239 su 3546 (`02-prova-insieme`, riga d). Il compito non può chiudersi com'è scritto.
3. **Il taglio 9 rimanda il controllo del piano (e)**: con la posa sbagliata di 1° un ostacolo di 10 cm è «libero» in 7 celle su 7 (F-404; condizione 4 rivista). In riproduzione non si vede; col sensore sì.
4. **Il taglio 7 toglie dall'ora 14 l'unica riga su persone vere.** Il predittore mostrato (`sd-0`) non è mai corso su THÖR (0,977 / 1,000 / 1,000 è del filtro con q = 0,2): la «valutazione realistica» resta solo simulata.

## 5. Rovesciamenti

| Rovesciamento | Ore guadagnate / P(MD) | Che cosa si perde | Esito |
|---|---|---|---|
| **A. Catena di f10 com'è, niente riscritto fino all'ora 5** | alla lettera **costa**: 0,097 contro 0,262 senza cancello (leggero), 0,014 contro 0,056 (medio): le riletture finiscono già fra le ore 3 e 6. Vale la parte «scheletro prima»: coda PI + TAB da 3,7 a 1,75 ore medie di lavoro (**ipotesi mia, non misurata**) | niente davanti alla giuria; anzi all'ora 6–8 c'è già qualcosa da mostrare (scheletro entro l'ora 8: 0,63 medio) | **tenere lo scheletro, respingere il cancello** |
| **B. Valutazione = solo il tabellone «dentro k su n»** | senza LAT: mediana −0,2…−0,3 h, P +0,003 o meno. Togliere anche le righe di sicurezza libererebbe circa 2 h di P4, fuori dal percorso critico (0,03–0,05) | le righe «0 celle libere sotto un ostacolo» e «0 nascosti fuori dall'avviso» sono la prova della priorità 2 e sono riuso (`misura_libero.py` 146 righe, `misura_passaggi.py` 354). La traccia chiede «bassa latenza»: VD vieta già la frase | **accettare solo LAT → una riga del tabellone** (tempo per ciclo sulla macchina della demo) |
| **C. Niente suono** | 0,5 h di P3; P +0,000 (C3a sul percorso critico 0,00–0,01) | il primo ambito della traccia (persone con disabilità visiva) resta senza canale; «affidabilità persa» solo a schermo non raggiunge chi non vede | **respinto**: resta un suono |
| **Regola ed eccezione** (mio) | la demo «del tronco com'è» è nel piano l'eccezione dell'ora 11; qui è la regola dall'ora 0 | la parola «minimo chiuso» | **adottare**: gelo all'ora 12, pioli nominati sullo schermo |

**La scala al gelo** (medio; probabilità che il piolo sia nel tronco, da solo): piano + F4 all'ora 12: «libero» 0,99; avviso che finisce solo guardando (B3b) **0,16**; regione disegnata 0,60; stati senza vuoti 0,08; identità 0,69. Alternativo: scheletro 0,96; «libero» 0,99; avviso **0,84**; regione 0,48; identità 0,91; stati 0,34; tabellone base 0,87; righe della regione 0,22. Alternativo all'ora 14: avviso 0,94; regione 0,72; identità 0,97; stati 0,57; tabellone base 0,95; righe della regione 0,45; all'ora 16: avviso 0,98, regione 0,86, stati 0,77, righe 0,66. **Nel calendario alternativo e nel modello medio la regione per tutta l'occlusione, cioè l'imperativo, è nel tronco all'ora 14 in 7 casi su 10 e le sue cifre in meno di 5 su 10** (nel piano + F4: 0,81 e 0,77, ma con l'avviso a 0,35).

## 6. Correzioni obbligate al piano, in ordine

1. Obiettivo: non «MD chiuso» ma **scala con gelo all'ora 12**; ordine d'ingresso: «libero» → avviso → regione → identità → stati → sensore non in salute. Ciò che non è entrato sta dietro il suo interruttore, spento, e lo schermo lo nomina.
2. **F4 sul percorso protetto**, nella forma sui gruppi di `06-identita`, mai la soglia per cella; a ogni fusione il banco controlla «0 celle libere nell'ombra vera» e scatola almeno 9 su 10. Preliminare, in attesa della controprova.
3. **B3b riscritto**: l'avviso resta finché le celle non sono viste libere (F-409, `strato_resta`), dominio «un soggetto per ombra» sullo schermo, costo dichiarato (dietro un pannello fermo non si spegne: 140 su 140). A P1 subito dopo A2.
4. **B3a diviso** fra P2 (M2 + c2) e P5 (M1 + c4 + c7); nessuno ha in fila più di due compiti dopo la rilettura.
5. **Tabellone sul tronco dall'ora 7–8**; le righe della regione si scrivono contro il predittore che la catena ha già (`fabbrica_predittore`, `regione_prevista` in `catena.py`), così non aspettano B2 (nel mio modello aspettano ancora B2: su questo punto la scala è prudente); la riga THÖR del predittore mostrato resta nel minimo.
6. **Taglio 9**: la prova d'ingresso della posa (10 cm a 2,5 m esce «occupato») precede ogni fotogramma di un sensore vero.
7. LAT diventa una riga di TAB; la macchina della demo si prova all'ora 2.
8. K0 preparato prima dell'ora 0 (ambiente, struttura di f10, sequenze); etichetta fissa sullo schermo con l'origine della sequenza (simulata realistica, a mano, vera).

**Calendario minimo alternativo** (mediane del modello leggero in `mediane_alt.txt`; col medio tutto slitta di 1–3 h: per questo comanda il gelo, non la fine dei compiti).

| Ore | P1 sicurezza | P2 previsione | P3 schermo | P4 misura | P5 tronco e identità |
|---|---|---|---|---|---|
| 0–2 | K0; A1 rilettura mappa | K0; B1 `step_sd` | K0; C1 lettore | K0; D1; inventario spedito | K0; banco di regressione dai due `rifai.sh` |
| 2–5 | A2 «libero» nel fotogramma | B1 → B2 `sd-0` dietro l'innesto | C1 | tabellone base sulla catena com'è | F4 dal diff, con i due cancelli |
| 5–8 | A2 → F9 avviso che resta | B2 | **scheletro (ora 6–7)** → C2 disegno | **primo tabellone (ora 7–8)**; righe della regione sul predittore esistente | F4 → M1 + c4 + c7 |
| 8–11 | F9 → A3 ridotto con la prova della posa | B2 → M2 + c2 | C2 → «affidabilità persa», un suono | righe della regione, THÖR | M1 + c4 + c7 |
| 11–12 | **gelo**: entra solo ciò che passa il banco | idem | scaletta con i pioli mancanti | tabellone sul tronco gelato | regressione |
| 12–14 | difetti bloccanti | difetti bloccanti | diapositive | tabella firmata (12–13:15) | tempo per ciclo; **prova generale 13:15–14** |
| 14–16 | pioli rimasti, nell'ordine del punto 1; sensore solo dopo la posa | idem | registro (se resta tempo) | righe rimaste, M8 | c3, sensore; **gelo finale 16** |
| 16–18 | regressione | regressione | documento | tabellone finale | video, prova generale 2, consegna |

## 7. Stati proposti e che cosa propongo dopo

- «MD entro l'ora 14»: **non provato**; 0,37 (stime e modello del piano, programma mio) → 0,001 (duro). «Con il calendario alternativo»: 0,26 → 0,007, **sostenuto solo da stime mie**, scelto dopo.
- «La sicurezza dell'avviso è nel tronco al gelo»: 0,16 nel piano, 0,84 nell'alternativo (medio): **stima**.
- «Riuso con un'ora di rilettura»: **sostenuto** per la mappa, **smentito** per `comp.c`, **non verificato** per l'ambiente su altre macchine.
- **Misura che decide, all'ora 2** (come nel piano, la tengo): (fine di K0 + rilettura B1) / stima; sopra 1,5 vale il modello medio o duro.
- **Dopo:** l'arbitro assegna gli stati; la controprova di `06-identita` decide la correzione 2; l'utente decide se K0 si prepara prima dell'ora 0.
