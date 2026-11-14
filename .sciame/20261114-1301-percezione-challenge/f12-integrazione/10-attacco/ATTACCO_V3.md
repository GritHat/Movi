# Attacco alla soluzione versione 3 come insieme — f12, `10-attacco` (`sciame-avversario`)

14 novembre 2026, 18:09–18:21 (`date -Is`), sui 35 minuti concessi. Accanto: `PREVISIONI.md` (P1–P9 alle 18:11:26, prima di aprire il codice; P10–P12 aggiunte dopo, ciascuna prima della sua prova), `a_libero.py`, `a_coperto.py`, `a_c7_fantasmi.py`, `rifai.sh` (circa 4 minuti), `ris/` (ogni numero qui sotto viene da lì), `libero_rifatto/` e `insieme_rifatto/` (copie dei due banchi di f12, impronte in `ris/IMPRONTE.txt`). **Tutto è simulazione su camera ideale o su profondità simulata da scheda: niente è «validato».**

## 0. In testa

**Cambi di stato proposti** (prove mie, dichiarate nel §1).
1. Regola del «libero» scritta nel §1.2 della versione 3 (un pixel dell'impronta; ripiego `stato` a 0,20 m): **controesempio in simulazione**, rifatto su semi miei. Va sostituita.
2. «Posa entro 1°» (§1.1, §1.9): **controesempio in simulazione** anche per la regola prudente `nuvole-1`.
3. Ripiego del riaggancio a 0,40 m (§1.8, «finché C-C non è passata»): **controesempio in simulazione** contro l'estraneo, su semi miei. Con c1 o senza, l'avviso cade senza aver visto.
4. «100 % degli istanti dentro l'area d'avviso» (§7, punto 4): **per costruzione, non misura il sistema**.
5. Ramo «ritorno dopo affidabilità persa» (§1.9), letto con le parole della versione 3: **controesempio per conto**.
6. c7 con i parametri del nucleo su profondità realistica: **controesempio** sulle uscite di f10 (avvisi che nessuna regola spegne).

**Scostamenti e regole.** Previsioni non cieche: avevo letto il contratto, la versione 3, `PROVA_INSIEME.md` e `LIBERO_DELLA_CELLA.md`. Non ho lanciato i `rifai.sh` nelle cartelle altrui (scrivono lì): ho copiato i banchi nella mia. Il banco del «libero» è rifatto per intero (riepilogo sui semi originali **identico**, `cmp`); del banco d'insieme ho lanciato 17 lanci su semi miei (`seme=31000000000`), non i 75. Per circa un minuto tre processi leggeri insieme (un filo e meno di 20 MB l'uno). **Tre mie previsioni sono smentite** (P3, P8, e la grandezza di P4) e una mia misura era costruita male (palo verticale: 4 settori su 5 non lo contengono; scartata). Letti per intero: contratto d'integrazione, versione 3, `PROVA_INSIEME.md`, `LIBERO_DELLA_CELLA.md`; del verdetto sui dati i §0–3, 5, 6; di `SCHERMO_E_DEMO.md`, della catena f10, di `TABELLA_CORREZIONI.md` e di `IDENTITA_SU_PROFONDITA.md` (comparso alle 18:18) le parti cercate. **Non letti:** VN, V7, V8, V9, audit, specializzazione, contratto e addendum della convocazione, `STATO_PROGETTO.md`, `RIFERIMENTI.md`. In `07-controprova-identita/` alle 18:20 c'è il lavoro in corso ma non `CONTROPROVA_IDENTITA.md`: **controprova sull'identità non ancora consegnata**. Niente git, sudo, rete; scritture solo in `10-attacco/`.

**Indipendenza.** Uso il codice dei due banchi di f12 (camera ideale, generatore dei camminatori, regole): miei sono i casi, i semi e i conteggi. Un errore dentro quei banchi passa intatto.

## 1. Attacchi: previsione, caso, esito

