# Consegna di `sciame-interfacce` — f9, S5 (regole di disegno e di suono) e uscita dei livelli di S8

Lavoro dalle 2026-11-14T15:38:51+01:00; previsioni scritte alle 15:41:47, prima di ogni prova (`PREVISIONI.md`, con gli esiti). S5 la prova f8, che non ho letto: questo è un secondo parere.

## 0. Scostamenti, regole violate, cambi di stato

- **Regola sfiorata:** un `ls` ha stampato i **nomi** delle sottocartelle di `f7-estensione`, `f8-continuita` e `f9-preproposta`; nessun file aperto al loro interno.
- **Previsioni:** sette; sei reggono; **int-P7 smentita in parte** (la regola sonora «per settore» resta al 10,7 % di segnali in ritardo con tre oggetti in tre settori, contro il 5 % previsto); di int-P4 ho indebolito dopo una conseguenza («non scatta mai» → «non scatta nello stato di massima ignoranza»).
- **Lunghezza:** circa 2400 parole, tabelle comprese: al limite delle tre pagine, forse poco oltre.
- **Limiti:** nessuna persona, nessuno schermo, nessun suono riprodotto. Gli script sono miei (generatore e giudice dello stesso autore): conti, non misure indipendenti. Le pagine in rete le ho lette attraverso uno strumento che riassume.
- **Cambi di stato proposti:** «il colore basta a distinguere gli stati» → **smentito**; «±X.XX m è leggibile e sostenuto dalla taratura» → **smentito**; «l'inviluppo scompare» compatibile con la continuità → **smentito per lettura** del criterio 4 di f8; «conf Z %» → **non risolto** (non è definito); i suoni → **non risolto** (servono persone).

## 1. Verdetti proposti

| Parte | Verdetto | Prova |
|---|---|---|
| **S5, disegno**: nessun riquadro pieno sul previsto, area ritagliata, parola «PREVISTO», righe sull'ombra con l'età | **approvata con sette correzioni**: trama prima del colore; niente sfumatura; contorno sulla posizione misurata, con l'età vera; etichetta nuova; l'area non sparisce; solo il cuneo d'ingresso, con la fascia; più tracce nella stessa ombra, un solo cuneo | il nocciolo rispetta gli invarianti 3 e 4 del nucleo; le correzioni vengono da int-P1…P6 e dalle critiche 1–7 |
| **S5, etichetta** «±X.XX m \| t_occ Y.Ys \| conf Z%» | **respinta in questa forma** | cambia 15 volte al secondo; «±σ» contiene il 39,3 %; «conf» non è definito; tre etichette non stanno sullo schermo |
| **S5, suono** | **non c'è niente da approvare**: il titolo lo promette, il testo non dà una regola. La mia proposta int-1 (§4) è **da provare con persone** | decide la prova del §5: almeno 54 risposte giuste su 60 |
| **S8, uscita dei livelli** | **approvata con correzioni**: quattro livelli, rinominati; via «Go», «TA», «HOLD», «RA», «FAIL-SAFE»; «RA / FAIL-SAFE» diviso in due | critiche 8–12; la logica dei livelli non mi compete |

## 2. Critiche numerate

