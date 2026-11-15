# MoVi, video: attacco alle tre proposte di preproduzione (`sciame-avversario`, f17-video/21)

Cominciato il 2026-11-15T00:30:12+01:00, chiuso verso le 00:50 (`date -Is`). Bersagli:
`10-messaggio/MESSAGGIO_E_ARCO.md` con `voce_en.txt` (M), `11-marketing/POSIZIONAMENTO_E_LOGO.md` (K),
`12-regia/REGIA_E_SISTEMA_VISIVO.md` con i fotogrammi `stile_*_v2.png` (R), `video/marchio/` (logo).
Il metro: `ISTRUZIONI_VIDEO_UTENTE.md` §3, §7 e §11 (regole d'onestà, ancora vincolanti) e i dati della fase 2.

## 0. Cambi di stato e regole violate

- **Previsioni.** Le ho scritte solo per i segnaposto (§3, alle 00:44, prima del verdetto, che alle 00:32
  non esiste: `30-verdetto/` manca). Le critiche 1–30 sono **osservazioni fatte dopo** la lettura, non
  previsioni confermate.
- **Rete:** due ricerche web generiche (nome di un marchio commerciale, forme di logo), senza dati del progetto.
- **Scritture:** solo questo file. Niente cancellazioni, niente git, niente sudo.
- **Indipendenza.** Non ho scritto nessuna delle tre proposte. Condivido con loro le istruzioni dell'utente e i
  file della fase 2: un difetto che sta già in quei file (per esempio una soglia presa per un risultato) lo vedo
  solo se si contraddicono fra loro.
- **Esecuzione.** Ho contato i pixel verdi sui tre fotogrammi v2 e sulla tavola del marchio, con un mio script
  (Pillow, tinta 90–160°, saturazione > 0,3). Esito: 0, 1, 0 e 0 pixel. Il pixel in B è antialias. Il controllo Q11
  regge, e lo confermo in modo indipendente.

## 1. Critiche, ciascuna con la prova

### A. Capacità promesse oltre le prove

1. **«For every object, one of three answers» è falso per gli oggetti mai rilevati.** È nella voce, scena 2 di M.
   - Il registro ha `stato ∈ {in_conferma, vista, vista_in_parte, non_vista, previsto_ampio, ricomparsa}`
     (R §1.2). Non c'è uno stato «ignoto» per oggetto.
   - Un drone piccolo sotto la soglia del radar, che non trasmette, non ha traccia. MoVi non dice «non lo so»
     su di lui: dice «non verificato» sulle **celle**.
   - Lo stesso difetto sta nella tagline T1 di K, «Seen, unseen, unknown: always declared».
   - *Caso che rompe:* scena 3 di M, «a small drone outside the radar threshold». Per costruzione quel drone non
     riceve nessuna delle tre risposte.
2. **«It never calls a space empty unless it has looked» è più forte della regola.** È nella voce, scena 9 di M.
   - La regola chiede la Pd cumulata **per la classe più piccola ammessa** (EV-B/EV-E; `scenari_eventi.json`
     E1: «'libero' solo dove la Pd cumulata lo consente per il multirotore piccolo»).
   - Il radar che guarda un drone piccolo oltre la sua portata di calcolo «ha guardato», ma non basta. R
     (critica 7) l'aveva già visto; M non l'ha recepito.
3. **«The radar alone still sees the aircraft»** è detto in voce senza riserva (scena 6 di M). Ma l'effetto della
   fiammata sul radar è «non verificato» (EV-C; `EFFETTI_SUI_SENSORI.md` §6).
   - La riserva sta solo a schermo, e il sottotitolo del fotogramma B la toglie del tutto: «The radar still holds
     the aircraft».
   - Il sottotitolo inoltre **non coincide con la voce**: Q20 fallirebbe.
4. **«If the radar drops too»** viene subito dopo «Fog rolls in» (scena 4 di M). Lo spettatore capisce che la
   nebbia spegne il radar, che è falso.
   - In E3(c) la caduta del radar è un **guasto iniettato** per 20 s, non un effetto del meteo.
5. **«A warning to the person below» e «The service vehicle is warned»** (scene 5 e 6) fanno intendere un canale
   diretto verso persone e mezzi, e una protezione tempestiva.
   - Il prototipo ha come uscite lo schermo, i suoni brevi e il registro (`ARCHITETTURA.md`). Il canale verso la
     persona non esiste.
   - In E1 il primo frammento tocca terra in 4,0 s. L'avviso «entro 2 s» è una **soglia scritta prima** (`misure`),
     non un risultato. I tempi di reazione sono ipotesi.
   - La frase urta anche «No output is a command»: un avviso diretto a un conducente si legge come un ordine.
6. **CIFRA-V1, «[k] of [n] simulated fragments stayed inside the declared volume»** (voce, scena 7): è la frase
   più esposta del video.
   - (a) La misura conta **campioni (frammento, istante)**, non frammenti (`misure`: «quota dei campioni
     (frammento, istante)»). La frase cambia il senso: viola la regola 5.
   - (b) Vale solo nel dominio «v_t ≥ v_t_min e |u| ≤ dv», che in voce non c'è.
   - (c) Frammenti e volume vengono dallo **stesso modello e dallo stesso autore** (M §5 lo dice). Un risultato
     come «0 su 1 131 692» misura la coerenza interna, non il mondo.
   - (d) Detta così, la frase vende «sappiamo dove vanno i frammenti», cioè la capacità vietata «prevedere dove
     andrà un frammento».
7. **CIFRA-V2, «Tracks lost without a warning»** usa «lost», vietato come stato (regola 15; M §7 lo vieta da sé).
   - Chiede inoltre E1–E4 eseguiti con le regole EV, che **non sono realizzate** in `movi_lp.py`
     (`REGOLE_E_SCENARI_EVENTI.md`, righe 23–24).
   - È incompatibile con STATO-1 «the full chain has not yet run end to end»: se la catena non gira, V2 non esiste.

### B. Cifre senza dominio e segnaposti a rischio

8. **CIFRA-S1** (scena 2) sarebbe una cifra di simulazione su una scena **Schematic**. Il suo valore, Wilson 0,8703,
   misura il generatore e non il mondo, e la classe e l'orizzonte non sono detti. Violerebbe le regole 11 e 23.
9. **CIFRA-S2:** la riga dice «(assumed)» per la sezione radar, ma non «by calculation» per la portata
   (regola 6). Manca anche il disturbo del suolo a quota bassa, il caso dei droni sul piazzale.
10. **CIFRA-S4, S5 e S6** sono **soglie** («≤ 2 s», «0 su 1000», «≤ 3 cicli»), non risultati. Se il verdetto non
    le misura, il rischio è che il montaggio metta la soglia al posto del risultato. S6 in «cicli» non ha
    significato senza la durata di un ciclo. S5, anche se esce 0 su 1000, vale solo per «due droni a 5 m, nessun
    contatto»: lo stormo resta un controesempio aperto (M §9).

### C. Lessico

11. **Lo stesso stato ha tre nomi inglesi diversi nelle tre proposte:**

    | Stato | M | R | K |
    |---|---|---|---|
    | Suolo vuoto osservato | OBSERVED EMPTY | SEEN FREE TO 2 000 m | seen clear up to d metres |
    | Zona allargata | WIDE ZONE | WIDE PREDICTION | — |
    | Ricomparsa | SEEN AGAIN · IDENTITY ASSUMED | REAPPEARED · IDENTITY PRESUMED | — |
    | Non vista | NOT SEEN FOR X s | NOT SEEN · 2.4 s | — |

    - Q10 fallisce.
    - «clear» è vietato da M §7, ma K lo usa due volte: «seen clear», e la frase di posizionamento EN «never
      presents … as clear».
    - «FREE» in inglese suggerisce il «via libera» (regola 9). La versione di R manca anche della classe.
12. **«PREDICTED» e «WIDE PREDICTION» a schermo** (fotogramma A: «A · PREDICTED») presentano la zona come una
    previsione della posizione. È la formula che M §7 vieta («predicts where it will be»).
13. **Parole vietate dentro le virgolette:** il fotogramma A scrive `never "gone"`. Q9 lo trova.
14. **«test ranges»** in K, nel posizionamento EN, evoca il poligono militare. Va scritto «test sites».
15. **«No engagement or pointing function»** è la formula L8, in negazione, e va tenuta. Q9 però la intercetta:
    serve un'eccezione scritta nel rapporto di QA.
16. **Il conflitto con le regole 15, 24 e 25 non è registrato.** Quelle regole vietano «drone» e «in volo». K lo
    segnala, M lo ignora, e Q27 chiede che ogni conflitto sia registrato con la scelta fatta.

### D. Immagini

17. **Fotogramma A, la previsione disegnata come osservazione.** Nel pannello «AS MoVi DECLARES IT» ci sono circa
    40 punti bianchi dentro il volume dei detriti.
    - R §5 dice che lì vanno «solo ritorni misurati, se il registro li dà». Il fotogramma fa il contrario.
    - Il bianco è anche il colore riservato alla posizione vera (regola 7 delle nove).
    - Il risultato si legge come «il sistema vede i frammenti». Violano la regola 22, la regola 1 delle nove (niente
      dentro la zona) e Q15.
18. **Fotogramma B, la fiammata è una stella bianca a 15 punte sull'aereo in corsa.** È l'icona fumettistica
    dell'esplosione, e l'immagine evoca un incidente reale in decollo. Senza alone resta comunque spettacolare.
19. **Fotogramma B, i cunei corallo vanno dai sensori all'aereo** e si leggono come fasci puntati sull'oggetto.
    Sono le coperture dei sensori guasti, ma l'aspetto è quello di un puntamento.
20. **Glifi a bersaglio.** Il glifo del radar (cerchio con punto) e il simbolo SDMs (anello tratteggiato con un
    anello pieno al centro) somigliano a un mirino o a un bersaglio a cerchi, davanti a una giuria del settore difesa.
    Il divieto «niente mirini né reticoli» (M §7, R §2.3) colpisce la forma, non l'intenzione.
21. **Fotogrammi di stile.** In alto c'è «SIMULATION», in basso «values schematic, not from the log»: le due righe
    si contraddicono. Nel video, un'inquadratura senza registro porta solo «SCHEMATIC» (regola 13; la proposta
    `creativo-videomaker-2` va resa obbligatoria).

