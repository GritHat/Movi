# Attacco alla preproposta esterna — `sciame-avversario`, f9

**In testa.** Previsioni scritte alle 2026-11-14T15:44:06+01:00 (`PREVISIONI.md`), prove dalle 15:47:40 alle 15:49:38 (`date -Is`): uno script, `attacchi_f9.py`, nove parti sotto i 10 s l'una, semi fissati, una alla volta. Tutto è **conto o simulazione logica**: niente vale per il sensore vero.

- **Previsioni mie cadute (non le ritocco).** P1c: «≥ 20 % delle combinazioni senza livello» → 1,8 %. P2b: «≤ 0,02 con σ₂ = 0,20» → 0,022. P5a: «pixel 7–10 %» → 6,8 %. P6a: lettura A «≥ 90 %» → 60,4 % nella variante principale; lettura B «≥ 30 %» → 1,3–2,1 %.
- **Scostamenti.** (1) `p6x` è scritta dopo aver visto P6: esplorativa. (2) Senza previsione: pannello nero, più persone in nero, carico sinusoidale, copertura dell'etichetta «± σ». (3) Il file non specifica S3–S4 (α, σ₂, regola dei pesi): il modello è mio, con tre varianti di σ₂ e due letture dei pesi (A cumulativa, B istantanea). (4) Letti solo per `grep`: torneo (parte 3), `f1`, fonti, `f6`; non letti `MISURE_V2*.md`. (5) Rete: due ricerche; la pagina SKYbrary su ACAS non si apre: vale solo il riassunto del motore. (6) Lunghezza al limite delle tre pagine (circa 2500 parole con le tabelle).
- **Regole violate:** nessuna che io sappia.
- **Che cosa condividono i controlli con la preproposta:** il modello linguistico; il testo del file nella mia lettura; la geometria del nucleo (camera a 1,2 m, 15°, 87°×58°, 3 m, 15 Hz). Nessun codice dell'autore. Valgono per i difetti di logica e di geometria, non per quelli del sensore.

## 1. Verdetti proposti

