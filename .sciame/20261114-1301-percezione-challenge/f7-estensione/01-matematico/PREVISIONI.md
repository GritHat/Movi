# Previsioni di `sciame-matematico` (f7, corsia A) — scritte PRIMA di ogni prova

Ora di scrittura: **2026-11-14T15:13:48+01:00** (`date -Is`). A quest'ora lo script `verifica_strati.py` non esiste ancora e non è stato lanciato niente.

Modello delle prove: sezione piana (2D) di 3,2 × 4,8 m, celle da 0,1 m, sensore in (0,0), campo 87°, portata 0,4–3,0 m, 15 Hz (Δ = 1/15 s), latenza λ = 0,150 s, orizzonte di validità h = λ + Δ = 0,217 s; oggetti mobili = dischi (raggio 0,15–0,25 m) con velocità ≤ v_max; pannelli fermi; profondità = minimo sul passo angolare di 0,5°, rumore limitato ±3 cm, buchi indipendenti. I teoremi non dipendono dalla dimensione; la prova numerica è in 2D e lo dichiaro.

Regole confrontate («falso libero» = cella dichiarata libera al fotogramma t e occupata da un oggetto in un istante campionato di [t+λ, t+h]; a parte, a latenza zero, all'istante t):
- **Π** (matematico-1): Π(t) = [Π(t−Δ) dilatato di v_max·Δ] meno F(t); dichiarabile = fuori da Π(t) dilatato di v_max·h.
- **cono-1**: solo il fotogramma corrente: fuori dal complemento di F(t) dilatato di v_max·h.
- **nucleo-simile** (lettura mia della regola del nucleo): cella vista libera ora, oppure senza dato ora e vista libera in uno dei due fotogrammi precedenti; nessun margine.
- **Bayes**: log-odds con i parametri di OctoMap (colpo +0,847, passaggio −0,405, saturazione [−2; 3,5]), «libero» se p < 0,3; variante «Bayes-2»: lo stesso, ma non libero se la cella è colpita ora.

| # | Previsione | Misura | Soglia di smentita |
|---|---|---|---|
| P1 | Con le ipotesi rispettate, la regola Π dà **0** falsi liberi (teorema: la prova controlla il codice e la dimostrazione, non è un dato) e ogni cella occupata al fotogramma t sta in Π(t) | falsi liberi e celle occupate fuori da Π su tutte le corse | ≥ 1 falso libero o ≥ 1 cella occupata fuori da Π |
| P2 | **Braccio che deve fallire.** Bayes dà falsi liberi (finestra [t+λ, t+h]) in ≥ 90 % delle corse; anche a latenza zero in ≥ 90 % (inerzia: servono più colpi) | quota di corse con ≥ 1 falso libero | < 90 % delle corse: il braccio non fallisce, la prova è cieca |
| P3 | La regola nucleo-simile dà falsi liberi in finestra in ≥ 90 % delle corse; a latenza zero in ≥ 50 % (buchi su una cella appena occupata) | idem | < 90 % (finestra) o < 50 % (latenza zero) |
| P4 | **Costo.** A v_max = 2,5 m/s la regola Π dichiara libero fra il **10 % e il 30 %** delle celle viste libere nel fotogramma (media, senza buchi); a v_max = 1,4 m/s fra il **25 % e il 50 %** | celle dichiarate / celle in F(t) | fuori dall'intervallo |
| P5 | **Valore della storia.** Con il 5 % di buchi la regola Π dichiara ≥ 70 % di ciò che dichiara senza buchi; la regola cono-1 (senza storia) scende sotto il 20 % del proprio valore senza buchi | rapporti fra le medie | Π < 70 % oppure cono-1 ≥ 20 % |
| P6 | **Sensore coperto** (2 s di fotogrammi tutti non validi): con Π le celle dichiarate vanno a 0 entro 0,5 s e restano a 0; con Bayes restano > 0 per tutti i 2 s | fotogrammi fino a zero; minimo delle celle dichiarate da Bayes durante la copertura | Π > 0,5 s; Bayes a zero |
| P7 | **Posa.** Errore vero ε_t = 3 cm e δ = 1°, mappa tenuta alla posa stimata: senza margine falsi liberi in ≥ 90 % di 200 scene; con il margine m = ε_t + r_max·δ = 8,2 cm (erosione di 1 cella) **0** in tutte. Con ε_t = 5 cm e δ = 2° (m = 15,5 cm): erosione di 2 celle → 0; erosione di 1 cella (insufficiente) → ≥ 1 scena su 200 con falsi liberi | scene con ≥ 1 falso libero | margine giusto con ≥ 1 falso libero; senza margine < 90 % |
| P8 | **Vetro e Bayes.** Con i parametri di OctoMap una superficie che ritorna con frequenza f < f* = 0,405/(0,405+0,847) = 0,323 converge a «libero»: per f = 0,05 e 0,20 la cella ha p < 0,5 in > 95 % dei fotogrammi dopo i primi 50; per f = 0,5 in < 5 % | quota di fotogrammi con p < 0,5 | fuori dalle soglie |
| P9 | **Filtro 3D.** Rango di osservabilità 6 con la posizione misurata sui tre assi; 4 se manca la quota (gruppo tagliato dal campo verticale). Un oggetto in caduta libera esce dal semiasse al 95 % della previsione a velocità costante (q = 0,2 m²/s³, R = (3 cm)²) dopo t* fra **0,10 e 0,30 s**; per coprire la caduta a 0,5 s servirebbe q fra 3 e 8 m²/s³ | ranghi; t*; q | fuori dagli intervalli |

Conti senza previsione (sono solo calcoli): volume del tronco di piramide visto (87° × 58°, 3 m) e numero minimo di voxel da allocare; raggio della sfera inscritta e «età utile massima» di un'osservazione di libero; numero di aggiornamenti per ribaltare una cella saturata.

Ciò che noterò dopo va in `CONSEGNA.md` sotto «notato dopo», distinto da questa tabella.

---

## Seconda tornata — previsioni scritte DOPO il primo lancio registrato e PRIMA del secondo

Ora di scrittura: **2026-11-14T15:18:55+01:00** (`date -Is`). Il primo lancio registrato (`risultati.txt`, 15:18:05–15:18:23) è già stato letto: P4 e P5 sono smentite (la regola Π dichiara lo 0,1 % e il 3,2 % delle celle viste libere, non il 10–30 % e il 25–50 %; con i buchi tiene il 13,7 %, non ≥ 70 %). Prima del lancio registrato c'è stato un lancio di prova con 2 mondi (15:16:37), di cui ho visto l'uscita: le previsioni della prima tabella erano già scritte e non le ho toccate.

Il secondo lancio (`verifica_strati.py F`, funzione `sim_F`, non ancora scritta a quest'ora) cerca la causa e la curva del costo. Non cambia nessuna previsione della prima tabella.

| # | Previsione | Soglia di smentita |
|---|---|---|
| D1 | Scena **vuota** (solo le pareti): la regola Π dichiara, sul visto libero, 5–20 % a v_max = 2,5 m/s; 20–45 % a 1,4; 45–70 % a 0,9; 65–85 % a 0,4 (margine di 6, 4, 2, 1 celle) | fuori dagli intervalli |
| D2 | Scena **dinamica** (come nel primo lancio): 15–40 % a 0,9 m/s; 40–65 % a 0,4 m/s (2,5 e 1,4 sono già visti: 0,1 % e 3,2 %) | fuori dagli intervalli |
| D3 | Scena con **soli pannelli fermi**: per ogni v_max il valore sta fra quello della scena dinamica e quello della scena vuota | ordine violato |
| D4 | Causa di P5: i buchi del primo lancio erano per passo angolare e annullavano tutte le celle lungo il raggio. Con buchi **per cella** (5 %, indipendenti, come il «suolo valido 95 %» del nucleo): a 0,9 m/s la regola Π tiene ≥ 70 % del suo valore senza buchi e cono-1 scende sotto il 40 %; a 1,4 m/s Π tiene ≥ 50 % e cono-1 scende sotto il 10 % | Π sotto soglia, o cono-1 sopra |
| D5 | In tutte le corse del secondo lancio: 0 falsi liberi della regola Π e 0 celle occupate fuori da Π | ≥ 1 |

---

## Terza tornata — braccio che deve fallire per la regola Π (scritta prima del lancio `verifica_strati.py G`)

Ora di scrittura: **2026-11-14T15:21:27+01:00** (`date -Is`). Già letti: `risultati.txt` e `risultati_dopo.txt`. La funzione `sim_G` a quest'ora non esiste.

| # | Previsione | Soglia di smentita |
|---|---|---|
| G1 | Se l'ipotesi di velocità è **violata** (oggetti fino a 2 × la v_max dichiarata, con v_max dichiarata 0,9 m/s e 0,4 m/s, 24 mondi ciascuno), la regola Π **deve** dare falsi liberi: in ≥ 50 % delle corse. Se non li dà, il controllo P1/D5 è cieco | < 50 % delle corse con falsi liberi |
| G2 | Con il fattore 1 (ipotesi rispettata, stessi semi) i falsi liberi sono 0 | ≥ 1 |