### E. Marchio, nome, licenze, tempi

22. **Il nome «MoVi» collide con «MōVI» di Freefly Systems**: stabilizzatori di camera, anche in configurazione
    aerea su drone.
    - È lo stesso settore del video, droni e aerei ([B&H](https://www.bhphotovideo.com/explora/node/30652),
      [heliguy](https://www.heliguy.com/blogs/posts/freefly-unveils-the-movi-pro/)).
    - Lo stato del marchio registrato **non è verificato**: non ho interrogato le banche dati dei marchi.
    - Il nome è una scelta dell'utente. Il rischio va detto a lui, non corretto qui.
23. **Somiglianza del logo.** Una ricerca non ha trovato marchi noti «disco pieno accanto ad anello tratteggiato».
    Il più vicino è Gojek Solv: anello con un'apertura e un punto al centro
    ([whatthelogo](https://whatthelogo.com/logo/gojek-solv/214212)).
    - Rischio basso, ma **non verificato**: una sola ricerca, nessuna banca dati dei marchi.
    - K §5 lo ammette: «ricerca di anteriorità non fatta».
24. **La musica di MacLeod (CC BY 4.0) obbliga all'attribuzione.** Il cartello dei crediti di K ne contiene circa
    70 parole in 3,5 s.
    - Viola la regola 3 (16 parole per schermata) e non si legge.
    - Il tappeto sintetico (R §4) non ha diritti di terzi e non obbliga a niente.
    - Il CC0 di Bartmann resta non ascoltato.
25. **Il cartello dei limiti di K è «letto anche in voce»**: aggiunge circa 37 parole alle 328 di `voce_en.txt`
    (conteggio `wc -w`), per un totale di circa 365, oltre il limite di 340 (regola 2).
    - Il titolo di K (0:00–0:04) si sovrappone alla scena 1 di M, che comincia a 0:00.
    - Le durate di M e di R non coincidono: la scena 2 dura 26 s in M e 20 s in R, la scena 6 dura 20 s in M e 26 s
      in R.

## 2. Stati che propongo

| Enunciato | Stato |
|---|---|
| «For every object, one of three answers» | **Smentito** dal caso del drone piccolo senza traccia (critica 1) |
| T1 «always declared» | **Smentito** come universale; vale per gli oggetti seguiti, per formato del registro |
| «never calls a space empty unless it has looked» | **Smentito** come formulato; regge con «… looked well enough for that class» |
| «The radar alone still sees the aircraft» | **Non risolto**: lo decide una fonte sull'effetto del lampo sul radar; fino ad allora «in the model» |
| Palette senza verde (fotogrammi, tavola) | **Verificato** sui quattro PNG (0/1/0/0 px), non sul video |
| Il logo non somiglia a marchi noti | **Non verificato** (una ricerca; nessuna banca dati) |

## 3. Previsioni sui segnaposti (scritte alle 00:44, prima del verdetto) e misure sostitute

| Segnaposto | Previsione | Smentita se | Misura sostituta |
|---|---|---|---|
| V1 | Arriva solo come campioni sullo stesso generatore, nel dominio dichiarato | Arriva su un generatore indipendente, con fisica diversa | In voce la proprietà «per costruzione»: «the declared volume never shrinks» (C). A schermo «0 free cells inside the footprint: k of n cycles», che è l'uscita di sicurezza vera. Se V1 resta, va detto «in our own fragment model, [k] of [n] samples» |
| V2 | **Non arriva**: le regole EV non sono realizzate | Il verdetto riporta E1–E4 eseguiti con EV-A…E | «Objects left with no declared state: [k] of [n] frames», contato da `valida_riga` sui registri che esistono, a corto raggio e `lp_A1`/`lp_A2` se ci sono, con il dominio |
| S4, S5, S6 | Non arrivano, per la stessa causa | Come sopra | Tolte dallo schermo. **Mai** la soglia al posto del risultato. Al massimo «test threshold, written before: ≤ 2 s · result pending» |
| S1 | Arriva solo sul generatore | Copertura misurata su tracce di classe aereo o drone | Tolta dalla scena 2 (che è Schematic) |
| S7 | Arriva per il corto raggio (6 ms), non per il lungo | Misura del ciclo di `movi_lp.py` | La cifra a corto raggio solo nella scena 8, con «scene simulate · portatile» |

## 4. Correzioni obbligate (prima del copione definitivo)

1. **Voce, scena 2:** «For every **tracked** object, one of three answers… What it has not observed, it never calls
   empty: **it marks it unverified**.»
2. **Voce, scena 9, e tagline:** «It never calls a space empty unless it has looked **well enough for that class**.»
   La tagline T1 diventa «Seen, unseen, unknown: **declared for every track**», oppure si passa a T3.
3. **Voce, scena 6:** «**In the model**, the radar alone still sees the aircraft.» A schermo «flash effect on radar:
   not verified». Il sottotitolo deve essere **uguale** alla voce.
4. **Voce, scena 4:** «If the radar **also fails, a fault we inject**: reliability lost, warning not timely.»
5. **Voce, scene 5 e 6:** «**the operator is warned: a person is inside the footprint**» e «**the operator is
   warned: unverified zone on the vehicle's path**». Niente avviso diretto a persone o mezzi.
6. **Scena 7:** V1 riformulata con «samples» e il dominio, oppure sostituita come in §3. V2 senza «lost»
   («objects left with no declared state»), oppure tolta. Se STATO-1 è «not yet», V2 si toglie.
7. **Un solo lessico.** Vale la tabella di M §6, con queste modifiche:
   - **OBSERVED EMPTY · class · to d m** al posto di SEEN FREE e di «seen clear»;
   - **WIDE ZONE** al posto di WIDE PREDICTION e di PREDICTED;
   - via `never "gone"` dal fotogramma A;
   - «test sites» al posto di «test ranges».

   R e K si allineano a M.
8. **Fotogramma A:** nessun punto nel pannello delle dichiarazioni, salvo i ritorni misurati del registro, marcati
   «RADAR RETURNS», mai bianchi. I frammenti restano solo nel pannello della verità.
9. **Fotogramma B:**
   - la fiammata diventa un'area bianca piatta, senza punte, sul motore, con la scritta «FLASH (3 s) · schematic»;
   - l'aereo resta intatto;
   - le coperture dei sensori guasti si disegnano come settori interi, non come cunei verso l'aereo.
10. **Glifi:** il radar diventa un cerchio pieno piccolo con un arco. Nel simbolo SDMs si toglie l'anello interno, e
    resta il disco pieno accanto all'anello tratteggiato vuoto. Al test dei cinque secondi (K §7) si aggiunge la
    domanda «somiglia a un mirino?». Smentita se 2 persone su 5 o più rispondono sì.
11. **Musica:** il tappeto sintetico. Se si sceglie MacLeod, l'attribuzione va in un cartello di 2 s da al più 16
    parole e nel `.srt`/descrizione, registrata in Q22.
12. **Durata:** il cartello dei limiti va **solo a schermo**. Un'unica tabella dei tempi, quella di M, poi
    riconciliata da R. Il titolo entra nei 12 s della scena 1. Il totale delle parole va riverificato ≤ 340.
13. **Conflitti e QA:**
    - si registrano in Q27 la decisione su «drone/aircraft» (solo oggetti osservati; sensori a terra, fermi) e
      l'eccezione L8 in Q9;
    - l'etichetta «SIMULATION» si stampa solo se c'è un registro (`creativo-videomaker-2`, resa obbligatoria);
    - il rischio del nome MoVi rispetto a «MōVI» si segnala all'utente.

## 5. Dopo

Il comunicatore rifà `voce_en.txt` e `voce_it.txt` con le correzioni 1–6. Il videomaker rifà i fotogrammi A e B
come nuove versioni `_v3`, accanto alle v2. Il marketing rifà il simbolo come `_v3`. Il lettore critico ripassa Q9,
Q10 e Q15 sui nuovi fotogrammi. All'arrivo del verdetto si applica la tabella di §3 senza riaprire il copione.
