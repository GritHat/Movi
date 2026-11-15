"""Allinea STATO_PROGETTO.md (v4) a VERDETTO_2C: note «superata» al posto dei commenti % 2C, riquadro 4.1, §11.14, riga 5 del registro."""
import sys, pathlib, re
p = pathlib.Path(sys.argv[1]); t = p.read_text(encoding='utf-8')
N = '<!-- % 2C -->'
assert t.count(N) == 17
NOTA = ' **[Superata dalla fase 2c: si veda il §11.14.]**'
# nota specifica per riga, per numero di riga del marcatore
SPEC = {
 '163 passaggi non C0 su 171': ' **[Superata dalla fase 2c (§11.14): col v3, ritenuta del ritorno 5 s, 0/171 [0; 0,022] in alta e in min, solo con la mappa dichiarata completa; con la mappa dichiarata ma sbagliata 5/6 «libero»; nel predefinito del prototipo la mappa non è dichiarata (0/6 «libero»).]**',
 'v2 163/171: **peggiorato**': ' **[Superata dalla fase 2c (§11.14): 0/171 col v3, con la mappa dichiarata completa.]**',
 '`prova_tutto.sh` dà esito 0 in 665 s': ' **[Superata dalla fase 2c (§11.14): 8 scene _v3 con 0 errori ai due validatori; `prova_tutto.sh` esito 0 in 698 s (non ricontato); `lp_A1_v3`, `lp_A2_v3`, `lp_A3_v3`, `lp_E3_v3`, `lp_E4_v3` «Simulation».]**',
 'quale dei due valga lo decide una riga del riconto': ' **[Superata dalla fase 2c (§11.14): col v3 51/60 [0,739; 0,919] entro 2 s, nessun ritardo negativo; con il tipo «contatto» 50/60.]**',
 '**Le scene per il video** (V2B, §5;': ' **[Superata dalla fase 2c: le scene _v3 e i loro verdetti sono nel §11.14.]**',
 'K-613, la famiglia di A1': ' **[Chiusa dalla fase 2c (§11.14): da sola smentita, 163/171; la famiglia «sito» resta il caso centrale col v3.]**',
 'Previsione: mediana ≤ 5 km; smentita se ≥ 10 km in ≥ 5/30.': ' **[Fase 2c (§11.14): regge, residuo 3,1–4,5–5,3 km, 0/60 ≥ 10 km; l\'ispezione non riduce l\'impronta (0/60), prova vuota.]**',
 'Rifare `lp_A1` e `lp_E1` scelti a caso': ' **[Fase 2c (§11.14): rifatte `lp_A1_v3` (n. 90, senza fase nascosta) e `lp_E1_v3` (K-614 aperto).]**',
 'collisione fra droni (E1) dedotta in 1,2–2,2 s': ' **[Superata dalla fase 2c (§11.14): col v3 51/60 [0,739; 0,919], ritardi 1,2–1,8–2,3 s; raggio residuo 3,1–4,5–5,3 km, 0/60 ≥ 10 km; non si riduce guardando (0/60).]**',
 'entro 2 s **49/60 [0,701; 0,894]**': ' **[Superata dalla fase 2c (§11.14): 51/60 col v3; impronta 3,1–4,5–5,3 km.]**',
}
righe = t.split('\n'); usate = set()
for i, r in enumerate(righe):
    if N not in r: continue
    nota = NOTA
    for k, v in SPEC.items():
        if k in r: nota = v; usate.add(k); break
    righe[i] = r.replace(' ' + N, nota).replace(N, nota)
