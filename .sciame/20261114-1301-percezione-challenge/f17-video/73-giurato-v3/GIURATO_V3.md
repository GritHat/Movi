# Giurato sul video v3 (f17-video/73-giurato-v3, `sciame-lettore`)

Inizio 2026-11-15T06:56:12+01:00, consegna entro le 07:05 (`date -Is`), ben dentro la scadenza delle 09:15.
Oggetto: `video/consegna/MoVi_pitch_EN_v3.mp4` e `MoVi_pitch_EN_v3.srt`.

## 0. In testa

- **Durata: 173,856 s** (ffprobe). Il vincolo dell'utente (non oltre 176 s) **regge**, ma il margine è di soli
  **2,1 s**. Le correzioni che seguono sono pensate a tempo invariato. Dove una aggiunge parole, indico che cosa
  togliere per compensare.
- **Metodo.**
  - Ho estratto un fotogramma ogni 3 s (58, in `fotogrammi/`), li ho uniti in fogli 2×2 (`fogli/`) e li ho letti in
    sequenza, con il .srt come voce.
  - Per la leggibilità ho preso tre fotogrammi a piena risoluzione, a 68, 100 e 137 s (`ritagli/`).
  - Solo dopo la prima lettura ho confrontato le cifre con `VERDETTO_FINALE.md` (f20) e con `MoVi_registro_cifre_v3.md`.
- **Non verificato.**
  - L'audio: non l'ho ascoltato. Restano da controllare l'equilibrio fra voce e musica, la pronuncia e la
    corrispondenza fra il .srt e il parlato.
  - Il ritmo fra un fotogramma e l'altro.
- **Indipendenza.** Condivido con gli autori i verdetti e il registro, che sono la mia fonte delle cifre. Non ho
  ricontato nulla.
- **Regole violate:** nessuna. Ho scritto solo in questa cartella e non ho cancellato niente.

## 1. Che cosa capisce il giurato

**Parafrasi a freddo (giurato esterno).** «È un software che, per ogni oggetto in volo, dice se lo vede. Se non lo vede,
disegna dove può essere, e quella zona cresce col tempo. Non dice mai "libero" dove non ha guardato. Lo hanno provato
in sei o sette scenari simulati: un'avaria, droni che si scontrano, un lampo che acceca le camere, un drone che ne segue
un altro mentre accanto c'è un'esplosione. Tutto è simulato. Osserva e avvisa, non comanda.»

**È quello che si voleva dire?** Sì, nel nucleo.

**Test dei 30 s.**
- **Superato a metà.** A 26 s le tre risposte sono chiare. La scena 2 (13–26 s) è la più limpida del video.
- **Che cosa manca nei primi 13 s.** Lo spettatore guarda un cruscotto denso (NOT SEEN, region, PROXIMITY WARNING) prima
  di conoscerne il vocabolario. Il titolo promette «Two fast drones, then contact», ma il contatto non si vede: il
  registro arriva a t = 25 s con il solo avviso di prossimità. E sullo schermo ci sono tre o quattro tracce, non due.
- **Che cosa non si capisce in 30 s.** Chi guarda quello schermo: un operatore, un pilota, una macchina?

**Caso centrale (giurato tecnico aerospaziale).**
- **Chiaro e ben costruito.** Il video ammette il limite principale a voce, a 63,9 s: la collisione veloce non è
  dichiarata come evento. È onesto.
- **La credibilità cala in quattro punti**, descritti nelle critiche 1–4:
  - la stessa collisione «non dichiarata» in F3 compare come «EVENT: nearby collision · inferred» in F7;
  - l'innesco ottimista, preso dal vero, si legge solo in piccolo;
  - la rappresentatività dei dati ADS-B;
  - il 60/60 detto mentre si vede il radar accecato.

**Previsione e osservazione: distinte quasi sempre**, ed è il punto forte del video:
- la legenda «truth (simulation only, MoVi does not see it)», SEEN contro NOT SEEN, «computed in the model»;
- nel § 7, i pannelli separati per la curva calcolata e per la copertura osservata.

Le eccezioni:
- le regioni piene (marroni) non hanno una voce nella legenda (critica 8);
- in F7 la barra della confidenza torna piena subito dopo il ripristino dichiarato dei sensori: il giurato la legge
  come un'osservazione.

**Momento più forte.** La scena 8, F7 «scorta» (108,7–139,1 s). È concreta: sensori dichiarati «UNRELIABLE · saturated»,
volume dei detriti «never clear inside», righe di limite in rosso. È la scena che un giurato ricorda.

