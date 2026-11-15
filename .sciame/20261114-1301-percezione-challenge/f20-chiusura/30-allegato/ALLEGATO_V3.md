# Documento tecnico v3 (f20-chiusura/30-allegato, `sciame-redattore`)

Lavoro fatto il 15-11-2026, dalle 06:34:58 alle 06:49 circa (`date -Is`).

## 0. In testa: regole e cambi di stato

**Regole.**
- **Violazione tentata e bloccata.** Ho scritto per errore un comando con `rm -f` su immagini di prova nello scratchpad
  (`pag/*.png`), che contraddice il divieto di cancellare file. Il sistema dei permessi l'ha negato e nessun file è
  stato cancellato. Le immagini nuove le ho messe in una cartella nuova (`pag3/`).
- Ho scritto solo in `allegato_tecnico/`, in questa cartella e nello scratchpad. Niente git, niente sudo, niente rete.
- Nessuna sovrascrittura senza copia.
  - La v2 intera (sorgenti, PDF, bib, log) è copiata in `allegato_tecnico/v2/`, che prima non esisteva.
  - I capitoli che ho modificato sul posto hanno anche una copia `*_v2.tex` in `capitoli/versioni_precedenti/`.
  - I capitoli 11 e 12 sono file nuovi, copiati dalla bozza `04-capitolo/`, che resta intatta.
- Il vincolo dell'utente sul video (durata non oltre 176 s) non tocca questo compito: non ho modificato nulla del
  video.

**Cambi di stato.** Nessuno di mio. Ho riportato gli stati del VERDETTO_FINALE (F-801…F-809) nel testo. I casi
principali:
- E1: 51/60 vale solo con l'integratore di Eulero; con quello stabile 48/60 e 3 eventi precoci, ed è un limite.
- La regola di contatto è provata e non adottata.
- La taratura è incoraggiante con condizioni; la virata è un limite.
- F7 e F7r come nel § 2.2 del verdetto.

## 1. Il documento

- **File:** `allegato_tecnico/allegato_tecnico.pdf`.
  - Pagine: **108** (la v2 ne aveva 84).
  - Titolo: «… dal corto raggio al volo ad alta velocità», «Documento tecnico, versione 3».
- **Compilazione** come la v2: `xelatex`, poi `bibtex`, poi `xelatex` due volte, ciascuno con `timeout`. Esito:
  - 0 errori;
  - **0 riferimenti indefiniti e 0 citazioni indefinite** (grep su «undefined» nel log: 0);
  - 0 overfull, 0 «Float too large» (la v2 aveva un «Float too large» di 3,4 pt);
  - 33 righe underfull, tutte nella bibliografia o nelle tabelle strette.
- **Indice controllato.**

  | Sezione | Pagina |
  |---|---|
  | § 10 Volo ad alta velocità | 73 |
  | § 10.7 «scorta» (F7) | 83 |
  | § 11 Limiti attuali e aree di miglioramento | 90 |
  | § 12 Conclusioni | 92 |
  | Appendice A | 95 |

- **Pagine guardate come immagini** (`scratchpad/pag3/`): 1, 5, 11, 84, 85, 86, 91 e 92 del file. Ho trovato e
  corretto un difetto: la tabella dei risultati del volo, con `[p]`, faceva slittare tutte e tre le tabelle di sintesi
  dell'introduzione dopo le conclusioni. Ora è `[!htbp]` e le tabelle sono alle pp. 10–12.

## 2. Capitoli cambiati

| File | Che cosa |
|---|---|
| `allegato_tecnico.tex` | titolo; inclusione di 11 e 12 dopo il 10 |
| `preambolo.tex` | pacchetto `longtable` |
| `00_sommario` | riscritto in testa: il caso centrale è il volo veloce, con V-1, V-6, la regola di contatto non adottata, F7 ed F7r, la formula di C(τ) e la taratura con le condizioni, l'hardware come ipotesi, «in un giorno». Il corto raggio e il sito sono gli altri usi; E1 è corretto |
| `00_simboli` | 14 simboli del volo (σ0v, σ_rif, C e C̃, k_α, r_α, t_C, μ_j, r0, V, Δv, v_t, L(τ), σ_vr, F1–F7, A e B) e 4 termini (portatore, mantenere la traccia, insieme di presenza in volo, classi) |
| `01_introduzione` | problema: il caso centrale è il volo, il sito e il corto raggio sono gli altri usi; contributi 9 e 10; nuova **Tabella 2**, sintesi del caso centrale con classe, intervallo e stato; righe del sito ed E1 corrette; riquadro «Dominio del volo»; ambiti; struttura |
| `08_limiti` | L5 con E1 corretto; nuova § «Limiti nel volo ad alta velocità» (V1–V6); nota sul sensore in moto, che rimanda a F7 |
| `09_conclusioni` | nuovo paragrafo sul caso centrale (dimostrato, solido, incoraggiante, limiti) con la frase «risultati incoraggianti… in un giorno… nessuno misurato su sensore fisico o hardware»; il sito ed E1 corretti |
| `10_lunga_portata` | «caso centrale» diventa «sito»; nota E1 con l'integratore stabile; L5 |
| `11_volo_alta_velocita` (nuovo) | dettagli sotto |
| `12_da_proposta_a_sistema` (nuovo) | frase sui risultati ottenuti in un giorno (senza «92–98»); la tabella § 5 del verdetto **per intero** (21 righe, longtable); il piano a tappe aggiornato; «che cosa resta fuori» con F7 |
| `B_riproducibilita` | paragrafo sulle prove di volo: programmi, 8 comandi, che cosa si rifà dal solo testo |
| `allegato.bib` | 17 voci di `nuove.bib` più `mphale2007` (F1 del rapporto F7r, riassunto letto); note ripulite da «curatore»; `#`, `&` e `~` corretti |

