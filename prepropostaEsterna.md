
### 1.1 Pool Hardware Massimo & Matrice di Selezione
L'orchestratore mappa il **Pool Hardware Massimo** `[D_front: Depth Cam densa frontale, T_lat[0..2]: 3x ToF multizona VL53L7CX/L8CX, C_rgb: RGB, G_opt: GPU/NPU, A_out: Audio, V_out: Display/Telemetry]`.

All'avvio e a `1–2 Hz` in esercizio, l'AI Selector valuta:
1. **Hardware Discovery & Startup Check (`Sez. 8`):** verifica presenza fisica, disattivazione forzata dei filtri di *hole-filling*, e test di risposta attiva (copertura sensore = crollo punti validi).
2. **Context Probe ($C$):** saturazione IR / luce ambientale stimata, tasso di buchi speculari (possibile vetro), carico computazionale ($T_{\text{cycle}}$ medio sugli ultimi 15 cicli).
3. **Utility Scorer Vincolato:** sceglie la configurazione $m^* \in \mathcal{M}_{\text{certified}}$ che massimizza copertura e precisione rispettando $T_{\text{cycle}}(m^*) \le 55\text{ ms}$ (margine di sicurezza rispetto a `66,6 ms`) e lo stato di salute dei sensori.

### 1.2 Regole di Degradazione e Scelta Autonoma (Policy Table)
| Condizione Rilevata | Configurazione Selezionata dall'AI | Garanzia di Sicurezza Mantenuta |
| :--- | :--- | :--- |
| **Full HW + CPU scarica ($T_{\text{cycle}} < 45\text{ ms}$)** | `D_front` (griglia 2.5D) + `T_lat` (flank cueing) + `Side NN = ON` | Massima copertura, continuità e classificazione laterale. |
| **No GPU / CPU sotto carico ($T_{\text{cycle}} > 55\text{ ms}$)** | `Side NN = OFF`; riduce griglia a `2D` o `2.5D-coarse` | Preserva i $\ge 15\text{ Hz}$ senza alterare il tracking geometrico. |
| **Luce intensa / Saturazione IR su `T_lat`** | Disabilita `T_lat` oltre `0,5 m` (o li esclude); ricalcola portata max `D_front` | I settori laterali restano `non osservato`, mai `libero`. |
| **Cross-talk IR rilevato (`D_front` $\leftrightarrow$ `T_lat`)** | Applica Time-Division Multiplexing su `T_lat` o disabilita i coni sovrapposti | Elimina falsi ostacoli/buchi fantasma sui bordi del FOV. |
| **`D_front` guasta/coperta, `T_lat` sani** | **Fallback Proximity-Only:** attiva allerta di prossimità a corto raggio da `T_lat` | Dichiara esplicitamente `affidabilità persa` sul varco frontale. |
| **GPU/NPU disponibile (`T_cycle < 30 ms`)** | Sblocca **Mappa 3D Voxel Sparsa Probabilistica (`Sez. 7`)** + `Side NN` | Copertura completa ostacoli bassi (`< 1,1 m`) e sospesi. |

---

## 2. Soluzione per `Sez. 2.5` & `Sez. 7`: Continuità Visiva per Tutta l'Occlusione

Il limite attuale (`v0.5`, punto 2.5) interrompe la previsione a `0,5 s`, lasciando solo un avviso statico sull'ombra. Per mantenere una **previsione continua, realistica e controllata** lungo *tutta* l'occlusione (es. pannello largo `1 m` attraversato a `0,5–1,4 m/s`, durata `0,7–2,0 s`), si propone un modulo a **3 componenti**:

### 2.1 Compensazione della Latenza (`Sez. 2.8`)
I `~155 ms` stimati erodono oltre il 30% di una finestra da `0,5 s`. Ogni frame acquisito porta un timestamp hardware $t_{\text{cap}}$; prima del rendering/uscita, lo stato Kalman viene sempre propagato a $t_{\text{now}}$ ($\Delta t_{\text{lat}} = t_{\text{now}} - t_{\text{cap}}$), dichiarando esplicitamente l'età del dato.

