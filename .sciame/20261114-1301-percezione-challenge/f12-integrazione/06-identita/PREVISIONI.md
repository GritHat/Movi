# PREVISIONI — f12, 06-identita (`sciame-tracciamento`)

Scritte alle **2026-11-14T17:56:12+01:00** (`date -Is`), dopo aver letto verdetti, catena, simulatore e le tabelle di taratura di f10
(`20-validazione/uscite/taratura_*.txt`: soglia 20 → scatola 10/10 e continuità 0/15; soglia 40 → continuità 13–15/15 e
scatola 3/10), **prima** di eseguire qualunque corsa mia. Tutto è simulazione.

## Criterio (dal verdetto dei dati, §6; non lo scelgo io)
- **C-A** continuità dell'identità («continuita_pulita» di `misura_passaggi.py`: stessa identità prima e dopo, mai
  «osservato» a soggetto nascosto, nessun riaggancio a soggetto nascosto) **≥ 28 passaggi su 30 per caso** (a12, a05, b).
- **C-B** scatola di 15 cm a 2 m vista (cella «occupato» entro 15 cm dall'impronta) **≥ 9 fotogrammi su 10**.
- Passa solo se C-A **e** C-B, **alle due risoluzioni** (424×240 e 848×480) con **gli stessi parametri**.
- Aggiunte: (C-C) 0 celle «libero» con il centro nell'ombra vera; (C-D) 0 tracce confermate sul pavimento vuoto;
  (C-E) pannello «in movimento» ≤ 1 passaggio su 30; (C-F) persona nascosta fuori dall'avviso: 0 fotogrammi nel caso
  dell'estraneo, ≤ 3 % nei passaggi singoli; (C-G) costo medio ≤ 66 ms per ciclo (15 Hz), un filo.

## Valori fissati PRIMA (non taratura)
- Soglia di cella: `N_cella(r) = max(3, ceil(fx·fy·Δaz·h_rif / r))`, **h_rif = 0,05 m** (una superficie verticale alta
  5 cm larga una cella): a 424 px (fx = 212) vale 19,6 a 2 m; a 848 px 78. Scelta guidata dalla tabella di f10
  (20 teneva la scatola): quindi **informata dai semi s00–s29**; conta come taratura su quei semi.
- Soglia di gruppo: `N_gruppo(r) = fx·fy·A_rif / r²`, **A_rif = 0,004 m²** (45 punti a 2 m a 424 px).
- Riaggancio: rifiuta gruppo tagliato da un'ombra, gruppo che tocca il bordo del campo (azimut o portata) e gruppo che
  dà il primo ritorno su un azimut del cuneo (l'occlusore). Dopo il riaggancio: filtro ripartito dalla misura,
  R gonfiato di (larghezza/2)²; le misure tagliate successive aggiornano con R gonfiato. Strato: resta («orfano»)
  finché le sue celle non sono viste libere 3 volte di fila.
- **Semi:** taratura = sequenze su disco (s00–s29). Prova finale = passaggi **k = 100…129** (mai generati da nessuno),
  generati in memoria; la cifra finale si riporta **solo** su quelli. Ogni valore cambiato dopo aver visto una corsa
  va scritto qui sotto con l'ora, e allora la cifra a 424 su s00–s29 non vale più come prova.

## Previsioni (misura; soglia di smentita)
- **T1** «prima» (parametri del nucleo) su disco: continuità 0 su 90. Smentita: ≥ 1.
- **T2** solo F-401/F-412: continuità < 28/30 in ogni caso (a soglia 20 f10 dava 0/15), scatola ≥ 9/10, 0 tracce sul
  pavimento vuoto del D435i nominale. Smentita: un caso ≥ 28/30, o scatola < 9, o tracce > 0.
- **T3** solo F-402: continuità < 28/30 (la fusione resta). Smentita: un caso ≥ 28/30.
- **T4** solo F-408 e solo F-409: continuità 0 su 90 (non toccano l'identità). Smentita: ≥ 5 su 90.
- **T5** tutte insieme, semi nuovi, 424: C-A e C-B passano in a12; **credo al 50 %** che passino anche a05 e b
  (a05 a soglia 40 dava 11/15 e 13/15). Smentita di «passa»: un caso < 28/30.
- **T6** tutte insieme, 848×480, stessi parametri: stessa cifra di T5 entro ±3 passaggi su 30 per caso. Smentita:
  differenza maggiore (allora la regola non è davvero proporzionale).
- **T7** estraneo (scena A3 dell'avversario e varianti): con tutte le correzioni l'identità di A passa ancora a B
  (la geometria non distingue due persone nella stessa ombra): identità sbagliate = tutte le varianti; ma A nascosta
  fuori dall'avviso: 0 fotogrammi con F-409 (25 senza). Smentita: identità giuste senza regola d'aspetto, o > 0.
- **T8** 0 celle «libero» nell'ombra vera in ogni configurazione. Smentita: ≥ 1 cella·fotogramma.
- **T9** chi torna indietro (c): ≥ 3 su 4 su disco con tutte; chi si ferma (b): come T5. Smentita: ≤ 2 su 4.
- **T10** costo medio: < 10 ms a 424, < 40 ms a 848. Smentita: oltre.
- **T11** con F-409 l'avviso dietro un pannello fermo **non si spegne mai** dopo il passaggio (le celle in ombra non
  sono mai viste libere): 100 % dei passaggi finiscono con l'avviso acceso. È il costo dichiarato della correzione.

## Dopo (aggiunte con l'ora, mai riscrivendo sopra)

### 2026-11-14T18:02:15+01:00 — esito della prima corsa su disco (s00–s29, valori fissati prima) e una correzione NUOVA, scelta dopo i dati
- **Esito (prima di cambiare qualunque cosa):** T1 regge (0 su 90). T2 regge sulla continuità (0/30 in ogni caso) e
  sulla scatola (10/10), **ma T8 è smentita per F-401**: 7 celle·fotogramma «libero» nell'ombra vera della scatola
  (`risultati/disco.jsonl`, `d435i_nom__scatola15_2p0m`, conf f401 e tutte). T3 regge (0/90), T4 regge (0/90).
  «Tutte» con la soglia sui pixel attesi: a12 21/30, b 20/30, **a05 0/30** → C-A cade già sui semi di taratura.
- **Visto dopo** (`diag_celle.py`, due fotogrammi): le celle ponte fra pannello e persona hanno 33–125 punti, le celle
  della scatola a 2 m 13–43, le superfici piene 460–690. **Nessuna soglia per cella, assoluta o proporzionale ai pixel
  attesi, separa il ponte dalla scatola**: il ponte ha più punti dell'ostacolo basso.
- **Correzione nuova «tracciamento-1» (taratura dichiarata):** la mappa resta quella di f10 (soglia 3: sicurezza
  intatta per costruzione); i GRUPPI si formano solo con le celle che hanno almeno **ρ = 0,30** dei punti della cella
  più piena della loro componente connessa, e un gruppo vale se ha almeno fx·fy·A_rif/r² punti (A_rif = 0,004 m²,
  invariato). ρ = 0,30 è scelto DOPO aver visto i due fotogrammi sopra: è taratura sui semi su disco.
- **Previsioni per «tutte_p» (F-401 sostituita da tracciamento-1), scritte prima di eseguirla:** su disco a12 ≥ 28/30,
  a05 ≥ 25/30, b ≥ 27/30; «libero» nell'ombra vera identico a «prima» (0); scatola 10/10; 0 tracce confermate sul
  pavimento vuoto D435i nominale. Risoluzione: stessa cifra a 848 entro ±3 su 30 (la regola è un rapporto).
  La cifra finale si legge solo sui semi nuovi (k = 100…).

### 2026-11-14T18:03:40+01:00 — esito di «tutte_p» su disco e SECONDO ritocco (taratura dichiarata)
- **Esito:** la previsione per «tutte_p» è **smentita** sui semi di taratura: a12 12/30, a05 5/30, b 6/30
  (`risultati/disco_picco.jsonl`). Reggono: «libero» nell'ombra vera 0, scatola 10/10, pannello «si muove» 0/90,
  persona nascosta fuori dall'avviso 0/3038. Cadono: 4 tracce confermate sul pavimento vuoto (D435i) e la continuità.
- **Causa letta nei motivi degli eventi** (conteggio in IDENTITA_SU_PROFONDITA.md): «N tracce pendenti». La fusione è
  sparita, ma i fantasmi del pavimento (celle con 3–15 punti, mappa invariata) fanno gruppi, tracce e strati pendenti.
- **Ritocco:** nei GRUPPI (non nella mappa) una cella conta solo se supera ANCHE la soglia sui pixel attesi
  N_cella(r) con h_rif = 0,05 m (il valore fissato prima). Cioè: cella forte = n ≥ max(ρ·picco, N_cella(r)).
  Nessun numero nuovo; è una scelta di struttura fatta dopo aver visto i dati → taratura.
- **Previsione (prima di eseguirla):** su disco a12 ≥ 26/30, a05 ≥ 22/30, b ≥ 24/30; 0 tracce confermate sul pavimento
  vuoto D435i nominale; sicurezza identica a «prima». Se una cade non ritocco più: riporto la cifra sui semi nuovi.
- 2026-11-14T18:04:37+01:00: lancio dei semi nuovi (k = 100…), nessun ritocco dopo questo punto; b = 27/30 su disco resta com'è.

### 2026-11-14T18:07:47+01:00 — esito sui semi nuovi a 424 (letto ora) e una prova in più, scritta prima di eseguirla
- Semi nuovi, 424, «tutte_p»: a12 29/30, a05 29/30, b 30/30, c 20/20, D455 10/10, Gemini 10/10, limite 0/10; scatola
  100/100; 0 tracce sul pavimento vuoto nominale; 0 «libero» in ombra (`risultati/nuovi424.jsonl`). «Tutte» come
  proposta dai ruoli: a12 23/30, a05 0/30, b 21/30, e 35 celle·fotogramma «libero» nell'ombra della scatola.
- **Z1 (nuova, attacco A8 dell'avversario rifatto):** linea di cammino a 2,1 m invece di 2,3 (geometria mai usata per
  tarare), k = 100…109, 424 e 848. Previsione: «tutte_p» ≥ 8 su 10 fra i passaggi in cui la persona sparisce
  (a 2,1 m la testa può restare in vista: se nessun passaggio è «nascosto» la prova non decide). Smentita: ≤ 6 su 10.
- 848 in corso: T6 resta com'è (stessa cifra entro ±3 su 30).

### 2026-11-14T18:15:01+01:00 — esito di Z1 e TERZO ritocco (taratura dichiarata), con semi ancora nuovi
- **Z1 smentita:** a 2,1 m «tutte_p» dà 0/10 a 424 e 1/10 a 848 (`risultati/z21_*.jsonl`); «tutte» (soglia sui pixel
  attesi) dà 9/10 e 9/10. Semi nuovi a 848 (T6): «tutte_p» a12 30/30, a05 29/30, b 29/30 → T6 regge per «tutte_p»;
  per «tutte» no (a05 0/30 a 424 contro 16/30 a 848).
- **Causa letta in `diag_z21.py`** (k = 100): con i gruppi per picco la cella di confine del gruppo che riemerge cade
  fra le deboli, la marca «tagliato» non scatta, il riaggancio prende una scheggia di 2 celle (k = 26) e al fotogramma
  dopo persona e pannello (anelli adiacenti, 400–680 punti per cella: superfici piene, non pixel misti) sono un gruppo.
- **Ritocco «tracciamento-2»** (interruttore `tagliato_su_componente`): la marca «tagliato» scavalca fino a 2 celle
  deboli (occupate ma fuori dal gruppo) prima di cercare l'ombra di un altro. Nessun numero tarato sui passaggi.
- **Previsione (prima di eseguire):** «tutte_p2» su z21 k = 100…109 (già visti: taratura) ≥ 8/10; su semi MAI usati
  (k = 200…229) a12, a05, b ≥ 28/30 a 424 e a 848; z21 k = 200…209 ≥ 8/10 alle due risoluzioni. Smentita: uno sotto.
  Dopo questa corsa non tocco più niente.
- 2026-11-14T18:15:29+01:00: **«tracciamento-2» smentita già sui semi visti**: z21 k = 100…109, «tutte_p2» 0/10 a 424
  (`risultati/z21_424_p2.jsonl`; a 848 vedi `z21_848_p2.jsonl`). Non la provo sui semi k = 200… (i blocchi
  `ultimi424/848` restano in `prova.py`, mai eseguiti) e non ritocco altro. La configurazione finale resta «tutte_p».
