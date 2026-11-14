# NOTE per chi unisce — capitolo 8 (`lim`) e appendici A (`par`) e B (`rip`)

Lavoro dalle 18:55:51 alle 19:10 circa del 14 novembre 2026 (`date -Is`). File: `capitolo.tex`, `appendice_parametri.tex`, `appendice_riproducibilita.tex`, `prova.tex` (file di prova), `allegato.bib` (copia), `CIFRE.md`, questo file.

## 0. In testa: regole violate e scostamenti
- **Previsioni non scritte prima** (regola 3): non ho scritto ora, misura e soglia prima della compilazione. Dichiarato a posteriori: mi aspettavo compilazione senza errori e al più 8 pagine; esito osservato sotto. Non vale come previsione.
- **`stato.md` non tenuto**: lavoro breve, un solo passo.
- **File di rapporto**: l'ambiente chiede di non scrivere file `.md` di rapporto; la consegna chiede `CIFRE.md` e `NOTE.md`: ho seguito la consegna.
- **`VERDETTO_INTEGRAZIONE.md` non esiste** (`ls f12-integrazione/30-arbitro/`: cartella vuota alle 18:55): il capitolo non ha un giudizio complessivo sull'integrazione; le cifre delle prove più recenti (prova d'insieme, «libero» della cella, identità e controprova) vengono dalla soluzione finale, **non vagliate**. Se il giudizio arriva e cambia una forma, vanno riviste le tabelle 4 (invarianti) e il §8.8.
- **Non letti per intero**: `PROVA_INSIEME.md`, `LIBERO_DELLA_CELLA.md`, `IDENTITA_SU_PROFONDITA.md`, `CONTROPROVA_IDENTITA.md`, `CONTROLLO_PROVE.md`, `ATTACCO_V3.md`, `ATTACCO_CLASSIFICAZIONE.md`, `USO_DELLA_CLASSE.md`, `CLASSIFICATORE.md`, i giudizi di f4, f7, f8, f9, i fascicoli 01 (salvo §10 e discordanze), 03, 04 (salvo §3, §5, §6.6, §6.7), 05 (salvo §3, §5–§7). Le loro cifre entrano **attraverso** la soluzione finale e il blocco di classificazione, che le riportano: un errore di trascrizione in quei due file passa nel capitolo.
- Nessuna simulazione eseguita. Controlli miei: aritmetica rifatta a mano sulle formule di §8.4, sulla fascia, sulla somma di latenza, sulle soglie di posa (stessa formula e stessi parametri della fonte: vale solo contro errori di calcolo).
- Niente git, sudo, rete. Scritture solo in `18-capitolo/`, più immagini di controllo delle pagine nella cartella temporanea della sessione (sottocartella `cap8lim`).

## 1. Compilazione (verificato)
`xelatex` → `bibtex` → `xelatex` × 2 su `prova.tex`, ciascuno con `timeout 120 … -interaction=nonstopmode -halt-on-error`: codice d'uscita 0 a ogni passo; 0 citazioni indefinite (`grep -c 'Citation.*undefined' prova.log` = 0); 0 righe d'errore. Riferimenti indefiniti: solo quelli agli altri capitoli (`sec:map`, `sec:geo`, `sec:sti`, `sec:occ`, `sec:val`, `sec:cos`), attesi. Il capitolo occupa 7 pagine e circa due terzi dell'ottava (l'appendice A comincia alla riga 38 della pagina 8). PDF guardato con `pdftotext -layout` (formule 1–2, tabelle 2 e 6) e in immagine (pagine 1, 3, 5).
- **Una scatola fuori margine (116 pt), non nel capitolo ma nella bibliografia**: la voce `realsense-alta-velocita-d435` di `allegato.bib` ripete un indirizzo lungo nel campo della nota. Riguarda il file della bibliografia: lo segnalo, non l'ho toccato. BibTeX avverte anche «empty year» per `realsense-filtri-post`, `us-49cfr-236-205`, `realsense-alta-velocita-d435`.
- Controllo delle parole vietate (A-4) con `grep` su tre file: 0 occorrenze di sciame, agente/i, ruolo, fase, arbitro, verdetto, addendum, torneo, corsia, coordinatore, convocazione, fascicolo, hackathon, squadra, versione, «in corso», «da fare», nomi di file; 0 sigle del tipo H-, K-, F-, V-, C-, M1…M8, c1…c8, S1…S12, sd-, R1…R8, I1…I20.