### 2.2 Inseguitore Bi-Ipotesi (Mini-IMM: Transito vs Sosta)
Senza stimare accelerazione né massa (`INV-5`), ogni traccia occlusa mantiene due ipotesi cinematiche leggere in parallelo sullo stato $\mathbf{x} = [X, Z, v_X, v_Z]^T$:
- **Ipotesi $H_1$ (*Transito a Velocità Costante*):** $\mathbf{v}_{k} = \mathbf{v}_{\text{entry}}$ (ultimo vettore velocità affidabile pre-occlusione), con rumore di processo $Q_{\text{transit}}$ che fa crescere la covarianza $P_1(t)$ nel tempo.
- **Ipotesi $H_2$ (*Rallentamento / Sosta dietro l'ostacolo*):** velocità smorzata esponenzialmente ($\mathbf{v}_k = \alpha \mathbf{v}_{k-1}$, $\alpha < 1$, verso velocità zero al centro dell'ombra di ingresso), con covarianza $P_2(t)$ ancorata alla zona occlusa.

I pesi delle due ipotesi $(\mu_1, \mu_2)$, inizializzati a `(0.8, 0.2)` all'ingresso nell'ombra, vengono aggiornati a ogni ciclo tramite **Informazione Negativa**.

### 2.3 *Negative-Information Shadow Clamping* ("Ciò che il sensore vede attorno all'ostacolo")
Ad ogni ciclo durante l'occlusione, la mappa locale conosce esattamente quali celle attorno all'ostacolo sono `libero` (osservate direttamente senza alcun target rilevato):
1. **Troncamento Geometrico (Clamping):** La distribuzione spaziale prevista $\mathcal{N}(\hat{\mathbf{p}}_1(t), P_1(t))$ viene proiettata sulla griglia; tutte le celle appartenenti alla classe `libero` ricevono probabilità **zero** ($p(\text{cell} \in \text{libero}) = 0$). La massa di probabilità prevista può esistere **solo** dentro l'inviluppo delle celle `in ombra` (o `non osservato` contigue).
2. **Aggiornamento Bayesiano dei Pesi $(\mu_1, \mu_2)$:** Sia $f_{\text{shadow}}(t) \in [0, 1]$ la frazione della massa gaussiana di $H_1$ che cade ancora dentro l'ombra.
   - Se $H_1$ prevede che il soggetto dovrebbe ormai essere uscito dall'altro lato del pannello, ma le celle di uscita sono viste come `libero` senza nessuna nuova rilevazione, $f_{\text{shadow}}(t)$ crolla rapidamente $\rightarrow$ il peso $\mu_1$ decade a favore di **$\mu_2$ (Sosta in ombra)**!
   - *Risultato critico:* Il sistema non fa "camminare un fantasma" nel vuoto visibilmente libero, e riconosce matematicamente la differenza tra un attraversamento in corso e una persona che si è fermata dietro il pannello (`Atto 5` della demo!).
