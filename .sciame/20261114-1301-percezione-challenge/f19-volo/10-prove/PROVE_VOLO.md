# Prove degli scenari di volo F1–F6 (sciame-validazione, f19-volo/10-prove)

15-11-2026, dalle 04:47 alle 05:30 (`date -Is`). Previsioni e soglie scritte **prima** in `PREVISIONI.md` (04:49:34),
con tre aggiunte **a posteriori** marcate (04:53, 05:04, 05:16). Tutto è **simulato** (nucleo `movi_lp_v3.py` + strato
eventi `eventi_v3.py` + estensioni di volo `eventi_volo.py`, sensori dalle schede). Nessun sensore fisico, nessuna
prova su hardware, etichette a mano, ADS-B spento (ipotesi prudente). Le latenze «sda» dell'elaborazione dedicata
sono **stime** per analogia (`02-sensori-hw/latenza.json`), non misure. Wilson 95 % **per passaggio** salvo dove è
scritto «campioni» (correlati: Wilson ottimista). Solo osservazione, monitoraggio e avviso.

## 0. In testa: cambi di stato e regole

- **Regole.** Nessun file cancellato (due run interrotti con `pkill`: i file parziali restano, `passaggi_volo.jsonl`
  con la misura di calibrazione sbagliata e `passaggi_volo_v4_interrotto_senza_inviluppo210.jsonl`). Niente git, niente
  sudo, nessuna rete. Al più 8 processi (7 figli + padre). Due misure corrette dopo i primi dati: (a) un campione di
  «perdita» conta solo se nessuna traccia vede l'oggetto (prima contavano i doppioni stantii: v3b); (b) l'avviso di
  prossimità ignora le coppie già entro 300 m (doppioni). Sono correzioni della **misura**, dichiarate.
- **Fatto nuovo (difetto del nucleo, trovato qui).** L'insieme di possibile presenza del nucleo usava l'inviluppo delle
  classi (v_max 90 m/s), non i 210 m/s decisi dal coordinatore, che stavano solo nello strato eventi. Con aerei a
  120–135 m/s il vero **esce** dalla regione dichiarata: F6/att vero in r99 o insieme 0,272 [0,228; 0,321] (campioni),
  F4/att dopo l'avaria 0,144 [0,124; 0,166]. Con la correzione (v4/v3i, `m.inviluppo` avvolto, `movi_lp_v3.py`
  intatto): **0,984 [0,966; 0,993]** e **1,000 [0,996; 1]**. P14 regge.
- **Smentite.** P1 (F3 evento entro 2 s): **0/60 in att e in sda** con le regole v3: i ritorni dei frammenti
  (RCS 2·10⁻⁴ m²) non arrivano dal radar a 2,1 km; l'E1 51/60 **non si trasferisce** al volo. P3 (zona al 99 % della
  covarianza del nucleo): smentita ovunque (0,02–0,91). P12/P13 (regola v4 «impulso»): rileva F3 59/60 entro 2 s ma
  con falsi eventi 198/200 in F6/att e con l'evento aperto **prima** dell'urto (mediana −10 s): **v4 respinta**. P10 (sda più rapido in F3) non è decidibile: nessun evento F3 in v3/v3i; in F4 il ritardo mediano scende da 0,3 a 0,1 s (non è ≥ 0,5 s).

## 1. Che cosa è stato eseguito

`prove_volo.py` riusa `eventi_v3.passaggio` tale e quale (sorgente letta con `inspect`) con **un gancio** per ciclo;
`prepara_volo` costruisce verità e sensori da `scenari_volo.json` (frammenti con l'integratore semi-implicito di
`eventi_volo.frammenti_volo`; nubi in quota e cecità degli ottici con `SensoreVolo`). Configurazioni: **att** = radar
`radar_sorveglianza_droni` 1 Hz rotante, camere EO/IR del catalogo, latenza scheda + 80 ms CPU; **sda** = radar AESA
10 Hz (EchoShield, scheda **non aperta**; r_rif 1400 m per 0,01 m², 4 pannelli: I), camere a 10 Hz, latenza scheda +
1,2 ms dedicata (STIMA). N = 60 per scenario e configurazione (F6: 200; F5: 20 per durata di cecità 2, 3, 4 s), semi
`SeedSequence(20261119, …)`. Tre giri completi (più due interrotti): **v3b** (regole f15 v3), **v4** (v3 + impulso + inviluppo 210),
**v3i** (v3 + solo inviluppo 210: è la configurazione proposta). Un record per passaggio: `passaggi_volo_{v3b,v4,v3i}.jsonl`;
aggregati `risultati_volo_*.json` (`analizza_volo.py`); `rifai.sh` rifà tutto (circa 30 min con 7 processi).