1. **In bianco e nero il colore non distingue niente.** I tre colori di stato del documento v0.5 stanno fra loro a 1,12 / 1,10 / 1,02 : 1 in grigio; in una terna «semaforo» verde e rosso a 1,10:1 (1,13 in deuteranopia). La soglia per gli oggetti grafici è 3:1 (WCAG 1.4.11). S5 scrive «zebrata/ambrata», l'una **o** l'altra: l'ambra da sola cade (tinta al 35 % su bianco: 1,17:1 dal grigio dell'ombra; ambra piena sul bianco: 1,8:1, conto a mano). *Prova:* `risultati_interfacce.txt`, A.
2. **La «sfumatura di densità»** su un proiettore è quella stessa tinta debole: non si vede. Con le due ipotesi separate dà due macchie, e chi guarda conta due oggetti.
3. **«±X.XX m» promette ciò che la previsione non ha.** (a) Con il filtro del nucleo l'ultima cifra cambia in 26 cicli su 26 fra 0,3 e 2 s: l'etichetta cambia 15 volte al secondo. (b) La taratura dell'attacco 5 non regge il secondo decimale: 27 passaggi su 30 danno una copertura fra 74,4 e 96,5 %, cioè un raggio fra 0,62 e 0,97 m su 0,80 dichiarati; 360 su 400, fra 0,75 e 0,85. (c) «±σ_eff» in due dimensioni contiene il soggetto nel 39,3 % dei casi, ma l'attacco 5 la chiama «ellisse al 95 %» (2,45 σ: 1,96 m con σ = 0,8). (d) Con la massa stesa su tutto il cuneo della demo lo scarto è 0,48–0,54 m: il numero misura il pannello, non ciò che il sistema sa, e lì la soglia d'esempio «σ_eff ≤ 0,8 m» non porta a «perso». *Prova:* ivi, B–E.
4. **«conf Z %» non è definito.** Può essere il peso μ₁, la quota di massa nell'ombra, il livello dell'area. Un giurato leggerà «sicuro al Z % che l'oggetto sia lì» (non verificato: lo decide una domanda del §5). Se è μ₁, all'ingresso vale 80 % per scelta del programmatore; e quando cala a favore della sosta, cioè quando il sistema è **più** convinto che la persona sia ancora dietro il pannello, il numero scende: lettura rovesciata. *Prova:* preproposta §2.2–2.4, a ragionamento.
5. **Tre oggetti nascosti.** A leggibilità da sala (maiuscole da 16–22 minuti d'arco a 6 m, schermo di 2 m e 1920 punti: ipotesi mie) l'etichetta di 40 caratteri è larga 843–1159 punti, 2,3–3,2 volte l'ombra del pannello; tre fanno 2528–3476 punti su 1920. In suono, una coda per oggetto fa partire il 20,4 % dei segnali oltre 300 ms. E il nucleo, con due tracce pendenti nella stessa ombra, **non dà l'identità**: aree distinte mostrerebbero una conoscenza che non c'è. *Prova:* ivi, F, G; `SOLUZIONE_V2.md`, B4, B5.
6. **«L'inviluppo scompare»** al passaggio previsto → perso. Il criterio 4 del contratto di f8 chiede che il sistema «continua a visualizzare con un segno diverso, invece di sparire»; una forma che sparisce si legge «se n'è andato». Inoltre la regola può tornare indietro (il ritaglio restringe σ_eff) e far lampeggiare i due stati: nel nucleo «perso» è assorbente fino al riaggancio.
7. **«Visto: età 0 ms»** è falso: la latenza nota è circa 155 ms, e S2 chiede di dichiarare l'età. Con S2, poi, il contorno pieno finirebbe sulla posizione **portata avanti** (0,22 m a 1,4 m/s): una previsione disegnata come osservazione, contro l'invariante 3.
8. **I nomi dei livelli sono comandi presi in prestito.** Nell'anticollisione di bordo, su un «TA» i piloti non devono manovrare; a un «RA» devono rispondere subito manovrando (Wikipedia, pagina aperta, fonte secondaria). Il prototipo dichiara e chiede, non comanda. «NOMINAL (Go)» è un «via libera», vietato dal nucleo (B7; condizione 9 del verdetto); «HOLD» vale «finché la pista non è confermata libera», ma il prototipo non conferma mai «libero».
9. **«RA / FAIL-SAFE» fonde due situazioni opposte**, «vedo un oggetto vicino» e «non vedo niente»: toglie proprio la segnalazione della perdita di affidabilità che la traccia chiede. «Fail-safe» promette una sicurezza che il prototipo dichiara di non avere.
10. **I quattro livelli non sono una scala.** «Attenzione» è «vedo qualcosa», «attesa prudente» è «non so»: possono valere insieme. In un semaforo a quattro gradini il verde diventa un permesso.
11. **Per una persona non vedente in Italia un battito regolare è già un codice.** Ai semafori acustici 60 impulsi al minuto vogliono dire via libera, 120 arresto o sgombero, il silenzio arresto (art. 162, comma 5, DPR 495/1992, letto su un sito divulgativo; testo ufficiale non aperto). Un battito a uno o due colpi al secondo sarebbe capito come un ordine.
12. **Il livello 3 può non finire mai**: con l'ostacolo fermo la possibile presenza non si rilascia (nucleo, B5). Un suono senza fine viene ignorato, ma non lo può togliere un timer.

## 3. Dove la preproposta ha letto male

- **«Interrompe la previsione a 0,5 s, lasciando un avviso statico»**: nel nucleo non c'è un tetto di tempo ma una regola geometrica (l'area copre metà del cuneo); l'avviso porta l'età e si rilascia cella per cella.
- **Ritaglio a zero su ogni cella «libero»**: il nucleo ammette previsione e possibile presenza su una fascia di 0,40 m di libero (invariante 4), perché «libero» ha un'età. Un'area tutta dentro l'ombra dice «fuori non può essere»: non è provato.
- **Righe «sull'intera area in ombra»**: nel nucleo la possibile presenza è il solo cuneo in cui la traccia è entrata; le altre ombre restano «in ombra» (correzione C5: 45,5 m² contro 1,01).
- **Il suono**: il nucleo ha già un segnale di 0,3 s per stato e la frase a stato stabile (C11); il v0.5 scrive «da provare con persone bendate». S5 non li riprende.
- **«Go» e «RA»**: il v0.5 scrive «mai via libera» e «non comanda nulla».

