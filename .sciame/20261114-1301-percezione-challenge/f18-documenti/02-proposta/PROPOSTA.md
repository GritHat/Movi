# Proposta v2.0: scelte e cifre con la fonte

`sciame-comunicazione`, 15-11-2026, dalle 03:03 alle 03:10 circa (`date -Is`). Previsioni in `PREVISIONI.md` (03:04:23).

## In testa: stato e regole

- **Uscite:** `proposta_sciame_v2.0.tex` e `proposta_sciame_v2.0.pdf` (2 pagine A4, `pdfinfo`: Pages 2,
  595.28 × 841.89 pt). L'originale `proposta/proposta_sciame.tex` non è toccato; una sua copia è qui come
  `proposta_sciame_v1.0_prima.tex`. Le bozze intermedie restano accanto (`_bozza1` … `_bozza4`); nessun file cancellato.
- **Fase 2c:** `60-fase2c/02-verdetto/VERDETTO_2C.md` **non esisteva** alle 03:08:24. Le cifre sono di VERDETTO_2B;
  le righe che la 2c può cambiare portano il commento `% 2C` (A1 «libero» col pannello, E1, scene del prototipo, aperti).
- **Regole:** nessuna violata, che io sappia. Niente rete, niente git. Nota: l'orologio della macchina dava 03:03 al
  mio avvio, mentre VERDETTO_2B si dichiara scritto «dalle 02:59 alle 03:15 circa»; il file era già completo. Non
  verificato quale orologio sia giusto.
- **Leggibilità:** corpo 8,7 pt; note 7,7 pt; tabella dei sensori 8,2 pt; testo dello schema 7,6 pt (era 6,5 nel
  v1.0), marche di stato 6 pt. **Sotto 8 pt restano lo schema, le note e le marche**, come nel v1.0.

## Previsioni ed esiti