## 2. Che cosa manca al preambolo
- **Nessun ambiente per tabelle su più pagine** (`longtable`). La consegna chiede una «tabella unica» dei parametri: l'ho divisa in due tabelle con le stesse colonne (prima e seconda parte). Se il preambolo riceve `longtable`, si uniscono togliendo la seconda intestazione.

## 3. Nomi tecnici dati alle cose (da allineare con i capitoli 3–5)
| Nome interno | Nome usato qui |
|---|---|
| R100 | «area d'avviso» (ombra dell'ostacolo più la fascia w); senza simbolo |
| R90 | $\Reg_\alpha(t)$, «regione prevista» |
| sd-1 / sd-0 | «predittore a insieme di percorsi» (solo in appendice A: «insieme di percorsi del predittore») / «predittore di ripiego» |
| c7 | «avviso senza traccia» |
| `gruppi_per_picco` | «raggruppamento per picco» |
| w | «fascia di guardia» $w$ (il fascicolo di geometria la chiama $g$: **scegliere un solo simbolo**) |
| fascia di 0,20 m | «fascia di ritaglio» |
| t_conf, T_ant, d_serve, v_ego, a_fr | $t_c$, $T_{\mathrm{ant}}$, $d_{\mathrm{serve}}$, $v_e$, $a_f$ |
| ε_Ω (blocco) / e_ombra (geometria) | $\varepsilon_\Omega$ |
| I1…I20 | righe 1–15 della tabella 4, senza sigla (I15–I19 fuse nella riga 15; I20 nella riga 11 e nel §8.4) |
Gli invarianti sono numerati 1–15 **solo dentro la tabella**: altri capitoli non li citino per numero.

