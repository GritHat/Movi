#!/usr/bin/env python3
"""riconta_arbitro.py — triage f8. Sola lettura sulle cartelle altrui.
(1) canarini; (2) cifre delle consegne ricontate sui file dei risultati; (3) conti binomiali per le soglie del protocollo.
Rifare: cd f8-continuita/10-triage; PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 riconta_arbitro.py > riconta_arbitro.txt
"""
import math, os, re, sys

B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = ["01-requisiti", "02-tracciamento", "03-kalman", "04-statistico", "05-inferenza", "06-visualizzatore", "07-ricercatore"]
Bc = ["08-rovesciatore", "09-creativo"]
CA, CB = "sciame-canarino-20c82ebff50dded3", "sciame-canarino-fe9992e292215898"


def leggi(p):
    with open(os.path.join(B, p), encoding="utf-8", errors="replace") as f:
        return f.read()


def tutti(d):
    for r, _, fs in os.walk(os.path.join(B, d)):
        for f in fs:
            if f.endswith((".png", ".json")):
                continue
            yield os.path.join(r, f)


print("== 1. Canarini ==")
ok = True
for d in A + Bc:
    prima = leggi(d + "/CONSEGNA.md").splitlines()[0].strip()
    atteso = "Canarino: " + (CA if d in A else CB)
    altro = CB if d in A else CA
    incroci = 0
    for p in tutti(d):
        try:
            incroci += open(p, encoding="utf-8", errors="replace").read().count(altro)
        except OSError:
            pass
    esito = prima == atteso and incroci == 0
    ok &= esito
    print("  %-18s prima riga %s | canarino dell'altra corsia: %d occorrenze" % (d, "ok" if prima == atteso else "DIVERSA", incroci))
print("  ESITO canarini:", "regge" if ok else "SMENTITA")

