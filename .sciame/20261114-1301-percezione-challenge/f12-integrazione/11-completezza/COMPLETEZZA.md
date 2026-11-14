# Completezza e coerenza della versione 3 — controlli C-A e C-B (`sciame-logico`, f12, 11-completezza)

14 novembre 2026, dalle 18:09:00 alle 18:23 (`date -Is`). Accanto: `PREVISIONI.md`, scritte prima di aprire V3, la tabella dell'autore, SCH e PIA. Sigle: **V3** `01-soluzione/SOLUZIONE_V3.md`; **SCH** `05-schermo/SCHERMO_E_DEMO.md`; **PIA** `04-piano/PIANO_14_4.md`; **VN, V7, V8, V9, VD** i cinque verdetti; **AS** l'attacco alla specializzazione; **AU** l'audit. Percorsi relativi a `.sciame/20261114-1301-percezione-challenge/`.

## 0. In testa

**Esito. C-A non regge alla lettera: 149 voci nel mio elenco, 120 presenti e conformi, 12 escluse con il motivo, 15 con una regola che non dice ciò che il verdetto chiede, 2 mancanti. C-B non regge: 13 incoerenze fra regole, 7 uscite non definite su 16 combinazioni, 8 parametri su 22 con due valori, 5 contraddizioni aperte non nominate e 3 senza prova.** Due difetti toccano la sicurezza del «libero» (B5, B13) e cinque la continuità (B1–B4, A9). Si riparano con modifiche di testo, salvo i quattro punti del §4, che aspettano l'arbitro.

**Cambi di stato proposti:** nessuno. **Prova nuova mia:** un conto geometrico (B13), con il comando. Il resto è lettura e ricerca testuale (`grep`): **verificato per lettura** sui file nominati, non misurato.

**Prova sull'identità: consegnata alle 18:18, controprova non ancora consegnata.** `06-identita/IDENTITA_SU_PROFONDITA.md` alle 18:15 non c'era e alle 18:19 sì (`ls`); `07-controprova-identita/` alle 18:22 ha il codice, non `CONTROPROVA_IDENTITA.md`. L'ho letta fino al §3 e la uso nel §4. Finché mancano la controprova e l'arbitro tratto la «stessa identità al ritorno» come **smentita su profondità realistica e in correzione** (VD §1, H-404).

**Scostamenti.** (1) Letti per intero: contratto d'integrazione, VN, V7, V8, V9, VD, V3, SCH, PIA. In parte, con righe tagliate a 300–700 caratteri: AU §1, gli addendum 1–8 (la lettura del coordinatore), AS (C1–C8), la tabella dell'autore. Solo per ricerca testuale: modifiche e controprove di f8, controprove di f7, `SOLUZIONE_V2.md`. Non aperti: tornei, banchi, `DECISIONE.md`, la specializzazione, `MOTO_PROPRIO.md`, gli altri file di f10, i due documenti di `documentazione/`. (2) Di `02-prova-insieme` e `03-libero`, consegne di f12 **non vagliate dall'arbitro**, ho letto le teste: le uso nel §4. (3) La grana delle 149 voci è mia. (4) Le previsioni non sono cieche rispetto ai verdetti. **Regole violate:** nessuna che io sappia (niente git, rete, sudo; scritture solo in questa cartella). *Indipendenza:* condivido con l'autore il modello linguistico e i verdetti; non la sua tabella, aperta dopo aver chiuso il mio elenco.

## 1. C-A, completezza

**Il mio elenco, per fonte (voci):** VN 12; AU 12; V7 24; V8 35; V9 14; AS 8; VD 27 (F-401…F-413, sette condizioni riviste, quattro cambi di stato, «da non dire», due gruppi di prove); addendum 8; R1–R8 con la loro mappa 9.

**Mancanti (2).**
- **A1.** La mappa requisito → blocco → misura per R1–R8: in V3 «R1»…«R8» compaiono 0 volte (`grep`). VN dava la completezza «verificata come mappa» sulla versione 2; i blocchi sono cambiati («perso» è uscito, 1.6 e 1.12 sono nuovi) e la mappa non è stata rifatta. SCH lega gli atti alle frasi della traccia, non ai blocchi.
- **A2.** «Nessuna funzione d'ingaggio o di puntamento» (priorità 5 del contratto; primo e secondo addendum): 0 occorrenze di «ingaggio» e «puntamento» in V3, SCH e PIA. V3 ha solo «nessuna uscita è un comando».

