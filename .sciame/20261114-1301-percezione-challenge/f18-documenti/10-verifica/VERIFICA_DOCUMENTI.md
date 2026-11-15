# Verifica dei documenti aggiornati contro VERDETTO_2C

`sciame-avversario`, 2026-11-15, dalle 03:35:26 alle 03:43 circa (`date -Is`). Previsioni scritte prima, alle 03:35:41,
in `PREVISIONI.md` (questa cartella). Tutto ciò che è verificato qui riguarda il testo dei documenti. Le misure non le
ho rifatte: le cifre giuste le prendo da VERDETTO_2C, che prevale, e da VERDETTO_2B o VERDETTO_FASE2 dove la 2c non le
cambia. **Indipendenza:** condivido con gli autori i verdetti da cui partono. Il controllo trova solo gli scarti fra
documento e verdetto, non gli errori dei verdetti.

## 0. In testa: esiti delle previsioni e regole

- **P1 regge.** I tre documenti sono stati scritti fra le 03:03 e le 03:17, prima di VERDETTO_2C (03:35). Avevano tutti
  le cifre della 2b ormai superate: 163/171 «libero» col pannello, E1 a 49/60, impronta oltre 10 km in 36/60 con
  mediana di 42 km, «nel prototipo la mappa è dichiarata completa», 665 s. Gli autori le avevano marcate `% 2C`:
  8 punti nell'allegato, 3 nella proposta, 17 nello stato.
- **P2 smentita per la proposta, regge per l'allegato.** Il programma `controlla_pdf.py` lavora sul testo estratto con
  `pdftotext`. Nella proposta ha trovato 1 riferimento interno: «Come è stato ottenuto. Uno sciame di agenti
  specialisti … riconti di un arbitro». Dopo la correzione ne trova 0 (resta solo «v2.0» nella testata, che è la
  versione del documento). Nell'allegato le 13 occorrenze sono tutte usi tecnici: H0 della prova binomiale, «nucleo
  veloce» della CPU, «riprovato», `api/v2` di adsb.lol. Esiti: `esito_*_prima.txt` e `esito_*_dopo.txt`.
- **P3 regge.** La proposta aveva 2 pagine. La mia prima correzione l'ha portata a 3. Ho accorciato il testo, senza
  rimpicciolire nulla, ed è tornata a **2 pagine** (`pdfinfo`). La copia a 3 pagine è conservata:
  `proposta_sciame_v2.0_verifica3pagine.tex`.
- **P4 regge.** L'allegato compila con xelatex, bibtex, xelatex, xelatex: 0 errori, 0 riferimenti indefiniti,
  0 Overfull, 84 pagine (erano 83). Resta un solo avviso, «Float too large by 3.4 pt» sulla tabella di sintesi, che
  c'era già prima (`allegato_tecnico_prima2.log`). Le mie righe l'avevano portato a 12,9 pt e le ho accorciate.