## 4. La specifica corretta (int-1)

**Regole d'accessibilità.** (1) Ogni stato si distingue per **forma o trama e per una parola**; il colore viene terzo (WCAG 1.4.1). Controllo: una schermata in grigio. (2) Tratti scuri su fondo chiaro, almeno 3:1; l'ambra solo come tinta sotto righe scure. (3) Maiuscole di almeno 27 punti, tratti di 3, passo delle righe di 16 (per 6 m e schermo di 2 m: da rifare sulla sala vera). (4) Il testo cambia al più due volte al secondo; un decimale, per eccesso; niente «σ», «t_occ», «conf». (5) Lo stato si legge su un fotogramma fermo. (6) Sulla mappa solo il numero d'identità; i testi a lato, per priorità. (7) Ogni coppia di suoni differisce per almeno due caratteri (numero d'impulsi, altezza, timbro); niente toni continui, niente battiti a 60 o 120 al minuto. (8) Un segnale alla volta, per settore, con la priorità di B7; quello scaduto si scarta. (9) **Il silenzio vuol dire solo «il sistema non sta vedendo»**, detto all'avvio. (10) Legenda sempre a schermo, con la riga «Area al 90 %: nelle prove ha contenuto la persona N volte su M».

| Stato o livello | Segno visivo | Segno sonoro | Testo |
|---|---|---|---|
| **VISTO ORA** | contorno pieno sulla posizione **misurata**; freccia = spazio in 1 s, solo se «mobile» | un tono pieno di 0,3 s, alto | «n. 2 VISTO · sinistra · 2,0 m»; l'età solo se supera 0,3 s |
| **PREVISTO** | nessun riquadro; contorno **tratteggiato** dell'area al 90 % ritagliata su ombra e fascia; al più un secondo contorno al 50 %; niente sfumatura | due impulsi in 0,3 s, medi; ogni 1,5 s finché dura | «n. 2 PREVISTO · nascosto da 1,5 s · entro 0,5 m» |
| **POSIZIONE NON NOTA** (perso + possibile presenza) | l'area **non sparisce**: si allarga al cuneo d'ingresso e diventa **righe oblique scure** su tinta ambra; il numero resta | tre impulsi in 0,3 s, gravi, una volta; poi il battito del livello 3 | «n. 2 NON VISTO da 12 s · possibile presenza dietro l'ostacolo · può aver lasciato l'area» |
| Più tracce nella stessa ombra | un solo cuneo a righe, nessuna area singola | come sopra | «almeno 2 entrati, non rivisti da 5 s» |
| **1 · Nessun ostacolo osservato** (ex «nominale», «Go») | banda neutra, **mai verde**, cerchio vuoto | un tocco sommesso ogni 3 s | «NESSUN OSTACOLO OSSERVATO fino a 3 m» |
| **2 · Attenzione** (ex «TA», più l'oggetto vicino di «RA») | banda con triangolo | il tono di stato, poi due toni che salgono ogni 1,5 s; frase a stato stabile | «ATTENZIONE: in avvicinamento · sinistra · 2 m» |
| **3 · Zona non verificata** (ex «HOLD», «attesa prudente») | banda con le stesse righe della mappa | doppio tocco alto-basso ogni 3 s, senza tetto di tempo | «ZONA NON VERIFICATA: possibile presenza da 12 s»; a parte, solo per l'operatore: «Richiesta: verifica» |
| **4 · Affidabilità persa** (ex «avaria», «FAIL-SAFE») | banda con croce; mappa in grigio con l'età dell'ultimo quadro | tre toni che scendono e subito la frase, ripetuta ogni 5 s; **il battito tace** | «AFFIDABILITÀ PERSA: non vedo da 2 s» |

**Che cosa non deve sembrare un comando.** Parole: «Go», «via libera», «libero», «OK», «sicuro», «stop», «fermati», «attendi», «evita», «hold». Segni: verde pieno, spunta, ottagono rosso, frecce che dicono dove andare (la freccia sta solo sull'oggetto). Suoni: tono continuo, sirena, arpeggio allegro. La richiesta all'operatore è una riga distinta dallo stato; alla persona non vedente nessun imperativo. **Livello 3 senza fine:** una «presa visione» dell'operatore ferma la ripetizione della frase, non le righe né il doppio tocco, e resta nel registro.

**Meccanismo, previsione, smentita.** Meno certezza, segno più frammentato, allo stesso modo all'occhio e all'orecchio (pieno, tratteggiato, a righe; uno, due, tre impulsi). Previsione: tre persone esterne riconoscono stato e livello in almeno 54 risposte su 60 per canale. La smentiscono: meno di 54; un «previsto» letto «visto» da due su tre; una sola persona che al battito del livello 1 dica «posso andare».

## 5. La prova in cinque minuti con tre persone

Tre persone esterne alla squadra, alla distanza dell'ultimo giurato; soglie scritte prima. **Vista, 2 minuti:** 20 fotogrammi fermi **in grigio**, 3 s l'uno, a caso, con la sola legenda; ognuno scrive V, P o N. **Suono, 2 minuti**, bendati e fermi: 20 s del battito del livello 1 senza spiegazione e la domanda «che cosa ti dice?»; ogni suono una volta con il suo nome; 20 suoni a caso; in coda il battito si ferma senza preavviso, e entro 5 s qualcuno deve dire «non vede più». **Parole, 1 minuto:** le quattro bande («ti sta dicendo di fare qualcosa?») e la vecchia etichetta («che cosa vuol dire 72 %?»). Con 54 su 60, chi riconosce l'80 % passa nel 3,1 % dei casi, chi il 95 % nel 97,0 % (`risultati_prova_persone.txt`).

## 6. Costo

- **Ore (stima mia, non verificata):** circa 6 ore-persona oltre le 6 di B8: 3 per il disegno, 2,5 per i suoni preregistrati e il miscelatore a priorità, 0,5 per la prova. Per farle posto cadono la sfumatura, «conf» e le etichette sulla mappa. Nel taglio a 24 ore, circa 3: trama, parola, tre suoni di stato, battito del livello 1, frase del livello 4.
- **Calcolo per ciclo (misurato, indicativo):** righe e contorno tratteggiato su 1920×1080, 0,59 ms in media e 1,03 al massimo (C, un core). Da evitare la maschera ricalcolata punto per punto: 18,3 ms, il 28 % del ciclo. Il suono è riproduzione di campioni: non misurato.

## 7. Non verificato, e che cosa lo decide

- Che trame, parole e suoni si riconoscano; che un giurato legga «conf» come probabilità; che il battito non copra l'udito ambientale: la prova del §5, e per l'udito una persona non vedente vera.
- Tre oggetti in tre settori: con 0,3 s più 0,1 s di pausa e l'ordine di B7, il 12,5 % dei segnali parte oltre 300 ms; con 0,2 s più 0,05 s, lo 0,8 % (esplorazione dopo l'esito). Se 0,2 s si riconoscano, non lo so. Con una sola persona nascosta, come nella demo, la coda non ritarda.
- I 16–22 minuti d'arco (ISO 9241-303, a pagamento, non aperta), la sala vera, e l'uso delle matrici di Machado in RGB lineare (scelta mia; le matrici sono verificate sulla pagina degli autori).
- Livello dell'area, ritaglio e regola previsto → perso: li decide f8; qui c'è solo come si mostrano.

**Fonti aperte oggi:** [WCAG 1.4.1](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html) · [WCAG 1.4.11](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html) · [Machado e altri 2009](https://www.inf.ufrgs.br/~oliveira/pubs_files/CVD_Simulation/CVD_Simulation.html) · [TCAS, Wikipedia](https://en.wikipedia.org/wiki/Traffic_collision_avoidance_system) · [art. 162 del regolamento del Codice della strada](https://leggeinchiaro.it/articolo-162-regolamento-codice-strada/) · [IEC 60601-1-8, copia non ufficiale](https://standards.har-el.com/Projects/181701/60601-1-8/html/A2SubCl-6-3-3-1-a-priority-encoded.htm), precedente per la regola 7.

**Rifare:** nella cartella, `PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 -I prove_interfacce.py` (seme 20261114), lo stesso per `prove_interfacce_bis.py`; `gcc -O2 costo_disegno.c -lm`.

**Dopo.** F8 fissa livello dell'area e regola previsto → perso con questa specifica davanti; il redattore porta nel documento i quattro nomi nuovi; la prova del §5 va nella prima ora con l'hardware.
