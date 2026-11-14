# Sezione B — Architettura del nucleo, componente per componente

Redatta da `sciame-architetto` (fase f11) il 14 novembre 2026, dalle 16:10 alle 16:22 (`date -Is`). Descrive la **soluzione versione 2** (il «nucleo»), che l'arbitro giudica «adottabile come progetto di prototipo, non come sistema validato».

**In testa.**
- **Niente è provato sull'hardware.** Ogni cifra viene da una simulazione, da un conto o da una scheda tecnica, sempre **a sensore fermo**. Nessun fotogramma di una camera vera è stato elaborato (`VER` §5).
- **Non ho eseguito prove.** Ho letto i file, ricontrollato dodici file grezzi di risultati (elenco in coda) e fatto due conti, marcati **[arch.]**. Condivido con gli autori il modello linguistico e la specifica.
- **Discordanze trovate fra i file:** margine dell'invariante 1 (§3); «il pannello da 1 m regge senza C6» e soglia trasversale della regola «si muove» (B3); durata del «previsto» e cifra «prima» di C4 (B5); ritardi del segnale di affidabilità (B8); distanza del pannello (B9); ore in fila (§4).
- **Una critica nuova, mia, non vagliata:** l'altezza minima del pannello (condizione 3 del verdetto) vale per un pannello a 1,15 m; nella geometria riprovata sta a 1,9 m e servono circa 1,67 m, non 1,5 (B9).
- **Lunghezza:** 5,7 pagine a 6 200 caratteri l'una (35 300 caratteri, elenchi in coda compresi); composta in PDF, con le tabelle, ne occupa di più.

**Sigle dei file** (percorsi relativi alla cartella della convocazione). `V2` = `f4/H-012/05-correzioni/SOLUZIONE_V2.md`; `V1` = `f3/H-012/01-scene-dinamiche/SOLUZIONE.md` (versione 1); `VER` = `f4/H-012/09-arbitro/VERDETTO.md`; `CP` = `f4/H-012/01-avversario/CONTROPROVE.md`; `M1`, `M2`, `M2b` = `f4/H-012/03-validazione/MISURE.md`, `MISURE_V2.md`, `MISURE_V2_bis.md`; `AUD` = `f5/02-audit/AUDIT.md`; `VRF` = `f3/H-012/02-validazione/VERIFICA.md`; `PM` = `f3/H-012/03-metrologo/PIANO_MISURE.md`; `FON` = `f3/fonti/FONTI_VERIFICATE.md`; `SEL` = `f2/05-selezione/SELEZIONE.md`; `T7`, `T8` = `f7-estensione/10-triage/TRIAGE.md`, `f8-continuita/10-triage/TRIAGE.md`. Gli altri file di risultati citati per nome stanno in `f4/H-012/01-avversario/` (`risultati_a…`) e in `f4/H-012/03-validazione/` (`v2_…`, `bis_…`).

**Sigle dello sciame.** R1–R8: gli otto requisiti ricavati dalla traccia (`CONTRATTO.md`). B1–B9: i blocchi del sistema. H-nnn: un'ipotesi numerata (H-012 è il nucleo). F-nnn: un fatto stabilito. K-nnn: una contraddizione fra due enunciati, con la prova che la decide. C1–C12: le correzioni nate dai dodici attacchi dell'avversario. H0–H13: le quattordici prove sull'hardware del piano delle misure (`PM`). Pd: probabilità che un oggetto visibile sia rilevato in un fotogramma. «Passaggio»: una camminata simulata, l'unità che si conta. `AUD` n: l'ipotesi nascosta numero n dell'audit.

**Stati.** **[DIM]** dimostrato, nel modello indicato. **[COSTR]** vero per costruzione della regola: controllo della logica, non dato. **[SIM]** sostenuto dai dati in simulazione. **[SMENT]** smentito. **[NR]** non risolto. **[NV-HW]** non verificato fino all'hardware. **[STIMA]** stima dell'autore. **[PREL]** preliminare: viene dalle estensioni in corso (f7–f10), non ancora vagliato dall'arbitro.

## 1. Schema a blocchi

```
scena ─► B1 camera stereo attiva + IMU, ferma (treppiede 1,2 m, 15° in basso)
           │ profondità 30 fps + contatore di fotogramma        │ RGB a bassa frequenza
           ▼                                                    ▼
         B2 griglia polare 1° × 0,1 m fino a 3 m              B6 rete a lato:
           │ quattro stati per cella                            persona / non persona
           ├─► celle occupate ─► B3 gruppi + regola «si muove»  (solo un'etichetta)
           │                       ▼                              ┆
           │                     B4 associazione + Kalman         ┆
           │                       ▼ tracce                       ┆
           └─► libero, ombra, ─► B5 stati della traccia ◄┄┄┄┄┄┄┄┄┄┘
               non osservato        osservato / previsto / perso
                                    strato 1 (possibile presenza), strato 2 (area probabile)
                                   ▼
                                 B7 tabella di regole, un messaggio per settore
                                   ▼
 contatore, celle valide, IMU ─► B8 suoni brevi, schermo, «affidabilità persa»
                                   ▼
                                 B9 demo in cinque atti; accettazione sulle registrazioni
```

L'ordine rilevamento → associazione → filtro → decisione è il fatto F-003 ([COSTR]; `f2/03-triage/TRIAGE.md`). Se B6 manca, la catena non cambia (`V2` B6).

## 2. I componenti

### B1. Sensore e montaggio

