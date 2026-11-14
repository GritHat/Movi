Canarino: sciame-canarino-20c82ebff50dded3

# Consegna f8, corsia A — `sciame-visualizzatore` (designer dell'informazione)

## 0. Scostamenti e regole violate

- **Previsioni smentite:** PV-1e, tutte e due le metà (§2, critiche 3 e 7). Le altre otto reggono (`PREVISIONI.md`, scritto alle 15:16:11, prima di ogni script; esiti in coda).
- **Emulazione non fedele:** la mia copia della regola «metà del cuneo» dà un «previsto» di 0,67–0,87 s contro i 0,40–0,53 s misurati dalla validazione. Per giudicare il nucleo uso i numeri dei suoi file, non i miei.
- **Notati dopo, non previsti:** marcati **[dopo]**.
- **Letture parziali:** con `grep` soltanto `MISURE_V2.md`, `SPECIALIZZAZIONE.md`, `MOTO_PROPRIO.md`, `proposta_sciame.tex`; non letti `AUDIT.md`, `CONTROPROVE.md`, le consegne di f1, i PDF.
- **Fonti:** di otto, tre pagine aperte; delle altre ho letto solo il riassunto del motore di ricerca (segnate «riassunto»).
- **Indipendenza:** con il nucleo condivido la specifica (velocità costante, q = 0,2) e il modello linguistico; scena e codice sono miei. La resa in bianco e nero l'ho giudicata io, che l'ho disegnata.
- L'SVG lo scrive uno script (`fotogrammi.py`), non la mano: così posizioni e raggi sono quelli del modello. Il disegno è stato corretto una volta dopo la prima resa (resta `fotogrammi_v1_1bit.png`). Tutto è modello senza rumore, a sensore fermo: nessuna persona ha guardato lo schermo né ascoltato un suono.

## 1. Q3 — l'imperativo è rispettato? (per la parte visiva)

| Parte | Esito | Prova |
|---|---|---|
| Nucleo, regola di visualizzazione | **non rispettato** | `MISURE_V2.md`, P4: nel transito la regione è mostrata per 0,40–0,53 s su 1,07–1,13 s di buio, cioè nel 35–50 % dei cicli senza osservazione; nella sosta («perso» 4,6–4,8 s) in circa l'8–10 % [conto mio]. Dopo «perso» non c'è né punto né regione: l'oggetto sparisce e riappare 0,47–0,67 s dopo, a 0,5–0,8 m [conto mio, a 1,13 m/s] |
| Nucleo, osservato contro previsto | **in parte** | i tre stati non si mescolano mai (invariante 3), ma il blocco B8 dice «schermo a tre colori»: solo colore, e nessun livello dichiarato a chi guarda (il cerchio «al 95 %» copre 0,89–0,93; 0,56–0,66 per chi torna: `TORNEO.md`) |
| Criteri di accettazione | **non rispettato** | R3 misura solo l'identità al ritorno; «area prevista alla riemersione» è tolta dalla promessa (`VERDETTO.md` §3). Nessuna misura di vuoti, salto alla ricomparsa, taratura |
| Specializzazione | **non rispettato** | `SPECIALIZZAZIONE.md` §3.3: «la durata del previsto non ha un valore proposto… per le classi veloci si riduce a un istante» |
| Sensore in moto | **non verificato** | `MOTO_PROPRIO.md` non parla di ciò che si mostra |
| Demo e documento v0.5 | **in parte** | l'atto 4 e il punto 5 sono marcati «in revisione» (`proposta_sciame.tex`, righe 94 e 157): onesto come dichiarazione; manca il tabellone della taratura |

## 2. Critiche, ciascuna con la prova

