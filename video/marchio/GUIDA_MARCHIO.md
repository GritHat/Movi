# Guida al marchio: SDMs e MoVi

Versione 2, 15 novembre 2026. Opera originale del gruppo SDMs (Ignazio Crocchiolo, Federico Dellini, Danilo Amalfitano, Emanuele Ciotola, Pierfrancesco Amendola).

## 1. L'idea

Il marchio ripete la regola del progetto: **ciò che si vede è pieno, ciò che non si vede è tratteggiato, e il segno resta**.

- **Simbolo SDMs.** A sinistra c'è un disco pieno ciano: l'oggetto visto, cioè con una misura adesso. A destra c'è una zona tratteggiata ambra con dentro un anello vuoto: l'oggetto non visto, di cui si dichiara una zona, con il segno che resta finché non si torna a guardare.
- **Marchio di parola MoVi.** La «o» è un anello tratteggiato ambra (ciò che non si vede). Il punto della «i» è un disco pieno ciano (ciò che si vede).
- Forme e colori sono gli stessi della grammatica degli stati del video: disco pieno ciano per «vista», anello e tratteggio ambra per «non vista». Il marchio e lo schermo parlano la stessa lingua. Anche senza colore lo stato si riconosce dalla forma (pieno contro tratteggiato), come chiede la regola «forma e parola prima del colore».

## 2. File

| File | Uso |
|---|---|
| `sdms_logo.svg` | Logo orizzontale (simbolo + «SDMs») a colori, per fondo scuro |
| `sdms_logo_mono.svg` | Lo stesso, tutto bianco #FFFFFF, per fondo scuro |
| `sdms_logo_mono_scuro.svg` | Lo stesso, tutto #0B0F17, per fondo chiaro |
| `sdms_simbolo.svg`, `sdms_simbolo_mono.svg`, `sdms_simbolo_mono_scuro.svg` | Il solo simbolo (icona, angolo dello schermo, avatar) |
| `movi_wordmark.svg` | Marchio di parola MoVi a colori, per fondo scuro |
| `movi_wordmark_mono.svg`, `movi_wordmark_mono_scuro.svg` | Le versioni monocrome, bianca e scura |
| `movi_wordmark*_v1.svg` | Versione 1 della «o» (6 tratti), conservata: a 64 px sembrava due punti. Non usarla |
| `tavola_controllo_v2.png` (e `_v1.png`) | Tavola di controllo: grandezze da 1080 px a 24 px, monocromi, spazio di rispetto, colori |

Gli SVG hanno il fondo trasparente, in modo da poterli sovrapporre nel video. Le lettere sono **tracciati**: per aprirli non serve nessun font. Il generatore è `.sciame/20261114-1301-percezione-challenge/f17-video/11-marketing/strumenti/genera_marchio.py` (fontTools 4.68.0, Inter SemiBold 4.1). La tavola si genera da `…/11-marketing/tavola/tavola_marchio_v2.html` con il Chrome locale di HyperFrames.

## 3. Costruzione

**Simbolo** (griglia 132 × 80 unità, con il centro del rigo a y = 40):

- Disco pieno: centro (30, 40), raggio 22.
- Zona tratteggiata: centro (94, 40), raggio 32, tratto 6, con 8 trattini pari al 60 % della circonferenza e le estremità tronche. I trattini cadono a ore 12, 3, 6 e 9.
- Anello vuoto: centro (94, 40), raggio 9,5, tratto 5.
- Distanza fra il disco e il bordo esterno della zona: 7 unità.

**Logo SDMs.** Simbolo, poi uno spazio di 30 unità, poi «SDMs» in Inter SemiBold a corpo 76: le maiuscole sono alte circa 55 unità, centrate otticamente sul simbolo. Ingombro: 380 × 84 unità.

**MoVi** (corpo 200, Inter SemiBold):

- La «o» è un anello che ha il diametro esterno e il centro della «o» di Inter. Lo spessore è 0,088 em (17,6 unità), un po' più sottile del tratto delle lettere, perché il tratteggio pesa come una lettera piena. Ha 8 trattini pari al 70 % della circonferenza.
- La «i» è una «ı» senza punto, con sopra un disco ciano grande 1,12 volte il punto originale.
- Crenatura «oV» ridotta a mano di 0,03 em, «Vi» di 0,01 em. Ingombro: 503 × 210 unità.

