# Costruisce TABELLA_CORREZIONI.md della versione finale: righe della prima stesura con i paragrafi aggiornati
# dove la regola è cambiata, più le righe delle critiche di f12. Uso: python -I fai_tabella.py <vecchia> <nuova>
import sys
old, new = sys.argv[1], sys.argv[2]
L = open(old, encoding='utf-8').read().split('\n')
def setcol(key, sub, col):
    n = 0
    for i, r in enumerate(L):
        c = r.split(' | ')
        if r.startswith('| ' + key + ' |') and sub in r:
            L[i] = ' | '.join(c[:2]) + ' | ' + col + ' |'; n += 1
    assert n == 1, (key, sub, n)
R = [
 ('VN-2','', '§1.7: una sola fascia w = 0,40 m; copre 1,13 m/s col conto a tre termini (0,56 con 20 cm d\'errore di bordo), 1,4 m/s solo con età e latenza; §1 convenzioni (secondi); K-015 nel §5'),
 ('VN-3','', '§7 «geometria della demo»: pannello alto **1,8 m** (VD), largo 1 m, attore a 2,3 m, una sola persona'),
 ('AU-9','', '§1.1 (taratura a scena vuota; posa entro 0,5°; due prove d\'ingresso)'),
 ('V7-a','', '§1.2: `nuvole-1` (esito di C-D, LC); K-107 nel §5: decisa in simulazione, aperta sul vero'),
 ('V7 §1, tabella','senza memoria', '§1.2 (`nuvole-1`; il ripiego `stato` a 0,20 m è caduto: LC, AT P1); I1'),
 ('V7 §1, tabella','`stato(p)`', '§1.6: il ritaglio usa la maschera di §1.2, la stessa delle celle (LC §3); la lettura per punto a 0,20 m da sola è caduta'),
 ('V7 §1, tabella','V-017', '§4: V-017 fuori dalle 14 ore (controesempio coi buchi a chiazze, LC); V-016, V-019, T-008: 4 ore, se confermate'),
 ('V7 §2','demo: pannello', '§7 (1,8 m, a 1,8 m, attore a 2,3 m); K-111 nel §5'),
 ('V7 §7','', 'eseguita in questo passo: LC (C-D). Esito in §1.2; K-107, K-106 nel §5'),
 ('A7 §3.1','', '§1.2 (3 pixel per «occupato»); la quota letta esce con V-017 (§4)'),
 ('A7 §3.3','', '§1.9; §1.7 (rilascio oltre w dall\'ombra corrente dell\'occlusore)'),
 ('A7 §3.5','', '§1.1, §1.9: **0,5°**, non 1° (controesempio a 1°: AT P2, LC, CO B13)'),
 ('c1','', '§1.8: **entra insieme a F-409**, col limite «un soggetto per ombra»; da sola cade contro l\'estraneo (PI riga d); K-218, K-219, K-016 nel §5'),
 ('c2','', '§1.7 (un avviso con contatore), §1.8 («la più recente», identità presunta); `sd-K3`, `sd-K7`, `logico-K1` nel §5'),
 ('c5','', '§1.6: 0,3 m/s **e** «sotto 0,3 m/s negli ultimi 2 s → ampio» (PI), coi due denominatori (AT P12)'),
 ('c7','', '§1.5: sostenuta in simulazione ideale (PI: 928 → 24 su 23 402); **dietro la prova d\'ingresso del rumore** (AT P11)'),
 ('statistico-5','', '§1.6: «almeno 9 su 10» fino a 2 s, «almeno 85 su 100» fra 2 e 3 s (una sola scritta: CO A8), solo con sd-1 e ostacolo largo 2 m'),
 ('V8 §4.2','', '§1.8: prova eseguita (PI): c1 cade contro l\'estraneo; entra con F-409'),
 ('V8 §4.9','', '§1.5, §1.7: sostenuta in simulazione (PI riga e2); `sd-K6` chiusa'),
 ('V8 §4','manca la prova', 'eseguita in questo passo: PI (C-C), controllata da ST; esiti in §1.5–§1.8, §7'),
 ('V8 §7','', 'eseguita: PI. Esiti: continuità regge; precisione regge in T e L, cade col pannello da 1 m; estraneo: cade; K-215 senza c3: cade'),
 ('S6','', '§1.10 (4 ore, sola etichetta, riferita al punto protetto, con la guardia per l\'oggetto fermo); K-305 nel §5; «probabilità d\'intrusione»: **esclusa**, §4'),
 ('F-401','', '§1.3: soglia per cella **esclusa** (smentita in ID: 98 e 91 celle «libero» in ombra); gruppi per picco dietro interruttore; §4; `sd-K4`'),
 ('F-402','', '§1.8: rifiuto dei tagliati (c1), del bordo del campo e dell\'occlusore (interruttore `riaggancio_f402`)'),
 ('F-403','', '§1.1: prova d\'ingresso del rumore (0 gruppi in 30 s); `logico-K1` nel §5; §1.3 (stato)'),
 ('F-404','', '§1.1: posa entro 0,5° **e** prova d\'ingresso (10 cm a 2,5 m «occupato») come cancello; I13; §7'),
 ('F-408','', '§1.4, §1.8: il filtro riparte dalla misura con R + (larghezza/2)² (ID: 5,00 → 0,17 m, N = 1)'),
 ('F-409','', '§1.7: **adottata**: l\'avviso resta al riaggancio (priorità 2; costo: non si spegne dietro un occlusore fermo); §1.4 (regola su q)'),
 ('F-412','', '§1.3: rapporto col picco al posto della soglia assoluta, sui soli gruppi (interruttore); `sd-K4`'),
 ('V10, condizioni 1–9','', '§1.1 (1, 4: posa entro 0,5°); §7 (3: pannello 1,8 m; 7: limiti; 9: dicitura); §1.3 (5); §1.8 e `logico-K1` (6)'),
 ('V10 §6','', 'prova senza sensore: **eseguita** (ID): il criterio con le correzioni dei ruoli cade; una variante scelta dopo i dati tiene come tasso (176 e 174 su 180) in un dominio stretto, non come criterio (controprova CI): §1.3, §1.8. Tre misure col sensore: §7'),
]
for k, s, c in R: setcol(k, s, c)
t = '\n'.join(L)
for a, b in [('non parte oltre 1°', 'posa entro 0,5° e prova d\'ingresso'), ('V10', 'VD')]:
    t = t.replace(a, b)