3. **Quando si passa da `previsto` a `perso`:**
   - Finché l'incertezza clonata sull'ombra (raggio efficace $\sigma_{\text{eff}}$ della distribuzione risultante dopo il clamping) resta entro la tolleranza dichiarata (es. $\sigma_{\text{eff}} \le 0,8\text{ m}$ o $\mu_1$ coerente col tempo di attraversamento massimo stimato per la larghezza dell'ostacolo a $v_{\min}$), lo stato resta **`previsto`** con precisione dichiarata in metri ($\pm \sigma_{\text{eff}}$).
   - Se la permanenza supera la finestra di prevedibilità cinematica (es. $\mu_2 \to 1$ per sosta prolungata oltre la soglia di incertezza o covarianza non più informativa), l'oggetto transisce a **`perso`**, ma l'intera zona d'ombra mantiene in modo permanente il flag **`possibile presenza`** (`INV-3`).

### 2.4 Regole di Rendering Visivo e Acustico (Distinzione Osservato vs Incerto)
Per rispondere a *"come disegnarla senza farla sembrare un'osservazione"* (`Sez. 7`):
- **`visto`:** contorno solido, vettore velocità pieno, indicatore età dato `0 ms` (netto).
- **`previsto` (durante tutta l'occlusione):** **nessun box solido**. Si disegna esclusivamente l'**inviluppo tratteggiato dell'area probabile clampata dentro l'ombra** (gradiente di densità $\mu_1 H_1 + \mu_2 H_2$), con etichetta numerica obbligatoria `PREVISTO ±X.XX m | t_occ Y.Ys | conf Z%`.
- **`perso` + `possibile presenza`:** l'inviluppo di moto scompare; resta la campitura zebrata/ambrata sull'intera area `in ombra` con l'età dell'ultima osservazione (`possibile presenza da T s`).

---

## 3. Integrazione dei Moduli Anti-Bird Strike (Solo Posizione e Velocità)

Sfruttando le sole variabili fisicamente osservabili ($\mathbf{r}, \mathbf{v}, P$), si innesta un valutatore cinematico derivato dai sistemi aeroportuali ABAR/ACAS:

1. **CPA & *Protected Volume* Probabilistico:**
   - Per ogni traccia `visto` o `previsto`, si calcola $t_{\text{CPA}} = \max\left(0, -\frac{\mathbf{r} \cdot \mathbf{v}}{\|\mathbf{v}\|^2}\right)$ e $d_{\text{CPA}} = \|\mathbf{r} + \mathbf{v} t_{\text{CPA}}\|$.
   - Invece di una soglia binaria sulla distanza, si calcola $P_{\text{intrusion}}$: la frazione di massa dell'ellisse di covarianza (già clampata sull'ombra se occluso!) che interseca il *Protected Volume* del varco o dell'utente.
2. **Indice di Minaccia *On-Boresight* (*Constant Bearing, Decreasing Range*):**
   - Calcolo immediato della variazione angolare $|\dot{\theta}|$ e della velocità radiale $\dot{r}$.
   - Permette di distinguere subito un attraversamento trasversale (Atto 3: $|\dot{\theta}|$ alto, bassa criticità frontale) da una traiettoria convergente ($|\dot{\theta}| \approx 0, \dot{r} < 0$).
3. **Logica Operativa *Runway Hold* (TA / HOLD / RA):**
   - **NOMINAL (Go):** settore `libero`, nessuna `possibile presenza`, $P_{\text{intrusion}} \approx 0$.
   - **TA (Caution):** target `visto` o `previsto` in avvicinamento al volume protetto.
   - **HOLD (Attesa Prudente):** qualsiasi cella del corridoio in stato `possibile presenza` o `non osservato`, oppure ipotesi $H_2$ (*Sosta in ombra*) dominante dietro un ostacolo adiacente al varco. Equivale al blocco del decollo finché la pista non è confermata libera.
   - **RA / FAIL-SAFE:** $P_{\text{intrusion}}$ critica o integrità sensore persa (`affidabilità persa`).
4. **Cueing Laterale dai 3 ToF (`T_lat`):**
   - Quando attivi, fungono da *early-warning flank guard*: un'intrusione entro `0,5 m` ai lati innesca un pre-allarme settoriale prima che il target entri nel FOV frontale.

---

## 4. Copertura Verticale (`< 1,1 m`) e Monitoraggio Attività (`Sez. 7`)

### 4.1 Mappa 2.5D a 3 Fasce (Alternativa CPU-Safe al Voxel 3D Completo)
Per chiudere il buco sotto `1,1 m` (`Sez. 4` e `Sez. 9`) senza far crollare il ciclo sotto `15 Hz` in assenza di GPU:
- La proiezione su griglia 2D mantiene 3 bitmask/livelli di altezza per ogni cella $(x, z)$:
  - **Fascia Bassa (`0,15 – 0,60 m`):** gradini, scatole, basi di carrelli (filtrando il piano pavimento con tolleranza pendenza/rumore).
  - **Fascia Media (`0,60 – 1,60 m`):** busto persone, pannelli, colonne, ostacoli principali.
  - **Fascia Alta (`> 1,60 m`):** ostacoli sospesi, sbarre, bracci meccanici.
- Una cella è dichiarata `libero` solo se **tutte le fasce pertinenti al profilo d'uso** risultano osservate e libere. Lo Stack Selector passa automaticamente al **Voxel 3D sparso probabilistico** solo se è presente GPU/NPU o se il profiling CPU conferma $T_{\text{cycle}} \le 45\text{ ms}$.

### 4.2 Macchina a Stati per il "Monitoraggio di Attività" (`Sez. 7`)
Per trasformare i frame in eventi temporali richiesti dalla traccia, sopra il tracker opera una FSM per ogni ID tracciato:
- `INGRESSO_AREA` (nuova traccia confermata con logica $M$-su-$N$ per rigettare rumore singolo frame).
- `ATTRAVERSAMENTO` (`visto` con $\|\mathbf{v}\| > v_{\text{sosta}}$ e $|\dot{\theta}|$ sostenuto).
- `AVVICINAMENTO_DIRETTO` (`On-Boresight`: $|\dot{\theta}| \approx 0, \dot{r} < 0$).
- `OCCLUSIONE_IN_CORSO` (transizione `visto` $\rightarrow$ `previsto` lungo il bordo di un ostacolo noto).
- `SOSTA_IN_OMBRA` (peso $\mu_2 > \theta_{\text{stop}}$ durante l'occlusione, oppure ingresso fermo prima dell'ombra).
- `RIAPPARIZIONE_CONFERMATA` (ri-associazione geometrica OC-SORT-like all'uscita dall'ombra con mantenimento ID).
- `USCITA_AREA` / `PERDITA_AFFIDABILITÀ_SENSORE`.

---

## 5. Vettori di Attacco e Test di Falsificazione per lo Sciame

Si chiede allo sciame di agenti specialisti di sottoporre questa proposta ai seguenti attacchi mirati prima dell'adozione nel ramo principale:

1. **Attacco 1 — "Fantasma nel corridoio libero" (Test su Negative-Information Clamping):**
   - *Scenario:* Soggetto entra dietro un pannello largo `1 m` a `1,2 m/s`, poi si ferma bruscamente a metà pannello (`Atto 5`).
   - *Criterio di rigetto:* Se anche per un solo frame l'area `previsto` viene disegnata sopra celle `libero` adiacenti al pannello, o se $\mu_1$ resta dominante oltre il tempo atteso di uscita senza riapparizione, il clamping è fallito.
2. **Attacco 2 — "Scambio di identità o doppia uscita" (Limite dichiarato `Sez. 2.4`):**
   - *Scenario:* Una persona entra in ombra da sinistra; escono due persone oppure esce una persona a velocità tripla rispetto a quella d'ingresso.
   - *Criterio di sicurezza:* Verificare che in caso di ambiguità cinematica oltre la soglia di associazione (gating $\chi^2$ di Mahalanobis violato), il sistema **non forzi** un falso `visto` con identità sicura, ma dichiari conflitto / nuova traccia mantenendo la `possibile presenza` fino a completa ri-osservazione dell'ombra.
3. **Attacco 3 — "Oscillazione dello Stack Selector" (*Thrashing* tra configurazioni):**
   - *Scenario:* CPU oscilla attorno a `55 ms` o luce ambiente varia rapidamente.
   - *Criterio di rigetto:* Il Control Plane deve includere **isteresi temporale** (es. cambio configurazione ammesso al massimo ogni `2–3 s` salvo fault critico di integrità) e durante la transizione non deve mai azzerare la mappa delle `possibili presenze`.
4. **Attacco 4 — "Cross-Talk IR e Tessuto Nero" (`Sez. 8`):**
   - *Scenario:* `D_front` e `T_lat` accesi simultaneamente al chiuso davanti a un soggetto vestito di nero opaco a `2,5 m`.
   - *Criterio:* I buchi di profondità generati dal tessuto nero devono mapparsi in `non osservato` / `affidabilità ridotta`, **mai** in `libero`, e non devono far scattare falsi positivi di "sensore coperto" se il resto della scena è valido.
5. **Attacco 5 — "Verifica Consistenza Covarianza (NIS)" durante occlusione:**
   - *Scenario:* `400` passaggi simulati + `30` passaggi reali a velocità variabili (`0,3–1,8 m/s`).
   - *Criterio:* L'errore reale al momento della riapparizione deve cadere dentro l'ellisse di confidenza al `95%` dichiarata dall'output `PREVISTO ±X.XX m` in almeno il `90–95%` dei casi (calibrazione realistica di $Q$ e $R$, evitando sovra-confidenza).

---

## 6. Piano di Integrazione Compatible con Budget 24h vs 38h (`Sez. 9`)

- **Taglio minimo garantito (`24h`):**
  - Core Real-Time: Stadio 1 (filtri spenti + startup hand-check) + Mappa 2D/2.5D a 4 stati + Mini-IMM (`H1+H2`) con Clamping su `libero` + CPA/HOLD + FSM Attività + I due profili d'uscita (Mappa + Audio) per i 5 Atti della demo.
  - Stack Selector in versione ridotta (Boot probe + CPU fallback `Side NN OFF`).
- **Estensione completa (`38h+`):**
  - Aggiunta `Side NN` asincrona (`YOLO26n` / `RF-DETR` solo etichetta), `3x ToF` laterali per cueing, Stack Selector completo con contesto luce/IR e valutazione benchmark `2.5D` vs `Voxel 3D` su hardware reale.

---
**Richiesta all'AI Orchestratrice dello Sciame:**
1. Eseguire l'*Audit delle Ipotesi Nascoste* sul modulo **Mini-IMM + Negative-Information Clamping** rispetto al contratto della `Sez. 2.5`.
2. Verificare mediante simulazione (incluso caso di sosta improvvisa dietro pannello `1 m`) che la curva di errore reale resti contenuta nell'incertezza dichiarata per l'intera durata dell'occlusione (`0,5 s → 3,0 s`).
3. Emettere verdetto (`C` / `P` / `S`) per l'adozione della **Mappa 2.5D a 3 fasce** come sostituto CPU-safe del Voxel 3D fino a disponibilità di GPU.