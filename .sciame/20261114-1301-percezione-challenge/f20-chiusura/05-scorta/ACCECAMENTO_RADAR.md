# F7r «scorta» con il radar disturbato dall'evento

Autore: `sciame-sensori`, fase 4, 15-11-2026, dalle 06:21 alle 06:40 (`date -Is`).

**Tutto è simulato. Nessun sensore fisico, niente è «validato».** Il sistema fa solo osservazione e avviso.

**Indipendenza.** Lo scenario e il tracciatore vengono da `scorta_f7.py` dell'altro agente. Io ho aggiunto il
disturbo radar e la misura. La misura trova gli errori di codice e di logica, non quelli della fisica ipotizzata.

## 0. In testa: cambi di stato e regole

- **Risposta alla domanda dell'utente.** Non era giusto lasciare il radar indisturbato, ma l'errore conta solo in
  parte. La luce, il fumo e l'impulso elettromagnetico **non** accecano un radar in banda X, Ku o mmW. La fiamma
  ionizzata lo attenua di qualche dB, e solo se la linea di vista ci passa dentro.
  - Ciò che può davvero togliere il radar è la **nube di detriti vicina**: eco forte che manda in saturazione l'AGC o
    l'ADC, mascheramento CFAR, cammini multipli.
  - L'accecamento di 0,2–2 s usato qui è **pessimista**: il comportamento fisico atteso è un calo di Pd di decine o
    centinaia di ms (ipotesi).
- **Previsioni.** Scritte alle 06:22:16 in `PREVISIONI_RADAR.md`. Congelamento alle 06:24:44 in
  `CONGELAMENTO_RADAR.md` (sha256 dello script). Valutazione lanciata una sola volta (06:24:50–06:29) sui semi nuovi
  20261122.
- **Esiti:**
  - P1 continuità: **smentita in 1 cella** (totale/att 59/60); regge nelle altre.
  - P2 riacquisizione ≥ 51/60: **smentita** in davanti/att (41/60) e vira/att (43/60). Regge altrove; vira/sda è
    56/60.
  - P3 «libero»: **regge** (0 in tutte le celle).
  - P4 associazioni spurie non dichiarate: **smentita in 1 cella** (totale/att 1/60).
  - P5 C contro la curva: **smentita al margine** a τ = 2 s in 3 celle att (scarto 0,10–0,11); regge altrove.
- **Esito non previsto e più grave** (notato dopo, non era una previsione): l'**avviso al portatore** prima che un
  frammento gli passi entro 10 m crolla.
  - davanti: 27/52 in att, 28/52 in sda;
  - vira: 19/55 in att, 21/55 in sda;
  - **totale: 0/59** in entrambe le configurazioni;
  - in F7 era 56/56. Il radar è cieco proprio quando i frammenti arrivano.
- **Regole.**
  - Ho scritto solo file nuovi:
    - in `05-scorta/`: `PREVISIONI_RADAR.md`, `CONGELAMENTO_RADAR.md`, `scorta_f7r.py`, `passaggi_f7r_*`,
      `risultati_f7r_*`, `esito_*_f7r.txt`, `esito_convalida_F7r.txt`, `avvio_valutazione_f7r.txt`;
    - i registri `prototipo/uscite/video_volo/registro_F7r_*.jsonl`.
  - Niente cancellazioni, niente git.
  - Rete: tre ricerche e due letture, senza dettagli del progetto.
  - **Violazione possibile:** la valutazione usava 6 processi figli più il padre (7 in tutto) contro un limite di 6.
  - Il raggio dello sviluppo con 5 semi (20261123) è stato scritto prima nelle previsioni.
  - **Difetto noto:** nel registro la C è quella 3D (χ²₃), mentre il confronto con la curva usa la C 2D della formula.

## 1. Modello aggiunto in `scorta_f7r.py` (tutto I)

- **R1, saturazione del ricevitore:** nessuna misura radar per d_rad = 0,2 + 1,8·(100 − d)/70 s (30 m → 2 s, 100 m → 0,2 s).
  - La saturazione la segnala il ricevitore (innesco ottimista).
  - Durante la saturazione e per 3 scansioni dopo, niente «libero».
  - Stato del radar nel registro: `non_affidabile_saturazione`, poi `ripristinato_dichiarato`.
