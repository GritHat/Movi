# Prova d'insieme della continuità visiva (controllo C-C) — `sciame-validazione`, f12

Lavoro dalle 17:47 alle 18:09 del 14 novembre 2026 (`date -Is`). **Tutto è simulazione su CPU, a sensore fermo: nessun fotogramma vero. Niente diventa «validato».** File, tutti in `f12-integrazione/02-prova-insieme/`: `PREVISIONI.md` (17:51:24, prima di compilare), `componi.py`, `insieme.c`, `DIFFERENZE.txt`, `rifai.sh`, `leggi.py`, `ris/TABELLE.txt` (ogni numero qui sotto viene da lì), `ris/<lancio>.txt` (75 lanci), `ris_prec_20261114T180057/` (primo giro). Tre numeri con «/» = geometrie D (demo, pannello 1 m) / T / L (pannello 2 m). «Sul percorso» = prosegue, rallenta, si ferma, torna, sosta lunga. «INS» = M1–M8 con c1, c2, c3 (forma simulabile), c4, c5, c7 insieme.

## 0. In testa

**Cambi di stato proposti.** (1) K-219, «c1 contro l'estraneo»: da aperta a **controesempio in simulazione**: con c1 l'estraneo prende l'identità del soggetto e l'avviso cade nel 0,995 / 0,966 / 0,913 dei casi (prima di c1: 0,481 / 0,711 / 0,676); c2 com'è scritta **non lo ripara**. (2) c7: da «non provata» a **sostenuta dai dati in simulazione**: i passaggi scoperti scendono da 928 a 24 su 23 402; **non a zero**. (3) Precisione «almeno 9 su 10 fino a 2 s»: **regge in T e L** (30 celle su 30), **cade in D** con il corpo esteso. (4) K-215: senza c3 **controesempio confermato** su semi nuovi (0,30–0,46 a 1 s); c3 lo ripara **solo se il bordo è riconosciuto a ogni ciclo** (con 8 cicli su 10: 0,74–0,76). (5) Chiusura «fuori dall'area osservata» che lascia l'avviso: da «mai eseguita» a **sostenuta dai dati in simulazione** (0 scoperti aggiunti; se lo togliesse: 271 / 268 / 340 passaggi scoperti). (6) K-218, identità al ritorno con C6 e c1: **regge** sul percorso (0,996 / 0,999 / 0,972).

**Scostamenti e regole.** (a) Il codice è **ricomposto, non riscritto**: `insieme.c` è `att.c` dell'avversario di f8 con 33 sostituzioni dichiarate (23 righe tolte, 68 messe, su 326: `DIFFERENZE.txt`, elenco in `ris/componi.txt`). (b) Le previsioni non sono cieche: avevo letto V8, le modifiche e le controprove. (c) Una prova di fumo su semi di sviluppo (5 000 000 000+, 100 per comportamento, cartella `fumo/`) è stata vista prima del giro; nessun parametro ritoccato dopo. (d) Il primo giro si è fermato per un mio tempo massimo troppo basso (150 s sul lancio più lungo): ne ho letto solo le durate, ho diviso quel lancio in due e rifatto tutto; i 72 file comuni ai due giri sono **identici** (`ris/RIPETIBILITA.txt`). (e) I lanci girano **quattro alla volta** (ognuno un filo, meno di 20 MB): 241 s; uno alla volta sarebbero circa 15 minuti (916 s di CPU), oltre i dieci chiesti. (f) Letti solo il contratto d'integrazione, V8, `MODIFICHE_CONTINUITA.md`, `CONTROPROVE_MODIFICHE.md`, `att.c`, e per ricerca testuale `SOLUZIONE_V2.md` e `gen.h`; `VERDETTO_DATI.md` alle 17:47 non esisteva (`ls`), f10 non è usata. (g) c6 e c8 non sono nell'insieme provato. (h) Per due ritocchi ai miei script e un conteggio ho usato il `python3` di sistema, senza numpy; `rifai.sh` usa l'interprete di f10. (i) **Regola toccata:** a lavoro finito ho lanciato un `git status` in sola lettura, per controllare di non aver cambiato niente fuori dalla cartella (così è); la consegna diceva «niente git». Nessuna scrittura fuori dalla cartella, niente rete. `PREVISIONI.md` non è cambiato dopo le prove (impronta `b60d31d0…`).