**Momento più debole.** Ce ne sono due:
- la scena 7 (82,8–108,7 s): quattro pannelli, una formula, una «fixed zone at loss 150 m» non spiegata e note da
  14 px;
- la scena 3 (26,6–33,4 s): la frase più forte del video, «never said clear», è detta sopra una scena in cui non
  accade nulla che la mostri.

**Ritmo.** Ci sono due tratti lenti:
- l'apertura (13 s senza una frase che dica che cosa fa il sistema);
- la scena 7 (26 s di grafico).

La scena 8 regge i suoi 30 s.

**Leggibilità a 1080p.**
- **Leggibili:** i titoli, il quadro dei sensori (~20 px) e le righe delle cifre in F7 (~20 px).
- **Illeggibili, anche su un monitor:**
  - le note della scena 7 (~14 px, grigie), a 93–108 s;
  - la riga V-11, grigia, a 64–73 s;
  - la riga F7-ID, grigia, a ~130 s.
- **Etichette tagliate dal bordo del pannello:**
  - «region 73 r» (~6 s);
  - «region 13(» (~28 s);
  - «region 87», «region 1.4» e «region 2.» (~47–52 s);
  - «region 16(» (~63 s).

## 2. Correzioni, in ordine d'importanza (con il secondo)

1. **119–139 s · F7, evento «nearby collision · inferred».**
   - **Il problema.** A 63,9 s la voce dice che la collisione non è dichiarata come evento; mezzo minuto dopo lo schermo
     scrive «EVENT: nearby collision · inferred». Il giurato conclude che MoVi rileva le collisioni in volo, che è una
     frase da non dire (VERDETTO_FINALE § 7, riga 302).
   - **Perché è falso.** In F7 l'evento nasce alla prima scansione per un artefatto ottimista (F-806): la saturazione è
     presa dalla finestra vera dell'evento, e i frammenti a 30–100 m sono visti subito.
   - **Correzione a tempo zero:** riscrivere la riga del quadro così: «EVENT: flash nearby · inferred from saturation
     (optimistic trigger, simulator)».
2. **122,6–138 s · F7, «In sixty of sixty simulated runs, the tracked drone stayed inside its region».**
   - **Il problema.** La frase è detta sopra il registro F7r, dove si vede il radar «UNRELIABLE · saturated». Ma il
     60/60 vale con il radar a 360° **non accecato** (lo dice la riga F7-CONT). Con il radar accecato il dato è 59–60/60,
     il peggiore 59/60 [0,911; 0,997] (S-6r).
   - **Correzione a tempo neutro:** fondere le due frasi in una. Per esempio: «With cameras and radar blinded for up to
     two seconds, the tracked drone stayed inside its region in at least fifty-nine of sixty runs, and no fragment was
     ever called clear.»
   - **Da aggiungere a schermo:** F-805, «avviso al portatore non discriminante: 60/60 anche senza frammenti vicini».
     Oggi la riga «warning: path enters debris volume» sembra una prestazione.
3. **39,5–48,5 s · F4, «MoVi infers the event… within one second».**
   - **Il problema.** L'innesco ottimista (la saturazione presa dal punto vero) compare solo in piccolo, come
     «optimistic trigger». Per un tecnico è la prima domanda.
   - **Correzione:** nella stessa riga del quadro, «trigger: optimistic (saturation from simulation truth)». Oppure,
     nella voce, «…within one second, with an optimistic trigger, in sixty of sixty runs», togliendo «simulated» per
     compensare il tempo.
4. **93,5–104 s · Scena 7: rappresentatività dei dati ADS-B.**
   - **Il problema.** «89.5 % of cases from 4 flights of one route» sta in una nota di 14 px, grigia. Il giurato
     tecnico che la legge (fermando il video) si sente fuorviato da «public flight tracks». In più, 0,85–0,89 è un po'
     sotto il 0,9 promesso, e il video non lo dice.
   - **Correzione:**
     - la nota a ≥ 20 px, in bianco;
     - nella voce, «…eighty-five to eighty-nine in a hundred, a little under target, mostly on one route», al posto di
       «from one to thirty seconds», che resta leggibile sull'asse del grafico.
5. **26,6–33,4 s · Scena 3: la frase V-1 non ha immagine.**
   - **Il problema.** La scena F1 mostra solo puntini SEEN. Inoltre dice «six flight scenarios», mentre il video ne
     mostra sette (F7 compreso).
   - **Correzione:**
     - inquadrare un istante in cui la croce del vero sta dentro una regione NOT SEEN, con la scritta «not observed ≠
       clear»;
     - scrivere «six flight scenarios with the core», perché F7 usa un tracciatore a parte (riga 272).
6. **139,6 s · «The same core works on a site».**
   - **Il problema.** I risultati del sito vengono dal nucleo v3 (LP-1) e dal v2 (LP-4), e F7 non usa il nucleo
     (VERDETTO_FINALE, riga 272).
   - **Correzione a tempo zero:** «The same approach works on a site».
7. **0–13 s · Apertura.**
   - **Il problema.** La scena è densa, il contatto promesso dal titolo non si vede e le tracce sono più di due.
   - **Correzione:** aprire con il lampo di F7 (a ~115 s) o con il contatto di F3 (a ~63 s). In alternativa, cambiare
     il titolo in «Fast flight: drones on a collision course».
8. **Tutte le scene di simulazione · La legenda non spiega le regioni piene.** Le aree marroni piene sono:
   - l'impronta in F4, a 35–52 s;
   - l'insieme di presenza in F3, a 60–73 s;
   - il volume dei detriti in F7.

   La correzione: aggiungere alla legenda «filled: where it can be after an event, no probability».
9. **~6, 28, 47–52 e 63 s · Etichette tagliate dal bordo.** Spostarle dentro il pannello.
10. **Ovunque · Sigle interne a schermo.**
    - **Il problema.** V-1, F7-CONT, C-TAR, LP-1, «S», «min. progressive» e «10 s threshold set after» non dicono nulla
      a un giurato.
    - **Correzione:** parole semplici; le sigle restano nel registro. Per esempio, «10 s threshold chosen after the
      runs».
11. **~136–139 s · F7, due radar diversi.**
    - **Il problema.** Il quadro dice «RADAR 360°», la riga rossa dice «forward-only radar», e il giurato non capisce
      quale sia.
    - **Correzione:** «with a forward-only radar instead: side/behind collision seen 1/60 and 0/60».
12. **64–73 s · Riga V-11, grigia.** «2/60 false events» non dice in quale prova.
    - **Correzione:** scrivere «false events in control flights 2/60», oppure togliere la riga, perché la scena 10 dice
      già «not adopted».
13. **63,9 s · «in every simulated run».** Il § 7 del verdetto chiede «in k su n, simulato».
    - **Correzione a tempo pari:** «in sixty of sixty runs».

## 3. Stati degli enunciati del video (dal registro e dal verdetto, non ricontati)

Le cifre dette sono coerenti con `MoVi_registro_cifre_v3.md` e con `VERDETTO_FINALE`. Non ho trovato frasi del § 7.
L'unica eccezione è l'**implicazione** visiva della critica 1.

| Enunciato | Dato | Stato |
|---|---|---|
| V-1 | F6 0/200 [0; 0,019]; altre celle 0/60 [0; 0,060] | sim |
| V-2 | 60/60 [0,940; 1], innesco ottimista | sim |
| V-3 | 58/60 [0,886; 0,991] | sim |
| V-5 | 60/60 [0,940; 1], soglia scelta dopo | sim |
| V-6 | 60/60 [0,940; 1] | sim |
| V-10 | 60/60 [0,940; 1], identità presunta | sim |
| C(τ) | | dim nel modello; mostrata come schema |
| Copertura | 0,85–0,89; 21–30 s 0,85 [0,81; 0,88]; virata 0,73 [0,67; 0,78] **L** | pub, casi correlati |
| F7-CONT | 60/60 ×4 [0,940; 1], radar non accecato | sim |
| F7r | «clear» 0/60 [0; 0,060]; regione 59/60 [0,911; 0,997] | sim, cecità ip |
| LP-1 | 200/200 [0,981; 1] | sim |
| Calcolo dedicato | 0,08–1,2 ms | ip |

## 4. Proposte

- **lettore-1: una riga fissa in F7, «event and trigger: optimistic in simulation».**
  - Previsione: un giurato tecnico che rivede le scene 5 e 8 non conclude più che MoVi rileva la collisione.
  - Prova che la smentirebbe: un lettore a freddo che, dopo la nuova versione, parafrasi ancora «rileva le collisioni
    in volo».

## 5. Dopo

1. Applicare le correzioni 1, 2 e 6, che non costano tempo, in una versione v3.1 accanto alla v3.
2. Ricontrollare la durata con ffprobe: deve restare ≤ 176 s.
3. Far ascoltare l'audio a un lettore: è la parte non verificata.
4. Ripetere la lettura a freddo, con un lettore nuovo, sulla v3.1.