| Strategia | Verdetto proposto | Prova (`risultati_pN.txt`) |
|---|---|---|
| **S1** selettore | **approvata con correzioni**, solo in forma ridotta (sonda all'avvio, degrado in un solo verso). Righe 2 e 6 della tabella **respinte** | cambio 3 fasce → 2D: 3,22 m² su 5,66 (57,0 %) diventano «libero» (p3); ciclo limite: 19 cambi al minuto con 3 s di permanenza, 188 in 600 s (p4) |
| **S6** massimo avvicinamento, volume protetto | massimo avvicinamento: **approvato come informazione**. Probabilità d'intrusione sulla distribuzione ritagliata: **respinta** | P = 0 esatto a ogni ciclo con il soggetto nascosto a 9 cm dal volume; 0,5–15 % con il soggetto **dentro** il volume (p2) |
| **S7** rotta convergente | **respinta** come indice a sé | è la stessa grandezza di S6: θ̇ = d_CPA·‖v‖/r², errore massimo 6·10⁻¹² su 10 000 coppie (p8); riferita al sensore e non al varco sbaglia verso |
| **S8** logica a livelli | **respinta com'è scritta; approvata nella riscrittura del §4** | attesa in 900 fotogrammi su 900 a stanza vuota; 289 combinazioni su 384 (75,3 %) con due o più livelli; atti 2 e 3 senza livello (p1) |
| **S9** sensori laterali | **respinta** come «preallarme prima dell'ingresso nel campo frontale»; resta il canale di sola prossimità che il nucleo ha già. Interferenza: **da provare sull'hardware** (150 fotogrammi con i laterali accesi e spenti: pixel non validi e stati dei laterali) | a 0,5 m l'anticipo è 0 s su tutte le linee oltre 0,36 m dal sensore; a 2,0 m, solo sotto 1,45 m (p9) |
| **S12** piano | **respinta com'è scritta** | il «taglio minimo a 24 h» contiene tutto il nucleo (54 ore-persona, 38 in fila) più cinque moduli nuovi, e rimette l'area prevista che il v0.5 (sezione 9, punto 3) taglia proprio a 24 h. Conto su stime |
| **Attacco 3** | eseguito: com'è posto **non rompe**; rompe la retroazione | 1 cambio in 60 s con rumore attorno a 55 ms; 56 / 28 / 19 cambi con 0 / 2 / 3 s di permanenza se il tempo di ciclo dipende dalla configurazione (p4) |
| **Attacco 4** | eseguito a conto: secondo criterio **regge**, primo **cade alla lettera**; interferenza **non eseguibile oggi** | nessun falso «sensore coperto» (celle non valide 3,5 %, pixel 6,8 %, soglia 50 %); 1,86 celle «libero» sotto il corpo nel 100 % dei fotogrammi a 1,4 m/s (p5) |
| **S3–S4** (audit) | **non approvabili come scritte**: da riformulare; decide il banco di f8 | attacchi 8, 9, 10 |
| S2, S5, S10, S11 (secondo parere) | S2 regge se lo stato portato all'istante dell'uscita non tocca la mappa; S5, S10, S11 da correggere | §3 |

## 2. Gli attacchi (dieci), con previsione ed esito

| # | Previsione | Esito | Conseguenza |
|---|---|---|---|
| **1** S8, attesa permanente | 100 %; 3–10 % a p = 0,95; ≥ 95 % con celle morte | Corridoio largo 1 m dal sensore: 501 celle su 1031 nell'anello cieco → **900 su 900**. Ristretto a 1,24–3 m (530 celle): 0 % con suolo sempre valido; **8,4 %** con suolo valido al 95 %, con 1,10 ingressi in attesa al secondo; con l'1 % di celle sempre non valide, attesa permanente in **198 estrazioni su 200** | **Smentita** la riga com'è scritta: stesso difetto dell'attacco 3 al nucleo. Regge solo con la zona dichiarata, il «buco» dopo 3 fotogrammi e le celle morte dichiarate all'avvio |
| **2** S8, livelli | ≥ 20 % senza livello; ≥ 10 % con più livelli | 7 su 384 senza livello (**previsione mia smentita**), ma sono i casi comuni: ostacolo fermo (atto 2), attraversamento in vista (atto 3), ombra senza traccia (K-016). **75,3 %** con due o più livelli, senza graduatoria; a sensore guasto valgono insieme «nominale» e «avaria» | **Da riformulare** (§4). «Nominale (Go): settore libero» e «finché la pista non è confermata libera» sono un «via libera» all'uscita dall'attesa: il nucleo lo vieta (B7) |
| **3** S6, intrusione ≈ 0 | 0 esatto; ≤ 0,20 | Volume tutto visibile, soggetto fermo 9 cm dentro l'ombra: **P = 0 a ogni ciclo, per costruzione**. Da lì al volume: 64 ms a 1,4 m/s, contro 222 ms di latenza nota più un ciclo. Volume che entra 0,20 m nell'ombra, soggetto dentro: P = **0,005–0,034** a 0,53 e a 1,00 s; massimo dopo 1,5 s **0,019–0,150** secondo σ₂ | **Smentita.** La misura dice «dov'è adesso secondo il modello», non «può entrare»: può solo abbassare un allarme |
| **4** S1, il cambio crea «libero» | 50–60 % | Con quota pertinente 1,8 m la fascia alta è vista solo oltre 2,41 m: le 3 fasce tengono «non osservato» il **57,0 %** della zona; la 2D, che guarda solo il suolo, lo dice «libero» | **Smentita** la riga 2 («senza alterare il tracking geometrico»). Stesso verso per la portata: accorciata, taglia il cuneo di possibile presenza; riallungata, quelle celle rinascono «in ombra» senza avviso (a ragionamento: manca una regola di trasferimento) |
| **5** S1, riga della scheda grafica | 1,243 e 1,087 m | L'ostacolo di 15 cm è fuori dal cono di vista sotto **1,087 m**; quota massima vista a 1 / 2 / 3 m: 1,45 / 1,70 / 1,95 m. Una mappa voxel non aggiunge raggi a un sensore fermo | **Smentita** «copertura completa ostacoli bassi (< 1,1 m) e sospesi» |
| **6** Attacco 3 del file | ≤ 2; ≥ 40; 18–20; 0 ritorni | Reggono tutte. Il ciclo limite parte da un risparmio di 12–13 ms (piena a 58 ms). Riga voxel (25 → 60 → 20 ms): 19 cambi al minuto. Verso opposto: risparmio di 5 ms e carico che cessa → **0 ritorni** alla configurazione piena | L'isteresi temporale chiesta dal file **non è necessaria** (la banda 45–55 ms lo è già) **né sufficiente**: rallenta il ciclo, non lo ferma. Ogni cambio di griglia rifà l'attacco 4 |
| **7** Attacco 4 del file | 0 falsi; ≥ 90 % a 1,4 m/s | Reggono. Una persona toglie metà dei pixel solo a 0,5 m. Senza previsione: il **pannello della demo, se nero**, toglie il 23,5 % delle celle e non è «occupato»: nessun occlusore, nessun cuneo | Il «mai libero» cade per al più 0,13 s sul bordo d'attacco di chi si muove: è la memoria di 3 fotogrammi del nucleo (K-015), e proprio lì S4 mette probabilità zero. La sonda «buchi → possibile vetro» non distingue il vetro dal nero |
| **8** S3–S4, falsa «sosta» | A ≥ 90 %; B ≥ 30 % | 2000 transiti normali, misura valida a corpo tutto fuori (C6), Pd 0,9. Lettura A: **60,4 / 100 / 99,5 %** dichiarati «sosta» prima di rivedere il soggetto. Lettura B: **1,3–2,1 %** (previsione mia smentita); dopo, con 2–3 fotogrammi di ritardo: 31–43 % | La regola dei pesi **non è scritta** e le due letture danno esiti opposti. Nessuna passa il criterio di rigetto che il file fissa nel suo attacco 1: con la sosta μ₁ resta dominante fino a 1,27 s (A) e 1,33 s (B), contro 1,07 s d'uscita attesa; a 0,5 m/s 3,53 s contro 2,56 (B) |
| **9** S3–S4, il modo che cammina | ≥ 0,6 m | Soggetto fermo 9 cm dentro l'ombra: il modo mostrato si allontana fino a **1,19 m** con μ₁ > 0,5. Senza previsione: l'etichetta «± σ_eff» lo contiene nel **3 %** dei fotogrammi (errore fino a 0,93 m, σ_eff al più 0,33 m); chi rallenta a 0,3 m/s nel 43 % | «Non fa camminare un fantasma» vale solo sulle celle viste libere: **dentro l'ombra cammina**. «Riconosce matematicamente» la sosta: **smentita**; riconosce «non riemerso dove atteso», cioè anche chi rallenta, torna, o si allontana lungo l'ombra oltre i 3 m (torneo, parte 3: contenimento 22–41 %) |
| **10** S4, «previsto finché σ_eff ≤ 0,8 m» | 0,45–0,60 m | Distribuzione **uniforme** sul cuneo, cioè chi non sa niente: raggio efficace **0,39 / 0,51 / 0,77 m** con pannelli da 0,5 / 1 / 2 m | **Smentita:** la soglia misura il pannello, non la previsione. Nella demo lo stato non diventa mai «perso»; chi è uscito dall'area resta «previsto ± 0,5 m» senza fine |

Per S7 (p8): un attraversamento a 1,5 m ha θ̇ = 0,80 rad/s («bassa criticità») e resta 0,83 s dentro un corridoio largo 1 m.

**Audit delle ipotesi nascoste su S3–S4.** Il file dà per scontato: (a) una regola dei pesi, non scritta; (b) ombra esatta e nessuna fascia: lo zero secco contraddice gli invarianti 4 e 6 del nucleo, e il torneo l'ha già misurato (ombra stretta di 20 cm: identità 68 %; falso «libero» di 0,3 s: massa giusta sotto il 5 %); (c) misura disponibile all'istante dell'uscita, mentre C6 la ritarda di 0,2 m di cammino; (d) «libero» senza età, mentre con la latenza vale 0,288 s; (e) velocità d'ingresso «affidabile», che con C6 è quella di prima del bordo; (f) sosta al centro dell'ombra; (g) «senza stimare accelerazione»: H2 impone 2,0 m/s² di frenata iniziale (α = 0,889 a 1,2 m/s), un'ipotesi e non una stima, da dichiarare.

## 3. Letture sbagliate del v0.5 e dei limiti del nucleo

1. **«Sotto 1,1 m» è una distanza dal sensore, non una quota** (v0.5, sezione 4 e riquadro finale; nucleo, B1: 1,09 m). La fascia bassa 0,15–0,60 m non «chiude il buco»: lì l'ostacolo è fuori dal cono. Lo chiudono il montaggio o un sensore in basso.
2. **`INV-3` e `INV-5` non esistono nel v0.5** (`grep -c INV`: 0); nel nucleo i numeri 3 e 5 sono altre regole.
3. **Parole.** Il v0.5 scrive «mai via libera» e «chiede, non comanda»; «Go», «RA» e «blocco del decollo» promettono un comando. In ACAS l'avviso di risoluzione raccomanda una manovra all'equipaggio, non segnala un'avaria (https://skybrary.aero/articles/acas-resolution-and-traffic-advisories: pagina **non aperta**). «ABAR»: nome di un prodotto, secondo il motore; **non verificato**.
4. **S5 contro S2:** «visto: età del dato 0 ms» contraddice la latenza dichiarata (circa 155 ms). «conf Z %» e i due decimali non hanno una taratura.
5. **S10 con S8:** «libero solo se tutte le fasce pertinenti sono osservate» rende «non osservato» il 57 % della zona (quota 1,8 m) o il 100 % (2,0 m): con S8, attesa permanente. Le fasce pertinenti vanno dichiarate per profilo.
6. **S11:** `SOSTA_IN_OMBRA` scatta nei transiti normali (attacco 8); il nome onesto è «non riemerso dove atteso».
7. **55 ms sulla media di 15 cicli** non è il 95° percentile che il nucleo chiede.

## 4. Le versioni corrette

**S8** (vale il livello più alto; mai «Go»):
1. *Affidabilità persa*: integrità del sensore persa, e solo quella.
2. *Attesa prudente*: possibile presenza o «buco» in una cella del corridoio **dentro la zona dichiarata**, oppure cuneo di possibile presenza a meno di v_max·T dal volume protetto. Finisce riosservando, o per azzeramento dell'operatore, registrato.
3. *Attenzione*: bersaglio visto, già nel corridoio o la cui retta di moto vi entra entro T.
4. *Ostacolo o ombra*: «ostacolo a d metri», «zona non vista dietro l'ostacolo».
5. *Nominale*: «nessun ostacolo osservato fino a d metri nella zona dichiarata». Anello cieco, fuori campo e celle morte si dichiarano una volta all'avvio.

**S6.** Traccia vista: tempo d'ingresso nel volume lungo la velocità stimata, con margine k·σ; avviso se minore di T (latenza più reazione). Traccia nascosta: **nessuna probabilità**; decide il cuneo (livello 2). Nessun numero abbassa un livello.

**S1.** In esercizio si scende soltanto, e si spegne solo la rete a lato; la griglia non cambia. Si risale al riavvio o su comando. La scelta usa il costo di ogni configurazione misurato all'avvio, non il tempo di ciclo corrente. Riga 6: «mappa voxel in prova, fuori dal percorso critico; ostacoli bassi sotto 1,09 m e sospesi sotto 2,41 m restano non osservati». Riga 4: «attenua, da misurare». La colonna diventa «che cosa resta dichiarato».

## 5. Costo (stime mie, non misurate)

S8 riscritta: 1–2 ore oltre le 3 di B7. S6 ridotta: 2 ore. S1 ridotta: 3 ore. S7 e S9: nessuna. Calcolo: due ipotesi ritagliate su 372 celle più i pesi, **0,125 ms** per ciclo e per traccia in Python puro (`risultati_costo.txt`, indicativo). Per farle posto si tagliano il selettore completo, la mappa voxel e i sensori laterali.

## 6. Non verificato

L'interferenza fra camera e sensori laterali; il nero vero (una stereo attiva può vederlo); le ore; le definizioni aeronautiche; il rumore e Pd veri, da cui dipendono gli attacchi 8 e 9; la sosta fuori centro e in due dimensioni (il mio modello di S3–S4 corre lungo una linea).

## 7. Correzioni obbligate prima di qualunque adozione, in ordine

1. Via «Go», «settore libero», «pista confermata libera»: il livello più basso è «nessun ostacolo osservato fino a d metri».
2. S8 riscritta con graduatoria, zona dichiarata e le righe per ostacolo fermo e attraversamento.
3. Via la probabilità d'intrusione sulla distribuzione ritagliata; nessun indice abbassa un livello.
4. S1: degrado in un solo verso; nessun cambio di griglia o di portata in esercizio senza una regola di trasferimento che non abbassa mai una cella (ordine: libero, occupato, in ombra, possibile presenza, non osservato), con la sua prova.
5. Via le promesse: «garanzia di sicurezza mantenuta», «elimina falsi ostacoli», «copertura completa», «riconosce matematicamente», «non fa camminare un fantasma».
6. S3–S4: una sola regola dei pesi, scritta; la fascia prima dello zero; il ritardo di C6 e della latenza nella verosimiglianza; «perso» non legato a σ_eff; evento rinominato.
7. S5: età vera del dato; niente «conf %» né centimetri prima della taratura.
8. S12 riscritto sulle ore del nucleo.

**Rifare:** nella cartella, `PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 attacchi_f9.py p1` (poi `p2` … `p9`, `p6x`).