| # | Previsione | Esito |
|---|---|---|
| 1 | 2 pagine esatte; prima composizione > 2 | **2 regge** (2 pagine). La prima composizione era già di 2: la mia previsione sulla prima composizione è **smentita** (pagina 2 aveva un terzo libero; l'ho usato per la tabella dei sensori e il «perché questo caso») |
| 2 | 0 frasi «da non dire» | **regge**: grep di validat, tempo reale, certificabil, detect and avoid, 122 droni, 51/60, 46 km, 59 km, contiene sempre, zero falsi, counter, threat, minacc, rileva droni, sempre: 0 righe |
| 3 | ogni cifra ha una fonte | **regge** (tabella sotto) |
| 4 | Wilson ricalcolati = arbitro | **regge**: 200/200 [0,981; 1], 188/200 [0,898; 0,965], 12/200 [0,035; 0,102], 49/60 [0,701; 0,894], 163/171 [0,910; 0,976], 50/200 [0,195; 0,314], 564/2400 [0,218; 0,252], 36/60 [0,474; 0,714], 149/200 [0,680; 0,800], 100/100 [0,963; 1], 60/60 [0,94; 1] (codice mio, z = 1,96; condivide con l'arbitro solo i k/n) |

## Scelte

1. **Impianto:** titolo con MoVi, gruppo SDMs e i cinque autori; caso centrale = sito aerospaziale sorvegliato con
   droni e aerei in rullaggio (decisione K-603 in ADDENDUM_UTENTE); aerei in volo e treni veloci come limite.
2. **Limiti per primi**, dal § 4 di VERDETTO_2B, più classificatore a mano e «nessuna funzione d'ingaggio».
3. **Marche:** alle S/C/P del v1.0 ho aggiunto **T** (traiettorie pubbliche) e **X** (smentito, detto come limite),
   perché VERDETTO_FASE2 § 2 usa questi stati e la giuria deve vedere dove una cosa non regge.
4. **Affermazioni:** § 3 e § 4 riprendono le convergenti 1–10 di VERDETTO_2B § 2 nella loro forma (con il limite dentro
   la frase); la 11 sta nella riga «classificazione» dei requisiti; la 12 sta nel riquadro dei limiti.
5. **Una cifra dalla sola fase 2:** «43 aerei, zona ~9/10» (VERDETTO_FASE2 § 6.3) non è nella lista 2B ma non è fra i
   «da non dire»; l'ho tenuta precisando «la zona di previsione, non l'avviso», perché con il vecchio limite di 90 m/s
   l'avviso perdeva 8–11 aerei su 43 (lo dico fra le idee scartate).
6. **Le cifre del nucleo precedente** (costo per ciclo, falsi avvisi, 460/460, 228/228) sono marcate «nucleo
   precedente, non rifatto».
7. **Prototipo:** una riga di lancio verificata come file esistente (`prototipo/prove/scene_lunghe.sh`), **non
   eseguita** da me; esito 0 in 665 s e 0 errori sulle 20 scene sono adottati da VERDETTO_2B, con la riserva K-611 (il
   validatore non guarda il «libero» dentro l'avviso), scritta nel testo.
8. **Nomi dei prodotti** (IRIS, SCANTER, AT128, Tele-15): fuori dal documento, sensori per tipo; restano nell'allegato.
   Evita il lessico della scheda IRIS (VERDETTO_FASE2 § 6).
9. **Corto raggio** in un paragrafo: persona dietro un ostacolo, avviso per persona non vedente, 0/4324, 1,44 m/s.

## Cifre e fonti

| Cifra nel documento | Fonte |
|---|---|
| A1: 806 m, ~950 m, 200/200, 100/100, 188/200, 12/200 | VERDETTO_2B § 1 e § 2.1; `10-riprova/riprova_passaggi.jsonl`, `11-controprova` |
| A2: 200/200, 0 fuori avviso, 0 «libero»; solo radar 50/200 | VERDETTO_2B § 2.2; VERDETTO_FASE2 § 2 (v1) |
| A3: 0/200 «libero», «zona non verificata per i multirotori» | VERDETTO_2B § 2.4 |
| 564/2400; 0/200 senza zona | VERDETTO_2B § 2.5; VERDETTO_FASE2 § 1.3 |
| 45 m/s, 25 m/s², 210 m/s, ~0,9 km, 3,4 km | VERDETTO_2B § 1 (correzioni 1–2) e § 2.3, 2.6 |
| 163/171 pannello; mappa `True` | VERDETTO_2B § 1 (A1, K-612), § 2.12 |
| 49/60, 1,2–2,2 s, 36/60 ≥ 10 km | VERDETTO_2B § 1 eventi, § 2.9 |
| 90/90 entro 3 cicli; 460/460 entro 5,3 s (v1) | VERDETTO_2B § 2.7 |
| E4 0/60 e 0/30; E5 0/300 | VERDETTO_2B § 2.8 |
| 43 aerei ~9/10 (zona); 8–11 su 43 con 90 m/s | VERDETTO_FASE2 § 2 e § 6.3 |
| falsi avvisi 3,8–91/h nel sito, 1594/h auto; costo 46 ms, p95 340 ms | `11-prove/PROVE_LUNGA_PORTATA.md` T4 e § 3.9 (non ricontati dall'arbitro) |
| A4 149/200 | VERDETTO_FASE2 § 2 |
| X4: 0,263 contro 0,010 | VERDETTO_FASE2 § 3.1 |
| 228/228 cicli | VERDETTO_FASE2 § 3.3; VERDETTO_2B § 2.11 |
| 46 % dei campi ipotesi | `02-sensori/SENSORI_LUNGA_PORTATA.md` § 1 (57 su 124) |
| portate dei sensori (1,1–7,6 km; 5 km per 1 m²; 210 e 320 m; 2 km EO; ~1 km Remote ID) | `02-sensori/SENSORI_LUNGA_PORTATA.md` § 2 |
| prova_tutto 665 s, 20 scene 0 errori | VERDETTO_2B § 2 (coda) |
| corto raggio 0/4324; 1,44 m/s; voxel 80 505/146 901 | v1.0 `proposta/proposta_sciame.tex` |

## Le due letture a freddo (fatte da me: non indipendenti dal testo)

**Giurato esterno.** (1) Il titolo andava a capo su due righe: allargato. (2) «In tempo» e «passaggio» non erano
definiti: aggiunta una frase in § 1. (3) «Semi nuovi» è gergo: ora «condizioni nuove». (4) «Pannello» non diceva che è
un radar: ora «secondo radar a pannello». (5) Il titolo del § 5 restava solo in fondo a pagina 1: interruzione di pagina.
(6) Mancava il perché del caso centrale: § 10.

**Giurato tecnico.** (1) Costo e falsi avvisi erano del nucleo precedente senza dirlo: marcati. (2) «1 594 falsi
avvisi/h» è delle auto, non del sito: separato (3,8–91 nel sito). (3) «40/40 in 5,3 s» era una sola riga del v1:
sostituito con la forma di VERDETTO_2B (90/90; 460/460 del v1). (4) I «0 errori» del validatore senza K-611: aggiunta
la riserva. (5) I limiti di velocità erano marcati C, ma la loro prova è su casi costruiti: ora S. (6) «46 %» era
attaccato alle sole Pd: riformulato. (7) «Due regole che nessun modulo scavalca» era falso (il prototipo scavalca la
mappa): ora «due regole del nucleo», con il rinvio ai limiti. (8) I «43 aerei» erano letti come avviso: precisato «zona».

## Dopo

- Rifare l'allineamento quando esiste VERDETTO_2C: cercare `% 2C` nel .tex (6 righe, compresa l'intestazione).
- Se il coordinatore lo vuole, portare il PDF in `proposta/` come `proposta_sciame_v2.0.pdf` (non fatto: fuori dalla mia cartella).
- Una lettura indipendente (lettore critico, esperto di dominio) delle due pagine: le mie due passate condividono l'autore.