**Il capitolo 11 nel dettaglio.**
- Tutti i marcatori `%% MIGLIORIA` sono sciolti, e ne restano 0:
  - **E1**: paragrafo nuovo con 60/60, 48/60, 3/60 precoci e 57/60 entro 2,5 s (soglia notata dopo); il rifacimento
    non isola l'integratore;
  - **F3**: paragrafo «La regola di contatto provata, e non adottata», con la tabella delle varianti di ATTACCO § 1 e
    la frase V-11;
  - **taratura**: sottosezione nuova con l'equazione con σ_rif², i quattro punti, la tabella del § 4 e le tre
    condizioni (concentrazione su una rotta, virata L, pochi droni), più la frase IT e i «da non mostrare».
- La tavola dei risultati è sostituita con quella del § 2.1: V-11 con la regola in prova, V-13 come L ed S.
- La lettura ADS-B è riscritta come «prima della taratura»: niente «16 aerei» né «da 92 a 98»; ci sono 12 aerei ICAO
  e 4 numeri di volo.
- **Sottosezione F7 nuova** (pp. 83–89). Contiene:
  - il modello del portatore e della navigazione inerziale (ipotesi);
  - le configurazioni e il tracciatore, dichiarato componente nuovo;
  - la **Proposizione 10.10**: il cono orizzontale e il cammino massimo L(τ) con la resistenza, con la dimostrazione
    per confronto. L'ho scritta io dalle formule di SCORTA e va riletta da un formalista;
  - la tavola S-1…S-9;
  - la robustezza su semi nuovi;
  - la tabella fisica dei sensori nella collisione vicina (Mphale citata, F2 ed F3 non citate);
  - F7r con gli esiti di F-809 e la frase S-6r;
  - la curva C(τ) di F7;
  - cinque limiti: F-806, F-807, S-9, l'avviso non discriminante e il controllo debole (F-808).
- **Fonti:**
  - EchoShield: 10 Hz da stampa, campo 120×80° dal produttore, portate «non verificate»;
  - ASR: stone1989 più Wikipedia, 4,8 s calcolato;
  - torretta: scheda non aperta, «oltre 25 km» come dato del produttore su bersaglio grande;
  - Taalas: dato aziendale da prove interne, nessuna misura indipendente;
  - Cerebras: 1936 contro 1800;
  - CERN: latenza contro portata 4,5×, PCIe;
  - CFAR: sim2023 e choi2021;
  - FAA: AC 90-48E;
  - IMM: blom1988, mazor1998 e li2003;
  - OpenSky: schafer2014;
  - Imhof e Ruben tolti.
- `\sloppy` nel capitolo.

**Controlli sul testo del PDF** (`pdftotext`, grep).
- Nel PDF non compaiono più: «validat», «sotto il millisecondo», «certificab», «detect and avoid», «16 aerei»,
  «16 mezzi», «92 a 98», «3812» come distanza, «130×90», «14 357», DA_VERIFICARE, sciame, sigle interne (F-80x, K-7xx,
  K-8xx, V-n, S-n), «curatore», «arbitro», «fase».
- Restano, legittimi:
  - «tempo reale», solo in citazioni di letteratura della v2;
  - «inseguimento», come termine tecnico del tracciamento già nella v2; in F7 c'è «non insegue e non intercetta»;
  - «zona al 99 %», solo dentro la frase «non si mostrano»;
  - «v3i», solo nei comandi di riproducibilità (`VOLO_REGOLA=v3i`).

## 3. Avvisi residui

1. **Fonti verificate solo in parte.**
   - Per blom1988, mazor1998 e li2003 sono verificati solo i metadati.
   - sim2023, choi2021, coluccia2020 e mphale2007 sono stati letti solo nel riassunto. Le note bib lo dicono.
   - BibTeX dà 3 avvisi «empty year» (Wikipedia, pagina Echodyne, Ophir): le pagine non hanno data, e la data non è
     stata inventata.
2. **Non verificati** (lasciati come «non aperta» o «ipotesi» nel testo): la scheda CM202A, il ΔT della SupIR, le
   portate EchoShield e i 0,5 s dell'ADS-B.
3. **Cifre riprese senza riconto mio.**
   - Tutte vengono dal VERDETTO_FINALE, da SCORTA, da ACCECAMENTO_RADAR, da ATTACCO_FINALE e dalla bozza del capitolo.
   - Ho ricalcolato io solo i Wilson che il verdetto non dava: 19/55 [0,234; 0,477], 21/55 [0,265; 0,514],
     7/60 [0,058; 0,222], 7/20 [0,181; 0,567], 56/56 [0,936; 1].
4. **Riproducibilità.** Ho dato i nomi dei programmi senza i percorsi delle cartelle di lavoro, che contengono sigle
   interne. Chi rifà le prove deve sapere dove stanno. I comandi di `e1_stabile.py` e `prove_v5.py` hanno argomenti
   segnaposto (`<modo>`, `<classe> <uscita>`): **non verificati** contro i file d'avvio.
5. **Non considerati:**
   - `05-scorta/correzione_f7r/`, perché il verdetto lo esclude;
   - il confronto della curva F7 contro l'osservato in F7r (ACCECAMENTO § 2), che il verdetto non ha ricontato.
6. **Fuori dal compito, ancora da fare:**
   - `documentazione/RIFERIMENTI.md` (voci da [394] a [410]);
   - la proposta v3.0 di due pagine;
   - la voce del video (K-806).
7. **Altri residui.**
   - Restano 33 underfull, tutti di estetica.
   - La Proposizione 10.10 non ha un controllo numerico mio.
   - La dicitura «solido nel modello» per S-4 si appoggia su un simulatore che condivide il modello fisico.