1. **L'oggetto sparisce.** Vedi §1, prima riga. È il difetto che l'imperativo vieta.
2. **La media del filtro non è il punto da disegnare.** Nella scena «si ferma dietro» (18 casi, `risultati_punto_mostrato.txt`) la media cammina su suolo che il sensore vede libero nel 48,0 % dei cicli (geometria del torneo) e nel 26,5 % (demo); proiettata sull'ombra resta parcheggiata sul bordo visibile nel 69–80 % dei cicli, proprio dove la persona si vedrebbe. Il **baricentro della previsione troncata all'ombra** non tocca mai il libero, avanza al più di v·dt per ciclo, arretra al più di 1,1 cm; a 3 s sbaglia di 0,62 m contro 2,75 m (torneo) e 0,33 contro 3,14 m (demo).
3. **Il salto alla ricomparsa non si elimina scegliendo il punto.** Con il baricentro vale 0,18–0,61 m, sopra 0,3 m in 4 casi su 6 (mia previsione smentita); è sempre 0,31–0,34 volte il raggio al 95 %. Va quindi **mostrato come scarto**, non nascosto da un'animazione.
4. **Il punto non è una certezza [dopo].** Chi si ferma a un quarto dell'ombra è previsto meglio da «fermo all'ultima posizione» (0,50 m contro 0,87–1,10 m; demo 0,30 contro 0,49–0,57). La media dei casi lo nasconde.
5. **Dieci transiti dal vivo non provano la taratura** (`risultati_tabellone.txt`): 9 su 10 dà 55,5–99,7 %; una regione che copre l'80 % mostra almeno 9 su 10 nel 37,6 % delle demo. Per separare 90 % da 80 % con i due errori sotto il 10 % servono 86 transiti (soglia 74); da 70 %, 25 (soglia 21). «Tutti dentro» è un sospetto: con copertura vera 0,90, 30 su 30 capita nel 4,2 % dei casi.
6. **Un tratteggio sottile sparisce in stampa [dopo].** Nella prima resa a 1 bit le righe da 0,7 px svanivano e «possibile presenza» era uguale all'ombra vuota; a 1,5 px si legge (`fotogrammi_1bit.png`).
7. **La soglia «metà del cuneo» non cresce sempre con l'incertezza [dopo, solo nel mio modello].** A 1,5 m/s il cerchio esce dal cuneo prima di coprirne metà e la soglia non scatta mai. L'area della regione al 90 % della previsione troncata cresce invece sempre: 4 % del cuneo a 0,2 s, 39 % a 0,8 s, 52 % a 1,53 s, 84 % a 4 s (`risultati_fotogrammi.txt`).

## 3. Il progetto

**(1) Che cosa vede l'occhio.** Un solo segno di taglia fissa per oggetto, che non cambia mai posto di colpo: disco pieno (osservato) → anello vuoto (previsto) → disco pieno. Il cambio avviene sul bordo dell'ombra, senza dissolvenza né rimpicciolimento. La scia è piena dove fu misurata, tratteggiata dove fu prevista, e **resta tratteggiata** anche dopo. Attorno all'anello la regione «respira»: cresce, è tagliata dal bordo dell'ombra e dall'ostacolo (mai disegnata su suolo visto libero), sparisce alla ricomparsa lasciando per mezzo secondo il segmento di scarto. Accanto, l'età: «non visto da 0,8 s». Sotto tutto resta il cuneo di «possibile presenza». Osservato e previsto si distinguono per **forma e tratto**: nel file ci sono solo nero, bianco e tre tratteggi (`grep` sui colori di `fotogrammi.svg`).

**(2) La precisione.** Livello dichiarato in parole: «9 volte su 10 è qui dentro» (righe fitte: 1 su 2). Più scuro = più probabile. Soglia: la stessa del nucleo (metà dell'ombra), ma **cambia il segno e non lo spegne**: bordo a punti grossi, croce al posto dell'anello, dicitura «previsione larga». Nel mio modello della demo scatta a 1,47 s. Errori evitati: regione letta come taglia (taglia fissa, e la legenda lo dice); punto letto come certezza (anello vuoto, croce oltre soglia); animazione che finge l'osservato (nessuna interpolazione sul disco pieno, che sta solo dove c'è una misura del ciclo).

