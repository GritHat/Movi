# Rifà CIFRE.md dalle righe della prima stesura (40-documento/CIFRE.md), aggiornate al testo finale. Uso: python3 -I fai_cifre.py
old=open('../40-documento/CIFRE.md',encoding='utf-8').read().split('\n')
rows=[r for r in old if r.startswith('| ') and not r.startswith('| Cifra')]
def drop(key):
    global rows; n=len(rows); rows=[r for r in rows if not r.startswith('| '+key)]; assert len(rows)==n-1,key
def sub(key,a,b):
    for i,r in enumerate(rows):
        if r.startswith('| '+key):
            if a not in r: print('NON APPLICATA:',key,'|',a[:50]); return
            rows[i]=r.replace(a,b); return
    print('RIGA MANCANTE:',key)
drop('1,22 m; 1,69 m'); drop('9 (persone)'); drop('quattro su nove')
S=[
('0,5°','«posa … nota entro 0,5°» (riquadro; tabella 1, ultima riga)',"«posa della camera nota (inclinazione entro 0,5°)» (riquadro); «se l'inclinazione è nota entro 0,5°» (§1); tabella 1, ultima riga"),
('0,5°','VI testa, cambio 5, e §5 condizione 4; CH §1 (c)',"VI testa, cambio 5, e §5 condizione 4 («posa»); V3 §1.3 («errore d'inclinazione entro 0,5°»); CH §1 (c)"),
('1,24 m; 1,7 m','[C] conto geometrico, campo di 58°','[C] conto geometrico, campo di 58° (DF, geometria 2: 1,71–1,73 m ai lati). **Non scritta nel testo:** la coppia 1,22 m e 1,69 m, che vale con f = 424 px (campo 59,0°)'),
('10 su 10 (prove)',"«tolto l'ostacolo, l'avviso resta acceso (10 prove su 10)»","«tolto l'ostacolo e rivisto il suolo, l'avviso non si spegne (10 prove su 10)»"),
('15°','verso il basso','in basso'),
('400','«ricavata da 400 percorsi registrati di persone» (§2)','«viene da 400 percorsi di camminatori simulati, lo stesso generatore delle prove» (§2)'),
('400','V3 §1.6, predittore `sd-1`','V3 §1.6, predittore `sd-1`; verdetto sulla continuità (f8), riga 31: libreria e passaggi dallo stesso generatore'),
('0 su 23 402; 6,4 su 10 000','«0 interruzioni su 23 402 passaggi, meno di 6,4 su 10 000» (§3)',"«0 interruzioni su 23 402 passaggi» (§1, marca dell'obiettivo)"),
('0 su 23 402; 6,4 su 10 000','[S] sensore ideale [R]; per costruzione la regola','[S] sensore ideale [R]; per costruzione la regola. **Non scritto nel testo:** i camminatori distinti sono 6 000, quindi «meno di 6,4 su 10 000»'),
('0 su 23 402; 6,4 su 10 000','| 0 su 23 402; 6,4 su 10 000 |','| 0 su 23 402 |'),
('24 su 23 402',"«l'avviso può non nascere (24 passaggi su 23 402)» (§3)","«l'avviso può non nascere (24 passaggi su 23 402 con la regola che lo cura, che parte spenta; 928 senza)» (§3)"),
('24 su 23 402','[S] [R]; 928 senza la regola che lo cura, che parte spenta (non scritto nel testo)','[S] [R]; la regola (c7) parte spenta: VI §3 e §5 condizione 5'),
('24 su 23 402','| 24 su 23 402 |','| 24 su 23 402; 928 |'),
('6–8 su 10','«Chi svolta o esce dal lato lontano: 6–8 casi su 10» (§3)','«Chi svolta o esce dal lato lontano: circa 6–8 casi su 10 a 2–3 s» (§3)'),
('6–8 su 10','[S] controesempio in simulazione','[S] controesempio in simulazione; V3 §3 vieta una cifra per chi svolta, VI la dà: seguo VI (dubbio 1 nel testo)'),
('3–5 su 10; 1 s',"«Bordo dell'ombra stimato, non noto: 3–5 su 10 a 1 s» (§3)","«Bordo dell'ombra stimato e non dato: 3–5 su 10 a 1 s» (§3)"),
('3 s |','«oltre 3 s: nessuna cifra» (§3)',"«oltre 3 s: nessuna cifra, resta l'avviso» (§3)"),
('2 983 su 4 552','«la traccia non è nello stato «previsto» in 2 983 fotogrammi su 4 552» (§3)','«il segno «previsto» manca in 2 983 fotogrammi su 4 552, circa due su tre» (§3)'),
('2 983 su 4 552','a 848 px: 2 968 su 4 553','a 848 px: 2 968 su 4 553; «due su tre»: conto mio, 2 983 / 4 552 = 0,655'),
('300; 9 000; due (lanci)','«(300 condizioni, 9 000 fotogrammi, due lanci, camera ideale)» (§4.1)','«(camera ideale, cioè profondità calcolata dalla geometria: 300 condizioni, 9 000 fotogrammi, due volte)» (§4.1)'),
('300; 9 000; due (lanci)','VI §7 affermazione 4 e §1 riga C-D','VI §7 affermazione 4 e §1 riga C-D; camera ideale: `03-libero/PREVISIONI.md` riga 9 (camera a foro, rumore k·z²)'),
('3 m; 0 su 4 324; 0 su 3 608','(0 fotogrammi su 4 324; 0 su 3 608 in una replica)','(0 fotogrammi su 4 324; replica: 0)'),
('3 m; 0 su 4 324; 0 su 3 608','424 px (0 su 4 325 a 848 px)','424 px (0 su 4 325 a 848 px); **non scritto:** la replica è 0 su 3 608'),
('3 m; 0 su 4 324; 0 su 3 608','| 3 m; 0 su 4 324; 0 su 3 608 |','| 3 m; 0 su 4 324; 0 (replica) |'),
('176 su 180; 94–99 %','«con la correzione 176 su 180 (94–99 %)»','«con una correzione che parte spenta, 176 su 180 (94–99 %)»'),
('176 su 180; 94–99 %','174 su 180 a 848 px','174 su 180 a 848 px; interruttore spento di norma: VI §5 condizione 13'),
('19 su 20','«prende il nome (19 volte su 20)»','«prende il numero (19 volte su 20)»'),
('3 m; 1,44 m/s; 1 s','«I 3 m di portata bastano … fino a 1,44 m/s (reazione di 1 s: ipotesi)» (§4.5)','«I 3 m di portata bastano … fino a 1,44 m/s, con 1 s di reazione (ipotesi)» (§4.4)'),
('1,13 m/s','(§4.5)','(§4.4)'),
('0,40 m','(§2; §4 punto 5)','(§2; §4 punto 4)'),
('360°; 180°','«Tre sensori a tempo di volo per 360°. Coprono 180° (scheda del costruttore)» (§5)','«Tre sensori a tempo di volo per 360°. Coprono 180°» (§5)'),
('80 505 su 146 901','[S] letto in V3, non ricontato','[S] letto in V3, non ricontato; 0,548 (conto mio), non scritto'),
('0 su 140','«0 su 140 con la correzione, nel suo dominio» (tabella 1)','«0 su 140 con una correzione che parte spenta, nel suo dominio» (tabella 1)'),
('1,3 m','«suolo visto libero da 1,3 m a d m» (tabella 1)','«suolo visto libero da 1,3 m a d metri» (tabella 1)'),
('6 ms; 81 ms','«6 ms per ciclo in media su scene simulate, 81 ms su una registrazione vera affollata» (tabella 1)','«calcolo su un portatile, un solo filo: 6 ms per ciclo in media su scene simulate, 81 ms su una registrazione pubblica affollata» (tabella 1)'),
('6 ms; 81 ms','un filo di un portatile, non la scheda di bordo','un filo di un portatile, non la scheda di bordo; registrazione vera di una camera D415, non nostra, 254 tracce (VD riga 16)'),
('0,13 s','«segnale in 0,13 s» (tabella 1)','«segnale in 0,13 s (rumore ipotizzato)» (tabella 1)'),
('0,13 s',"[S] rumore dell'IMU ipotizzato","[S] rumore dell'IMU ipotizzato; valore da rifissare (V3 §1.9, righe 223–224)"),
('cinque (atti); cinque (minuti)','«Cinque atti in cinque minuti» (§8)','«Cinque atti, cinque minuti» (§8)'),
('1,8 m (alto)','| 1,8 m (alto); 1 m (largo); 1,8 m (dal sensore); 2,3 m; 0,5 m/s | «pannello alto 1,8 m e largo 1 m, a 1,8 m dal sensore; un adulto a 2,3 m, a 0,5 m/s» (§8)','| 1,8 m (alto); 1 m (largo) | «pannello alto 1,8 m e largo 1 m, un adulto a passo lento» (§8)'),
('1,8 m (alto)','| [P] |','| [P]; **non scritti:** a 1,8 m dal sensore, adulto a 2,3 m |'),
('5–6; tre (misure)','| 5–6; tre (misure); 30 s; 150; 30 (passaggi) | «Ore 5–6 … tre misure: posa e pavimento vuoto per 30 s; pannello sul suolo segnato, 150 fotogrammi; 30 passaggi» (§9)','| 5–6; 30 (passaggi) | «Ore 5–6. Se arriva una camera: posa, pavimento vuoto, pannello sul suolo segnato, 30 passaggi» (§9)'),
('5–6;','| [P] mai eseguite |','| [P] mai eseguite; **non scritti:** 30 s di pavimento vuoto, 150 fotogrammi |'),
('14; quattro (gradini)',"«i primi quattro gradini pronti all'ora 14 con probabilità fra 0,82 e 0,99»","«i primi quattro gradini all'ora 14 con probabilità 0,82–0,99»"),
('0,04; 0,43','fra 0,04 e 0,43','0,04–0,43'),
]
for k,a,b in S: sub(k,a,b)
new=[
"| 4 (fotogrammi) | «una persona già vista per almeno 4 fotogrammi» (§1) | VI §5 condizione 9 e §7 affermazione 5 | [C] premessa della garanzia |",
"| 5 cm | «Su sensore ideale (la persona è un punto, con 5 cm di rumore)» (§3) | VI §3, riga «Cifra» | [S] definizione del banco |",
"| 14; 4 (ore) | «Nelle 14 ore lo schermo mostra prima un disco, senza cifra; la zona con la cifra è un lavoro delle ultime 4 ore» (§2) | V3 §1.6 (`sd-0` per primo, senza cifre); VI §5 condizione 11; PIA riga 55 (`sd-1` fuori dal minimo), riga dell'ora 15 e ordine dei tagli (quarto) | [P]; se si taglia, la zona con la cifra non c'è |",
"| 1,8 s; 0,92 m/s | «Con un operatore remoto (1,8 s): 0,92 m/s» (§4.4) | BL §3, riga «lo stesso, con operatore remoto» | [C] per conto; **rifatto da me**: (3 − 0,95) m / (0,267 + 0,155 + 1,8) s = 0,92 m/s; con 1,0 s: 1,44. **Non scritto:** 1,07 m/s con 1,5 s (ipotesi per la persona non vedente) |",
"| 98–100 %; 9 persone (non scritte) | — (punto tolto per spazio) | VI §7 affermazione 12; VD §5 punto 4; DF, stima D6 | [S] è il cerchio del filtro con q = 0,2, non la zona mostrata; q tarato 0,05–0,1 (VD riga 14) |",
]
H='''# CIFRE del testo finale di due pagine — una riga per cifra (`sciame-redattore`, f12, 43-documento-finale, 14 novembre 2026)

**In testa.** Tabella rifatta dalla prima stesura (`40-documento/CIFRE.md`) con `fai_cifre.py` e riletta contro il testo finale. Nessuna cifra è mia, salvo tre conti a mano dichiarati nella riga (0,655; 0,548; 0,92 m/s). Nessuno stato è cambiato rispetto al verdetto d'integrazione: niente è «validato». Le cifre sono **lette** nei file indicati, non ricontate da me; «[R]» = ricontato dall'arbitro nel suo verdetto. Percorsi relativi a `.sciame/20261114-1301-percezione-challenge/`. Sigle: **VI** `f12-integrazione/30-arbitro/VERDETTO_INTEGRAZIONE.md`; **CH** `f5/CHIUSURA.md`; **V3** `f12-integrazione/20-finale/SOLUZIONE_V3.md`; **BL** `f14-classificazione/20-inclusione/BLOCCO_CLASSIFICAZIONE.md`; **SCH** `f12-integrazione/22-schermo-finale/SCHERMO_E_DEMO.md`; **PIA** `f12-integrazione/21-piano-finale/PIANO_14_4.md`; **DF** `f13-allegato/DISCORDANZE_DEI_FASCICOLI.md`; **VD** `f10-dati/23-verdetto/VERDETTO_DATI.md`; **VN** `f4/H-012/09-arbitro/VERDETTO.md`; **CI** contratto `f12-integrazione/CONTRATTO_INTEGRAZIONE.md`. Marca: [S] provato in simulazione, [C] per regola scritta, calcolo o scheda tecnica, [P] in progetto, non provato.

| Cifra | Frase del testo in cui compare | Origine (file, paragrafo) | Stato |
|---|---|---|---|
'''
T='''

## Note

**Non letti per intero, contro la consegna** (20 minuti): VD (righe 14, 16 e 86; il resto tramite VI), DF (righe 21 e 45; il resto tramite la consegna e la prima stesura), il decimo addendum (solo il titolo), V3 (righe cercate: §1.2, §1.3, §1.6, §1.7, §1.9, §3 «non si dice mai»), BL (§3, §6, §9), SCH (§6), PIA (quattro righe su `sd-1`), il verdetto sulla continuità (riga 31); **non aperti:** VN, V7, V9, l'audit, f6, i file di f14 diversi da BL, gli addendum 1–9, `STATO_PROGETTO.md`, `RIFERIMENTI.md`, la prova sull'identità e la sua controprova (esistono, viste con `ls`: ne uso le cifre ricontate dall'arbitro in VI). Letti per intero: il contratto, la prima stesura con CIFRE.md, le due letture, VI.

**Indipendenza.** `controlla.sh` ha lo stesso autore del testo e viene dalla prima stesura: vale per conteggi e ricerche testuali, non per il contenuto. **Nessun lettore ha riletto il testo finale: il controllo C-G resta «non verificato» sulla versione finale.**
'''
open('CIFRE.md','w',encoding='utf-8').write(H+'\n'.join(rows[:-1]+new+[rows[-1]])+T)
