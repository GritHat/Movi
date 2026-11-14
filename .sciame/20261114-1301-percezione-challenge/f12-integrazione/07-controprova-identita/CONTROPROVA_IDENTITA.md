# Controprova dell'identità al ritorno — f12, `07-controprova-identita` (`sciame-avversario`)

Lavoro dalle 2026-11-14T18:18:11+01:00 alle 18:33 (`date -Is`). Percorsi relativi a questa cartella. Oggetto: `../06-identita/IDENTITA_SU_PROFONDITA.md` e la sua configurazione finale «tutte_p». **Tutto è simulazione: niente qui è «validato».** Intervalli fra parentesi quadre: Wilson al 95 %, in percento.

## 0. In testa: cambi di stato e regole violate

- **Il criterio del verdetto dei dati (≥ 28 su 30 per caso, a 424 e a 848 px) non regge alla replica.** Sui semi dell'autore (k = 100…129) le sue cifre si rifanno identiche; sui semi mai usati k = 200…229 ottengo 30, 30, 28 a 424 px e 29, 30, **27** a 848 px (caso b, chi si ferma 3 s). Il tasso per passaggio è stabile (176 su 180 [94–99] a 424 px, 174 su 180 [93–98] a 848 px): la soglia di 28 sta sul bordo del tasso vero, e «passa» dipende dai semi. Stato proposto: da «sostenuta dai dati» a **«sostenuta come tasso (circa 97 %), non come superamento del criterio»**.
- **Il dominio è più stretto di quello dichiarato.** Cade anche con: persona oltre 2,6 m dalla camera (0 su 10), bambino di 1,0 m (2 su 10), posa sbagliata di +0,5° (6 su 10), rumore «limite» (0 su 10). Regge a 1,5–2,0 m, a 640 px, sugli altri due profili a 0,5 m/s, a 1,6 m/s, con buchi 3,5 volte più frequenti al rumore nominale, con persona scura.
- **Sicurezza: nessun controesempio contro le correzioni.** Su 381 sequenze mie «tutte_p» non aggiunge alcun «libero» nell'ombra vera (5 celle·fotogramma, le stesse 5 della catena di f10) e lascia la persona nascosta fuori dall'avviso in 0 fotogrammi su 2360 [0–0,2] (catena di f10: 379).
- **L'estraneo:** con le correzioni l'identità di A passa allo sconosciuto B in 19 casi su 20 [76–99]; la catena di f10 non la passava mai (0 su 20) perché non riagganciava niente. La correzione trasforma «nessuna identità» in «identità sbagliata marcata presunta». L'avviso resta su A: 0 fotogrammi fuori su 264 [0–1,4].
- **Regole violate, per errore:** (1) il primo lancio del rifacimento è fallito per un errore di shell, senza corse; (2) il rifacimento cancellava `tmp/`, cartella temporanea anche del mio banco: il blocco «geometria» è morto a metà ed è stato rilanciato intero, senza cambiare parametri (`risultati/registro_attacchi_1.txt`); (3) attese con `sleep`; (4) riassunti con il Python di sistema (sola libreria standard); (5) nei blocchi statici `n=30` vale 30 semi da 10 fotogrammi, non 30 fotogrammi: le numerosità sotto sono quelle vere. Niente git, sudo, rete; al più 8 processi; `f10-dati` e `06-identita` solo letti. **Non letti:** `ANALISI_DATI.md`, `VALIDAZIONE_DATI.md`, `22-avversario/`, `c1` di f8. **Scostamento dalla consegna:** il verdetto dei dati non l'ho letto per intero, solo le righe del criterio (riga 90), di K-403 e di K-407; del verdetto sulla continuità solo K-218 e K-219. Sequenze a 640 e 848 px: 0 GB su disco, si rigenerano in memoria (`rifai.sh`).
- *Indipendenza:* condivido con l'autore la catena (copia identica, `DIFFERENZE.md`), il simulatore, la sua verità, `misura_passaggi.py` e il modello. Sono miei: il riconto (`riconta.py`), i semi, le scene, le misure del vuoto, dell'estraneo, del gruppo sul bersaglio e della rimozione (`attacco.py`). Un difetto del simulatore o della misura di f10 non lo vedo.

## 1. Rifacimento e riconto

- **Rifatto:** `prova.py nuovi424` (prima, tutte, tutte_p) e `nuovi848` (tutte_p): 579 + 193 righe, **0 diverse** dall'autore nei campi deterministici (`risultati/RICONTO.md`, ultima sezione). Il codice su disco è posteriore alle sue misure (`catena/gruppi.py` 18:15:01, `nuovi424.jsonl` 18:06:54): la versione finale le riproduce.
- **Ricontato con programma mio:** tutte_p 29, 29, 30, 20 su 30, 30, 30, 20 a 424 px e 30, 29, 29, 20 a 848; «tutte» a05 0 e 16 su 30; «libero» in ombra 0 · 4 (tutte_p) e 98 · 91 (tutte); nascosta fuori dall'avviso 0 su 3921 e 0 su 3922; scatola 100 su 100; avviso acceso alla fine 140 su 140. Tutte coincidono.

