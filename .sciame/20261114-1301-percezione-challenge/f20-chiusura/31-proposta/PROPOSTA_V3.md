# Proposta v3.0, stato del progetto v5, riferimenti (f20-chiusura/31-proposta, `sciame-comunicazione`)

15-11-2026, dalle 06:34:56 alle 06:45 circa (`date -Is`). Fonte unica delle cifre:
`f20-chiusura/20-verdetto/VERDETTO_FINALE.md` (compreso F-809, F7r).

## 1. In testa: cambi di stato e regole

- **Cambi di stato:** nessuno proposto da me. Riporto quelli del verdetto finale (F-801…F-809).
- **Regole.**
  - Nessun file cancellato.
  - Le copie sono state fatte prima di modificare, con `cp -n`: `STATO_PROGETTO_v4.md`, `RIFERIMENTI_v4.md` e
    `riferimenti_v4.bib`. Le copie `proposta_sciame_v2.0.*` esistevano già, e sono identiche al sorgente e al PDF
    v2.0 (`cmp`).
  - **Sovrascritture, da dichiarare:**
    - `proposta/proposta_sciame.pdf` (v2.0) è stato sostituito dal PDF v3.0. VERSIONI.md lo prevede, e la copia
      v2.0 esiste.
    - Ho riscritto due volte la mia copia `proposta_sciame_v3.0.pdf`/`.tex`, creata pochi minuti prima, dopo una
      correzione di frase.
  - Niente git, niente sudo, niente rete.
  - Compilazione nello scratchpad, poi copia nel progetto.
- **Indipendenza.** Condivido con il verdetto il modello linguistico e i file. Non ho ricontato nessuna cifra:
  controllo la trascrizione dal verdetto, non i conti.

## 2. Che cosa è stato consegnato

| File | Stato | Prova |
|---|---|---|
| `proposta/proposta_sciame.tex`, `.pdf`, copie `proposta_sciame_v3.0.tex` e `.pdf` | v3.0, **2 pagine** | `pdfinfo`: Pages 2; 0 overfull; sorgente e PDF uguali alle copie (`cmp`) |
| `proposta/VERSIONI.md` | riga v3.0 aggiunta in coda | — |
| `documentazione/STATO_PROGETTO.md` | v5: testa nuova; voce d'indice; **cap. 12** nuovo (fasi 3 e 4, D1–D6, risultati, confidenza, limiti, file, regole violate, aperto); riga «5 (b)» nel registro | 2681 → circa 2780 righe; i capitoli 1–11 non sono toccati |
| `documentazione/RIFERIMENTI.md` | 393 → 410 voci: § 6bis nuovo con [394]–[410] da FONTI_APERTE § 4; note f20 su [348], [349] e [353]; testa f20 con le correzioni di frase | 410 testate `###` |
| `documentazione/riferimenti.bib` | 211 → 228 voci (`nuove.bib` in coda) | `bibtex` su una copia: 228 voci, 0 errori, 1 avviso già noto (`vovk2005`) |

## 3. Le scelte di comunicazione della proposta

- **Messaggio in una frase.** «Dove la vista si perde, MoVi non dice mai "libero": dichiara dove l'oggetto può essere
  e quanto vale, secondo dopo secondo, quella regione.»
- **Ordine:**
  1. limiti per primi, con la collisione veloce non dichiarata e il radar accecato;
  2. l'idea;
  3. il volo veloce;
  4. la confidenza, con la formula e la tabella;
  5. F7;
  6. F3, come limite e come miglioria in prova;
  7. sensori e calcolo, come stime;
  8. il sito e gli altri usi;
  9. i requisiti;
  10. la strada verso il sistema attuato, con una soglia per ogni miglioria.
- **Marche.** Le marche sono le classi del verdetto: S, I, L, NP. Lo stato di ogni cifra è scritto in corsivo: sim,
  pub, calc, ip, dim.

**Da dove viene ogni cifra (sigle del verdetto finale).**
- § 2: V-1…V-10.
- § 3: § 4 del verdetto e curva F7.
- § 4: S-1…S-9, S-6r, F-806, F-807, F-808.
- § 5: V-11, § 3 e § 5 riga 1 del verdetto, V-13.
- § 6: § 5 righe «Latenza del calcolo», «Primo avviso», «Tempestività», «Continuità col radar rotante»; § 6 del
  verdetto.
- § 7: LP-1…LP-11, CR-6, § 2.4.
- § 9: § 5 del verdetto.

**Frasi vietate (§ 7 del verdetto): controllate sul testo estratto del PDF.**
- «niente è validato» compare solo come negazione.
- «tarata» porta sempre la sua condizione.
- «sempre» è stato tolto dalla tabella dei requisiti.
- In F7 si usa solo «mantiene la traccia» e «drone seguito». Il verdetto usa queste stesse parole in S-1.

## 4. Scostamenti e cose da segnalare

1. **Avaria «0,1–0,4 s».** La consegna lo chiede, ma la frase viene dal verdetto della fase 3 (V-2). Il verdetto
   finale dice «entro 1 s». Ho usato **«entro 1 s»**, perché la regola è «cifre solo dal verdetto finale».
2. **Correzione F7r.** `05-scorta/correzione_f7r/` (addendum 19) non è considerata dal verdetto, quindi nemmeno qui.
   Se migliora l'avviso col radar accecato, servono una riga nuova in § 4 e un rigo in § 9 della proposta, e
   l'aggiornamento del § 12.3 dello stato.
3. **Documento tecnico v3 e video.** Lo stato li cita come da fare o in corso, e non li ho verificati.
   - La durata del video **non è verificata**. Il vincolo dell'utente (≤ 176,0 s, con ffprobe sul file finale) è
     scritto in testa allo stato e nel § 12.8.
4. **`imhof1961` e `ruben1962`.** Non sono nell'elenco dei riferimenti. La testa f20 dice di toglierle dai testi o di
   segnarle «non verificata». Non ho cercato dove compaiono.
5. **Ripetizione nel registro.** Nel registro dello stato c'erano già le righe «5» e «5 (a)», per la versione 4.1. La
   mia è «5 (b), titolo "Versione 5"».
6. **Bibliografia del documento tecnico.** Alcune voci nuove sono verificate solo nei metadati o nel riassunto
   (blom1988, mazor1998, li2003, sim2023, choi2021, coluccia2020), e lo dice la loro riga «Verifica». Nella proposta
   cito come analogia solo sim2023 e choi2021.

## 5. Stati che propongo

Nessuno nuovo. La proposta non rafforza nessuna classe del verdetto. Ho reso più deboli due formule:
- «regione mantenuta … 60 su 60 per cella simulata», invece di «sempre»;
- «tarata su traiettorie pubbliche con sensore simulato».

## 6. Dopo

1. Una lettura da commissario (`sciame-lettore-critico`) del PDF v3.0, che lo confronti con il verdetto riga per
   riga.
2. Integrare l'esito di `correzione_f7r` se arriva entro le 10:45.
3. Nel video:
   - usare le voci s5, s7 ed F7 del verdetto § 8;
   - misurare la durata con ffprobe e verificare che resti ≤ 176,0 s.
