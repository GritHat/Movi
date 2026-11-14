# VERIFICA dell'allegato tecnico — lettura da commissario esterno (sciame-lettore, f13)

14 novembre 2026, 19:26–19:41 (`date -Is`). Percorsi relativi a `.sciame/20261114-1301-percezione-challenge/`.
Oggetto: `f13-allegato/20-unione/allegato_tecnico.pdf` (69 pagine) e i suoi capitoli. Niente è stato modificato.

## Esito in tre righe

- **Controllate:** 38 punti d'inciampo della lettura a freddo (`PRIMA_LETTURA.md`), 19 dei quali confrontati con le
  fonti; circa 230 cifre del PDF rifatte, 62 con `riconti.py` (uscita in `riconti_uscita.txt`), le altre a mano senza
  registro riga per riga (il «circa» è questo).
- **Tornano:** tutte le cifre rifatte tranne 4 (correzioni 9 e 21); geometria, intervalli di Wilson, potenze della
  tabella 22, percentili Beta, fascia, distanze d'avviso, latenza: senza scarti. Due miei punti cadono (i 23 402 e i
  44 000 passaggi sono lanci diversi: `02-prova-insieme/PROVA_INSIEME.md` r. 19 e r. 33).
- **Non tornano:** 34 correzioni: 9 su frasi false o non sostenute, 16 su imprecisioni, 9 di forma.

## In testa: regole violate, previsioni, indipendenza

- Il contratto andava letto per primo; l'ho letto dopo la lettura a freddo, per non sapere che cosa gli autori
  volevano dire. La scheda del ruolo lo chiede; lo dichiaro come scostamento dalla consegna.
- L'ambiente chiede di non scrivere rapporti `.md`; la consegna chiede questo file: ho seguito la consegna.
- «Niente git»: a lavoro finito ho eseguito un `git status --short` di sola lettura sulla cartella `20-unione/`, per
  controllare di non averla toccata. Non ha scritto niente, ma è un comando git: lo dichiaro.
- I conti a mano della prima lettura non hanno una previsione scritta prima (regola 3). Le cinque previsioni sono
  state scritte alle 19:32, prima di aprire le fonti: P1 (tabella 22 e Beta tornano) **regge**; P2 (tabella 14, «prova
  singola», non si rifà) **regge**; P3 (2 907 032 è su 135 sequenze) **regge**; P4 (l'avviso senza traccia è regola
  adottata, non condizionata) **smentita** (`20-finale/SOLUZIONE_V3.md` r. 129); P5 (NOTE e SCELTE conoscono già α,
  Π/W, i nomi dei gruppi) **smentita**: conoscono k, η, la focale, la lunghezza, «(opzionale)», le somme del limite 9.
- In `PRIMA_LETTURA.md` avevo dichiarato più pagine guardate in immagine di quelle guardate davvero: rettificato in
  fondo a quel file. Pagine del PDF guardate: 8, 11, 12, 14, 32, 41.
- *Indipendenza.* Con gli autori condivido il modello linguistico e, per i riconti, le formule dell'allegato; non il
  codice né i dati. I confronti con le fonti valgono per le infedeltà del testo, non per un errore già nelle fonti.

## Che cosa arriva al lettore (parafrasi e voti)