## 2. Disciplina

1. **Soglie scritte prima:** il criterio viene dal verdetto; l'ora dichiarata (17:56:12) è coerente con la prima corsa (17:59:56) e con la copia dell'originale (17:56:12). Oltre gli orari dei file non è verificabile: il file delle previsioni è stato riscritto fino alle 18:15:29 e non c'è un registro esterno.
2. **Scelti dopo i dati:** ρ = 0,30, la struttura «rapporto col picco E pixel attesi», e (informati dalle tabelle di f10) h_rif e A_rif. Tutti tarati sui semi su disco, e dichiarati. La configurazione è congelata alle 18:04:37, prima dei semi nuovi: le cifre a 424 e 848 px non hanno subito ritocchi. **Ma i semi nuovi cambiano rumore e percorso, non la scena:** è una prova di ripetibilità, non di generalità.
3. **Casi esclusi:** la riga «tutti i casi (130)» esclude il livello «limite» (0 su 10) e il caso d (0 su 10, «non ricompare»): con loro è 128 su 150. Sono dichiarati altrove, non nell'etichetta. «100 su 108» sui semi di taratura esclude anche 2 passaggi «mai nascosto» (persona di 1,85 m dietro un pannello di 1,6 m): non dichiarato, innocuo.
4. **Margine:** il criterio è passato con celle a 29, 29, 30, 30, 29, 29 e con b = 27 su 30 sulla taratura. Avevo scritto prima (18:25) che in replica una cella sarebbe caduta una volta su due: è caduta.

## 3. Attacchi (D435i, nominale, 424 px, caso a12, 10 semi k = 300…, salvo indicazione)

| Caso | Previsto | «tutte_p» | Esito |
|---|---|---|---|
| Pannello 2,1 m, persona 2,8 m | ≤ 2 | **0/10 [0–28]** | continuità **smentita**: «a meno della fascia dal bordo della portata» in 10 su 10 |
| Pannello 1,5 m, persona 2,0 m | ≥ 8 | 9/10 [60–98] | regge |
| 640×360 · D455 a 0,5 m/s · Gemini 335 a 0,5 m/s | ≥ 8 | 10/10 · 10/10 · 9/10 | regge |
| 1,6 m/s · 0,5 m/s | ≥ 8 | 10/10 · 10/10 | regge |
| Rumore «limite» · limite con buchi ×3,5 | ≤ 3 | 0/10 · 0/10 | **smentita**; 272 e 182 tracce confermate |
| Buchi ×3,5, rumore nominale | — | 10/10 [72–100] | regge: i buchi da soli non rompono |
| Persona 1,2 m · **bambino 1,0 m** | ≥ 8 · ≤ 6 | 9/10 · **2/10 [6–51]** | il bambino **smentisce** |
| Persona scura · nera | ≥ 8 · ≤ 6 | 10/10 · 7/10 [40–89] | regge · **non risolta** |
| Posa −0,5° · **+0,5°** | ≥ 8 | 10/10 · **6/10 [31–83]** | a +0,5° **smentita**; tracce sul pavimento vuoto in 2 sequenze su 30 |
| Bordo del campo, 0,2 m liberi | ≤ 2 | 9/10 | smentita **la mia** previsione |
| Bordo del campo, nessun margine | ≤ 2 | 0/10 stessa, **10/10 identità nuova** | regge; vuoto 0 fotogrammi su 499 |

**Ciò che la correzione ha rotto.**
- **Oggetti piccoli come oggetti:** il cubo di 10 cm a 2 m resta «occupato» nella mappa (60/60 fotogrammi) ma non è mai un gruppo: **0/60 [0–6]** contro 60/60 di f10. La scatola di 15 cm a 2,8 m: mappa 60/60, gruppo **45/60 [63–84]** contro 60/60. A 2,0 m regge (59/60).
- **Avviso perpetuo:** dopo il riaggancio l'avviso resta acceso in tutti i fotogrammi successivi. Tolto il pannello, è ancora acceso 30 fotogrammi (2 s) dopo in **10 su 10 [72–100]**: previsto «spento entro 5», smentito. Su k = 301 a quel punto non c'è più nessuna traccia e restano 117 celle d'avviso fra 2,3 e 3,0 m, 95 delle quali la mappa chiama «libero» (`diag.py rimozione 301`). Con il pannello presente, 286–331 celle d'avviso su 729–778 sono «libero» (la fascia di 0,4 m; due semi).
- **Non rotto:** bambino fermo in campo aperto, gruppo 200/200. Chi tocca il fianco del pannello non è un oggetto a sé né prima né dopo (adulto 0/200 contro 7/200; bambino 70/200 contro 33/200).

## 4. Estraneo e sicurezza

