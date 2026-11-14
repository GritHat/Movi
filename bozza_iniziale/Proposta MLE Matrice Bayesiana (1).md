> Exported with **GPTAha Free**. [Remove watermark & unlock unlimited exports →](https://www.gptaha.com/pricing?utm_source=export_watermark)

# Proposta MLE Matrice Bayesiana

**User:**

Ciao chat, ascolta questa idea.
Dopo che l'hai ascoltata volevo proporre una miglioria, una matrice beyesiana avrebbe problemi riguardanti i pesi, per fare fine tuning si potrebbe sftuttare una stima maximum likelihood?

![WhatsApp Ptt 2026-11-06 at 17.47.49.ogg](gptaha-image://file_0000000056ec82108320fec5d4f34d3f)

---

**Assistant:**

L'idea è interessante e, soprattutto, **la tua proposta di utilizzare la Maximum Likelihood Estimation (MLE) è matematicamente sensata**, ma farei una distinzione importante: la MLE può servire a stimare i parametri del modello, mentre l'approccio bayesiano permette di incorporare conoscenze precedenti e aggiornare le probabilità quando arrivano nuove osservazioni.

Per il progetto degli occhiali intelligenti destinati a persone non vedenti, secondo me la soluzione migliore sarebbe **una mappa probabilistica dinamica, con parametri stimati tramite MLE o MAP**.

Ti spiego come la strutturerei.

## 1. Il problema della matrice bayesiana

Nell'audio viene proposta una matrice bidimensionale o tridimensionale che rappresenta l'ambiente circostante.

Invece di memorizzare semplicemente:

- `0` = spazio libero
- `1` = ostacolo

Ogni cella potrebbe contenere una probabilità:

\[
M_{ij}=P(O_{ij}=1\mid Z_{1:t})
\]

dove \(O_{ij}\) indica la presenza di un ostacolo e \(Z_{1:t}\) rappresenta le osservazioni raccolte fino all'istante \(t\).

Questo approccio è già noto in robotica come **Occupancy Grid Mapping**.

Il problema è che la probabilità di occupazione non basta a descrivere se un ostacolo sia pericoloso.

Un muro e una persona possono entrambi avere una probabilità di occupazione del 99%, ma richiedere comportamenti differenti.

Servono quindi altre informazioni, come la velocità dell'oggetto, la sua classe e la probabilità che attraversi il percorso dell'utente.

## 2. Dove entra in gioco la Maximum Likelihood Estimation?

La tua intuizione è utilizzare i dati osservati per ottimizzare i pesi del modello, anziché assegnarli manualmente.

Supponiamo di avere un modello che stima la probabilità che un oggetto si muova nei prossimi due secondi.

Potremmo definire:

\[
P(Y=1\mid X;\theta)
\]

dove:

- \(Y=1\) significa che l'oggetto si muoverà.
- \(X\) contiene classe dell'oggetto, velocità osservata e altre caratteristiche.
- \(\theta\) rappresenta i parametri da stimare.

Raccogliendo un dataset di osservazioni, possiamo stimare:

\[
\boxed{
\hat{\theta}_{MLE}
=
\arg\max_\theta
\prod_{i=1}^{N}
P(y_i\mid x_i;\theta)
}
\]

In questo modo, i pesi vengono appresi dai dati.

Per esempio, il modello potrebbe imparare che una bicicletta in movimento ha una probabilità elevata di cambiare posizione, mentre un muro ha una probabilità praticamente nulla.

**Attenzione però:** la MLE non garantisce automaticamente una buona generalizzazione, soprattutto con pochi dati o classi rare.

## 3. Perché utilizzerei MAP invece della sola MLE

Qui arriva la parte che trovo più interessante.

La Maximum A Posteriori Estimation (MAP) combina la likelihood dei dati con una distribuzione a priori sui parametri.

\[
\boxed{
\hat{\theta}_{MAP}
=
\arg\max_\theta
\left[
\log P(D\mid\theta)
+
\log P(\theta)
\right]
}
\]

Questo permette di incorporare conoscenze precedenti.

Per esempio, possiamo assegnare inizialmente una forte preferenza a modelli che considerano i muri statici, senza impedire al sistema di apprendere dai dati.

<box border radius="xl" padding={3} gap={2}>
  <text weight="medium" size="sm">Architettura che proporrei</text>
  <box background="surface-secondary" radius="lg" padding={3} align="center">
    **Sensori e telecamera**

    <caption>Profondità, immagini, movimento</caption>
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="surface-secondary" radius="lg" padding={3} align="center">
    **Riconoscimento e tracking**

    <caption>Classificazione degli oggetti e stima delle traiettorie</caption>
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="rgba(38,115,180,0.08)" border={{size:1,color:"info"}} radius="lg" padding={3} align="center">
    **Mappa probabilistica dinamica**

    <caption>Occupazione, velocità, incertezza, rischio</caption>
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="surface-secondary" radius="lg" padding={3} align="center">
    **Predizione e pianificazione**

    <caption>Stima del rischio di collisione lungo il percorso</caption>
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="surface-secondary" radius="lg" padding={3} align="center">
    **Feedback vocale o aptico**

    <caption>Segnalazione degli ostacoli e indicazioni di movimento</caption>
  </box>
</box>

## 4. Un miglioramento ulteriore: stimare il rischio, non soltanto il movimento

Secondo me, questa sarebbe la vera evoluzione dell'idea originale.

Una persona ferma davanti all'utente potrebbe essere più pericolosa di una bicicletta che si sta allontanando.

Quindi, anziché usare soltanto:

\[
P(\text{oggetto mobile})
\]

stimerei:

\[
P(\text{collisione entro }T\mid \text{osservazioni})
\]

Tenendo conto di posizione, velocità relativa, direzione e incertezza della previsione.

<grid columns={2} gap={3}>
  <grid-item>
    <box gap={1}>
      <AsyncImage query="pedestrian walking on sidewalk urban street daytime" aspectRatio="5:4"/>
      <text weight="medium" size="sm">Persona in movimento</text>
      <caption>Potenzialmente rischiosa se attraversa la traiettoria</caption>
    </box>
  </grid-item>
  <grid-item>
    <box gap={1}>
      <AsyncImage query="concrete wall along empty sidewalk pedestrian perspective" aspectRatio="5:4"/>
      <text weight="medium" size="sm">Ostacolo statico</text>
      <caption>Rischio dipendente dalla distanza e dal percorso</caption>
    </box>
  </grid-item>
</grid>

## 5. MLE, MAP oppure apprendimento online?

| Metodo | Vantaggio | Limite |
|---|---|---|
| MLE | Impara i parametri dai dati | Può sovradattarsi |
| MAP | Integra dati e conoscenze precedenti | Richiede prior adeguate |
| Aggiornamento bayesiano online | Aggiorna le probabilità con nuove osservazioni | Dipende dal modello e dalla qualità dei sensori |

Questi metodi non sono necessariamente alternativi: potresti usare MAP per addestrare i parametri e un filtro bayesiano per aggiornare continuamente lo stato degli ostacoli.

Inoltre, non confonderei l'aggiornamento online delle probabilità con il riaddestramento online dei pesi: sono due operazioni diverse.

## 6. La mia valutazione della tua proposta

La modifica che suggerisci è valida, ma la formulerei così:

**Utilizzare una Occupancy Grid dinamica, integrata con un modello probabilistico di previsione del movimento, i cui parametri siano stimati mediante Maximum Likelihood o Maximum A Posteriori.**

Per un dispositivo assistivo reale, aggiungerei un sistema conservativo di gestione dell'incertezza: se il riconoscimento non è affidabile, il sistema non deve presumere che il percorso sia libero. La sicurezza andrebbe poi verificata con test controllati prima di qualsiasi utilizzo come ausilio alla mobilità.

C'è però una domanda tecnica che farei al tuo amico, perché cambia radicalmente l'architettura:

**Gli occhiali utilizzeranno soltanto una telecamera RGB oppure anche un sensore di profondità, come uno stereo camera o un ToF?**

Perché con una sola telecamera il problema principale potrebbe non essere l'ottimizzazione dei pesi, ma la stima affidabile delle distanze e del movimento tridimensionale.

---

**User:**

quindi sostanzialmente è l'idea dell'audio? Qual è la differenza?

---

**Assistant:**

Sì, **sostanzialmente è la stessa idea dell'audio**, ma con una differenza importante: nell'audio viene proposta una rappresentazione probabilistica dell'ambiente, mentre tu proponi **un metodo per apprendere e ottimizzare i parametri di quel modello**.

La tua proposta non sostituisce quella originale: la completa.

## Le differenze principali

| Aspetto | Idea dell'audio | Tua proposta con MLE |
|---|---|---|
| Rappresentazione | Matrice probabilistica bayesiana | Stessa matrice |
| Probabilità | Associate agli oggetti e alla loro mobilità | Stimate attraverso dati osservati |
| Pesi | Metodo di determinazione non specificato | Parametri ottimizzati mediante MLE |
| Apprendimento | Non esplicitato | Apprendimento statistico dai dati |
| Adattamento | Aggiornamento probabilistico ipotizzato | Possibilità di riaddestrare i parametri |

### Un esempio concreto

Nell'audio il tuo amico propone:

- Muro: probabilità di movimento 1%.
- Persona: probabilità di movimento 70%.
- Bicicletta: probabilità di movimento 85%.

Ma **come vengono determinate queste probabilità?**

È qui che entra la tua idea.

Con la Maximum Likelihood Estimation, raccogli un dataset di osservazioni e stimi i parametri che massimizzano la probabilità dei dati.

Per esempio, se osservi 1.000 persone e 650 si muovono nell'intervallo temporale considerato, in un modello Bernoulli molto semplice ottieni:

\[
\hat p_{MLE}=\frac{650}{1000}=0.65
\]

Quindi il 65% non è più un valore scelto arbitrariamente, ma una stima statistica.

Naturalmente, in un sistema reale servirebbe un modello più complesso, che tenga conto anche della velocità, della direzione e del contesto.

## Ma c'è una precisazione fondamentale

**Una matrice bayesiana non implica necessariamente che i pesi siano assegnati manualmente.**

L'aggiornamento bayesiano e la MLE risolvono problemi differenti:

- **Inferenza bayesiana:** aggiorna ciò che il sistema crede sullo stato dell'ambiente, date nuove osservazioni.
- **MLE:** stima i parametri del modello probabilistico a partire dai dati.

Quindi il tuo amico potrebbe già prevedere implicitamente un apprendimento dei parametri, anche se non lo specifica nell'audio.

Inoltre, non è necessario usare MLE per ogni cella della matrice: puoi stimare i parametri di un modello condiviso che descrive il comportamento degli oggetti.

## La vera miglioria che proporrei

Io suggerirei di passare da:

\[
P(\text{oggetto in movimento})
\]

a:

\[
\boxed{P(\text{collisione entro }T\mid X)}
\]

Dove \(X\) include distanza, velocità relativa, traiettoria, classe dell'oggetto e incertezza delle misurazioni.

I parametri di questo modello potrebbero essere appresi mediante MLE oppure MAP.

Questo rappresenterebbe un miglioramento più sostanziale rispetto alla sola introduzione della MLE, perché **non stai soltanto migliorando la stima delle probabilità: stai cambiando ciò che il sistema cerca di prevedere**.

In sintesi: **la tua MLE è un'ottima proposta per rendere quantitativamente fondata l'idea dell'audio, ma non costituisce da sola una nuova architettura.** La vera evoluzione sarebbe combinare mappatura bayesiana, stima dei parametri e predizione del rischio di collisione.

---

**User:**

Pensa bene a come potresti migliorare questa idea.

---

**Assistant:**

Voglio valutare l’idea come un vero sistema di navigazione assistiva: capire dove la matrice probabilistica funziona, dove rischia di fallire e quale architettura sarebbe più utile, leggera e sicura. Verificherò anche le soluzioni già studiate in robotica, per distinguere i miglioramenti concreti da quelli solo teorici.

---

**Assistant:**

Il punto decisivo che emerge è questo: assegnare a un oggetto una probabilità di muoversi non basta per decidere se l’utente rischia di urtarlo. La miglioria più forte sarebbe separare la mappa degli ostacoli dalla previsione delle loro traiettorie, e usare entrambe per stimare il rischio nei prossimi secondi. Sto anche distinguendo ciò che conviene implementare davvero da ciò che renderebbe il sistema inutilmente pesante.

---

**Assistant:**

Ho approfondito l'idea confrontandola con gli approcci utilizzati nella robotica autonoma, nella computer vision e nei sistemi assistivi per persone non vedenti.

Credo che ci sia un modo per migliorarla sensibilmente, **sia dal punto di vista matematico sia da quello computazionale**, senza dover utilizzare un modello di intelligenza artificiale enorme.

La mia proposta sarebbe sviluppare un sistema che chiamerei:

**Adaptive Spatio-Temporal Risk Mapping**

Una mappa probabilistica spazio-temporale capace non soltanto di riconoscere gli ostacoli, ma anche di prevedere dove potrebbero trovarsi nei prossimi secondi e valutare il rischio per la persona.

Il nome è descrittivo, non quello di un algoritmo nuovo: esistono già ricerche sulle *Spatio-Temporal Occupancy Grid Maps* e sulle mappe di rischio dinamiche. Questo significa che abbiamo una solida base scientifica dalla quale partire. <Cite refs={["turn676818search6","turn343496search8"]}/>

## 1. Il problema fondamentale dell'idea originale

Nell'audio il ragionamento è:

> Riconosco un oggetto, gli assegno una probabilità di movimento e utilizzo questa informazione per comprendere quanto sia sicuro l'ambiente.

Il limite è che **la probabilità che un oggetto si muova non equivale alla probabilità che quell'oggetto rappresenti un pericolo**.

Considera tre situazioni:

| Situazione | Probabilità di movimento | Rischio per l'utente |
|---|---|---|
| Muro davanti alla persona | Quasi nulla | Alto, se la persona continua a camminare |
| Bicicletta che si allontana | Alta | Potenzialmente basso |
| Persona che attraversa il percorso | Alta | Potenzialmente alto |

Il modello proposto nell'audio considera soprattutto le caratteristiche degli oggetti.

Io introdurrei anche **la relazione tra il movimento degli oggetti e il movimento dell'utente**.

La domanda del sistema diventerebbe:

*Se continuo a camminare in questa direzione, qual è la probabilità che il mio corpo e un ostacolo occupino lo stesso spazio nei prossimi due secondi?*

Questa è una previsione molto più utile per un dispositivo di navigazione assistiva.

## 2. La modifica architetturale: non una matrice, ma tre livelli di informazione

Anziché creare un'unica matrice bayesiana contenente tutti i dati, dividerei il sistema in tre componenti logiche.

<box border radius="xl" padding={3} gap={2}>
  <box background="surface-secondary" radius="lg" padding={3} align="center" gap={1}>
    <text weight="medium">Livello 1 — Mappa geometrica</text>
    <text color="secondary" size="xs" textAlign="center">Dove si trovano gli ostacoli? Quali spazi sono liberi o sconosciuti?</text>
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="surface-secondary" radius="lg" padding={3} align="center" gap={1}>
    <text weight="medium">Livello 2 — Modello dinamico</text>
    <text color="secondary" size="xs" textAlign="center">Come si muovono gli oggetti? Quali sono le traiettorie possibili?</text>
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="rgba(37,99,235,0.07)" border radius="lg" padding={3} align="center" gap={1}>
    <text weight="medium">Livello 3 — Mappa predittiva del rischio</text>
    <text color="secondary" size="xs" textAlign="center">Quali zone diventerebbero pericolose seguendo un determinato percorso?</text>
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="surface-secondary" radius="lg" padding={3} align="center" gap={1}>
    <text weight="medium">Sistema di feedback</text>
    <text color="secondary" size="xs" textAlign="center">Avvisi aptici o vocali, in base a urgenza e affidabilità</text>
  </box>
</box>

### Livello 1 — Occupancy Grid bayesiana

Qui manterrei l'idea del tuo amico.

Ogni cella rappresenta la probabilità che una determinata porzione di spazio sia occupata:

\[
P(O_{ij}=1\mid Z_{1:t})
\]

Per aggiornare queste probabilità utilizzerei la rappresentazione in **log-odds**:

\[
L_{t,i}=L_{t-1,i}+
\log\frac{p_{t,i}}{1-p_{t,i}}-L_{0,i}
\]

Dove \(p_{t,i}\) è la probabilità di occupazione fornita dal modello inverso del sensore per la nuova osservazione.

È particolarmente interessante perché gli aggiornamenti diventano addizioni, evitando di moltiplicare ripetutamente probabilità. È una tecnica consolidata nell'Occupancy Grid Mapping. <Cite refs={["turn343496search0","turn343496search1"]}/>

**Un miglioramento ulteriore:** distinguere obbligatoriamente tre stati: libero, occupato e sconosciuto. Una cella che la telecamera non riesce a vedere non deve essere considerata libera.

### Livello 2 — Predizione dinamica

Qui invece cambierei profondamente il ragionamento dell'audio.

Non attribuirei semplicemente a ogni classe di oggetti un peso fisso.

Per ogni oggetto tracciato manterrei uno stato:

\[
S_k=(x,y,v_x,v_y,\Sigma,c)
\]

Dove:

- \(x,y\): posizione.
- \(v_x,v_y\): velocità stimata.
- \(\Sigma\): matrice di covarianza, che quantifica l'incertezza della stima.
- \(c\): classe dell'oggetto, come persona o bicicletta.

Inizialmente utilizzerei un **filtro di Kalman**, con un modello di movimento semplice.

Se una persona sta camminando, il sistema potrebbe stimarne la posizione dopo un intervallo \(\Delta t\):

\[
\hat{\mathbf p}_{t+\Delta t}
=
\hat{\mathbf p}_t+\hat{\mathbf v}_t\Delta t
\]

E propagherebbe anche l'incertezza della posizione futura.

Questo permette di prevedere non soltanto un punto, ma una regione nella quale l'oggetto potrebbe trovarsi.

Una precisazione fondamentale: bisogna compensare il movimento della telecamera. Se l'utente cammina verso un muro, il muro cambia posizione nell'immagine, ma non sta realmente camminando.

### Livello 3 — Predizione del rischio

Qui introdurrei la parte più interessante del progetto.

La matrice non descriverebbe solamente l'ambiente attuale, ma anche la sua evoluzione.

Possiamo rappresentarla concettualmente come:

\[
M(x,y,t+\Delta t)
\]

In pratica, il sistema valuta più istanti futuri.

<box border radius="xl" padding={3} gap={2}>
  <text weight="medium" size="sm">Esempio di mappa predittiva</text>
  <caption>Scenario ipotetico: una persona attraversa il percorso dell'utente da destra verso sinistra.</caption>
  {@body const scenes=[{label:"Adesso",people:[[5,1]],risk:[[5,1]]},{label:"Tra 1 s",people:[[4,2]],risk:[[4,2],[4,3]]},{label:"Tra 2 s",people:[[3,3]],risk:[[3,3],[3,4]]}]}
  {@body const [frame,setFrame]=DIL.useState(0)}
  <segmented-control size="md" block value={String(frame)} onChange={v=>setFrame(Number(v))} options={[{"label":"Adesso","value":"0"},{"label":"+1 s","value":"1"},{"label":"+2 s","value":"2"}]}/>
  <box background="#131B28" theme="dark" padding={3} radius="lg">
    <svg viewBox="0 0 330 240" width="100%" xmlns="http://www.w3.org/2000/svg">
      {#each Array.from({length:7},(_,r)=>r) as r}
        {#each Array.from({length:9},(_,c)=>c) as c}
          <rect x={16+c*33} y={10+r*29} width="30" height="26" rx="3" fill={c===1||c===7?"#465568":c===4?"#244A40":"#273241"} stroke="#4B5767" strokeWidth=".65"/>
        {/each}
      {/each}
      <path d="M164 194 L164 29" stroke="#5ED9A0" strokeWidth="2.5" strokeDasharray="5 5"/>
      <path d="M159 37 L164 27 L169 37" stroke="#5ED9A0" strokeWidth="2" fill="none"/>
      {#each scenes[frame].risk as p}
        <rect x={16+p[0]*33} y={10+p[1]*29} width="30" height="26" rx="3" fill="#D68B32" opacity=".7"/>
      {/each}
      {#each scenes[frame].people as p}
        <circle cx={31+p[0]*33} cy={23+p[1]*29} r="10" fill="#EF6464" stroke="#FFB9B9" strokeWidth="2"/>
      {/each}
      <circle cx="164" cy="192" r="10" fill="#5ED9A0" stroke="#DAFFEC" strokeWidth="2"/>
      <text x="164" y="195" fontSize="8" fill="#07392C" textAnchor="middle" fontWeight="bold">U</text>
      <text x="164" y="228" fontSize="10" fill="#D7E1EB" textAnchor="middle">Direzione ipotizzata di marcia ↑</text>
    </svg>
    <row justify="between" align="center" wrap="wrap">
      <row align="center" gap={1}><box background="#5ED9A0" size="10px" radius="sm"/><text size="2xs">Utente</text></row>
      <row align="center" gap={1}><box background="#EF6464" size="10px" radius="sm"/><text size="2xs">Persona</text></row>
      <row align="center" gap={1}><box background="#D68B32" size="10px" radius="sm"/><text size="2xs">Zona di attenzione</text></row>
    </row>
  </box>
  <caption>Schema illustrativo, non risultato di una simulazione fisica. Cambia l'istante per vedere come si sposta l'area di attenzione.</caption>
</box>

Formalmente, si potrebbe cercare di stimare:

\[
\boxed{
R(\pi)=P\left(
\exists \tau\in[0,T]:
B_u(\pi,\tau)\cap O(\tau)\neq\varnothing
\mid Z_{1:t}
\right)
}
\]

Dove \(\pi\) rappresenta un possibile percorso, \(B_u\) lo spazio occupato dal corpo dell'utente e \(O\) quello degli ostacoli.

Per calcolarlo in tempo reale si possono usare approssimazioni basate sulle traiettorie previste, sulle covarianze e sul tempo alla collisione (*Time to Collision*).

Il vantaggio è sostanziale: il sistema potrebbe segnalare un ostacolo **prima che entri effettivamente nel percorso immediato dell'utente**.

---

## 3. Miglioramento computazionale: utilizzerei una rappresentazione 2.5D

Secondo me, sviluppare una matrice tridimensionale completa, come ipotizzato nell'audio, non è necessariamente la scelta migliore per un dispositivo indossabile.

Un ambiente 3D è certamente utile, ma memorizzare continuamente ogni voxel può diventare costoso.

Proporrei una **mappa locale 2.5D**, nella quale ogni posizione orizzontale contiene informazioni verticali essenziali.

<box border radius="lg" padding={3} gap={2}>
  <row align="start" gap={3}>
    <box background="surface-secondary" radius="lg" padding={2} justify="center" align="center">
      <icon name="footprints" size="lg"/>
    </box>
    <box flex="1" gap={1}>
      **Livello inferiore — Piedi**

      <text color="secondary" size="sm">Gradini, buche, dislivelli, ostacoli a terra.</text>
    </box>
  </row>
  <divider color="subtle"/>
  <row align="start" gap={3}>
    <box background="surface-secondary" radius="lg" padding={2} justify="center" align="center">
      <icon name="person-standing" size="lg"/>
    </box>
    <box flex="1" gap={1}>
      **Livello intermedio — Corpo**

      <text color="secondary" size="sm">Persone, biciclette, tavoli, ostacoli all'altezza del busto.</text>
    </box>
  </row>
  <divider color="subtle"/>
  <row align="start" gap={3}>
    <box background="surface-secondary" radius="lg" padding={2} justify="center" align="center">
      <icon name="scan-face" size="lg"/>
    </box>
    <box flex="1" gap={1}>
      **Livello superiore — Testa**

      <text color="secondary" size="sm">Rami, cartelli sporgenti, ostacoli sospesi.</text>
    </box>
  </row>
</box>

Questa è una semplificazione: non bisogna perdere la geometria degli ostacoli che attraversano più livelli e serve una rilevazione specifica dei dislivelli negativi. Le sole telecamere frontali potrebbero non essere sufficienti a individuare in modo affidabile buche o gradini in discesa.

Soluzioni di navigazione robotica come Nav2 utilizzano già costmap bidimensionali con informazioni provenienti da sensori 3D, quindi il principio è applicabile. <Cite refs={["turn752659search2","turn752659search5"]}/>

Per rendere il sistema ancora più leggero, terrei le traiettorie degli oggetti mobili in una struttura separata, senza duplicarle in tutte le celle della matrice.

## 4. La tua MLE: la userei, ma in un punto preciso

Qui arriviamo alla tua proposta iniziale.

Io **non userei MLE per cercare di ottimizzare direttamente tutta la matrice di occupazione**.

La utilizzerei per stimare i parametri del modello dinamico e, eventualmente, del modello di misura dei sensori.

Per esempio, definirei un modello:

\[
p_\theta(\mathbf v_{t+\Delta t}\mid X_t)
\]

Che rappresenta una distribuzione delle velocità future, condizionata alle caratteristiche osservate.

Stimerei quindi:

\[
\hat\theta =
\arg\max_\theta
\sum_{i=1}^{N}
\log p_\theta(y_i\mid X_i)
\]

Questo potrebbe permettere al modello di apprendere comportamenti differenti in contesti differenti.

Per esempio, una persona che cammina in un corridoio stretto potrebbe avere un comportamento predicibile diverso da una che si trova in una piazza affollata.

Non trascurerei però la MAP:

\[
\hat\theta_{MAP}=
\arg\max_\theta
\left[
\log P(D\mid\theta)+\log P(\theta)
\right]
\]

La preferirei quando il dataset è limitato o abbiamo conoscenze precedenti affidabili da incorporare.

**La soluzione che sceglierei è ibrida:** stimare offline i parametri mediante MLE o MAP, poi utilizzare filtri probabilistici online per aggiornare continuamente posizione e velocità degli ostacoli.

Non farei invece riaddestrare liberamente i pesi mentre una persona utilizza il dispositivo: aggiornare le stime dello stato è utile, ma cambiare un modello di sicurezza sul campo senza validazione introduce rischi.

## 5. Un problema sottovalutato: la posizione della testa non è la direzione del movimento

Gli occhiali sono montati sulla testa.

Ma una persona può camminare in avanti mentre guarda a destra.

Se il sistema utilizzasse soltanto l'orientamento della telecamera, potrebbe confondere il campo visivo con la traiettoria futura del corpo.

Per correggerlo, introdurrei una stima del moto dell'utente mediante sensori inerziali e visual odometry, tenendo conto della differenza tra movimento della testa e spostamento effettivo.

Questo è fondamentale anche per stimare correttamente la velocità degli ostacoli.

Un muro immobile, infatti, sembra avvicinarsi rapidamente quando camminiamo verso di esso.

## 6. Un'altra miglioria: feedback intelligente invece di notifiche continue

Il sistema non dovrebbe descrivere continuamente ogni oggetto riconosciuto.

Sarebbe faticoso e potrebbe interferire con l'ascolto dell'ambiente.

Progetterei due modalità di feedback complementari: vibrazioni direzionali per gli avvisi ordinari e brevi messaggi vocali per situazioni più complesse. La frequenza delle segnalazioni dovrebbe dipendere dall'urgenza, con meccanismi che evitino continui cambi di indicazione.

Soprattutto, distinguerei tra *percorso apparentemente libero* e *percorso verificato sufficientemente*: il sistema deve comunicare quando non riesce a interpretare la scena con affidabilità.

La ricerca sull'accessibilità conferma l'importanza di una progettazione guidata dagli utenti reali. Uno studio del 2026, pubblicato su *Nature Biomedical Engineering*, ha valutato un'applicazione con sensor fusion e audio personalizzato insieme al bastone bianco, osservando una riduzione dei contatti con l'ambiente nei percorsi studiati. <Cite refs={["turn676818search2","turn676818search4"]}/>

## 7. Come lo svilupperei concretamente

Proporrei una progressione in quattro fasi, evitando di introdurre subito machine learning predittivo e mappatura tridimensionale complessa.

| Fase | Implementazione | Obiettivo |
|---|---|---|
| MVP 1 | Sensore RGB-D, IMU, mappa locale 2.5D e ostacoli statici | Valutare la rilevazione e il posizionamento degli ostacoli |
| MVP 2 | Object tracking, filtro di Kalman e compensazione del moto | Distinguere il movimento dell'utente da quello degli oggetti |
| MVP 3 | Predizione delle traiettorie e risk map | Generare avvisi anticipati e contestuali |
| MVP 4 | Modello predittivo calibrato tramite MLE/MAP e feedback personalizzato | Migliorare le prestazioni rispetto alle versioni precedenti |

Partirei da un sensore di profondità e una IMU, con elaborazione locale su smartphone o dispositivo dedicato. La fattibilità dipenderà molto da consumo energetico, latenza, peso e comportamento dei sensori alla luce solare, con superfici riflettenti o in condizioni di scarsa visibilità.

Per misurare il successo, non utilizzerei soltanto l'accuratezza della classificazione. Valuterei principalmente i pericoli non rilevati, i falsi allarmi, l'anticipo delle segnalazioni, la calibrazione delle probabilità, la latenza e l'effettiva utilità del feedback per persone non vedenti.

I test iniziali dovrebbero avvenire in ambienti controllati, con supervisione, senza considerare il prototipo un sostituto del bastone bianco.

## 8. Quanto sarebbe originale questa soluzione?

Una considerazione importante: **né le matrici bayesiane né la predizione dinamica del rischio sono concetti nuovi**.

Sono già presenti in sistemi di navigazione robotica e in diverse pubblicazioni, incluse ricerche su mappe probabilistiche spazio-temporali. <Cite refs={["turn676818search6","turn676818academia36"]}/>

E anche il parallelismo con Doom va interpretato correttamente. Il Doom originale utilizzava una rappresentazione 2.5D, organizzata in settori, con ottimizzazioni per il rendering e la visibilità. Non doveva acquisire e interpretare il mondo reale attraverso sensori: il fatto che Doom possa funzionare su hardware molto modesto non implica che un sistema di computer vision abbia lo stesso costo computazionale. <Cite refs={["turn312306search1","turn312306search4"]}/>

Per rendere il progetto tecnicamente distintivo, punterei sull'**adattamento delle mappe dinamiche alla navigazione umana**, dove la traiettoria non è controllata da un robot ma dipende dai movimenti dell'utente, e dove la priorità è minimizzare sia il rischio sia il carico cognitivo.

---

## La proposta che porterei al tuo amico

Non proporrei di migliorare semplicemente i pesi della sua matrice.

Proporrei di **mantenere la matrice bayesiana come rappresentazione geometrica e aggiungere un secondo modello probabilistico capace di prevedere l'interazione futura tra utente e ostacoli**.

Il sistema potrebbe quindi avere queste tre quantità fondamentali:

\[
\underbrace{P(O\mid Z)}_{\text{Occupazione}}
\qquad
\underbrace{P(V_{\text{futura}}\mid X)}_{\text{Movimento}}
\qquad
\underbrace{P(C\mid Z,\pi)}_{\text{Collisione}}
\]

Sono tre probabilità diverse, con tre significati diversi.

La prima dice dove si trova qualcosa, la seconda come potrebbe muoversi e la terza quanto il movimento dell'utente potrebbe diventare pericoloso.

**È la terza probabilità che dovrebbe guidare le segnalazioni degli occhiali.**

E qui la tua idea della Maximum Likelihood acquista davvero valore: puoi utilizzarla per stimare dai dati i parametri che governano il modello di movimento, mentre il filtro bayesiano gestisce l'incertezza che evolve nel tempo.

Se dovessi scegliere un singolo contributo da approfondire anche in chiave di ricerca universitaria, sceglierei **la previsione del rischio di collisione a breve termine, con incertezza esplicita, utilizzando una mappa 2.5D e modelli dinamici leggeri**. È un problema sufficientemente circoscritto da permettere esperimenti rigorosi, ma abbastanza complesso da offrire spazio per miglioramenti misurabili.

---

**User:**

riassumi il tutto in modo che possa mandare su what'sapp quest'ultima parte di miglioramento

---

**Assistant:**

<WritingBlock id="58321" variant="chat_message">Ho ragionato un po' sulla tua idea della matrice bayesiana e secondo me si potrebbe migliorare parecchio, mantenendo comunque il sistema leggero.

Il punto principale è che **la probabilità che un oggetto si muova non coincide necessariamente con la probabilità che sia pericoloso**. Ad esempio, una bicicletta che si allontana è meno pericolosa di un muro fermo davanti a noi.

Io proporrei quindi un'architettura composta da tre livelli:

1. **Mappa geometrica bayesiana:** mantiene la tua idea originale, rappresentando l'ambiente tramite celle con probabilità di occupazione.
2. **Modello dinamico:** tramite object tracking e filtri di Kalman, stima posizione, velocità e traiettoria futura degli oggetti, considerando anche l'incertezza delle misurazioni.
3. **Mappa predittiva del rischio:** combina le informazioni precedenti con il movimento dell'utente per stimare la probabilità di collisione nei prossimi secondi.

Per quanto riguarda la matrice, utilizzerei una rappresentazione **2.5D anziché completamente 3D**, mantenendo informazioni sull'altezza degli ostacoli (piedi, corpo, testa). Questo potrebbe ridurre il costo computazionale.

Inoltre, per ottimizzare i parametri del modello dinamico, pensavo di utilizzare la **Maximum Likelihood Estimation (MLE)** oppure la **Maximum A Posteriori (MAP)**. In questo modo, anziché assegnare manualmente probabilità di movimento alle varie classi di oggetti, potremmo stimarle attraverso dati reali, tenendo conto anche del contesto.

La cosa interessante sarebbe combinare:
- P(occupazione): probabilità che una zona sia occupata.
- P(movimento): probabilità delle possibili traiettorie future.
- P(collisione): probabilità che un ostacolo interferisca con il percorso dell'utente.

**L'obiettivo finale sarebbe passare da un sistema che riconosce gli ostacoli a uno che anticipa i potenziali pericoli.**

Per mantenerlo leggero, potremmo utilizzare modelli probabilistici relativamente semplici, senza dover necessariamente ricorrere a reti neurali enormi. Bisognerebbe inoltre compensare il movimento della testa rispetto a quello del corpo, magari tramite IMU, e prevedere un feedback aptico o vocale soltanto quando necessario.

Ovviamente questi approcci esistono già in robotica, ma sarebbe interessante adattarli a un dispositivo indossabile per persone non vedenti, ottimizzando soprattutto latenza, consumo energetico e affidabilità.</WritingBlock>

---

**User:**

Rendi più chiaro il calcolo del rischio

---

**Assistant:**

<WritingBlock id="58321" variant="chat_message">Ho ragionato un po' sulla tua idea della matrice bayesiana e secondo me si potrebbe migliorare parecchio, mantenendo comunque il sistema leggero.

Il punto principale è che **la probabilità che un oggetto si muova non coincide necessariamente con la probabilità che sia pericoloso**. Ad esempio, una bicicletta che si allontana è meno pericolosa di un muro fermo davanti a noi.

Io proporrei quindi un'architettura composta da tre livelli:

**1. Mappa geometrica bayesiana**

Manteniamo la tua idea originale: una matrice in cui ogni cella rappresenta una porzione dell'ambiente e contiene la probabilità che sia occupata da un ostacolo.

**2. Modello dinamico**

Tramite object tracking e filtri di Kalman, stimiamo posizione, velocità e direzione degli oggetti, cercando di prevedere dove potrebbero trovarsi nei prossimi secondi.

Per stimare i parametri del modello, potremmo utilizzare la *Maximum Likelihood Estimation (MLE)* oppure la *Maximum A Posteriori (MAP)*, apprendendo dai dati anziché assegnare manualmente i pesi.

**3. Mappa predittiva del rischio**

Questa secondo me sarebbe la miglioria più importante.

Invece di calcolare semplicemente la probabilità che un oggetto si muova, calcoliamo **la probabilità che la traiettoria futura dell'oggetto intersechi quella dell'utente entro un certo intervallo temporale**, ad esempio 2 secondi.

Il procedimento sarebbe:

- Stimiamo posizione, velocità e direzione dell'utente.
- Stimiamo posizione, velocità e direzione degli ostacoli.
- Prevediamo le possibili posizioni future di entrambi, considerando l'incertezza delle stime.
- Calcoliamo la probabilità che le rispettive aree occupate si sovrappongano nello stesso istante.

Ad esempio, immaginiamo una persona che cammina trasversalmente davanti all'utente.

Se il modello prevede che tra 1,5 secondi entrambi potrebbero trovarsi nello stesso punto, il rischio aumenta. Se invece la persona si sta allontanando, il rischio diminuisce, anche se la sua probabilità di movimento rimane elevata.

Matematicamente, vogliamo stimare:

**P(collisione entro T | osservazioni e traiettoria dell'utente)**

Questa probabilità potrebbe essere calcolata utilizzando le distribuzioni delle posizioni future stimate dal filtro di Kalman, verificando quanto è probabile che le aree occupate dai due soggetti si sovrappongano.

Per gli ostacoli statici, come i muri, il ragionamento è analogo: la loro posizione futura rimane sostanzialmente invariata, ma il rischio cresce se la traiettoria dell'utente li attraversa.

Inoltre, potremmo considerare anche il *Time to Collision (TTC)*, cioè il tempo stimato prima di un eventuale impatto, per stabilire quanto urgentemente avvisare l'utente.

**Ottimizzazione computazionale**

Per mantenere il sistema leggero, utilizzerei una rappresentazione **2.5D anziché completamente 3D**, conservando le informazioni essenziali sull'altezza degli ostacoli (piedi, corpo e testa).

Utilizzerei inoltre una IMU per distinguere il movimento della testa da quello effettivo dell'utente, evitando errori nella previsione delle traiettorie.

In sostanza, avremmo tre informazioni fondamentali:

- **P(occupazione):** quanto è probabile che una zona sia occupata.
- **P(movimento):** come potrebbe evolvere la posizione di un oggetto.
- **P(collisione):** quanto è probabile che l'oggetto interferisca con il percorso dell'utente.

L'obiettivo sarebbe quindi **passare da un sistema che rileva gli ostacoli a uno che anticipa i pericoli**, avvisando l'utente soltanto quando necessario.

La parte interessante sarebbe ottenere tutto questo con modelli probabilistici relativamente leggeri, senza dover utilizzare necessariamente reti neurali enormi, e adattare tecniche già utilizzate in robotica a un dispositivo indossabile per persone non vedenti.</WritingBlock>

---

**User:**

Il mio amico dice che Però poi serve fare recognition sullo spazio, e non sa se si riesce online, il modello proposto riesce a compensare? 

---

**Assistant:**

Il tuo amico ha sollevato un problema concreto, ma **il modello che abbiamo proposto può ridurre notevolmente la necessità di eseguire continuamente il riconoscimento degli oggetti**.

La distinzione fondamentale è questa: **per evitare un ostacolo non è sempre necessario sapere che cosa sia. È necessario sapere dove si trova, quanto spazio occupa e come si muove.**

## 1. Il riconoscimento non è indispensabile per calcolare il rischio

Immagina che la telecamera rilevi un oggetto a 2 metri di distanza.

Il sistema potrebbe non sapere se sia una persona, una bicicletta o un carrello.

Tuttavia, se conosce la sua posizione e riesce a stimarne il movimento, può comunque prevedere un'eventuale collisione.

Quindi possiamo separare tre operazioni:

| Operazione | Serve una rete neurale? | Costo indicativo |
|---|---|---|
| Rilevazione geometrica degli ostacoli tramite profondità | Non necessariamente | Relativamente basso |
| Tracking e predizione con filtro di Kalman | No | Generalmente basso |
| Riconoscimento semantico (persona, bicicletta, muro) | Generalmente sì, per scene complesse | Più elevato |

Questo significa che **il riconoscimento semantico può diventare un componente opzionale**, anziché essere necessario per ogni aggiornamento della matrice.

Attenzione: la rilevazione geometrica richiede comunque dati di profondità affidabili. Con una sola telecamera RGB, stimare distanze e geometria è molto più difficile e potrebbe richiedere modelli computazionalmente costosi.

## 2. Come compenserei il problema: riconoscimento asincrono

Io proporrei un'architettura a due frequenze.

<box border radius="xl" padding={3} gap={2}>
  <row align="center" justify="center" gap={2}>
    <icon name="camera" size="lg"/>
    **Telecamera + profondità + IMU**
  </row>
  <divider color="subtle"/>
  <grid columns={2} gap={2}>
    <grid-item>
      <box background="rgba(25,125,85,0.07)" radius="lg" padding={3} gap={2} height="100%">
        <text weight="medium" size="sm">Percorso veloce</text>
        <badge color="secondary">Esempio: 20–30 Hz</badge>
        <text size="xs">Mappa geometrica, tracking, filtro di Kalman, rischio di collisione</text>
      </box>
    </grid-item>
    <grid-item>
      <box background="surface-secondary" radius="lg" padding={3} gap={2} height="100%">
        <text weight="medium" size="sm">Percorso lento</text>
        <badge color="secondary">Esempio: 2–5 Hz</badge>
        <text size="xs">Riconoscimento semantico degli oggetti tramite modello leggero</text>
      </box>
    </grid-item>
  </grid>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="surface-secondary" radius="lg" padding={3} align="center" gap={1}>
    **Fusione delle informazioni**

    <caption>La classificazione arricchisce la mappa, ma non blocca il calcolo geometrico del rischio</caption>
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="rgba(25,125,85,0.07)" radius="lg" padding={3} align="center">
    **Avviso all'utente**
  </box>
</box>

Le frequenze sono obiettivi progettuali indicativi, non prestazioni garantite: dipendono dall'hardware e dagli algoritmi.

Per esempio, il riconoscimento potrebbe identificare una persona al tempo \(t=0\).

Nei successivi 300 millisecondi, anche senza rieseguire la classificazione, il tracking potrebbe continuare a stimarne la posizione.

Quando arriva una nuova classificazione, il sistema aggiorna le informazioni semantiche.

In questo modo il modello di riconoscimento non deve necessariamente funzionare a 30 FPS.

## 3. Il filtro di Kalman può compensare il ritardo?

**Parzialmente sì, ma non può sostituire le osservazioni.**

Supponiamo che un oggetto si trovi a:

\[
x_0=2\text{ m}
\]

e che si muova verso l'utente a:

\[
v=-1\text{ m/s}
\]

Dopo 0,2 secondi, il filtro può prevedere:

\[
\hat x(0.2)=2-1(0.2)=1.8\text{ m}
\]

Quindi non serve necessariamente riconoscere nuovamente l'oggetto per prevederne la posizione.

Ma se l'oggetto cambia improvvisamente direzione, il filtro non può saperlo finché non arrivano nuove misurazioni.

Più tempo passa senza osservazioni, maggiore diventa l'incertezza.

Per questo farei continuare il tracking con nuove misure geometriche anche quando il riconoscimento semantico non viene eseguito.

## 4. La soluzione migliore: riconoscimento attivato quando serve

Un miglioramento ulteriore sarebbe usare un sistema di **riconoscimento adattivo**.

Invece di classificare continuamente tutti gli oggetti:

- Se una zona è libera e ben osservata, non serve una classificazione semantica.
- Se un oggetto è lontano e non interferisce con il percorso, si può ridurre la frequenza di riconoscimento.
- Se un oggetto si avvicina o la sua traiettoria è incerta, si aumenta la frequenza.
- Se il sistema rileva un potenziale pericolo ma non riesce a identificarlo, segnala comunque l'ostacolo.

In questo modo concentriamo le risorse computazionali nelle situazioni più importanti.

Non eliminerei, però, la scansione geometrica periodica dell'ambiente: un oggetto nuovo potrebbe comparire in una zona precedentemente libera.

## 5. Cosa riesce e cosa non riesce a compensare il nostro modello

| Problema | Il modello compensa? |
|---|---|
| Riconoscimento semantico troppo lento | Sì, rendendolo asincrono |
| Oggetto già rilevato ma non classificato | Sì, con tracking geometrico |
| Breve perdita delle osservazioni | Parzialmente, tramite predizione |
| Nuovo ostacolo mai osservato | No |
| Mancanza di informazioni sulla profondità | No, non completamente |
| Movimento improvviso e imprevedibile | Solo parzialmente |

Quest'ultimo punto è particolarmente importante: **MLE e MAP non risolvono il costo computazionale della computer vision**. Servono a stimare i parametri dei modelli probabilistici, non a generare informazioni visive che i sensori non hanno acquisito.

---

## Cosa risponderei al tuo amico

<WritingBlock id="62418" variant="chat_message">Secondo me possiamo compensare buona parte del problema separando il riconoscimento semantico dalla rilevazione geometrica.

Per calcolare il rischio di collisione non dobbiamo necessariamente sapere se un oggetto è una persona, una bici o un muro. Ci basta inizialmente conoscerne posizione, dimensioni e movimento.

Potremmo quindi avere due processi asincroni:

1. **Un processo veloce**, che aggiorna la matrice di occupazione, traccia gli ostacoli e ne prevede le traiettorie tramite filtri di Kalman.
2. **Un processo più lento**, che esegue object recognition soltanto periodicamente o quando serve, aggiungendo informazioni semantiche alla mappa.

In questo modo non dobbiamo eseguire una rete neurale di riconoscimento a ogni frame. Il tracking continua a funzionare anche tra due classificazioni successive.

Potremmo inoltre rendere il riconoscimento adattivo: se un oggetto è lontano e non presenta rischi, non serve classificarlo continuamente; se invece si avvicina o ha una traiettoria incerta, gli assegniamo maggiore priorità computazionale.

L'unico requisito importante è avere una stima geometrica affidabile dell'ambiente, idealmente tramite un sensore di profondità e una IMU. Con una sola RGB il problema diventa molto più complesso.

**Quindi l'idea sarebbe rendere la predizione del rischio indipendente dal riconoscimento semantico, utilizzando quest'ultimo per migliorare le previsioni, non come requisito per poterle calcolare.**

Questo non elimina i limiti dei sensori o gli errori di predizione, ma potrebbe ridurre parecchio il carico computazionale.</WritingBlock>

**La domanda decisiva da fargli è: gli occhiali avranno una semplice telecamera RGB oppure anche un sensore di profondità?**

Perché nel secondo caso l'architettura proposta è molto più realistica; nel primo, dovremmo ripensare soprattutto la componente di ricostruzione geometrica dell'ambiente.

---

**User:**

Il filtro di kalaman aiuterebbe? 

---

**Assistant:**

**Sì, il filtro di Kalman sarebbe molto utile per il vostro progetto.** Anzi, lo considererei uno dei componenti fondamentali per ridurre il carico computazionale del riconoscimento in tempo reale.

Il motivo è che **il filtro di Kalman permette di stimare la posizione futura di un oggetto senza doverlo riconoscere nuovamente a ogni frame**.

Attenzione però: può ridurre la frequenza del riconoscimento semantico, ma non elimina la necessità di nuove misurazioni.

## 1. Come funzionerebbe nel vostro caso

Immagina che gli occhiali rilevino una persona a 3 metri di distanza, in movimento verso l'utente.

Il sistema misura:

- Posizione iniziale: 3 metri.
- Velocità relativa: −1 m/s.
- Direzione: verso l'utente.

Il filtro di Kalman mantiene una stima dello stato dell'oggetto:

\[
\mathbf{x}_t =
\begin{bmatrix}
x_t\\y_t\\v_{x,t}\\v_{y,t}
\end{bmatrix}
\]

A ogni aggiornamento esegue due operazioni.

**Predizione:** calcola dove dovrebbe trovarsi l'oggetto dopo un intervallo \(\Delta t\).

\[
\hat{\mathbf{x}}_{t+1}^{-}=F\hat{\mathbf{x}}_t
\]

**Correzione:** quando arriva una nuova misurazione dalla telecamera o dal sensore di profondità, corregge la previsione.

\[
\hat{\mathbf{x}}_{t+1}=
\hat{\mathbf{x}}_{t+1}^{-}
+K(z_{t+1}-H\hat{\mathbf{x}}_{t+1}^{-})
\]

Dove \(K\) è il guadagno di Kalman, che determina quanto fidarsi della nuova misurazione rispetto alla previsione.

## 2. Esempio concreto

<box border radius="xl" padding={3} gap={3}>
  <text weight="medium">Simulazione di un oggetto che si avvicina</text>
  {@body const [elapsed,setElapsed]=DIL.useState(0.5)}
  {@body const distance=3-elapsed}
  <svg viewBox="0 0 340 130" width="100%">
    <rect x="12" y="8" width="316" height="112" rx="10" fill="#8C9DA4" opacity=".10"/>
    <path d="M30 85 H310" stroke="currentColor" strokeWidth="1.5" opacity=".3" strokeDasharray="5 5"/>
    <circle cx="30" cy="85" r="12" fill="#279E78"/>
    <text x="30" y="112" fontSize="10" fill="currentColor" textAnchor="middle">Utente</text>
    <circle cx={30+distance/3*280} cy="85" r="12" fill="#E17D45"/>
    <text x={30+distance/3*280} y="65" fontSize="11" fill="currentColor" textAnchor="middle">Ostacolo</text>
    <path d={`M${30+distance/3*280-14} 85 l-24 0 m7 -5 l-7 5 l7 5`} stroke="#E17D45" fill="none" strokeWidth="2"/>
    <text x="170" y="29" fontSize="14" fill="currentColor" fontWeight="600" textAnchor="middle">{distance.toFixed(1)} m</text>
  </svg>
  <row justify="between" align="center">
    <text color="secondary" size="xs">Tempo trascorso</text>
    <text weight="medium" tabularNums>{elapsed.toFixed(1)} s</text>
  </row>
  <slider min={0} max={2.5} step={0.1} value={elapsed} onChange={setElapsed}/>
  <grid columns={2} gap={2}>
    <grid-item>
      <box background="surface-secondary" radius="lg" padding={3} gap={1}>
        <text color="secondary" size="xs">Distanza prevista</text>
        <title size="xl" color="default" tabularNums>{distance.toFixed(1)} m</title>
      </box>
    </grid-item>
    <grid-item>
      <box background="surface-secondary" radius="lg" padding={3} gap={1}>
        <text color="secondary" size="xs">Tempo all'impatto stimato</text>
        <title size="xl" color="default" tabularNums>{distance.toFixed(1)} s</title>
      </box>
    </grid-item>
  </grid>
  <caption>Modello semplificato a velocità relativa costante di 1 m/s, con traiettorie coincidenti e senza incertezza.</caption>
</box>

In un caso reale, il filtro manterrebbe anche una matrice di covarianza \(P_t\), che rappresenta l'incertezza della stima.

Quando mancano nuove osservazioni, il filtro continua a prevedere, ma l'incertezza generalmente aumenta.

## 3. Come si integra con la vostra architettura?

| Componente | Funzione |
|---|---|
| Occupancy Grid bayesiana | Determina quali zone sono occupate |
| Object detection | Rileva nuovi ostacoli |
| **Filtro di Kalman** | Stima e aggiorna posizione e velocità degli ostacoli |
| MLE/MAP | Stima i parametri del modello dinamico |
| Risk prediction | Valuta le possibili collisioni future |

Un vantaggio importante è che potreste far funzionare il riconoscimento semantico a frequenza inferiore rispetto al tracking.

Ad esempio, il riconoscimento potrebbe funzionare a 5 FPS e il filtro di Kalman aggiornare le predizioni a 30 Hz, correggendole quando arrivano nuove misurazioni geometriche. Sono frequenze illustrative, da verificare sull'hardware.

## 4. Quale filtro utilizzerei?

Per un primo prototipo sceglierei il **Kalman Filter lineare**, assumendo un modello a velocità quasi costante.

Successivamente valuterei:

- **Extended Kalman Filter (EKF):** per modelli di movimento o misurazione non lineari.
- **Unscented Kalman Filter (UKF):** per gestire non linearità più complesse.
- **Interacting Multiple Model (IMM):** per combinare più modelli di movimento, ad esempio velocità costante e accelerazione.

L'IMM sarebbe particolarmente interessante per prevedere i movimenti di persone e biciclette, che possono cambiare velocità o direzione.

## 5. Il limite fondamentale

Il filtro di Kalman **non fa object recognition e non ricostruisce autonomamente lo spazio tridimensionale**.

Se il sistema non conosce la distanza di un ostacolo, il filtro non può inventarla.

Inoltre, bisogna distinguere il movimento della telecamera da quello degli oggetti, utilizzando informazioni dell'IMU e possibilmente visual odometry.

Perciò il Kalman è un ottimo complemento a una pipeline di percezione geometrica, non un suo sostituto.

**La mia proposta finale:** Occupancy Grid 2.5D + tracking geometrico + filtro di Kalman + modello di rischio probabilistico, mantenendo il riconoscimento semantico asincrono.

Questa combinazione permetterebbe di dedicare meno risorse alla classificazione continua degli oggetti e più risorse alla previsione del rischio, che è l'obiettivo principale degli occhiali.

---

**User:**

Bisogna tenere traccia dello Stato nel tempo? Se si, a livello di spazio e computazione abbiamo problemi?

---

**Assistant:**

**Sì, bisogna mantenere uno stato nel tempo, ma non è necessario conservare tutta la storia dell'ambiente.** Ed è proprio questo il vantaggio del filtro di Kalman: permette di rappresentare le informazioni rilevanti del passato attraverso uno stato compatto.

Per il vostro progetto degli occhiali intelligenti, distinguerei due tipi di memoria:

1. **Memoria spaziale:** dove si trovano gli ostacoli nell'ambiente.
2. **Memoria temporale:** come si stanno muovendo gli ostacoli e quanto sono affidabili le previsioni.

La buona notizia è che, con un'architettura progettata correttamente, il costo di entrambe può rimanere contenuto.

## 1. Cosa dobbiamo conservare nel tempo?

Per ogni oggetto tracciato, il filtro di Kalman mantiene:

\[
\mathbf{x}_t=
\begin{bmatrix}
x_t & y_t & v_{x,t} & v_{y,t}
\end{bmatrix}^{T}
\]

Oltre allo stato, mantiene la matrice di covarianza:

\[
P_t\in\mathbb{R}^{4\times4}
\]

Questa contiene le informazioni sull'incertezza delle stime.

Quando arriva una nuova osservazione, il filtro aggiorna lo stato e la covarianza.

**Non serve conservare tutte le posizioni precedenti**, perché nel modello lineare-gaussiano del Kalman lo stato corrente e la covarianza riassumono le informazioni necessarie per la stima successiva.

Naturalmente, per applicare il filtro bisogna anche conservare i parametri del modello dinamico e del rumore.

## 2. Quanto occupa in memoria?

Facciamo un esempio utilizzando `float32`, quindi 4 byte per valore.

Per ogni oggetto:

| Informazione | Dimensione |
|---|---:|
| Stato (4 float) | 16 byte |
| Covarianza (4 × 4 float) | 64 byte |
| Totale matematico | 80 byte |

<box border radius="xl" padding={3} gap={3}>
  <text weight="medium">Simulatore della memoria per il tracking</text>
  {@body const [objects,setObjects]=DIL.useState(100)}
  {@body const bytes=objects*80}
  <row justify="between" align="center">
    <text color="secondary" size="sm">Oggetti tracciati</text>
    <title size="lg" tabularNums>{objects}</title>
  </row>
  <slider min={10} max={1000} step={10} value={objects} onChange={setObjects}/>
  <grid columns={2} gap={2}>
    <grid-item>
      <box background="surface-secondary" padding={3} radius="lg" gap={1}>
        <text color="secondary" size="xs">Memoria teorica</text>
        <title size="xl" tabularNums>{(bytes/1024).toFixed(1)} KB</title>
      </box>
    </grid-item>
    <grid-item>
      <box background="surface-secondary" padding={3} radius="lg" gap={1}>
        <text color="secondary" size="xs">Stato + covarianza</text>
        <title size="xl" tabularNums>{objects*20}</title>
        <caption>Valori float32</caption>
      </box>
    </grid-item>
  </grid>
  <caption>Stima del solo contenuto numerico dei filtri. Non include identificativi, strutture dati, associazione degli oggetti, buffer e overhead del runtime.</caption>
</box>

Come puoi vedere, **la memoria del Kalman non è il vero problema**.

Anche con centinaia di oggetti, parliamo di quantità molto contenute.

## 3. Il costo maggiore è la matrice spaziale

Qui bisogna prestare più attenzione.

Supponiamo di rappresentare un'area di 20 × 20 metri con celle di 10 centimetri.

Otteniamo:

\[
N=\frac{20}{0.1}\cdot\frac{20}{0.1}
=40\,000\text{ celle}
\]

Se ogni cella contiene una probabilità `float32`:

\[
40\,000\cdot4=160\,000\text{ byte}
\]

Ovvero circa 156 KiB.

Se invece usassimo una griglia 3D con 30 livelli verticali:

\[
40\,000\cdot30\cdot4
=4\,800\,000\text{ byte}
\]

Circa 4,58 MiB, sempre per un solo valore per voxel.

<box border radius="xl" padding={3} gap={3}>
  <text weight="medium">Confronto memoria delle mappe</text>
  {@body const [side,setSide]=DIL.useState(20)}
  {@body const [resolution,setResolution]=DIL.useState("0.1")}
  {@body const cellCount=Math.ceil(side/Number(resolution))**2}
  {@body const map2=cellCount*4}
  {@body const map25=cellCount*3*4}
  {@body const map3=cellCount*30*4}
  <row align="center" justify="between">
    <text size="sm">Lato area quadrata</text>
    <text weight="medium" tabularNums>{side} m</text>
  </row>
  <slider min={10} max={50} step={5} value={side} onChange={setSide}/>
  <row align="center" justify="between">
    <text size="sm">Risoluzione orizzontale</text>
    <box width="135px">
      <select block size="md" value={resolution} onChange={setResolution} options={[{label:"5 cm",value:"0.05"},{label:"10 cm",value:"0.1"},{label:"20 cm",value:"0.2"}]}/>
    </box>
  </row>
  <box gap={3}>
    {#each [{name:"2D",value:map2,desc:"1 valore/cella"},{name:"2.5D",value:map25,desc:"3 valori/cella"},{name:"3D",value:map3,desc:"30 valori/cella"}] as m}
      <box gap={1} key={m.name}>
        <row align="center" justify="between">
          <text weight="medium" size="sm">{m.name} <text inline color="secondary" size="xs">({m.desc})</text></text>
          <text weight="medium" tabularNums>{(m.value/1048576).toFixed(2)} MiB</text>
        </row>
        <box background="surface-tertiary" height="12px" radius="full" clip>
          <box background={m.name==="3D"?"#D18B45":m.name==="2.5D"?"#438CB6":"#429779"} height="100%" width={`${m.value/map3*100}%`} radius="full"/>
        </box>
      </box>
    {/each}
  </box>
  <caption>Stime teoriche con float32. Il 2.5D è modellato con tre valori per cella; il 3D con 30 livelli verticali. Sono esclusi overhead e dati aggiuntivi.</caption>
</box>

La griglia 3D può quindi richiedere molta più memoria, ma anche in questo caso non siamo necessariamente davanti a un problema insormontabile.

Il problema diventa più serio quando aumentiamo risoluzione, dimensioni dell'area, numero di attributi e frequenza degli aggiornamenti.

## 4. Il vero rischio computazionale: la dimensione dello stato

Per un filtro di Kalman con uno stato di dimensione \(n\), l'aggiornamento delle matrici può richiedere fino a \(O(n^3)\) operazioni in una implementazione generica, soprattutto per inversioni e fattorizzazioni.

Tuttavia, **non utilizzerei un unico filtro gigantesco che contiene tutte le celle e tutti gli oggetti**.

Utilizzerei invece un filtro piccolo per ogni oggetto.

Se ogni oggetto ha uno stato di dimensione fissa, come quattro o sei variabili, il costo del singolo filtro rimane praticamente costante.

Con \(K\) oggetti tracciati:

\[
T_{\text{filtri}}=O(K)
\]

Questo vale per i soli aggiornamenti dei filtri a dimensione fissa, escludendo il costo di rilevamento e associazione delle osservazioni agli oggetti.

L'associazione dei dati, la ricostruzione geometrica e l'elaborazione delle immagini potrebbero essere molto più costose dei filtri stessi.

## 5. Come gestirei lo stato nel tempo?

Proporrei una **Rolling Occupancy Grid**, cioè una matrice locale che segue il movimento dell'utente.

<box border radius="lg" padding={3} gap={2}>
  <text weight="medium" size="sm">Esempio di mappa locale mobile</text>
  <svg viewBox="0 0 340 165" width="100%">
    <rect x="15" y="12" width="310" height="140" rx="9" fill="#64748b" opacity=".09"/>
    {#each [0,1,2,3,4,5,6,7,8,9,10,11] as i}
      <path d={`M${24+i*25} 20 V145`} stroke="currentColor" opacity=".11"/>
    {/each}
    {#each [0,1,2,3,4,5] as i}
      <path d={`M24 ${20+i*25} H324`} stroke="currentColor" opacity=".11"/>
    {/each}
    <rect x="25" y="31" width="145" height="108" rx="5" fill="#478DAD" fillOpacity=".15" stroke="#478DAD" strokeWidth="1.5" strokeDasharray="5 3"/>
    <rect x="105" y="31" width="145" height="108" rx="5" fill="#449D7A" fillOpacity=".14" stroke="#449D7A" strokeWidth="2"/>
    <circle cx="100" cy="85" r="9" fill="#478DAD"/>
    <circle cx="180" cy="85" r="9" fill="#449D7A"/>
    <path d="M112 85 H165 M157 80 L165 85 L157 90" stroke="currentColor" strokeWidth="2" fill="none"/>
    <rect x="210" y="44" width="20" height="38" rx="3" fill="#D58D42"/>
    <text x="97" y="119" fontSize="10" textAnchor="middle" fill="currentColor">Prima</text>
    <text x="190" y="119" fontSize="10" textAnchor="middle" fill="currentColor">Dopo</text>
  </svg>
  <caption>La finestra spaziale si sposta con l'utente. Le celle fuori dall'area di interesse vengono scartate e le nuove zone inizializzate come sconosciute.</caption>
</box>

In questo modo non dobbiamo memorizzare tutta la città o l'intero percorso compiuto dall'utente.

Manteniamo soltanto una regione locale, ad esempio 10–20 metri attorno alla persona, da dimensionare in base a velocità, portata dei sensori e tempo necessario per reagire.

Gli oggetti tracciati vengono mantenuti finché sono rilevanti. Quando escono dalla zona di interesse o non vengono più osservati per troppo tempo, possono essere rimossi dopo un criterio di scadenza.

## 6. Bisogna salvare tutte le matrici nel tempo?

**No. Questo sarebbe uno degli errori architetturali da evitare.**

Se memorizzassimo una matrice completa per ogni frame, la memoria crescerebbe linearmente con il tempo.

Per esempio, una mappa da 160 KB salvata 30 volte al secondo produrrebbe circa 4,8 MB/s, ovvero circa 288 MB al minuto (unità decimali).

Invece manterrei:

- Una sola mappa di occupazione corrente.
- Uno stato e una covarianza per ciascun oggetto tracciato.
- Un breve buffer di osservazioni per sincronizzare i sensori.
- Eventualmente alcune mappe future del rischio, generate temporaneamente e poi sovrascritte.

Il Kalman non richiede l'intera storia delle osservazioni: utilizza una rappresentazione ricorsiva dello stato.

---

## 7. La mia scelta architetturale

Per un primo prototipo utilizzerei:

| Componente | Strategia |
|---|---|
| Mappa | Rolling Grid 2.5D |
| Memoria temporale | Stato corrente + covarianza |
| Tracking | Un filtro di Kalman per oggetto |
| Predizione | Orizzonte futuro di 1–3 secondi |
| Riconoscimento | Asincrono e adattivo |
| Gestione memoria | Buffer circolari e scadenza degli oggetti |
| Elaborazione | Locale, con frequenze diverse per i vari moduli |

**Conclusione:** il mantenimento dello stato nel tempo non dovrebbe rappresentare il principale collo di bottiglia del sistema.

Le criticità più importanti saranno probabilmente l'elaborazione delle immagini, la stima della profondità, l'associazione degli oggetti tra frame, il consumo energetico e la latenza complessiva.

Il vantaggio del filtro di Kalman è proprio quello di **comprimere l'informazione temporale in uno stato matematico molto piccolo**, permettendo di effettuare previsioni senza conservare continuamente tutto ciò che è accaduto in passato.

C'è però una distinzione decisiva: questo vale per la stima ricorsiva di uno stato sotto le ipotesi del modello. Se vogliamo riconoscere comportamenti complessi, prevedere intenzioni o gestire occlusioni prolungate, potrebbe servire anche una breve storia temporale.

Per il vostro progetto partirei senza questa complessità, aggiungendola soltanto se i test mostrassero che è necessaria.

---

**User:**

Quindi si può aggiornare la matrice di covarianza dei pesi mantenendo bassa la computazione?

---

**Assistant:**

**Sì, assolutamente.** Ma c'è una distinzione matematica importante: **la matrice di covarianza dello stato del filtro di Kalman non è necessariamente la matrice di covarianza dei pesi del modello.**

Nel vostro progetto possiamo aggiornare entrambe, ma con costi computazionali differenti.

## 1. Covarianza dello stato vs covarianza dei pesi

Supponiamo che il filtro di Kalman descriva un oggetto attraverso:

\[
\mathbf{x}_t=
\begin{bmatrix}
x & y & v_x & v_y
\end{bmatrix}^{T}
\]

La matrice di covarianza dello stato è:

\[
P_t\in\mathbb{R}^{4\times4}
\]

Questa descrive l'incertezza sulla posizione e sulla velocità dell'oggetto.

Il filtro la aggiorna ricorsivamente:

**Predizione:**

\[
P_t^-=FP_{t-1}F^T+Q
\]

**Correzione:**

\[
K_t=P_t^-H^T(HP_t^-H^T+R)^{-1}
\]

\[
P_t=(I-K_tH)P_t^-
\]

Dove \(Q\) rappresenta l'incertezza del modello dinamico e \(R\) quella delle misurazioni.

Con uno stato di sole quattro variabili, queste operazioni sono generalmente molto economiche.

## 2. E se volessimo aggiornare la covarianza dei pesi?

Qui entriamo nella tua idea iniziale della MLE/MAP.

Supponiamo di avere un modello parametrico con pesi:

\[
\theta=
\begin{bmatrix}
w_1&w_2&\dots&w_n
\end{bmatrix}^{T}
\]

Possiamo rappresentare anche l'incertezza sui pesi mediante una matrice:

\[
\Sigma_\theta\in\mathbb{R}^{n\times n}
\]

**Se il numero di pesi è piccolo, possiamo aggiornare questa matrice online con un costo contenuto.**

Per esempio, se utilizziamo un modello lineare per stimare la velocità futura di un ostacolo, possiamo impiegare il *Recursive Least Squares* (RLS), strettamente collegato al filtro di Kalman.

Le equazioni sono:

\[
k_t=
\frac{P_{t-1}\phi_t}
{\lambda+\phi_t^TP_{t-1}\phi_t}
\]

\[
\theta_t=\theta_{t-1}
+k_t(y_t-\phi_t^T\theta_{t-1})
\]

\[
P_t=\frac{1}{\lambda}
\left(P_{t-1}-k_t\phi_t^TP_{t-1}\right)
\]

Dove:

- \(\theta_t\) sono i pesi aggiornati.
- \(\phi_t\) è il vettore delle caratteristiche osservate.
- \(y_t\) è il valore misurato.
- \(P_t\) rappresenta la matrice di incertezza dei parametri, proporzionale alla loro covarianza sotto opportune ipotesi.
- \(\lambda\) è il fattore di dimenticanza.

Con \(\lambda=1\) non introduciamo dimenticanza esponenziale; con valori leggermente inferiori a 1 diamo maggiore importanza alle osservazioni recenti.

In un modello lineare-gaussiano, RLS può essere interpretato come un aggiornamento bayesiano dei parametri.

## 3. Quanto costa computazionalmente?

Per RLS con \(n\) pesi, l'aggiornamento richiede tipicamente:

\[
\boxed{O(n^2)}
\]

e la matrice richiede:

\[
\boxed{O(n^2)\text{ memoria}}
\]

<box border radius="xl" padding={3} gap={3}>
  <text weight="medium">Costo della covarianza dei pesi</text>
  {@body const [n,setN]=DIL.useState(16)}
  {@body const bytes=n*n*4}
  <row align="center" justify="between">
    <text color="secondary" size="sm">Numero di parametri</text>
    <title size="lg" tabularNums>{n}</title>
  </row>
  <slider min={4} max={256} step={4} value={n} onChange={setN}/>
  <box background="surface-secondary" padding={3} radius="lg" gap={1}>
    <text color="secondary" size="xs">Memoria della sola matrice di covarianza (float32)</text>
    <title size="xl" tabularNums>{bytes>=1048576?(bytes/1048576).toFixed(2)+" MiB":(bytes/1024).toFixed(1)+" KiB"}</title>
    <caption>{(n*n).toLocaleString("it-IT")} elementi della matrice</caption>
  </box>
  <text color="secondary" size="xs">La memoria cresce quadraticamente con il numero dei pesi. Anche il lavoro per aggiornamento RLS cresce tipicamente in modo quadratico.</text>
</box>

Con 16 pesi, per esempio, la matrice contiene soltanto 256 elementi.

Con 10.000 pesi, invece, conterrebbe 100 milioni di elementi, occupando circa 400 MB in `float32`.

Quindi l'approccio è molto interessante per **modelli probabilistici piccoli**, ma non per aggiornare online la covarianza completa di una grande rete neurale.

## 4. Come lo utilizzerei nel vostro progetto?

Separerei due meccanismi:

**A. Kalman per gli oggetti**

Aggiorna continuamente posizione, velocità e incertezza di ogni ostacolo. È il componente che deve funzionare a frequenza elevata.

**B. RLS o aggiornamento bayesiano per i parametri**

Aggiorna, eventualmente a frequenza inferiore, i parametri di un piccolo modello predittivo, ad esempio quello che stima come cambia la velocità degli ostacoli.

Non aggiornerei i parametri sulla base delle sole previsioni del sistema: servono nuove osservazioni che permettano di misurare l'errore predittivo.

Inoltre, per un dispositivo assistivo, inizierei con parametri addestrati offline e validati, limitando gli aggiornamenti online a quantità ben controllate.

## 5. La soluzione ancora più leggera

Se anche \(O(n^2)\) fosse troppo costoso, potremmo approssimare la covarianza dei pesi con una matrice diagonale:

\[
\Sigma_\theta\approx
\operatorname{diag}(\sigma_1^2,\dots,\sigma_n^2)
\]

In questo caso la memoria scende a:

\[
O(n)
\]

Perdiamo però le correlazioni tra i parametri, e non otteniamo più l'equivalente esatto dell'RLS completo.

---

**In conclusione:** sì, la tua intuizione è corretta. Possiamo mantenere una stima ricorsiva dei pesi e della loro incertezza senza conservare tutte le osservazioni precedenti, sfruttando RLS o un filtro di Kalman sui parametri.

La distinzione fondamentale è che **Kalman aggiorna l'incertezza sullo stato degli ostacoli, mentre RLS può aggiornare l'incertezza sui parametri del modello**.

Per la vostra architettura, userei entrambi, ma terrei il modello dei pesi piccolo e separato dal tracking. È un modo matematicamente rigoroso per ottenere adattamento online con un costo computazionale prevedibile.

---

**User:**

Per non scalare esponenzialmente con le Classi, organizzare la struttura delle classi in un albero sarebbe un idea? Pensa quale albero sarebbe il migliore 

---

**Assistant:**

Valuto due possibilità distinte: un albero per classificare gli oggetti e un albero per organizzare lo spazio. Nel vostro sistema hanno scopi diversi, quindi la scelta migliore potrebbe essere combinarli senza rendere il calcolo del rischio dipendente dal riconoscimento.

---

**Assistant:**

**Sì, organizzare le classi in un albero è una buona idea.** Per il vostro sistema di occhiali intelligenti, però, sceglierei una struttura specifica: **un albero gerarchico probabilistico, bilanciato per quanto possibile e organizzato in base al comportamento degli ostacoli**, non semplicemente alla loro categoria.

La tecnica da cui partirei è la *Hierarchical Classification*, eventualmente combinata con una *Hierarchical Softmax*. Esistono già lavori che dimostrano come strutture ad albero possano rendere più efficiente la classificazione quando il numero delle classi è elevato. <Cite refs={["turn826764search1","turn826764search2"]}/>

C'è una precisazione matematica: il numero di classi non fa necessariamente crescere il costo in modo esponenziale. Un classificatore tradizionale con \(C\) classi può richiedere \(O(C)\) operazioni per il livello finale di classificazione. Un albero bilanciato può ridurre il numero di decisioni da eseguire per una singola classificazione a \(O(\log C)\), se ciascun nodo ha un costo limitato.

## 1. L'albero che proporrei

Non utilizzerei una tassonomia puramente semantica come `Animale → Mammifero → Cane`.

Per il vostro progetto, le caratteristiche interessanti sono soprattutto la mobilità, la geometria e la possibile interferenza con il percorso.

<box border radius="xl" padding={3} gap={2}>
  <text weight="medium" size="sm">Esempio di albero gerarchico orientato al comportamento</text>
  <box background="surface-secondary" radius="lg" padding={3} align="center">
    **Ostacolo rilevato**
  </box>
  <row justify="center"><icon name="git-branch" color="secondary"/></row>
  <grid columns={2} gap={2}>
    <grid-item>
      <box border radius="lg" padding={2} gap={2} height="100%">
        <box background="rgba(30,135,100,0.09)" radius="md" padding={2} align="center">
          **Statico o quasi statico**
        </box>
        <box background="surface-secondary" radius="md" padding={2} align="center">
          <text weight="medium" size="sm">Strutturale</text>
          <caption>Muri, colonne, gradini</caption>
        </box>
        <box background="surface-secondary" radius="md" padding={2} align="center">
          <text weight="medium" size="sm">Spostabile</text>
          <caption>Sedie, carrelli fermi, biciclette parcheggiate</caption>
        </box>
      </box>
    </grid-item>
    <grid-item>
      <box border radius="lg" padding={2} gap={2} height="100%">
        <box background="rgba(210,125,40,0.09)" radius="md" padding={2} align="center">
          **Dinamico**
        </box>
        <box background="surface-secondary" radius="md" padding={2} align="center">
          <text weight="medium" size="sm">Moto più prevedibile</text>
          <caption>Veicoli su traiettorie regolari</caption>
        </box>
        <box background="surface-secondary" radius="md" padding={2} align="center">
          <text weight="medium" size="sm">Moto meno prevedibile</text>
          <caption>Pedoni, animali, bambini</caption>
        </box>
      </box>
    </grid-item>
  </grid>
  <caption>Gerarchia illustrativa: staticità, mobilità e prevedibilità sono proprietà stimate, non categorie immutabili. Una bicicletta può passare da ferma a mobile.</caption>
</box>

Il vantaggio è che **non dobbiamo sempre arrivare alle foglie dell'albero**.

Se gli occhiali rilevano un ostacolo immobile davanti all'utente, il sistema può calcolare il rischio senza stabilire se si tratti di una colonna, di un muro o di un armadio.

La classificazione più dettagliata viene eseguita soltanto quando può migliorare la previsione.

## 2. Quale tipo di albero sceglierei?

| Struttura | Vantaggio | Valutazione |
|---|---|---|
| Albero binario bilanciato | Profondità logaritmica | Ottimo per classificazione efficiente |
| Albero di Huffman | Percorsi brevi per classi frequenti | Utile se le frequenze sono stabili |
| Decision tree tradizionale | Semplice e interpretabile | Possibile, ma meno flessibile |
| **Albero gerarchico probabilistico** | Mantiene incertezza tra categorie | **La mia scelta** |
| Octree | Comprime lo spazio tridimensionale | Utile per la mappa, non per le classi |

Per il riconoscimento sceglierei dunque un albero probabilistico con diramazioni piccole, preferibilmente binarie, ma consentirei al sistema di conservare più ipotesi quando la classificazione è incerta.

Questo evita che un errore ai primi livelli obblighi l'algoritmo a seguire un unico ramo sbagliato, uno dei limiti noti dei classificatori gerarchici. <Cite refs={["turn826764search3","turn826764search6"]}/>

## 3. Quanto risparmieremmo computazionalmente?

Prendiamo 1.024 classi.

<box border radius="xl" padding={3} gap={2}>
  <text weight="medium" size="sm">Confronto teorico delle decisioni</text>
  <grid columns={2} gap={3}>
    <grid-item>
      <box background="surface-secondary" radius="lg" padding={3} gap={1}>
        <text color="secondary" size="xs">Classificazione piatta</text>
        <title size="2xl" color="default" tabularNums>1.024</title>
        <caption>Score di classe valutati</caption>
      </box>
    </grid-item>
    <grid-item>
      <box background="surface-secondary" radius="lg" padding={3} gap={1}>
        <text color="secondary" size="xs">Albero binario bilanciato</text>
        <title size="2xl" color="success" tabularNums>10</title>
        <caption>Decisioni lungo un percorso</caption>
      </box>
    </grid-item>
  </grid>
  <text color="secondary" size="xs">Il confronto riguarda il solo livello di classificazione: i 10 nodi possono avere un costo diverso dal calcolo di 1.024 score. L'estrazione delle caratteristiche visive resta necessaria.</text>
</box>

Per un albero binario bilanciato:

\[
D=\lceil\log_2 C\rceil
\]

Con 1.024 classi abbiamo una profondità di 10.

Tuttavia, non significa che l'intero sistema diventi 100 volte più veloce. La rete che estrae informazioni dalle immagini può continuare a rappresentare la maggior parte del costo.

## 4. Come collegherei l'albero alla vostra matrice bayesiana

Qui introdurrei un miglioramento importante.

Ogni nodo dell'albero potrebbe contenere un modello probabilistico condiviso tra le classi discendenti.

Per esempio:

- Il nodo *oggetto dinamico* potrebbe contenere un modello generale di movimento.
- Il nodo *pedone* potrebbe contenere parametri più specifici.
- Il nodo *bambino* potrebbe aggiungere un modello di comportamento distinto, soltanto se supportato dai dati.

In questo modo, **non è necessario addestrare da zero un modello completamente indipendente per ogni classe**.

Possiamo rappresentare i parametri di una classe come:

\[
\theta_c=\theta_{\text{padre}}+\Delta_c
\]

Dove \(\Delta_c\) rappresenta una correzione specifica della classe.

Possiamo utilizzare MLE o MAP per stimare questi parametri, favorendo mediante una prior MAP correzioni piccole quando disponiamo di pochi dati.

È una forma di apprendimento gerarchico con condivisione dei parametri.

### Ma attenzione alla covarianza

Se ogni classe avesse una matrice di covarianza completa dei propri pesi, il costo sarebbe indicativamente:

\[
O(Cd^2)
\]

dove \(C\) è il numero di classi e \(d\) il numero di parametri per classe.

L'albero, da solo, **non elimina questo costo di memoria**.

Per limitarlo, utilizzerei:

- Parametri condivisi nei nodi principali.
- Piccole correzioni nei nodi figli.
- Covarianze diagonali o a basso rango dove accettabile.
- Aggiornamenti soltanto per i modelli effettivamente utilizzati.

L'obiettivo sarebbe evitare di mantenere molti modelli completi e indipendenti.

## 5. E per organizzare lo spazio? Un altro albero: Octree

Se per *struttura delle classi* intendi anche la suddivisione dello spazio fisico, allora valuterei una struttura completamente diversa: l'**Octree**.

<AsyncImage query="octree hierarchical 3D spatial subdivision cube visualization computer graphics" aspectRatio="16:9"/>

Un Octree suddivide ricorsivamente un volume in otto sottovolumi.

È interessante perché permette di rappresentare le regioni con risoluzione adattiva: aree uniformi con pochi nodi e aree geometricamente complesse con più nodi.

È già utilizzato nella libreria di robotica <Entity category="software" value="OctoMap"/>, che supporta mappe probabilistiche tridimensionali e aggiornamenti incrementali. <Cite ref="turn826764search0"/>

Per gli occhiali, però, partirei da una rolling grid 2.5D. Passerei a Octree soltanto se i test mostrassero che la rappresentazione tridimensionale adattiva offre vantaggi sufficienti rispetto ai suoi costi.

---

## 6. L'architettura che sceglierei definitivamente

Separerei tre strutture:

<box border radius="xl" padding={3} gap={2}>
  <box background="surface-secondary" radius="lg" padding={3} gap={1}>
    <row align="center" gap={2}>
      <icon name="scan" color="secondary"/>
      **Mappa 2.5D / Octree**
    </row>
    <text color="secondary" size="sm">Dove si trovano gli ostacoli e quali spazi sono sconosciuti?</text>
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="surface-secondary" radius="lg" padding={3} gap={1}>
    <row align="center" gap={2}>
      <icon name="git-branch" color="secondary"/>
      **Albero gerarchico probabilistico**
    </row>
    <text color="secondary" size="sm">Quale modello di comportamento è più appropriato per l'ostacolo?</text>
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="surface-secondary" radius="lg" padding={3} gap={1}>
    <row align="center" gap={2}>
      <icon name="activity" color="secondary"/>
      **Kalman + modelli dinamici**
    </row>
    <text color="secondary" size="sm">Dove potrebbe trovarsi l'ostacolo nei prossimi secondi?</text>
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box border radius="lg" padding={3} gap={1}>
    <row align="center" gap={2}>
      <icon name="shield-alert" color="secondary"/>
      **Risk Prediction**
    </row>
    <text color="secondary" size="sm">Qual è la probabilità che la traiettoria dell'utente intersechi quella dell'ostacolo?</text>
  </box>
</box>

Il calcolo geometrico del rischio dovrebbe comunque poter funzionare anche quando la classificazione gerarchica fallisce: un oggetto sconosciuto non deve diventare invisibile al sistema.

C'è infine un compromesso progettuale interessante. **Non cercherei di bilanciare l'albero soltanto in base al numero di classi.** Lo organizzerei soprattutto per ridurre il costo medio delle decisioni, dando priorità a quelle che influenzano la sicurezza.

Per esempio, distinguere un ostacolo sospeso da uno a terra è probabilmente più importante che distinguere due tipi di veicoli con traiettorie già osservate.

Inoltre, terrei mobilità, altezza e classe semantica come attributi distinti: un singolo albero rigido non rappresenta bene tutte queste dimensioni contemporaneamente.

**La mia scelta finale sarebbe quindi un albero gerarchico probabilistico orientato al rischio, con classificazione grossolana iniziale, raffinamento selettivo e condivisione dei parametri.**

È probabilmente più utile, per il vostro caso, di un normale albero di Huffman o di un semplice albero binario costruito sulle etichette degli oggetti.

---

**User:**

Dato che è una matrice 2.5d che struttura dati consiglieresti?

---

**Assistant:**

Per il vostro progetto degli occhiali intelligenti per persone non vedenti, **consiglierei una Rolling Grid 2.5D implementata tramite un array bidimensionale contiguo e gestita come buffer circolare (Ring Buffer)**.

Non utilizzerei inizialmente né un Octree né un albero binario, perché la vostra mappa rappresenta principalmente uno spazio bidimensionale con informazioni verticali aggiuntive.

L'obiettivo è avere una struttura dati che permetta di:

- Accedere a una cella in \(O(1)\).
- Aggiornare le probabilità di occupazione in tempo reale.
- Conservare informazioni sull'altezza degli ostacoli.
- Spostare la mappa insieme all'utente senza copiarla interamente.
- Ridurre allocazioni, consumo di memoria e latenza.

## 1. La struttura che sceglierei

<box border radius="xl" padding={3} gap={2}>
  <text weight="medium">Rolling Grid 2.5D — struttura logica</text>
  <grid columns={2} gap={2}>
    <grid-item>
      <box background="surface-secondary" radius="lg" padding={3} gap={1}>
        <icon name="grid-3x3" color="secondary" size="lg"/>
        **Array 2D contiguo**
        <text size="xs" color="secondary">Accesso diretto alle celle tramite coordinate</text>
      </box>
    </grid-item>
    <grid-item>
      <box background="surface-secondary" radius="lg" padding={3} gap={1}>
        <icon name="refresh-cw" color="secondary" size="lg"/>
        **Ring Buffer**
        <text size="xs" color="secondary">Riutilizza la memoria mentre la persona cammina</text>
      </box>
    </grid-item>
    <grid-item>
      <box background="surface-secondary" radius="lg" padding={3} gap={1}>
        <icon name="layers-3" color="secondary" size="lg"/>
        **Canali verticali**
        <text size="xs" color="secondary">Piedi, corpo e testa oppure intervalli di altezza</text>
      </box>
    </grid-item>
    <grid-item>
      <box background="surface-secondary" radius="lg" padding={3} gap={1}>
        <icon name="activity" color="secondary" size="lg"/>
        **Tracking separato**
        <text size="xs" color="secondary">Kalman e traiettorie degli oggetti mobili</text>
      </box>
    </grid-item>
  </grid>
</box>

In memoria sarebbe sostanzialmente:

```cpp
struct Cell {
    float occupancyLogOdds;
    float minHeight;
    float maxHeight;
    uint32_t lastUpdate;
    uint8_t flags;
};

std::vector<Cell> grid(width * height);
```

La struttura è un esempio semplificato: nella versione reale distinguerei anche il terreno osservato dagli ostacoli e lo spazio non ancora esplorato. L'occupazione, infatti, non deve essere considerata nota prima delle misurazioni.

L'indice di accesso, per un array contiguo, sarebbe:

\[
index = y\cdot width+x
\]

Con un Ring Buffer, invece, prima traduciamo le coordinate logiche in indici fisici mediante gli offset circolari.

Il risultato è sempre un accesso \(O(1)\).

## 2. Come organizzerei i dati: Structure of Arrays (SoA)

Rispetto a un array di strutture `Cell`, farei un'ulteriore ottimizzazione: memorizzerei le proprietà delle celle in array separati.

```cpp
struct Grid25D {
    int width, height;

    std::vector<float> occupancy;
    std::vector<float> groundHeight;
    std::vector<float> obstacleMinHeight;
    std::vector<float> obstacleMaxHeight;

    std::vector<uint32_t> lastUpdate;
    std::vector<uint8_t> flags;

    int offsetX = 0;
    int offsetY = 0;
};
```

Questo approccio si chiama **Structure of Arrays (SoA)**.

Il vantaggio è che, quando aggiorni soltanto le probabilità di occupazione, puoi leggere un array contiguo senza caricare necessariamente anche tutte le altre proprietà delle celle.

Inoltre, permette di sfruttare meglio SIMD e operazioni vettorializzate in alcune elaborazioni.

Non è sempre più veloce di Array of Structures: dipende dal pattern di accesso. Per questo confronterei le due implementazioni con benchmark.

## 3. Come funzionerebbe il Ring Buffer?

Supponiamo di avere una griglia 200 × 200 celle.

Quando l'utente cammina di un metro, anziché spostare fisicamente tutti i 40.000 elementi, aggiorniamo l'origine logica della griglia.

Gli indici fisici diventano:

\[
i_x=(x+offsetX)\bmod width
\]

\[
i_y=(y+offsetY)\bmod height
\]

E l'indice lineare:

\[
index=i_y\cdot width+i_x
\]

In questo modo lo spostamento della finestra non richiede una copia completa.

Bisogna soltanto reinizializzare le righe o le colonne entrate nella nuova area, marcandole come sconosciute.

Questa strategia è già implementata in <Entity category="software" value="grid_map" disambig="Libreria C++ di robotica per mappe 2.5D"/> di ANYbotics, che utilizza proprio mappe multistrato e buffer circolari bidimensionali. <Cite refs={["turn900846search0","turn900846search4"]}/>

## 4. Quali dati conserverei nella griglia?

| Layer | Tipo | Scopo |
|---|---|---|
| Occupancy log-odds | `float32` | Probabilità di occupazione |
| Ground elevation | `float32` | Altezza del terreno |
| Elevation variance | `float32` | Incertezza sull'altezza |
| Obstacle min/max height | 2 × `float32` | Ingombro verticale |
| Last update | `uint32` | Età delle osservazioni |
| Flags | `uint8` | Stati e validità delle celle |

Per un ostacolo che presenta più intervalli verticali separati, una coppia min/max può essere insufficiente. In quel caso aggiungerei una piccola maschera verticale a bit, oppure ricorrerei a voxel locali soltanto nelle zone complesse.

Per gli oggetti in movimento manterrei invece una struttura separata:

```cpp
struct TrackedObject {
    uint32_t id;

    Eigen::Vector4f state;  // x, y, vx, vy
    Eigen::Matrix4f covariance;

    float lastSeen;
};
```

Questa separazione è importante: **la griglia rappresenta lo spazio; il tracker rappresenta gli oggetti che si muovono nello spazio**.

Non memorizzerei quindi una matrice di covarianza di Kalman dentro ogni cella.

## 5. Quanto costerebbe?

Prendiamo una mappa locale di 20 × 20 metri con risoluzione di 10 cm.

<box border radius="lg" padding={3} gap={2}>
  <text weight="medium">Configurazione di esempio</text>
  <grid columns={2} gap={2}>
    <grid-item>
      <box background="surface-secondary" radius="lg" padding={3} gap={1}>
        <text color="secondary" size="xs">Celle</text>
        <title size="xl" tabularNums>40.000</title>
      </box>
    </grid-item>
    <grid-item>
      <box background="surface-secondary" radius="lg" padding={3} gap={1}>
        <text color="secondary" size="xs">Memoria dei layer</text>
        <title size="xl" tabularNums>~0,8 MiB</title>
      </box>
    </grid-item>
  </grid>
  <caption>Stima per 21 byte per cella nei sette canali numerici dell'esempio, senza overhead, allineamento, buffer di acquisizione o dati del tracker.</caption>
</box>

Anche aggiungendo lo stato dei filtri di Kalman per gli oggetti tracciati, la memoria della rappresentazione resterebbe contenuta.

Il carico computazionale dipenderebbe soprattutto da quante celle vengono aggiornate per osservazione, dalla ricostruzione della profondità e dalla previsione delle collisioni, non dall'accesso alla struttura dati.

## 6. Confronto con altre strutture

| Struttura | Accesso | Quando la sceglierei |
|---|---|---|
| **Array contiguo + Ring Buffer** | \(O(1)\) | Mappa locale densa, aggiornamenti frequenti |
| Quadtree | \(O(\log N)\) tipico, se bilanciato | Mappa 2D ampia e sparsa |
| Octree | Dipende dalla profondità | Ricostruzione volumetrica 3D |
| Hash Grid | \(O(1)\) medio | Mappa sparsa o area estesa |
| Matrice dinamica ridimensionabile | \(O(1)\) accesso | Mappa piccola con dimensioni variabili |

Non utilizzerei un Quadtree soltanto per ridurre la memoria: su una finestra locale relativamente piccola e densa, i nodi e i puntatori possono introdurre più overhead di quanto risparmino.

---

## 7. Una libreria da cui partire

Vi suggerisco di guardare direttamente <Link url="https://github.com/ANYbotics/grid_map" title="ANYbotics/grid_map su GitHub"/>.

È una libreria C++ per mappe 2.5D che offre già una struttura multistrato e un buffer circolare. Se utilizzate ROS 2, può evitare di dover implementare da zero tutta la gestione della mappa.

Come riferimento alternativo, <Entity category="software" value="Nav2" disambig="Stack di navigazione robotica ROS 2"/> dispone di rolling costmap e layer per informazioni sugli ostacoli. <Cite refs={["turn900846search6","turn900846search1"]}/>

**La mia scelta definitiva per voi sarebbe:**

\[
\boxed{\text{Rolling Grid 2.5D}+\text{SoA}+\text{Ring Buffer}}
\]

Con una tabella separata di oggetti tracciati e filtri di Kalman.

È una struttura semplice, prevedibile in memoria e adatta agli aggiornamenti locali frequenti. Inoltre permette di aggiungere successivamente classificazione gerarchica e mappe predittive del rischio senza riprogettare completamente la rappresentazione spaziale.

---

**User:**

Fammi una descrizione completa del progetto, con filtri e strutture dati concordate in modo che possa presentarlo al mio team per l’implementazione 

---

**Assistant:**

Organizzo la proposta come una specifica tecnica per il team: architettura, strutture dati, filtri, flusso real-time, stima del rischio, requisiti hardware, roadmap e criteri di test. Distinguerò ciò che abbiamo scelto come base dalle parti ancora da validare sperimentalmente.

---

**Assistant:**

# Progetto: Sistema intelligente di navigazione assistiva con mappatura probabilistica 2.5D

Di seguito trovi una proposta architetturale pensata per essere discussa direttamente con il team di sviluppo.

L'idea originale viene mantenuta, ma è stata estesa con le soluzioni individuate durante la nostra discussione: **Rolling Grid 2.5D, Ring Buffer, Structure of Arrays, filtri di Kalman, classificazione gerarchica, inferenza bayesiana, MLE/MAP e predizione probabilistica delle collisioni**.

La proposta distingue l'architettura di riferimento dalle ottimizzazioni successive, per consentire al team di realizzare un primo prototipo senza dover implementare immediatamente tutti i componenti.

<box border radius="xl" padding={3} gap={2}>
  <text weight="medium" size="sm">Architettura generale proposta</text>
  <box background="surface-secondary" padding={3} radius="lg" align="center" gap={1}>
    **Sensori RGB-D + IMU**
    <caption>Immagini, profondità, accelerazione e orientamento</caption>
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="surface-secondary" padding={3} radius="lg" align="center">
    **Percezione geometrica + stima del moto dell'utente**
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <grid columns={2} gap={2}>
    <grid-item>
      <box border radius="lg" padding={3} gap={1} height="100%">
        <text weight="medium" size="sm">Mappa 2.5D</text>
        <caption>Occupancy Grid, log-odds, Ring Buffer, SoA</caption>
      </box>
    </grid-item>
    <grid-item>
      <box border radius="lg" padding={3} gap={1} height="100%">
        <text weight="medium" size="sm">Tracking dinamico</text>
        <caption>Kalman, velocità, covarianze, traiettorie</caption>
      </box>
    </grid-item>
  </grid>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="surface-secondary" padding={3} radius="lg" align="center" gap={1}>
    **Modelli comportamentali gerarchici**
    <caption>Classificazione asincrona, MLE/MAP, parametri condivisi</caption>
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="rgba(38,115,180,0.07)" padding={3} radius="lg" border align="center" gap={1}>
    **Predizione del rischio di collisione**
    <caption>Posizioni future, incertezza, tempo alla collisione</caption>
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="surface-secondary" padding={3} radius="lg" align="center">
    **Feedback aptico e vocale**
  </box>
  <caption>La percezione geometrica resta il percorso primario: il riconoscimento semantico deve arricchire le previsioni, non bloccare il rilevamento degli ostacoli.</caption>
</box>

La base tecnica proposta ha già riferimenti concreti nell'ecosistema robotico. Ad esempio, la libreria <Entity category="software" value="grid_map" disambig="Libreria C++ ANYbotics per mappe robotiche multistrato 2.5D"/> implementa mappe multistrato mediante buffer circolari; <Entity category="software" value="Nav2" disambig="Framework di navigazione robotica ROS 2"/> utilizza costmap con layer per ostacoli, voxel e margini di sicurezza. <Cite refs={["turn809964search0","turn809964search7"]}/>

## Specifica tecnica per il team

<WritingBlock id="74621" variant="document"># Progetto — Adaptive Spatio-Temporal Risk Mapping

**Sistema intelligente di navigazione assistiva per persone non vedenti**

**Stato:** proposta architetturale per l'implementazione di un prototipo sperimentale  
**Approccio:** computer vision, robotica probabilistica, tracking e previsione dinamica  
**Obiettivo:** realizzare un sistema leggero, modulare e capace di funzionare in tempo reale.

---

# 1. Descrizione generale

Il progetto consiste nello sviluppo di un sistema di navigazione assistiva, integrabile in occhiali intelligenti, capace di ricostruire l'ambiente circostante, rilevare ostacoli statici e dinamici e prevedere potenziali collisioni con l'utente.

La caratteristica principale del progetto è il passaggio da un sistema di semplice *obstacle detection* a un sistema di **predictive collision risk assessment**.

Non vogliamo limitarci a identificare se davanti all'utente sia presente un ostacolo. Vogliamo stimare come evolverà l'ambiente nei prossimi secondi e se, continuando lungo una determinata traiettoria, l'utente potrebbe entrare in collisione con esso.

Per ottenere questo risultato utilizzeremo una rappresentazione probabilistica dello spazio, combinata con modelli dinamici e algoritmi di stima ricorsiva.

Il sistema dovrà funzionare localmente, senza dipendere necessariamente da una connessione Internet.

**Il dispositivo sarà progettato come ausilio supplementare e non come sostituto del bastone bianco o delle competenze di orientamento e mobilità.**

# 2. Obiettivi del sistema

Gli obiettivi principali sono:

1. Ricostruire continuamente una rappresentazione locale dell'ambiente.
2. Distinguere le zone libere, occupate e non osservate.
3. Identificare ostacoli a diverse altezze, inclusi quelli sospesi.
4. Stimare posizione, direzione e velocità degli ostacoli dinamici.
5. Compensare il movimento della telecamera causato dallo spostamento della testa e dell'utente.
6. Prevedere la posizione futura degli oggetti.
7. Calcolare la probabilità di collisione entro un orizzonte temporale definito.
8. Generare feedback aptici o vocali in modo selettivo.
9. Ridurre il carico computazionale attraverso strutture dati compatte e algoritmi ricorsivi.
10. Gestire esplicitamente l'incertezza dei sensori e delle previsioni.

# 3. Architettura hardware

Per il primo prototipo proponiamo tre componenti hardware fondamentali.

## 3.1 Telecamera RGB-D

Il sensore RGB-D fornisce immagini a colori e una stima della profondità dei punti osservati.

La componente RGB può essere utilizzata per il riconoscimento semantico, mentre la profondità permette di ricostruire la geometria dell'ambiente senza dover necessariamente classificare ogni oggetto.

La presenza di un sensore di profondità è una scelta importante: riduce la dipendenza da modelli monoculari di stima della distanza.

## 3.2 Unità di misura inerziale — IMU

L'IMU acquisisce accelerazioni e velocità angolari.

Verrà utilizzata, insieme alle osservazioni visive, per stimare il movimento del dispositivo e distinguere il movimento apparente degli ostacoli da quello prodotto dall'utente.

La sola IMU non è sufficiente a stimare senza deriva la posizione a lungo termine; occorre combinarla con una tecnica di visual odometry o visual-inertial odometry.

## 3.3 Unità di elaborazione

Per il primo prototipo consigliamo di separare gli occhiali dall'unità di calcolo.

La telecamera e l'IMU saranno montate sul dispositivo indossabile, mentre l'elaborazione potrà essere eseguita su uno smartphone compatibile o su una scheda embedded dedicata.

Questa scelta permette di sviluppare e misurare gli algoritmi prima di affrontare i vincoli definitivi di peso, dissipazione e autonomia degli occhiali.

# 4. Struttura dati principale: Rolling Occupancy Grid 2.5D

## 4.1 Motivazione

Una matrice completamente tridimensionale può richiedere una quantità di memoria e un costo di aggiornamento superiori a quelli necessari per una navigazione locale.

Proponiamo quindi una **Rolling Grid 2.5D**, cioè una griglia bidimensionale nella quale ogni cella conserva più informazioni relative alla geometria verticale.

La matrice rappresenterà un'area locale attorno all'utente e verrà aggiornata mentre questo si sposta.

## 4.2 Organizzazione della memoria

La struttura sarà implementata mediante:

- Array contigui.
- Structure of Arrays (SoA).
- Buffer circolare bidimensionale.
- Allocazione iniziale della memoria.
- Gestione delle celle mediante indici interi.

Ogni attributo della mappa sarà conservato in un array dedicato.

Esempio concettuale in C++:

```cpp
struct Grid25D {
    int width;
    int height;
    float resolution;

    std::vector<float> occupancyLogOdds;
    std::vector<float> groundElevation;
    std::vector<float> elevationVariance;

    std::vector<float> obstacleMinHeight;
    std::vector<float> obstacleMaxHeight;

    std::vector<uint32_t> lastUpdate;
    std::vector<uint8_t> flags;

    int offsetX = 0;
    int offsetY = 0;
};
```

I vettori dovranno essere dimensionati all'inizializzazione e riutilizzati durante l'esecuzione.

L'accesso alle celle deve avere complessità O(1).

L'utilizzo di SoA consente inoltre di elaborare separatamente gli attributi della mappa, favorendo accessi contigui alla memoria e, dove applicabile, ottimizzazioni SIMD.

## 4.3 Informazioni conservate

Ogni cella conterrà:

| Attributo | Significato |
|---|---|
| Occupancy log-odds | Probabilità di occupazione in forma logaritmica |
| Ground elevation | Altezza stimata del terreno |
| Elevation variance | Incertezza sulla stima del terreno |
| Minimum obstacle height | Altezza minima dell'ostacolo rilevato |
| Maximum obstacle height | Altezza massima dell'ostacolo rilevato |
| Last update | Ultimo aggiornamento valido |
| Flags | Stato della cella e validità dei dati |

La rappresentazione min/max non è sufficiente a descrivere ogni geometria verticale. Per ostacoli complessi o sospesi sarà possibile aggiungere una maschera di occupazione verticale a pochi bit oppure un piccolo volume voxel locale.

Dovremo distinguere esplicitamente tra **spazio libero, occupato e sconosciuto**. Una cella non osservata non potrà essere automaticamente interpretata come libera.

## 4.4 Ring Buffer

La griglia dovrà seguire lo spostamento dell'utente.

Per evitare di copiare continuamente tutta la matrice, utilizzeremo un Ring Buffer.

Quando l'utente si muove, modifichiamo gli offset logici della griglia e reinizializziamo soltanto le nuove righe o colonne entrate nell'area osservabile.

Gli indici fisici sono determinati tramite:

\[
i_x=(x+offsetX)\bmod W
\]

\[
i_y=(y+offsetY)\bmod H
\]

Il Ring Buffer deve essere mantenuto in un sistema di riferimento locale continuo, per evitare che la rotazione della testa o correzioni improvvise della localizzazione spostino artificialmente gli ostacoli.

## 4.5 Aggiornamento bayesiano della mappa

Per rappresentare l'occupazione utilizzeremo una formulazione in log-odds.

\[
L_t=L_{t-1}+
\log\frac{p_t}{1-p_t}-L_0
\]

Dove:

- \(L_t\) rappresenta la log-odds aggiornata.
- \(p_t\) è la probabilità di occupazione stimata dal modello inverso del sensore.
- \(L_0\) rappresenta la log-odds della probabilità a priori.

La mappa potrà così essere aggiornata ricorsivamente senza conservare tutte le osservazioni precedenti.

Le celle dovranno essere aggiornate distinguendo le misurazioni che indicano un ostacolo dai raggi che confermano spazio libero. La perdita delle osservazioni non deve essere interpretata come prova che un ostacolo sia scomparso.

# 5. Tracking degli ostacoli dinamici

La mappa geometrica descrive dove si trovano gli ostacoli, ma non è sufficiente a prevedere come si muoveranno.

Per questo manterremo una struttura dati separata, dedicata agli oggetti tracciati.

## 5.1 Struttura TrackedObject

```cpp
struct TrackedObject {
    uint32_t id;

    Eigen::Vector4f state;
    Eigen::Matrix4f covariance;

    float radius;
    float confidence;

    uint64_t lastSeenNs;
    uint32_t modelId;
};
```

Lo stato iniziale sarà:

\[
x_t=[x,y,v_x,v_y]^T
\]

Per ogni oggetto conserveremo anche la covarianza, un'approssimazione delle dimensioni e le informazioni necessarie ad associare le nuove osservazioni al tracciato esistente.

Gli oggetti dinamici saranno gestiti in una struttura contigua o in un pool di slot riutilizzabili, associato a una tabella ID → indice.

Questo consente di evitare allocazioni continue e di rimuovere i tracciati non più validi.

## 5.2 Data association

Un problema da risolvere è identificare se un ostacolo osservato in un nuovo frame corrisponde a un oggetto già tracciato.

Per il primo prototipo proponiamo:

1. Predizione della posizione degli oggetti esistenti.
2. Associazione delle nuove misurazioni usando distanza geometrica e incertezza.
3. Correzione dei filtri associati.
4. Creazione di nuovi tracciati per le osservazioni non associate.
5. Scadenza dei tracciati rimasti non osservati troppo a lungo.

Per le associazioni può essere utilizzata una distanza di Mahalanobis con soglie di gating.

Il metodo di assegnazione iniziale potrà essere greedy; successivamente si potrà valutare l'algoritmo ungherese per scene più affollate.

La perdita di un tracciato non deve cancellare automaticamente la presenza dell'ostacolo dalla mappa.

# 6. Filtri di Kalman

Il filtro di Kalman costituirà il principale algoritmo di stima dello stato dinamico.

## 6.1 Obiettivo

Stimare continuamente posizione e velocità degli oggetti, correggendo le previsioni quando arrivano nuove misurazioni.

Il vantaggio è che non occorre conservare tutta la sequenza temporale delle posizioni precedenti.

Nel modello lineare-gaussiano, stato e covarianza riassumono le informazioni rilevanti necessarie al passo successivo.

## 6.2 Modello iniziale

Utilizzeremo un modello a velocità quasi costante.

La matrice di transizione sarà:

\[
F=
\begin{bmatrix}
1&0&\Delta t&0\\
0&1&0&\Delta t\\
0&0&1&0\\
0&0&0&1
\end{bmatrix}
\]

Il filtro eseguirà due operazioni principali.

**Predizione dello stato:**

\[
\hat x_t^-=F\hat x_{t-1}
\]

**Predizione della covarianza:**

\[
P_t^-=FP_{t-1}F^T+Q
\]

Quando sarà disponibile una nuova osservazione:

\[
K_t=P_t^-H^T(HP_t^-H^T+R)^{-1}
\]

\[
\hat x_t=\hat x_t^-+K_t(z_t-H\hat x_t^-)
\]

Dove \(Q\) descrive il rumore del processo e \(R\) quello della misurazione.

Per stabilità numerica, la covarianza potrà essere aggiornata mediante la forma di Joseph.

## 6.3 Evoluzioni possibili

Il primo prototipo utilizzerà il Kalman Filter lineare.

Successivamente valuteremo:

- Extended Kalman Filter (EKF), per modelli non lineari.
- Unscented Kalman Filter (UKF), per non linearità significative.
- Interacting Multiple Model (IMM), per combinare differenti modelli di movimento.

Non introdurremo filtri più complessi senza evidenze sperimentali che giustifichino il loro costo.

# 7. Riconoscimento semantico asincrono

Il riconoscimento degli oggetti rappresenta uno dei componenti potenzialmente più costosi.

Per questo motivo verrà separato dal tracking geometrico.

Il sistema dovrà essere capace di rilevare e segnalare un ostacolo anche senza conoscerne la classe semantica.

Proponiamo due processi indipendenti:

**Processo veloce**

- Elaborazione delle misurazioni geometriche.
- Aggiornamento della mappa.
- Tracking degli ostacoli.
- Predizione delle traiettorie.
- Valutazione del rischio.

**Processo lento**

- Object recognition.
- Aggiornamento delle classi semantiche.
- Selezione del modello comportamentale.
- Eventuale raffinamento delle previsioni.

Il riconoscimento semantico dovrà funzionare in maniera asincrona, senza bloccare il processo di rilevazione geometrica.

Sarà inoltre possibile attivarlo con frequenza adattiva, concentrando le risorse sugli oggetti che presentano maggiore incertezza o rilevanza per il percorso.

# 8. Classificazione gerarchica degli oggetti

Per organizzare le classi semantiche utilizzeremo una gerarchia probabilistica, anziché considerare ogni categoria completamente indipendente.

Non costruiremo una tassonomia puramente biologica o descrittiva.

La classificazione sarà orientata alle proprietà rilevanti per la navigazione.

Esempio:

```text
Oggetto rilevato
│
├── Struttura o ostacolo prevalentemente statico
│   ├── Elemento strutturale
│   └── Oggetto spostabile
│
└── Oggetto potenzialmente dinamico
    ├── Movimento vincolato
    └── Movimento meno prevedibile
```

Questa struttura è concettuale. In implementazione, la classe semantica e lo stato di movimento dovranno rimanere attributi separati.

Per esempio, una bicicletta è semanticamente una bicicletta sia quando è parcheggiata sia quando è in movimento.

La gerarchia sarà utilizzata per selezionare un modello comportamentale adeguato e permettere la condivisione dei parametri tra classi simili.

La classificazione potrà fermarsi a un livello intermedio quando una distinzione più dettagliata non aggiunge informazioni utili per la sicurezza.

Un albero bilanciato può ridurre a O(log C) il numero di decisioni gerarchiche per una singola classificazione, assumendo costo limitato per nodo e un solo ramo visitato. Tuttavia, questa ottimizzazione non implica che l'intera pipeline di computer vision abbia complessità logaritmica.

# 9. Maximum Likelihood e Maximum A Posteriori

La proposta prevede di utilizzare MLE e MAP per stimare i parametri dei modelli dinamici.

## 9.1 Motivazione

Non vogliamo stabilire manualmente che una persona ha, per esempio, una probabilità fissa del 70% di muoversi.

Vogliamo apprendere dai dati come evolvono posizione e velocità degli oggetti, tenendo conto del contesto.

## 9.2 Maximum Likelihood

Sia \(\theta\) il vettore dei parametri di un modello predittivo.

Stimiamo:

\[
\hat\theta_{MLE}=
\arg\max_\theta
\sum_{i=1}^{N}\log p(y_i\mid X_i,\theta)
\]

Dove \(X_i\) contiene le caratteristiche osservate e \(y_i\) rappresenta il comportamento futuro effettivamente misurato.

## 9.3 Maximum A Posteriori

Quando disponiamo di pochi dati o conoscenze precedenti, possiamo utilizzare:

\[
\hat\theta_{MAP}=
\arg\max_\theta
\left[
\log P(D\mid\theta)+\log P(\theta)
\right]
\]

Questo approccio permette di regolarizzare i modelli e condividere informazioni tra categorie correlate.

## 9.4 Modelli gerarchici

Per evitare un modello completamente indipendente per ciascuna classe, proponiamo una struttura parametrica gerarchica.

\[
\theta_c=\theta_{parent}+\Delta_c
\]

Ogni classe eredita quindi una base comune e aggiunge soltanto correzioni specifiche.

In questo modo possiamo riutilizzare parte dell'apprendimento e limitare la quantità di parametri.

# 10. Aggiornamento ricorsivo dei parametri

Se il modello comportamentale contiene pochi parametri, potremo valutare il Recursive Least Squares (RLS) per aggiornamenti incrementali.

RLS consente di aggiornare le stime senza conservare tutto il dataset precedente.

Per \(d\) parametri, l'aggiornamento della matrice completa richiede tipicamente O(d²) operazioni e O(d²) memoria.

Per ridurre ulteriormente la memoria potremo valutare covarianze diagonali o approssimazioni a basso rango.

È importante distinguere:

- Covarianza dello stato: incertezza sulla posizione e velocità di un ostacolo.
- Covarianza dei parametri: incertezza sui pesi del modello predittivo.

Sono due oggetti matematici differenti.

**Decisione progettuale:** nel primo prototipo i parametri comportamentali saranno addestrati offline e mantenuti fissi durante l'uso.

Gli aggiornamenti online dei parametri verranno valutati in una fase successiva, dopo aver verificato stabilità, robustezza e qualità delle osservazioni.

# 11. Predizione del rischio di collisione

Questa rappresenta la funzionalità centrale del progetto.

Il sistema dovrà stimare non semplicemente se un oggetto sia mobile, ma se il suo movimento possa interferire con quello dell'utente.

## 11.1 Informazioni necessarie

Per ogni ostacolo considereremo:

- Posizione e dimensioni.
- Velocità relativa.
- Direzione del movimento.
- Distribuzione delle possibili posizioni future.
- Incertezza delle stime.

Per l'utente considereremo:

- Posizione.
- Velocità e direzione di avanzamento.
- Ingombro corporeo.
- Possibili traiettorie a breve termine.
- Incertezza sulla direzione futura.

## 11.2 Formulazione probabilistica

L'obiettivo è stimare:

\[
P(C_{[0,T]}\mid Z_{1:t},\pi)
\]

Dove:

- \(C_{[0,T]}\) indica una collisione entro l'orizzonte temporale \(T\).
- \(Z_{1:t}\) rappresenta le osservazioni disponibili.
- \(\pi\) rappresenta una possibile traiettoria dell'utente.

La collisione avviene quando le regioni occupate dall'utente e da un ostacolo si sovrappongono nello stesso istante.

## 11.3 Implementazione pratica

Per il primo prototipo proponiamo:

1. Predire le posizioni dell'utente e degli ostacoli a intervalli temporali discreti.
2. Propagare le covarianze dei modelli dinamici.
3. Rappresentare ciascun ostacolo con una geometria semplificata, per esempio cerchio o rettangolo.
4. Aggiungere un margine di sicurezza all'ingombro dell'utente.
5. Valutare la distanza prevista e la possibilità di sovrapposizione negli istanti futuri.
6. Aggregare le informazioni in un indicatore di rischio per il percorso.

Potremo iniziare con un indicatore conservativo basato su distanza, tempo alla collisione e incertezza.

Successivamente, mediante integrazione probabilistica o campionamento Monte Carlo, potremo stimare una probabilità di collisione vera e propria.

Non dovremo interpretare un semplice punteggio euristico come probabilità calibrata: quest'ultima richiede un modello probabilistico e una validazione sperimentale.

## 11.4 Ostacoli statici

Gli ostacoli statici non richiedono necessariamente un tracker dinamico individuale.

Il rischio sarà calcolato confrontando la geometria della mappa con le possibili traiettorie dell'utente.

## 11.5 Gestione dell'incertezza

Quando le osservazioni sono insufficienti, il sistema deve aumentare il livello di cautela, anziché assumere che il percorso sia sicuro.

In particolare:

- Le zone sconosciute non saranno trattate come libere.
- Le previsioni senza correzioni avranno incertezza crescente.
- Le misurazioni non affidabili non dovranno cancellare ostacoli confermati.
- Un errore del riconoscimento semantico non dovrà impedire il funzionamento del rilevamento geometrico.

# 12. Feedback all'utente

Il sistema di feedback dovrà fornire informazioni brevi, tempestive e non invasive.

Proponiamo due modalità:

**Feedback aptico:** segnalazioni direzionali e avvisi immediati.

**Feedback vocale:** messaggi sintetici per informazioni più complesse.

L'urgenza della segnalazione dipenderà da un insieme di fattori:

- Rischio di collisione.
- Tempo previsto all'impatto.
- Distanza dall'ostacolo.
- Affidabilità della previsione.
- Disponibilità di un percorso alternativo sufficientemente osservato.

Le regole iniziali saranno conservative e configurabili. Le soglie numeriche definitive dovranno essere stabilite mediante test.

Non forniremo indicazioni di attraversamento o dichiarazioni di sicurezza quando il sistema non possiede informazioni sufficienti.

# 13. Pipeline di elaborazione real-time

La pipeline dovrà essere progettata per evitare che componenti lenti blocchino quelli critici.

```text
RGB-D + IMU
      |
      v
Acquisizione e sincronizzazione
      |
      v
Stima del movimento del dispositivo
      |
      v
Ricostruzione geometrica
      |
      +-----------------------------+
      |                             |
      v                             v
Rolling Grid 2.5D          Rilevamento e tracking
      |                             |
      |                       Kalman Filter
      |                             |
      |                       Modello dinamico
      |                             |
      +--------------+--------------+
                     |
                     v
             Risk Prediction
                     |
                     v
              Feedback Engine

Pipeline parallela:
RGB -> Object Recognition -> Classificazione
                |
                v
       Modelli comportamentali
```

## 13.1 Frequenze indicative

Le seguenti frequenze rappresentano obiettivi iniziali, da misurare e verificare sull'hardware scelto.

| Componente | Obiettivo indicativo |
|---|---|
| Acquisizione RGB-D | 15–30 FPS |
| Aggiornamento geometrico | 10–30 Hz |
| Tracking e predizione | 20–30 Hz |
| Riconoscimento semantico | 2–5 Hz |
| Valutazione del rischio | 10–20 Hz |
| Feedback | Event-driven |

La pipeline dovrà scartare o sostituire le osservazioni obsolete quando necessario, evitando l'accumulo illimitato di frame in coda.

Tutti i dati dovranno avere timestamp monotoni e dovranno essere trasformati in sistemi di riferimento coerenti.

# 14. Analisi computazionale

La memoria sarà dominata principalmente dalle mappe, dai buffer dei sensori e dai modelli di percezione.

Il solo stato matematico del filtro di Kalman è relativamente piccolo.

Per un filtro con quattro variabili:

- Stato: 4 float32.
- Covarianza: 16 float32.
- Totale numerico: 80 byte.

Il costo cresce linearmente con il numero di filtri indipendenti, mantenendo fissa la dimensione dello stato.

## 14.1 Esempio della mappa

Configurazione iniziale proposta:

- Area quadrata: 20 × 20 metri.
- Risoluzione: 10 centimetri.
- Numero di celle: 40.000.
- Dati di base: 21 byte per cella nella rappresentazione SoA illustrata.

La memoria minima dei layer è quindi:

\[
40.000 \times 21 = 840.000\text{ byte}
\]

Circa 0,80 MiB, esclusi overhead, buffer e strutture aggiuntive.

La configurazione potrà essere modificata in funzione della portata effettiva dei sensori e della velocità di movimento dell'utente.

## 14.2 Principali costi

I componenti che richiederanno maggiore attenzione saranno:

1. Elaborazione RGB-D.
2. Stima del movimento del dispositivo.
3. Segmentazione e associazione degli ostacoli.
4. Riconoscimento semantico.
5. Predizione probabilistica delle collisioni.

Il filtro di Kalman e l'accesso alla griglia non dovrebbero rappresentare i principali colli di bottiglia, ma dovranno comunque essere misurati.

# 15. Stack tecnologico proposto

Per il nucleo real-time consigliamo C++.

La motivazione principale è il controllo sull'allocazione della memoria, sui layout dei dati e sulle prestazioni degli algoritmi numerici.

| Componente | Tecnologia |
|---|---|
| Core di elaborazione | C++20 |
| Algebra lineare | Eigen |
| Computer vision | OpenCV |
| Griglia 2.5D | ANYbotics grid_map o implementazione custom |
| Filtro di Kalman | Implementazione con Eigen o OpenCV |
| Ricerca e integrazione | ROS 2, opzionale |
| Addestramento MLE/MAP | Python, NumPy, SciPy, PyTorch se necessario |
| Simulazione e visualizzazione | RViz o visualizzatore dedicato |
| Testing | GoogleTest, benchmark e replay di dati registrati |

Suggeriamo di utilizzare ROS 2 come infrastruttura di prototipazione, non necessariamente come dipendenza del prodotto finale.

Il core matematico dovrebbe rimanere indipendente da ROS, per facilitare la migrazione verso hardware embedded.

# 16. Modularizzazione del software

Proponiamo la seguente organizzazione:

```text
assistive-navigation/
│
├── sensors/
│   ├── rgbd/
│   ├── imu/
│   └── synchronization/
│
├── localization/
│   ├── visual_odometry/
│   └── motion_estimation/
│
├── mapping/
│   ├── rolling_grid/
│   ├── occupancy/
│   └── elevation/
│
├── perception/
│   ├── geometric_detection/
│   ├── object_recognition/
│   └── data_association/
│
├── tracking/
│   ├── kalman/
│   └── track_manager/
│
├── prediction/
│   ├── motion_models/
│   ├── hierarchical_models/
│   └── risk_estimation/
│
├── feedback/
│   ├── haptic/
│   └── speech/
│
├── common/
│   ├── geometry/
│   ├── timestamps/
│   └── messages/
│
├── simulation/
├── tests/
├── benchmarks/
└── docs/
```

I moduli dovranno comunicare tramite interfacce chiare, evitando dipendenze circolari.

Le strutture dati condivise dovranno usare timestamp e sistemi di coordinate documentati.

# 17. Piano di implementazione

## Fase 1 — MVP geometrico

Implementare:

- Acquisizione RGB-D.
- Acquisizione IMU.
- Sincronizzazione dei sensori.
- Stima iniziale del movimento del dispositivo.
- Rolling Grid 2.5D.
- Occupancy Grid con aggiornamento log-odds.
- Visualizzazione della mappa.
- Rilevamento geometrico degli ostacoli.

**Risultato atteso:** il sistema rappresenta ostacoli e spazi liberi in una mappa locale che segue l'utente.

## Fase 2 — Tracking dinamico

Implementare:

- Rilevamento di oggetti mobili.
- Data association.
- Track manager.
- Kalman Filter.
- Predizione di posizione e velocità.
- Gestione della perdita temporanea delle osservazioni.

**Risultato atteso:** il sistema distingue il movimento dell'utente da quello degli ostacoli e mantiene tracciati coerenti nel tempo.

## Fase 3 — Predizione del rischio

Implementare:

- Stima della traiettoria dell'utente.
- Predizione temporale degli ostacoli.
- Calcolo della distanza futura.
- Valutazione del tempo alla collisione.
- Gestione dell'incertezza.
- Feedback preliminare.

**Risultato atteso:** il sistema produce segnalazioni anticipate per potenziali collisioni.

## Fase 4 — Classificazione e apprendimento

Implementare:

- Object recognition asincrono.
- Classificazione gerarchica.
- Modelli comportamentali condivisi.
- Addestramento MLE/MAP.
- Selezione adattiva dei modelli predittivi.

**Risultato atteso:** il sistema migliora la predizione utilizzando informazioni semantiche, senza renderle obbligatorie.

## Fase 5 — Ottimizzazione e validazione

Implementare:

- Benchmark computazionali.
- Profilazione CPU/GPU.
- Riduzione delle allocazioni.
- Test con scene affollate.
- Analisi dei consumi.
- Validazione della qualità probabilistica.
- Valutazione dell'interazione con gli utenti.

# 18. Strategia di testing

Il progetto dovrà essere verificato su tre livelli.

## 18.1 Test unitari

Testare indipendentemente:

- Conversione coordinate → indici.
- Spostamento del Ring Buffer.
- Aggiornamento log-odds.
- Predizione e correzione del Kalman.
- Associazione degli oggetti.
- Calcolo delle intersezioni geometriche.
- Gestione delle celle sconosciute.
- Comportamento in presenza di dati mancanti.

## 18.2 Test di integrazione

Utilizzare sequenze registrate per verificare l'intera pipeline.

Gli scenari includeranno:

- Muro frontale.
- Persona che attraversa.
- Bicicletta che si allontana.
- Persona che cambia improvvisamente direzione.
- Ostacolo sospeso.
- Gradino o dislivello negativo.
- Oggetto temporaneamente occultato.
- Movimento rapido della testa.
- Scarsa illuminazione.
- Perdita temporanea del sensore di profondità.

## 18.3 Metriche di valutazione

Le principali metriche saranno:

- Tasso di mancato rilevamento degli ostacoli pericolosi.
- Tasso di falsi allarmi.
- Accuratezza del tracking.
- Errore della posizione futura.
- Calibrazione delle probabilità di collisione.
- Tempo di anticipo delle segnalazioni.
- Latenza end-to-end.
- Utilizzo di CPU, GPU e memoria.
- Consumo energetico.
- Robustezza ai dati mancanti.

I test iniziali dovranno essere condotti in ambienti controllati, con supervisione e senza affidare la sicurezza dei partecipanti esclusivamente al prototipo.

Successivamente saranno necessari studi con persone non vedenti e professionisti dell'orientamento e mobilità, per valutare l'effettiva utilità e accessibilità del dispositivo.

# 19. Principali rischi tecnici

**Affidabilità della profondità.** Alcuni sensori possono funzionare male alla luce solare, con superfici riflettenti o trasparenti, oppure oltre una determinata distanza.

**Perdita di informazioni nella rappresentazione 2.5D.** Una cella con un solo intervallo verticale non descrive necessariamente geometrie complesse. Saranno necessarie rappresentazioni locali aggiuntive dove opportuno.

**Errori di localizzazione.** La deriva della visual odometry può creare ostacoli duplicati o spostati.

**Predizioni errate.** Il Kalman a velocità costante non può prevedere improvvisi cambi di direzione senza nuove osservazioni.

**Classificazione semantica.** Un errore nella classe di un oggetto può introdurre una previsione comportamentale errata. La geometria deve quindi rimanere il riferimento principale.

**Sicurezza delle segnalazioni.** Un basso punteggio di rischio non equivale necessariamente a percorso sicuro.

**Latenza e consumi.** Anche con strutture dati efficienti, computer vision e stima della profondità possono diventare il collo di bottiglia.

# 20. Decisioni architetturali

Le scelte raccomandate per il primo prototipo sono:

| Area | Decisione |
|---|---|
| Mappatura | Rolling Occupancy Grid 2.5D |
| Memoria | Structure of Arrays |
| Movimento della finestra | Ring Buffer |
| Occupazione | Aggiornamento bayesiano in log-odds |
| Localizzazione | Visual-inertial odometry |
| Tracking | Kalman Filter lineare |
| Gestione oggetti | Track manager separato |
| Classificazione | Asincrona, inizialmente opzionale |
| Struttura delle classi | Gerarchia probabilistica comportamentale |
| Addestramento | MLE/MAP offline |
| Adattamento online dei pesi | RLS soltanto dopo validazione |
| Rischio | Predizione delle traiettorie con incertezza |
| Feedback | Aptico e vocale, selettivo |
| Linguaggio core | C++20 |
| Infrastruttura iniziale | ROS 2 opzionale |

# 21. Conclusione

Il progetto propone un'architettura che combina mappatura probabilistica, tracking dinamico e predizione del rischio.

La scelta di una Rolling Grid 2.5D permette di limitare la memoria utilizzata per rappresentare l'ambiente.

I filtri di Kalman consentono di mantenere una stima ricorsiva degli oggetti senza conservare l'intera storia temporale.

La classificazione gerarchica permette di organizzare i modelli comportamentali e condividere parametri, mentre MLE e MAP possono essere utilizzati per apprenderli dai dati.

L'elemento centrale è la separazione tra **riconoscimento dell'oggetto** e **valutazione del suo rischio**.

Il sistema non deve necessariamente conoscere il nome di ogni ostacolo per stimare una possibile collisione.

L'obiettivo finale è un dispositivo capace di mantenere una rappresentazione dell'ambiente, prevedere l'evoluzione delle situazioni dinamiche e fornire segnalazioni tempestive, mantenendo controllabili memoria, carico computazionale e incertezza.

**Il principio guida è progettare un sistema che non si limiti a riconoscere ciò che si trova davanti all'utente, ma sia in grado di anticipare quando un ostacolo potrebbe diventare pericoloso.**</WritingBlock>

## Riferimenti tecnici per iniziare l'implementazione

I riferimenti più utili per il team sono <Link url="https://github.com/ANYbotics/grid_map" title="ANYbotics grid_map — mappe 2.5D e buffer circolari"/>, <Link url="https://docs.nav2.org/" title="Nav2 — costmap, obstacle layer e navigazione"/> e <Link url="https://octomap.github.io/" title="OctoMap — alternativa probabilistica 3D"/>. Il primo è particolarmente vicino alla struttura dati concordata. <Cite refs={["turn809964search0","turn809964search7","turn809964search3"]}/>

Segnalo inoltre lo studio <Link url="https://pubmed.ncbi.nlm.nih.gov/40100749/" title="NavWear (2025)"/>, dedicato a un ausilio indossabile basato su RGB-D e feedback aptico. È utile per impostare la valutazione dell'interazione con gli utenti, oltre a quella puramente algoritmica. <Cite ref="turn809964search12"/>

### Le tre decisioni da prendere nella prima riunione

Prima di scrivere il codice, il team dovrebbe fissare tre aspetti:

1. **Hardware di acquisizione:** quale sensore RGB-D e quale IMU utilizzare, verificando portata, campo visivo e funzionamento all'aperto.
2. **Piattaforma di elaborazione:** computer embedded o smartphone, in modo da fissare un budget reale di latenza, memoria ed energia.
3. **Ambito del primo MVP:** limitarsi inizialmente a ostacoli geometrici e tracking, rinviando riconoscimento gerarchico, apprendimento dei pesi e modelli avanzati di rischio.

La scelta che ritengo più importante è **non iniziare implementando la parte di machine learning**: prima costruirei una pipeline geometrica affidabile, misurabile e riproducibile. Solo dopo introdurrei i modelli probabilistici più sofisticati, confrontandoli con una baseline semplice per dimostrare che aggiungono un beneficio effettivo.

---

**User:**

L’albero gerarchico probabilistico per cosa va usato?

---

**Assistant:**

Nel nostro progetto, **l'albero gerarchico probabilistico serve a selezionare il modello di comportamento più adatto a un ostacolo**, senza dover necessariamente riconoscere con precisione ogni singolo oggetto.

Il suo compito principale non è mappare lo spazio né calcolare direttamente il rischio di collisione, ma **aiutare il sistema a prevedere come potrebbe muoversi un ostacolo**.

## 1. Come funzionerebbe concretamente?

Supponiamo che gli occhiali rilevino un oggetto davanti all'utente.

La Rolling Grid 2.5D ci dice dove si trova, mentre il filtro di Kalman ne stima posizione e velocità.

L'albero probabilistico aggiunge un'altra informazione: *che tipo di comportamento possiamo aspettarci da quell'oggetto?*

<box border radius="xl" padding={3} gap={2}>
  <box background="surface-secondary" radius="lg" padding={3} align="center">
    **Oggetto rilevato**
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <grid columns={2} gap={3}>
    <grid-item>
      <box gap={2}>
        <box background="rgba(32,140,105,0.09)" border radius="lg" padding={3} align="center">
          **Prevalentemente statico**
        </box>
        <box background="surface-secondary" radius="lg" padding={2} align="center">
          <text weight="medium" size="sm">Strutturale</text>
          <caption>Muro, colonna</caption>
        </box>
        <box background="surface-secondary" radius="lg" padding={2} align="center">
          <text weight="medium" size="sm">Spostabile</text>
          <caption>Sedia, carrello fermo</caption>
        </box>
      </box>
    </grid-item>
    <grid-item>
      <box gap={2}>
        <box background="rgba(220,145,45,0.09)" border radius="lg" padding={3} align="center">
          **Potenzialmente dinamico**
        </box>
        <box background="surface-secondary" radius="lg" padding={2} align="center">
          <text weight="medium" size="sm">Movimento vincolato</text>
          <caption>Veicolo in corsia</caption>
        </box>
        <box background="surface-secondary" radius="lg" padding={2} align="center">
          <text weight="medium" size="sm">Movimento variabile</text>
          <caption>Pedone, animale</caption>
        </box>
      </box>
    </grid-item>
  </grid>
  <caption>Schema concettuale: un oggetto può cambiare stato di movimento. La categoria semantica non deve essere confusa con la sua mobilità attuale.</caption>
</box>

L'albero può fornire più probabilità contemporaneamente. Per esempio, un oggetto potrebbe avere una probabilità del 75% di essere una persona e del 25% di essere un altro ostacolo mobile.

Invece di scegliere obbligatoriamente una sola classe, il sistema può mantenere entrambe le ipotesi.

## 2. Qual è il vantaggio rispetto al solo Kalman?

Il Kalman standard con modello a velocità costante prevede il movimento soprattutto sulla base dello stato osservato.

L'albero permette di introdurre **modelli dinamici differenti in funzione del comportamento presumibile dell'oggetto**.

| Oggetto | Modello potenzialmente utile |
|---|---|
| Muro | Posizione statica |
| Persona | Velocità variabile e cambi di direzione |
| Bicicletta | Movimento generalmente continuo, con possibili svolte |
| Automobile | Movimento soggetto a vincoli cinematici |

Questo non significa che una persona debba avere sempre un unico modello. L'albero può aiutare a selezionare o combinare diversi modelli.

Per esempio, potremmo utilizzare un filtro IMM (*Interacting Multiple Model*) per combinare un modello a velocità costante e uno con accelerazione, usando le probabilità del classificatore come informazione iniziale.

## 3. Dove entra in gioco MLE/MAP?

Supponiamo che il modello di movimento di una persona abbia parametri:

\[
\theta_{\text{persona}}
\]

E che il modello generale degli oggetti dinamici abbia parametri:

\[
\theta_{\text{dinamico}}
\]

Possiamo impostare:

\[
\theta_{\text{persona}}
=
\theta_{\text{dinamico}}
+
\Delta_{\text{persona}}
\]

In questo modo, i modelli dei figli ereditano informazioni dai nodi superiori.

**MLE/MAP serve a stimare questi parametri dai dati**, mentre l'albero permette di organizzarli e condividerli.

Questo è particolarmente vantaggioso quando alcune classi hanno pochi esempi di addestramento.

## 4. Come contribuisce al calcolo del rischio?

Il flusso sarebbe:

<box border radius="xl" padding={3} gap={2}>
  <box background="surface-secondary" radius="lg" padding={3} align="center" gap={1}>
    **Rolling Grid 2.5D**
    <caption>Rileva posizione e ingombro geometrico</caption>
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="surface-secondary" radius="lg" padding={3} align="center" gap={1}>
    **Kalman Filter**
    <caption>Stima posizione, velocità e incertezza</caption>
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="surface-secondary" radius="lg" padding={3} align="center" gap={1}>
    **Albero probabilistico**
    <caption>Determina quali modelli comportamentali siano plausibili</caption>
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="rgba(37,99,235,0.07)" border radius="lg" padding={3} align="center" gap={1}>
    **Predizione probabilistica**
    <caption>Combina le possibili traiettorie e le rispettive incertezze</caption>
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="surface-secondary" radius="lg" padding={3} align="center">
    **Probabilità di collisione**
  </box>
</box>

Matematicamente, se \(c\) indica una possibile classe comportamentale, possiamo stimare:

\[
\boxed{
P(C\mid Z)=
\sum_c P(C\mid c,Z)\,P(c\mid Z)
}
\]

Dove:

- \(P(c\mid Z)\) rappresenta la probabilità della classe, data l'osservazione.
- \(P(C\mid c,Z)\) rappresenta la probabilità di collisione condizionata alla classe.
- \(P(C\mid Z)\) rappresenta la probabilità complessiva di collisione.

L'espressione è una marginalizzazione sulle classi: nella pratica ogni termine dipenderebbe anche dalla traiettoria prevista dell'utente e dalle osservazioni del movimento.

Il sistema può così considerare più scenari possibili senza dover decidere con certezza quale oggetto abbia davanti.

## 5. Ma è davvero necessario?

**Per il primo prototipo, no.**

La Rolling Grid 2.5D, il tracking e il Kalman possono già permettere una prima previsione geometrica del rischio senza conoscere la categoria degli oggetti.

L'albero diventa interessante quando vogliamo migliorare la previsione del comportamento, soprattutto in presenza di oggetti con dinamiche differenti.

Inoltre, non garantisce automaticamente un risparmio computazionale: bisogna comunque eseguire il riconoscimento visivo e gestire le incertezze delle classificazioni. Se il numero di classi rimane piccolo, una struttura piatta potrebbe essere più semplice e altrettanto efficiente.

**Quindi, per il vostro team, lo definirei un modulo di ottimizzazione e raffinamento della predizione, non un componente indispensabile dell'MVP.**

La distinzione da tenere presente è:

- **Rolling Grid:** dove si trova l'ostacolo?
- **Kalman:** come si sta muovendo?
- **Albero gerarchico probabilistico:** quali comportamenti futuri sono plausibili, considerando anche la tipologia dell'oggetto?
- **Risk Prediction:** quali di questi comportamenti potrebbero causare una collisione con l'utente?

È questa la funzione concreta dell'albero nella vostra architettura.

---

**User:**

fammi una descrizione da scrivere come presentazione, descrizione veloce

---

**Assistant:**

<WritingBlock id="62741" variant="standard">Il progetto prevede lo sviluppo di un **sistema intelligente di navigazione assistiva per persone non vedenti**, capace di rilevare gli ostacoli e prevedere potenziali collisioni in tempo reale.

Il sistema utilizza una **Rolling Occupancy Grid 2.5D** per mappare l'ambiente circostante in modo efficiente, sfruttando strutture dati ottimizzate come Ring Buffer e Structure of Arrays (SoA).

Attraverso **filtri di Kalman**, vengono stimate posizione, velocità e traiettoria degli ostacoli, mentre un **albero gerarchico probabilistico** permette di classificare gli oggetti e selezionare modelli comportamentali appropriati, i cui parametri possono essere stimati mediante MLE/MAP.

L'obiettivo principale è sviluppare un modello di **Predictive Collision Risk Assessment**, capace di valutare la probabilità di collisione tra l'utente e gli ostacoli nei secondi successivi, considerando anche l'incertezza delle previsioni.

Il sistema è progettato per essere computazionalmente leggero, modulare e utilizzabile su dispositivi indossabili, fornendo segnalazioni aptiche o vocali per supportare una navigazione più sicura e consapevole.</WritingBlock>

---

**User:**

mi fai un riassunto su come andrebbero usati il filtro di kalman?

---

**Assistant:**

Nel nostro progetto, i **filtri di Kalman** servono a stimare e prevedere il movimento degli ostacoli, riducendo la necessità di eseguire continuamente il riconoscimento degli oggetti.

L'idea è utilizzare **un filtro di Kalman per ogni oggetto dinamico tracciato**, mantenendo aggiornate posizione, velocità e incertezza della stima.

## 1. Come funzionerebbero?

Il processo si divide in quattro passaggi:

1. **Rilevamento:** la telecamera RGB-D individua un ostacolo e ne misura la posizione.
2. **Inizializzazione:** viene creato un filtro di Kalman associato all'oggetto.
3. **Predizione:** il filtro stima dove si troverà l'oggetto nell'istante successivo, utilizzando posizione e velocità precedenti.
4. **Correzione:** quando arriva una nuova misurazione, il filtro confronta la previsione con la posizione osservata e aggiorna la stima.

Questo processo si ripete continuamente.

## 2. Quali informazioni conserva?

Per ogni oggetto manteniamo un vettore di stato:

\[
\mathbf{x}_t=
\begin{bmatrix}
x & y & v_x & v_y
\end{bmatrix}^{T}
\]

E una matrice di covarianza:

\[
P_t\in\mathbb{R}^{4\times4}
\]

La covarianza rappresenta **quanto siamo incerti sulla posizione e sulla velocità dell'oggetto**.

Quando arrivano nuove osservazioni affidabili, il filtro può ridurre l'incertezza; quando mancano, continua a prevedere, ma l'incertezza generalmente aumenta.

Non serve memorizzare tutte le posizioni passate: bastano lo stato corrente, la covarianza e i parametri del filtro.

## 3. Esempio pratico

Una persona viene rilevata a 4 metri di distanza e si sta avvicinando a 1 m/s.

Il filtro può prevedere:

| Tempo futuro | Distanza stimata |
|---|---|
| Adesso | 4 m |
| +1 secondo | 3 m |
| +2 secondi | 2 m |
| +3 secondi | 1 m |

Questi valori assumono velocità costante e movimento direttamente verso l'utente.

Se la persona cambia direzione, una nuova osservazione permette al filtro di correggere la previsione.

Il sistema può utilizzare queste posizioni future, insieme alle rispettive incertezze, per calcolare il rischio di collisione con l'utente.

## 4. Come si integrano con gli altri componenti?

<box border radius="xl" padding={3} gap={1}>
  <box background="surface-secondary" padding={3} radius="lg" align="center">
    **RGB-D + IMU**

    <caption>Misurazioni geometriche e stima del movimento del dispositivo</caption>
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="surface-secondary" padding={3} radius="lg" align="center">
    **Rolling Grid 2.5D**

    <caption>Posizione e geometria degli ostacoli</caption>
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="rgba(35,115,185,0.08)" border radius="lg" padding={3} align="center">
    **Tracking + filtri di Kalman**

    <caption>Posizione, velocità, predizione e covarianza</caption>
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="surface-secondary" padding={3} radius="lg" align="center">
    **Predizione del rischio**

    <caption>Confronto tra traiettoria dell'utente e ostacoli</caption>
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="surface-secondary" padding={3} radius="lg" align="center">
    **Feedback aptico / vocale**
  </box>
</box>

L'albero gerarchico probabilistico può affiancare il tracking, fornendo informazioni sulla tipologia dell'oggetto e aiutando a scegliere modelli di movimento più appropriati.

## 5. Perché sono computazionalmente convenienti?

Un filtro con quattro variabili di stato richiede soltanto:

- 4 valori per lo stato.
- 16 valori per la covarianza.

Con `float32`, sono **80 byte per oggetto**, esclusi metadati e strutture accessorie.

Poiché ogni filtro ha dimensione fissa, il costo complessivo degli aggiornamenti cresce approssimativamente in modo lineare con il numero di oggetti tracciati.

Inoltre, possiamo effettuare predizioni a frequenza elevata senza eseguire continuamente il riconoscimento semantico. Servono comunque nuove misurazioni geometriche per correggere le stime e individuare ostacoli nuovi.

## 6. Quale filtro scegliere?

Per il primo prototipo consiglierei il **Kalman Filter lineare con modello a velocità costante**.

È semplice, leggero e sufficiente per verificare il funzionamento dell'architettura.

Successivamente potremmo introdurre un **Interacting Multiple Model (IMM)**, che combina diversi modelli di movimento per gestire meglio accelerazioni e cambi di direzione.

È inoltre fondamentale compensare il movimento degli occhiali mediante visual-inertial odometry, altrimenti il sistema potrebbe interpretare come movimento dell'ostacolo quello causato dall'utente.

---

**In sintesi:** il filtro di Kalman è il componente che permette al sistema di mantenere una memoria compatta del movimento degli ostacoli, prevederne la posizione futura e correggere progressivamente le stime.

La **Rolling Grid 2.5D descrive dove sono gli ostacoli**, mentre **i filtri di Kalman stimano come si muovono**. Il modulo di Risk Prediction combina queste informazioni per anticipare le possibili collisioni.

---

**User:**

Mi è stato detto che l’albero gerarchico probabilistico potrebbe essere pericoloso se non riconosce la classe, quindi il problema era l’integrazione col filtro di kalman 

---

**Assistant:**

L'obiezione che ti hanno fatto è corretta, ma **non significa che l'albero gerarchico probabilistico sia incompatibile con il filtro di Kalman**. Il problema nasce se utilizziamo la classe riconosciuta per scegliere rigidamente un unico modello di movimento.

Nel vostro progetto, questo potrebbe effettivamente essere pericoloso.

## 1. Dove nasce il problema?

Supponiamo che il sistema rilevi un oggetto e che l'albero probabilistico produca:

| Classe | Probabilità |
|---|---:|
| Muro | 60% |
| Persona | 35% |
| Altro | 5% |

Se scegliamo semplicemente la classe con probabilità maggiore, il sistema considera l'oggetto un muro.

A quel punto potrebbe utilizzare un modello di Kalman statico, assumendo:

\[
v_x=v_y=0
\]

**Il problema:** se l'oggetto fosse effettivamente una persona in movimento, il sistema potrebbe sottostimare il rischio di collisione.

L'errore non deriva dal filtro di Kalman, ma dalla scelta di utilizzare una classificazione incerta per vincolarne il comportamento.

## 2. La soluzione che consiglierei: IMM + classificazione probabilistica

Invece di associare rigidamente un modello di Kalman a ciascuna classe, utilizzerei un **Interacting Multiple Model (IMM)**.

L'IMM combina diversi modelli dinamici, mantenendo una probabilità per ciascuno.

Per esempio:

<box border radius="xl" padding={3} gap={2}>
  <box background="surface-secondary" radius="lg" padding={3} align="center">
    **Oggetto rilevato geometricamente**
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <grid columns={3} gap={2}>
    <grid-item>
      <box border radius="lg" padding={2} gap={1} height="100%" align="center">
        <text weight="medium" size="sm" textAlign="center">Modello statico</text>
        <caption textAlign="center">Kalman 1</caption>
      </box>
    </grid-item>
    <grid-item>
      <box border radius="lg" padding={2} gap={1} height="100%" align="center">
        <text weight="medium" size="sm" textAlign="center">Velocità costante</text>
        <caption textAlign="center">Kalman 2</caption>
      </box>
    </grid-item>
    <grid-item>
      <box border radius="lg" padding={2} gap={1} height="100%" align="center">
        <text weight="medium" size="sm" textAlign="center">Accelerazione</text>
        <caption textAlign="center">Kalman 3</caption>
      </box>
    </grid-item>
  </grid>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="surface-secondary" radius="lg" padding={3} align="center" gap={1}>
    **IMM — Fusione probabilistica**
    <caption>Combina le stime e aggiorna la probabilità dei modelli dalle misurazioni</caption>
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="rgba(37,99,235,0.07)" border radius="lg" padding={3} align="center" gap={1}>
    **Distribuzione delle traiettorie future**
    <caption>Include più ipotesi di movimento e le relative incertezze</caption>
  </box>
</box>

L'albero gerarchico potrebbe continuare a esistere, ma avrebbe soltanto un ruolo ausiliario: fornire informazioni semantiche per influenzare, con cautela, le probabilità iniziali dei modelli.

Non dovrebbe decidere da solo quale filtro utilizzare.

## 3. Come funziona matematicamente?

Supponiamo di avere tre modelli dinamici \(M_1,M_2,M_3\).

L'IMM mantiene una probabilità:

\[
\mu_t^{(j)}=P(M_j\mid Z_{1:t})
\]

Ogni filtro produce una previsione della posizione futura:

\[
p(x_{t+\Delta t}\mid M_j,Z_{1:t})
\]

La distribuzione complessiva diventa:

\[
\boxed{
p(x_{t+\Delta t}\mid Z_{1:t})
=
\sum_j
\mu_t^{(j)}
p(x_{t+\Delta t}\mid M_j,Z_{1:t})
}
\]

Questo è il punto fondamentale: **non scegliamo una singola previsione, ma manteniamo una combinazione di possibili evoluzioni dell'oggetto**.

Quando arrivano nuove misurazioni, l'IMM aggiorna le probabilità dei modelli in base alla loro capacità di spiegare il movimento osservato.

### E se il riconoscimento fallisce?

Il sistema continua a funzionare.

L'IMM può stimare il movimento attraverso le misurazioni geometriche, anche senza sapere se l'oggetto sia una persona, un animale o una bicicletta.

Quindi il riconoscimento semantico diventa un miglioramento facoltativo, non una dipendenza critica.

## 4. Come gestirei l'incertezza sulla classe?

Non farei coincidere automaticamente:

\[
P(\text{persona})=P(\text{modello dinamico})
\]

Una persona può essere ferma e una bicicletta può essere parcheggiata.

Piuttosto, utilizzerei una distribuzione condizionata:

\[
P(M_j\mid c,Z)
\]

Dove \(c\) è la classe semantica e \(Z\) contiene le osservazioni geometriche e dinamiche.

Se la classificazione è poco affidabile, il sistema può ridurre l'influenza delle informazioni semantiche e affidarsi principalmente alle osservazioni del movimento.

Se invece il classificatore è affidabile e ben calibrato, le informazioni sulla classe possono contribuire a migliorare le previsioni.

**Non eliminerei comunque le ipotesi dinamiche plausibili soltanto perché il classificatore ritiene che l'oggetto sia statico.**

## 5. Quale soluzione sceglierei per il vostro progetto?

| Soluzione | Vantaggio | Limite |
|---|---|---|
| Kalman selezionato dalla classe | Semplice | Sensibile agli errori di classificazione |
| Kalman indipendente dalla classe | Robusto agli errori semantici | Modello di movimento meno flessibile |
| **IMM indipendente dalla classe** | Gestisce più dinamiche senza recognition | Maggiore costo computazionale |
| IMM + albero probabilistico | Sfrutta anche informazioni semantiche | Richiede calibrazione e validazione |

**La mia scelta sarebbe sviluppare prima un IMM indipendente dalle classi**, con un numero ridotto di modelli dinamici.

Successivamente integrerei l'albero gerarchico soltanto se i test dimostrassero che migliora le previsioni senza aumentare i pericoli non rilevati.

Un IMM con tre piccoli filtri per oggetto rimane generalmente gestibile dal punto di vista computazionale, anche se triplica approssimativamente il numero di filtri rispetto a un Kalman singolo e introduce il costo di combinazione delle ipotesi.

## 6. Un'ultima precauzione fondamentale

L'IMM non garantisce di prevedere ogni comportamento improvviso.

Se un oggetto cambia direzione bruscamente, tutti i modelli possono sbagliare prima che arrivino nuove osservazioni.

Per questo il modulo di rischio dovrebbe mantenere margini di sicurezza e considerare anche scenari poco probabili ma potenzialmente pericolosi, soprattutto quando l'incertezza è elevata.

La geometria degli ostacoli statici deve inoltre rimanere nella Rolling Grid, senza dipendere dalla classificazione semantica o dall'IMM.

---

**In sintesi:** la criticità che ti hanno segnalato esiste soltanto se la classe riconosciuta determina rigidamente il modello dinamico. Possiamo evitarla separando classificazione e tracking.

La nuova architettura sarebbe:

**Rolling Grid 2.5D → Tracking geometrico → IMM (più filtri di Kalman) → Predizione probabilistica del rischio**, con l'albero gerarchico come modulo opzionale di supporto.

Questa soluzione è più robusta agli errori di riconoscimento e mantiene il sistema operativo anche quando non è possibile identificare correttamente un oggetto.

---

**User:**

Integra ora questa idea con i pesi probabilistici che verrebbero rilevati con l’albero gerarchico, il mio collega ha posto il problema di coerenza solo eventuale 

---

**Assistant:**

Il problema sollevato dal tuo collega è molto interessante, perché riguarda uno degli aspetti più delicati della nostra architettura: **la sincronizzazione tra le probabilità prodotte dall'albero gerarchico e lo stato dinamico mantenuto dai filtri di Kalman**.

La mia proposta è integrare l'albero probabilistico con l'IMM (*Interacting Multiple Model*), ma evitando che gli aggiornamenti asincroni del riconoscimento semantico compromettano la coerenza delle previsioni.

In particolare, introdurrei tre meccanismi:

1. **Fusione bayesiana dei pesi:** le probabilità dell'albero contribuiscono ai pesi dei modelli dinamici dell'IMM.
2. **Versionamento temporale:** ogni risultato semantico è associato al timestamp dell'osservazione che lo ha generato.
3. **Consistenza temporale controllata:** il sistema di sicurezza utilizza sempre uno stato geometrico coerente, anche quando la classificazione non è ancora aggiornata.

## 1. Come integrerei albero probabilistico e IMM

L'albero gerarchico non deve scegliere direttamente quale filtro di Kalman utilizzare.

Deve invece produrre una distribuzione probabilistica sulle classi degli oggetti.

Per esempio, immaginiamo che venga rilevato un ostacolo:

<box border radius="lg" padding={3} gap={3}>
  <text weight="medium">Esempio: probabilità semantiche prodotte dall'albero</text>
  {@body const classes=[{name:"Persona",p:0.65},{name:"Bicicletta",p:0.25},{name:"Altro / sconosciuto",p:0.10}]}
  {#each classes as c}
    <box gap={1} key={c.name}>
      <row justify="between" align="center">
        <text size="sm">{c.name}</text>
        <text weight="medium" tabularNums>{Math.round(c.p*100)}%</text>
      </row>
      <box background="surface-tertiary" radius="full" height="9px" clip>
        <box background="#5386BB" height="100%" width={`${c.p*100}%`} radius="full"/>
      </box>
    </box>
  {/each}
  <caption>Probabilità illustrative, non prodotte da un modello addestrato.</caption>
</box>

L'IMM mantiene invece una distribuzione sui modelli di movimento:

- \(M_1\): oggetto statico.
- \(M_2\): velocità costante.
- \(M_3\): movimento con accelerazione o cambiamenti di velocità.

Per collegare le due distribuzioni, definiamo una matrice di probabilità condizionate:

\[
A_{jc}=P(M_j\mid c)
\]

Questa matrice descrive quanto ciascun modello dinamico sia plausibile per ogni classe semantica.

I valori devono essere stimati dai dati e validati, non scelti arbitrariamente.

La distribuzione semantica sui modelli diventa:

\[
\boxed{
q_j=\sum_c A_{jc}P(c\mid I_t)
}
\]

Dove \(I_t\) rappresenta l'immagine da cui è stata ricavata la classificazione.

Questo ci permette di passare da una probabilità di classe a una probabilità di comportamento, **senza confondere le due grandezze**.

## 2. Come aggiornare i pesi dell'IMM

Qui farei una distinzione importante.

L'IMM possiede già probabilità dei modelli dinamici, che aggiorna utilizzando le osservazioni geometriche e le probabilità di transizione tra modelli.

Non possiamo semplicemente moltiplicarle per \(q_j\) a ogni frame, perché rischieremmo di contare ripetutamente la stessa informazione semantica, rendendo il modello eccessivamente sicuro.

La soluzione più rigorosa è trattare la classificazione come una nuova osservazione, con una propria affidabilità.

Se disponiamo di una likelihood semantica calibrata \(L_j\), l'aggiornamento può essere:

\[
\boxed{
\mu_j^+
=
\frac{\mu_j^-L_j}
{\sum_k\mu_k^-L_k}
}
\]

Dove:

- \(\mu_j^-\) è la probabilità del modello prima dell'aggiornamento semantico.
- \(L_j\) misura quanto la nuova osservazione semantica supporti il modello \(M_j\).
- \(\mu_j^+\) è la probabilità aggiornata.

La distribuzione \(q_j\) ricavata dall'albero può contribuire a costruire queste likelihood, ma **non coincide automaticamente con esse**: bisogna considerare le probabilità a priori usate nell'addestramento e la dipendenza tra osservazioni.

Inoltre, se il classificatore è incerto, non disponibile o produce risultati fuori distribuzione, possiamo ignorare l'aggiornamento semantico e lasciare che l'IMM continui a funzionare geometricamente.

## 3. Il problema della coerenza eventuale

Il tuo collega ha individuato un problema reale.

Supponiamo che i componenti lavorino a frequenze diverse:

| Componente | Frequenza ipotetica |
|---|---:|
| Sensori geometrici | 30 Hz |
| Filtri IMM | 30 Hz |
| Risk Prediction | 20 Hz |
| Albero probabilistico | 5 Hz |

L'albero potrebbe produrre al tempo \(t=1.2\) secondi una classificazione relativa a un'immagine acquisita a \(t=1.0\).

Nel frattempo, l'IMM ha già aggiornato diverse volte la posizione dell'oggetto.

Se associamo direttamente la classificazione ricevuta allo stato corrente, rischiamo di utilizzare informazioni riferite a istanti diversi, o addirittura a un oggetto che non è più presente.

**La coerenza eventuale, da sola, non è una garanzia sufficiente per un sistema di sicurezza in tempo reale.**

In particolare, non possiamo semplicemente aspettare che tutti i moduli convergano allo stesso stato: nel frattempo l'utente continua a muoversi.

## 4. La soluzione: consistenza forte nel percorso critico, eventuale nella semantica

Separerei il sistema in due domini.

<box border radius="xl" padding={3} gap={2}>
  <box background="rgba(30,130,95,0.07)" border radius="lg" padding={3} gap={1}>
    <row align="center" gap={2}>
      <icon name="shield-check" color="success"/>
      **Dominio critico — stato geometrico**
    </row>
    <text size="sm">Sensori → Tracking IMM → Predizione del rischio</text>
    <caption>Snapshot temporali coerenti, aggiornamenti ordinati e scadenze definite</caption>
  </box>
  <row justify="center"><icon name="arrow-down-up" color="secondary"/></row>
  <box background="surface-secondary" radius="lg" padding={3} gap={1}>
    <row align="center" gap={2}>
      <icon name="git-branch"/>
      **Dominio asincrono — classificazione**
    </row>
    <text size="sm">Albero gerarchico → Probabilità semantiche → Adattamento dei modelli</text>
    <caption>Aggiornamenti ritardati ammessi, con controlli di validità</caption>
  </box>
</box>

Per ottenere questo comportamento utilizzerei un modello **single-writer, multiple-reader**: un solo componente è responsabile dell'aggiornamento dello stato del tracker, mentre gli altri leggono snapshot immutabili pubblicati in modo atomico.

Ogni classificazione dovrebbe contenere almeno:

```cpp
struct SemanticObservation {
    uint64_t trackId;
    uint32_t trackGeneration;

    uint64_t observationTimestamp;
    uint64_t modelVersion;

    std::vector<float> classProbabilities;
    float confidence;
};
```

Quando arriva un risultato, il sistema verifica:

1. Che l'oggetto tracciato esista ancora.
2. Che l'identificativo non sia stato riutilizzato per un altro oggetto.
3. Che il risultato non sia troppo vecchio.
4. Che la classificazione corrisponda alla stessa osservazione geometrica.
5. Che le probabilità siano sufficientemente affidabili.

Se uno di questi controlli fallisce, la classificazione viene scartata.

## 5. Come gestire i risultati arrivati in ritardo?

Qui abbiamo due possibilità.

**Soluzione A — Semplice, consigliata per l'MVP**

Quando arriva una classificazione valida, aggiorniamo soltanto le informazioni semantiche utilizzabili per le predizioni successive.

Non modifichiamo retroattivamente le stime geometriche già prodotte.

Questa soluzione introduce una certa approssimazione temporale, ma è molto semplice e prevedibile dal punto di vista computazionale.

**Soluzione B — Più rigorosa, per una versione avanzata**

Manteniamo un breve buffer circolare degli stati passati.

Quando arriva un'osservazione ritardata:

- Recuperiamo lo stato relativo al timestamp originale.
- Applichiamo l'aggiornamento probabilistico.
- Ripropaghiamo lo stato fino al presente.
- Pubblichiamo un nuovo snapshot coerente.

Questo approccio è noto come gestione delle *out-of-sequence measurements*.

Richiede maggiore memoria e computazione, ma con un buffer temporale limitato può rimanere gestibile.

Non lo introdurrei inizialmente, soprattutto perché un risultato semantico ritardato non giustifica sempre la ricostruzione dell'intero stato geometrico.

## 6. Come combinare effettivamente i pesi nel calcolo del rischio?

Facciamo un esempio numerico.

Supponiamo che, dopo la fusione delle informazioni geometriche e semantiche, l'IMM produca:

{@body const [pStatic,setPStatic]=DIL.useState(20)}
{@body const [pConstant,setPConstant]=DIL.useState(50)}
{@body const [pAccel,setPAccel]=DIL.useState(30)}
{@body const probs=[pStatic,pConstant,pAccel]}
{@body const total=probs.reduce((a,b)=>a+b,0)}
{@body const normalized=total>0?probs.map(v=>v/total):[1/3,1/3,1/3]}
{@body const risks=[0.05,0.35,0.8]}
{@body const overall=normalized.reduce((s,p,i)=>s+p*risks[i],0)}
<box border radius="xl" padding={3} gap={3}>
  <text weight="medium">Simulazione della fusione dei modelli</text>
  <text color="secondary" size="xs">Modifica i pesi dei tre modelli. I valori vengono normalizzati automaticamente.</text>
  {#each [{name:"Statico",value:pStatic,set:setPStatic,risk:5},{name:"Velocità costante",value:pConstant,set:setPConstant,risk:35},{name:"Accelerazione",value:pAccel,set:setPAccel,risk:80}] as m,i}
    <box gap={1} key={m.name}>
      <row justify="between" align="center">
        <text size="sm" weight="medium">{m.name}</text>
        <text size="sm" tabularNums>{(normalized[i]*100).toFixed(1)}% peso</text>
      </row>
      <slider min={0} max={100} step={5} value={m.value} onChange={m.set}/>
      <caption>Probabilità di collisione condizionata: {m.risk}%</caption>
    </box>
  {/each}
  <divider color="subtle"/>
  <box background="surface-secondary" radius="lg" padding={3} gap={1}>
    <text color="secondary" size="xs">Probabilità complessiva di collisione</text>
    <title size="2xl" tabularNums>{(overall*100).toFixed(1)}%</title>
    <text color="secondary" size="xs">Somma pesata delle probabilità condizionate</text>
  </box>
  <caption>Esempio didattico: le probabilità di collisione condizionate sono ipotetiche e fisse. In un sistema reale sarebbero calcolate dalle traiettorie future, dalle geometrie e dalle covarianze.</caption>
</box>

La formula è:

\[
\boxed{
P(C\mid Z)=
\sum_{j=1}^{M}\mu_jP(C\mid M_j,Z)
}
\]

La cosa importante è che **la probabilità di collisione viene calcolata separatamente per ogni modello**, prima di combinare i risultati.

Non combinerei soltanto le posizioni medie dei filtri: così potremmo perdere scenari di collisione importanti.

Inoltre, per un dispositivo assistivo, la media probabilistica non dovrebbe essere l'unico criterio di allarme. Possiamo affiancarle una verifica conservativa delle traiettorie plausibili e dell'incertezza, per evitare che un rischio grave venga mascherato da un peso basso.

## 7. E se i pesi dell'albero vengono aggiornati online con MLE/MAP?

Qui c'è un secondo problema di coerenza: **la versione dei parametri del modello**.

Se utilizziamo RLS o un altro metodo di apprendimento incrementale, non dovremmo permettere che i pesi cambino mentre un altro componente li sta utilizzando per calcolare il rischio.

Proporrei quindi:

- Parametri attivi immutabili durante ogni ciclo di predizione.
- Aggiornamenti calcolati su una copia separata.
- Validazione dei nuovi parametri.
- Pubblicazione atomica di una nuova versione.
- Possibilità di ripristinare la versione precedente.

Per esempio, una classificazione prodotta dal modello versione 12 non deve essere interpretata automaticamente come se fosse stata generata dalla versione 13.

Questa separazione rende il sistema più facile da testare e permette di mantenere riproducibili le previsioni.

Per l'MVP continuerei comunque a preferire pesi addestrati offline e fissi.

---

## 8. Architettura finale che proporrei al team

<box border radius="xl" padding={3} gap={2}>
  <box background="surface-secondary" radius="lg" padding={3} align="center">
    **RGB-D + IMU**
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="surface-secondary" radius="lg" padding={3} align="center">
    **Rolling Grid 2.5D + rilevamento geometrico**
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <grid columns={2} gap={2}>
    <grid-item>
      <box border radius="lg" padding={3} gap={1} height="100%">
        **IMM / Kalman**
        <caption>Stima geometrica e probabilità dei modelli dinamici</caption>
      </box>
    </grid-item>
    <grid-item>
      <box border radius="lg" padding={3} gap={1} height="100%">
        **Albero probabilistico**
        <caption>Classi, pesi semantici e modelli comportamentali</caption>
      </box>
    </grid-item>
  </grid>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="surface-secondary" radius="lg" padding={3} align="center" gap={1}>
    **Temporal Fusion Manager**
    <caption>Timestamp, versioni, validità, fusione bayesiana e snapshot coerenti</caption>
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="rgba(30,120,185,0.07)" border radius="lg" padding={3} align="center" gap={1}>
    **Risk Prediction Engine**
    <caption>Probabilità di collisione + verifica conservativa</caption>
  </box>
  <row justify="center"><icon name="arrow-down" color="secondary"/></row>
  <box background="surface-secondary" radius="lg" padding={3} align="center">
    **Feedback aptico / vocale**
  </box>
</box>

Il *Temporal Fusion Manager* sarebbe una responsabilità logica, non necessariamente un microservizio separato. In implementazione, il tracking IMM e la fusione dovrebbero condividere un proprietario dello stato, per evitare aggiornamenti concorrenti incoerenti.

### La decisione architetturale più importante

Non cercherei di ottenere una consistenza forte tra tutti i componenti: introdurrebbe attese e potrebbe peggiorare la latenza.

Sceglierei invece **consistenza temporale nel percorso critico e coerenza eventuale controllata per i dati semantici**, con una regola fondamentale:

> Se la classificazione è assente, ritardata o incoerente, il sistema deve continuare a stimare il rischio sulla base delle informazioni geometriche, senza assumere che l'ostacolo sia innocuo.

Questa è, secondo me, la soluzione più equilibrata per mantenere i vantaggi dell'albero probabilistico e dell'IMM senza introdurre una dipendenza pericolosa dal riconoscimento delle classi.

Resta da validare sperimentalmente: né l'IMM né la fusione bayesiana garantiscono da soli la sicurezza del dispositivo, soprattutto in presenza di ostacoli mai osservati o movimenti imprevedibili.

---

*This file was created with GPTAha Free. [Upgrade to remove this notice →](https://www.gptaha.com/pricing?utm_source=export_watermark)*