print("\n== 2. Cifre delle consegne sui file (espressione cercata nel file dei risultati) ==")
# (ruolo, cifra nella consegna, file, espressione regolare che deve comparire)
C = [
    ("requisiti", "raggio 95 % 0,84 m a 1 s (5 cm)", "01-requisiti/risultati_conto.txt", r"0\.050\s+1\.0\s+0\.344\s+0\.84"),
    ("requisiti", "raggio 3,6 m a 3 s", "01-requisiti/risultati_conto.txt", r"0\.050\s+3\.0\s+1\.485\s+3\.63"),
    ("requisiti", "«previsto» fino a 0,67–0,87 s", "01-requisiti/risultati_conto.txt", r"fino a 0\.87 s[\s\S]*fino a 0\.67 s"),
    ("requisiti", "saturi 0 %, 46 %, 31 %, 83 %", "01-requisiti/risultati_conto.txt", r"saturi 0 = 0 %[\s\S]*= 46 %[\s\S]*= 31 %[\s\S]*= 83 %"),
    ("requisiti", "quota demo 35–50 %", "01-requisiti/risultati_conto.txt", r"T_p = 0\.4: demo 35 %[\s\S]*T_p = 0\.53: demo 50 %"),
    ("tracciamento", "V3 prosegue 68,9 %", "02-tracciamento/prove/fin_V3.txt", r"prosegue: cicli nascosti \d+; il NUCLEO .* nel 68\.9%"),
    ("tracciamento", "V3 svolta 13,8 %", "02-tracciamento/prove/fin_V3.txt", r"svolta: cicli nascosti \d+; il NUCLEO .* nel 13\.8%"),
    ("tracciamento", "V3 sosta 26,2 %", "02-tracciamento/prove/fin_V3.txt", r"sosta: cicli nascosti \d+; il NUCLEO .* nel 26\.2%"),
    ("tracciamento", "V1 d1 errore a 3 s 0,88; cop90 0,922; area 0,43", "02-tracciamento/prove/fin_V1.txt", r"3\.0 1650 \| d1 \+sosta\s+0\.88\s+2\.37 \| 0\.736\s+0\.922 \|\s+0\.11\s+0\.43"),
    ("tracciamento", "V1 d1 cop90 a 2 s 0,794", "02-tracciamento/prove/fin_V1.txt", r"2\.0 1949 \| d1 \+sosta\s+0\.73\s+1\.73 \| 0\.556\s+0\.794"),
    ("tracciamento", "V1 KF errore a 3 s 2,99; area 4,35", "02-tracciamento/prove/fin_V1.txt", r"3\.0 1650 \| a KF libero\s+2\.99\s+4\.11 \| 0\.101\s+0\.640 \|\s+1\.31\s+4\.35"),
    ("tracciamento", "V1 fermo 1,18 / 1,78 / 2,15", "02-tracciamento/prove/fin_V1.txt", r"1\.0 2708 \| f fermo\s+1\.18[\s\S]*3\.0 1650 \| f fermo\s+1\.78[\s\S]*5\.0 1197 \| f fermo\s+2\.15"),
    ("tracciamento", "V3 d1 a 4 e 5 s 1,39 e 2,01; fermo 1,10 e 1,22", "02-tracciamento/prove/fin_V3.txt", r"4\.0 1402 \| d1 \+sosta\s+1\.39[\s\S]*4\.0 1402 \| f fermo\s+1\.10[\s\S]*5\.0 1200 \| d1 \+sosta\s+2\.01[\s\S]*5\.0 1200 \| f fermo\s+1\.22"),
    ("tracciamento", "V3 KF area 24,9 volte l'ombra a 3 s", "02-tracciamento/prove/fin_V3.txt", r"3\.0 1591 \| a KF libero .*24\.89"),
    ("tracciamento", "costo 63,5–69,9 µs", "02-tracciamento/prove/fin_V1.txt", r"69\.9 microsecondi"),
    ("tracciamento", "V1 identità «torna» col filtro 49,8 %", "02-tracciamento/prove/fin_V1.txt", r"a KF libero\s+2\.20/3\.42 ; 6\.2 ; 0\.0 ; 49\.8"),
    ("kalman", "A0 90 %: 0,962 0,939 0,904 0,890 0,884", "03-kalman/risultati_main.txt", r"cop 90%\s+0\.962\s+0\.939\s+0\.904\s+0\.890\s+0\.884"),
    ("kalman", "A0 50 %: 0,780 0,829 0,760 0,695 0,633", "03-kalman/risultati_main.txt", r"cop 50%\s+0\.780\s+0\.829\s+0\.760\s+0\.695\s+0\.633"),
    ("kalman", "torna 90 %: 0,765 0,647 0,454", "03-kalman/risultati_main.txt", r"torna\s+n= 592 90%:\s+0\.907\s+0\.851\s+0\.765\s+0\.647\s+0\.454"),
    ("kalman", "ombra 2 m: cerchio 0,827 / 0,765 / 0,812", "03-kalman/risultati_ombra.txt", r"cerchio A0 ritagliato: cop 0\.827[\s\S]*cerchio A0 ritagliato: cop 0\.765[\s\S]*cerchio A0 ritagliato: cop 0\.812"),
    ("kalman", "ombra 2 m: miscela troncata 0,940 / 0,973 / 0,951", "03-kalman/risultati_ombra.txt", r"miscela troncata e rinormalizzata: cop 0\.940[\s\S]*cop 0\.973[\s\S]*cop 0\.951"),
    ("kalman", "G1 a 5 s: 0,785 e 0,636", "03-kalman/risultati_ombra_G1.txt", r"cop 0\.785[\s\S]*cop 0\.636"),
    ("statistico", "1 s: 0,915 · 1,000 · 0,867 · 0,603 · 0,829; 50 % 0,798", "04-statistico/out_misure.txt", r"D=1\.0 s[\s\S]*?prosegue .*0\.970 1\.000[\s\S]*?sosta .*0\.585 0\.867[\s\S]*?torna .*0\.422 0\.603[\s\S]*?svolta .*0\.571 0\.829[\s\S]*?MISCELA .*0\.798 0\.915"),
    ("statistico", "2 s: torna 0,536; abilità −0,38", "04-statistico/out_misure.txt", r"torna\s+n= 1500 \| cop 50/90/95: 0\.340 0\.536 .*ab -0\.38"),
    ("statistico", "unione: classe peggiore 0,890 / 0,904 / 0,909", "04-statistico/out_unione.txt", r"D=1\.0 s:.*svol 0\.890[\s\S]*D=2\.0 s:.*svol 0\.904[\s\S]*D=3\.0 s:.*svol 0\.909"),
    ("statistico", "H9: regge 1,000 con «torna» mai coperto", "04-statistico/out_h9.txt", r"chi torna MAI coperto.*0\.000\s+1\.000\s+0\.000"),
    ("statistico", "correlazione intraclasse 0,205 e 0,512", "04-statistico/out_fotogrammi.txt", r"intraclasse 0\.205[\s\S]*intraclasse 0\.512"),
    ("inferenza", "PF 4000 lisciata: 0,928 / 0,902 / 0,895", "05-inferenza/risultati2_pf2.txt", r"N=4000.*0\.928 \| 2\.09 ; 0\.91 \| 0\.89 \| 0\.902 \| 3\.55 ; 0\.87 \| 0\.88 \| 0\.895 \| 4\.04"),
    ("inferenza", "28,6 ms per dieci oggetti", "05-inferenza/risultati4_dieci.txt", r"totale 28\.6 ms"),
    ("inferenza", "MG: svolta 40 %, lontano 18 % a 2 s", "05-inferenza/risultati_copertura.txt", r"svolta .*t=2\.0:\s+2 \|\s+40 \(52\)[\s\S]*?lontano .*t=2\.0:\s+1 \|\s+18 \(74\)"),
    ("inferenza", "nucleo: emessa 91 / 65 / 45 / 88 / 58 / 42 %", "05-inferenza/risultati_copertura.txt", r"NUCLEO[\s\S]*emessa 91%[\s\S]*emessa 65%[\s\S]*emessa 45%[\s\S]*emessa 88%[\s\S]*emessa 58%[\s\S]*emessa 42%"),
    ("inferenza", "salto alla ricomparsa 0,87 m (95º 1,79)", "05-inferenza/risultati_copertura.txt", r"mediana 0\.87 m, 95o pct 1\.79 m"),
    ("inferenza", "MG area 7,27 m² a 3 s", "05-inferenza/risultati_det.txt", r"t=3\.00 s: IoU 0\.56 \| massa oracolo mediana 0\.972 .*area 7\.27"),
    ("visualizzatore", "media su libero 48,0 % e 26,5 %", "06-visualizzatore/risultati_punto_mostrato.txt", r"su libero 48\.0 %[\s\S]*su libero 26\.5 %"),
    ("visualizzatore", "9 su 10 con copertura 0,80: 37,6 %", "06-visualizzatore/risultati_tabellone.txt", r"copertura vera 0\.80: 37\.6 %"),
    ("visualizzatore", "86 transiti, soglia 74", "06-visualizzatore/risultati_tabellone.txt", r"n = 86, soglia 74"),
    ("visualizzatore", "soglia «larga» a 1,47 s", "06-visualizzatore/risultati_fotogrammi.txt", r"superata a t = 1\.47 s"),
    ("ricercatore", "raggio medio: torna 0,455 a 2 s", "07-ricercatore/risultati_conforme.txt", r"marginale, per comportamento: .*torna 0\.455"),
    ("ricercatore", "Kalman nominale: torna 0,291 e 0,108", "07-ricercatore/risultati_conforme.txt", r"torna 0\.291[\s\S]*torna 0\.108"),
    ("ricercatore", "miscela spostata 0,796", "07-ricercatore/risultati_conforme.txt", r"miscela spostata: marginale 0\.796"),
    ("ricercatore", "raggio peggiore 5,82 m a 3 s e 12,20 m a 5 s", "07-ricercatore/risultati_conforme.txt", r"peggiore' 5\.82 m[\s\S]*peggiore' 12\.20 m"),
    ("rovesciatore", "emessa 60,8 % e 39,8 %", "08-rovesciatore/esito_rov_f8.txt", r"TUTTI\s+18595\s+11309\s+60\.8%[\s\S]*TUTTI\s+27446\s+10917\s+39\.8%"),
    ("rovesciatore", "sosta 40,0 % (vuoto 3,13 s) e 28,5 % (3,93 s)", "08-rovesciatore/esito_rov_f8.txt", r"sosta\s+120\s+8468\s+3386\s+40\.0%.*3\.13[\s\S]*sosta\s+120\s+9755\s+2776\s+28\.5%.*3\.93"),
    ("rovesciatore", "cerchio a 2 s: torna 44,4 %, lontano 49,0 %", "08-rovesciatore/esito_rov_f8.txt", r"2\.0\s+100\.0%/100\.0% n=13\s+24\.7%/71\.2% n=299\s+11\.1%/44\.4% n=99\s+14\.1%/49\.0% n=255"),
    ("rovesciatore", "regione A: 86,4 / 89,5 / 89,5 % dell'ombra", "08-rovesciatore/esito_rov_f8.txt", r"1\.5  A .*27\.8\s+86\.4[\s\S]*?2\.0  A .*52\.3\s+89\.5[\s\S]*?3\.0  A .*47\.6\s+89\.5"),
    ("rovesciatore", "regione B sul pannello da 2 m: 15,3 % e 0,0 %", "08-rovesciatore/esito_rov_f8.txt", r"2\.0  B\s+15\.3%[\s\S]*3\.0  B\s+0\.0%"),
    ("rovesciatore", "0 cicli su 115437 fuori dal disco di v_max", "08-rovesciatore/esito_rov_f8.txt", r"0 cicli su 115437"),
    ("creativo", "fronte + scia: informativa 98,6 % in sosta; nucleo 39,4 %", "09-creativo/esito_v2_w1_senzaC.txt", r"sosta\s+6873 \| 100 \|\s+98\.6 \|\s+34\.9 \|\s+28\.4\s+63\.1 \|\s+39\.4"),
    ("creativo", "svolta 21 % a 2 s; lontano 17 %", "09-creativo/esito_v2_w1_senzaC.txt", r"svolta\s+2\.0\s+73 \|\s+5\s+21[\s\S]*lontano\s+2\.0 100 \|\s+4\s+17"),
    ("creativo", "costo 0,48 ms (p95 0,56), 4,3 ms all'ingresso", "09-creativo/esito_v2_w1_senzaC.txt", r"mediana 0\.48 ms\s+p95 0\.56 ms.*mediana 4\.3 ms"),
    ("creativo", "24 su 30: 0,974 e 0,607; 51 su 60: 0,927 e 0,213", "09-creativo/esito_tabellone.txt", r"n=30 soglia k=24: p=0\.90 -> 0\.974\s+p=0\.80 -> 0\.607[\s\S]*n=60 soglia k=51: p=0\.90 -> 0\.927\s+p=0\.80 -> 0\.213"),
]
torna = 0
for ruolo, cifra, f, rx in C:
    try:
        t = leggi(f)
        esito = re.search(rx, t) is not None
    except OSError as e:
        esito = False
        cifra += " [file mancante: %s]" % e
    torna += esito
    print("  %-14s %-62s %-52s %s" % (ruolo, cifra, f, "torna" if esito else "NON TORNA"))