- **Estraneo con rumore** (A entra e si ferma nascosta; B, mai visto, esce dall'altra parte; 10 semi per risoluzione): identità di A data a B in 9/10 a 424 px e 10/10 a 848; evento marcato `identita: presunta`. A nascosta dopo l'uscita di B: fuori dall'avviso 0/264, cella «libero» 0. K-016 **confermata**; K-219 (`c1` di f8) **non verificato**.
- **«Libero» nell'ombra vera:** 5 celle·fotogramma su 3 992 186 in «tutte_p», le stesse 5 in «prima»: 4 con la scatola a 2 m al limite con buchi ×3,5, 1 con la scatola a 2,8 m **al nominale, 424 px**. È un difetto della catena di f10, non delle correzioni; resta aperto se sia la catena o il bordo della maschera di verità (K-014).
- **Riagganci a persona nascosta:** 2 in 180 passaggi (entrambi nel caso 2,1/2,8 m) contro 17 di f10; l'avviso non si è spento.

## 5. Chiusura

**Che cosa regge, e dove.** Simulazione, rumore nominale, un adulto solo (≥ 1,2 m, chiaro o scuro), 0,5–1,6 m/s, pannello fermo fra 1,5 e 1,8 m, persona 0,5 m dietro ed entro 2,6 m dalla camera, tre profili, 424–848 px, posa nota entro meno di 0,5°. Lì: stessa identità presunta in circa 97 passaggi su 100, pannello mai «in movimento», avviso mai spento su una persona nascosta entro i 3 m della griglia (autore 0 su 3921 e 0 su 3922, replica 0 su 3608 per risoluzione, attacchi 0 su 2360).

**Controesempi certificati** (ognuno: `$PY attacco.py <blocco> 8`, poi `python3 riassumi.py`; `$PY` = interprete di f10 con `-I -B`):
1. replica del criterio, b = 27/30 a 848 px — `F12_CONFIG=tutte_p F12_ETICHETTA=_replica $PY prova_autore.py ultimi848 8`;
2. persona a 2,8 m, 0/10 — blocco `geometria`; 3. bambino, 2/10 — `persona`; 4. posa +0,5°, 6/10 — `rumore`;
5. cubo di 10 cm senza gruppo, 0/60, e avviso acceso dopo la rimozione, 10/10 — `rotto`;
6. identità nuova sul bordo del campo, 10/10 — `bordo2`; 7. estraneo, 19/20 — `estraneo`.

**Correzioni obbligate alle regole proposte.**
1. *Soglie, riga 8:* dichiarare la taglia minima inseguibile (15 cm entro 2 m); sotto, l'oggetto è solo «occupato».
2. *Riaggancio, riga 3:* scrivere nel dominio «entro portata − fascia = 2,6 m»; oltre, l'identità non si riprende mai.
3. *Riaggancio, riga 4:* chi ricompare sul bordo del campo prende sempre un'identità nuova: dichiararlo.
4. *Riaggancio, righe 9–10:* dietro un pannello fermo lo strato non finisce mai, quindi l'identità non diventa mai «confermata»: o un'altra condizione di conferma, o si dichiara che resta presunta per sempre.
5. *Riga 9:* serve una regola di rilascio che funzioni fra 2,3 e 3,0 m, e l'interfaccia deve distinguere l'avviso residuo dall'avviso fresco.
6. *Prova d'ingresso, riga 10 delle soglie:* aggiungere il controllo della posa (a +0,5° compaiono tracce sul pavimento vuoto).
7. *Criterio:* sostituire «≥ 28 su 30» con un tasso e il suo intervallo su almeno 90 passaggi per cella.

**avversario-1 — avviso con età.** *Meccanismo:* ogni cella d'avviso porta il tempo dall'ultimo ingresso; oltre una durata T senza nuovi ingressi passa a «in ombra, non osservato da T». *Previsione:* avviso residuo dopo la rimozione 0 su 10 a T + 0,5 s; persona nascosta fuori dall'avviso fresco > 0 nel caso b se T < 3 s. *La smentisce:* una persona ferma nascosta più di T che esce senza avviso.

**La frase più forte che resta vera, per la giuria.** «In simulazione, con profondità ricostruita dalle schede tecniche a rumore nominale, un adulto che passa da solo dietro un pannello fermo, a mezzo metro dal pannello ed entro 2,6 m dalla camera, ritrova la stessa identità — che il sistema dichiara *presunta* — in 176 passaggi su 180 a 424 px (IC 95 %: 94–99 %) e in 174 su 180 a 848 px; in nessuno dei fotogrammi con la persona nascosta entro i 3 m della griglia l'avviso di possibile presenza si è spento. Non vale per un bambino, per due persone nella stessa ombra (l'identità passa alla persona sbagliata 19 volte su 20), oltre 2,6 m, con rumore al limite, né su un sensore vero, mai provato.»

**Dopo.** Provare tracciamento-3 dell'autore sugli stessi blocchi miei; decidere il rilascio dell'avviso; con il sensore, prima il pavimento vuoto e la posa.

File: `PREVISIONI.md`, `DIFFERENZE.md`, `rifai.sh` (circa 12 minuti), `attacco.py`, `riassumi.py`, `riconta.py`, `diag.py`, `prova_autore.py`, `catena/`, `risultati/` (`RICONTO.md`, `ATTACCHI.md`, `att_*.jsonl`, `*_rifatto.jsonl`, `*_replica.jsonl`, registri).
