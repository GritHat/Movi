# Verifica avversaria dell'allegato tecnico: sovraffermazioni e riferimenti interni (`sciame-avversario`, f13)

Lavoro del 14 novembre 2026, dalle 19:26:20 alle 19:36 (`date -Is`). Oggetto: `../20-unione/allegato_tecnico.tex`, `../20-unione/capitoli/*.tex` e il PDF (69 pagine). Niente è stato modificato. **Tutto ciò che l'allegato riporta è dimostrazione, conto o simulazione: nessuna mia verifica lo rende «validato».**

## Esito in tre righe

- **Voci controllate: 64.** Sovraffermazioni 44 (i 7 risultati negativi obbligati; le frasi sul classificatore in 8 luoghi; 25 frasi «da non dire» dei giudizi; 4 luoghi di sintesi: sommario, contributi e riquadro dei limiti del cap. 1, elenco dei limiti del cap. 8, conclusioni). Riferimenti interni 20 (19 classi di schemi del mio programma su sorgente, bibliografia composta e testo del PDF; la lettura a occhio).
- **Tornano: 49** (6 negativi su 7; 7 luoghi su 8; 19 frasi su 25; 0 luoghi di sintesi su 4; 17 voci interne su 20). Il testo è quasi ovunque condizionato al suo dominio; le parole e le sigle vietate dal contratto (A-4) sono **0** nel sorgente e nel PDF.
- **Non tornano: 15**, che diventano le 19 correzioni qui sotto (una voce può darne più d'una): 4 frasi non sostenute dalle fonti, 10 imprecise o più tenui dei giudizi, 5 di forma (tracce del modo di lavorare in parafrasi, segnaposto, lunghezza).

**Cambi di stato proposti.** (1) «Pannello fermo mai dato per mobile» (cap. 4): da *sostenuto* a **sostenuto solo nel dominio; fuori, controesempio 7 su 10** (correzione 2). (2) Conclusioni, primo punto del «dimostrato»: **non è ciò che la proposizione dimostra** (correzione 1).

**Regole violate e scostamenti miei.** (a) Errore mio, corretto: al primo `ls`, troncato da `head`, ho creduto che `VERDETTO_INTEGRAZIONE.md` non esistesse; esiste, e ne ho letto testa, §3 e §7 (non i §1–2, 4–6, 8–9). (b) Le previsioni (`PREVISIONI.md`, 19:26) sono scritte dopo il contratto e prima dei capitoli. (c) L'ambiente sconsiglia i file di rapporto: la consegna chiede questo file, ho seguito la consegna. (d) Non ho consegnato un `CIFRE.md` separato: non scrivo cifre nuove; ogni cifra dei testi corretti porta qui accanto il file d'origine. Niente git, sudo, rete; scritture solo in questa cartella.

**Indipendenza.** Il mio programma (`cerca_interni.py`) non condivide codice con `controlla_interni.py` di chi ha unito, che non ho aperto. Condivido con gli autori il contratto, i file d'origine e il modello linguistico: un errore già presente nei file d'origine non lo vedo.

**Esito delle previsioni** (scritte prima). P1, almeno 3 tracce interne: **smentita in senso stretto** (0 parole dell'elenco A-4), regge solo per le parafrasi (correzioni 15–17). P2, almeno 5 verbi di garanzia da correggere: **non raggiunta** (4: correzioni 1, 3, 12, 10b), sopra la soglia di smentita (2). P3, almeno un negativo mancante: **regge** (correzione 2). P4, frase sul classificatore attenuata: **regge** (sommario, correzione 10). P5, una frase che fa pensare a dati reali: **regge** («percorsi registrati», correzione 4).

Sigle delle fonti: **VI** `f12-integrazione/30-arbitro/VERDETTO_INTEGRAZIONE.md`; **CI** `f12-integrazione/07-controprova-identita/CONTROPROVA_IDENTITA.md`; **VD** `f10-dati/23-verdetto/VERDETTO_DATI.md`; **V8** `f8-continuita/16-verdetto/VERDETTO_CONTINUITA.md`; **VN** `f4/H-012/09-arbitro/VERDETTO.md`; **V7** `f7-estensione/16-verdetto/VERDETTO_ESTENSIONE.md`; **BL** `f14-classificazione/20-inclusione/BLOCCO_CLASSIFICAZIONE.md`; **V3** `f12-integrazione/20-finale/SOLUZIONE_V3.md`. Gli intervalli sono ricontati in `conti_uscita.txt`.

---

## A. Falso o non sostenuto

**1. Conclusioni, «Che cosa è dimostrato», primo punto (`09_conclusioni.tex`, riga 7).**
*Frase:* «una cella dichiarata «libero» è priva di superfici fino al suolo, se la profondità valida è corretta, la posa è nota entro la tolleranza e il suolo è piano».
*Che cosa non torna.* La Proposizione sulla sicurezza del «libero» (`03_mappa.tex`, righe 84–91) dimostra meno, in due punti: (i) la parte (b) vale con **posa esatta** («con ε_p = 0»), non «entro la tolleranza»; (ii) riguarda **i raggi dei pixel che leggono il suolo della cella**, non la cella: l'Osservazione che segue (riga 96) dice che «la sicurezza della cella intera è verificata in simulazione, non dimostrata» e che un oggetto sospeso lascia la cella «libero». La tabella di sintesi del cap. 1 (riga 89) dice correttamente «posa esatta». La stessa conclusione poi cita come controesempio «l'errore d'inclinazione di 1°», che starebbe *fuori* da una tolleranza mai quantificata.
*Testo corretto:*
> Nessuna cella non osservata è dichiarata «libero» (per costruzione). Se una cella è dichiarata «libero», nessuna superficie interseca i raggi dei pixel che ne leggono il suolo, all'istante d'acquisizione, purché la profondità valida sia corretta, la posa sia esatta e il suolo sia piano (Proposizione~\ref{prop:map-sicurezza}). L'enunciato non copre la cella intera né la colonna sopra di essa: per la cella vale la verifica in simulazione del \S\ref{sec:map}, entro $0{,}5^\circ$ d'errore d'inclinazione. Fuori da queste ipotesi cade: i controesempi sono il vetro, l'ostacolo che non rimanda segnale e l'errore d'inclinazione di $1^\circ$ (\S\ref{sec:map-controesempi}).

**2. Cap. 4, regola dei gruppi a celle forti (`04_stima.tex`, riga 71), e conclusioni.**
*Frase:* «pannello «mobile» in 0 passaggi su 140».
*Che cosa non torna.* È data senza dominio, e il risultato contrario fuori dominio è omesso: VI, cambio di stato 10: «Fuori dominio […] il pannello è «in movimento» in 7 passaggi su 10 alle due risoluzioni: «mai in movimento» vale solo nel dominio»; VI §7 lo mette fra le frasi da non dire. Riscontro mio: `30-arbitro/riconteggio2.txt`, righe 7 e 9 («pannello mobile 7» su 120 passaggi della replica, a 424 e a 848 pixel) e `30-arbitro/riconteggio3.txt`, righe 10 e 14 (tipo «a12z»: 7/10). Il tipo «a12z» è il soggetto a 1,2 m/s sulla linea a 2,1 m dalla camera (`07-controprova-identita/prova_autore.py`, righe 69 e 204). Nell'allegato «7 su 10» per il pannello ha 0 occorrenze (`contesto.py`). Nelle conclusioni i falsi «in movimento» non compaiono affatto (79 su 90 sta solo nei cap. 1, 6 e 8).
*Testo corretto (cap. 4, al posto di «pannello «mobile» in 0 passaggi su 140 (130 e 94 con i gruppi della Definizione…)»):*
> pannello «mobile» in 0 passaggi su 140 nel dominio dell'identità al ritorno (130 e 94 con i gruppi della Definizione~\ref{def:sti-gruppo}); fuori da quel dominio, con il soggetto sulla linea a $2{,}1\unita{m}$ dalla camera, in 7 passaggi su 10 a entrambe le risoluzioni (40--89\,\%): lo zero vale solo nel dominio
*Da aggiungere alle conclusioni, in «Dove le simulazioni mostrano che il sistema cede»:*
> Su profondità simulata dalle schede tecniche un pannello fermo è dichiarato «in movimento» in 79 passaggi su 90 con i gruppi per componenti connesse; con i gruppi a celle forti in 0 su 140 nel dominio dell'identità al ritorno e in 7 su 10 fuori da esso (soggetto sulla linea a $2{,}1\unita{m}$).
*Non verificato:* che la «linea a 2,1 m» coincida con il caso «a 0,3 m dal pannello» già scritto nei cap. 4, 6 e 8 (è una mia deduzione dalla posizione del pannello): se coincide, basta aggiungere la cifra a quella riga.

**3. Cap. 1, contributi, punto 4 (`01_introduzione.tex`, riga 71).**
*Frase:* «regione di previsione a livello dichiarato che non si svuota mai».
*Che cosa non torna.* «Mai» senza dominio. La proposizione dice «non si svuota finché la traccia è nell'ombra»; la premessa manca in 24 passaggi su 23 402 (928 senza la regola che la cura); su profondità simulata la regola non è mai stata eseguita (solo 44 e 43 passaggi su 140 hanno una previsione in ogni fotogramma nascosto: VI, cambio 9; `08_limiti.tex`, limite 9); il livello è dichiarato solo in un dominio. V8 §7 vieta «continuità garantita» senza il limite dell'ingresso.
*Testo corretto:*
> Il trattamento dell'occlusione: insieme di possibile presenza con contenimento e monotonia, fascia di guardia, regione di previsione che, per costruzione, non si svuota finché la traccia è nell'ombra (se l'ingresso nell'ombra è stato riconosciuto), con un livello dichiarato solo nel dominio in cui è stato misurato in simulazione, e l'enunciato che previsione ed etichetta non riducono l'avviso (\S\ref{sec:occ}).

**4. «400 percorsi registrati» (`05_occlusione.tex` riga 115; `06_valutazione.tex` righe 109 e 170).**
*Che cosa non torna.* Un commissario legge «registrati» come camminate vere registrate. Nel progetto non esistono: V8 §2.1 colloca la libreria fra i prodotti di un generatore («in nessuna prova la libreria viene da un generatore e i passaggi da un altro»), e l'allegato stesso dice che nessuna prova usa un sensore. La parola viene dalle fonti (`04-statistica/FASCICOLO_VALUTAZIONE.md` righe 114 e 164; V3 riga 144), che però sono lette da chi conosce il contesto.
*Testo corretto (tre luoghi):* «una libreria di 400 percorsi simulati, prodotti dallo stesso generatore di camminate usato per i passaggi di prova, trapiantati sul punto e sulla velocità d'ingresso»; nella riga 170: «(400 percorsi simulati)».
*Non verificato:* non ho aperto il codice del generatore; se la libreria avesse un'altra origine, la frase va scritta con quella.

## B. Impreciso, o più tenue dei giudizi

**5. Conclusioni, «Dove le simulazioni mostrano che il sistema cede»; cap. 8, limite 5.**
*Frasi:* «Chi svolta o esce dal lato lontano dell'ombra è nella regione in una quota di casi fra 0,57 e 0,86 a 2 e 3 s»; limite 5: «per chi parte da fermo […] 0,82–0,83».
*Che cosa non torna.* Sono i valori più favorevoli fra quelli che l'allegato stesso riporta. `05_occlusione.tex` riga 223 dà, per il lato lontano con soggetto puntiforme e altri semi, 0,32–0,67 a 2 s e 0,13–0,47 a 3 s (sono le cifre di V8 §2.1); per chi parte da fermo `06_valutazione.tex` riga 229 dà 15/141 = 0,11, 21/134 = 0,16, 14/54 = 0,26 (V8 §2.1) e `05_occlusione.tex` riga 225 dà 0,146 / 0,049 / 0,043 senza la soglia di velocità. Nessun file decide fra le due serie: vanno entrambe, con la condizione.
*Testo corretto (conclusioni):*
> Chi svolta o esce dal lato lontano dell'ombra è nella regione in una quota di casi fra $0{,}57$ e $0{,}86$ a 2 e $3\unita{s}$ nella prova d'insieme (corpo esteso); nelle prove di base, con soggetto puntiforme e altri semi, chi esce dal lato lontano scende a $0{,}32$--$0{,}67$ a $2\unita{s}$ e a $0{,}13$--$0{,}47$ a $3\unita{s}$. Chi parte da fermo accanto all'ostacolo è nella regione in $0{,}11$--$0{,}26$ dei casi fra 1 e $3\unita{s}$ nelle prove di base.
*Testo corretto (limite 5, al posto di «per chi parte da fermo accanto all'ostacolo, sugli istanti con il centro nascosto, 0,82–0,83»):*
> per chi parte da fermo accanto all'ostacolo, $0{,}11/0{,}16/0{,}26$ a 1, 2 e $3\unita{s}$ nelle prove di base ($N=141$, 134, 54) e $0{,}82$--$0{,}83$ nella prova d'insieme, sugli istanti con il centro nascosto

**6. Conclusioni e cap. 8, limite 4: il secondo soggetto nella stessa ombra.**
*Frase:* «riceve l'identità del primo (19 casi su 20)».
*Che cosa non torna.* È la cifra con meno casi. L'allegato ha anche 2400 su 2400 con modello ideale (`06_valutazione.tex` riga 251; V7 §5.6: «la scambia sempre») e 3027/3041, 3493/3616, 3239/3546 (`05_occlusione.tex` riga 234; VI, cambio 2).
*Testo corretto:*
> Un secondo soggetto mai visto che esce dalla stessa ombra riceve l'identità del primo: 2400 casi su 2400 nelle prove di base con modello ideale del sensore, fra $0{,}91$ e $0{,}995$ in una seconda prova con modello ideale (3 geometrie, oltre 3000 casi ciascuna), 19 su 20 (76--99\,\%) su profondità simulata dalle schede tecniche. Nessuna regola lo ripara: per questo l'identità è presunta e l'avviso non ne dipende.

**7. Conclusioni, «Su profondità simulata dalle schede tecniche»: manca il «libero» nell'ombra vera.**
*Che cosa non torna.* Il punto elenca solo gli zeri favorevoli. VI, cambio 8, e `01_introduzione.tex` riga 91 riportano 5 celle·fotogramma «libero» nell'ombra vera su 3 992 186 in una seconda serie, non risolte; VI §7 vieta «0 su 2,9 milioni» senza «sulle sequenze di partenza». È il risultato più vicino al principio di sicurezza e non sta nelle conclusioni.
*Testo da aggiungere:*
> Una cella «libero» dentro l'ombra vera di un ostacolo: 0 su $2\,907\,032$ celle\,$\cdot$\,fotogramma in una prima serie di 131 sequenze, 5 su $3\,992\,186$ in una seconda di 381 (una al livello di rumore nominale); entrambe con la variante che conserva il «libero» per tre fotogrammi, non con la regola della cella adottata. Non è risolto se le 5 dipendano dalla regola o dal bordo della maschera di riferimento.

**8. Termine dell'avviso dopo la rimozione dell'ostacolo: tre diciture per lo stesso fatto.**
*Frasi:* cap. 1 riga 98 e conclusioni: «non è verificato (acceso dopo 2 s in 10 prove su 10)»; tabella degli invarianti, riga 7: «il rilascio a ostacolo rimosso non funziona (10 prove su 10)».
*Che cosa non torna.* La prova aveva una previsione scritta («spento entro 5 fotogrammi») ed è finita 10 su 10 dalla parte opposta (CI, riga 44: «smentito»); VI, cambio 10, aggiunge che il difetto c'è anche nella configurazione di riferimento. «Non verificato» è lo stato di ciò che non è stato provato; qui è stato provato ed è andato male.
*Testo corretto (uguale nei tre luoghi):*
> che l'avviso termini quando il suolo è rivisto dopo la rimozione dell'ostacolo non è sostenuto: nella realizzazione provata resta acceso dopo $2\unita{s}$ in 10 prove su 10 (72--100\,\%), per una causa non determinata

**9. Traiettorie pubbliche di pedoni: conclusioni e `06_valutazione.tex` righe 296–303.**
*Che cosa non torna.* Le conclusioni dicono «(219 tratti di 9 persone, senza profondità)» e tacciono le due riserve che il cap. 6 scrive. Il cap. 6 a sua volta omette le cifre con cui VD §5 vieta di leggere «0,2 m a 1 s» come prestazione: «0,32–0,52 m con misure peggiori; circa 1 m a 2 s per chi si ferma, N = 12».
*Testo corretto (conclusioni):*
> copre il soggetto in $0{,}977$, $1{,}000$ e $1{,}000$ dei casi a 1, 2 e $3\unita{s}$ (219 tratti di 9 persone; numerosità efficace fra 9 e 219; posizioni note al millimetro fino all'ultimo istante, senza profondità): riguarda il modello di moto, non la catena.
*Da aggiungere al cap. 6, dopo «non conferma il livello 0,90 della regione adottata»:*
> L'errore mediano di $0{,}2\unita{m}$ a $1\unita{s}$ non è una prestazione del prototipo: con misure peggiori è $0{,}32$--$0{,}52\unita{m}$, e per chi si ferma è circa $1\unita{m}$ a $2\unita{s}$ ($N=12$).
*Non verificato:* le due cifre le ho lette in VD §5, non nel file dei risultati.

**10. Sommario (`00_sommario.tex`).**
(a) «Il classificatore degli oggetti è un componente richiesto, qui simulato e non valutato»: manca «non realizzato» e manca «a mano»; BL riga 191 vieta proprio «classificatore simulato» senza «a mano». (b) «i risultati valgono a camera ferma, al chiuso, fino a 3 m»: «valgono» si legge come validità; sono ottenuti in quelle condizioni. (c) Le cifre del modello ideale sono date senza dire che su profondità simulata la regola non è stata eseguita e che con l'ostacolo da 1 m la soglia non è raggiunta.
*Testo corretto (ultime tre frasi del sommario):*
> In simulazione, con modello ideale del sensore, un ostacolo fermo largo $2\unita{m}$, il bordo dell'ombra noto e un soggetto alla volta sul proprio percorso, la regione di previsione è emessa a ogni ciclo dell'occlusione (0 interruzioni su $23\,402$ passaggi, se l'ingresso nell'ombra è riconosciuto: manca in 24) e contiene il soggetto in almeno 9 casi su 10 fino a $2\unita{s}$ e in almeno 85 su 100 fino a $3\unita{s}$; con un ostacolo largo $1\unita{m}$ la soglia di 9 su 10 non è raggiunta, e su profondità simulata dalle schede tecniche questa regola non è stata eseguita. Il classificatore degli oggetti è un componente richiesto dal sistema: in questo lavoro non è realizzato né valutato, ed è simulato con etichette assegnate a mano. Nessuna prova è stata eseguita su un sensore fisico: tutti i risultati sono ottenuti a camera ferma, al chiuso, fino a $3\unita{m}$, e non sono stati verificati fuori da queste condizioni.

**11. Cap. 1, riquadro «Limiti di validità», voce «Dominio» (riga 132).**
*Frase:* «Il livello della regione vale con il bordo dell'ombra noto e per chi resta sul proprio percorso».
*Che cosa non torna.* Mancano due condizioni senza le quali la cifra è smentita o non esiste: ostacolo largo 2 m (con 1 m: 942 su 1045, limite 0,882; VI, cambio 1) e modello ideale del sensore (VI, cambio 9).
*Testo corretto:* «Il livello della regione è misurato solo in simulazione con modello ideale del sensore, e vale con un ostacolo largo $2\unita{m}$, il bordo dell'ombra noto e per chi resta sul proprio percorso; con un ostacolo largo $1\unita{m}$ è «almeno 87 su 100» fino a $1\unita{s}$; non è dichiarata alcuna cifra oltre $3\unita{s}$.»

**12. Cap. 7, tabella delle alternative (`07_costo.tex`, riga 132).**
*Frase:* «Le garanzie sul «libero» e sull'avviso sono dimostrate su regole scritte».
*Che cosa non torna.* «Garanzie dimostrate» senza il modello: VN §4 vieta «R8 garantito»; V7 §6 vieta «mai dato per libero» senza condizioni.
*Testo corretto:* «Gli enunciati sul «libero» e sull'avviso sono dimostrati, nel modello dichiarato e sotto le sue ipotesi, su regole scritte».

**13. Conclusioni, latenza (riga 28).**
*Frase:* «La latenza di 155 ms è una somma di voci note.»
*Che cosa non torna.* Più netta del cap. 8, dove la stessa somma vale circa 131 ms con un secondo dato del costruttore e «nessuna decide», e dove il requisito sul 95° percentile non è soddisfatto; V3 riga 244: «Latenza: non risolta».
*Testo corretto:* «La latenza non è misurata: la somma delle voci note dà $155\unita{ms}$ in media, o circa $131\unita{ms}$ con un altro dato del costruttore per il tratto del sensore; le due fonti non concordano e nessuna voce è misurata sulla catena.»

**14. Cap. 1, principio di sicurezza (riga 41); cap. 8, limite 10 (riga 172).**
(a) «È lo stesso principio dei sistemi industriali di sorveglianza tridimensionale»: la fonte è classificata «fonte di parte» nella mappa delle citazioni (`06-bibliografia/FASCICOLO_BIBLIOGRAFIA.md`, riga 177), e «lo stesso» suggerisce un'equivalenza con sistemi certificati. *Testo:* «Il principio è analogo a quello dichiarato da un costruttore di sistemi industriali di sorveglianza tridimensionale, che trattano come occupato ciò che nessun sensore vede \cite{therobotreport-veo}, […]; l'analogia riguarda il principio, non il livello di integrità né la conformità a una norma.»
(b) Limite 10: «Con 3 m di portata e $T_r=1{,}0$ s l'avviso è tempestivo, per calcolo»: BL riga 191 vuole «ipotesi» accanto al tempo di reazione. *Testo:* «e un tempo di reazione ipotizzato $T_r=1{,}0\unita{s}$».

## C. Forma e tracce del modo di lavorare (A-4)

Il mio programma: 159 riscontri grezzi sugli schemi interni, 0 veri fra parole e sigle del contratto (106 «orari» sono coordinate dei disegni, decimali e numeri di proposizione; nel testo del PDF nessuna stringa `hh:mm`; le sigle trovate sono «RPLIDAR C1», $R_1$, $H_0$; «membri» è matematica). Metadati del PDF: nessun autore né titolo (`pdfinfo.txt`). Restano, a occhio:

**15. Didascalia della tabella dei profili (`04_stima.tex`, riga 84).** «$^{b}$ letto in un risultato di ricerca o riportato a memoria, non verificato» racconta come è stato raccolto il dato. *Testo:* «$^{b}$ valore non verificato su una fonte primaria».

**16. Cap. 7, «Rete neurale e classificazione» (`07_costo.tex`, riga 150).** «Sullo stato dell'arte dei rilevatori di oggetti si è fatta solo una ricognizione, senza eseguire alcun modello» è uno stato dei lavori. Inoltre «9 dei circa 25 tipi della tassonomia» non si concilia a prima vista con le «15 classi profilate» dei cap. 5, 8 e 9 (la cifra «9 su circa 25» è nella fonte: `03-classificatore/CLASSIFICATORE.md` riga 52). *Testo:* «Nessun rilevatore di oggetti è stato eseguito in questo lavoro. Dalla documentazione pubblica, i rilevatori pronti addestrati sull'insieme di immagini COCO coprono 9 dei circa 25 tipi di oggetto considerati per la tassonomia, di cui 15 hanno un profilo nella Tabella~\ref{tab:sti-profili} […]». *Non verificato:* il rapporto fra i 25 tipi e i 15 profili; lo confermi l'autore del capitolo.

**17. La storia delle versioni in parafrasi.** La stessa configurazione ha tre nomi che dicono «prima c'era altro»: «parametri di partenza» (`01` righe 112, 116; `09` riga 19), «catena di partenza» e «regola di partenza» (`06` righe 142, 145, 270), «parametri di base» (`08` limite 9; invariante 3), «regola di lettura precedente a quella adottata», «regola precedente», «serie successiva», «ripetizione successiva» (`01` riga 91; `03` righe 157, 164; `06` riga 143), «137 e 206 prima» (`04` riga 71). Vanno nominate per contenuto, con un nome solo (anche per A-6, notazione unica):
- «parametri di partenza / di base», «catena di partenza» → «configurazione di riferimento (gruppi per componenti connesse, Definizione~\ref{def:sti-gruppo}; riaggancio a soglia fissa)»;
- «regola di lettura precedente a quella adottata», «regola precedente», «regola di partenza» → «variante che conserva il «libero» per tre fotogrammi»;
- «serie successiva», «ripetizione successiva» → «una seconda serie di 381 sequenze»;
- «137 e 206 prima» → «137 e 206 con i gruppi per componenti connesse».
Restano ammessi, perché sono metodo: «un secondo programma indipendente», «altri semi», «una replica».

**18. Frontespizio.** Nel PDF si legge «Autori: [nome della squadra]» e il sorgente ha il commento «% Nome degli autori: da compilare.»: mettere i nomi e togliere il commento prima della consegna.

**19. Lunghezza (A-6), fuori dal mio controllo ma visibile a chiunque:** 69 pagine contro «una trentina più le appendici». Lo dichiara già chi ha unito (`../20-unione/NOTE.md`, §0); decide l'autore.

---

## Che cosa torna (per non rifarlo)

- **I 7 negativi obbligati:** secondo soggetto (cap. 5, 6, 8, 9), identità su profondità simulata con le cadute fuori dominio (0 su 90; 176 e 174 su 180; 0, 2, 6 su 10: cap. 4, 6, 8), vetro (654 e 600 punti su 800: cap. 3, 8), errore di posa (0,67° e 0,57°; 150, 145, 146 su 300: cap. 2, 3, 8), precisione fuori dominio (cap. 5, 6, 8, salvo la correzione 5), latenza non misurata (cap. 8, 9) ci sono tutti con la cifra. Solo i falsi «in movimento» sono incompleti (correzione 2).
- **Classificatore:** «richiesto; non realizzato né valutato; etichette a mano; nessuna classe diversa da persona nella catena completa; la sicurezza non dipende dall'etichetta» sta nei cap. 1, 4, 5, 6, 8, 9 (nel 7 con rimando al 4); la riserva «rispetto allo scenario dichiarato, non contro uno scenario dichiarato male» c'è (`05_occlusione.tex` riga 267). Manca solo nel sommario (correzione 10).
- **Frasi «da non dire» cercate e non trovate come affermazioni:** «validato»; «tarato» come esito; un livello 50 %; una cifra oltre 3 s; cifre in moto o indossato; «prevede dove sarà»; «via libera»; «bassa latenza» e «15 Hz» come prestazione (solo citazione della sfida e ciclo di progetto); «identità al 100 %»; «9 su 10» con l'ostacolo da 1 m; «criterio sull'identità superato»; «riconosce», «classifica», «gestisce» veicoli; «drone», «UAV»; «orientamento»; «conforme a» una norma; «360°»; massa e accelerazione stimate.
- **Sensore fisico:** ogni capitolo apre dicendo che nessuna cifra viene da un sensore; le 52 frasi con «sensore fisico», «reale», «sperimentalmente» sono negazioni, condizioni («sul sensore il livello non si dichiara finché…») o citazioni di letteratura; l'unica frase che fa pensare a dati reali è quella della correzione 4.
- **Conti:** `conti_uscita.txt` rifà 15 intervalli di Wilson e tre conti in forma chiusa (1,13 e 0,56 m/s; 155 e 131 ms; 1,44 m/s): coincidono con l'allegato.

## Che cosa non ho controllato

- Cap. 2 e 7 e appendice A non letti riga per riga: solo le frasi estratte dai miei schemi. Tabelle del cap. 6 non ricontate cella per cella.
- Le dimostrazioni (A-1) e le citazioni (A-3): fuori dalla mia parte. Ho guardato una sola voce della mappa delle citazioni.
- Le figure: non ho guardato le pagine in immagine; didascalie lette solo dove uno schema le ha estratte.
- `VERDETTO_INTEGRAZIONE.md` §1–2, 4–6, 8–9; gli elenchi «da non dire» di V3 §3 e di `SCHERMO_E_DEMO.md` §6 (letto solo quello di BL, riga 191); `ATTACCO_CLASSIFICAZIONE.md`, `PROFILI.md`, `USO_DELLA_CLASSE.md`, `PROVA_INSIEME.md`, `LIBERO_DELLA_CELLA.md`, `IDENTITA_SU_PROFONDITA.md` per intero: usati per ricerca testuale.
- `CIFRE.md`, `SCELTE.md` di chi ha unito: di `CIFRE.md` solo le righe cercate; `controlla_interni.py` non aperto, per indipendenza.
- La coincidenza fra «linea a 2,1 m» e «0,3 m dal pannello» (correzione 2), l'origine della libreria di percorsi (correzione 4), le cifre 0,32–0,52 m e N = 12 (correzione 9), il rapporto 25 tipi / 15 profili (correzione 16): marcati «non verificato» nel punto.
- `allegato.bib` non esaminato dal mio programma (solo la bibliografia composta, `.bbl`, e il testo del PDF).

## File accanto

`PREVISIONI.md` (prima dei capitoli); `cerca_interni.py` → `uscita_cerca.txt` (159 riscontri interni e 354 verbi di garanzia, grezzi); `contesto.py` (contesto di uno schema nei capitoli); `conti.py` → `conti_uscita.txt`; `allegato_testo.txt` (testo del PDF, `pdftotext -layout`); `pdfinfo.txt`. Si rifà con: `timeout 60 pdftotext -layout ../20-unione/allegato_tecnico.pdf allegato_testo.txt && timeout 120 python3 cerca_interni.py ../20-unione allegato_testo.txt > uscita_cerca.txt && python3 conti.py`.