## 2. Risultati (simulato; [Wilson 95 % per passaggio])

Configurazione proposta **v3i** (`risultati_volo_v3i.json`); att | sda. «Libero» sul punto vero dell'oggetto: **0
passaggi in tutte le 12 celle** (per esempio F6: 0/200 [0; 0,019]); «libero» su un frammento vero dentro l'impronta:
0/60 in F3 e F4.

| misura | att | sda | soglia (prima) |
|---|---|---|---|
| F1 avviso di prossimità con anticipo ≥ 20 s sul CPA vero (80 s) | 60/60 [0,940; 1], mediana 74 s | 56/60 [0,841; 0,974], mediana 33 s | P9 ≥ 0,90: regge |
| F1/F2/F5 falsi eventi | 0/60 ciascuno [0; 0,060] | 0/60 ciascuno | P5, P9: reggono |
| F6 falsi eventi | **0/200 [0; 0,019]** | **0/200 [0; 0,019]** | P6: regge |
| F3 evento (collisione dei droni) entro 1 / 2 / 3 s | 0/60 [0; 0,060] | 0/60 | P1: **smentita** |
| F3 avviso di prossimità prima dell'urto (≥ 10 s) | 60/60 [0,940; 1], mediana 18,0 s | 60/60, mediana 19,5 s | (non previsto: a posteriori) |
| F4 evento (avaria + fiammata) entro 1 s | 60/60 [0,940; 1], ritardo 0,2–0,4 s | 60/60, 0,1–0,2 s | P2 ≥ 0,80: regge |
| F4 camere «affidabilità persa» entro 3 cicli | 60/60 [0,940; 1] | 60/60 | P2: regge |
| F4 tempestivo per un sistema di bordo (dichiarazione + 0,001 + 0 + 2 s prima del primo frammento a terra, 8,9 s) | 60/60, margine mediano 6,65 s | 60/60, 6,85 s | P11 era su F3: lì 0/60 (smentita); F4 non previsto |
| F4 tempestivo per l'operatore (+ 0,05 + 5,4 + 2 s) | 60/60 [0,940; 1], margine mediano **1,2 s** | 60/60, 1,4 s | P11b su F3: 0/60 (regge, per assenza d'evento); F4 non previsto |
| F4 frammenti conformi dentro V(τ) (campioni) | 0,9991 [0,9990; 0,9992] | 0,9950 [0,9948; 0,9952] | P8 ≥ 0,99: regge |
| F4 passaggi con tutti i frammenti in V | 58/60 [0,886; 0,991] | 58/60 | — |
| F4 raggio dell'impronta (mediana) | 6,9 km | 6,8 km | (prudente, grande) |
| F5 cecità totale degli ottici 2–4 s: tracce con regione per tutta la cecità | 60/60 [0,940; 1] | 60/60 | P5: regge |
| F5 scambio d'identità alla riacquisizione | 28/60 = 0,47 [0,35; 0,59] | 38/60 = 0,63 [0,51; 0,74] | previsto 0,21–0,29 (03-confidenza): **fuori** |
| Continuità: passaggi senza alcun ciclo senza regione | F1 39/60 [0,52; 0,76]; F6 186/200 [0,886; 0,958]; F2–F5 60/60 | **tutte le celle 60/60 o 200/200** [0,940 (0,981); 1] | P4 ≥ 0,95: regge in sda, smentita in att (F1, F6) |
| Vero dentro r99 **o** insieme di presenza nei cicli di perdita (campioni; primo per passaggio) | F1 0,993; F4 dopo l'avaria 1,000 (1072/1072); F6 0,984 [0,966; 0,993]; altre 1,000 | 1,000 in tutte (per esempio F3 dopo l'urto 939/939 [0,996; 1]) | P14: regge |
| Vero dentro la sola zona al 99 % della covarianza del nucleo | 0,003 (F6) – 0,912 (F2) | 0,19 (F6) – 0,83 (F1) | P3: **smentita** |
| Tempo di calcolo per passaggio (Python, CPU, non è una misura di latenza) | 1,4–4,2 s | 2,7–7,9 s | — |