- **R2, occultamento:** Pd del bersaglio × 0,3 quando la linea di vista passa nella sfera della nube (baricentro e 80°
  percentile dei frammenti), per 3 s.
- **R3, cella `totale`:** urto a 30–50 m davanti, radar cieco 2 s, camera saturata 2–3 s, fumo.
- **Contromisure scritte prima:**
  - la saturazione radar vale come indizio d'evento;
  - t0 del volume dei detriti è l'inizio della saturazione.
- **Riacquisizione** (definizione): misura vera del bersaglio associata alla sua traccia, oppure riacquisizione
  presunta da una traccia nata in maggioranza dal bersaglio. Una riacquisizione presunta da un'altra traccia conta
  come spuria.
## 1. Tabella fisica (ordini di grandezza; I = ipotesi, F = fonte)

Lunghezze d'onda: banda X 3 cm, Ku 1,9 cm, mmW a 77 GHz 3,9 mm; visibile 0,4–0,7 µm; MWIR 3–5 µm; LWIR 8–12 µm.
Parametro di dimensione x = πd/λ: se x ≪ 1 (Rayleigh) la sezione di diffusione va come x⁴ e la particella è trasparente.

| Effetto | Radar X/Ku/mmW | Camera EO | IR (MWIR/LWIR) | Camera a eventi | Durata (I) |
|---|---|---|---|---|---|
| **Fumo** (fuliggine 0,1–1 µm, polvere 1–100 µm) | **non degradato.** x ≈ 10⁻⁴–10⁻¹ anche a 77 GHz: diffusione trascurabile. Esperimenti a 79 e 300 GHz attraverso fumo denso e fiamme vedono gli oggetti (F2, non verificato dal testo) | **accecata** lungo la linea di vista: x ≈ 1 (Mie), estinzione massima | **degradato**: in LWIR la fuliggine è piccola rispetto a λ e passa meglio del visibile; il fumo caldo però emette e fa ingombro (I) | **accecata** come la EO (stessa ottica nel visibile) | finché il fumo copre la linea di vista: 5–20 s nel simulato (I) |
| **Fiammata, luce** (palla di fuoco 1000–2000 K, metri) | **nessun effetto** della luce | **accecata** per saturazione: 0,5–3 s più il recupero dell'esposizione automatica (qualche fotogramma, I) | **accecato**: il picco di Planck a 1500 K cade a circa 2 µm, MWIR e LWIR saturano, possibile alone sul rivelatore raffreddato (I) | **degradata, non accecata**: gamma dinamica alta (circa 120 dB, I) ma raffica di eventi che satura la banda di lettura (I) | durata della palla di fuoco: 0,5–3 s (I) |
| **Fiamma ionizzata** | **degradato solo se la linea di vista attraversa la fiamma.** Fiamma vegetale a 1050 K in banda X (8–9,6 GHz): ε'' ≈ 0,11–0,12, cioè assorbimento collisionale misurabile (F1). Con ne ≈ 10¹⁶ m⁻³ la frequenza di plasma è fp = 8,98·√ne ≈ 0,9 GHz ≪ 10 GHz: nessuna riflessione, solo attenuazione di qualche dB per metro di fiamma (ordine dalla stessa linea di ricerca, I). Batteria al litio: il litio (potenziale di ionizzazione 5,4 eV) può alzare ne di 1–2 ordini (I), e fp arriva a 3–9 GHz: la banda X si avvicina al taglio nel nucleo, mmW resta trasparente. La fiamma dà anche un'eco propria debole (I) | luce: vedi la riga sopra | luce: vedi la riga sopra | vedi la riga sopra | 0,5–3 s, su 1–5 m di fiamma (I) |
| **Nube densa di detriti vicina** | **degradato, e accecato solo se molto vicino.** (a) *Eco forte:* a parità di guadagno, l'eco va come σ/R⁴. Un corpo da 0,03 m² a 30 m sta circa 33 dB sopra un bersaglio da 0,02 m² a 200 m; 30 frammenti e 2 corpi sommano altri 5–15 dB. (b) *Saturazione del ricevitore o del convertitore (ADC):* nei radar FMCW il filtro passa-alto sui battimenti attenua le distanze piccole, quindi la saturazione vera è plausibile sotto i 20–30 m, oppure con corpi grandi (I). Il guasto atteso è l'**AGC** che abbassa il guadagno e la Pd del bersaglio, per il tempo della costante dell'AGC (da ms a 100 ms) più l'elaborazione (I). Lo 0,2–2 s di F7r è **pessimista**. (c) *Blanking a breve distanza:* nel radar a impulsi c'è un'eclissi di c·τ/2 (1 µs → 150 m): la nube vicina resta invisibile, il bersaglio no; nel FMCW la portata minima è di pochi metri (I). (d) *Cammini multipli:* rimbalzi bersaglio-nube-radar danno echi fantasma più lontani della nube, con Doppler spostato (I). (e) *Occultamento:* l'ostruzione geometrica è trascurabile (30 frammenti da 1–10 cm in 20 m: meno dello 0,1 % della sezione del fascio, I). Ciò che nasconde il bersaglio è il **mascheramento CFAR** o i lobi laterali nella stessa cella di distanza e Doppler, non il blocco fisico | **degradata**: occlusioni sparse, sfocatura e scie dei frammenti veloci (I) | **degradato**: i frammenti caldi sono sorgenti puntiformi, falsi bersagli (I) | **degradata**: i frammenti veloci generano molti eventi; separa bene il moto (I) | nube densa: 1–3 s (si disperde a ~50 m/s); detriti in aria: 5–20 s |
| **Impulso elettromagnetico** (esplosione chimica piccola, batterie) | **trascurabile**: per esplosivi chimici il campo misurato è da mV/m a decine di V/m, scala con la massa ed è lungo circa µs (F3, non verificato nel testo). Due droni non portano esplosivo: niente detonazione, al più deflagrazione. Un ricevitore schermato non ne risente; al più un picco su una rampa (< 1 ms) | trascurabile (I) | trascurabile (I) | trascurabile (I) | < 1 ms (I) |

