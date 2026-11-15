# Scenari di volo F1–F6 per il caso centrale (f19-volo/04-scenari)

Ruolo: `sciame-scene-dinamiche`. Data: 15-11-2026, dalle 04:36 alle 04:50 (`date -Is`). Tutto è **simulazione o
conto**: nessun sensore fisico, nessun dato registrato di un incidente. Etichette di classe a mano. Ambito: solo
osservazione, monitoraggio e avviso. Gli incidenti in volo sono eventi da osservare e segnalare.

## 0. Cambi di stato e regole

- **P4 smentita al primo giro, poi corretta: era un difetto del simulatore, non del volume.** Alla prima prova (04:42)
  i frammenti dentro V(τ) erano 0,978 in F3 e 0,945 in F4 (soglia 0,99). Il controllo dei campioni fuori da V mostra
  frammenti a 100–300 km dal punto dell'evento già a τ = 0,5 s. La causa è l'integratore di Eulero esplicito di
  `eventi_lp.frammenti`: con |v| ≈ 195 m/s, v_t ≈ 6 m/s e dt = 0,05 s, il prodotto g|v|dt/v_t² ≈ 2,6 supera 2. Ho
  scritto in `eventi_volo.frammenti_volo` una resistenza semi-implicita, che è stabile con qualunque passo. Dopo la
  correzione: **F3 600/600 frammenti sempre dentro V** (Wilson 95 % [0,9936; 1]), **F4 1000/1000** ([0,9962; 1]),
  **0 frammenti a terra fuori dall'impronta** in entrambi (**simulato**). La prima versione resta accanto:
  `prova_frammenti_volo_v0_euler_instabile.json`.
- **Il difetto è nel simulatore di f15 ma non cambia E1 ed E2.** Ho rifatto 300 frammenti per ciascuno (seme 1): 0 su
  300 oltre i 10 km. Eulero però porta il frammento più lontano di E1 a 154 m, contro i 130 m del semi-implicito. Va
  all'arbitro: non ho verificato se questo sposti le misure di E1, e la correzione andrebbe in una versione nuova
  accanto a `eventi_lp.py`.
- **La nota di F1 era sbagliata e l'ho corretta.** Avevo scritto «distanza minima circa 128 m»; il conto dà **40,8 m a
  t = 80,0 s**. F1 diventa una **quasi collisione**, e quindi una prova dura per i falsi eventi.
- **r0 dell'inviluppo corretto.** Nella prima versione di `conti_volo.json` r_inv(0) era più piccolo di r99(0) (30
  contro 33,7 m). Ora r0 = 3,4 s0; la prima versione è in `conti_volo_v0_r0_basso.json`.
- **I sensori sono segnaposto.** La cartella `f19-volo/02-sensori-hw` era vuota alle 04:36, quindi il radar a schiera
  attiva si simula con `radar_sorveglianza_droni` (banda X, 360°, 1 s), marcato `segnaposto_per`.
- **Regole.** Non ho cancellato niente e ho scritto solo in questa cartella. Le fonti marcate «P» (procedure ICAO e
  FAA) le cito da conoscenza: **non le ho riaperte in rete, quindi non sono verificate**.

## 1. Gli scenari (`scenari_volo.json`, formato di `scenari_eventi.json`)

| id | Geometria (C = conto, I = ipotesi) | Eventi | Che cosa mette alla prova |
|---|---|---|---|
| F1 | Aereo sul sentiero di 3° (z = 15 + \|x\| tan 3°), 75 m/s (cat. C/D, P), soglia a t = 120 s. Un drone non cooperante attraversa a x = −3000 m e z = 172 m, a 20 m/s; distanza minima 40,8 m a t = 80,0 s (C) | nessuno | Avviso d'intrusione nel tubo del sentiero (raggio 150 m, I), con almeno 20 s d'anticipo; il «candidato di contatto» **non** deve diventare un evento |
| F2 | Salita da 90 a 125 m/s (P: 250 kt sotto 10000 ft), dentro una cella di pioggia in quota (raggio 1,5 km, da 0 a 1600 m). Un aereo leggero non cooperante attraversa la cella | nube in quota (nuova) | Portata ridotta dichiarata (radar ×0,70; EO ×0,26; IR ×0,29, prudenti da f15-40-01); «solo radar, ridondanza assente»; giri mancati con C(τ) |
| F3 | Due droni a 40 e 35 m/s si urtano a 120 m di quota (t = 20 s); B cade, A prosegue danneggiato a 25 m/s | collisione, vc = velocità dei droni (nuovo) | Evento entro 2 s; V(τ) con la pianta allungata lungo vc; impronta di 5,1 km (C); nessun «libero» dentro |
| F4 | Aereo a 135 m/s e 450 m; avaria non contenuta a t = 30 s; poi virata e discesa lenta | avaria + fiammata (EO cieca 5 s, IR 13 s) + fumo in quota | Affidabilità persa entro 3 quadri; «separazione (dedotto)» entro 2 s; impronta di 6,8 km (C); aereo «vista (radar)», classe sospesa |
| F5 | Aereo a 80 m/s e drone a 45 m/s si incrociano a 300 m di quota; distanza minima 39,2 m a t = 40,24 s (C) | **perdita totale degli ottici** per 3 s (varianti 2 e 4 s) + nube | Solo radar; continuità e identità con curva di confidenza; nessun evento di contatto |
| F6 | Controllo: due aerei a 120 e 100 m/s, separati di 300 m in quota e 1,5 km in pianta | nessuno | 0 falsi eventi, 0 tracce non risolte |