| # | Attacco e caso | Previsione (scritta prima) | Esito ottenuto | Stato |
|---|---|---|---|---|
| P1 | Il «libero» del §1.2 è la regola che `03-libero` rompe. Banco rifatto, semi `avv`, 7200 fotogrammi | violazioni > 0 | un pixel: **123 fotogrammi su 7200** con una cella libera dentro un corpo; col corpo che non rimanda segnale **900 su 900**. Ripiego a 0,20 m: **1730 su 7200** (15 629 celle). `nuvole-1`: 0 su 7200, 0 su 900, 0 su 900 | **rompe** |
| P2 | Tolleranza di posa 1° contro il dominio di `nuvole-1` (0,5°) | almeno 1 cella | a −1° la scatola di 10 cm a 2,6–2,9 m è «libero» in **146 fotogrammi su 300** (407 celle dentro il corpo, 256 di suolo nascosto); sulle 16 combinazioni 0 su 4800 | **rompe** |
| P3 | Anello cieco: oggetto alto 0,35 m a 0,75–1,05 m | non visto, d = 3,0 m | **smentita**: visto in 150 settori-fotogramma su 150, d = 1,3 m («sconosciuto»). *Notato dopo:* alto 0,35 m a 0,50–0,80 m, o 0,60 m a 0,30–0,60 m: 0 pixel sull'oggetto, e il settore dice **d = 3,0 m** (mediana; 600 su 600 oltre l'oggetto) | non rompe la regola; **rompe la frase** (W3) |
| P4 | Barra orizzontale di 1 cm a quota 0,8 m, a 2,0 m | ≥ 30 % (k 0,010), ≥ 10 % (k 0,004) dei settori-fotogramma con d oltre la barra | **7, 9, 10, 11 su 150** (4,7–7,3 %); per azimut la barra è «occupato» solo in 245–415 casi su 750. Con 2 cm o più: 0 su 150. Grandezza prevista **smentita** | rompe **debolmente**; camera ideale, sul vero non verificato |
| P5 | Ripiego N-C1 (0,40 m) con l'estraneo; n = 2000 per comportamento, geometrie D / T / L | identità sbagliata ≥ 40 % | **1445/3039 = 0,475 · 2594/3620 = 0,717 · 2361/3508 = 0,673**; col soggetto ancora tutto nascosto: 1025 · 2070 · 2146. Con c1: 0,991 · 0,964 · 0,911 | **rompe** (conferma su semi nuovi) |
| P6 | La catena f10 contraddice la versione 3 | almeno 4 righe | 8 righe (§3) | **rompe** |
| P7 | Rilascio «cella per cella oltre la fascia» a occlusore fermo (pannello 1 m a 1,8 m) | 0 celle rilasciabili | cuneo 396 celle, R100 808; libere ora 353, tutte nella fascia; **rilasciabili 0** | per costruzione: a occlusore fermo l'avviso finisce **solo** col riaggancio |
| P8 | «0 nascosti fuori da R100» è una tautologia; ombra stimata più stretta di 0,10 / 0,20 / 0,45 / 0,60 m (T, 2000 passaggi l'una) | > 0 fuori a −0,45 m | **smentita nel numero**: 0 / 0 / 0 / 3 istanti fuori su 110 867. *Notato dopo:* la cifra resta 0 finché l'errore non supera fascia più mezzo corpo; intanto i passaggi **scoperti** (avviso spento) sono **2 / 15 / 1704 / 1979 su 2000** | la cifra non vede il guasto: **denominatore comodo** |
| P9 | Formula della fascia (ultima riga di 1.7) contro il parametro | 0,83 m contro 0,40 m | 0,20 + 0,225 + 1,4 × (0,133 + 0,155) = **0,83 m** (0,64 m con età 0; l'età è una mia lettura) | le due righe non stanno insieme |
| P10 | Sensore coperto 2 s, la persona va dietro il pannello; «regione ∩ non osservato» | lettura letterale: fuori | persona nella regione al ritorno: **0 istanti su 13** (la sua cella è «in ombra», non «non osservato»); con «∩ non visto libero»: 13 su 13 | **rompe il testo** |
| P11 | c7 contro i fantasmi (F-403): uscite di f10, 36 sequenze nominali col pannello, parametri del nucleo | mediana ≥ 3 | tracce finite entro 0,75 m da un'ombra: **mediana 20 per sequenza di 3 s** (da 1 a 42; 36 su 36); strati già pendenti alla fine: mediana 12 | **rompe**: avvisi che non si spengono più (P7) |
| P12 | Limite di 0,3 m/s contro chi parte da fermo (D, T; n = 800) | < 0,90 a 1 s | c5 scritta: **0,756 · 0,710** a 1 s. «Fermo negli ultimi 2 s»: 1,000 a corpo tutto nascosto (n = 290, 333) ma **0,832 · 0,818** su tutti gli istanti col centro nascosto (n = 774, 776) | **rompe**; il «256 su 256» di `PROVA_INSIEME` vale col solo denominatore stretto |

**Sessione (D, 120 passaggi di fila, semi miei).** Dal passaggio 47 resta una traccia pendente nella stessa ombra, e i **47 riagganci su 47** successivi danno l'identità con due pendenti: il §1.8 (c2, «la più recente») fa ciò che il §1.4 vieta («con due tracce pendenti non si dà mai»).

**A ragionamento, non eseguito.** (R1) Chi entra dal bordo del campo già tagliato dall'ostacolo non fa mai nascere una traccia (§1.3) e va in ombra senza avviso: il settore dice comunque «zona non verificata», quindi nessun «libero» falso, ma nessuna «possibile presenza». (R2) Dopo un'affidabilità persa di T secondi chiunque può essere entrato in un'ombra: la regola «ombra in cui non è entrato nessuno: mai avviso» non lo sa. (R3) La riga «suolo visto libero fino a d ← solo celle libero fino a d» (§1.10), alla lettera, non esce mai: sotto 1,24 m nessuna cella è «libero».

**Dove ho cercato senza rompere.** C6 contro c1 sul percorso: nessun caso mio (resta lo 0,996 / 0,999 / 0,972 di `PROVA_INSIEME`). Oggetto nell'anello cieco che entra nel campo (P3 previsto, e un corpo alto 1 m a 0,1–0,3 m): visto, 750 azimut su 750. Barre da 2 cm in su: viste. Palo verticale di 2 cm a 2,5 m: visto nel suo settore (30 fotogrammi su 30 a k 0,004). `nuvole-1` entro ±0,5°: 0 violazioni su 9000 fotogrammi miei. Fascia di 0,20 m contro 0,40 m: nessuna contraddizione trovata (la prima sta dentro la seconda). «Libero» senza memoria contro il contatore di 3 fotogrammi del rilascio: non si contraddicono (il contatore non crea «libero»); il rilascio però è lettera morta (P7). Vetro, occlusore mobile, due soggetti visti insieme: non attaccati da me (limiti già dichiarati).

## 2. Le parole: frasi che un giurato legge come garanzia

- **W1, §7 punto 4:** «dentro l'area d'avviso nel 100 % degli istanti … nessun timer toglie l'avviso». Il 100 % è geometria (P8); con l'avviso davvero acceso gli scoperti sono 29 passaggi su 95 399 (`PROVA_INSIEME`), e l'avviso cade quando esce un altro (P5).
- **W2, `SCHERMO_E_DEMO.md` riga 27 e invariante I7:** «sparisce solo guardando, cella per cella». A occlusore fermo guardando non sparisce mai (P7; `IDENTITA_SU_PROFONDITA.md` §2.6: 140 passaggi su 140): sparisce per identità.
- **W3, `SCHERMO_E_DEMO.md` righe 37, 89, 111:** «NESSUN OSTACOLO OSSERVATO FINO A 2,7 m». È la dicitura che la versione 3 ha scartato (`sd-K2`). Casi: oggetto di 0,35 m a 0,5–0,8 m (P3), barra di 1 cm (P4), ostacolo sospeso (97,5 %, F-410). Anche «suolo visto libero fino a d m» tace che d parte da 1,3 m.
- **W4, §3 «frase della prova» e §7 punto 2:** «almeno 9 casi su 10 fino a 2 secondi». Nella geometria della demo, col corpo esteso, `PROVA_INSIEME` la dà **smentita**.
- **W5, §7 intestazione:** «entrando fra 0,3 e 1,8 m/s» fa credere coperto chi parte piano: a 1 s è 0,71–0,76 (P12).

## 3. La catena f10 contro la versione 3 (percorsi sotto `f10-dati/10-catena/`)

| Riga | Che cosa fa | Regola della versione 3 che contraddice |
|---|---|---|
| `parametri.py:32`, `mappa.py:119` | «libero» ricordato per 3 fotogrammi | §1.2, I1 |
| `parametri.py:29` e `:31` | tolleranza del suolo fissa a 5 cm; 3 punti assoluti | §1.2 (margine con la distanza; metà impronta) |
| `inseguimento.py:171–175`, `parametri.py:52` | stato «perso» a metà del cuneo | §1.5 («perso» non è uno stato), §1.6 |
| `inseguimento.py:155–156` | il riaggancio spegne lo strato | priorità 2 del contratto; F-409 |
| `inseguimento.py:183–184` | traccia non confermata scartata in silenzio | c7 (§1.5) |
| `presenza.py:76` | rilascia le celle del **nucleo** viste libere, senza «oltre la fascia»; a pannello fermo 18–38 celle per strato in 2 s (`d435i_nom__pannello_a12__s00`, fotogramma 40) | §1.7 |
| `inseguimento.py:198–200` | «affidabilità persa» è lo stato di una traccia, non del sistema | §1.9 (manca il blocco) |
| `presenza.py`, predittore | cerchio a velocità costante | §1.6 (già detto nel §6 della versione 3) |

## 4. Correzioni OBBLIGATE alla versione 3, in ordine (prima la sicurezza)

1. **L'avviso non deve cadere per sola identità** (§1.7, §1.8, I7). Controesempio: P5 (0,475–0,717 col ripiego, 0,911–0,991 con c1). La versione 3 deve scegliere e scriverlo: o l'avviso sopravvive al riaggancio (F-409, provata in `06-identita`: con due persone porta a 0 i fotogrammi nascosti fuori dall'avviso; costo: dietro un pannello fermo non si spegne più, 140 passaggi su 140), o I7 e la frase «finisce solo guardando» escono dal testo e dallo schermo. È la priorità 2 del contratto: senza decisione dell'utente vale la prima.
2. **§1.2: sostituire la regola del «libero» con `nuvole-1`** (metà impronta, una cella di guardia, margine con la distanza) e togliere il ripiego. Controesempio: P1.
3. **§1.1 e §1.9: tolleranza d'inclinazione 0,5°, non 1°**, più la prova d'ingresso (un oggetto di 10 cm a 2,5 m esce «occupato»). Controesempio: P2.
4. **§1.9: «∩ non visto libero»** al posto di «∩ non osservato». Controesempio: P10.
5. **§1.10 e schermo: una sola dicitura del livello più basso**, «suolo visto libero da 1,3 m a d m», «sconosciuto» se d = 1,3 m; mai «nessun ostacolo osservato». Controesempi: P3 (dopo), P4, F-410.
6. **c7 entra solo dopo la prova d'ingresso «0 tracce confermate in 30 s a pavimento vuoto»**; altrimenti resta spento e si dichiarano gli scoperti. Controesempio: P11.
7. **§7 punto 4 e I7:** al posto del «100 %», «avviso acceso: 29 passaggi scoperti su 95 399 con la maschera esatta; 15 su 2000 con l'ombra più stretta di 20 cm». Controesempio: P8.
8. **§3 e §7 punto 2:** in demo «almeno 88 su 100 a 1 s, poi "è ancora dietro"» (cifra di `PROVA_INSIEME`). Controesempio: W4.
9. **§1.6: c5 nella forma «fermo negli ultimi 2 s»**, con i due denominatori scritti. Controesempio: P12.
10. **§1.7: una sola fascia.** O 0,40 m «a margine zero», o la formula (0,64–0,83 m): oggi ci sono tutte e due. Controesempio: P9.
11. **§1.4 contro §1.8:** dire che con due pendenti l'identità è «la più recente (c2)» solo con un soggetto per ombra, o toglierla. Controesempio: sessione, 47 su 47.
12. **§6: le 8 righe del §3** entrano nell'elenco «da correggere» della catena prima che la squadra la riusi.

## 5. Che cosa resta aperto

- Due soggetti nella stessa ombra (K-016): identità sbagliata 12 volte su 12 anche con ogni correzione (`IDENTITA_SU_PROFONDITA.md`); nessuna regola la ripara.
- Identità al ritorno: **sostenuta in un dominio stretto**, con una correzione scelta dopo i dati; fuori cade (0 e 1 su 10 a 0,3 m dal pannello; 0 su 10 al rumore limite). Controprova **non consegnata**.
- Rilascio dell'avviso nella catena per sfarfallio del bordo (18–38 celle per strato): f10 conta 99 fotogrammi su 3038 col centro nascosto «in ombra senza avviso» (verdetto sui dati); che la causa sia questo rilascio è **non verificato**.
- Oggetti sottili e bassi sul sensore vero; R1 e R2; quale denominatore vale per chi parte da fermo; la decisione dell'utente al punto 1.
- Tutto ciò che è già aperto nel §5 della versione 3 (latenza, rumore, occlusore mobile, sensore in moto).

**Rifare:** `sh rifai.sh` in questa cartella (circa 4 minuti).