Fonti (al più 4):
- **F1.** K. M. Mphale, D. Letsholathebe, M. L. Heron, «Effective complex permittivity of a weakly ionized vegetation
  litter fire at microwave frequencies», *J. Phys. D: Appl. Phys.* 40 (2007) 6651–6656,
  doi:10.1088/0022-3727/40/21/026, https://researchonline.jcu.edu.au/2588/1/17382_Mphale_et_al_2007.pdf.
  **Verificata** (letto l'abstract: fiamma a 1050 K, 8,0–9,6 GHz, ε'' 0,113–0,119, ε' 0,898–0,903). La fiamma è
  vegetale, non da idrocarburi o batterie: il trasferimento è un'ipotesi.
- **F2.** Bystrov et al., *Sensors* 21(2):439, 2021 (radar a 79 e 300 GHz in fuoco e fumo),
  https://research.birmingham.ac.uk/files/223804685/sensors-21-00439.pdf. **Non verificata**: la pagina risponde 403,
  ho solo il riassunto della ricerca.
- **F3.** Rapporto di Los Alamos sull'impulso elettromagnetico di esplosioni chimiche,
  https://sgp.fas.org/othergov/doe/lanl/lib-www/la-pubs/00356917.pdf. **Non verificata**: solo un estratto della
  ricerca, con l'OCR rovinato.

## 2. Esiti (valutazione, semi 20261122)

60 passaggi per cella e 200 per F7c. Wilson al 95 % per passaggio. Stato di tutte le righe: **sim**.

Classi:
- **S** = solido: limite inferiore ≥ 0,90, oppure 0/N con limite superiore ≤ 0,06;
- **I** = incoraggiante: limite inferiore ≥ 0,80;
- **L** = limite: limite inferiore ≥ 0,50;
- **NP** = non provato.

