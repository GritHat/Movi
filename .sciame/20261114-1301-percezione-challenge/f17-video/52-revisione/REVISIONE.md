# Revisione indipendente da giurato: `MoVi_pitch_EN_v1.mp4`

`sciame-lettore`, 2026-11-15, dalle 04:11 (`date -Is`). Due letture: prima **a freddo** (58 fotogrammi, uno ogni 3 s,
più il `.srt` come voce, senza aver letto i lavori dello sciame); poi **annotata** contro `VERDETTO_2C.md`,
`cifre.json`, `regole_challenge.md`, `prototipo/uscite/video/INDICE.md` e il testo della proposta v2.0.
I secondi indicati sono quelli del fotogramma (precisione circa ±1,5 s) o del `.srt`.

**Indipendenza.** Non ho prodotto il video e non ho letto prima i piani di regia. In comune con gli autori ho il
verdetto 2c e `cifre.json`, che ho letto dopo la prima visione. Non ho riletto i registri delle scene, salvo `INDICE.md`.
Non ho ascoltato l'audio: la voce l'ho letta nel `.srt`. Per questo la pronuncia, la musica e la sincronia fine sono
**non verificate**.

## 0. In testa

- **Regole violate da me:** nessuna. Ho scritto solo in questa cartella, più i fotogrammi nello scratchpad. Niente
  rete, niente git, nessuna cancellazione.
- **Cambi di stato proposti:** due righe a schermo vanno contro il «da non dire» del verdetto 2c (sotto, n. 1 e
  n. 2).
- **Controlli tecnici (verificati):**
  - durata 172,77 s, dentro 165–175;
  - video H.264 High, yuv420p, 1920×1080, 30 fps;
  - audio AAC 48 kHz;
  - −14,0 LUFS e picco vero −2,3 dBTP (`ffmpeg ebur128`);
  - `moov` in testa (faststart).

  Il bitrate audio misurato è 287 kb/s contro i 320 chiesti. Se l'impostazione era 320, la differenza è normale per
  l'AAC: **non verificato**.

## 1. Le quattro domande (§11, Q29)

1. **In 30 s si capisce che cosa fa?** In parte.
   - A 30 s il giurato esterno ha capito l'idea: ogni oggetto riceve «lo vedo / non lo vedo, ecco dove può essere /
     non lo so», e il «vuoto» si dice solo dove si è guardato.
   - Non ha ancora capito con che cosa lavora il sistema né per chi. I sensori arrivano a 37 s; l'operatore è nominato
     a 8 s, ma non si vede.
   - Il tecnico aerospaziale a 30 s ha capito la grammatica, non l'architettura.
2. **Ogni richiesta della traccia è riconoscibile?** Tutte tranne una.
   - **Riconoscibili:**
     - elementi mobili e ostacoli (s1, s3);
     - interruzioni della visibilità (s2, s5, s6);
     - osservato contro incerto (s2, il punto più forte);
     - feedback tempestivo (s1: 956 m contro 806 m);
     - perdita di affidabilità (s6);
     - accessibilità (s8);
     - sicurezza delle indicazioni («no output is a command»).
   - **Non riconoscibili:** «bassa latenza ed efficienza elaborativa». La parola «efficiency» compare solo nel
     sottotitolo grigio di «7 · LIMITS» (114–147 s), senza nessun contenuto. La proposta v2.0 dà un tempo per ciclo
     (mediana fino a 46 ms, 95° percentile fino a 340 ms, nucleo precedente, non rifatto). `cifre.json` (CIFRA-S7)
     dice invece «nessuna misura del tempo per ciclo del modo lungo». Il video tace, e il giurato tecnico lo nota.
3. **Nessuna frase promette più del verdetto?** Quasi. Ci sono due punti fuori dal verdetto e uno al limite.
   - Fuori dal verdetto: le critiche n. 1 e n. 2.
   - Al limite: la critica n. 6.

   Il resto torna con il §3 del 2c: 200/200, 0/171 con la mappa dichiarata, 12/200, 51/60, circa 4,5 km, circa 96
   tracce, 1062 → 1041 m, 50/200, 564/2400, 46 %.
4. **Una previsione si distingue sempre da un'osservazione?** Quasi sempre.
   - La grammatica regge: il punto pieno ciano è «visto»; l'anello arancio vuoto è «non visto», con la zona; il
     tratteggio è il possibile; «INFERRED» è scritto sugli eventi.
   - Tre eccezioni: n. 7 (la portata calcolata disegnata a tratto pieno), n. 8 (gli stati estranei in s8) e n. 9
     (il riquadro «TRUTH (SIM.)», mai spiegato).

## 2. Critiche numerate, in ordine d'importanza

1. **A 75–81 s la zona dei detriti sembra restringersi mentre la voce dice «does not shrink».**
   - L'inquadratura passa da «500 m» a «2 km» proprio su «It grows, does not shrink by looking». A 78 s il
     tratteggio riempie il quadro; a 81 s, dopo lo zoom, è un disco più piccolo.
   - Il giurato vede il contrario di ciò che sente: è il punto più fuorviante del video.
   - *Proposta:* scala fissa a 2 km per tutta la s5, oppure uno zoom dichiarato prima della frase («zoom out ·
     scale 2 km»).
   - *Prova:* fotogrammi 27–28 (`t_07`).