t = '\n'.join(righe)
print('non usate:', set(SPEC) - usate)
# riquadro 4.1 prima di «Che cosa è aperto (seconda fase)»
A = '**Che cosa è aperto (seconda fase).**'
assert t.count(A) == 1
BOX = ('> **Versione 4.1 (fase 2c, `f15-lunga-portata/60-fase2c/02-verdetto/VERDETTO_2C.md`, verifica del 15-11-2026).** '
 'Prevale sulle righe 2, 4, 7 e 8 qui sopra e sul paragrafo seguente, che restano come storia. '
 'A1, «libero» sul drone non C0: da smentito (163/171) a **sostenuto dai dati**, 0/171 [0; 0,022] in alta e in min col nucleo v3 '
 '(ritenuta del ritorno, 5 s), **solo con la mappa dichiarata completa** (ipotesi del simulatore); con la mappa dichiarata ma sbagliata '
 '5/6 «libero» (non risolto); nel predefinito del prototipo la mappa non è dichiarata (0/6 «libero»), la validazione-3 non è chiamata. '
 'A1 tempestivo 200/200 e fuori avviso in min 12/200 [0,035; 0,102] invariati. K-613 chiusa. E1: 51/60 [0,739; 0,919] entro 2 s (resta smentito), '
 'impronta 3,1–4,5–5,3 km (sostenuta), l\'ispezione non la riduce (0/60, non risolto), 0/60 eventi prima dell\'urto con una regola notata dopo. '
 'E2 30/30, circa 96 tracce avvisate; E5 0/30 [0; 0,114]. Il v3 è rimisurato solo su A1, E1, E2, E5: A2, A3, A4 e la controprova restano v2. '
 'K-614 nuovo (`lp_E1_v3` non è il passaggio n. 30). Dettagli nel §11.14.\n\n')