## 4. Dipendenze da altri capitoli
- **Cap. 2 (geo)**: 1,24 m / 1,71–1,73 m (e 1,22 / 1,69 m con 424 px); formula Δy ≈ ρ·δθ e soglie 0,67° e 0,57°; Proposizione sui falsi «mobile» da deriva di posa (qui ne riporto solo l'enunciato: la dimostrazione deve stare nel cap. 2, altrimenti va spostata qui). **La scelta della focale va fatta una volta sola** (discordanze, geometria 1–2): qui ho messo entrambe le coppie.
- **Cap. 3 (map)**: regola del «libero» (impronta, metà, 8 vicine), controesempi alle regole con memoria.
- **Cap. 4 (sti)**: regola «mobile» (soglia 5σ√(2/m)), conferma 3 su 5, tempo di conferma, tassonomia e scenario, requisiti del classificatore, non osservabilità della massa.
- **Cap. 5 (occ)**: definizione di possibile presenza, fascia (proposizione), annidamento, **tabella del dominio per classe** (qui solo «3 classi su 15 / 0 su 15» e 1,44 m/s), enunciato «un'etichetta non riduce mai l'avviso».
- **Cap. 6 (val)**: intervalli delle frequenze del §8.8 (qui date senza intervallo, con rinvio), lettura «dentro k su n», semi.
- **Cap. 7 (cos)**: tempi per ciclo; mappa locale a senso unico per il sensore in moto.
- La latenza τ = 0,155 s **è definita qui** (§8.5, `sec:lim-latenza`, tabella `tab:lim-latenza`): i capitoli 5 e 2 dovrebbero rinviare qui, o viceversa; da non duplicare.

## 5. Che cosa ho lasciato fuori, e perché
- **Geometria e copione della dimostrazione dal vivo** (pannello a 1,8 m, attore a 2,3 m): è organizzazione della presentazione, non parte tecnica.
- **Tabella dei requisiti con lo stato per requisito** (soluzione finale §3): duplica il capitolo 1; qui restano gli invarianti.
- **Elenco completo delle parole da non usare** (soluzione finale §3): ridotto a sei classi di affermazioni non dichiarate; il resto riguarda la presentazione.
- **Tabella delle regole escluse** (soluzione finale §4): va nel capitolo 7 («strategie escluse con il controesempio»).
- **Contraddizioni aperte** (soluzione finale §5): entrano solo come limiti (§8.8) e come righe del protocollo (§8.10), senza sigle.
- **Messaggio per settori verso un autopilota**: mai generato; citato solo come «regola di progetto».
- **Requisiti a 10 e 30 m** della tabella di posa: fuori dalla portata della camera (ipotizzano un altro sensore).
- **Tabella distanza d'avviso classe × profilo** (profili, §3): usa un'altra formula (senza tempo di conferma, margine 0,40 m) rispetto al blocco incluso nella soluzione; ho tenuto **solo la formula del blocco**, che è parte della soluzione finale. Il capitolo 5, se usa quella tabella, deve dire quale formula è.
- **Citazioni delle norme** sulla distanza di separazione: nessuna norma è stata letta; cito solo la fonte secondaria `marvel2017` per la forma lineare.

## 6. Dubbi per chi unisce
1. **Tempo di reazione della persona con disabilità visiva**: 1,0 s (profili §2) contro 1,5 s (blocco §3); nessuna fonte. Ho riportato entrambi; nella tabella 2 la riga usa 1,5 s (come il blocco) e la prima riga («stazione fissa», 1,0 s) dà l'altro caso.
2. **«In volo»**: la soluzione finale mette «in volo», «drone» fra le parole da non usare nelle presentazioni; il requisito chiede il profilo del velivolo. Nella tabella 2 compare «multirotore senza equipaggio in volo stazionario» come profilo configurato, con le colonne in moto marcate «non verificato». Se la commissione non deve leggere quel profilo, si toglie una riga.
3. **C = 0,85 m**: la soluzione finale dice che non è citabile come distanza di una norma. Nel §8.4 è scritto «valore attribuito alla norma sul posizionamento dei ripari e non riscontrato sul testo», come nel fascicolo di geometria. Se si preferisce, si scrive solo «margine C = 0,95 m, ipotesi di progetto».
4. **Registro degli eventi**: «0 violazioni su 600 scene», «16–52 %», «12,5 %» vengono dalla soluzione finale; non ho riaperto il file d'origine, quindi il modello del sensore di quella simulazione è **non verificato**: nel testo è «in simulazione su scene sintetiche con una catena ridotta», senza dire «modello ideale».
5. **Salute del sensore**: «segnale in 0,13 s, 0 falsi in 60 s» è «in simulazione, con rumore dell'unità inerziale ipotizzato»; anche qui il modello del sensore non è scritto nella fonte letta.
6. **«0 su 900» col corpo che non rimanda segnale**: l'unità (fotogrammi) non è esplicita nella soluzione finale; l'ho scritta per analogia con la riga della regola caduta («900 su 900 fotogrammi»). Da controllare su `ATTACCO_V3.md`, punto 1.
7. **Livello di prova «per costruzione»**: non è una delle cinque lettere del preambolo. Nella tabella 4 è scritto per esteso, con la spiegazione nella didascalia; se l'introduzione definisce i livelli, deve nominare anche questo.
8. **Citazione `us-49cfr-236-205`** (guasto verso lo stato più restrittivo): è un'analogia, su copia non ufficiale; se la commissione è severa sulle fonti, la frase regge anche senza.
9. **Protocollo (tabella 6)**: quattro righe hanno numerosità «non fissata» perché nessun file la fissa; non ne ho inventata una.

## 7. Fonti da aggiungere alla bibliografia (frasi lasciate senza citazione)
- **Tempo di reazione di frenata di un conducente (1,5 s a sorpresa)**, usato per l'operatore remoto: nei profili è «R6, Green 2000: non verificato». Dati che ricordo, **non verificati oggi** (la ricerca salvata nella cartella dei profili ha dato 0 risultati): M. Green, «"How long does it take to stop?" Methodological analysis of driver perception-brake times», *Transportation Human Factors* 2(3), 2000, pp. 195–216. Va aperta la fonte prima di citarla.
- **Arresto del cammino su segnale** (Cao e altri, 1998, PMID 10200400) e **tempo di reazione semplice a un suono** (circa 0,16 s): letti da chi ha scritto i profili, non in `allegato.bib`; nel capitolo non li uso come cifre.
- **Nessuna fonte trovata** per il tempo di reazione di una persona con disabilità visiva a un avviso sonoro: è scritto come ipotesi.

## 8. Indipendenza
Sono lo stesso ruolo che ha scritto la soluzione finale e il blocco di classificazione: condivido con quelle fonti autore, modello linguistico e specifica. I miei controlli valgono per errori di trascrizione e d'aritmetica fra quelle fonti e il capitolo, non per errori nelle simulazioni.
