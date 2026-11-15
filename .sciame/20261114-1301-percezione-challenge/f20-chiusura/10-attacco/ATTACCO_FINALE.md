# Attacco finale e riconto: regola di contatto v4c, E1 rifatto, taratura della confidenza (`sciame-avversario`)

15-11-2026, ripresa dalle 06:10:34 (`date -Is`); un'istanza precedente dello stesso ruolo aveva lavorato in questa cartella dalle 05:59
(previsioni P-A1..P-A7 in `PREVISIONI.md`, 05:59:34). Previsioni aggiuntive P-A8, P-A9 in `PREVISIONI_2.md` (06:12:28).
**Tutto è simulato dalle schede o su traiettorie pubbliche con un sensore simulato**: nessun sensore fisico, nessuna prova su hardware.
Wilson al 95 % per passaggio (per la taratura: per caso, ottimista perché i casi sono correlati dentro un mezzo).

## 0. In testa

**Cambi di stato proposti all'arbitro.**
- C-1 (v4c, sda, F3 entro 2 s): **regge con condizione** nella geometria nominale e in 4 varianti su 5; resta **L** per i falsi
  eventi di F5 (confermati) e per gli eventi prima dell'urto, che nelle varianti salgono fino a 2/20.
- C-2 (v4c, att): **smentita** confermata, e peggio fuori dalla geometria nominale (fino a 9/20).
- «F1, F5 senza falsi eventi»: **smentita** (F1/att 1/60, F5 2/60 in tutte e due le configurazioni). «F6 senza falsi»: **regge**, anche
  in 3 varianti. «F4 non peggiora»: **regge**.
- E1 rifatto (K-709): **regge** il riconto (48/60 e 3 precoci); una nota di conteggio sul «60/60 entro 2,5 s» (§ 3).
- Taratura: **regge con condizione**. Nessuna fuga fra le metà; ma il 90 % dei casi di prova aerei viene da 4 numeri di volo di
  una sola rotta (LHR–ZRH): sugli altri 12 mezzi la fascia 21–30 s scende a 0,81 [0,75; 0,86]. La frase «16 aerei» va corretta.

**Regole.** Ho scritto solo in questa cartella; niente rm, niente sovrascritture (i file dell'istanza precedente sono intatti; i
riconti nuovi hanno nomi nuovi: `conteggi_geometria_finale.txt`, `geometria_2.jsonl`, `riconto_e1.txt`, `riconta_e1.py`). Niente git,
sudo, rete. La corsa `geometria.py` usa un Pool da 6 più il principale (7 processi, con `timeout`). **Violazione da dichiarare:**
la prima corsa delle geometrie (06:01) si era fermata a metà senza dichiararlo; la previsione P-A9 non è cieca (il calcolo della
concentrazione era già stato fatto alle 06:02).

**Indipendenza.** Condivido con ciò che controllo il simulatore, il tracciatore, il nucleo v4 congelato (importato, non modificato),
le definizioni di evento, di falso evento e di copertura, i json della taratura e il modello linguistico. Il codice dei conteggi,
delle varianti di geometria e dei controlli di fuga è mio. Il controllo vale per gli errori di conteggio, di divisione e di geometria
nominale, non per i difetti del simulatore.

## 1. Attacchi alla regola v4c (CONTATTO.md)