2. **A 69–90 s l'intestazione dice «run E1 n. 30, random».**
   - Il 2c §4 mette fra le frasi da non dire «`lp_E1_v3` è il passaggio n. 30 delle misure» (K-614: non è la stessa
     esecuzione).
   - *Proposta:* «run E1, chosen at random (seed declared)», senza il numero, oppure con la nota «not the measured
     run n. 30».
3. **A 23 s, «It says empty only where it has looked.»**
   - Il 2c §4 vieta «MoVi non dichiara mai libero ciò che non ha osservato» senza «con la mappa dichiarata, in
     simulazione». La qualifica arriva solo a 145 s.
   - *Proposta:* aggiungere in s2, a voce o a schermo, «…in simulation, with the site map declared». Oppure
     anticipare il limite della mappa (5 su 6 con la mappa sbagliata, che ora è solo a schermo a 120–126 s) e
     dirlo anche a voce.
4. **Latenza ed efficienza assenti.**
   - *Proposta:* una riga in s7, da `cifre.json` dopo la decisione del coordinatore. Una via è la cifra della
     proposta, con «earlier core, not re-measured». L'altra è dire onestamente «processing time per cycle: not
     measured for the long-range mode».
   - Va tolta la parola «efficiency» dal sottotitolo di s7 finché non c'è un contenuto. Oggi promette senza dare.
5. **Dati di sviluppo a schermo.**
   - Ecco dove compaiono:
     - «90 of 90 runs (v2), 30 of 30 (v3)» (93–113 s);
     - «earlier core, not re-measured» (138–147 s);
     - «PROVISIONAL REGISTER» nella fascia di s8 (148–158 s);
     - «own fragment model» e «seed declared».
   - *Proposta:* «within 3 cycles in all 120 simulated runs». La fascia di s8 diventa «Simulation · depth camera
     modelled from datasheets», se il verdetto lo consente.
   - Il 2c non ha s8 nella tabella §5: lo stato della fascia di s8 è **non verificato**. Va deciso, oppure s8
     diventa «Schematic».
6. **A 70–79 s, «infers contact … within two seconds in fifty-one runs of sixty.»**
   - Il 2c §1 dice: col tipo giusto («contatto») entro 2 s in 50/60; 51/60 è per l'evento di qualunque tipo.
   - *Proposta:* «infers the event», oppure 50/60.
7. **Nebbia, 51–69 s: il momento più debole.**
   - La nebbia non si vede: c'è solo l'etichetta.
   - La voce parla di un piccolo drone, ma nel quadro c'è un solo bersaglio, un aereo leggero («TRUTH»), «SEEN
     (RADAR ONLY)».
   - Il risultato è del 2 %, e la frase stessa lo smonta. Sono 18 s per un non-risultato.
   - Due difetti di impaginazione:
     - dopo lo zoom, «1 · SEEN (RADAR ONLY)» resta senza punto (57–66 s);
     - «1062 m» si sovrappone a «light aircraft» (57–66 s).
   - La portata dichiarata è un calcolo, ma è disegnata a tratto pieno, come un'osservazione.
   - *Proposta:* accorciare a circa 10 s. Velo grigio della nebbia, con la scritta «Schematic» solo sul velo. Portata
     dichiarata tratteggiata e con l'etichetta «declared (calculated)». Le etichette fissate al punto o tolte.
8. **«Same core», 148–158 s: il cambio è brusco.**
   - Da aerei e droni si passa alla persona cieca in 2 s di voce.
   - Compaiono «PARTLY SEEN» e «CONFIRMING»: due stati che non sono fra le «three answers» appena promesse.
   - Nel riquadro della verità c'è un testo tagliato, «out of sensor vi…».
   - *Proposta:* mostrare solo i tre stati, oppure una riga che dica che sono sotto-stati di «seen». Una frase di
     raccordo: «the same three answers, one metre from a person». Sistemare il taglio.
9. **«TRUTH (SIM.)» non è mai spiegato** (s1, s4, s5, s6, s8).
   - L'esterno può credere che MoVi conosca la verità; il tecnico capisce, ma si chiede se il pannello sia
     un'uscita.
   - *Proposta:* «simulator ground truth · not given to MoVi», almeno la prima volta (6 s).
10. **Ci si perde sui numeri delle tracce.**
    - In s1 due etichette, «3» e «26», stanno sullo stesso punto, e la verità mostra un drone (6–12 s).
    - In s5, «Two drones collide», ci sono tre tracce: 1, 2, 4.
    - In s6 la voce dice «about ninety-six tracks» mentre il pannello dice «POSSIBLE PRESENCE · 8–16» (96–113 s).
    - In s5 tre raggi diversi sono a schermo insieme: «radius 383…2138 m», «FOOTPRINT 5.0 km», «about 4.5 km, never
      over 5.3».
    - *Proposta:*
      - s1: una sola etichetta, oppure «2 tracks, same drone (radar + LiDAR)», se il registro lo conferma;
      - s5: evidenziare le due tracce che si urtano;
      - s6: «96 tracks warned over the whole run (median of 30 runs)»;
      - s5: un solo raggio a voce e a schermo, con gli altri in piccolo.