**Presenti, ma la regola non dice ciò che il verdetto chiede (15).**
- **A3, A4. Posa (VD condizione 4; F-404).** V3 §1.1 scrive «oltre 1° NON PARTE». VD chiede «meno di 1°», e il controesempio F-404 sta proprio a +1° (7 celle su 7). La prova d'ingresso (oggetto di 10 cm a 2,5 m «occupato») in V3 è una «prima misura col sensore», non un cancello dell'avvio. Conto al §2, B13.
- **A5. F-413.** V3 conta le celle che ricevono suolo (giusto), ma dichiara ancora «suolo solo da 1,24 m» (§1.1, §7; SCH, schermata d'avvio): a ±44° VD dà 1,69 m.
- **A6, A7. Dicitura (V8, condizione 9; C1).** La «frase della prova» di V3 §3 dà «almeno 9 casi su 10 fino a 2 secondi» senza «a camera ferma» e senza il limite che V8 §4.5 impone finché c3 non è provata («con la maschera esatta»). Il dominio completo sta solo nel §7.
- **A8. `statistico-5`.** Fra 2 e 3 s V3 §1.6 scrive «almeno 8 su 10», V3 §7 e SCH «almeno 85 su 100» (`interfacce-K2`, non nominata in V3).
- **A9. Decima condizione e `sd-0`.** Il livello di V3 §1.6 non dipende dal predittore. V8 §5: `sd-0` tiene 0,90 solo in 37 celle su 45 fino a 2 s. PIA mette nel minimo solo `sd-0` (`sd-1` è B4*, taglio 4): «almeno 9 su 10» uscirebbe col predittore che non lo sostiene.
- **A10. (c) di V7.** V3 §1.5 mette «affidabilità persa» fra le chiusure; V7 chiede che le tracce «continuino in previsione» (B1). La stringa è «ampio, non aggiornata» in V3, «dedotto, sensore non affidabile» in V7, SCH e PIA.
- **A11, A12. c2 e VD condizione 6.** «Una sola traccia pendente» è falsa su profondità realistica (7–66 fantasmi per passaggio): V3 lo registra in §1.8 ma non ne trae la regola (§2, B2).
- **A13. S6.** Le correzioni di V9 («riferite al punto protetto», «guardia per l'oggetto fermo») e K-305 non sono in V3 (0 occorrenze).
- **A14–A17. «Da non dire» (V7 §6, V8 §7, V9 §6, VD §5).** Nell'elenco di V3 §3 mancano almeno 15 frasi (`grep`: 0): «ispezione», «detect and avoid», «UAV», «conforme a», «il vetro è risolto», «in cinque ci sta», «continuità garantita», «la preproposta è stata adottata», «30 prove bastano», «l'ellisse al 95 %», «riconosce la sosta», «TA/RA», «anti-bird strike», «soglia 40» senza la risoluzione, «validato su dati veri». SCH §7 ne ha tredici, nessuna delle due di VD.

**Escluse con il motivo (12):** mappa voxel; V-016, V-017, V-019 e T-008 (4 ore); c10; `statistico-7`; S7; S9; le correzioni di F-401, F-402 (occlusore), F-408, F-409, F-411, F-412 («non provate», V3 §4). Il motivo regge, ma V3 non ne scrive il prezzo: finché restano fuori, sulle sequenze simulate di f10 l'identità al ritorno tiene in 0 passaggi su 90 e il pannello è «mobile» in 79 su 90 (VD).

**Voci della tabella dell'autore che nei verdetti non ci sono:** nessuna trovata; due regole senza sigla le ho ritrovate alla fonte (`MODIFICHE_CONTINUITA.md`, riga 66; `CONTROPROVE_MODIFICHE.md`, riga 40). Composizioni dell'autore, da mostrare all'arbitro: il cancello «oltre 1° non parte»; la scelta provvisoria di `sd-K3`; «tagliato» senza sensore (fonte **non verificata** da me). **Voci escluse senza motivo:** nessuna.

## 2. C-B, coerenza

**Stati e transizioni della traccia, come risultano da V3 §1.4–§1.9** (solo le righe con un difetto).

| Da | Evento | A | Difetto |
|---|---|---|---|
| tentativa | 3 misure su 5 (§1.4) / «vista almeno 4 fotogrammi» (§1.5) | osservato | **due soglie di conferma** |
| tentativa, senza misura | entro 0,75 m da un'ombra (c7) | nessuna traccia, avviso acceso | nessun segno a schermo |
| osservato | gruppo tagliato | «visto in parte» **e** ENTRATA subito (c4) | due regole (B3) |
| osservato | senza misura, vicino al vuoto o al bordo del campo (C2) | avviso sul non osservato | **stato della traccia non scritto** |
| osservato | senza misura, campo aperto | «non confermato» 0,2 s, poi chiusa | nessuna forma in §1.10 né in SCH |
| previsto | oltre l'80 %, pavimento, oltre 3 s, sotto 0,3 m/s, dati degradati | previsto ampio | il ritorno da «ampio» a «previsto» non è scritto (SCH: non torna) |
| previsto, ampio | misura fuori soglia, o più pendenti | (2) «identità ambigua» | chiusa (§1.5) o «resta previsto ampio» (§1.8)? (B1) |
| ogni stato | sensore non in salute | (4) / «ampio, non aggiornata» | chiusa (§1.5) o continua (§1.9)? (B1) |
| previsto, ampio | ombra vista libera | chiusa (3) | con l'occlusore fermo: mai (`SOLUZIONE_V2.md`, riga 26) |
| previsto, ampio | membri oltre portata o campo | chiusa (5), l'avviso resta | la condizione sta in M, non in V3 |

**Uscite a schermo: 8 stati × salute sì / no = 16 combinazioni; 9 definite, 7 no.** Non definite: traccia tentativa (2); «non confermato» (2); ramo C2 (2); traccia osservata in campo aperto quando il sensore cade e torna (1): la regione dilatata ∩ «non osservato» può essere vuota, e il «pavimento» di §1.6 presuppone un'ombra. Età: definita fino a 3 s, salvo A8; non è scritto da quando si conta «non visto da Y s» se il soggetto è «visto in parte» (in SCH quasi 1 s, metà dell'orizzonte).

**Stato senza uscita.** Dopo un'«identità ambigua», con l'occlusore fermo, la vecchia traccia e il suo avviso non hanno più uscita: (3) non avviene mai, restano (4) e (5). È voluto per l'avviso (priorità 2); per la traccia va scritto, con il contatore di c2 e chi lo azzera (`sd-K3`). Costo noto: 87 / 117 / 95 pendenti a fine sessione prima di c2 (V8 §2).

**Incoerenze fra regole (13).**
- **B1.** Chiusure (2) e (4): §1.5 le chiama chiusure; §1.8 e §1.9 tengono la traccia in «previsto ampio». I10 promette la regione «fino a una chiusura»: letta con §1.5, durante la perdita del sensore non esce niente, cioè i 30 cicli muti che V7 (c) vieta.
- **B2.** c2 («più pendenti: un avviso, senza predittore») ↔ I10 e priorità 1, quando le pendenti sono fantasmi (VD: 7–66 per passaggio; §1.4: con due pendenti l'identità non si dà mai). Su profondità realistica ogni passaggio finirebbe senza regione prevista. Con c7 in più, ogni fantasma chiuso entro 0,75 m da un'ombra accende un avviso che niente toglie. **Non nominata in V3 §5** (`logico-K1`). Decide: pavimento vuoto e pannello fermo, 30 s, sulle sequenze simulate di f10: avvisi accesi e tracce pendenti senza persona (soglia 0).
- **B3.** «Visto in parte» è uno stato della traccia (§1.5, elenco) ↔ «gruppo tagliato → ENTRATA subito»: va scritto che contorno e regione coesistono e da quando parte l'età.
- **B4.** «Non confermato» ha due significati (§1.5: confermata senza misura; c7: non ancora confermata).
- **B5.** «Libero» della cella (§1.2): le regole sono in ordine, e una cella con 1–2 pixel a quota d'ostacolo e un pixel di suolo esce «libero», mentre l'elenco del «non osservato» cita «1–2 pixel». Due righe decidono lo stesso caso in modo diverso.
- **B6.** Rilascio «oltre la fascia» (§1.7, I7): R100 è «cuneo più 0,40 m», quindi nessuna sua cella è oltre la fascia. Va scritto da che cosa si misura.
- **B7.** Dopo il ritorno del sensore §1.9 dilata «la regione» di v_max·T: se è la sola R90 viola I4 (R90 ⊆ R100); va detto che si dilata anche R100.
- **B9.** Livello basso: V3 «suolo visto libero fino a d m», d ≤ 3 − 0,40 = 2,6 m (I12) ↔ SCH «NESSUN OSTACOLO OSSERVATO FINO A 2,7 m» (due volte). V3 sceglie V7 (`sd-K2`); SCH non l'ha seguita, e 2,7 supera il tetto. La soglia di C-D (mediana ≥ 2,7 m) va quindi misurata prima del taglio di I12, e va scritto.
- **B8, B10 (minori).** `sd-1` «pesa un decimo a ogni ciclo» ↔ V9, S4a, «pesi non cumulati»: va scritto se il decimo si moltiplica. Banda: V3 dà per settore «il livello più alto», SCH «li mostra tutti e due» finché K-306 è aperta.
- **B11.** Fascia: V3 §1.7 tiene 0,40 m «onesta fino a 1,4 m/s» e, sotto, la formula di C4. Con i 155 ms stimati la formula dà 0,20 + 0,20 + 1,4 · 0,288 = 0,80 m. Il valore 0,40 è una costante in R100, I4, I12, §1.5 e §1.8: alla prima misura della latenza cambiano tutti. K-015 è nominata; l'effetto no.
- **B12.** Tabellone: 30 passaggi per cella e «≥ 28 regge» (V3 §1.12) ↔ «50 per riga» (SCH, V8 §5) ↔ «almeno 90 passaggi» (PIA §2). V3 stessa nota che 28 su 30 non mostra il 90 %.
- **B13 (conto mio).** `f10-dati/ambiente/venv/bin/python -I -c "…atan((h−0,07)/d)…"`: perché un oggetto di 10 cm resti sopra la soglia di 0,07 m l'errore d'inclinazione deve stare sotto 0,69° a 2,5 m e 0,57° a 3 m; con 1° legge 5,6 e 4,8 cm. Per 15 cm a 3 m bastano 1,53°. Modello: piano e raggio ideali, nessun rumore. Il cancello a 1° lascia quindi passare gli ostacoli di 7–12 cm oltre 2,5 m.

**Invarianti.** Tutti e 14 hanno un controllo scritto; I13, I12 e I5 non hanno in PIA un compito che lo esegua. Il controllo di I3 ha soglia 0, e VD dà 8 passaggi su 90 con «osservato» a soggetto nascosto: cade finché F-402 resta fuori. In tensione: I10 ↔ c2 (B2); I4 ↔ §1.9 (B7); I12 ↔ SCH (B9). Nessuna coppia si contraddice alla lettera.

**Parametri: 22 controllati, 14 con un solo valore** (fra questi le fasce di 0,40 e 0,20 m, la soglia dell'80 %, gli orizzonti di 2 e 3 s, 0,3–1,8 m/s, la distanza del pannello e dell'attore), **8 con due:** scritta fra 2 e 3 s (A8); conferma (3 su 5 / 4 fotogrammi); stringa e d del livello basso (B9, due parametri); n del tabellone (B12); predittore del minimo (`sd-0` in PIA, «previsione sd-1» nella riga fissa di SCH); stringa del sensore non in salute (A10); altezza del pannello (V3 «almeno 1,7 m, 1,8 m se c'è»; SCH «almeno 1,7 m»; VD propone 1,8 m; PIA non la scrive).

**Contraddizioni aperte su regole adottate.** Le righe di V3 §5 nominano 27 sigle: 24 con la prova, 3 senza. **Non nominate (5):** K-003 (q = 0,2 adottato; VD: «aperta con la catena su profondità», decide 0,1 su `exp2`); K-216 (velocità nella porta di M7); K-305 (orizzonte dell'etichetta di S6); K-404 (V3 scrive l'errore del bordo «verso il largo», VD chiede di riformulare: al limite da −65 a +73 cm); K-406 (tolleranza del suolo 5 cm ↔ soglia d'ostacolo 7 cm, tutte e due in §1.2; decide il pavimento vuoto a ±0,5°). Più `logico-K1` (B2). **Senza prova (3):** K-016, K-214, K-108 (solo «D»).

## 3. Piano e schermo

**PIA, un compito per blocco: 10 blocchi su 12.** Mancano: il controllo all'avvio con la configurazione dichiarata (1.1; per V9 è «14 ore»); la marca «tagliato» senza sensore e la regola «mobile» (1.3), da cui dipendono B3a e B3b: c'è solo A4*, fuori dal minimo. **Prove chieste: 14; con un compito pieno 6, in parte 5, senza 3.** Senza: pannello sul suolo segnato, 150 fotogrammi (VD §6, K-014); 60 s a vuoto e sotto carico (AU 7); prove con tre persone (V9, S5). In parte: la prova senza sensore di VD §6 (A4* non ne porta il criterio); posa e oggetto di 10 cm; 30 passaggi col metro e mano sul sensore (PIA: 10, senza metro); stanza ferma 60 s; latenza (solo in riproduzione). PIA e SCH sono scritti prima di VD, e lo dichiarano.

**Tre punti del piano che toccano la priorità 1.** (i) La demo più probabile è la riproduzione di sequenze simulate di f10, dove le regole adottate tengono l'identità in 0 passaggi su 90; la correzione (A4*) è fuori dal minimo. (ii) Il criterio «fatto» di B3b («con l'estraneo nessun avviso rilasciato senza averlo visto») non è raggiungibile con nessuna regola adottata: K-016 non è riparata (V8) e la prova C-C lo dà caduto (§4). B3b è sul percorso critico. (iii) SCH non taglia mai l'atto 6; senza camera l'atto 6 vive di D4°, che PIA taglia (taglio 7). Le due scalette (PIA §9, cinque passi; SCH, nove atti) non coincidono.

**SCH mostra ciò che V3 non produce (4):** «NESSUN OSTACOLO OSSERVATO FINO A d» e d = 2,7 m; due livelli insieme nella banda; «dedotto, sensore non affidabile»; «almeno 85 su 100». In più la targhetta «P1» in «previsto ampio» (proposta `interfacce-K1`; V3: «nessun punto»). **V3 produce ciò che SCH non mostra (3):** traccia tentativa, «non confermato», ramo C2. Nella schermata d'avvio di SCH mancano i limiti aggiunti da VD alla condizione 7: ostacolo che non rimanda segnale (F-405), ostacolo sospeso (F-410), posa (F-404).

## 4. Che cosa cambia VD, e che cosa cambiano le prove di f12 già consegnate

**VD cambia voci in tutti e tre i documenti.** In V3 è entrato con ritocchi: restano A3–A5, A12, A17, K-003, K-404, K-406. In SCH e PIA non è entrato: pannello, limiti, «da non dire», le tre misure col sensore.

**Consegne di f12 non ancora vagliate dall'arbitro, che contraddicono regole di V3** (cifre degli autori, non ricontate da me):
1. `03-libero`: «un pixel dell'impronta valido» (V3 §1.2, regola principale) dà una cella libera con un corpo sotto in 98 fotogrammi su 7200, e in 900 su 900 se il corpo non rimanda segnale; il ripiego a 0,20 m da solo cade (15 648 celle). Regge una variante più prudente (`nuvole-1`), scelta dopo il primo lancio, un autore.
2. `02-prova-insieme`: con c1 l'estraneo prende l'identità e l'avviso cade nel 0,995 / 0,966 / 0,913 dei casi. Per la condizione scritta in V3 §1.8, c1 allora **non entra** e resta la soglia del nucleo, con cui il riaggancio cade (102 su 273 in demo, V8).
3. `02-prova-insieme`: «almeno 9 su 10 fino a 2 s» regge nelle due geometrie larghe e **cade nella geometria della demo** con il corpo esteso: lì si può dire «almeno 88 su 100 a 1 s», poi nessuna cifra. La scritta di V3 §1.10 e la frase del §3 sono quelle che lo schermo mostrerebbe in demo.
4. `06-identita` (senza controprova): il criterio di VD §6 con le correzioni come proposte **cade** (un caso a 0 passaggi su 30 a 424 pixel, 16 su 30 a 848), e la soglia proporzionale di F-401 mette «libero» nell'ombra vera (98 e 91 celle·fotogramma): l'esclusione di V3 §4 ne esce sostenuta. Una correzione scelta dopo i dati (`tracciamento-1`) passa su semi nuovi alle due risoluzioni (29–30 su 30) solo nella geometria del catalogo: 0 e 1 su 10 con la persona a 0,3 m dal pannello, 0 su 10 col rumore «limite». Con F-409 la persona nascosta non è mai fuori dall'avviso, ma dietro un pannello fermo l'avviso non si spegne più (140 passaggi su 140): è lo stato senza uscita del §2. A 848 pixel e rumore «limite» la catena invariata dà 4 celle·fotogramma «libero» nell'ombra vera: lo «0 casi» di K-014 valeva a 424 pixel.

## 5. Correzioni obbligate, in ordine (prima la sicurezza, poi la continuità, poi il resto)

1. §1.2: il «libero» riscritto con l'esito di C-D, quando l'arbitro lo fissa; intanto «libero» richiede zero pixel validi a quota d'ostacolo nella cella (B5).
2. §1.1: posa «sotto 1°» più la prova d'ingresso di VD come condizione di partenza, oppure il limite dichiarato «con 1° gli ostacoli sotto 12 cm oltre 2,5 m non sono garantiti» (A3, A4, B13); 1,24 m al centro e 1,69 m ai bordi (A5).
3. §1.8, §1.3, §4: l'esito del cancello su c1 e la cifra del riaggancio che ne segue; K-219 e K-016 con la prova; l'esito di `sd-K4` e il nuovo caso di K-014. Nessuna correzione scelta dopo i dati entra senza controprova.
4. §1.5, §1.8, §1.9: (2) e (4) non chiudono la traccia; definire la «pendente ambigua», il contatore e chi lo azzera (B1).
5. §5: `logico-K1` con la sua prova (B2); K-003, K-216, K-305, K-404, K-406; la prova per K-016, K-214, K-108.
6. §1.6, §1.10, §3: livello per predittore e per geometria; una sola scritta fra 2 e 3 s; frase della prova con «a camera ferma» e «con il bordo dell'ombra esatto» (A6–A9).
7. §1.5, §1.10, SCH: forma e parola per traccia tentativa, «non confermato» e ramo C2; «visto in parte» con la regione, e l'origine dell'età; una sola soglia di conferma (B3, B4).
8. §1.7, §1.9: da dove si misura «oltre la fascia»; R100 si dilata con R90; la fascia come simbolo (B6, B7, B11).
9. §3: le 15 frasi «da non dire»; «nessuna funzione d'ingaggio o di puntamento»; la mappa R1–R8 → blocco → misura; le correzioni di S6; i pesi di `sd-1` (A1, A2, A13–A17, B8).
10. SCH: «suolo visto libero fino a d m», d ≤ 2,6 m; un livello per settore; stringa del sensore; limiti e «da non dire» di VD; pannello 1,8 m; il predittore in uso nella riga fissa (B9, B10).
11. PIA: compiti per il controllo all'avvio e per «tagliato»; le tre misure di VD §6 nelle istruzioni di registrazione; la correzione dell'identità nel minimo, o la demo dichiarata «identità in correzione»; criterio «fatto» di B3b riscritto; una scaletta e un n del tabellone (B12, §3).

## 6. Esito dei controlli ed esito delle previsioni

- **C-A: non regge** (si chiude con le correzioni 2, 4, 5, 6, 9). 149 voci: 120 conformi, 12 escluse con il motivo, 15 non conformi, 2 mancanti; 0 aggiunte non approvate; 0 escluse senza motivo.
- **C-B: non regge.** 13 incoerenze; 7 uscite non definite su 16; 1 stato senza uscita da dichiarare; 8 parametri su 22 con due valori; 24 contraddizioni nominate con la prova, 3 senza, 5 non nominate (più `logico-K1`).
- **Piano e schermo: in parte.** 10 blocchi su 12 e 6 prove su 14 con un compito pieno; 4 uscite di SCH che V3 non produce, 3 stati di V3 senza segno.

Previsioni (`PREVISIONI.md`, 18:09): P1, P3, P4, P6 reggono (17 voci contro la soglia 3; 8 parametri contro 2; 7 uscite non definite); **P2 smentita** (F-408, F-409, F-412, F-413 hanno tutte un paragrafo); **P5 smentita** (4 uscite, ne prevedevo al più 1).

**Dopo.** L'autore applica le correzioni 4–9 (solo testo). L'arbitro fissa i quattro punti del §4, con la controprova sull'identità; poi si chiudono 1, 3, 6, e questo controllo si rifà sulle sole voci toccate.