| # | Attacco | Previsione (scritta prima) | Comando / file | Esito |
|---|---|---|---|---|
| 1 | Semi nuovi | P-A1 regge | `riconta.py` su `valutazione_v4c.jsonl`; idx dei jsonl di sviluppo e di `f19-volo/10-prove/passaggi_volo_v3i.jsonl` | **regge**: valutazione 1000–1059 (F6 1000–1199), 60 idx unici per cella; sviluppo 0–19; v3i 0–199. Intersezione vuota |
| 2 | La regola legge il vero? | P-A2 regge | lettura di `regola_v4c`, `_dop_di`, `_risoluzione` in `prove_volo_v4_congelato.py` | **regge con condizione**: usa tracce, covarianze e `D["doppler"]` (t, z, v_r, los: niente identità dell'oggetto). Due condizioni: `ing_max` è l'ingombro massimo degli oggetti **della scena** (non frammenti), cioè un'informazione di classe presa dall'elenco vero; e la v_r simulata dei ritorni uniti è quella di un oggetto vero (modello del sensore, non fuga) |
| 3 | Il ritardo è misurato dall'istante retrodatato? | (non previsto) | `eventi_v3.py:483` | **regge**: ritardo = t_b (dichiarazione) − t_urto, non t_a = min(t_c, tk). Il «entro 2 s» non è gonfiato dalla retrodatazione |
| 4 | Riconto delle 10 celle | P-A3 regge | `riconta.py` → `riconto_v4c.json` | **regge**: tutte le celle identiche a `risultati_v4c.json` |
| 5 | F1, F5, F6 senza falsi eventi; F4 non peggiora | — | idem | F6 0/200 [0; 0,019] att e sda: **regge**. F1/att **1/60 [0,003; 0,089]**, F5 **2/60 [0,009; 0,114]** att e sda: **smentita**. F4 60/60 [0,940; 1]: **regge** |
| 6 | Geometrie variate di F3 (idx 5000–5019, semi nuovi) | P-A4: almeno una variante sotto 0,85 | `geometria.py`, `conteggi_geometria_finale.txt`, `geometria_2.jsonl` | **la mia previsione regge** (cioè la regola **non** regge ovunque): tabella sotto |
| 7 | Geometrie variate di F6 | P-A8: ≥ 1 falso in F6-vicino | `geometria_2.jsonl` | **la mia previsione è smentita**: 0/20 in tutte e 3 le varianti, att e sda |

**F3 fuori dalla geometria nominale** (n = 20 per cella, Wilson; «prima» = evento dichiarato prima dell'urto, da contare come falso
allarme):

| Variante | att entro 2 s | att prima | sda entro 2 s | sda prima | sda mai |
|---|---|---|---|---|---|
| nominale (CONTATTO, n 60) | 34/60 [0,441; 0,684] | 1/60 | 57/60 [0,863; 0,983] | 1/60 | 0/60 |
| incrocio a 30° | **10/20 [0,299; 0,701]** | **4/20 [0,081; 0,416]** | 19/20 [0,764; 0,991] | 1/20 | 0/20 |
| incrocio a 150° | 16/20 [0,584; 0,919] | 0/20 | 17/20 [0,640; 0,948] | **2/20 [0,028; 0,301]** | 1/20 |
| quota 40 m | 14/20 [0,481; 0,855] | 0/20 | 19/20 [0,764; 0,991] | 0/20 | 1/20 |
| quota 400 m | **9/20 [0,258; 0,658]** | 0/20 | **16/20 [0,584; 0,919]** | 0/20 | 0/20 |
| sensori a ~570 m dall'urto | 17/20 [0,640; 0,948] (rifatta: identica) | 0/20 | **parziale** 7/7 [0,646; 1] alle 06:24 | 0/7 | 0/7 |

Note. Le varianti di distanza spostano **tutti** i sensori (`geometria.py`), non solo il radar. In ogni variante «libero» sul punto
vero: 0/20 [0; 0,161]. Con 20 passaggi il limite inferiore di Wilson non arriva mai a 0,85 anche con 20/20 (0,839): le varianti
servono a cercare il caso che rompe, non a sostenere la cifra. Il caso che rompe c'è: **sda a quota 400 m, 16/20**, e **eventi prima
dell'urto fino a 2/20 in sda e 4/20 in att**.

**F6 fuori dalla geometria nominale** (incrocio portato dentro la finestra; tutte 0/20 [0; 0,161], att e sda, «libero» sul vero 0):
F6-vicino (500 m in pianta, 150 m di quota; distanza minima vera mediana 354 m), F6-ang45 (1267 m), F6-radar6km (1006 m). **Limite
dell'attacco:** nessuna variante F6 scende sotto i 300 m, quindi non tocca il punto debole, che è il quasi incrocio a 39 m di F5.

## 2. Frase che l'esito di v4c permette alla giuria

«In simulazione, una regola di contatto ancora in prova ha dichiarato la collisione di due droni veloci entro 2 s in 57 passaggi su 60
col radar a scansione elettronica [0,86; 0,98], e fra 16 e 19 su 20 cambiando angolo d'incrocio e quota; dà ancora falsi eventi in un
quasi incrocio a 39 m (2 su 60) e a volte dichiara prima dell'urto. Non è adottata: la collisione veloce resta un limite dichiarato.»
Col radar rotante a 1 Hz: «non basta (34 su 60, e 9 su 20 a quota 400 m)». Restano vietate «MoVi rileva la collisione in volo» ed
«entro 2 s» senza «in N su 60, simulato».

## 3. E1 rifatto (K-709)

Riconto mio (`riconta_e1.py` → `riconto_e1.txt`, dai sei `e1_stabile_0*.jsonl`): n 60, idx unici 60.
- 0 ≤ ritardo ≤ 2 s: **48/60 [0,682; 0,882]** — regge.
- prima dell'urto: **3/60 [0,017; 0,137]**, ritardi −11,5, −11,0, −11,0 s, tutti di tipo «separazione» — regge.
- mai: 0/60 [0; 0,060]; tutti i frammenti dentro V: **60/60 [0,940; 1]** — regge.
- **Nota di conteggio:** «entro 2,5 s: 60/60, di cui 3 negativi» in CONTATTO § 5 vale solo contando i negativi; contando
  0 ≤ ritardo ≤ 2,5 s è **57/60 [0,863; 0,983]**. Da scrivere così.
- Condizione già dichiarata da CONTATTO e confermata nella lettura: il rifacimento cambia anche l'estrazione del rumore delle camere,
  quindi **non isola l'integratore**. V-13 da I a L: d'accordo.

Frase ammessa: «Con l'integratore stabile, nella simulazione E1 l'evento è dichiarato entro 2 s dall'urto in 48 passaggi su 60
[0,68; 0,88], con 3 eventi aperti prima dell'urto; i frammenti restano nel volume dichiarato in 60 su 60.»

## 4. Attacchi alla taratura (TARATURA.md)

| # | Attacco | Previsione | Comando / file | Esito |
|---|---|---|---|---|
| 1 | Fuga di mezzi fra le metà | P-A5 regge | `riconta_taratura.py` → `riconto_taratura.txt` (usa `prove_v5.dividi`, seme 20261115) | **regge**: intersezione vuota per aerei (15/16), ala fissa (15/16), multirotori (98/98); nessuna scena di prova fuori dalla metà di prova |
| 2 | La scelta di σ_rif, q e a* usa la prova? | (lettura) | `prove_v5.py` righe 150–185 | **regge**: griglia e a* (quantile 0,9 del PIT, per fascia e regime) calcolati solo su `casi_tar`; la prova gira con la tabella già fissata |
| 3 | Riconto della copertura per fascia (aerei, dopo + isotonica) | P-A6 entro 0,01 | idem | **regge**, identico: 1–2 s 655/733 = 0,894 [0,869; 0,914]; 3–5 372/416 = 0,894; 6–10 344/385 = 0,894; 11–20 334/374 = 0,893; 21–30 328/388 = **0,845 [0,806; 0,878]**; virata 161/221 = 0,729 [0,666; 0,783]; accelerazione 81/107 = 0,757 [0,668; 0,828] |
| 4 | Concentrazione per mezzo | P-A9 (non cieca) | `concentrazione.py` → `concentrazione.txt` | **regge con condizione (forte)**: 4 chiavi «nvolo» (SWR81C, SWR9FV, SWR7GP, SWR4YZ: numeri di volo di una sola rotta, LHR–ZRH, più giorni) fanno 2055/2296 = **89,5 %** dei casi di prova aerei; i 12 aerei ADS-B fanno 241 casi. La metà di taratura contiene altri 3 numeri di volo della **stessa rotta**: non è fuga di mezzo, ma è correlazione di rotta fra le metà |
| 5 | Copertura senza i voli dominanti | — | idem | sugli «altri 14 mezzi» (tutti tranne i 2 più pesanti): 1–2 s 0,914 [0,880; 0,939]; 21–30 s **0,807 [0,748; 0,855]**. Un mezzo, icao:a4077d, ha 10/16 = 0,625 [0,386; 0,815] |

Due osservazioni in più.
- La «banda 0,85–0,89 in ogni fascia» della frase per la giuria in TARATURA § 6 è **inesatta**: la fascia 21–30 s è 0,845, e il Wilson
  va da 0,81; col bootstrap per mezzo {0,784; 0,886}.
- «16 aerei» non è vero: 12 aerei (icao) e 4 **numeri di volo**, che su più giorni possono essere aerei diversi.

Frase ammessa: «Dopo la perdita, nella simulazione su traiettorie pubbliche, la regione al 90 % ha contenuto l'aereo reale fra 85 e 89
volte su 100 nelle fasce da 1 a 20 s e 85 su 100 fra 21 e 30 s [0,81; 0,88]; i casi vengono per nove decimi da quattro voli della
stessa rotta, e in virata la copertura scende a 73 su 100 [0,67; 0,78]: è un limite dichiarato.» Niente «tarata» senza condizione.

## 5. Stati proposti

| Enunciato | Stato | Esito dell'attacco |
|---|---|---|
| C-1 v4c sda F3 entro 2 s | simulato; L | regge con condizione (nominale e 4 varianti su 5 ≥ 16/20; prima dell'urto fino a 2/20) |
| C-2 v4c att | simulato; L | smentita (34/60; 9/20 a quota 400 m) |
| C-3 F6 senza falsi | simulato | regge (0/200 nominale; 0/20 in 3 varianti, nessuna sotto 300 m) |
| C-F1F5 senza falsi | simulato | smentita (F1/att 1/60; F5 2/60) |
| C-4 F4 invariato | simulato | regge (60/60) |
| E1 stabile | simulato; V-13 → L | regge; «60/60 entro 2,5 s» da riscrivere come 57/60 + 3 precoci |
| kalman-6/7 (1–2 s 0,89; scarto 0,016) | su dati pubblici, sensore simulato; I | regge con condizione: 89,5 % dei casi da 4 voli di una rotta |
| kalman-8 (virata 0,73) | su dati pubblici; L | regge |
| frase TARATURA § 6 | — | smentita nella forma («in ogni fascia 85–89», «16 aerei»): sostituire con la frase del § 4 |

## 6. Che cosa manca e che cosa propongo dopo

**Mancante:** F3 con i sensori a ~570 m in sda è a 7 passaggi su 20 alla consegna (06:25; la corsa si ferma con la consegna;
`geometria_2.jsonl` tiene le righe scritte; il resto si ottiene rilanciando `geometria.py` su F3-radar600 e contando con
`conta_geometria.py`). La riesecuzione di F3-radar600/att sugli stessi
semi ha dato lo stesso 17/20: il simulatore è riproducibile; varianti F6 a meno di 100 m (il vero bordo, quello di F5) non provate; nessuna variante con più di
20 passaggi; nessun controllo della taratura con divisione diversa (TARATURA § 6 punto 3, non fatto da nessuno).
1. **F6/F5 a distanza minima 40–150 m**, 60 semi nuovi per variante. Previsione: falsi ≥ 1/60 sotto 80 m. Smentita: 0/60 a 40 m.
2. **Taratura con divisione per rotta** (tutti gli LHR–ZRH da una parte). Previsione: la copertura sui 12 aerei ADS-B scende sotto
   0,85 in almeno una fascia. Smentita: tutte le fasce ≥ 0,85 col Wilson sopra 0,75.
3. **Nel video** (limite dell'utente: al più 176 s in totale) le due frasi del § 2 e del § 4 vanno nelle etichette esistenti, non in
   scene nuove.
