#!/usr/bin/env python3
"""leggi.py — legge le righe «R» di ris/*.txt e scrive le tabelle con il limite inferiore di Wilson al 95 %."""
import glob, math, os, sys

def wil(k, n, z=1.959964):
    if n == 0: return float("nan")
    p = k / n; d = 1 + z * z / n
    return (p + z * z / (2 * n) - z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / d
def wup(k, n, z=1.959964):
    if n == 0: return float("nan")
    p = k / n; d = 1 + z * z / n
    return (p + z * z / (2 * n) + z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / d

R = []
for f in sorted(glob.glob(os.path.join(sys.argv[1], "*.txt"))):
    for ln in open(f, encoding="utf-8"):
        if ln.startswith("R "):
            d = {}
            for kv in ln.split()[1:]:
                k, v = kv.split("=", 1)
                try: d[k] = int(v)
                except ValueError:
                    try: d[k] = float(v)
                    except ValueError: d[k] = v
            d["file"] = os.path.basename(f)[:-4]; R.append(d)
def sel(pref): return [r for r in R if r["file"].startswith(pref)]
def tot(rows, k): return sum(r[k] for r in rows)
def q(k, n): return f"{k}/{n}=" + (f"{k/n:.3f}" if n else "nan")
PERC = ["prosegue", "rallenta", "sosta", "torna", "sostalunga"]; PARTE = ["svolta", "lontano", "fermo-in-vista"]

print("== (a) CONTINUITA' — per geometria, rilevamento, corpo; cinque comportamenti sul percorso, 400 semi l'uno ==")
print("file | passaggi confermati | con un vuoto | scoperti (>=1 ciclo) | scoperti >=3 cicli | non confermati prima dell'ombra | di cui scoperti (>=1; >=3 cicli) | cicli nascosti | cicli scoperti | cicli coperti solo da c7 | cicli c7 a soggetto in piena vista")
for g in "DTL":
    for r0 in sorted({r["file"] for r in sel(f"a_{g}_")}):
        rows = [r for r in R if r["file"] == r0]
        print(f"{r0} | {tot(rows,'validi')} | {tot(rows,'gap_p')} | {tot(rows,'scop_p')} | {tot(rows,'scop3_p')} | {tot(rows,'nonconf')} | {tot(rows,'nc_scop')}; {tot(rows,'nc_scop3')} | {tot(rows,'hid_all')} | {tot(rows,'scop_c')} | {tot(rows,'cyc_c7')} | {tot(rows,'c7_vis')}")
for c7 in (1, 0):
    rows = [r for r in R if r["file"].startswith("a_") and r["c7"] == c7]
    n = tot(rows, 'validi') + tot(rows, 'nonconf'); s = tot(rows, 'scop_p') + tot(rows, 'nc_scop'); s3 = tot(rows, 'scop3_p') + tot(rows, 'nc_scop3')
    print(f"TOTALE (a) c7={c7}: passaggi {n}; con un vuoto {tot(rows,'gap_p')} (limite superiore al 95 %: {wup(tot(rows,'gap_p'), tot(rows,'validi')):.5f}); scoperti {s} = {s/n:.4f}; scoperti per almeno 3 cicli {s3} = {s3/n:.4f}; cicli scoperti {tot(rows,'scop_c')} su {tot(rows,'hid_all')} nascosti")
    for pd in (0.9, 0.7):
        for rb in (0.225, 0.0):
            rr = [r for r in rows if r["pd"] == pd and r["rb"] == rb]
            n = tot(rr, 'validi') + tot(rr, 'nonconf'); s = tot(rr, 'scop_p') + tot(rr, 'nc_scop'); s3 = tot(rr, 'scop3_p') + tot(rr, 'nc_scop3')
            print(f"   c7={c7} rilevamento {pd} corpo {'esteso' if rb else 'puntiforme'}: scoperti {q(s, n)}; per almeno 3 cicli {q(s3, n)}; vuoti {tot(rr,'gap_p')}")

print("\n== (b) PRECISIONE — corpo esteso, rilevamento 0,9, maschera esatta; unita' = passaggio, un istante per passaggio e per orizzonte ==")
print("PRIMARIA = segno «previsto» (non «ampio»), corpo tutto nascosto: dentro R90. SECONDARIA = tutti gli istanti a corpo tutto nascosto, R90 grezza. MOSTRATA = regione a schermo (in «ampio» tutta l'ombra).")
print("geo beh | s | primaria k/n=quota [Wilson inf] | secondaria k/n=quota [Wilson inf] | mostrata | area R90/ombra | nota")
cade = []
for g in "DTL":
    for r in sel(f"b_{g}"):
        for i, soglia in ((1, 0.90), (2, 0.90), (3, 0.85)):
            kD, nD, kT, nT, kS = r[f"inD{i}"], r[f"nD{i}"], r[f"inT{i}"], r[f"nT{i}"], r[f"shT{i}"]
            nota = []
            if nD < 400: nota.append("primaria: n<400")
            if nT < 400: nota.append("secondaria: n<400")
            if r["beh"] in PERC:
                if nD >= 400 and wil(kD, nD) < soglia: nota.append(f"PRIMARIA SOTTO {soglia}"); cade.append((g, r["beh"], i, "primaria", kD, nD))
                if nT >= 400 and wil(kT, nT) < soglia: nota.append(f"SECONDARIA SOTTO {soglia}"); cade.append((g, r["beh"], i, "secondaria", kT, nT))
            else: nota.append("a parte")
            print(f"{g} {r['beh']:<14} | {i} | {q(kD,nD)} [{wil(kD,nD):.3f}] | {q(kT,nT)} [{wil(kT,nT):.3f}] | {q(kS,nT)} | {r[f'ar{i}']:.2f} | {'; '.join(nota)}")
print("CELLE SUL PERCORSO CON n>=400 SOTTO SOGLIA:", cade if cade else "nessuna")
for g in "DTL":
    rows = [r for r in sel(f"b_{g}") if r["beh"] in PERC]
    for i, soglia in ((1, 0.90), (2, 0.90), (3, 0.85)):
        kD, nD, kT, nT = tot(rows, f"inD{i}"), tot(rows, f"nD{i}"), tot(rows, f"inT{i}"), tot(rows, f"nT{i}")
        print(f"   {g} sul percorso, cinque comportamenti insieme, {i} s: primaria {q(kD,nD)} [{wil(kD,nD):.3f}]; secondaria {q(kT,nT)} [{wil(kT,nT):.3f}]; quota di istanti in «ampio» {1 - nD/nT if nT else float('nan'):.2f}")

print("\n== (c) K-215 — ombra stimata piu' stretta, corpo esteso; cinque comportamenti sul percorso insieme e «prosegue» da solo ==")
print("file | prosegue a 1 s, 2 s (secondaria) [Wilson inf] | sul percorso a 1 s, 2 s, 3 s (secondaria) [Wilson inf] | scoperti | vuoti | cicli fuori da R100")
for r0 in sorted({r["file"] for r in sel("c_")}):
    rows = [r for r in R if r["file"] == r0]; p = [r for r in rows if r["beh"] == "prosegue"][0]
    a = " ".join(f"{q(p[f'inT{i}'], p[f'nT{i}'])} [{wil(p[f'inT{i}'], p[f'nT{i}']):.3f}]" for i in (1, 2))
    b = " ".join(f"{q(tot(rows,f'inT{i}'), tot(rows,f'nT{i}'))} [{wil(tot(rows,f'inT{i}'), tot(rows,f'nT{i}')):.3f}]" for i in (1, 2, 3))
    print(f"{r0} | {a} | {b} | {tot(rows,'scop_p') + tot(rows,'nc_scop')}/{tot(rows,'validi') + tot(rows,'nonconf')} | {tot(rows,'gap_p')} | {tot(rows,'f100c')}")

print("\n== (d) ESTRANEO mai visto che esce dall'ombra in cui il soggetto e' nascosto (sosta e sosta lunga insieme) ==")
print("file | casi decisi (prima misura dell'estraneo con la traccia del soggetto pendente) | identita' sbagliata = avviso rilasciato senza aver visto il soggetto [Wilson] | di cui col soggetto tutto nascosto | rifiutati (ambiguo: l'avviso resta, c2) | regione gia' «ampio» | non applicabili | estraneo mai uscito")
for r0 in sorted({r["file"] for r in sel("d_")}):
    rows = [r for r in R if r["file"] == r0]; n = tot(rows, 'es_n'); k = tot(rows, 'es_id')
    print(f"{r0} | {n} | {q(k, n)} [{wil(k, n):.3f}-{wup(k, n):.3f}] | {tot(rows,'es_ril')} | {tot(rows,'es_amb')} | {tot(rows,'es_ampio')} | {tot(rows,'es_na')} | {tot(rows,'es_mai')}")

print("\n== (e) SICUREZZA — tutti gli istanti a corpo tutto nascosto dentro l'area osservata, tutte le prove tranne il braccio «toglie» ==")
rows = [r for r in R if r["toglie"] == 0 and r["estr"] == 0]; rc7 = [r for r in rows if r["c7"] == 1]
print(f"tutti i lanci: istanti nascosti {tot(rows,'hid_all')}; con il centro fuori da R100 (geometria): {tot(rows,'f100c')}; limite superiore al 95 % {wup(tot(rows,'f100c'), tot(rows,'hid_all')):.6f} (per istante; gli istanti di un passaggio non sono indipendenti)")
print(f"lanci con c7: istanti nascosti {tot(rc7,'hid_all')}; scoperti (senza traccia pendente e senza avviso) {tot(rc7,'scop_c')}; passaggi {tot(rc7,'validi') + tot(rc7,'nonconf')}; passaggi con almeno uno scoperto {tot(rc7,'scop_p') + tot(rc7,'nc_scop')}")
rm = [r for r in rc7 if r["e"] == 0.0 and r["ch5"] == 0]
print(f"   di cui con la maschera esatta e senza chiusura 5: scoperti {tot(rm,'scop_c')} istanti su {tot(rm,'hid_all')}; passaggi {tot(rm,'scop_p') + tot(rm,'nc_scop')} su {tot(rm,'validi') + tot(rm,'nonconf')}")
print("chiusura «fuori dall'area osservata»: file | passaggi | condizione debole vera | condizione scritta vera | chiusure eseguite | col soggetto tutto nascosto alla chiusura | cicli nascosti dopo la chiusura | di cui fuori da R100 | passaggi scoperti | cicli scoperti")
for r0 in sorted({r["file"] for r in sel("e_")}):
    rows = [r for r in R if r["file"] == r0]
    print(f"{r0} | {tot(rows,'validi') + tot(rows,'nonconf')} | {tot(rows,'ch5w_p')} | {tot(rows,'ch5s_p')} | {tot(rows,'ch5_n')} | {tot(rows,'ch5_nasc')} | {tot(rows,'ch5_cyc')} | {tot(rows,'ch5_f100')} | {tot(rows,'scop_p') + tot(rows,'nc_scop')} | {tot(rows,'scop_c')}")
rows = [r for r in R if r["estr"] == 0]
print(f"condizione scritta («tutti i membri fuori»), su tutti i lanci: vera in {tot(rows,'ch5s_p')} passaggi su {tot(rows,'validi')}; condizione debole: {tot(rows,'ch5w_p')}")

print("\n== (f) REGRESSIONE — identita' al ritorno con C6 e c1 (lanci b_, corpo esteso) ==")
print("geo beh | ricomparsi dopo essere stati nascosti | riagganciati [Wilson inf] | falliti per distanza dall'ombra | per margine dal bordo | per la porta M7")
for g in "DTL":
    rows = sel(f"b_{g}")
    for r in rows: print(f"{g} {r['beh']:<14} | {r['ricomp']} | {q(r['riagg'], r['ricomp'])} [{wil(r['riagg'], r['ricomp']):.3f}] | {r['f_dist']} | {r['f_bordo']} | {r['amb_m7']}")
    pp = [r for r in rows if r["beh"] in PERC]
    print(f"   {g} sul percorso: {q(tot(pp,'riagg'), tot(pp,'ricomp'))} [{wil(tot(pp,'riagg'), tot(pp,'ricomp')):.3f}]")
for f in sorted(glob.glob(os.path.join(sys.argv[1], "s_*.txt"))):
    for ln in open(f, encoding="utf-8"):
        if ln.startswith("SESSIONE"): print("   c2,", ln.strip())

print("\n== c5 — chi parte da fermo accanto al pannello (a parte) ==")
print("file | a 1, 2, 3 s: secondaria (R90 grezza) | mostrata | primaria (solo con segno «previsto»)")
for r0 in sorted({r["file"] for r in sel("f_")} | {f"b_{g}_parte" for g in "DTL"}):
    for r in [r for r in R if r["file"] == r0 and r["beh"] == "fermo-in-vista"]:
        print(f"{r0} | " + " ".join(q(r[f'inT{i}'], r[f'nT{i}']) for i in (1, 2, 3)) + " | " + " ".join(f"{q(r[f'shT{i}'], r[f'nT{i}'])} [{wil(r[f'shT{i}'], r[f'nT{i}']):.3f}]" for i in (1, 2, 3)) + " | " + " ".join(q(r[f'inD{i}'], r[f'nD{i}']) for i in (1, 2, 3)))

print("\n== (g) COSTO del predittore, dieci tracce, C, un filo ==")
print(open(os.path.join(sys.argv[1], "tempo_C.txt"), encoding="utf-8").read().strip())
print("\n== SEMI ==")
print(open(os.path.join(sys.argv[1], "semi.txt"), encoding="utf-8").read().strip())