**Che cosa condivido con f8, e che cosa no.** Condiviso con l'avversario di f8 (tutto ciò che non sta in `DIFFERENZE.txt`): **il generatore dei camminatori, il modello del sensore** (disco di 0,45 m, misura = baricentro della parte visibile, rumore gaussiano di 5 cm, rilevamento a probabilità fissa), il filtro, il predittore `sd-1`, il ciclo di vita, le geometrie, la griglia da 0,10 m; con tutti, la specifica a parole e il modello linguistico. **Non condiviso:** i semi e il loro mescolatore; c3, c7, la chiusura 5, l'estraneo, «fermo negli ultimi 2 s»; i conteggi (scoperti con i non confermati, istanti con l'avviso spento, misura primaria); gli script di lettura. **La prova è indipendente solo per i difetti di quelle parti e per la sorte dei semi**: un errore nel generatore o nel sensore di `att.c` passa intatto. Rispetto al codice dell'autore delle modifiche (`comp.c`, `gen.h`) l'indipendenza è quella di `att.c`.

**Semi (K-223).** Prova: 7 000 000 000 + 1 000 003·s; libreria: 9 000 000 000 + 1 000 003·s; f8 usava 1000–1199, 12000–12399, 100000+, 200000+, 300000+. Stato iniziale da tre passate di `fmix64`. Su 1000 coppie di semi vicini, flussi uguali a meno di uno spostamento fra −8 e +8: **0** a passo 1 000 003, **0** anche per semi contigui, 0 fra prova e libreria; il controllo positivo (il seme di `gen.h` prima della riparazione) dà **1000 su 1000**, quindi la prova vede il difetto. Correlazione fra flussi vicini: 0,003 (errore tipo 0,004). Stato: **verificato** su quelle 1000 coppie (`ris/semi.txt`).

## 1. Le soglie del contratto: regge o cade

| # | Soglia (scritta prima) | Esito | Numero | Dominio in cui la cifra si può ancora dichiarare |
|---|---|---|---|---|
| a1 | 0 passaggi con un vuoto dopo l'ingresso nell'ombra | **regge** | 0 su 23 402 (12 combinazioni × 5 comportamenti × 400), e 0 su 217 861 in tutti i lanci; limite superiore al 95 %: 1,7 su 10 000 | traccia entrata nell'ombra |
| a2 | 0 passaggi con la traccia chiusa prima dell'ombra (scoperti) | **cade** | con c7 24 su 23 402 (0,10 %); senza c7 928 (3,97 %). Rilevamento 0,9: 2 su 11 701; 0,7: 22 su 11 701 (esteso 17, puntiforme 5) | «meno di 1 passaggio su 1000 con rilevamento 0,9; circa 2 su 1000 con 0,7», maschera esatta |
| b | persona dentro la regione: Wilson ≥ 0,90 a 1 e 2 s, ≥ 0,85 a 3 s, per cella | **regge in T e L; cade in D** | T: minimo 0,955 fino a 2 s, 0,936 a 3 s. L: 0,921 e 0,899. D: vedi §2 | ombra larga (T, L), sul percorso, maschera esatta, rilevamento 0,9. In D: «almeno 88 su 100 a 1 s», poi nessuna cifra |
| c | K-215: regione ≥ 0,85 a 1 s con l'ombra stimata a −10 e −20 cm | **cade senza c3**; con c3 regge solo se il bordo è visto a ogni ciclo | T, «prosegue», 1 s: 0,414 e 0,297 senza c3; 0,998 e 1,000 con c3; 0,742 e 0,757 con c3 che manca 2 cicli su 10 | **«con la maschera esatta»** (V8 §7), finché il sensore non misura c3 |
| d | con l'estraneo, nessun avviso rilasciato senza aver visto il soggetto | **cade** | 3027/3041, 3493/3616, 3239/3546 | un solo soggetto per ombra (condizione 7 del nucleo, intatta) |
| e1 | 0 nascosti fuori dall'area d'avviso (R100), tutti gli istanti | **regge** | 0 su 11 946 289 istanti, anche a −20 cm | un soggetto per ombra, sensore fermo |
| e2 | la chiusura «fuori dall'area osservata» non toglie l'avviso | **regge** | 0 scoperti aggiunti, 0 fuori da R100 su 52 391 cicli nascosti dopo la chiusura | — |
| f | identità al ritorno con C6 e c1 ≥ 0,95 sul percorso | **regge** | 10 711/10 757, 9228/9240, 6772/6967 (Wilson: 0,994 / 0,998 / 0,968) | sul percorso; chi svolta o esce lontano: 0,72–0,80 in T e L, e l'avviso resta |
| g | costo ≤ 6,7 ms, dieci tracce | **regge** | 95º percentile 0,32 / 0,62–1,02 / 1,78–1,96 ms in C; massimo 3,5 ms | solo il predittore, in C; Python **non verificato** da me (f8: 5,3 ms) |

## 2. I risultati, prova per prova

**(a) Continuità.** Per costruzione (il pavimento) più conteggio: nessun ciclo senza regione. Gli scoperti che restano con c7 sono 24 passaggi, **tutti lunghi almeno 3 cicli** (0,2 s): non è il ciclo di ritardo di c4, come avevo previsto. La causa non è diagnosticata: **non risolto**; lo decide il registro dell'ultima misura in quei 24 passaggi (ipotesi: ultima misura oltre 0,75 m dall'ombra, o nessuna misura prima dell'ombra). Costo di c7: l'avviso resta acceso a soggetto in piena vista per 62–548 cicli ogni 1741–2000 passaggi con rilevamento 0,9 e per 1441–3639 con 0,7 (in media meno di 2 cicli a passaggio). Dei passaggi mai confermati prima dell'ombra (f8 li scartava): 248 su 248 scoperti senza c7, 7 con c7. Con l'ombra stimata a −20 cm gli scoperti risalgono: 31 su 3956 con rilevamento 0,9 e 175 su 3956 con 0,7, anche con c3 e c7.

**(b) Precisione**, corpo esteso, rilevamento 0,9, maschera esatta; un istante per passaggio e per orizzonte; D con 4000 semi per comportamento, T e L con 2400. *Primaria* = istanti in cui il segno è «previsto» e l'etichetta dice «almeno 9 su 10»; *secondaria* = tutti gli istanti, R90 grezza (confrontabile con f8).

| Geometria | 1 s: primaria; secondaria (cella peggiore, limite di Wilson) | 2 s | 3 s | Area R90/ombra a 1, 2, 3 s |
|---|---|---|---|---|
| T | 0,975 (torna); 0,956 (torna) | 0,961; 0,955 (prosegue) | 0,939 (rallenta); 0,936 (prosegue) | 0,11 0,24 0,30–0,36 |
| L | 0,964 (torna); 0,951 (torna) | 0,934; 0,921 (torna) | 0,909; 0,899 (torna) | 0,06 0,15 0,26 |
| D | **0,882** (sosta lunga, 942/1045); quattro celle su cinque sotto 0,90 (0,882–0,892), «rallenta» 0,909. Secondaria: 0,911 (torna) | primaria: **n < 400** in ogni cella (il segno è già «ampio» nel 92 % degli istanti); cinque comportamenti insieme 518/788 = 0,657. Secondaria: «prosegue» **0,889** (1257/1388) | primaria: n < 400 (95/258 = 0,368 insieme). Secondaria: «prosegue» **0,836** (845/984); le altre ≥ 0,876 | 0,71 1,00 1,10 |

In D la cifra di V8 («45 celle su 45, limite peggiore 0,922») **non si ritrova** con il corpo esteso: lo «0,90 fino a 2 s» lì non si può dichiarare, e quando in D il segno «previsto» resiste oltre 1 s la regione stretta contiene la persona in 2 casi su 3. **A parte** (nessuna soglia): chi svolta 0,86 / 0,67 / 0,79 a 2 s e 0,84 / 0,58 / 0,67 a 3 s; chi esce dal lato lontano 0,82 / 0,61 / 0,79 e 0,76 / 0,57 / 0,70 (secondaria; a 1 s 0,91–0,96): li copre solo l'avviso. Chi **parte da fermo**: R90 grezza 0,146 / 0,049 / 0,043 a 1 s. Con c5 com'è scritta la regione mostrata lo contiene nel 0,787 / 0,745 / 0,717 a 1 s: **non basta** (conferma V8). Con «fermo negli ultimi 2 s → ampio» (forma citata in V8, mai provata): 256/256, 342/342, 249/249 a 1 s, cioè il sistema non dichiara un livello e dice «è dietro»; n fra 107 e 383 per cella, sotto i 400.

**(c) K-215**, corpo esteso, cinque comportamenti sul percorso insieme, a 1 / 2 / 3 s (`c_*`):

| Geometria, errore | senza c3 | c3, bordo visto sempre | c3, bordo visto 8 cicli su 10 |
|---|---|---|---|
| T, −10 cm | 0,535 / 0,661 / 0,768 | 0,992 / 0,976 / 0,969 | 0,780 / 0,803 / 0,862 |
| T, −20 cm | 0,459 / 0,649 / 0,765 | 0,996 / 0,974 / 0,968 | 0,801 / 0,835 / 0,884 |
| L, −20 cm | 0,350 / 0,375 / 0,482 | 0,986 / 0,960 / 0,928 | 0,750 / 0,708 / 0,733 |
| D, −20 cm | 0,730 / 0,883 / 0,928 | 0,948 / 0,906 / 0,901 | 0,854 / 0,886 / 0,957 |

Con rilevamento 0,7 in T le cifre sono entro 0,04 da queste. c3 qui è **ottimista per costruzione**: «tagliato» è deciso sul bordo vero, che in simulazione si conosce. Il braccio «8 su 10» dice quanto è fragile: basta mancare il bordo due cicli su dieci e in T e L la cifra torna sotto 0,85. In nessun braccio un nascosto esce da R100.

**(d) L'estraneo** (K-219, K-016). Il soggetto entra e sosta dietro il pannello (2–4 s o 6–8 s); un estraneo mai visto parte da dentro l'ombra 0,5–3 s dopo ed esce da un lato a caso; conto la decisione sulla sua prima misura valida, con la traccia del soggetto pendente (`d_*`, 2000 semi × 2 comportamenti per geometria; i corpi non si occludono fra loro).

| | D | T | L |
|---|---|---|---|
| Regola prima di c1 (0,40 m, margine dalla portata): identità sbagliata | 1457/3029 = 0,481 | 2567/3609 = 0,711 | 2393/3540 = 0,676 |
| **Con c1**: identità sbagliata, cioè avviso rilasciato senza aver visto il soggetto | **3027/3041 = 0,995** | **3493/3616 = 0,966** | **3239/3546 = 0,913** |
| di cui col soggetto ancora tutto nascosto | 2124 | 2713 | 2984 |
| Rifiutati dalla porta («ambiguo»): l'avviso resta, e solo qui c2 serve | 14 | 123 | 307 |

c1 allarga il riaggancio all'estraneo di 51 / 26 / 24 punti. La porta M7 non lo ferma perché all'uscita dell'estraneo la regione è già «ampio», cioè tutta l'ombra, nel 98 / 75 / 90 % dei casi. **c2 com'è scritta agisce solo dopo un rifiuto: non ripara.** Se l'avviso di un'ombra si rilasciasse solo guardando (priorità 2 del contratto), i rilasci sarebbero 0 **per costruzione**; ma con l'occlusore fermo l'avviso non finirebbe mai: è la seconda metà di C7 che il nucleo non adottò (`SOLUZIONE_V2.md`, riga 79). **Non provato**; scelta da nominare nella versione 3.

**(e) Sicurezza.** Il centro del nascosto non esce mai da R100 (0 su 11,9 milioni di istanti; gli istanti di un passaggio non sono indipendenti). Con l'avviso davvero acceso come requisito, e la maschera esatta: scoperti 1791 istanti su 5 642 995 (29 passaggi su 95 399). La chiusura 5 nella forma scritta («tutti i membri fuori») è vera in 25 passaggi su 194 861: con `sd-1` è quasi lettera morta, perché la scia resta nell'ombra. Nella forma debole (punto del filtro fuori area) scatta in 748 / 644 / 636 passaggi su 741 / 800 / 800 («esce lontano» e «sosta lunga»), in 228 / 258 / 333 col soggetto ancora tutto nascosto.

**(f), (g).** In L i 195 riagganci mancati sul percorso sono 173 per il margine dalla portata e 22 per la porta M7. Sessione di 120 passaggi con c1 e c2: riagganci 79/79, 111/111, 83/84; pendenti alla fine 1 / 1 / 2 (f8 senza c2: 87 / 117 / 95). Il costo è misurato a lanci finiti, su macchina condivisa.

## 3. Stati proposti

- «Nessun vuoto dopo l'ingresso»: **per costruzione, e sostenuto dai dati in simulazione** (217 861 passaggi, semi nuovi).
- c7: **sostenuta dai dati in simulazione**; «0 scoperti» **smentito** (24 su 23 402); causa del residuo **non risolta**.
- «Almeno 9 su 10 fino a 2 s, 85 su 100 fino a 3 s»: **sostenuto dai dati in simulazione in T e L**; **smentito in D** con il corpo esteso.
- K-215: **controesempio in simulazione** confermato; c3 **non risolta**: decide il sensore (errore della maschera al bordo e quota dei cicli in cui il bordo si riconosce).
- K-219: **controesempio in simulazione** contro c1 con un estraneo; K-016 **non riparata**; c2 **non lo ripara** (per costruzione più conteggio).
- c5 com'è scritta: **non basta** (0,72–0,79 a 1 s); «fermo negli ultimi 2 s»: **sostenuta dai dati in simulazione**, con n sotto 400.
- Chiusura 5 che lascia l'avviso, K-218 con c1, costo in C: **sostenuti dai dati in simulazione**.

## 4. Previsioni (scritte alle 17:51:24): esito

Reggono: P1 (0 vuoti), P3 (cade in D, regge in T e L), P6 e P7 (estraneo), P9 nella sostanza, P11, P12. **P2** regge nel numero (24 contro 928, meno di un decimo), **smentita nel meccanismo** (non sono cicli isolati). **P4 mista**: svolta e lontano sotto 0,70 a 2 s solo in T; «sopra 0,90 con c5» **smentita** (0,72–0,79). **P5** regge in T e L, **non risolta** in D (n = 119–204, sotto 400). **P8** regge (cade per gli scoperti; 0 fuori da R100). **P9**, «la forma scritta non scatta mai»: 25 su 194 861. **P10**: regge la soglia; in D avevo previsto 0,90–0,99, è 0,996. **Notato dopo:** la fragilità di c3 a 8 cicli su 10; gli scoperti a −20 cm; la porta M7 vuota in «ampio».

## 5. Non provato, e che cosa segue

**Non provato:** sensore vero, falsi rilevamenti, buchi di profondità; c3 sull'immagine; due soggetti visti insieme nella stessa ombra; occlusione fra i due corpi; c6 e c8; sensore in moto; `sd-0`; il costo in Python e dell'intera catena; la libreria da un generatore diverso da quello dei passaggi (limite già scritto in V8 §2.1, intatto).

**Per la versione 3 (niente idee nuove: solo ciò che i numeri impongono).** (1) La cifra di precisione si scrive «con la maschera esatta, ombra larga, sul percorso»; in demo (D) «almeno 88 su 100 a 1 s, poi "è dietro"». (2) c7 entra; si dichiara «meno di 1 passaggio su 1000 scoperto con rilevamento 0,9». (3) c1 entra **con il limite scritto accanto**: «un soggetto per ombra; se ne esce un altro, prende l'identità del primo e l'avviso cade in 9 casi su 10». (4) c5 nella forma «fermo negli ultimi 2 s». (5) La chiusura 5 lascia l'avviso. (6) Sul sensore, per primi: l'errore della maschera al bordo del pannello e la quota dei cicli in cui il bordo di profondità si riconosce (decidono K-215 e c3). *Dopo l'hackathon:* una regola d'identità che distingua l'estraneo.

**Rifare:** `cd f12-integrazione/02-prova-insieme && sh rifai.sh` (241 s con quattro lanci leggeri alla volta, ognuno con `timeout 280`; `P=1 sh rifai.sh` per farli uno alla volta, circa 15 minuti). Il giro precedente resta in `ris_prec_<ora>/`. Impronte di `att.c`, `componi.py`, `insieme.c`: `ris/IMPRONTE.txt`.