Ogni scenario contiene la `sceneggiatura_attesa` (che cosa il sistema deve dichiarare, intervallo per intervallo, con
la soglia `entro`) e le `misure`:

- tempestività;
- continuità;
- ritardo dell'evento;
- frammenti dentro V;
- «libero» dentro il volume;
- falsi eventi;
- confidenza prevista contro osservata;
- scambi d'identità osservati contro previsti.

## 2. La perdita di confidenza nel tempo (forma chiusa, `eventi_volo.py --conti`)

**Modello (ipotesi dichiarata).** L'errore di posizione predetto è gaussiano e isotropo. Il moto è a velocità costante
con rumore bianco d'accelerazione di densità q. Per asse:

σ²(τ) = s0² + sv0²·τ² + q·τ³/3

Questa varianza è **esatta per quel modello (dimostrato: è la covarianza dell'integrale doppio del rumore bianco)**. La
confidenza che l'oggetto sia nella porta di raggio g è:

C(τ) = F_χ²₃(g²/σ²(τ)), con F_χ²₃(x) = erf(√(x/2)) − √(2x/π)·e^(−x/2)

Il sistema dichiara anche due zone:

- **zona al 99 %**: r99 = 3,368·σ(τ);
- **zona garantita**, non probabilistica, se |a| ≤ a_max: r_inv = r0 + dv·τ + a_max·τ²/2.

Lo stato «non vista da τ s» porta tutte e tre le grandezze: C(τ), r99 e r_inv.

| Caso (parametri I) | C a 1 s | C a 2 s | C a 3 s | C a 5 s | C < 0,9 dopo | C < 0,5 dopo | r99 a 3 s | r_inv a 3 s |
|---|---|---|---|---|---|---|---|---|
| aereo, solo radar (s0 15 m, g 50 m, a_max 3) | 0,987 | 0,976 | 0,937 | 0,688 | 3,48 s | 6,11 s | 62 m | 83 m |
| drone veloce (s0 10 m, g 30 m, a_max 6,9) | 0,934 | 0,669 | 0,312 | 0,058 | 1,24 s | 2,43 s | 83 m | 92 m |
| mezzo danneggiato (sv0 10 m/s, a_max 10) | 0,723 | 0,241 | 0,075 | 0,012 | 0,61 s | 1,39 s | 147 m | 169 m |

- **Controllo Monte Carlo** dello stesso modello (2·10⁵ campioni, passo esatto del modello discreto): scarto massimo
  0,0017. P5 (≤ 0,005) **regge**. È **calcolato**, e il controllo non è indipendente dal modello.
- **Scambio d'identità alla riacquisizione (F5).** Con l'assegnazione a costo minimo lo scambio vince se
  d·(e_b − e_a) > |d|², e d·(e_b − e_a)/|d| segue N(0, 2s²). Quindi p_scambio = Φ(−d/(√2·s)) (**dimostrato** per
  errori gaussiani indipendenti e isotropi). Il controllo Monte Carlo dà 0,1444 contro 0,1444 (4·10⁵ campioni).
- **In F5** (d = 39 m, σ_mis = 33 m del radar a 2,5 km), p_scambio vale 0,214 / 0,227 / 0,252 / 0,285 dopo 1 / 2 / 3 /
  4 s di predizione. La confidenza d'identità è quindi 0,79–0,71: per questo l'identità resta «presunta». A 166 m,
  p_scambio scende a 0,002. P6 ([0,05; 0,4]) **regge**.
- **Che cosa resta da misurare.** La confidenza prevista contro quella osservata nel nucleo (per i cicli «non vista»,
  la quota di casi con il vero dentro r99) è una **prova da fare** con il nucleo v3: non l'ho eseguita in questo
  turno.

## 3. Estensioni del simulatore (`eventi_volo.py`; `eventi_lp.py` non toccato, solo importato)

1. **`frammenti_volo`**: i frammenti partono con la velocità del mezzo (vc) più u, con |u| ≤ dv. La resistenza è
   semi-implicita, con t_max = 90 s. In F4 alcuni frammenti con v_t = 5 m/s sono ancora in aria a 90 s: è un limite
   dichiarato. `frammenti_volo_euler` resta come traccia.
2. **Nube in quota**: un cilindro fra z_base e z_top, con deriva 3D e crescita (`nube_quota_al_tempo`,
   `segmento_in_cilindro`, campionato in 96 punti).
3. **Perdita totale degli ottici**: il tipo nuovo `perdita_ottici_totale` dà finestre di cecità a tutte le camere
   (`finestre_cecita`).
4. **`SensoreVolo`** (sottoclasse di `SensoreSim`) applica 2 e 3 attraverso `visibile()` e `salute`. **Non
   verificato** con un passaggio completo del nucleo: `scansioni()` chiama `self.visibile` (riga 298 di `sim_lp.py`),
   ma il cablaggio di F1–F6 dentro un `passaggio()` per il volo non è scritto.
5. **`--prova`**: i frammenti di F3 e F4 contro V(τ) e l'impronta di `frammenti.py` (risultati nel § 0).

## 4. Stati proposti

| Enunciato | Stato |
|---|---|
| Con vc del mezzo, i frammenti di F3 e F4 stanno sempre dentro V(τ) di frammenti.py (profili prudenti) | **simulato**: 600/600 [0,9936; 1] e 1000/1000 [0,9962; 1]; 10 passaggi; stessa fisica ipotizzata e stesso autore della regola |
| Primo frammento a terra in F3: 4,9 s senza resistenza da fermo (C); 3,4 s nel simulato (spinta verso il basso) | P1: regge il conto; il simulato è più rapido, ma l'avviso entro 2 s resta prima del primo impatto |
| Impronta F3 > 1 km; F4 > 3 km | P2 e P3 reggono: 5,1 km e 6,8 km (**calcolato**, prudente). È **onesto ma grande**: per un'impronta utile servono la misura della velocità dei frammenti (Doppler) e un profilo per classe |
| C(τ) in forma chiusa | **dimostrato** nel modello gaussiano a rumore bianco; parametri **ipotesi** |
| F1, F2, F5, F6: sceneggiatura rispettata dal nucleo | **non risolto**: il cablaggio nel nucleo manca; lo decide un `passaggio()` per il volo con N ≥ 60 a scenario e Wilson |
| F6: 0 falsi eventi | **ipotesi** (P7 non provata) |

## 5. Proposte e passi dopo

- **Correggere l'integratore di f15 in una versione nuova accanto** (`eventi_lp_v2.py`, con la resistenza
  semi-implicita) e rifare E1 ed E2, per vedere se il 51/60 si sposta.
  - Previsione: la variazione è minima, perché 0/300 frammenti superano i 10 km.
  - Smentita: un cambio ≥ 3/60.
- **Scrivere `passaggio_volo()`** su `SensoreVolo` con F1–F6: 60 passaggi a scenario (F6: 300), tutte le misure del
  JSON, la confidenza prevista contro osservata.
  - Soglia di smentita: la quota del vero dentro r99 ha un Wilson superiore < 0,97.
- **Impronta di chilometri.** Ridurla con la velocità radiale misurata sui frammenti (radar Doppler o LiDAR FMCW,
  da `02-sensori-hw`) al posto di dv = 100–120 m/s a priori.
  - Previsione: con dv misurato a ±15 m/s l'impronta di F3 scende sotto 1,5 km. Non calcolato.
- **Per l'allegato, i limiti da dichiarare:**
  - fisica dei frammenti ipotizzata;
  - nube cilindrica;
  - scia di fumo lungo la rotta non modellata;
  - frammenti in aria oltre 90 s;
  - classe «aereo_volo» e «drone_veloce» da aggiungere alle regole di f15-04;
  - sensori segnaposto;
  - nessun hardware.
