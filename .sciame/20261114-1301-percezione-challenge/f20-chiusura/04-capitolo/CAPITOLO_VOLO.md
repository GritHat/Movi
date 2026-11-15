# Capitolo sul volo ad alta velocità e «da proposta a sistema attuato» (f20-chiusura/04-capitolo, `sciame-formalista`)

15-11-2026, dalle 05:37 alle 05:47 circa (`date -Is`). Bozza in LaTeX per la commissione esterna.

## 0. In testa: cambi di stato e regole

**Regole.** Non ho cancellato né sovrascritto file. Non ho usato git né sudo né la rete. Ho scritto solo in questa
cartella e non ho toccato `allegato_tecnico/`.

**Cambi di stato trovati scrivendo le dimostrazioni.**
1. **t_C: la semplificazione «t_C = 0 se σ0 ≥ r/k_α» è vera solo con σ0v ≥ 0.**
   - Se σ0v < 0, l'insieme {C ≥ α} può essere un intervallo [t−, t+] che non parte da 0.
   - Prova: `conti/unicita_v2.py` → `unicita_v2.json`, su 40 000 casi. Con f(0) < 0 c'è sempre una e una sola
     radice positiva (26 870/26 870), come dice la dimostrazione per convessità. Con f(0) ≥ 0 ci sono 0 radici in
     11 169 casi e 2 radici in 1961 casi, tutti con σ0v < 0.
   - Il primo script, `esempio_confidenza.py`, mescolava i due casi: le sue 13 130 «violazioni» sono questo stesso
     fenomeno, non un errore della dimostrazione.
   - Stato: dimostrato (prop. 10.x (iii)) e calcolato.
2. **Contenimento r(τ) = r0 + v_max·τ.**
   - Basta |v| ≤ v_max: |a| ≤ a_max serve solo alla forma più stretta della proposizione 9.x.
   - Ipotesi tacita ora dichiarata: |p(0) − p̂0| ≤ r0 vale solo in probabilità. La «garanzia» è quindi condizionata
     a questo evento.
3. **Monotonia della C della miscela.** Non è dimostrabile in generale: lo spostamento dei pesi può farla crescere,
   e questa è una causa possibile, non verificata, delle 76 violazioni.
   - Correzione dimostrata in una riga: C̃(τ) = min_{s≤τ} C(s), che non cresce e non supera C.
   - Non corregge la taratura.

## 1. Che cosa ho scritto

| File | Contenuto | Pagine (documento completo di prova) |
|---|---|---|
| `11_volo_alta_velocita.tex` | sezione 10 nel documento completo (§ 11 secondo la numerazione dei file) | pp. 71–81, circa 10,5 |
| `12_da_proposta_a_sistema.tex` | sezione 11 | pp. 81–83, circa 2,5 |

**Contenuto di `11_volo_alta_velocita.tex`:**
- riquadro sulla natura delle prove;
- scenari F1–F6 in tabella, con le configurazioni A e B e l'avvertenza che sensore e calcolo cambiano insieme;
- l'integratore di Eulero instabile, come limite del simulatore;
- l'inviluppo a 210 m/s nel nucleo come miglioria trovata, con le cifre prima e dopo;
- il volume dei detriti e l'avaria non contenuta come caso non provato;
- la tavola dei risultati V-1…V-13 con classi, intervalli e stati;
- la regola «impulso» come Controesempio, con il meccanismo dei doppioni;
- la perdita di confidenza, con proposizioni dimostrate:
  - σ²(τ) dalla Φ e dalla Q;
  - convessità;
  - C per il disco e per la sfera, con k_α;
  - r_α(τ);
  - t_C, con esistenza e unicità per convessità;
  - caso anisotropo come chi quadro generalizzato, con la quadratura;
  - miscela IMM;
  - contenimento fuori modello;
  - un esempio calcolato da me;
  - verifica numerica;
  - tabella ADS-B con i tre limiti;
- sensori, bilancio della latenza, analogia con gli acceleratori per modelli linguistici (dove vale e dove no), le
  correzioni 3312 m, 1058 m, 0,08–1,2 ms e la rivisita come leva vera;
- il rullaggio e gli altri usi in breve;
- le condizioni di validità.

**Contenuto di `12_da_proposta_a_sistema.tex`:**
- la frase sui risultati ottenuti in un giorno;
- la tabella del § 4 del verdetto per intero (12 righe);
- il piano a quattro tappe: simulazione estesa, banco con registrazioni, sensore su banco, campo;
- che cosa resta fuori.

**Marcatori, ciascuno con il testo per gli esiti possibili:**
- `%% MIGLIORIA-F3`: nel capitolo 11 dopo la tavola, e nel capitolo 12 dopo la tabella;
- `%% MIGLIORIA-TARATURA`: nel capitolo 11 dopo la verifica ADS-B, e nel capitolo 12;
- `%% MIGLIORIA-E1`: aggiunto da me per il rifacimento di E1 con l'integratore stabile.

**Compilazione.**
- `prova/` contiene i soli capitoli nuovi: 13 pagine con la bibliografia, nessun errore e 2 overfull sotto i 6 pt.
- `prova_completa/` contiene tutto l'allegato più i due capitoli: 97 pagine, tutti i rimandi risolti, nessun errore.
- Restano indefinite solo le citazioni `DA_VERIFICARE`.
- Ho guardato le pagine 73–82 come immagini, in `prova_completa/pagine/`.

## 2. Citazioni

**Chiavi esistenti:** wilson1927, barshalom2001, cfr-91-227, cfr-89-310, livox-tele15, faa-ac-90-48d.
- Quest'ultima è in `riferimenti.bib` ma non in `allegato.bib`, e nella prova l'ho aggiunta da lì.
- La sua nota contiene diciture interne («[353] Stato di verifica… Seconda fase»): va ripulita prima della versione
  finale.

**Nuove, `\citep{DA_VERIFICARE:…}`:**
- echodyne-echoshield;
- asr11;
- torretta-eo-mwir;
- heise-taalas-hc1;
- cerebras-blog-llama;
- cern-kalman-fpga;
- imhof1961;
- ruben1962.

Le ultime due non sono state aperte da nessuno: le cito da conoscenza.

## 3. Stati degli enunciati toccati

| Enunciato | Stato |
|---|---|
| σ²(τ), C2, C3, r_α, t_C (i–iii), miscela, contenimento | dimostrato nel modello dichiarato |
| unicità di t_C, campionata | calcolato (40 000 casi, `unicita_v2.json`) |
| esempio σ0 7,5 m, σv 2 m/s, q 4 m²/s³ (parametri di ipotesi): t_C 10,7 s (2D), 9,6 s (3D); r_0,9 17/39/91/238/427 m | calcolato (`esempio_confidenza.json`) |
| tutte le altre cifre | riprese dal verdetto, dalle prove e dall'attacco della fase 3, senza ricontarle |

## 4. Che cosa manca

- Una figura di C(τ) e di r_0,9(τ) contro r(τ), che non ho fatto per il tempo.
- Gli esiti delle prove in corso: regola di contatto, taratura, E1. I marcatori sono pronti.
- La ripulitura della voce faa-ac-90-48d.
- L'apertura delle fonti DA_VERIFICARE.
- Nella versione finale va controllata la coerenza della numerazione: il volo diventa la sezione 10, quindi prima
  delle conclusioni.
- I testi delle frasi «da non dire» li ho controllati con grep su pdftotext delle pp. 71–84: nessuna occorrenza di
  «validat», «sotto il millisecondo», «in tempo reale», «certificab», «sempre», «bersagli».