t = t.replace(A, BOX + A + ' **[Superato in parte dalla versione 4.1: K-613 chiusa, mappa non più `True` nel predefinito, zona dei detriti di E1 sostenuta; resta l\'ispezione dell\'impronta.]**')
# §11.14 prima del glossario
G = '\n## Glossario'
assert t.count(G) == 1
S14 = '''
### 11.14 La fase 2c (versione 4.1)

Fonte: `f15-lunga-portata/60-fase2c/02-verdetto/VERDETTO_2C.md` (arbitro, 03:32–03:40; riconto `riconto_2c.py`, `riconto_scene_v3.py`). Prevale su VERDETTO_2B dove i due differiscono. Indipendenza del riconto: condivide record e definizioni dei campi con l'autore; controlla l'aggregazione, non la misura.

| Enunciato | VERDETTO_2B | VERDETTO_2C |
|---|---|---|
| A1, «libero» sul drone non C0 | smentito, 163/171 | **sostenuto dai dati**, 0/171 [0; 0,022] in alta e in min (v3, ritenuta del ritorno 5 s), **solo con la mappa dichiarata completa** |
| K-613 | decisione del coordinatore | chiusa: da sola smentita (163/171) |
| A1 tempestivo | 200/200 | invariato, 200/200 [0,981; 1]; falsi confermati, mediana 0 |
| A1 min, fuori avviso | 12/200 | invariato, 12/200 [0,035; 0,102]; K-606 aperto |
| X5 / K-612 (mappa) | riaperto | chiuso nel predefinito (0/6 «libero»); **non risolto** con la mappa dichiarata (5/6 «libero»); validazione-3 non chiamata |
| E1, impronta | smentita (mediana 42 km) | **sostenuta**: residuo 3,1–4,5–5,3 km, 0/60 ≥ 10 km |
| E1, riduzione guardando | — | **non risolto, prova vuota**: 0/60 (0/30 in E2) |
| E1 entro 2 s | smentito, 49/60 | resta smentito, 51/60 [0,739; 0,919]; ritardi 1,2–1,8–2,3 s; col tipo «contatto» 50/60 |
| E1, evento prima dell'urto | 1/60 | 0/60 [0; 0,060], regola notata dopo |
| E2, avviso al mezzo | giusto, non discrimina | invariato, 30/30; tracce avvisate mediana 96 |
| E5, 5 m | 0/30 | 0/30 [0; 0,114] col v3 |
| Scene video | `lp_A1` con 56 celle «libero» nell'avviso | 8 scene _v3 a 0 errori ai due validatori; fotogramma 0 con 576 «non osservato» corretto |

**Limiti da dire per primi (VERDETTO_2C § 2):** nessun sensore fisico (Pd, falsi allarmi, latenze, 45 m/s e 25 m/s² sono ipotesi); il «libero» dipende dalla mappa (0/171 con la mappa dichiarata completa, 5/6 falsi con la mappa sbagliata; per predefinito il prototipo non la dichiara); aerei in volo fuori dal caso centrale; 12/200 fuori avviso; eventi dedotti entro 2 s in 51/60, zona dei detriti di circa 4,5 km che non si riduce guardando, circa 96 tracce avvisate in E2, fiammata con innesco ottimista; v3 rimisurato solo su A1, E1, E2, E5 (A2, A3, A4 e la controprova 100/100 restano v2; il prezzo della ritenuta non è misurato); un solo multirotore e un solo ala fissa reali.

**Da non dire, nuove:** «MoVi non dichiara mai libero ciò che non ha osservato» senza «con la mappa dichiarata, in simulazione»; «il v3 elimina il "libero" falso»; «l'impronta si restringe guardando»; «E1 entro 2 s» e «sempre»; «avvisa solo i mezzi in pericolo»; «tutte le correzioni sono applicate» (6, 7, 8 no); cifre v3 per A2, A3, A4; `lp_A1_ingenua_v3` come contrasto; «`lp_E1_v3` è il passaggio n. 30».

**Scene _v3:** `lp_A1_v3` «Simulation» (n. 90, seme dichiarato prima; senza fase nascosta: per il drone dietro l'edificio `lp_A1` v2 resta solo «Schematic»); `lp_A1_ingenua_v3` da non usare (contrasto: `lp_A1_ingenua` v1); `lp_A2_v3`, `lp_A3_v3`, `lp_E3_v3`, `lp_E4_v3` «Simulation»; `lp_E1_v3` «Simulation» per evento (2,2 s) e avviso, zona dei detriti solo «Schematic»; `lp_E2_v3` «Simulation» solo per le camere non affidabili.

**K-614 (nuovo):** `lp_E1_v3` e il record E1 n. 30 di `passaggi_v3.jsonl` non sono la stessa esecuzione (tipo, origine, raggio diversi); causa non verificata.

**Regole violate (dal rapporto 2c):** sovrascritte due volte le cartelle `uscite/video/*_v3`; un `mv -n`; processi ≤ 6 non verificato; la regola dei 3 s scritta dopo il pilota sul passaggio 31.

**Aperti (VERDETTO_2C § 6):** D1, rigenerare A1 col v3 fra i 22 passaggi con fase nascosta, seme scritto prima; K-614; rimisurare col v3 A2, A3, A4 e la controprova di A1 (n = 100) e il prezzo della ritenuta (previsione: mediana ≤ 1, smentita se ≥ 3); la validazione-3 della mappa nel simulatore e cp_X5b con la mappa dichiarata; K-606; ispezione dell'impronta con T_c per punto; correzioni 6–8.
'''
t = t.replace(G, S14 + G)
R5 = '| 5 | *(da scrivere)* |'
assert t.count(R5) == 1
i = t.index(R5); j = t.index('\n', i)
riga5 = t[i:j]
t = t[:i] + riga5.replace('| *si veda il §5.7* |', '| *si veda il §5.7* — superata dalla riga 5 (a)* |') + \
    '\n| 5 (a) | 2026-11-15, verifica dei documenti | VERDETTO_2C (`f15-lunga-portata/60-fase2c/02-verdetto/`) | riquadro «Versione 4.1» nella sintesi; i 17 commenti `% 2C` sostituiti da note «superata» con le cifre del v3; §11.14 nuovo. Da «smentito» a «sostenuto dai dati, con la mappa dichiarata completa» il «libero» di A1 (0/171); E1 da 49/60 a 51/60 (resta smentito), impronta da smentita a sostenuta; K-613 chiusa; K-614 nuovo |' + t[j:]
p.write_text(t, encoding='utf-8'); print('ok', t.count(N))