- **Entra / esce.** Entra la scena; escono profondità e RGB a 30 fotogrammi al secondo con il contatore di fotogramma. L'elaborazione gira a 15 Hz, la frequenza di tutte le simulazioni (`V1` B1).

| Parametro | Valore | Da dove viene, stato |
|---|---|---|
| Camera | stereo attiva con IMU: D455 o D435i (campo 87°×58°), Gemini 335 (90°×65°) | `V2` B1; campi verificati in `FON` [realsense-confronto] https://www.realsenseai.com/compare-depth-cameras/ ; [orbbec-gemini335] link: manca in `FON`. «Posseduta dalla squadra»: **superato**, oggi la squadra non ha sensori (`ADDENDUM_UTENTE.md`, settimo) |
| Montaggio | treppiede a 1,2 m, orizzontale, inclinata di 15° in basso | 1,2 m è un'ipotesi del torneo, da misurare in H0 |
| Portata dichiarata | dove il rumore radiale del centro di una persona resta ≤ 5 cm | da misurare in H1 [NV-HW]; nella versione 1 era «0,5–3 m» |
| Curve di rumore delle prove, a 2 / 3 / 4 m | nominale 1,5 / 3,4 / 6,0 cm; pessimista 4 / 9 / 16; del torneo 5 / 11 / 20 | nominale: σ = z²·s/(f·B), f = 424 px, B = 50 mm, s = 0,08 (`VRF` §4) [realsense-tuning] https://dev.realsenseai.com/docs/tuning-depth-cameras-for-best-performance ; le altre due sono ipotesi |
| Limiti geometrici | suolo visto solo da 1,24 m (anello cieco: 30 % dell'estensione 0,5–3 m); ostacolo di 15 cm invisibile a meno di 1,09 m **di distanza**; ostacolo a 1,8 m di quota visto solo oltre 2,41 m | [DIM] nel modello geometrico (camera ideale, pavimento piano): `CP` attacco 3; 2,41 m dal torneo (via `VRF` §1) |

- **Corretto rispetto alla versione 1.** La portata non è più un intervallo fisso e i limiti vicini sono dichiarati. Controesempio: scatola a 0,8 m vista 0 volte su 5 (`CP`, attacco 3).
- **Invarianti:** 2. **Aperte:** K-009 (tenuta al sole: H3); montaggio orizzontale o verticale (verticale: suolo da 0,74 m, ma 58° in orizzontale; `V2` §6).
- **Ipotesi nascoste [NR].** `AUD` 9: il piano del suolo si stima all'avvio su scena vuota; 1,34° d'errore alzano il suolo di 7 cm a 3 m. `AUD` 10: accanto all'ombra, da un lato, c'è una banda senza dato di 9,5 cm (D455) o 5 cm (D435i). `AUD` 11: allineando la profondità all'RGB il campo della D435i scende a circa 69°×42° (non verificato) e il suolo si vede da 1,65 m.
- **Condizioni del verdetto** (numeri del §4): 1, 4, 7.
- **Costo:** 3 ore [STIMA]. **Dipende da:** quale sensore arriva; fino ad allora la sorgente è una registrazione o un sensore simulato ([PREL]: f10 li sta preparando, nessun esito). **Lo invalida:** sole pieno, sensore indossato o in moto, campo diverso.

### B2. Mappa a quattro stati

- **Entra / esce.** Entra la profondità; esce una griglia polare centrata sul sensore. Ogni cella è: **libero** (suolo visto alla quota attesa e nessun ostacolo), **occupato osservato** (primo ritorno fra 0,07 e 2 m di quota), **in ombra** (oltre il primo ritorno), **non osservato** (fuori campo, oltre portata, anello cieco, buco nei dati).

| Parametro | Valore | Da dove viene, stato |
|---|---|---|
| Cella | 1° × 0,1 m, fino a 3 m | `V1` B2 (ipotesi H-008) |
| «Libero» | suolo visto in almeno uno degli ultimi 3 fotogrammi; esce con l'età (0,13 s) | correzione C9 |
| «Buco» | dopo 3 fotogrammi non validi di fila | correzione C3 |
| «Occupato ricordato» | esce con l'età | la scadenza di 2 s della versione 1 («ipotizzata, non tarata») nella `V2` non è ripetuta: **manca** |
| Soglia di quota | 0,07–2 m; quanti pixel fanno «occupato»: **manca** | `AUD` 11 |
| Tempo di calcolo | 20 ms a 640×480, Python puro, scene sintetiche: non è il prototipo | torneo (via `VRF` §1) |

- **Corretto rispetto alla versione 1.** Con «libero solo nel fotogramma corrente» e suolo valido al 95 %, la distanza annunciata cambiava 11,9 volte al secondo; con C9: 0,00 per direzione, 0,65 per settore (`risultati_a09.txt`; 60 s a 15 Hz, buchi indipendenti: modello dell'avversario) [SIM]. All'80 % la correzione non basta (2,8–11,8).
- **Invarianti:** 1, 2, 5, 6. **Contraddizioni:** K-006 (risolta per composizione; vetro aperto); K-015 (§3).
- **Limiti dichiarati.** Vetro: la lastra risulta «libero» [SMENT], limite scritto. Pavimento piano dichiarato: a 5° di pendenza «occupato» falso dopo 0,80 m; con 2° d'errore d'assetto oltre 2 m (`V1` B2).
- **Ipotesi nascoste [NR].** `AUD` 1: i filtri della camera trasformano un buco in un dato (B8). `AUD` 2: **nessuno script ha mai calcolato «libero» da un'immagine di profondità**; i quattro stati non coprono i ritorni sotto il suolo o solo sopra 2 m. `AUD` 6: con l'1 % di celle sempre non valide l'83,6 % dei settori da 10° contiene un buco permanente. `AUD` 7: «3 fotogrammi» sono 0,13–0,2 s a 15 Hz, ma 33–50 ms a 60–90 fps.
- **Condizioni:** 1, 2, 7, 9.
- **Costo:** 6 ore [STIMA]. **Dipende da:** B1. **Lo invalida:** rampe, vetro, suolo valido in meno del 95 % dei fotogrammi, filtri accesi.
- **[PREL]** (`T7`) L'uscita va detta «suolo visto libero»: entro 3 m la colonna fino a 2 m non è mai vista tutta (fatto F-108). Una mappa che conserva il «libero» nel tempo crea falsi liberi (138 230 celle-fotogramma; proposta V-010, smentita). Aperta K-105: 45 829 celle-fotogramma «libere» e occupate, secondo la lettura di un ruolo; da rifare col codice del nucleo.

### B3. Rilevamento e regola «si muove»

- **Entra / esce.** Entrano le celle occupate; escono gruppi connessi con centro e larghezza, e per ciascuno l'etichetta «mobile» o no. Nessuna rete.

| Parametro | Valore | Da dove viene, stato |
|---|---|---|
| Regola | «mobile» se lo spostamento fra due misure distanti al più 1 s supera 5·σ(z)·√2 lungo un asse | ipotesi H-010 corretta (`V1` B3) |
| Finestra | cresce fino a 1 s | correzione C8 |
| Misure | ciascuna è la media di 3 fotogrammi | proposta `validazione-1` |
| Gruppo tagliato da un'ombra | non entra nella finestra, non aggiorna il filtro | correzione C6, **obbligata** (condizione 5) |
| Larghezza minima rilevabile | 0,15 m, oppure 3 colonne da 1° | `PM` critica 2; `VRF` §4; nella `V2` non è fissata |
| Regola alternativa | test χ² con R(z), registrato in parallelo | K-007 |

- **Testo contro codice.** Il testo dà la stessa soglia sui due assi; il codice della validazione usa sull'asse trasversale una soglia d'angolo, 1,18° a ogni distanza (`f6-specializzazione/02-slam/MOTO_PROPRIO.md`, in testa, da `sim_v2.py` righe 449 e 496–499). Va scritto quale vale.
- **Prove** [SIM]. Persona a 0,5 m/s vista entro 1 s: di traverso a 2 e 3 m 100 % (N = 2000, limite inferiore 99,85 %); in avvicinamento a 2 m 100 % con lo spostamento e 99,0–100 % con la χ² (`M1`). Da 3 m decide la curva di rumore: spostamento 100 / 10,8 / 0,1 %, χ² 100 / 56,7 / 45,2 % (nominale / pessimista / torneo; `M1`, B4); con la regola finale 100 / 85,9 / 26,6 % (`M2`, P3a). Falsi sul muro con rumore noto: 0 su 12 000 finestre (`M1`).

| Correzione | Controesempio (prima) | Dopo | File |
|---|---|---|---|
| C6 | muro fermo detto «mobile» nel 100 % (500 passaggi); 400 su 400 nella riprova | 0,0–0,2 %; 0 su 400 con tre curve | `CP` 6a; `v2_WALLP.txt` |
| C8 | finestra fissa: visto entro 1 s nel 79,0 % (Pd 0,9, N = 2000) | 99,9 % | `CP` attacco 8 |
| `validazione-1` | velocità minima vista da 2 m: 0,380 m/s (curva del torneo) | 0,278 m/s (0,095 con la nominale) | `M1` |

- **Discordanza.** La `V2` (§5) scrive che il pannello da 1 m «regge senza C6». **[SMENT]**: senza C6 la previsione contiene la riemersione nel 61,1 % o 80,2 % dei passaggi secondo il rilevatore, con C6 nel 100,0 % (N = 2000; `v2_C6.txt`).
- **Costo di C6** (K-017, aperta). Il buio dietro il pannello passa da 0,60–0,67 s a 1,07–1,27 s (`CP`); per chi torna indietro il contenimento scende dal 99 % al 47–50 % (N = 400; `M2`, P2c).
- **Invarianti:** 3. **Aperta:** K-007, spostamento contro χ²: a 2 m passano tutte e due; la decide il rumore misurato del centro di una persona a 2–4 m (H1, H8). Lo spostamento è scelta provvisoria: 0 etichette false nel primo secondo di una traccia ferma, contro lo 0,15–2,3 % della χ² (N = 4000; `M1`).
- **Costo:** 6 ore [STIMA] (5 nella versione 1). **Dipende da:** B2 e R(z) misurata. **Lo invalida:** misure anomale (con il 2 %, falsi sul muro al 5,7–14,9 %); rumore creduto la metà del vero (31 % delle finestre scorrevoli con un'etichetta falsa); sensore che ruota (dopo 10° d'imbardata i gruppi fermi sono «mobile» nel 96–100 %; `CP`, attacco 10).

### B4. Associazione e filtro di Kalman

- **Entra / esce.** Entrano i gruppi; escono le tracce: identità, posizione e velocità sul piano con la loro incertezza, stato «tentativa» o «confermata». Il filtro di Kalman fonde ogni misura con la previsione del passo prima.

| Parametro | Valore | Da dove viene, stato |
|---|---|---|
| Stato del filtro | [x, y, vx, vy], velocità quasi costante | H-010, H-012. Niente accelerazione (F-004: sotto il rumore) né massa (F-002: non osservabile, [DIM] nel modello del punto materiale) |
| Rumore di processo q | 0,2 m²/s³ | torneo: copertura 0,927 / 0,916 / 0,902 a 2 s su tre generatori non dell'autore; con q = 0,01: 0,738 / 0,710 (`SEL` §1) [SIM] |
| Rumore di misura | R(z) per asse | da H1 [NV-HW] |
| Associazione | porta al 99 %, assegnazione ungherese, priorità alle confermate | H-013 |
| Conferma | 3 rilevamenti su 5 | H-013, mai attaccata |
| Taratura di q | sulle innovazioni alla ricomparsa, su 15 passaggi diversi da quelli del criterio | `SEL` §4; `PM` |
| Copertura del cerchio al 95 % | 0,89–0,93 (cerchio intero, pochi ritorni); 0,56–0,66 per chi torna | `VRF` §1 [SIM] |

- **Corretto rispetto alla versione 1:** niente nel blocco; cambia ciò che riceve (C6) e il riaggancio (B5).
- **Invarianti:** 3, 9. **Contraddizione:** K-003 (valore di q) risolta in simulazione, aperta sul vero (H9).
- **Lo invalida:** due persone che tornano insieme da dietro il pannello: 74 % di scambi, 44 % senza avviso (torneo, via `VRF` §1). Per questo con due tracce pendenti l'identità non si dà mai.
- **Costo:** 5 ore [STIMA]; calcolo trascurabile (SORT, stessa famiglia: 260 Hz [bewley2016] https://arxiv.org/abs/1602.00763 ). Schema d'associazione: [cao2023] https://arxiv.org/abs/2203.14360 . Velocità costante contro predittori appresi sui pedoni: [scholler2020] https://arxiv.org/abs/1903.07933 . Tutte verificate in `FON`.
- **[PREL]** (`T8`) Il cerchio non è tarato per comportamento né al 50 % (fatto F-202): per chi torna contiene 0,29–0,77 a 2 s.

### B5. Stati dell'oggetto e i due strati durante l'occlusione

- **Entra / esce.** Entrano tracce e griglia. Esce per ogni traccia uno stato: **osservato** (c'è una misura nel ciclo), **previsto** (non c'è: si mostra un'area probabile), **perso** (l'area non informa più). Escono anche «non confermato», «identità ambigua» e due aree:
  - **strato 1, garanzia:** il cuneo d'ombra dell'ostacolo in cui la traccia è entrata, allargato di una fascia; dice «possibile presenza» con la sua età;
  - **strato 2, informazione:** il cerchio al 95 % del filtro ritagliato sul cuneo; dice «probabile qui».

| Parametro | Valore | Da dove viene, stato |
|---|---|---|
| Ingresso nell'ombra | ultima **misura** a meno di 0,40 m da un'ombra | definizione del responsabile, non provata (`V2` §9) |
| «Non confermato» | in campo aperto, al più 3 fotogrammi, poi traccia chiusa | idem. Tracce vere chiuse per errore: 118 su 20 000 (0,59 %) con Pd 0,9 (`v2_PD.txt`) [SIM] |
| Fascia | 0,40 m = 0,20 d'errore d'ombra + mezzo corpo di 40 cm | `V1` B5 |
| Durata dello strato 1 | nessun tetto; esce l'età | correzione C4 |
| Rilascio dello strato 1 | per riaggancio, o cella per cella se «libero» per ≥ 3 fotogrammi oltre la fascia | `M1` A7; con ostacolo fermo: mai |
| Fine del «previsto» | quando il cerchio copre metà dell'area del cuneo in griglia; «perso» è assorbente | fissata, non misurata (K-004) |
| Riaggancio | rilevamento entro la fascia dell'ombra d'ingresso, a più di 0,40 m da ogni altro bordo del non osservato, con una sola traccia pendente; altrimenti «identità ambigua» | correzione C1 |
| Portata della garanzia | solo chi è stato visto ≥ 4 fotogrammi | con 3 la traccia manca nel 27,1 % dei casi, con 4 nel 5,2 % (`CP`, attacco 7) |

| Correzione | Controesempio (prima) | Dopo | File |
|---|---|---|---|
| C1 riaggancio | riaggancio sbagliato e muto nel 9,5–100 % delle scene (200 per riga) | 0,0 %. Costo: riemersioni legittime riagganciate 100 % fino a 2,3 m, 86,3 % a 2,5 m, 0 % a 2,8 m | `risultati_a01.txt` |
| C4 tetto di 10 s | sosta di 11 / 12 / 20 / 60 s: 15 / 30 / 150 / 750 fotogrammi di nascosto senza avviso | 0. (`CP` §2 scrive «30–750», la `V2` «15–750»: il file dà 15 per la sosta di 11 s) | `risultati_a04.txt` |
| C5 estensione dello strato 1 | con le celle contigue copriva il 100 % del non osservato: 45,47 m² contro 1,01 d'ombra | 1,01 m² | `risultati_a05.txt` |
| Rilascio | rilascio a soggetto nascosto nel 92,5–99,5 % delle soste (prova sul punto previsto) | nessuno [COSTR] | `M1`, A7 |

- **Prove dell'insieme** [SIM] (`M2`, N = 400 per cella).
  - Garanzia: 0 passaggi falliti su 14 400 (36 celle, limite 0,75 % per cella) con Pd = 1; i bracci che dovevano fallire sono falliti.
  - Stessa identità al ritorno: 100 % in 27 celle (limite inferiore 99,25 %); 99,7–100 % con Pd 0,9.
  - Demo corretta: buio 1,07–1,13 s, «previsto» 0,40–0,53 s, «perso» 0,47–0,67 s; area prevista ancora mostrata alla riemersione nello 0,5–1,2 % dei transiti. **La continuità la porta lo strato 1, non l'area prevista** (`V2` §1; `VER` §5).
- **Discordanza sulla durata del «previsto».** `V2` §1: 0,6–0,7 s (da `CP`, attacco 11); `M2` e `VER`: 0,40–0,53 s; [PREL] emulazioni di f8: 0,67–0,87 e 0,66–1,14 s (K-211 in `T8`).
- **Costo dichiarato.** La fascia mette «possibile presenza» sul 28,2 % del suolo visto libero: circa 1,34 m² su 4,75 [arch.] (`risultati_a05.txt`). Con Pd 0,9, nel 12,8–14,3 % dei passaggi resta acceso uno strato 1 a soggetto visibile (`M2b`).
- **Margine sull'errore d'ombra** [SIM] (`M1`, 1200 passaggi per riga). Corpo di 40 cm: a −20 cm 0 fuori, a −30 cm 107 (8,9 %), a −40 cm 1075 (89,6 %); corpo di 60 cm a −30 cm: 399 (33,3 %). Oltre i 20 cm ipotizzati il margine è meno di 10 cm.
- **Invarianti:** 3, 4, 6, 7.

| Contraddizione aperta | Enunciato e cifra | La decide |
|---|---|---|
| K-014 | con Pd 0,9 e ombra stimata 20 cm più stretta del vero: 13 passaggi falliti su 4800; 0 su 9600 a 0 e +20 cm. `validazione-4` li riduce a 8, o a 2 se la traccia chiusa rinasce: non chiude (`M2b`) | hardware: celle «libero» dentro l'ombra vera, 150 fotogrammi |
| K-016 | un secondo soggetto mai visto che esce dalla stessa ombra è riagganciato con l'identità sbagliata, senza avviso, in 2400 casi su 2400 (`v2_SECOND.txt`) | H11; regola nuova |
| K-018 | «a meno di 0,40 m da un'ombra» è sempre vero per l'ombra propria della persona: alla lettera il ramo «campo aperto» non scatta mai (`AUD` 4) | regola scritta prima del codice |
| K-004 | «metà dell'area del cuneo»: le letture davano «perso» fra 0,8 e 5,8 s (`risultati_a05.txt`) | — |

- **Limiti dichiarati.** Ostacolo che si muove; rilevamenti falsi al bordo del pannello (mai simulati); un'ombra in cui non è entrato nessuno resta «in ombra», senza avviso. «Perso» si dice sempre «può aver lasciato l'area».
- **Condizioni:** 2, 3, 5, 6, 7, 8. **Costo:** 9 ore [STIMA] (8 nella versione 1). **Dipende da:** B2 (maschera d'ombra), B4.
- **[PREL]** Lo strato 2 com'è **non rispetta** l'imperativo della continuità (quarto addendum) per nove ruoli su nove: il nucleo emette una stima solo nel 35–50 % dei cicli senza osservazione in demo; in gara «perso» non assorbente e cinque predittori (`T8` §1, §3). «Il cuneo arriva sempre al bordo della portata» è smentito per ostacoli più bassi del sensore (fatto F-109 in `T7`; già `AUD` 5).

### B6. Ramo asincrono di riconoscimento

- **Entra / esce.** Entra l'immagine a colori a bassa frequenza; esce l'etichetta «persona / non persona» su una traccia che esiste già, mostrata a schermo.
- **Parametri.** RF-DETR-N (2,3 ms su scheda grafica T4, licenza Apache 2.0) [roboflow-rfdetr] https://github.com/roboflow/rf-detr , oppure YOLO26n (38,9 ± 0,7 ms su CPU, licenza AGPL-3.0) [ultralytics-yolo26] https://docs.ultralytics.com/models/yolo26/ : verificati in `FON`. Il tempo sulla macchina della squadra: **manca**.
- **Regole.** Non crea né chiude tracce, non tocca celle, non decide allarmi (invariante 5).
- **Stato.** Nessuna correzione, nessun attacco specifico. Copre la parola «riconoscere» della traccia per lettura dichiarata (`V2` §7). Le classi d'ostacolo (muro, porta, gradino) non sono fra quelle del rilevatore: 0 su 7 (`SEL`, H-006).
- **Costo:** 4 ore [STIMA]; primo taglio se manca tempo (`AUD` 8; `VER` §6). **Dipende da:** B4.

### B7. Logica di decisione

- **Entra / esce.** Entrano griglia e tracce; esce, per ogni settore angolare, il messaggio più grave. È una tabella di regole scritta a mano, non un modello appreso.

| Parametro | Valore | Da dove viene, stato |
|---|---|---|
| Zona di valutazione | 1,24–3 m dentro il campo; anello cieco, fuori campo e oltre portata si dicono una volta all'avvio | proposta `validazione-3`, correzione C3 |
| Graduatoria | buco > mobile in avvicinamento > occupato > previsto > perso con possibile presenza > in ombra > «nessun ostacolo osservato fino a d metri» | `V2` B7 |
| Larghezza del settore | 10° nelle prove; nella `V2`: **manca** | `risultati_a03_correzione.txt` |

- **Corretto rispetto alla versione 1.** Con «non osservato» sempre in testa, «mobile in avvicinamento» non usciva mai (0 %). Dopo C3: 100 / 100 / 99,5 % con il suolo valido al 100 / 99 / 95 % (200 ripetizioni); 65,6 % all'80 % [SIM], solo nel simulatore dell'avversario.
- **Regola fissa:** mai «via libera» (condizione 9). **Invarianti:** 2, 5.
- **Limiti.** Mai riprovata insieme al resto (`VER` §2). Con buchi persistenti «buco» copre il messaggio utile (`AUD` 6). Un oggetto alto fino a 0,42 m a 0,8 m dà «nessun ostacolo fino alla portata» nel 100 % dei fotogrammi (`f6-specializzazione/03-avversario/ATTACCO_SPECIALIZZAZIONE.md`, S1).
- **Costo:** 3 ore [STIMA] (2 nella versione 1). **Dipende da:** B2, B5.

### B8. Uscita e segnale di «affidabilità persa»

- **Entra / esce.** Entrano i messaggi, il contatore di fotogramma, la quota di celle valide, l'IMU. Escono: in voce un segnale di 0,3 s per stato (C11), la frase «direzione, distanza, stato» solo a stato stabile; a schermo tre colori con l'età e il contatore della latenza; il segnale «affidabilità persa».

| Causa di «affidabilità persa» | Soglia | Ritardo in simulazione | Origine |
|---|---|---|---|
| Nessun fotogramma nuovo, o tre identici | contatore fermo; contenuto uguale | 0,13 e 0,07 s. **I file non concordano su quale cifra a quale causa:** nel torneo 0,13 s è la regola sul contatore e 0,07 quella sul contenuto (`f2/04-torneo/esito_attacchi_parte1.txt`, righe 63–64); nell'attacco 10 «nessun fotogramma nuovo» 0,07 s e «ripetuto con contatore nuovo» 0,13 s (`risultati_a10.txt`) | H-017 (`V1` B8) |
| Poche celle valide | sotto metà della taratura per 3 fotogrammi | 0,13 s | C10 |
| Sensore mosso | IMU a più di 0,5° dalla taratura, o oltre 5°/s | 0,00 s | C10; rumore dell'IMU ipotizzato, non di scheda |

- **Corretto rispetto alla versione 1.** C10: con il 10 % di celle valide, o dopo un urto, nessun segnale in 3 s → 0,13 s e 0,00 s, 0 falsi in 60 s (`risultati_a10_correzione.txt`). C11: la frase finiva a stato già scaduto nel 100 % dei passaggi → 0 % (n = 500; `risultati_a11_correzione.txt`). Entrambe solo nel simulatore dell'avversario.
- **Latenza: [NR]** (K-011; H12). Soglia di R7: 95° percentile ≤ 150 ms dalla marca di cattura alla chiamata audio. Le sole voci note sommano circa 155 ms in media (`VRF` §3c): 95 ms dall'esposizione all'applicazione a 30 fps [realsense-highspeed] https://dev.realsenseai.com/docs/high-speed-capture-mode-of-intel-realsense-depth-camera-d435 ; 22 ms di calcolo; almeno 21,3 ms di audio [pipewire-conf] https://docs.pipewire.org/page_man_pipewire_conf_5.html . Riaperta oggi la prima pagina (con uno strumento che riassume: prova debole): i 95 ms comprendono schermo, scheda grafica e USB, cioè sono un limite superiore per la sola camera.
- **Ipotesi nascoste.** `AUD` 1: con i filtri accesi una mano sul sensore non fa scendere le celle valide; la pagina [realsense-postprocessing] https://dev.realsenseai.com/docs/post-processing-filters/ conferma la persistenza predefinita «valido in 2 degli ultimi 4» e il riempimento dei buchi con un pixel vicino (riaperta oggi, stessa cautela). `AUD` 7: se la camera salta l'1 % dei fotogrammi sono 9 segnali falsi attesi in 60 s.
- **Condizioni:** 1 (autoverifica all'avvio: mano sul sensore, pixel validi sotto il 10 % in 3 fotogrammi, altrimenti il programma non parte), 4 (il criterio dell'IMU vale solo a sensore fermo), 9. **Invarianti:** 8. **Aperte:** K-010 (suoni o battito: tre persone bendate, ≥ 54 stati giusti su 60), K-011, K-015.
- **Costo:** 6 ore [STIMA] (5 nella versione 1). **Dipende da:** B7. **Lo invalida:** una camera che ripete i fotogrammi cambiando il contatore [NV-HW].
- **[PREL]** Con la latenza nota la fascia di 0,40 m copre fino a 0,40 / (0,133 + 0,155) = 1,39 m/s (`f9-preproposta/02-tempo-reale/CONSEGNA.md`).

### B9. Demo e accettazione

- **Che cosa si mostra.** Cinque atti: campo mezzo coperto; ostacolo fermo oltre 1,1 m; attraversamento; passaggio dietro il pannello mentre una seconda persona si muove in vista; sosta, o mano sul sensore.
- **Accettazione.** Sulle registrazioni riprodotte, non dal vivo, con le prove H0–H13 (due persone, circa 2 h 40; H0–H6 nella prima ora perché possono cambiare sensore, portata e luogo; `PM`).

| Parametro | Valore | Da dove viene, stato |
|---|---|---|
| Attore | sulla linea a non più di 2,3 m | C2: a 3 m le tracce confermate erano lo 0,4 % (500 transiti), a 2,3 m il 100 % (`CP`) |
| Pannello, larghezza | 1 m; quello da 0,5 m solo dopo dieci passaggi riusciti sull'hardware | con 0,5 m la previsione conteneva la riemersione nel 14,2–16,5 %, con 1 m nel 97,0–100 % (`M1`, A3) |
| Pannello, altezza | almeno 1,5 m | condizione 3; `AUD` 5 |
| Dietro il pannello | una sola persona | condizione 3 (K-016) |
| Criterio delle 30 occlusioni (H9) | ≥ 28 regge; ≤ 22 smentita; fra 23 e 27 altre 30, e ≥ 52 su 60 | `PM`: il «26 su 30» secco promuoveva una taratura mediocre nel 25,5 % dei casi, i due stadi nel 14,2 % [conto] |

- **Discordanza sulla distanza del pannello.** La `V2` non la fissa: **manca**. Nei file: 1,15 m (C2, «stessa ombra di 1 m»: pannello da 0,5 m); 1,5 m con attore a 2,5 m (`M1`); 1 m di larghezza a 1,9 m con attore a 2,3 m, 1,21 m d'ombra (`M2`: la sola riprovata con le correzioni insieme).
- **Critica nuova [arch.], conto non vagliato.** «Almeno 1,5 m» viene dall'audit, con il pannello a 1,15 m: lì il raggio più alto del campo passa a 1,49 m. A 1,9 m lo stesso raggio passa a 1,67 m: sopra un pannello alto 1,5 m la camera vede, a 2,3 m, tutto ciò che supera 1,56 m, cioè la testa dell'attore. Altezza minima = 1,2 m + distanza del pannello × tan 14°. La smentisce un metro a nastro (H0).
- **Limiti.** La seconda persona dell'atto 4 non è mai stata simulata (`V2` §9); se passa davanti all'attore è un ostacolo mobile, che il nucleo dichiara di non reggere (`AUD` 4).
- **Prossima prova che cambia la decisione** (`VER` §6): H0–H6 più tre controlli (autoverifica dei filtri; celle per stato su 150 fotogrammi della sala vuota; «libero» dentro l'ombra vera), poi H12: circa un'ora e quaranta in due.
- **Costo:** 12 ore [STIMA] (10 nella versione 1). **Dipende da:** tutti i blocchi, un pannello opaco, nastro a terra, un luogo lontano da vetri e finestre.
- **[PREL]** (`T8` §1) Il criterio H9 misura l'identità, non la continuità: passa anche se chi torna non è mai coperto dalla previsione; un buio di 1,1 s non mostra una previsione di 2–5 s.

## 3. I nove invarianti e il loro stato

Un invariante è una regola che deve valere a ogni ciclo, da scrivere come controllo nel codice. Testo dalla `V2` §3; garanzia da `VRF` §2; stato da `CP` §3, `AUD` e `VER` §1.

| # | Regola | Stato oggi |
|---|---|---|
| 1 | «Libero» solo dove il suolo è stato visto in almeno uno degli ultimi 3 fotogrammi; esce con l'età; non si deduce mai | Riscritto e indebolito di proposito (C9). La regola è [COSTR] (premesse: pavimento piano, profondità valida = giusta). **Il margine è [SMENT]:** la `V2` scrive «0,33 m in 0,13 s a 2,5 m/s, meno della fascia»; con la latenza nota sono 0,288 s e 0,72 m, e il margine è zero già a 1,4 m/s (`AUD` 3; `VER`). Aperta K-015 |
| 2 | Buco, fuori campo, oltre portata, anello cieco, ombra: mai «libero» | [COSTR], se un buco arriva come «nessun dato». Nessun «libero» falso in dodici attacchi e 14 400 passaggi: controllo della logica, non dato (`AUD` 2). Lo violano i filtri accesi e il vetro. [NV-HW] |
| 3 | Nessuna uscita «osservato» senza una misura in porta nel ciclo | [COSTR] **in un solo verso**: un rilevamento falso al bordo del pannello uscirebbe «osservato». Mai simulato [NR] |
| 4 | «Previsto» e «possibile presenza» non stanno su celle «libero» oltre la fascia | [COSTR] sull'ombra stimata; su quella vera è una misura. Costo: 28,2 % del suolo visto libero |
| 5 | Nessun timer e nessun modello appreso produce un «libero», toglie un avviso o decide un allarme | [COSTR]. Nella versione 1 il tetto di 10 s lo violava nella sostanza: corretto con C4 |
| 6 | Evidenza negativa solo dove la profondità è valida, e mai sul punto previsto | [COSTR]; riscritto dopo `M1` A7; non attaccato. Tessuti scuri [NV-HW] |
| 7 | Lo strato 1 finisce solo per riaggancio o per celle viste libere | [COSTR] con ostacolo fermo; riscritto senza tetto. Controesempi [SIM]: K-014 (13 su 4800), K-016 (2400 su 2400) |
| 8 | Ogni uscita porta il contatore del sensore | **Necessario, non sufficiente:** servono anche celle valide e IMU (C10). Sulla camera [NV-HW] |
| 9 | Una grandezza non osservabile (massa, accelerazione) non compare in uscita | [COSTR] (interfaccia); non attaccato, nessun caso che lo violi |

Per l'arbitro gli invarianti 2, 5 e 9 sono una «dimostrazione condizionata» alle premesse; 2, 3, 5 e 9 reggono come logica in ogni profilo d'uso; 1, 4, 6 e 7 sono provati solo a sensore fermo, con la griglia che coincide col mondo (`AUD` 12; `VER` §4). **[PREL]** f8 propone un decimo invariante sulla continuità e di riscrivere il 6 e il 9 (`T8`, C-014).

## 4. Costo, dipendenze, condizioni

| Blocco | B1 | B2 | B3 | B4 | B5 | B6 | B7 | B8 | B9 | Totale |
|---|---|---|---|---|---|---|---|---|---|---|
| Ore-persona, versione 2 (`V2` §2) | 3 | 6 | 6 | 5 | 9 | 4 | 3 | 6 | 12 | **54** |
| Ore-persona, versione 1 (`V1` §2) | 3 | 6 | 5 | 5 | 8 | 4 | 2 | 5 | 10 | 48 |

- **Tutte [STIMA]**, senza prova (`V2` §9), e senza l'integrazione.
- **Ore in fila: due cifre.** B1 → B2 → B3 → B4 → B5 → B7 → B8 in serie fanno 38 ore (`AUD` 8). [PREL] Con corsie parallele e dati finti dietro le interfacce: 26,8 ore in fila, e 59,5 ore-persona probabili (39–115) con l'integrazione (`f9-preproposta/11-pianificatore/CONSEGNA.md`). Contro 14 ore e 5 persone (sesto e settimo addendum) comanda la catena, non il numero di mani.
- **Che cosa si può tagliare.** Per l'audit: B6, lo strato 2, l'assegnazione ungherese, la regola «si muove» fine; senza B2, il cuneo e i contatori di B8 non c'è demo (`AUD` 8). **[PREL]** Dopo il quarto addendum lo strato 2 non si taglia più: è la continuità visiva (`T7` §6).
- **Mai provato** (`V2` §9; `VER` §2). Provate insieme da un altro autore: C1, C4, C5, C6, C8, media di 3 fotogrammi, rilascio cella per cella, geometria nuova (`M2`). Solo nel simulatore dell'avversario: C3, C9, C10, C11. Senza prova: «non confermato», «metà dell'area del cuneo», la seconda persona dell'atto 4, B7 e B8 nell'insieme, il canale laterale dei sensori a tempo di volo (un conto d'aree: la camera vede il 20,0 % del disco di 3 m, tre sensori da 60° aggiungono il 22,2 %; `CP` attacco 12; [st-vl53l7cx] https://www.pololu.com/file/0J1992/vl53l7cx.pdf ). E tutto ciò che dipende dal sensore vero.

**Le nove condizioni del verdetto** (`VER` §4): (1) filtri della camera spenti e autoverifica all'avvio; (2) fascia a formula, v_max · (età + latenza) più l'errore d'ombra, oppure velocità coperta dichiarata (circa 1,4 m/s); soglie in secondi; (3) pannello alto almeno 1,5 m e largo 1 m, attore a non più di 2,3 m, una sola persona dietro; (4) profilo «sensore fermo» dichiarato: nessuna soglia vale in moto; (5) C6 obbligata, con il suo costo; (6) garanzia solo per chi è stato visto almeno 4 fotogrammi, con una traccia pendente e ostacolo fermo; (7) limiti scritti: rilevamenti mancati vicino all'ombra, secondo soggetto, vetro, ostacoli bassi sotto 1,09 m, sole; (8) regola per l'ombra propria fissata prima del codice; (9) la dicitura «provato solo in simulazione, a sensore fermo», e mai «via libera».

## 5. File letti

- **Per intero:** `ADDENDUM_UTENTE.md`; `CONTRATTO.md`; i quattordici file delle sigle in testa; `f9-preproposta/01-architetto/CONSEGNA.md`; `f9-preproposta/11-pianificatore/CONSEGNA.md`.
- **File grezzi ricontrollati** (le cifre citate tornano): `risultati_a01.txt`, `_a03_correzione`, `_a04`, `_a05`, `_a09`, `_a10_correzione`, `_a11_correzione`; `v2_PD.txt`, `v2_SECOND.txt`, `v2_WALLP.txt`, `bis_FURTO.txt`, `v2_C6.txt` (prime 20 righe). Per ricerca: `risultati_a10.txt`, `f2/04-torneo/esito_attacchi_parte1.txt`.
- **In parte:** `f3/H-012/H-012.md` (righe 1–60); `f2/03-triage/TRIAGE.md` (fatti F-001…F-008); `f6-specializzazione/` (tre intestazioni); `f9-preproposta/` (intestazioni delle consegne 02, 05–10, 12; di 02 anche le righe sulla latenza); `f10-dati/CONTRATTO_DATI.md` (inizio).
- **Non letti:** f1; il torneo di f2 (citato attraverso `VRF` e `SEL`: cifre di seconda mano); le consegne dei singoli ruoli di f7 e f8; il resto di f10.

## 6. Chiavi di riferimento usate

I link sono nel testo, accanto alla chiave.
- **Riaperte oggi da me**, con uno strumento che riassume la pagina (prova più debole di una lettura del testo): [realsense-tuning] (le tre frasi citate in `VRF` ci sono; la formula è un'immagine, non letta); [realsense-postprocessing]; [realsense-highspeed] (tabella 4: 127 / 95 / 47 / 39 ms a 15 / 30 / 60 / 90 fps, modi 848×100; autori non indicati); [pipewire-conf] (frequenza 48000, quanto 1024).
- **Verificate da `sciame-fonti` in `FON`, non riaperte da me:** [realsense-confronto]; [orbbec-gemini335] (link: manca); [roboflow-rfdetr]; [ultralytics-yolo26]; [bewley2016] (Bewley, Ge, Ott, Ramos, Upcroft, SORT, ICIP 2016); [cao2023] (Cao, Pang, Weng, Khirodkar, Kitani, OC-SORT, CVPR 2023); [scholler2020] (Schöller, Aravantinos, Lay, Knoll, IEEE RA-L 5(2), 2020); [st-vl53l7cx] (STMicroelectronics, DS13865 Rev 6, copia ospitata da Pololu).