| Misura | lato att / sda | davanti att / sda | vira att / sda | totale att / sda | F7c att / sda |
|---|---|---|---|---|---|
| Continuità (P1) | 60/60 [0,940; 1] S / 60/60 S | 60/60 S / 60/60 S | 60/60 S / 60/60 S | **59/60 [0,911; 0,997] S, smentita** / 60/60 S | 200/200 [0,981; 1] S / S |
| Riacquisizione ≤ 2 s dal ritorno del radar (P2) | 60/60 S (max 1,32 s) / 60/60 S (0,30 s) | **41/60 [0,558; 0,787] L** / 60/60 S (1,25 s) | **43/60 [0,592; 0,815] L** / 56/60 [0,841; 0,974] I | 59/60 [0,911; 0,997] S / 58/60 [0,886; 0,991] I | — |
| «Libero» sul bersaglio o su un frammento (P3) | 0/60 [0; 0,060] S / S | 0/60 S / S | 0/60 S / S | 0/60 S / S | 0/200 [0; 0,019] S / S |
| Spurie non dichiarate (P4) | 0/60 S / S | 0/60 S / S | 0/60 S / S | **1/60 [0,003; 0,089] I, smentita** / 0/60 S | 0/200 S / S |
| Identità a fine passaggio (entro 30 m) | 60/60 S / S | 56/60 I / 60/60 S | 49/60 [0,701; 0,894] L / 58/60 I | 60/60 S / 58/60 I | 200/200 S |
| Evento dichiarato | 0/60 (fuori campo) / 60/60 S | **41/60 L** / 60/60 S | **33/60 [0,425; 0,669] NP** / 60/60 S | **7/60 NP** / 60/60 S | falsi 0/200 S / S |
| Avviso prima del frammento entro 10 m | — | **27/52** / **28/52** | **19/55** / **21/55** | **0/59 / 0/59** | — |
| Volume dei detriti: frammenti dentro | — | tutti i campioni dentro, quando il volume esiste | uguale | uguale | — |

**Cause, misurate sui casi mancati:**
- **Riacquisizione in att.** Fra i casi mancati, l'evento era dichiarato in 18 su 19 (davanti) e in 16 su 17 (vira);
  fra quelli riusciti, solo in 23 su 41 e in 17 su 43.
  - Il bersaglio sta dentro il volume dei detriti, che cresce di circa 90 m/s.
  - Dopo 1 s di perdita si riaggancia solo con una riacquisizione presunta **fuori** dal volume, quindi resta
    «regione».
  - È la prudenza del volume che costa la riacquisizione, non l'accecamento in sé: era fra le attese scritte prima.
- **Caso totale/att idx 34.** Una riacquisizione presunta da una traccia che non era del bersaglio: 41 cicli fuori
  dalla regione. È l'unico errore d'identità non dichiarato.
- **Evento non dichiarato in att.**
  - Dopo 2 s di cecità i frammenti sono sparsi su circa 100 m e manca il grappolo di 5 misure entro 40 m.
  - Il radar a ±60° e a 5 Hz ne raccoglie troppo poche.
  - Il radar però è dichiarato `non_affidabile_saturazione` in ogni ciclo, e non c'è mai «libero».
- **Avviso.** A 30–50 m, con frammenti a circa 50 m/s, i frammenti arrivano prima che il radar torni. Nessun avviso
  basato sul volume localizzato può precederli.

**Confidenza contro C(τ) di `curva_F7.json`** (perdita totale), media sui cicli di cecità:

| | τ = 1,0 s | τ = 1,5 s | τ = 2,0 s |
|---|---|---|---|
| att, curva | 0,983 | 0,840 | 0,621 |
| att, osservata | 0,990–0,991 | 0,895–0,905 | 0,683–0,731 |
| sda, curva | 0,999 | 0,935 | 0,734 |
| sda, osservata | 0,998–0,999 | 0,943–0,951 | 0,782–0,823 |

- La curva cade **un po' prima** del filtro: è prudente di 0,05–0,11.
- La quota dei cicli col bersaglio vero dentro la r_0,9 3D durante la cecità è **0,92–1,00** (1,00 per τ ≥ 1 s).
- La curva è una descrizione onesta, e conservativa, della perdita totale: **I**.
- P5 è smentita al margine soltanto perché lo scarto supera 0,10 a τ = 2 s (lato, davanti e vira in att).