11. **Lettura in s7, 114–147 s.**
    - Paragrafi in monospazio con cifre non dette («0 of 171», «564 of 2400», «50 of 200», «5 of 6») scorrono mentre
      la voce dice altro.
    - Lo schema «sensors → cells → tracks → rules → outputs» non è mai commentato. «Cells» è gergo.
    - *Proposta:* al più due righe per volta, le stesse dette a voce. Lo schema si toglie o si commenta in una frase.
12. **Leggibilità.**
    - I testi principali sono leggibili a 1080p.
    - Le righe tecniche sono attorno ai 22 px. Sono leggibili a schermo pieno, ma marginali in una finestra o su un
      telefono: «run …», i sottotitoli grigi delle scene, «radii not to scale», «all counts in simulation…».
    - I sottotitoli incisi coprono la nota «radii not to scale · schematic» a 45 s.
    - *Proposta:* portarle a 26–28 px e alzare il contrasto del grigio. La nota va spostata sopra la fascia dei
      sottotitoli.
13. **Fasce «Simulation» su scene in parte «Schematic»** (s5, s6).
    - Il 2c vuole i detriti di E1 ed E2 e l'avviso al mezzo «solo Schematic». C'è l'etichetta interna «DEBRIS ZONE ·
      SCHEMATIC», ma la fascia in alto dice «SIMULATION» per tutta la scena, e il tratteggio occupa quasi tutto il
      quadro.
    - *Proposta:* fascia «Simulation · debris zone: Schematic» per tutta la durata.

## 3. Le altre risposte

- **Il momento più forte** è s2, 13–33 s: i tre stati, «EMPTY» barrato su «UNVERIFIED ZONE», «POSSIBLE PRESENCE».
  È chiaro per tutti e due i giurati. Subito dopo viene l'apertura di s7, «First, the limits», che per il tecnico
  vale credibilità.
- **Il momento più debole** è s4, la nebbia (n. 7). Poi viene s8 (n. 8).
- **Gli eventi** (collisione, fiammata, nebbia):
  - Sono credibili e non spettacolari: niente esplosioni, la fiammata è un riquadro «SATURATED» schematico, e i
    limiti sono detti (2,2 s, «does not discriminate», «optimistic»).
  - Non sono però **chiari**: tracce, raggi e zoom confondono (n. 1, n. 10).
  - I blocchi rossi pieni «RELIABILITY LOST» sono il colore più forte del video. Non è vietato, ma è molto acceso per
    una perdita di affidabilità. *Proposta:* il bordo rosso senza riempimento.
  - Nessun verde, nessun «via libera», nessun lessico d'ingaggio o militare: verificato sui 58 fotogrammi.
- **Il marchio e la chiusura funzionano.**
  - Il logo (punto pieno e anello tratteggiato) è la stessa grammatica di s2: buona continuità.
  - Le chiusure «Seen, not seen, unknown: declared for every track» e «No output is a command» sono buone.
  - I nomi restano a schermo circa 5 s (165–171 s): bastano.
  - La pronuncia di «MoVi» (Kokoro, «Mowvee») è **non verificata**.
- **Il ritmo.** 172,8 s, con pause di 3,5–4,6 s fra le scene (33–37, 66–70, 86–90, 127–130). Le pause vanno bene; a
  33–37 s il quadro dei sensori è quasi vuoto. s7 è densa (n. 11).

## 4. Stati proposti

| Voce | Stato | Motivo |
|---|---|---|
| Tecnica (durata, formato, −14 LUFS, picco, faststart) | **verificato** | misure sopra |
| Q29, domanda 1 | sostenuto, in parte | vedi §1 |
| Q29, domanda 2 | **smentito** per latenza ed efficienza | vedi §1 |
| Q29, domanda 3 | smentito in 2 punti | n. 2 e n. 3 |
| Q29, domanda 4 | sostenuto con 3 eccezioni | n. 7, n. 8, n. 9 |
| s8 come «Simulation» | **non risolto** | assente dalla tabella §5 del 2c |
| «loses the aircraft for seconds at a time» (s6) | sostenuto dai fotogrammi | 2,5 → 10,0 s «NOT SEEN»; registro non riletto |

## 5. Che cosa propongo dopo

1. Applicare i n. 1, 2, 3 e 5, che sono correzioni di testo e scala, e decidere il n. 4 col coordinatore, in
   `cifre.json`. Poi rendere `MoVi_pitch_EN_v2.mp4` accanto alla v1, senza cancellare niente.
2. Rifare questa lettura a freddo con un lettore nuovo sulla v2, e ascoltare davvero l'audio.