**Che cosa dice la ricerca.**
- Il cono d'incertezza è letto come estensione dell'oggetto; l'errore ha un nome, «deterministic construal error»: Joslyn e Savelli 2021, aperta, https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2020.590232/full. Anche Padilla e altri 2017, riassunto, https://pmc.ncbi.nlm.nih.gov/articles/PMC5626802.
- Sfocatura, posizione e valore di grigio sono i segni più intuitivi per l'incerto: MacEachren e altri 2012, riassunto, https://ieeevis.org/year/2012/paper/infovis/visual-semiotics-uncertainty-visualization-empirical-study.
- Il tratteggio è preferito a sfocatura e grigio: Boukhelifa e altri 2012, riassunto, https://tobias.isenberg.cc/p/Boukhelifa2012ESV.
- Un oggetto resta «lo stesso» dietro un ostacolo solo se scompare e ricompare lungo un bordo fisso, non se implode o svanisce: Scholl e Pylyshyn 1999, riassunto, https://ruccs.rutgers.edu/images/tech_rpt/tr-40/scholl.pdf.
- Esiti possibili animati battono le barre d'errore nei confronti: Hullman e altri 2015, aperta, https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0142444. Li terrei per il racconto, non per lo schermo di sicurezza.
- Suono: l'accoppiata altezza–luminosità piace ma «non è adatta» all'incertezza: Vriend e altri 2025, aperta solo la sintesi, https://arxiv.org/abs/2505.14379. Volume e nitidezza sarebbero i più intuitivi: riassunto, **non verificato**. Su un non vedente che segue un oggetto previsto non ho trovato studi.

**(3) Fotogrammi e legenda.** `fotogrammi.svg` (resa: `fotogrammi.png`; a 1 bit: `fotogrammi_1bit.png`). Scena A, passa dietro: A1 osservato; A2 e A3 previsto a 0,3 e 0,8 s, con la regione tagliata dal bordo; A4 ricompare a 1,1 s con scarto 0,28 m dentro il 90 %; A5 osservato. Scena B, si ferma: B1 previsto; B2 e B3 «regione larga» a 1,5 e 3,0 s; B4 ricompare a 4,1 s con scarto 0,47 m. Sono disegni di progetto dal mio modello, non misure.

**(4) Il tabellone.** Le lettere sono segnaposto; gli intervalli sono conti veri.

```
TARATURA — la persona è ricomparsa dentro la zona dichiarata?
                    DAL VIVO (oggi)        REGISTRAZIONI          larghezza
zona «9 su 10»      k su n  [da–a %]       k su n  [da–a %]       mediana, m
zona «1 su 2»       k su n  [da–a %]       k su n  [da–a %]       mediana, m
 per comportamento: prosegue | si ferma | torna indietro | svolta   (una riga l'uno)
 per tempo non visto: < 1 s | 1–3 s | > 3 s
previsione larga    k su n   (contata a parte: non fa punteggio)
ultimo transito: DENTRO · scarto 0,28 m · zona larga 0,78 m · non visto 1,1 s
esempio: 9 su 10 -> [55–100 %]: «compatibile con 9 su 10; troppo pochi per escludere 8 su 10»
```

Regole: mai la parola «tarato» dal solo conto dal vivo; l'intervallo esatto sempre accanto al conto; la larghezza sempre accanto alla copertura; la riga «1 su 2» è la prova rapida contro le zone enormi (10 su 10 dentro capita nello 0,1 % dei casi se la zona è giusta [conto mio: 0,5¹⁰]); la colonna delle registrazioni porta gli 86 transiti che i dieci dal vivo non possono dare.

**(5) Che cosa resta uguale.** Su stazione fissa, piattaforma in moto e ausilio sonoro restano: i tre segni più quello oltre soglia; la taglia fissa; la zona in metri sul suolo a livello dichiarato; l'età; lo scarto alla ricomparsa e il suo conto; il divieto di disegnare sul visto libero; la possibile presenza sotto. Cambiano, come parametri: la soglia in metri per classe; il riferimento del disegno (in moto la mappa va ancorata al terreno, altrimenti i segni scorrono per il moto del sensore: **non verificato**).
**Suono, proposta non verificata:** un battito che non si ferma mai finché la traccia è aperta. Nitido e nella direzione dell'oggetto se osservato; soffiato, nella direzione del punto previsto e tanto più lungo quanto più larga è la zona, se previsto; lento e senza direzione, su tutto il settore, oltre soglia; un segnale di chiusura alla ricomparsa. L'incertezza va sulla nitidezza e non sul volume: un avviso non deve farsi più debole quando si sa di meno. Restano i segnali brevi della correzione C11.

## 4. Stati proposti

