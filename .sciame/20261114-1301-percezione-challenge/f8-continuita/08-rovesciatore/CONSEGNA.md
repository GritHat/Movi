Canarino: sciame-canarino-fe9992e292215898

# Consegna — `sciame-rovesciatore`, f8 (continuità visiva), f1 corsia B

Lavoro dalle 2026-11-14T15:14:09+01:00. File: `PREVISIONI.md` (scritte alle 15:17:19, prima del codice), `rov_f8.py`, `esito_rov_f8.txt` (più `_primo` e `_secondo`: le parti già viste non cambiano, `diff` vuoto). **Rifare:** `cd f8-continuita/08-rovesciatore; timeout 120 python3 -B rov_f8.py` (seme 20261114, 2–3 s di CPU, tempi indicativi).

## 1. Scostamenti e regole violate

- **Regole violate:** nessuna che io sappia. Ho importato in sola lettura `f2/04-torneo/scena_parte3.py` (generatore, visibilità e Kalman dell'avversario) con `-B`: nessun file scritto fuori dalla mia cartella (controllato).
- **Previsioni aggiunte dopo:** P-rov-2d, P-rov-3 e P-rov-2e sono state scritte dopo la prima o la seconda esecuzione (con l'ora, nel file), prima della loro misura. Portano **[dopo]**.
- **Mie previsioni cadute:** 1a nelle fasce (il nucleo emette più di quanto attendevo sul pannello da 1 m); 2b (attendevo una cella sotto l'80 %: il minimo è 87,0 %); 2c per «prosegue» (+8,1 punti, attesi ±5); 2e alla lettera (torna, pannello 2 m: 89,0 % < 90 %, per la finestra di 5,4 s); 1d mista.
- **Limiti:** la scena è quella del torneo (pedone puntiforme a 4 m, portata 6 m, ombra esatta, sensore fermo), **non la scala della demo**; la regola del nucleo è riprodotta dal testo di §B5, non da `sim_v2.py`; quattro comportamenti su sei (**mancano «rallenta» e «svolta»**); taratura e prova vengono dallo stesso generatore (semi diversi, e una geometria diversa). Le regioni A e B sono mie: sono riferimenti di prova, non il predittore proposto.
- **Non letti:** `AUDIT.md`, `CONTROPROVE.md`, `MISURE.md`, `MOTO_PROPRIO.md`, `ATTACCO_SPECIALIZZAZIONE.md`, i PDF; di specializzazione, proposta e creativo di f1 solo le righe trovate con `grep`.

## 2. Q3 — l'imperativo è rispettato? (le parti che mi competono)

| Parte | Esito | Prova |
|---|---|---|
| Nucleo, regola «previsto → perso» (B5, strato 2) | **non rispettato** (controllo 1) | T1a: stima emessa nel **60,8 %** dei cicli in ombra (pannello 1 m) e nel **39,8 %** (2 m); in sosta 40,0 % e 28,5 %, vuoto mediano 3,13 e 3,93 s. Alla scala della demo è peggio: «previsto» 0,40–0,53 s su 1,07–1,13 s di buio (35–50 %, conto mio sulle mediane di `MISURE_V2.md`, P4); in sosta «perso» 4,6–4,8 s |
| Nucleo, la regione del «previsto» (cerchio del Kalman, q = 0,2) | **non rispettato** (controllo 3) | T1b: al livello 90 % copre 44,4 % (torna, 2 s), 49,0 % (lontano, 2 s), 71,2 % (sosta, 2 s), 100 % (prosegue); al livello 50 % da 6 a 100 % (celle con n ≥ 30) |
| Nucleo, strato di possibile presenza | **rispettato** per i controlli 4 e 5; è già la regione giusta, chiamata male | T1c: la regione al 90 % tarata sul comportamento peggiore copre l'**86–90 % dell'ombra** fra 1,5 e 3 s (regione A; 78–98 % con la B) |
| Criteri di accettazione (V2 §7, R3) | **non rispettato** | misurano solo l'identità al ritorno; «area prevista ancora mostrata» è «tolta dalla promessa»; nessuna misura di taratura |
| Specializzazione | **non rispettato**, per il suo stesso testo | riga 83: «per le classi veloci si riduce a un istante: resta perso» |
| Proposta v0.5 | **in parte**: lo dichiara «in revisione» | `proposta_sciame.tex`, righe 94, 157, 164 |
| Sensore in moto | **non verificato** | non letto |

## 3. Critiche

1. **«Perso» è una soglia d'informatività usata come interruttore di visibilità.** La regola «meno di metà dell'ombra» dice quando la previsione smette di informare; il nucleo la usa per spegnerla. Prova: T1a (sopra). Il vuoto non nasce dal predittore: nasce dalla regola.
2. **Tenere acceso il cerchio non basta: è sbagliata la forma, non la scala.** Un solo fattore ricavato dai salti alla ricomparsa (k90 = 3,58 contro 2,15) porta il livello 90 % all'87–100 % in ogni cella con n ≥ 30, ma lascia il livello 50 % fra 17 e 100 % (T2b). Una gaussiana sola non rende «prosegue» e «si ferma o torna» insieme: servono almeno due modi.
3. **Il punto fluido è il danno dell'imperativo preso alla lettera.** T3: a 2 s senza osservazione il punto a velocità costante sta su **suolo visto libero** nell'86–88 % dei casi (sosta, torna, lontano), a 1,4–1,9 m dal soggetto; a 3 s nel 96–100 %, a 2,3–3,0 m (torna: n = 15). È un movimento continuo, liscio e falso, disegnato dove il sensore vede vuoto.
4. **Sicurezza e continuità sono la stessa regione a due livelli.** Da 1,5 s la regione onesta al 90 % (a disco) è quasi tutta l'ombra (T1c: 86,4 / 89,5 / 89,5 % a 1,5 / 2 / 3 s; il torneo dà 52–68 % alle particelle con sosta, che però perdono chi esce dal lato lontano). L'informazione vive nel livello 50 %: 0,6 / 4,3 / 27,8 / 52,3 / 47,6 % dell'ombra a 0,5 / 1 / 1,5 / 2 / 3 s.
5. **Una taratura in metri non passa da un'ombra all'altra [dopo].** T1e: la regione B (raggio in metri dall'ultima osservazione), tarata sul pannello da 1 m, sul pannello da 2 m copre 15,3 % (prosegue, 2 s), 0,0 % (prosegue, 3 s), 26,0 % (lontano, 3 s); la regione A (in unità di σ(t) del filtro) tiene il 93,6–100 % fino a 3 s e scende a 83,3 e 78,7 % per «torna» a 4 e 5 s. La popolazione «ancora nascosta» dipende dalla geometria: la taratura va dichiarata per geometria.
6. **La ricomparsa è una verità parziale.** Chi esce dal lato lontano non dà campioni (0 su 300, T2a). Il percorso ricostruito all'indietro con un ponte rettilineo falsa la copertura da −78,6 a +8,1 punti (T2c). La scala ricavata dipende dalla miscela vista: con 90 % di «prosegue» k90 scende a 0,98 e la copertura al 90 % crolla (sosta 17,7 % a 2 s; T2d [dopo]).
7. **Due difetti nel criterio del contratto.** (a) Il controllo 1 confronta il salto alla ricomparsa «con la regione dichiarata», il controllo 4 vieta alla regione lo spazio visto libero: la prima misura cade per definizione su spazio visto libero. Va scritto «regione del ciclo precedente, dilatata della fascia» (0,40 m; conto mio: mezzo corpo 0,2–0,3 m più 0,1 m per ciclo; **non verificato**). (b) Il controllo 3 chiede la copertura «per tempo e per comportamento», ma a soggetto nascosto le popolazioni si svuotano (prosegue: n = 13 a 2 s, 0 a 3 s): le celle con n < 30 vanno dichiarate vuote, non mediate.

## 4. Stati proposti

| Enunciato | Stato |
|---|---|
| Il nucleo V2 rispetta il controllo 1 | **smentito** (60,8 e 39,8 % in simulazione; 35–50 % alla scala della demo, per conto) |
| Basta tenere acceso il cerchio del Kalman | **smentito** (T1b) |
| Oltre circa 1,5 s la regione al 90 % tarata coincide quasi con la possibile presenza | **sostenuto dai dati** (una scena, quattro comportamenti, 1,5–3 s, regioni a disco); a 4–5 s resta solo «sosta»: non verificato |
| Un punto che prosegue liscio oltre l'orizzonte inganna | **sostenuto dai dati** (T3; P-rov-3 regge) |
| Centro sull'ultima osservazione meglio del centro a velocità costante | **smentito** come regola (meglio a 2 s, peggio a 3 s, non si trasferisce) |
| Il percorso ricostruito alla ricomparsa vale come verità | **smentito** (T2c) |
| La scala dalla ricomparsa tara il nascosto | **smentito** con miscela realistica (T2d); con miscela in parti uguali tiene il livello 90 % e non il 50 % |
| Lato e ritardo della ricomparsa etichettano il comportamento | **sostenuto dai dati**, prova facile: 4 etichette sbagliate su 1477 ricomparsi; i non ricomparsi entro 5,4 s (29 e 261 soste, 33 ritorni) restano senza etichetta |
| Previsioni: 1b, 1c, 1e, 2a, 2d, 3 | **reggono**; 1a, 2b, 2c (prosegue), 2e: **smentite** nei numeri detti al §1; 1d: mista |

## 5. Proposte per Q4

**rovesciatore-1 — «perso» non esiste: una regione annidata, e l'orizzonte toglie il punto, non la regione.**
- *Enunciato.* Per ogni traccia confermata entrata in un'ombra il sistema emette a ogni ciclo, fino a una chiusura motivata (riaggancio; celle viste libere, cella per cella), tre regioni annidate: **R100** = lo strato di possibile presenza, con le sue regole intatte; **R90 e R50** = le regioni del predittore ritagliate sul non osservato. Lo stato «perso» è sostituito da **«previsto ampio»**, che scatta quando R90 supera l'80 % dell'ombra: resta a schermo con un altro segno e dice «può essere ovunque nell'ombra». Il **punto** si disegna solo finché sta su una cella non osservata e R50 copre meno di metà dell'ombra. Le due soglie (80 % e metà) sono proposte, non misurate: si fissano prima della prova.
- *Regole che impediscono il danno.* (i) Una previsione non ha mai il segno dell'osservazione (contorno o tratteggio, mai pieno; sempre con l'età). (ii) Nessun punto su suolo visto libero e nessuna interpolazione grafica che aggiunga moto fra due stime. (iii) Oltre l'orizzonte del punto si mostrano solo regioni. (iv) Il predittore non tocca R100.
- *Guadagno atteso.* Stima emessa dal 40–61 % al 100 % dei cicli (per costruzione); nessun meccanismo di sicurezza nuovo; la soglia «metà dell'ombra» (K-004) diventa un cambio di segno.
- *Vincoli.* R50 e R90 chiedono un predittore con almeno due modi (critica 2), tarato per comportamento e per geometria (critica 5).
- *Chi la prova.* Kalman e tracciamento (predittore), validazione e statistico (generatore indipendente con «rallenta», «svolta» e corpo largo), avversario.
- *Falsificatore (3 s).* Le regioni del candidato al posto della regione A in `rov_f8.py`, griglia T1c/e. Cade se una cella con n ≥ 30 copre meno dell'85 % al livello 90 %, o se R50 supera il 60 % dell'ombra prima di 3 s. *Atteso, scritto ora:* regge al 90 % per prosegue, sosta e torna; **incerto su «lontano»** (il torneo: 22–41 %).

**rovesciatore-2 — si tara all'indietro: la ricomparsa etichetta il comportamento e tiene un contatore; non regola la scala.**
- *Enunciato.* A ogni ricomparsa il sistema registra lato, ritardo e se la prima misura cade nella R50 e nella R90 del ciclo precedente (dilatate della fascia). Ne ricava: (a) l'**etichetta** del comportamento, che aggiorna i pesi dei modi del predittore con un minimo dichiarato per «si ferma» e «torna» (i casi rari non si dimenticano); (b) un **contatore per etichetta** a schermo e nel registro («ultime N: k dentro la regione al 90 %»), più il numero dei non ricomparsi. Se un contatore esce dall'intervallo compatibile con il livello dichiarato, le regioni passano a «previsione non tarata» e R90 diventa R100. Il contatore può solo allargare o segnalare; non stringe e non tocca la possibile presenza.
- *Guadagno atteso.* È l'unica valutazione della precisione disponibile sul sensore vero senza verità esterna, ed estende «affidabilità persa» alla previsione.
- *Vincoli.* Vale solo all'istante della ricomparsa e per chi ricompare. Il contatore dev'essere per etichetta: mescolato, con 90 % di «prosegue» e il cerchio nominale leggerebbe 95,2 % (conto mio da T2a) mentre «torna» è al 4,0 %.
- *Chi la prova.* Statistico (intervalli con N piccoli), metrologo (protocollo sull'hardware con comportamenti recitati e una seconda camera oltre il pannello come verità).
- *Falsificatore (3 s, eseguito).* T2e: cade se le etichette giuste sono meno del 90 % per prosegue o torna. *Esito:* prosegue 300 su 300 nelle due geometrie; torna 300 su 300 (1 m) e 267 su 300 (2 m, 33 non ricomparsi): **soglia superata alla lettera, per la finestra di 5,4 s**; fra i ricomparsi 4 errori su 1477.

## 6. Che cosa propongo dopo

1. Al triage: adottare rovesciatore-1 come **forma dell'uscita** e passare ogni predittore candidato dalla stessa griglia (comportamento × tempo × due geometrie, celle con n < 30 dichiarate).
2. Rifare T1a e T1c **alla scala della demo** (portata 3 m, attore a 2,3 m, corpo largo, gruppo tagliato escluso) con un generatore di un altro autore che abbia «rallenta» e «svolta»: i miei numeri valgono per la scena del torneo.
3. Correggere il criterio del contratto nei due punti della critica 7 prima del torneo.
4. Sull'hardware: contatore alla ricomparsa su almeno 30 passaggi per comportamento recitato. Fino ad allora tutto ciò che è scritto qui è **simulazione, a sensore fermo**.