print("  ESITO: %d cifre su %d tornano dal file" % (torna, len(C)))

# terzo generatore del creativo: 12 celle su 12 con n >= 30 fra 96 e 100
t = leggi("09-creativo/esito_terzo.txt")
celle = [(int(m.group(2)), int(m.group(3))) for m in re.finditer(r"^(prosegue|sosta|torna)\s+[\d.]+\s+(\d+) \|\s+\d+\s+(\d+)", t, re.M)]
grandi = [c for n, c in celle if n >= 30]
print("  creativo, terzo generatore: celle con n>=30: %d; copertura al 90 %%: minimo %d, massimo %d (consegna: 12 su 12 fra 96 e 100)" % (len(grandi), min(grandi), max(grandi)))

print("\n== 3. Conti binomiali per le soglie del protocollo ==")


def pmf(n, k, p):
    return math.comb(n, k) * p ** k * (1 - p) ** (n - k)


def coda_alta(n, k, p):  # P(X >= k)
    return sum(pmf(n, i, p) for i in range(k, n + 1))


def wilson(k, n, z=1.959964):
    ph = k / n
    d = 1 + z * z / n
    c = (ph + z * z / (2 * n)) / d
    h = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


for n in (30, 100, 200, 400):
    k = math.ceil(0.85 * n)
    lo, hi = wilson(round(0.9 * n), n)
    print("  n=%3d soglia «almeno %d dentro» (0,85): bocciata per errore se copre 0,90: %.4f | promossa se copre 0,80: %.4f | promossa se copre 0,75: %.4f | Wilson 95 %% a 0,90: [%.3f; %.3f]"
          % (n, k, 1 - coda_alta(n, k, 0.90), coda_alta(n, k, 0.80), coda_alta(n, k, 0.75), lo, hi))