## 4. Colori

| Nome | Codice | Ruolo | Contrasto su #0B0F17 |
|---|---|---|---|
| Ciano «visto» | #3DD6E8 | disco pieno, punto della i | 10,9:1 |
| Ambra «non visto» | #F5A524 | zona tratteggiata, anello, «o» | 9,4:1 |
| Bianco testo | #E8EDF2 | lettere | 16,3:1 |
| Fondo | #0B0F17 | fondo di riferimento; colore del monocromo scuro | — |
| Bianco puro | #FFFFFF | monocromo chiaro | 19,2:1 |

I contrasti sono calcolati con la formula WCAG 2 della luminanza relativa e coincidono con quelli delle istruzioni del video. Le tinte (HSL) sono 186° per il ciano e 37° per l'ambra: nessuna cade nella fascia del verde (90°–160°) vietata dal controllo Q11. Su fondo chiaro il ciano dà solo 1,6:1 e l'ambra 1,9:1, quindi lì si usa il monocromo scuro (17,7:1 su #F4F6F8).

## 5. Spazio di rispetto e grandezze minime

- **Spazio di rispetto:** su ogni lato, almeno il raggio del disco del simbolo (22/80 dell'altezza del logo). Per MoVi vale il raggio del disco della «i» moltiplicato per 2,5 (circa 0,2 dell'altezza). Il riquadro tratteggiato della tavola lo mostra.
- **Grandezze minime:** logo SDMs alto 24 px; MoVi alto 32 px (a 24 px il tratteggio della «o» si impasta, come si vede sulla tavola); simbolo largo 32 px. A 64 px tutto si legge, controllato su due motori di disegno: Chrome 152 e librsvg (`rsvg-convert`).
- **Nel video:** il logo SDMs alto almeno 64 px nei titoli; MoVi largo 1080 px nel titolo d'apertura, oppure alto 48–64 px nell'angolo.

## 6. Usi vietati

- Cambiare i colori, invertire ciano e ambra (il pieno è sempre «visto») o aggiungere il verde, in qualunque parte.
- Riempire la «o» o il cerchio tratteggiato: il tratteggio è il significato del marchio.
- Mettere dentro la zona tratteggiata una sagoma o un oggetto: la regola 1 del disegno dell'incertezza lo vieta.
- Deformare, ruotare, aggiungere ombre, bagliori, sfumature o contorni.
- Usare la versione a colori su un fondo chiaro.
- Affiancare il marchio a loghi di terzi o a immagini d'ingaggio, puntamento o mirini. Il simbolo non è un mirino e non va animato come tale: niente croci, niente aggancio.
- Animare il disco «visto» in modo che sparisca senza che il segno tratteggiato resti.

## 7. Animazione consigliata (facoltativa, da dare al videomaker)

Durata 1,5 s. Il disco ciano entra pieno. Scorre a destra e, al posto del disco, compaiono la zona tratteggiata e l'anello vuoto (un tratto alla volta, nell'ordine orario). Poi il disco torna a sinistra. Il segno tratteggiato non sparisce mai durante l'animazione.

## 8. Licenza

- Il simbolo, il logo e il marchio di parola sono **opera originale del gruppo SDMs**, disegnati a mano in SVG senza immagini esterne né generatori. Il gruppo ne decide l'uso e ne tiene i diritti. Nessuna registrazione come marchio è stata fatta né verificata. Non è stata fatta una ricerca di anteriorità su marchi simili: **non verificato**.
- Le lettere vengono da **Inter 4.1**, Copyright (c) 2016 The Inter Project Authors, sotto SIL Open Font License 1.1 (testo in `…/00-strumenti/hyperframes/prova/assets/fonts/Inter-LICENSE-OFL.txt`). La OFL riguarda il software del font. Un logo con le lettere convertite in tracciati non è software del font e non ricade nei suoi obblighi: lettura nostra della licenza, non un parere legale.