- «Il nucleo mostra una stima in ogni ciclo senza osservazione»: **smentito** (35–50 % nel transito, file della validazione).
- «La media del filtro è un buon punto da mostrare»: **smentito** nel mio modello (48,0 % e 26,5 % dei cicli sul libero).
- «Il baricentro troncato scorre senza salti e resta in ombra»: **sostenuto dal modello** (18 casi senza rumore); non verificato con rumore, rilevamenti mancati, chi torna indietro.
- «Dieci transiti dal vivo provano la taratura»: **smentito** dal conto binomiale (transiti indipendenti).
- «Nessuna distinzione dipende dal colore»: **verificato** sul file. «Si legge in bianco e nero»: controllato solo dall'autore. Daltonici, giurati, non vedenti: **non verificato**.
- Efficacia e taratura del predittore: non le ho toccate, **non risolte** da questa corsia.

## 5. Proposte per Q4

**visualizzatore-1 — «il segno cambia, non scompare».**
- *Enunciato:* per ogni traccia confermata, in ogni ciclo fra l'ultima misura e la ricomparsa (o una chiusura dichiarata), lo schermo disegna il baricentro della previsione troncata alle celle non osservate del cuneo d'ingresso (anello vuoto, taglia fissa), la zona al 90 % e al 50 %, l'età; quando la zona al 90 % supera metà del cuneo il segno diventa croce con bordo a punti; alla ricomparsa, lo scarto per 0,5 s. «Perso» resta solo per le chiusure motivate.
- *Guadagno:* cicli con una stima mostrata dal 35–50 % (transito) e 8–10 % (sosta) al 100 %; il salto «dal nulla» di 0,5–0,8 m diventa uno scarto dichiarato di 0,18–0,61 m.
- *Vincoli:* niente su celle viste libere; il disco pieno solo con una misura del ciclo; la possibile presenza non cambia; costo indicativo sotto 1 ms a ciclo in Python puro [dopo].
- *Chi la prova:* `sciame-validazione`, dentro `sim_v2.py` (altro autore, con rumore).
- *Falsificatore (5 minuti):* 400 transiti e 400 soste con rumore e rilevamenti al 90 %; contare i cicli senza segno, le celle della zona su «libero», i passi del punto oltre 2·v·dt o all'indietro oltre 5 cm. **Esito atteso, scritto ora:** 0, 0, e passi anomali in meno del 5 % dei transiti (qui non sono sicuro: il rumore all'ingresso può far tremare il punto). La smentisce un solo ciclo senza segno o una sola cella su «libero».

**visualizzatore-2 — tabellone a due colonne.**
- *Enunciato:* quello del §3 (4), con la regola di lettura fissata prima della demo: sulle registrazioni, almeno 74 dentro su 86 per dire «compatibile con 9 su 10 e non con 8 su 10».
- *Guadagno:* la precisione è valutata davanti alla giuria; la probabilità di promuovere una zona che copre l'80 % scende dal 37,6 % a meno del 10 %.
- *Vincoli:* registrazioni diverse da quelle usate per tarare; righe per comportamento; previsione larga a parte.
- *Chi la prova:* `sciame-statistico` (la regola), poi tre persone esterne alla squadra.
- *Falsificatore (5 minuti):* mostrare tabellone e fotogramma A3 per dieci secondi a tre persone e chiedere «quante volte su dieci ricompare nella zona tratteggiata?» e «la zona è grande quanto la persona?». **Esito atteso:** almeno due su tre rispondono «nove»; nessuna risponde sì alla seconda. Un sì alla seconda smentisce la legenda.

## 6. Che cosa proporrei dopo

1. Portare la regola di `visualizzatore-1` in `sim_v2.py` e rifare le misure del controllo 1 con rumore.
2. La prova con tre persone (dieci secondi, due domande), anche su una stampa in bianco e nero.
3. Il battito sonoro con tre persone bendate, con la soglia già scritta nel nucleo (almeno 54 su 60).
4. Decidere con lo statistico se il tabellone dal vivo mostra una o due zone.

**Rifare:** nella cartella, `timeout 120 python3 punto_mostrato.py`; `timeout 120 python3 tabellone.py`; `timeout 120 python3 fotogrammi.py`; poi `rsvg-convert -w 1860 fotogrammi.svg -o fotogrammi.png` e `magick fotogrammi.png -colorspace Gray -threshold 50% -type bilevel fotogrammi_1bit.png`. Nessun seme: tutto è deterministico.
