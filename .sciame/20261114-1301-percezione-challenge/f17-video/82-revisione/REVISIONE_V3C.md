# Revisione da giurato del video v3c (`sciame-lettore`, 82-revisione)

Inizio 2026-11-15T07:36 (date -Is). Previsioni scritte prima di guardare: `PREVISIONI.md` (07:36).
Video: `video/consegna/MoVi_pitch_EN_v3c.mp4`, durata **174,379 s** (ffprobe) ≤ 176,0: regge.
Metodo: un fotogramma ogni 3 s (58), in 15 fogli 2×2 con l'ora (`fogli/s_01..15.jpg`), letti nell'ordine e con il
`.srt` EN v3c al posto della voce. **L'audio non l'ho ascoltato** (ritmo, pronuncia e velocità: non verificato).
Indipendenza: condivido con gli autori soltanto i rapporti c1, che ho usato come riferimento. Non ho letto la QA v3.

## 0. In testa

- **Esito delle previsioni.**
  - P1 regge: a 123–138 s è a schermo «59/59 [0.939; 1] · without 0/59 [0; 0.061] · same seeds · sim.».
  - P2 regge in parte: la voce dice un solo limite («the warning does not say where»). Gli altri due compaiono solo
    a schermo, in rosso e in piccolo.
  - P3 regge: «SIMULATION», «SCHEMATIC» o «SIMULATION (site) · SCHEMATIC (short range)» compaiono in tutti i 58
    fotogrammi.
  - P4 regge.
- **Regole violate:** nessuna nota. Non ho cancellato file. Ho scritto solo in `82-revisione/`.
- **Difetto principale:** il riquadro LIMITS (circa 153–167 s) contraddice la scena F7 (vedi C1).

## 1. Che cosa capisce un giurato (parafrasi)

«MoVi non dice mai "libero" dove non vede: dice "lo vedo", "non lo vedo ma è qui intorno" oppure "non lo so". In
simulazione regge al guasto in volo, alla collisione fra droni e al lampo. Sulle tracce reali la regione tiene circa
l'85–89 % dei casi, meno del 90 % promesso, e in virata scende al 73 %. Su un drone in scorta, quando radar e camere si
accecano insieme, una correzione in prova fa partire l'avviso al portatore prima dei frammenti in 59 casi su 59. Senza
la correzione l'avviso non partiva mai. L'avviso però non dice dove.»

Questo è ciò che si voleva dire. La scena F7 è **chiara e onesta**:
- voce: «With a fix under test… against none without it», poi «A promising path: the warning does not say where»;
- schermo: «fix under test», «conservative, not localised, not selective», «flash and smoke: drawn for illustration»
  e i tre limiti in rosso.

La scena non promette più del dimostrato. Le cifre e gli intervalli coincidono con VERIFICA.md e con l'addendum 19:
59/59 e 0/59, 49/60 e 40/60, 565 m e mediana 8 s, 11/200. Ho ricontrollato i limiti Wilson: 59/59 dà 0,939; 0/59 dà
0,061; 11/200 dà [0,031; 0,096].

## 2. Correzioni in ordine d'importanza

Sono tutte fattibili in 30 minuti e a durata invariata.

1. **~153–167 s · Riquadro LIMITS: «radar blinded: debris warning to the carrier not reliable».**
   - **Il problema.** È il limite di prima di c1 (`cifre_v3c.json`, riga 170, copiato da `cifre_finale.json`).
     Quindici secondi prima la scena F7 mostra l'avviso in 59/59. Un giurato legge una contraddizione: o la
     correzione non conta, o il riquadro è vecchio. Documento tecnico e proposta v3.1 riportano c1.
   - **Correzione (solo testo, 0 s):** «radar blinded: fix under test; warning not localised; reacquisition still
     below threshold».
2. **~140 s · Voce F7: dice un solo limite su tre.**
   - **Il problema.** La frase permessa da VERIFICA.md chiude con «target reacquisition improves only partly». La
     voce v3c la omette, e un tecnico aerospaziale chiederà proprio «e il bersaglio lo riprendete?».
   - **Il margine di tempo.** Fra la riga 24 (fine 137,674 s) e la riga 25 (inizio 140,524 s) ci sono 2,85 s di
     silenzio.
   - **Correzione:** «A promising path: the warning does not say where, and reacquisition is still partial.» Sono
     circa 1,5 s in più, da far stare in quella pausa, a durata totale invariata e senza accelerare la voce. Va
     verificato con ffprobe dopo il rendering.