i = t.index('\n## 1.')
testa = '''# Tabella delle correzioni obbligate → dove stanno nella versione 3 FINALE — f12, `20-finale` (`sciame-scene-dinamiche`)

14 novembre 2026. «§» rimanda a `SOLUZIONE_V3.md` **di questa cartella** (versione finale); «I#» agli invarianti del suo §2. La numerazione dei blocchi (§1.1–§1.12) e dei paragrafi §2–§7 è la stessa della prima stesura: le righe dei §1–§8 qui sotto sono quelle della prima stesura, con la terza colonna riscritta dove la regola è cambiata (31 righe, elenco in `fai_tabella.py`); le altre le ho lasciate com'erano e **non le ho ricontrollate una per una**. I §9–§15 sono nuovi: una riga per ogni correzione delle quattro critiche di f12 e per gli esiti delle prove nuove, con **applicata** o **non applicata** e il motivo. **Esclusa** = non entra nel prototipo, con il motivo. **Altro ruolo** = è del piano o dello schermo finali. **[prel.]** = f10 col verdetto VD; **[f12]** = prova di questo passo, non vagliata dall'arbitro. Nessuna riga è «validata».
'''
t = testa + t[i:]
coda = open(sys.argv[3], encoding='utf-8').read()
open(new, 'w', encoding='utf-8').write(t.rstrip('\n') + '\n\n' + coda)
print('righe:', t.count('\n') + coda.count('\n'))
# ritocchi finali su quattro righe rimaste con valori vecchi (aggiunti dopo un grep sulla tabella prodotta)
t = open(new, encoding='utf-8').read()
for a, b in [
 ('§7 (geometria: 1,7 m; «dietro', '§7 (geometria: 1,8 m; «dietro'),
 ('| coerente con 1,7 m: §7 |', '| coerente con 1,8 m (VD): §7 |'),
 ('| §1.1, §1.9; la seconda parte decade:', '| §1.1, §1.9, con **0,5°** al posto di 1° (AT P2, CO B13); la seconda parte decade:'),
 ('| §1.7; §1.10; I12; §7 |\n| C5', '| §1.7 (w come simbolo; coperti 1,13 m/s col conto a tre termini, non 1,4); §1.10; I12; §7 |\n| C5'),
 ('(31 righe, elenco', '(35 righe, elenco'),
]:
    assert t.count(a) == 1, (a, t.count(a)); t = t.replace(a, b)
open(new, 'w', encoding='utf-8').write(t)