Confronto v3b (senza la correzione dell'inviluppo): F4/att continuità 13/60 [0,13; 0,34] e vero nella regione 0,144;
F6/att 126/200 e 0,272. La correzione v3i porta F4/att a 60/60 e F6/att a 186/200. Regola v4 «impulso»
(`risultati_volo_v4.json`): F3 entro 2 s 59/60 [0,911; 0,997] ma falsi eventi F6 198/200 (att) e 158/200 (sda),
F1 57/60: **respinta**.

### 2.1 Calibrazione della confidenza durante la perdita (la cifra del video)

Per ogni ciclo in cui **nessuna** traccia vede l'oggetto: C prevista = P(vero entro la porta g dalla previsione) con la
covarianza **del nucleo** (integrale esatto sull'ellissoide, `stima_v4.prob_gauss_ellissoide`); osservata = frequenza
del vero entro g. Configurazione v3b (la calibrazione non dipende dall'inviluppo).

| caso | C prevista (fascia) | C media | osservata (campioni) | un campione per passaggio |
|---|---|---|---|---|
| F2 att (aereo in salita, cella di pioggia) | 0,95–0,99 | 0,974 | 0,966 (592/613) | 56/60 = 0,933 [0,841; 0,974] |
| F2 att | 0,99–1 | 0,998 | 0,987 (1771/1795) | 59/60 = 0,983 [0,911; 0,997] |
| F2 att | 0,9–0,95 | 0,927 | 0,905 (277/306) | 44/51 = 0,863 [0,743; 0,932] |
| F2 att | 0,6–0,8 | 0,697 | 0,484 (199/411) | 20/53 = 0,377 [0,259; 0,512] |
| F1 sda (drone non cooperante) | 0,8–0,9 / 0,9–0,95 / 0,95–0,99 | 0,85 / 0,93 / 0,97 | 0,89 / 0,96 / 0,95 | 34/45; 40/42; 48/50 |
| F5 sda (solo radar, ottici ciechi) | 0,99–1 | 0,9997 | 0,998 (509/510) | 60/60 [0,940; 1] |
| F5 att | 0,95–0,99 / 0,99–1 | 0,974 / 0,999 | 0,872 / 0,968 | 27/31; 57/58 |
| F3 sda dopo l'urto (fuori modello) | 0,95–0,99 | 0,976 | 0,533 (24/45) | 14/24 = 0,583 [0,388; 0,755] |

**Perdita di confidenza nel tempo** (C media dichiarata contro osservata, per fasce di τ; campioni):
F1 sda: τ 0,5–1 s 0,77 / 0,69; 1–2 s 0,68 / 0,62; 2–3 s 0,57 / 0,57; 3–5 s 0,33 / 0,46; 5–10 s 0,06 / 0,24.
F5 att (aereo e drone, solo radar 1 Hz): 1–2 s 0,91 / 0,83; 2–3 s 0,90 / 0,81; 3–5 s 0,70 / 0,69.
F2 att: 1–2 s 0,85 / 0,79; 2–3 s 0,78 / 0,70; 3–5 s 0,76 / 0,28 (n = 39).

**Lettura.** Nel modello, le fasce alte (C ≥ 0,9) sono vicine all'osservato entro 0,01–0,10 (**incoraggiante**);
le fasce medie sono **ottimiste** di 0,1–0,3 (**limite**); oltre 3–5 s la formula diventa prudente (F1). Fuori dal
modello (dopo l'urto, dopo l'avaria) la covarianza del nucleo **non** vale: lì vale solo l'insieme di presenza, che ha
contenuto il vero nel **100 %** dei campioni (F3 sda 939/939; F4 v3i: vedi tabella). La zona al 99 % della sola
covarianza contiene il vero in 0,02–0,91 dei cicli (smentita P3): **non va mostrata come «99 %»**.

## 3. Classificazione (solido / incoraggiante / limite) e migliorie

| enunciato (simulato) | classe | intervallo | miglioria necessaria (quale e come) |
|---|---|---|---|
| Mai «libero» dove l'oggetto o un frammento è (12 celle, 1000 passaggi) | **solido** | 0/200 [0; 0,019] in F6; 0/60 [0; 0,060] altrove | provarlo con detriti densi e clutter reale (registrazioni) |
| Nessun falso evento con quasi collisioni a 40 m, incroci e cecità (v3i) | **solido** | F6 0/200 [0; 0,019]; F1, F5 0/60 | radar reale con clutter e uccelli |
| Avaria in volo con fiammata: evento entro 1 s, camere dichiarate inaffidabili entro 3 cicli | **solido** (nel modello della fiammata) | 60/60 [0,940; 1] | il baricentro della saturazione è un'ipotesi: misurarlo su camera vera |
| Avviso tempestivo per bordo e operatore in F4 | **incoraggiante** | 60/60 [0,940; 1], ma margine dell'operatore 1,2–1,4 s | dipende da 5,4 s di risposta umana (ipotesi di latenza.json) |
| Frammenti dentro V(τ) | **incoraggiante** | 0,995–0,9991 (campioni); 58/60 passaggi | fisica dei frammenti ipotizzata; impronta di 7 km: serve Doppler sui frammenti |
| Avviso di prossimità (F1 ≥ 20 s; F3 18–19,5 s prima dell'urto) | **incoraggiante** | 60/60 [0,940; 1]; sda F1 56/60 [0,841; 0,974] | regola semplice (CPA a velocità costante < 150 m): tarare i falsi avvisi su traffico reale |
| Continuità: il vero sempre dentro una regione dichiarata | **solido in sda, limite in att** | sda 60/60 e 200/200; att F1 39/60 [0,52; 0,76] | rivisita 10 Hz (sda) e inviluppo 210 m/s nel nucleo (v3i) |
| Confidenza C(τ) dichiarata contro osservata | **incoraggiante nelle fasce alte, limite nelle medie** | C 0,95–0,99: osservata 0,93–0,97; C 0,6–0,8: osservata 0,38–0,48 | σ_rif e q tarati sulla metà di taratura (§ 5.3); IMM con P monotona in perdita |
| Zona «al 99 %» dalla sola covarianza | **limite** (smentita) | 0,003–0,91 | non mostrarla come 99 %; mostrare l'insieme di presenza (garantito con \|a\| ≤ a_max) |
| Collisione di droni in volo dichiarata come evento | **limite** | 0/60 [0; 0,060] in att e sda | regola di contatto con impulso su tracce risolte e Doppler (§ 5.2); radar più vicino ai frammenti |
| Identità dopo 2–4 s di solo radar | **limite** | scambio 0,47–0,63 | identità «presunta» (già nel nucleo); attributi (Doppler, RCS, termico) per la riassociazione |
| Latenze sda | **ipotesi** (stima per analogia) | 1,2 ms di elaborazione dedicata contro 80 ms CPU | misura su FPGA o ASIC reale |

## 4. Registri per il video

`prototipo/uscite/video_volo/registro_F1…F6.jsonl` (passaggio idx 0, configurazione sda, regole v3i: seme dichiarato
prima), un fotogramma ogni 0,1 s con i campi nuovi: `tracce[].confidenza_C`, `porta_m`, `r99_m`,
`insieme_presenza_r_m`, `non_vista_da_s`, `parola`; `evento` (tipo, V(τ), impronta, campioni ispezionati);
`affidabilita_sensori`; `verita` (solo per il montaggio); `avviso_prossimita`. Indice dei momenti: `INDICE.md` nella
stessa cartella. Validatore nuovo, accanto a `movi.sh convalida` (che non è cambiato): `prototipo/prove/convalida_volo.py`.
Convalida (`esito_convalida.txt`): F1, F4, F6 senza violazioni; **F2 34, F3 16, F5 26 violazioni della regola «C non
cresce durante la perdita»**, tutte piccole (C da 0,994 a 0,999 per esempio). Causa probabile (non verificata): nel
mescolamento IMM del nucleo la covarianza predetta non cresce in modo monotono. È un **limite** reale del registro, non
un difetto del validatore: va corretto nel nucleo (C calcolata sulla miscela con pesi fissati durante la perdita) prima
di mostrare la curva. L'indice raggruppa le perdite per traccia in modo grossolano (una traccia può essere vista e
persa più volte nello stesso intervallo). **F3 nel registro non ha l'evento** (coerente con 0/60): per il video F3 mostra
l'avviso di prossimità a 0,4 s (urto previsto fra 15,8 s), la caduta e la regione che cresce, non un «evento».

## 5. Che cosa propongo dopo

1. **Adottare v3i** (inviluppo 210 m/s anche nel nucleo) come correzione nella versione v4 del nucleo, accanto alla v3.
2. **Evento di contatto in volo senza ritorni di frammenti.** Meccanismo: contatto fra due tracce *risolte e non
   doppioni* (velocità relativa > 10 m/s per ≥ 3 aggiornamenti prima del contatto) + cambio di velocità sostenuto
   (≥ 3 aggiornamenti) misurato col Doppler. Previsione: F3 entro 2 s ≥ 0,85 con F6 0/200. Smentita: un falso evento
   in F6 o F3 < 0,75. La v4 qui provata è il controesempio di ciò che non basta (conta i doppioni come coppie).
3. **Taratura della covarianza per la confidenza**: σ² + σ_rif² e fattore su q stimati sulla metà di taratura (come
   proposto in 03-confidenza). Previsione: scarto medio |C − osservata| < 0,05 nelle fasce medie. Smentita: > 0,10.
4. **Radar più vicino o a portata maggiore sui frammenti** (RCS 2·10⁻⁴ m²): oggi l'impronta resta di 5–7 km.