**Registri video** `prototipo/uscite/video_volo/registro_F7r_{lato,davanti,vira,totale,F7c}.jsonl` (sda, idx 0):
validatore `prototipo/prove/convalida_volo.py` (la copia di `f19-volo/10-prove/` non esiste a quel percorso), **0
violazioni su 5 × 240 fotogrammi** (`esito_convalida_F7r.txt`).

## 3. Frasi per la giuria

| Italiano | English | Classe |
|---|---|---|
| «Abbiamo accecato anche il radar fino a 2 secondi, insieme alle camere: MoVi non ha mai detto "libero" né sul drone seguito né sui frammenti, 0 su 60 in ogni caso, e ha dichiarato il radar non affidabile in ogni istante.» | "We also blinded the radar for up to 2 seconds, together with the cameras: MoVi never said 'clear' on the tracked drone or on any fragment, 0 of 60 in every case, and flagged the radar as unreliable at every instant." | S, sim |
| «Con la perdita totale il drone seguito resta nella regione dichiarata in 59 passaggi su 60 col radar piccolo e in 60 su 60 col radar a 360 gradi.» | "Under total sensor loss the tracked drone stays inside the declared region in 59 of 60 runs with the small radar and 60 of 60 with the 360-degree radar." | S, sim |
| «La confidenza che MoVi dichiara scende come la curva calcolata in anticipo, ed è un po' più prudente.» | "The confidence MoVi reports falls as the precomputed curve predicts, slightly on the cautious side." | I, sim |
| «Col radar a 360 gradi il drone si riaggancia entro 2 s dal ritorno del radar in 56–60 passaggi su 60; col radar piccolo frontale, quando l'urto è davanti, solo in 41–43 su 60: MoVi lo dichiara come regione, non come identità.» | "With the 360-degree radar the drone is re-acquired within 2 s of radar recovery in 56–60 of 60 runs; with the small forward radar and a collision ahead, only 41–43 of 60: MoVi reports a region, not an identity." | I / L, sim |

**Da non dire:**
- «Il radar vede attraverso l'esplosione»: vale per il fumo e la luce, non per la nube vicina.
- «Avvisa sempre dei detriti»: con il radar accecato, 0/59 nella cella peggiore.
- «Riacquisisce sempre».
- «Validato».

## 4. Limiti e migliorie

| Limite | Miglioria | Prova che la decide |
|---|---|---|
| **Avviso dei detriti: 0/59 con la perdita totale** | Avviso immediato «evento vicino non localizzato» quando il radar e la camera saturano insieme; la direzione dal lampo nell'immagine e un volume centrato sul portatore | avviso prima del frammento entro 10 m ≥ 0,9, con falsi in F7c ≤ 0,05 |
| Riacquisizione bloccata dal volume (att) | Riacquisizione presunta anche nel volume, se Doppler e velocità sono coerenti con il bersaglio e incoerenti con la dispersione; identità «presunta_dubbia» | davanti/att ≥ 51/60 con spurie non dichiarate 0/60 |
| Evento non dichiarato dopo la cecità (att 7–41/60) | La saturazione stessa apre l'evento, anche senza il grappolo | evento ≥ 57/60 in att davanti e totale |
| Riacquisizione presunta sbagliata (1/60) | Esigere la coerenza Doppler per più scansioni | 0/60 |
| R1 di 0,2–2 s è pessimista e non viene da una scheda; R2 × 0,3 è inventato | Modello dell'AGC e dell'ADC dalla scheda del radar; controllo del filtro passa-alto (STC) | registrazioni con detriti vicini |
| Fiamma ionizzata, cammini multipli e impulso non simulati; nessuna camera a eventi | Attenuazione di qualche dB sulla linea di vista nella palla di fuoco; echi fantasma dietro la nube | spurie non dichiarate 0/60 con i fantasmi |
| Stesso tracciatore dell'autore F7; fonti F2 e F3 non verificate | Revisione indipendente; lettura dei testi completi | — |
