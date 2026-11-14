# Verifica avversaria di `STATO_PROGETTO.md`, parte 3 di 3 — `sciame-validazione`, f11

**Oggetto.** `f11-documentazione/unione/STATO_PROGETTO.md` (1609 righe con `wc -l`, versione 1 delle 17:05:19), righe **1073–1609**: coda del cap. 7, cap. 8, 9, 10, glossario, registro, appendici A, B, C. Lavoro dalle 17:05:46 alle 17:20 circa del 14 novembre 2026 (`date -Is`). I percorsi sono relativi alla cartella della convocazione; «radice» è la radice del progetto.

## 0. In testa: cambi di stato, regole violate, limiti

- **Cambi di stato che propongo** (li decide l'arbitro). (1) «La traccia della challenge ha sei righe» (§8.1, e §1.2 che cita `CONTRATTO.md`): **smentito**, `wc -l` e `cat -A` su `regole_challenge.md` (radice) danno 5 righe, di cui una vuota. (2) «Le cifre di f6 portano "non vagliato dall'arbitro (f6)"» (legenda): **smentito** per il cap. 8, dove la marca non compare mai (righe 1078–1255: 0 occorrenze). (3) I controlli P2 e P3 dell'unione, rifatti da me con uno script mio sulla mia parte: **verificati** (121 percorsi completi su 121 esistono; 85 righe dell'appendice B su 85 tornano con l'elenco per numero di voce, stato e capitoli). (4) Il conto di [arch.] sull'altezza del pannello e quello di [dom.] sulla distanza protettiva a 2,0 m/s: **ricalcolati, tornano** nella stessa geometria ideale; restano non vagliati e non verificati sull'hardware.
- **Niente di ciò che ho controllato è provato sull'hardware.** Ho confrontato un testo con altri testi: le cifre tornano o non tornano *rispetto ai file dello sciame*, non rispetto al mondo.
- **Regole.** Nessun comando git (per questo «tre commit locali (15:57:51)» resta non verificato). La rete non è stata usata: **nessuna fonte esterna è stata riaperta**; le fonti sono controllate solo contro i file dello sciame e contro `f11-documentazione/unione/RIFERIMENTI.md`. Ho scritto solo in `f11-documentazione/verifica-3/` (`VERIFICA.md`, `stato.md`). Scostamento: le istruzioni di sessione chiedono di non scrivere file di rapporto; la consegna chiede questo file, e l'ho scritto.
- **Indipendenza.** Condivido con il documento il modello linguistico e i file dello sciame; non condivido l'autore né lo script di composizione. Vale per gli errori di trascrizione, di attribuzione e di stato; non vale per un errore che sta già nel file d'origine. Nessuna simulazione rieseguita; tre conti rifatti a mano o con Python (geometria della camera, distanza protettiva, altezza del pannello).
- **Previsioni** (scritte alle 17:05:46 in `verifica-3/stato.md`, prima dei controlli). P1 «almeno il 90 % delle cifre torna»: **regge** (circa 98 %). P2 «almeno 3 cifre sbagliate o assenti dal file citato»: **regge** (5). P3 «almeno uno stato più forte del file»: **regge** (§2). P4 «tutti i percorsi completi esistono»: **regge** (121 su 121).

## 1. (a) Cifre sbagliate

| # | Dove | Nel documento | Valore giusto e file |
|---|---|---|---|
| a1 | §8.1, riga 1086 (e §1.2, riga 107) | la traccia della challenge ha «sei righe» | **5 righe** (4 di testo e una vuota): `wc -l` = 5 su `regole_challenge.md` (radice, file delle 12:54, anteriore al contratto). Il «6» viene da `CONTRATTO.md`, riga 27, che sbaglia. Le «7 frasi, 156 parole» tornano (`wc -w` = 156) |
| a2 | §10.2, punto 1, riga 1355 | la durata del «previsto» va «da 0,40–0,53 s a 0,66–1,14 s» | l'estremo alto fra le sei cifre elencate nel §2.2, B5 è **«1–1,6 s»** (`f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md`, §2c). «Sei cifre in cinque file» torna. In più `f4/H-012/05-correzioni/SOLUZIONE_V2.md`, §6, scrive «le letture davano da 0,8 a 5,8 s»: non è fra le sei |
| a3 | Appendice B, riga 1495, [codice-strada-reg-art162] | link «**manca** nel file che lo cita» | il link c'è: `f9-preproposta/09-interfacce/CONSEGNA.md`, riga 80 (https://leggeinchiaro.it/articolo-162-regolamento-codice-strada/, non riaperto da me); lo porta anche la voce 164 dell'elenco |
| a4 | Appendice B, riga 1520, [lupu2020] | link «**manca**» | l'elenco, voce 57, dà https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7602506/ e il DOI 10.3390/s20205821 (non riaperti). Il capoverso «Che cosa manca» lo dice per il DOI, la riga della tabella no |
| a5 | Appendice B, «Che cosa manca», riga 1575 | senza verifica «i prezzi (tutti, salvo quello della Femto Bolt)»; «non hanno né chiave né verifica … la OAK-D Pro W, la camera Arducam» | `RIFERIMENTI.md`, §8.3: prezzi non verificati «salvo Femto Bolt a 418 $ in f3 **e Unitree L2 a 419 $** oggi»; le voci `luxonis-oak-d-pro-w` e `arducam-tof` **esistono**, con stato «non raggiungibili» |
| a6 | §8.9, riga 1247 | «`QUADRO_DOMINIO.md` §1 scrive "tramite la controllata CTMAVIO"» | nel §1 c'è «tramite CTMAVIO»; «preso tramite la controllata CTMAVIO» sta nel capoverso «In testa» dello stesso file |

Nessun'altra cifra della mia parte è diversa dal file citato.

## 2. (b) Affermazioni più forti di ciò che il file sostiene, con la riscrittura

1. **§8.3, titolo: «Tre pratiche consolidate usano il principio del nucleo».** Le prime due righe vengono da f6, che l'arbitro dichiara di non aver letto (`f4/H-012/09-arbitro/VERDETTO.md`, in testa: «`f6-specializzazione/` non letto»); la terza da f7 e f9 (**[prel.]**), con le norme ISO mai lette e C = 0,85 m da un riassunto di ricerca; ASTERIX è letto su una copia non ufficiale dell'edizione 1.18. *Riscrittura:* «Tre pratiche del dominio usano un principio analogo. Fonti: f6 (non vagliata dall'arbitro) e f7–f9 **[prel.]**; nessuna norma è stata letta sul testo ufficiale.»
2. **§10.1, riquadro 2: «Lo scioglie la misura sull'hardware … con i filtri spenti e accesi (condizione 1 del verdetto; previsione P13 di f10)».** `sensori-P13` (`f10-dati/02-sensori/PREVISIONI.md`, riga 43) è una prova **in simulazione** («catena del nucleo su profondità simulata, con e senza l'emulazione del filtro»); la condizione 1 del verdetto chiede i filtri spenti e l'autoverifica; la misura che decide è nel §3 del verdetto. *Riscrittura:* «Lo scioglie la misura sull'hardware del §3 del verdetto: pannello sul suolo segnato col nastro, 150 fotogrammi, celle "libero" dentro l'ombra vera (soglia 0) e banda non valida sui due lati. `sensori-P13` di f10 **[prel.]** è in simulazione: può dire solo se il meccanismo dei filtri esiste nel modello.»
3. **§8.2, riga «Alla perdita di affidabilità»: «0,13 s in simulazione».** Per il verdetto (§2, V3) C10 ha «prima e dopo solo nel simulatore dell'avversario» e non è stata riprovata nell'insieme; `SOLUZIONE_V2.md`, §7, aggiunge «rumore dell'IMU ipotizzato». *Riscrittura:* «0,13 s nel solo simulatore dell'avversario (C10; rumore dell'IMU ipotizzato; mai riprovata con le altre correzioni).»
4. **§8.5, C3, e §10.1, riquadro 3: «pannello a 1,15 m: 18 settori su 18 "sconosciuto"».** Vale con la possibile presenza accesa; spenta sono 12 su 18 (`f6-specializzazione/03-avversario/ATTACCO_SPECIALIZZAZIONE.md`, S1b; `risultati_spec2.txt`, righe 1–2). *Riscrittura:* «12 settori su 18 "sconosciuto", 18 su 18 con la possibile presenza accesa».
5. **§8.5, C7: «oltre 0,37 m/s "nessun ostacolo" a torto nell'1,0 % dei fotogrammi».** Il file (S6c) dà l'1,0 % con il suolo valido al 95 % e il **40,5 % con il 99 %**, in un modello a buchi indipendenti. *Riscrittura:* «1,0 % dei fotogrammi con suolo valido al 95 %, 40,5 % con il 99 % (modello a buchi indipendenti)».
6. **§8.5, C8: citazione fra «» accorciata.** Il file scrive «al chiuso **o all'ombra**, fino a 3 m, con la camera a 1,2 m: **a un'altra quota tutti i numeri cambiano**; il messaggio per l'autopilota è progetto, **non ancora simulato**». Fra «» va il testo del file, oppure si tolgono le virgolette.
7. **§8.1, riga «Non rileva oggetti estranei al suolo»: «dimostrato nella geometria della camera».** Lo stato è quello del ruolo (`f7-estensione/05-esperto-dominio/CONSEGNA.md`, §5), ma la riga non porta **[prel.]** e tace che i «5 pixel di lato» sono «criterio mio» dell'autore (C6). *Riscrittura:* «conto nella geometria della camera a foro (848 × 480, 87°), con il criterio di 5 pixel scelto dal ruolo; **[prel.]**».
8. **§8.3, [balch2019] «[A, A11]».** In f11 la fonte è stata aperta «solo per i dati bibliografici» (`f11-documentazione/sez-e/PREVISIONI.md`, «Consultazioni senza previsione»); la frase citata l'ha letta solo il ruolo di f9. *Riscrittura:* «[A] da f9; in f11 solo i dati bibliografici».
9. **§9.1, «Audit, verdetto, cancelli (f5)».** Il verdetto è in f4 (`f4/H-012/09-arbitro/`), i cancelli chiudono ogni fase. *Riscrittura:* «Audit (f5), verdetto (f4), cancelli».
10. **§8.2, in coda: «In due studi l'aptico costa più dell'audio».** Il documento lo segnala (riquadro 6, a), ma lascia la frase all'indicativo. Il file del curatore di f3, fase chiusa, già riporta per Martinez e altri «22 times higher cognitive load» senza dire di quale canale (`f3/fonti/FONTI_VERIFICATE.md`, riga 57); l'elenco dice che è il sonoro. *Riscrittura:* «due studi discordi ([martinez2014], [lupu2020]); non decide».

## 3. (c) Cifre senza file, o con un file che non le contiene

| # | Cifra | Che cosa ho trovato |
|---|---|---|
| c1 | §8.2: a 3 m si vede fino a «1,95» m con la camera a 1,2 m | non è in `ATTACCO_SPECIALIZZAZIONE.md`, S7; è in `f6-specializzazione/03-avversario/risultati_spec.txt`, riga 40 (e in `f7-estensione/10-triage/TRIAGE.md`, F-108). Ricalcolata: 1,2 + 3·tan 14° = 1,948 m; suolo da 1,243 m; a 0,25 m: 0,998 m e 0,259 m. Torna |
| c2 | §8.8, tappa 4: «le prove 2 e 3 indossando il sensore, poi la 1 in cammino» | **non è** in `f6-specializzazione/02-slam/MOTO_PROPRIO.md` §2d, §3 (né altrove nel file): è una proposta dell'autore della sezione. Va marcata [dom.], o tolta |
| c3 | §8.3, riga 1: «funzione solo orizzontale» | non è in `QUADRO_DOMINIO.md` né nell'esito E2 di `sez-e/PREVISIONI.md`; sta in `f7-estensione/05-esperto-dominio/CONSEGNA.md`, C8, **[prel.]** |
| c4 | §8.3, riga 1: «oltre 0,5 s un avviso» | `QUADRO_DOMINIO.md` §2e scrive «azzera i comandi orizzontali»; «avviso» viene da `f11-documentazione/sez-e/PREVISIONI.md`, E2. Il file va indicato |
| c5 | §8.3, riga 2: I062/290, I062/500 | non in `QUADRO_DOMINIO.md`; in `f8-continuita/07-ricercatore/FONTI.md` (riga 76), nel suo `PREVISIONI.md` (riga 69) e in `sez-e/PREVISIONI.md`, E4. Il documento non dà il file |
| c6 | §8.3, riga 2: «the target's last position should be clearly indicated» | `f8-continuita/07-ricercatore/FONTI.md`, riga 84. Il documento non dà il file |
| c7 | §8.3: 3,26 e 1,86 m con v_H = 2,0 m/s | `f11-documentazione/sez-e/PREVISIONI.md`, ultimo capoverso («notato dopo»). Ricalcolati: 2,0·1,155 + 0,95 = 3,26; 2,0·0,455 + 0,95 = 1,86. Tornano anche 2,80, 1,68 e 1,44 m/s. Che la norma raccomandi 2,0 m/s: **non verificato** (fonte non riaperta) |
| c8 | §9.2: «Tre commit locali (15:57:51)» | fonte `git log`: **non verificato** (git vietato). Il contesto di questa sessione elenca quattro commit; il quarto è «Verdetto sulle strategie della preproposta esterna (estensione f9)», quindi posteriore alla fotografia |
| c9 | §10.2, coda: «20 ms contro circa 161 ms» | i 20 ms sono in `SOLUZIONE_V2.md`, B2; i 161 ms **non li ho ritrovati** con `grep` nelle consegne di f9: non controllata (la cifra appartiene al §6.2, parte 2) |
| c10 | §8.6: «entro 24 mesi», «diritto di salire al 51 %» | `QUADRO_DOMINIO.md` §1: «opzione per il 51 %»; «entro 24 mesi» e «diritto di salire» vengono da `sez-e/PREVISIONI.md`, E9, letti con lo strumento che riassume; l'elenco li contesta. Già dichiarato nel riquadro 6, g |

## 4. (d) Contraddizioni interne al documento

1. **Legenda contro cap. 8.** La legenda promette che le cifre di f6 portino «non vagliato dall'arbitro (f6)». Nel cap. 8 (tabelle dei §8.2, §8.5, §8.8, tutte da f6) la marca non c'è mai; compare solo nel §10.1, riquadri 3 e 5.
2. **Regole comuni: due elenchi diversi nello stesso paragrafo (§8.2), non segnalati nel §8.9.** «Regole identiche 4 su 9» sono la 3, 6, 7, 9 (`SPECIALIZZAZIONE.md`, allegato B; `ATTACCO_SPECIALIZZAZIONE.md`, S2). «Ciò che è comune davvero» per l'audit e per il verdetto sono gli invarianti **2, 3, 5, 9** (`f5/02-audit/AUDIT.md`, 12; `VERDETTO.md`, §4); l'audit mette l'1, il 4, il 6 e il 7 fra quelli provati «per costruzione» solo con la griglia uguale al mondo. In comune restano la 3 e la 9. La prima riga della tabella dà per «comune» anche «la possibile presenza finisce solo guardando», che è l'invariante 7. Va aggiunta una riga al §8.9; la scioglie l'arbitro.
3. **§8.4 e §8.6: «Nessuna di queste fonti è passata dal curatore»** contro l'appendice B, dove delle 21 chiavi del §8.4 otto sono «verificata» e sei «verificata in parte», e delle 8 del §8.6 sette sono «verificata» (conteggio mio sulle righe dell'appendice). *Riscrittura:* «Nessuna era passata dal curatore di f3; i curatori di f11 ne hanno poi verificate alcune (appendice B), con i limiti scritti nell'elenco, che non è ancora verificato».
4. **§10.2, punto 1** contro §2.2, B5: vedi a2.
5. **§8.1 «sei righe»** contro il file: vedi a1.
6. **Appendice B, colonna dei link e capoverso «Che cosa manca»** contro l'elenco: vedi a3, a4, a5.
7. **§9.2.** La riga «14:06–14:56» precede la riga «14:40–14:55»: la tabella non è in ordine d'inizio. Per l'audit il §4.1.7 dà 14:39–14:50, il §9.2 «14:40–14:55» insieme alla riprova (file: 14:46:56, 14:47:28, 14:55:23). Non cambia niente.
8. **Fuori dalla mia parte, segnalo:** il riquadro in testa (riga 20) riporta dal verdetto di f9 «F-301…F-311, K-301…K-309»; il file chiuso scrive «F-301…F-309, K-301…K-308» (`f9-preproposta/13-verdetto/VERDETTO_PREPROPOSTA.md`, «Cambi di stato»).

## 5. (e) Ciò che manca di importante nella mia parte

1. **f6 non è passata dall'arbitro**, e il cap. 8 non lo dice (d1). Riguarda quasi tutte le cifre dei §8.2, §8.5, §8.8.
2. **§8.2, «ciò che è comune davvero».** Manca la voce dell'audit ripresa dal verdetto (§4): il rilascio «mai» dello strato 1 vale a sensore fermo; in moto la parallasse scopre l'ombra, e gli invarianti 1, 4, 6, 7 sono provati per costruzione solo con la griglia uguale al mondo.
3. **§8.7, frase «Un limite».** La condizione 7 del verdetto chiede cinque limiti scritti: rilevamenti mancati vicino all'ombra, secondo soggetto, vetro, **ostacoli bassi sotto 1,09 m**, **sole**. La frase ha il vetro e «al chiuso»; la frase «Una prova» copre i primi due; gli ostacoli bassi mancano (il v0.6 li ha: `proposta/proposta_sciame.tex`, riga 190). Di C8 mancano «a un'altra quota tutti i numeri cambiano» e «il messaggio per l'autopilota non è ancora simulato».
4. **§8.5, parti di correzioni obbligate lasciate fuori.** C2: il limite da scrivere («ciò che è più basso di 0,4–0,7 m e più vicino di 0,8–0,5 m non è visto») e «come un autopilota tratti ciò che sta sotto 1,24 m: non verificato». C3: l'alternativa ammessa (dichiarare «sconosciuto» su tutti i settori durante l'occlusione). C4: la seconda formula («"nessun ostacolo" non oltre la portata meno velocità massima × (età + latenza)») e la sua cifra: per chi entra a 2,5 m/s «fino a 3 m» è onesto solo fino a 2,28 m. C6: come si mostra (persona bendata ferma accanto al treppiede).
5. **§8.5, C4.** I 2,31 m e i 5,48 m dipendono da velocità di classe non verificate (mezzo a 8 m/s: «NV» in `SPECIALIZZAZIONE.md` §3.3; drone a 19 m/s da guide secondarie; l'elenco, §8.4, mette «il mezzo di piazzale a 5–8 m/s» fra le cifre senza fonte). Va detto accanto alle cifre.
6. **§10.1, riquadro 3.** Non dice che il v0.6 scrive già la combinazione contestata: «pannello alto almeno 1,5 m e largo 1 m, a 1,7–1,9 m dal sensore» (`proposta/proposta_sciame.tex`, riga 160). Con il conto di [arch.], rifatto da me nella stessa geometria ideale, a 1,7 m servono 1,62 m e a 1,9 m 1,67 m; sopra un pannello di 1,5 m la camera vede, a 2,3 m, ciò che supera 1,56–1,61 m. È un conto non vagliato, ma tocca un testo già dato alla giuria.
7. **§9.1, «che cosa i file mostrano sul rispetto del metodo».** Mancano: il cancello di f3 è stato invalidato dal completamento del dossier e **riapprovato alle 15:05:21** (nota di `GATE_f3_H-012.json`; il primo, delle 14:18:59, è copiato in `f4/H-012/GATE_f3_H-012.primo.json.txt`); in f4 «nessun file PREVISIONI.md» (nota di `GATE_f4_H-012.json`: le previsioni stanno in testa ai file delle misure); le regole violate dichiarate (un `git status` dell'arbitro; nessuna previsione prima delle ricerche in `QUADRO_DOMINIO.md`). «C'è solo la consegna» per debugger e statistico è ambiguo: nelle due cartelle c'è solo `TASK.md`, cioè l'incarico, e nessun lavoro.
8. **§8.3, distanza protettiva.** Il documento non dice che 1,68 m è l'esito di una previsione mancata del ruolo (`esp9-P6`: «< 1,5 m»; `f9-preproposta/06-esperto-dominio/CONSEGNA.md`, §1), né che i 1,44 m/s contano 0,27 s di conferma.
9. **§8.8, tappa 6.** Manca il costo già misurato: «col rumore perde il 21,4 % del libero» (`f7-estensione/10-triage/TRIAGE.md`, V-002).
10. **Per la versione 2 (non è un errore della 1).** Il verdetto di f9 conferma ciò che il cap. 8 prende da `f9-preproposta/06-esperto-dominio/CONSEGNA.md` come **[prel.]**: S7 respinta come modulo, la probabilità d'intrusione respinta come criterio, «mai "minaccia"». La distanza protettiva (2,80 e 1,68 m) **non è nel verdetto** (0 occorrenze con `grep`): resta **[prel.]**.

## 6. (f) Quante cifre ho controllato, e quante tornano

Conteggio a mano, per paragrafo; conta una cifra, una numerosità, un orario o un numero di riga. Tolleranza del conteggio: circa ±10.

| Parte | Controllate | Tornano nel file citato | Note |
|---|---|---|---|
| Coda del cap. 7, testa del cap. 8 | 7 | 7 | |
| §8.1 | 31 | 30 | a1 |
| §8.2 | 29 | 28 | c1 (file accanto) |
| §8.3 | 28 | 28 | quattro senza file indicato (c3–c6) |
| §8.4 | 7 | 7 | rispetto ai file dello sciame; «35 s e oltre un chilometro» già contestato dall'elenco |
| §8.5 | 59 | 57 | b4, b5 (condizione omessa); i nove numeri di riga del sorgente v0.6 tornano tutti |
| §8.6 | 16 | 16 | rispetto a `QUADRO_DOMINIO.md` e a `sez-e/PREVISIONI.md`; 0 occorrenze della società nel sorgente: ricontato |
| §8.7 | 13 | 13 | |
| §8.8 | 49 | 48 | c2 |
| §8.9 | 10 | 10 | a6 è sul paragrafo citato, non sulla cifra |
| §9.1 | 20 | 20 | 20 / 8 / 12 ricontati su `f2/03-triage/TRIAGE.md`; 124 minuti = 13:01:29 → 15:05:21 |
| §9.2 | 26 | 24 | c8 (due non verificate) |
| §10.1 | 48 | 48 | i quindici punti del riquadro 6 corrispondono all'elenco, numero per numero |
| §10.2 | 24 | 22 | a2; c9 non controllata |
| Glossario | 23 | 23 | |
| Appendice C | 30 | 30 | 5906 / 675; 24 = 3 + 1 + 2 + 15 + 3; 209 = 196 + 13; 35 173 parole nelle sei sezioni |
| **Totale** | **circa 420** | **circa 411 (98 %)** | 2 sbagliate, 2 fuori dal file citato, 2 con condizione omessa, 3 non verificate |

Controlli meccanici a parte, con uno script mio: **appendice B**, 85 righe, per ognuna numero della voce, stato e capitoli che la citano: 255 su 255 tornano con `RIFERIMENTI.md` (290 voci contate; 90 chiavi provvisorie contate nel suo §7); due link dati per mancanti esistono (a3, a4). **Appendice A e testo**, 121 percorsi completi: esistono tutti; 32 nomi senza cartella cercati a mano: esistono tutti. Le frasi fra «» delle fonti esterne **non sono state ricontrollate sulle fonti**.

## 7. Stati che propongo

| Enunciato | Stato | Prova |
|---|---|---|
| La traccia della challenge non nomina uncrewed, drone, UAV, veicolo, volo, 3D, voxel, autopilot, unmanned, pilot | **verificato** (ricerca esaustiva su tutto il testo, dieci radici, 0 occorrenze; rifatto da me) | `grep -oi` su `regole_challenge.md` |
| La traccia della challenge ha sei righe | **smentito** (5) | `wc -l`, `cat -A` |
| Appendice B allineata all'elenco | **verificato** su 85 righe per numero, stato e capitoli; due link da correggere | script mio; condivide i due file |
| Percorsi citati nella mia parte | **verificato**: 121 su 121 | script mio |
| Altezza del pannello ≥ 1,2 m + distanza × tan 14° | conto che torna nella geometria ideale (58° verticali, 15°, 1,2 m); **non vagliato, non verificato fino all'hardware** | ricalcolo mio; stesse ipotesi di [arch.] |
| Distanza protettiva 3,26 e 1,86 m a 2,0 m/s | conto che torna; la premessa (2,0 m/s raccomandati) **non verificata** | ricalcolo mio |
| «Tre commit locali (15:57:51)» | **non verificato** | lo decide `git log`, che la consegna vieta |
| Regole comuni ai due profili: 3-6-7-9 oppure 2-3-5-9 | **non risolto**: due file dicono cose diverse | lo decide l'arbitro leggendo f6 |

## 8. Proposte

- **`validazione-f11v3-1` — due controlli meccanici a ogni versione.** *Meccanismo:* uno script confronta ogni riga dell'appendice B con l'elenco (numero, stato, link) e verifica l'esistenza di ogni percorso fra apici. *Previsione:* sulla versione 2, 0 scarti su numero e stato e 0 percorsi mancanti. *La smentisce* uno scarto. Oggi: 0 e 0, più due link.
- **`validazione-f11v3-2` — la marca di f6 dove serve.** *Meccanismo:* una riga in testa al cap. 8 e la marca nelle tre tabelle da f6. *Previsione:* dopo la correzione `grep` trova la marca almeno una volta in ciascuno dei §8.2, §8.5, §8.8. *La smentisce* un paragrafo senza marca.
- **`validazione-f11v3-3` — una riga nuova nel §8.9** sulla discordanza 3-6-7-9 contro 2-3-5-9, con la domanda per l'arbitro: «l'invariante 7 è comune ai profili o vale solo a sensore fermo?». *La decide* la lettura di f6 da parte dell'arbitro.

## 9. Che cosa propongo dopo

1. Correggere a1–a6 e applicare le riscritture b1–b10: sono tutte di testo, nessuna cambia un risultato.
2. Aggiungere le righe mancanti e1–e9; e6 va portato anche a chi tiene il PDF, perché tocca una frase del v0.6.
3. Far decidere all'arbitro d2 insieme ai sei punti «da sciogliere».
4. Alla versione 2: integrare il verdetto di f9 (e10), verificare il conto dei commit con `git log`, ricontrollare sul testo grezzo le frasi fra «» del cap. 8, che oggi vengono tutte da uno strumento che riassume.