La parafrasi in dieci righe, le cinque domande e le altre risposte ai punti (1)–(8) della consegna sono in
`PRIMA_LETTURA.md`. Voti: chiarezza del problema 8; correttezza e rigore 7; onestà sui limiti 9; riproducibilità 5;
completezza 8. La cosa che un commissario non capisce è **quale sia il sistema dichiarato**: le cifre di testa vengono
da tre catene diverse (ideale d'insieme; da scheda «di partenza»; da scheda con le regole aggiunte) e la soluzione
descritta non è mai stata eseguita tutta insieme. Il documento lo dice, ma al limite 9 di §8.8, a pagina 56.
In quaranta minuti le 55 pagine di corpo non si leggono (criterio A-6, già dichiarato in `NOTE.md` §0): che cosa
toglierei è al punto 6 di `PRIMA_LETTURA.md`.

## CORREZIONI

Forma di ogni voce: dove · che cosa non torna · prova · testo corretto.

### A. Falso o non sostenuto

**1. «pavimento» sostituito con «suolo» anche dove voleva dire «soglia minima di ripiego».**
Dove: `capitoli/05_occlusione.tex` r. 118 «(\emph{suolo})», r. 125 «se scatta il suolo», r. 197 «Regione
persistente con suolo»; `capitoli/06_valutazione.tex` r. 103 «[Suolo per comportamento peggiore]».
Prova: gli originali hanno «pavimento» (`15-capitolo/capitolo.tex` r. 118, 125, 197; `16-capitolo/capitolo.tex` r.
103); `SCELTE.md` §1 dichiara 22 sostituzioni meccaniche; in `SOLUZIONE_V3.md` r. 148 «pavimento» è la regione di
ripiego. Alla lettura «se scatta il suolo» non ha senso.
Testo: r. 118 «(\emph{regione di ripiego})»; r. 125 «se scatta la regione di ripiego della
Definizione~\ref{...}»; r. 197 «Regione persistente con ripiego»; r. 103 «[Soglia del comportamento peggiore]».

**2. Conclusioni, primo punto: più forte della proposizione che cita.**
Dove: `capitoli/09_conclusioni.tex` r. 7; stessa cosa nel sommario («sono dimostrati la sicurezza del libero»).
Che cosa: «una cella dichiarata libero è priva di superfici fino al suolo, se … la posa è nota entro la tolleranza».
La Proposizione 3.6(b) vale «con ε_p = 0» e solo per «i raggi dei pixel che ne leggono il suolo»; l'Osservazione
3.7(ii) dice che la cella intera è verificata in simulazione, non dimostrata.
Testo: «Nessuna cella non osservata è dichiarata «libero» (per costruzione). Se la profondità valida è corretta, la
posa è esatta e il suolo è piano, i raggi dei pixel che leggono il suolo di una cella dichiarata «libero» sono privi
di superfici all'istante d'acquisizione (Proposizione 3.6). Per la cella intera, con inclinazione nota entro
$0{,}5^\circ$, l'enunciato è verificato in simulazione su 300 condizioni dichiarate, non dimostrato (§3.4). Fuori da
queste ipotesi cade: …». Sommario: «sono dimostrati che ciò che non è osservato non è mai «libero», il contenimento
…».

**3. §7.5: il sistema «mantiene Π(t)» per ciò che non è mai stato visto.**
Dove: `capitoli/07_costo.tex` r. 160, «per ciò che non è mai stato visto mantiene un insieme di possibile presenza
Π(t) costruito sull'ombra».
Prova: §5.2 («Π è il riferimento teorico; il sistema realizza l'area d'avviso W … che nasce solo quando una traccia
entra in un'ombra»), §5.4 («un'ombra in cui non è entrata alcuna traccia … non porta l'avviso»), `SOLUZIONE_V3.md`
r. 182.
Testo: «per l'ombra in cui è entrato un oggetto seguito mantiene un'area d'avviso $W(t)$, che realizza l'insieme di
possibile presenza $\Pi(t)$ del §5 con una velocità massima assunta $v_{\max}$; un'ombra in cui non è entrato alcun
oggetto seguito resta «in ombra», senza avviso».

**4. Capitolo 6: Π scritto al posto di W.**
Dove: `capitoli/06_valutazione.tex` r. 18 («area d'avviso $\Pres(t)$»), r. 137 («Soggetto nascosto fuori da
$\Pres$»), e dopo la tabella 27 («un soggetto nascosto esce da Π»).
Prova: tavola dei simboli (Π insieme di possibile presenza, W area d'avviso); §8.6 dice che lo zero è «una
conseguenza della costruzione finché l'errore dell'ombra non supera w più mezzo corpo», cioè si misura W.
Testo: «fuori dall'area d'avviso $W(t)$»; «Soggetto nascosto fuori da $W$»; «esce da $W$».

**5. α in tre sensi.**
Dove: `capitoli/00_simboli.tex` r. 34 e tabella 1 («livello dichiarato 1 − α = 0,90»); §6.1 («1 − α = 0,90»);
§6.4–6.5 (α è il complemento); §6.3 (α è il livello della prova, 0,05); §4.4, §5.5 («quota α = 0,9», R_0,9), §7.5,
appendice A («α … 0,90»): α è il livello.
Testo (la scelta che tocca meno righe: α è il livello, come in R_0,9): simboli «regione di previsione al livello
dichiarato $\alpha$ (qui $\alpha = 0{,}90$)»; tabella 1 e §6.1 «al livello dichiarato $\alpha = 0{,}90$»; §6.3
«in modo che il livello della prova sia al più 0,05»; §6.4–6.5 e Osservazione 6.7 sostituire «$1-\alpha$» con
«$\alpha$» e «$\lceil(1-\alpha)(n_c+1)\rceil$» con «$\lceil\alpha(n_c+1)\rceil$».

**6. I 2 907 032 celle·fotogramma sono su 135 sequenze, non 131.**
Dove: tabella 2 (riga «Libero nell'ombra vera») e tabella 23 (`06_valutazione.tex`, riga «Celle libero nell'ombra
vera, regola di partenza»). §3.6 dice 135.
Prova: `04-statistica/FASCICOLO_VALUTAZIONE.md` r. 143 («135 sequenze (4 con i filtri del costruttore accesi) … 131
sequenze senza filtri») e r. 304 («135 = 131 + 4»).
Testo: condizioni «135 sequenze, 131 con i filtri del costruttore spenti»; intervallo «per sequenza, sulle 131:
0–2,9 %».

**7. Continuità: lo zero è detto senza la sua premessa, e la premessa è data nella forma migliore.**
Dove: sommario («0 interruzioni su 23 402 passaggi»); tabella 2, riga «Continuità» («premessa mancata in 24 su
23 402»); §9 («manca in 24 passaggi»).
Prova: `PROVA_INSIEME.md` r. 20 («con c7 24 su 23 402; senza c7 928 (3,97 %)»); `SOLUZIONE_V3.md` r. 129 (quella
regola è accesa «solo se la prova d'ingresso del rumore è passata»); tabelle 23 e 38 dell'allegato danno 928 e 24.
Testo: sommario «…è emessa a ogni ciclo dell'occlusione, una volta riconosciuto l'ingresso nell'ombra (0
interruzioni su 23 402 passaggi; l'ingresso non è riconosciuto in 928 di essi, in 24 con una regola aggiuntiva)».
Tabella 2 e §9: «premessa mancata in 928 passaggi su 23 402 (3,97 %); in 24 (0,10 %) con l'avviso acceso anche per
le tracce chiuse entro 0,75 m da un'ombra, regola attivata solo dopo la prova d'ingresso sul suolo vuoto (§8.3)».

**8. Quali regole fanno parte del sistema (dubbio già in `NOTE.md` §3.5; la lettura lo conferma).**
Dove: §4.2 «Regola dei gruppi a celle forti», §4.9 condizioni (c)–(e), avviso senza traccia; appendice A le marca
«(opzionale)»; tabelle 3 e 28 danno 176 su 180 come risultato del sistema.
Prova: `SOLUZIONE_V3.md` r. 24 («restano spenti di norma e si accendono solo dopo le due prove d'ingresso»), r. 87,
r. 129, r. 200.
Testo, in §4.2 prima di «Regola dei gruppi a celle forti» e richiamato in §4.9: «Questa regola, le condizioni
(c)–(e) del riaggancio (§4.9) e l'avviso per le tracce chiuse vicino a un'ombra (§5.6) non fanno parte della
configurazione di base: si attivano all'avvio solo se le prove d'ingresso del §8.3 sono superate, e l'uscita dichiara
quali sono attive». Appendice A: «(opzionale)» → «(attivo solo dopo le prove d'ingresso)».

**9. Tabella 14, colonna «Prova singola»: 0,853 e 0,371 non si rifanno.**
Dove: `capitoli/04_stima.tex`, tabella della regola «mobile», righe «da 3 m, curva pessimista» e «severa».
Prova: con la Proposizione 4.4, T_w = 13∆ = 0,867 s, σ = 9 e 11,25 cm a 3 m: 0,815 e 0,389 (`riconti.py`; le stesse
v_0,5 e v_0,9 del testo, 0,424/0,533 e 0,530/0,666, tornano e implicano 0,81). Le cifre del PDF coincidono con
`03-stima/FASCICOLO_STIMA.md` r. 63–64, che non dà i parametri del conto. Stato: **non risolto**; lo decide il
programma che ha prodotto la colonna.
Testo, finché non è deciso (due cifre, ciascuna con la sua condizione): nella didascalia «Prova singola: valori del
calcolo d'origine; la Proposizione 4.4 con $T_w = 0{,}867$ s e $\sigma$ a 3 m dà 0,815 e 0,389, e lo scarto non è
spiegato».

### B. Impreciso

**10. Segno dell'errore d'inclinazione.** Dove: §2.5 (pericoloso «+1°»), Controesempio 3.9 e §6.6 («−1°»), §3.6
(«+1°»), §8.8 punto 7 (tutti e due). Dal testo deduco δθ = creduta − vera (§2.5) ed e = vera − creduta (§3.4, «la
camera è inclinata di 15° + e, la regola assume 15°»); non verificato sul codice. Testo, in §3.4 dopo quella frase:
«(con la convenzione del §2.5, $\delta_\theta = -e$: l'errore che fa scendere un ostacolo sotto la soglia è
$\delta_\theta > 0$, cioè $e < 0$)»; in §8.8 punto 7 scrivere i due casi con lo stesso simbolo.

**11. «tenuta» non è definita.** Dove: tabella 18, §8.7 punto 5, appendice A. Prova:
`01-dimostrazioni/FASCICOLO_DIMOSTRAZIONI.md` r. 134 («termine di tenuta Δ»). Testo, prima della tabella 18: «La
tenuta è il termine $\Delta$ della (17): il ciclo durante il quale un'uscita resta in uso».

**12. «cella» usata per «combinazione» prima di essere definita.** Dove: tabella 20 e «Lettura» di §5.6 («30 celle
su 30», «N < 400 per cella»); la definizione è in §6.1; tabella 2 e §9 dicono «combinazioni». Testo: in §5.6 e nel
capitolo 6 «combinazione» al posto di «cella» in questo senso (definizione di §6.1: «Una combinazione è una
terna…»).

**13. La stessa cosa con più nomi.** «gruppi a celle forti» (§4.2) = «gruppi dalle celle forti» (tabelle 28–29) =
«raggruppamento per picco» (tabella 38 riga 3, §8.8 punto 9, appendice A) = «gruppi e riaggancio modificati»
(tabella 3, §9): tenere il primo. «marca tagliato» (tabella 27) = «bordo di profondità riconosciuto» (tabella 20,
§8.8 punto 6): tenere il primo. «traccia pendente» (§4.9) = «traccia in previsione» (§5): tenere il secondo.
Finestra: $T_w$ (§4.2) e $W$ (§8.9, che è anche l'area d'avviso): tenere $T_w$. Larghezza della fascia: $g$ nella
figura 3 e nella sua didascalia, $w$ altrove: mettere $w$.

**14. Tracce della storia dei lavori (criterio A-4, «stato dei lavori»).** Dove: «parametri di partenza», «catena
di partenza», «regola di partenza», «parametri di base», «poi … modificati», «Prima e dopo» (tabella 19), «regola
di lettura precedente», «serie successive», «prove d'insieme più recenti», «poi scartata», «una variante
esaminata». Il controllo delle parole vietate non le vede. Testo: due nomi fissi, «configurazione di base» e
«configurazione con gruppi a celle forti»; tabella 19 «Continuità e precisione con il cerchio del filtro e con la
regione persistente»; «regola di lettura con memoria di tre fotogrammi» al posto di «precedente».

**15. «Nascosto fuori dall'avviso» su profondità simulata: quattro denominatori senza legame.** Dove: 0 su 4324 e
0 su 3608 (tabella 2, §9); 0 e 0 su 3921 e 3922 (tabella 23); 0 su 336, 169 e 2360 (tabella 38); 0 su 264 (§6.6).
Prova: `30-arbitro/VERDETTO_INTEGRAZIONE.md` r. 14 (riconteggio: 4324 a 424 pixel, 4325 a 848; replica 3608);
`06-identita/IDENTITA_SU_PROFONDITA.md` r. 53 («3921 · 3922 fot., senza d»); `SOLUZIONE_V3.md` r. 188 (336 e 169 due
persone; 2360 casi d'attacco; 264 estraneo). Sono la stessa prova contata con e senza una disposizione, più altre
tre prove. La differenza di 403 fotogrammi non l'ho ricontata: **non verificato**. Testo, tabella 23: «0 e 0 | 3921 e
3922 fotogrammi (4324 e 4325 nel riconteggio che comprende tutte le disposizioni, entro 3 m); replica 0 su 3608 per
risoluzione; altre prove: 0 su 336 e 169 (due persone), 0 su 2360, 0 su 264».

**16. Tabella 3, «Ostacoli fermi»: cifre che il capitolo 6 non ha; requisito senza esito.** Prova:
`FASCICOLO_VALUTAZIONE.md` r. 221; `SOLUZIONE_V3.md` r. 295 («5 su 5 … cassa 84 su 84, scatola 10 su 10 [prel.]; sul
vero non verificato»). Testo, riga da aggiungere alla tabella 29: «Ostacolo fermo entro 15 cm dalla posizione vera |
cassa alta 1 m a 1,68 m; scatola di 15 cm a 2,0 m | 84; 10 | 84; 10 fotogrammi (una sequenza ciascuno) | — | II [S]»;
in tabella 3 aggiungere «la soglia «5 prove su 5 fra 1,1 e 3 m» non è stata provata in questa forma» (da confermare
con gli autori: non verificato).

**17. §7.4: «9 dei circa 25 tipi della tassonomia del §4».** La tabella 15 ha 15 tipi e «carrozzina» non compare
nel §4. Prova: `f14-classificazione/03-classificatore/CLASSIFICATORE.md` r. 15 e r. 52 (la tassonomia di quel file è
più fine). Testo: «coprono 9 dei circa 25 tipi di una tassonomia più fine di quella della Tabella 15, che distingue
per esempio la persona su carrozzina (mancano carrello elevatore, tram, multirotore, carrozzina)».

**18. §6.6, dopo la tabella 28: sembra che il sistema rilasci l'avviso con l'identità.** Prova: §5.6 e
`PROVA_INSIEME.md` r. 7 (è la variante in cui il riaggancio chiude l'avviso); `SOLUZIONE_V3.md` r. 188 (regola
adottata: l'avviso resta). Testo: «…e, con il modello ideale, nella variante scartata in cui il riaggancio chiude
l'avviso, l'avviso viene rilasciato insieme all'identità (quote della tabella); con la regola adottata i rilasci
sono zero per costruzione, non contati».

**19. §9: «fra 0,57 e 0,86» è la serie migliore.** Prova: tabelle 2 e 27 (soggetto puntiforme: 0,13–0,70). Testo:
«…fra 0,57 e 0,86 a 2 e 3 s con il corpo esteso, e fra 0,13 e 0,70 nella serie con soggetto puntiforme».

**20. §9: «(Proposizione 4.7) [C]» copre anche l'accelerazione.** Testo: «(Proposizione 4.7 per la massa [D]; conto
del §4.5 per l'accelerazione [C])».

**21. §8.8 punto 9: le somme non chiudono.** 1568 + 2983 = 4551 contro 4552; 1584 + 2968 = 4552 contro 4553. Le
cifre coincidono con `VERDETTO_INTEGRAZIONE.md` r. 16 (dubbio già in `NOTE.md` §3.3). Non verificato sui dati.
Testo: aggiungere «(un fotogramma per risoluzione in un altro stato)» solo se il riconteggio lo conferma;
altrimenti togliere i totali e scrivere «in circa due fotogrammi nascosti su tre».

**22. Due definizioni di «occupato».** Definizione 3.1(i) senza, Definizione 4.2 con «ed è il primo ritorno lungo
il suo azimut» (`FASCICOLO_STIMA.md` r. 13). Testo, Definizione 4.2: «Una cella è «occupata osservata» secondo la
Definizione 3.1; ai gruppi concorrono le celle occupate che danno il primo ritorno lungo il loro azimut» (da
confermare: quale delle due vale nel codice non è verificato).

**23. Due regole di riaggancio (§4.9 e §5.5) e due R_α (Definizione 5.9 e §6.4).** Testo, in §5.5 «Riaggancio»:
«È la forma usata nelle prove d'insieme con modello ideale del sensore; le condizioni complete (a)–(f) sono nel
§4.9». In testa a §6.4: «Questo paragrafo analizza la costruzione per quantili, che non è quella adottata
(Definizione 5.9): dice che cosa una taratura può garantire e che cosa no».

**24. «400 percorsi registrati» fa pensare a registrazioni vere.** Prova: `PROVA_INSIEME.md` r. 13 (semi propri
della libreria) e r. 85 (libreria da un generatore diverso: non provato); §6.5 dell'allegato. Testo (§5.5, §6.4,
§6.6): «400 percorsi generati dallo stesso simulatore di camminate delle prove, con semi disgiunti». Appendice A,
«libreria di taratura dei percorsi: almeno 200 percorsi, due persone, tre andature»: dire che è il requisito per la
libreria da registrare sul posto, se è questo (non verificato).

**25. Passaggi saltati, da esplicitare (nessun testo proposto: servono gli autori).** (a) §4.2: perché le prove sono
«al più 13» e la finestra massima 13∆, se la Definizione 4.3 ammette k − j fino a 15. (b) Osservazione 3.7(iii):
0,33 m «per 1,4 m/s» con finestra d'uso 0,20 s (1,4 × 0,20 = 0,28). (c) Lemma 3.8: a quali due casi si riferiscono
114 e 162 su 200. (d) Tabella 18: da che cosa viene l'età di 0,133 s se il «libero» ha memoria zero; latenza 0,150 s
nella prima riga e 0,155 nelle altre (già in `SCELTE.md` §3.6). (e) §8.9: il conto di 0,375 m/s. (f) §5.5: nucleo
delle «3 lisciature» e «raggio da tabella». (g) Tabella 20 e tabella 27 danno cifre diverse per «bordo riconosciuto»
e «chi parte da fermo» senza dire che sono prove diverse.

### C. Forma

**26.** §8.1: «Con la geometria del capitolo 2 9 settori su 17» → «Con la geometria del capitolo 2, nove settori su
17».
**27.** §3.3: «(b) [D] nel modello delle tre ipotesi, [N].» → «(b) [D] nel modello delle tre ipotesi; [N] su un
sensore fisico.»
**28.** Proposizione 3.14, fine: «[C]; il secondo enunciato [S] (Tabella 13, quarta riga).» → «Il primo enunciato è
un calcolo [C]; il secondo è verificato in simulazione [S] (Tabella 13, quarta riga).»
**29.** §4.8 «Consistenza del filtro.» e §8.3 «Livello di prova.» sono titoli finiti in mezzo al capoverso: a capo.
**30.** §8.9: «[D] (§2)»: il rimando al §2 non porta a niente; «(§4.2)».
**31.** §5.6 lettura (6): «lo "0 su 11,9 milioni di istanti"» arriva prima della tabella 23 che lo introduce:
aggiungere «(tabella 23)».
**32.** Stile non uniforme fra capitoli: gradi «87°» nel capitolo 2 e «$58^\circ$» altrove; «figura 2», «tabella 5»
minuscoli nei capitoli 2, 6, 7, 8 e maiuscoli negli altri; tipi (I)(II)(III) nel capitolo 6 e «ideale», «da scheda»
nel capitolo 1; «misure mancanti» (capitolo 6) e «pixel non validi» (capitolo 3); «maschera di verità» e «maschera
di riferimento».
**33.** §8.8 punto 2: «1,71–1,73 m» e «1,69 m»; §2.2 dà 1,71 m (a 43,5°) e 1,70 m (a 44°, focale di 424 pixel):
allineare a §2.2.
**34.** Frontespizio: «Autori: [nome della squadra]» è un segnaposto. Figura 2(a): l'etichetta «1,62» tocca la
linea tratteggiata.

## Che cosa manca per rifare i conti (criterio A-5)

Dal solo allegato si rifanno i conti a mano e la statistica (fatto: tornano). Non si rifanno le simulazioni: mancano
la geometria di G1–G3, i parametri del generatore di camminate e dei sette comportamenti, le dieci scene della regola
del «libero», il modello del simulatore da scheda (pixel misti, pixel senza dato), quali registrazioni dell'insieme
pubblico, i semi e un rimando a programmi e dati. L'appendice B dovrebbe dirlo in una riga.

## Stati proposti

- «Le cifre dell'allegato coincidono con le fonti»: **sostenuto** sul campione confrontato (19 punti), con le
  eccezioni 6, 15, 16, 17; non è un controllo esaustivo.
- «I conti in forma chiusa e la statistica sono rifacibili dal testo»: **verificato** sull'insieme di `riconti.py`
  e dei conti a mano elencati in `PRIMA_LETTURA.md`, salvo la correzione 9 (**non risolto**).
- «Notazione unica» (A-6): **smentito** (correzioni 4, 5, 13).
- «Autosufficienza» (A-5): **non risolto** per le simulazioni.

## Proposta nuova

`lettore-1`: una tabella di mezza pagina in §1.5, «quale catena ha prodotto quale cifra» (ideale d'insieme; da
scheda, configurazione di base; da scheda, con gruppi a celle forti; dati pubblici), con le regole attive in
ciascuna. Meccanismo: toglie la domanda 1 del commissario. Previsione: un secondo lettore a freddo saprà dire in una
riga che cosa è stato eseguito insieme. Smentita: non lo sa dire neanche con la tabella.

## Che cosa non ho controllato

La bibliografia e le 78 citazioni contro la mappa del fascicolo 06; `CIFRE.md` riga per riga; i sorgenti `.tex` per
intero (solo le righe citate); le figure 1, 4, 5, 7, 8 in immagine; le dimostrazioni dei capitoli 5 e 6 passo per
passo (lette, non rifatte: in particolare le Proposizioni 5.10 e 5.15, che `NOTE.md` segnala); i dati grezzi dietro
ogni cifra; la tabella 39; i verdetti f4, f7, f8, f9, f10. Dopo: applicare A1–A9, poi una seconda lettura a freddo
di un lettore diverso sul solo capitolo 1 e sulle conclusioni.