3. **~117–119 s · F7, barra di confidenza.**
   - **Il problema.** Il quadro dice «RADAR 360°: UNRELIABLE · saturated», «CAMERA: UNRELIABLE» e «NOT SEEN 0.5 s».
     Eppure la barra «confidence on the tracked drone» resta piena, oltre il segno 0.9; a 120 s (NOT SEEN 1,6 s) è
     ancora quasi piena. Poi, a 126–138 s, il drone torna SEEN con «identity presumed, doubtful» e la barra torna
     piena. Per un tecnico l'immagine dice «fiducia alta senza vedere» e «identità dubbia ma fiducia piena».
   - **La correzione** si fa in due tempi:
     - subito, una scritta accanto alla barra: «position confidence, model; identity: doubtful»;
     - se c'è tempo, l'etichetta del segno: «0.9 (optimistic)», che è la correzione «(optimistic)» del giurato v3
       ancora aperta.
4. **~84–109 s · Sigle interne** (giurato v3, punto 10, ancora aperto).
   - **Il problema.** «C-TAR 1-2 s», «min. progressive», «Wilson 95 % per case», «(F5)» a 69 s e «LP-1 · S» /
     «LP-4 · S» a 141–152 s non dicono nulla a un giurato.
   - **Correzione:** parole semplici. Per esempio, «LP-1 · S» diventa «simulation».
5. **~84–109 s · Etichetta tagliata a sinistra**: «…d zone at last sighting · 150 m» (giurato v3, punto 9, aperto per
   questa scena). Spostarla dentro il pannello.
6. **0–13 s · Aggancio.**
   - **Che cosa si vede.** Il titolo dice «drones on a collision course» e la domanda arriva a 9,9 s. Fino a 13 s,
     però, si vedono quattro o cinque tracce e cerchi sovrapposti, senza un evento leggibile.
   - **Che cosa capisce il giurato.** Che il tema è serio, ma non vede ancora il «non osservato ≠ libero», che arriva
     solo a 21–25 s.
   - **Correzione a tempo zero:** far comparire la riga «not observed ≠ clear» già sotto la domanda a 10–13 s. Il
     punto 7 del giurato v3 resta aperto solo in parte.
7. **~26–34 s · F1** (giurato v3, punto 5).
   - **Che cosa è fatto.** «with the core» c'è, e il quadro scrive «not observed ≠ clear».
   - **Che cosa manca.** Un istante in cui la croce del vero sta dentro una regione NOT SEEN. Nei fotogrammi 27, 30 e
     33 s non lo vedo (non verificato fra un fotogramma e l'altro).

Già a posto rispetto al giurato v3:
- la legenda delle aree piene, «filled: where it can be after an event · no probability» (punto 8);
- la riga di controllo, che dice in quale prova («false events in a 39 m near miss (F5) 2/60 · not adopted», punto
  12), con la sigla «(F5)» ancora da togliere;
- «The same approach works on a site» (punto 6).

## 3. Stati

| Enunciato a video | Stato proposto |
|---|---|
| F7r c1: avviso prima dei frammenti in 59/59, contro 0/59 | Sostenuto dai dati (simulazione, stessi semi), «strada promettente» |
| Riquadro LIMITS: «debris warning to the carrier not reliable» | Superato da c1: da correggere (C1) |
| La previsione è distinta dall'osservazione? | Sì: «computed in the model», «predicted close pass», «simulated run, log readout», «drawn for illustration» |
| Niente verde, niente lessico militare | Verificato sui 58 fotogrammi, non fra un fotogramma e l'altro |
| Etichetta su tutta la durata | Verificato sui 58 fotogrammi |

## 4. Proposta

**lettore-1: la riga di C1 è l'unico cambio indispensabile prima della consegna.**
- **Meccanismo:** elimina l'unica contraddizione interna fra scena e sintesi.
- **Previsione:** un lettore nuovo che vede la v3d non segnala contraddizioni su F7.
- **Smentita:** il lettore nuovo segnala ancora un'incoerenza su F7.

## 5. Dopo

1. Applicare C1 e C2, e se possibile C3, in una v3d accanto alla v3c, che resta.
2. Rifare ffprobe: la durata deve restare ≤ 176,0 s.
3. Far ascoltare l'audio della scena F7 a un lettore umano: è la parte che non ho verificato.