- **P5 smentita.** Le frasi «da non dire» del § 4 non compaiono in forma affermativa: compaiono solo negate («nessuna
  funzione d'ingaggio», «non si restringono») o come «in tempo reale» detto di lavori altrui. I difetti veri sono
  frasi **più forti del verdetto** perché superate (sotto).
- **Regole.** Non ho cancellato nulla e non ho usato rete, git o sudo. Un processo alla volta, con `timeout`. Prima
  di ogni modifica ho fatto una copia accanto con `cp -n`. Poiché esistevano già dei `_prima` degli autori, le mie
  copie si chiamano `*_prima2.tex` e `*_prima3.tex` (allegato), `proposta_sciame_v2.0_prima.tex/.pdf` e
  `STATO_PROGETTO_prima.md`. Ho scritto solo in `f18-documenti/`.

## 1. Correzioni

### Allegato (`01-allegato/allegato_tecnico_v2/`)

Le correzioni sono fatte con `correggi_allegato.py` (sostituzioni esatte, una occorrenza ciascuna) più due ritocchi in
linea, poi ricompilate.

1. **«Libero» col pannello** (sommario, tabella di sintesi, cap. 8, cap. 9, cap. 10 nei §§ mappa, prove, smentiti e
   validità). Prima: «falso in 163 su 171», un limite. Ora: 0/171 [0; 0,022] con la ritenuta del ritorno di 5 s,
   **solo con la mappa del sito dichiarata completa (ipotesi)**. Con la mappa dichiarata ma sbagliata è falso in 5 casi
   costruiti su 6. Il 163/171 resta come storia della regola precedente.
2. **Mappa nel prototipo.** La frase «nel prototipo provato la mappa è dichiarata completa per impostazione» era falsa
   dopo la 2c. Ora dice che per impostazione la mappa non è dichiarata, con 6/6 «non osservato», e che la convalida
   con lo sfondo non è chiamata.
3. **E1.** Da «1,2–2,2 s, 49/60, oltre 10 km in 36/60, mediana 42 km, massimo 74 km, separazione a −12,5 s» a:
   - 1,2–1,8–2,3 s, cioè 51/60 [0,739; 0,919], 50/60 col tipo «contatto»;
   - un residuo di 3,1–4,5–5,3 km, con 0/60 sopra i 10 km;
   - una zona che non si riduce guardando (0/60);
   - 0/60 eventi prima dell'urto, «regola notata dopo, non una previsione».

   Le cifre della controprova della 2b (24/30, 20/30) sono tolte. Il 0,9973 resta, marcato «versione precedente».
4. **E2 ed E5.** Aggiunti 30/30 col v3, la mediana di 96 tracce avvisate e 0/30 [0; 0,114].
5. **Ritenuta del ritorno** (cap. 10, «Più sensori»): la regola dei 5 s, con il suo prezzo non misurato.
6. **Limite 6 di VERDETTO_2C** (cifre non rimisurate col v3): nuovo punto nel cap. 8 e «Tre precisazioni» nel
   cap. 10. I 100/100 e 9/100 sono marcati «versione precedente delle regole».
7. **Classificatore** (introduzione, cap. 8, cap. 9, riquadro del cap. 10): mancava «supposto esistente, lavori
   futuri», e l'ho aggiunto. Le etichette a mano c'erano già.
8. **Appendice B**: da 665 s a 698 s (VERDETTO_2C lo adotta senza ricontarlo). Tolti i commenti `% 2C`.
9. **Rimasti, e vanno bene:** nessuna prova su un sensore fisico lasciata intendere (le occorrenze sono tutte
   negazioni). Il nome `lp_A1` resta nei comandi dell'appendice B, come chiede la consegna del redattore.

### Proposta (`02-proposta/proposta_sciame_v2.0.tex/.pdf`)

Le correzioni sono fatte con `correggi_proposta.py` più un passaggio di accorciamento.

1. **Limiti per primi.**
   - «Il "libero" dipende dalla mappa»: 0 su 171 solo con la mappa dichiarata completa; falso in 5 casi su 6 con la
     mappa sbagliata; il prototipo non la dichiara. Prima diceva 163/171 e «come fa oggi il prototipo», due cose
     superate.
   - Eventi: 51/60, circa 4,5 km che non si riducono guardando, nessuna distinzione di chi è in pericolo.
   - «Rullaggio e radar d'aeroporto: cifre delle regole precedenti, non rimisurate».
2. **§ 3.1**: «(regole precedenti)» sui 100/100; aggiunto «mai "libero" sul drone (0 su 171), con la mappa dichiarata
   completa».
3. **§ 4, collisione**: 1,2–2,3 s, 51/60 [0,74; 0,92], circa 4,5 km (mai oltre 5,3). Era «enorme, oltre 10 km in 36
   su 60».
4. **Tabella dei requisiti**: 51/60; «0/171 col pannello solo con la mappa dichiarata».
5. **§ 9**: da «665 s, 20 scene, il controllo non guarda ancora il "libero" dentro l'avviso» a «698 s; 8 scene rifatte
   con 0 errori e 0 "libero" dentro l'avviso».
6. **§ 11 Aperti**: tolti il «libero» col pannello e la mappa nel prototipo, che sono chiusi. Aggiunti «convalidare
   la mappa con lo sfondo» e «rimisurare le altre scene».
7. **Organizzazione interna**: la nota «Come è stato ottenuto. Uno sciame di agenti… arbitro» è diventata «Dove sono
   le prove. … nell'allegato tecnico».
8. **Verificato:** il classificatore è detto «supposta esistente, lavoro futuro; oggi etichette a mano»; «Nessun
   sensore fisico» è il primo limite; le pagine sono 2.

### Stato v4 (`03-stato/STATO_PROGETTO.md`, Markdown, niente da compilare)

Le correzioni sono fatte con `correggi_stato.py` più due ritocchi. Ho seguito la regola del documento: il superato
resta, con la dicitura «superata».

1. **Riquadro «Versione 4.1»** nella sintesi, prima di «Che cosa è aperto». Prevale sulle righe 2, 4, 7 e 8.
2. **I 17 commenti `<!-- % 2C -->`** sono sostituiti da note «[Superata dalla fase 2c: …]» con la cifra nuova. Quattro
   righe citavano il commento fra apici e il programma le aveva rovinate. Le ho ripristinate dalla copia `_prima`, con
   l'aggiunta «(alla versione 4.1 sostituito da note "superata")».
3. **§ 11.14 nuovo**, la fase 2c, con:
   - la tabella dei cambi di stato;
   - i limiti, i «da non dire» nuovi e le scene _v3;
   - K-614, le regole violate dagli autori della 2c e gli aperti.
4. **§ 11.10**: le affermazioni della 2b sono marcate come superate da VERDETTO_2C, §§ 3–4.
5. **Registro**: la riga 5 «(da scrivere)» è marcata superata, e c'è una riga 5 (a) nuova.

## 2. Stati proposti

- «Le cifre dei tre documenti coincidono con VERDETTO_2C»: **verificato** sull'insieme dei punti `% 2C`, sui grep di
  163, 171, 49/60, 42/74 km, 10 km, 665 s, «copre il sito», «enorme» e sui riferimenti alla mappa. Non ho controllato
  in modo esaustivo le altre cifre dei documenti, salvo quelle che toccavo. Le restanti occorrenze di «163» sono altre
  grandezze: una tabella di costo, un DOI di Zenodo.
- La sezione 2 di `PROPOSTA.md` (la tabella delle fonti della proposta) e `ALLEGATO_AGGIORNATO.md` sono rapporti degli
  autori e citano ancora le cifre della 2b. Non li ho toccati: **da aggiornare** a cura degli autori.

## 3. Che cosa propongo dopo

1. Un rilettore guardi le immagini delle due pagine della proposta: ho controllato solo il testo estratto, non
   l'impaginazione visiva.
2. Se il coordinatore vuole citare il metodo nella proposta, lo faccia senza nominare l'organizzazione interna.
3. Al rifacimento col v3 di A2, A3, A4 e della controprova, togliere le diciture «regole precedenti».