print("  controllo incrociato del visualizzatore: P(>=74 su 86 | 0,90) = %.3f ; P(>=74 su 86 | 0,80) = %.3f" % (coda_alta(86, 74, 0.9), coda_alta(86, 74, 0.8)))
print("  controllo incrociato del visualizzatore: P(>=9 su 10 | 0,80) = %.3f" % coda_alta(10, 9, 0.8))
print("  controllo incrociato del creativo: P(>=24 su 30 | 0,90) = %.3f ; P(>=24 su 30 | 0,80) = %.3f" % (coda_alta(30, 24, 0.9), coda_alta(30, 24, 0.8)))
# banda per il livello 50 % sulla miscela: n = 400, banda 0,40-0,60
n = 400
dentro = sum(pmf(n, i, 0.5) for i in range(math.ceil(0.40 * n), math.floor(0.60 * n) + 1))
dentro79 = sum(pmf(n, i, 0.79) for i in range(math.ceil(0.40 * n), math.floor(0.60 * n) + 1))
print("  livello 50 %%, n=400, banda 0,40-0,60: una regione giusta sta nella banda con probabilita' %.4f; una che contiene 0,79 con probabilita' %.2e" % (dentro, dentro79))
# zero vuoti su 400: limite superiore al 95 % della quota vera di passaggi con un vuoto
print("  0 passaggi con un vuoto su 400: limite superiore al 95 %% della quota vera = %.4f (regola del tre: %.4f)" % (1 - 0.05 ** (1 / 400), 3 / 400))
# ore: bilancio grezzo
for p in (3, 4, 5):
    print("  squadra di %d: %d ore-persona in 14 ore, %d nelle 4 di raffinamento (nucleo stimato: 54 ore-persona, 38 in fila; VERDETTO.md, righe 16 e 93)" % (p, 14 * p, 4 * p))
