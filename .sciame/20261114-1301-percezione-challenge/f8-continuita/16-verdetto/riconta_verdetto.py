#!/usr/bin/env python3
"""Riconteggio dell'arbitro (f8, fase f5): sola lettura dei file dei risultati.
Rifare: cd f8-continuita/16-verdetto; PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 riconta_verdetto.py > riconta_verdetto.txt
Non esegue alcun simulatore: legge i .tsv e i .txt scritti dagli altri ruoli e ricalcola le cifre.
"""
import os, re, glob

QUI = os.path.dirname(os.path.abspath(__file__))
F8 = os.path.dirname(QUI)
PERCORSO = ["prosegue", "rallenta", "sosta", "torna", "sostalunga"]
ESITI = []


def esito(nome, atteso, trovato, ok):
    ESITI.append((nome, atteso, trovato, ok))
    print(f"[{'TORNA' if ok else 'NON TORNA'}] {nome}\n      scritto: {atteso}\n      dal file: {trovato}")


def leggi_tsv(p):
    righe = []
    with open(p, encoding="utf-8") as f:
        for r in f:
            r = r.rstrip("\n")
            if not r or r.startswith("#"):
                continue
            c = r.split("\t")
            d = {"tipo": c[0], "campi": c}
            kv = {}
            prec = None
            for x in c:
                if "=" in x:
                    k, v = x.split("=", 1)
                    # la chiave "pass" e' ripetuta: la lego a quella che la precede
                    if k == "pass" and prec:
                        k = prec + "_pass"
                    kv[k] = v
                    prec = k
            d["kv"] = kv
            righe.append(d)
    return righe


def H(righe, beh, pred, tau):
    for d in righe:
        c = d["campi"]
        if d["tipo"] == "H" and c[2] == beh and c[3] == pred and abs(float(c[4]) - tau) < 1e-9:
            return {k: float(v) if re.fullmatch(r"-?[0-9.]+", v) else v for k, v in d["kv"].items()}
    return None


def P(righe, beh, pred):
    for d in righe:
        c = d["campi"]
        if d["tipo"] == "P" and c[2] == beh and c[3] == pred:
            return d["kv"]
    return None


def comportamenti(righe):
    return [d["campi"][2] for d in righe if d["tipo"] == "G"]


print("=" * 100)
print("A. BANCO (11-misure/risultati/prova_*_pd09.tsv)")
banco = {g: leggi_tsv(f"{F8}/11-misure/risultati/prova_{g}_pd09.tsv") for g in "DTL"}
for g in "DTL":
    print(g, "comportamenti:", comportamenti(banco[g]))

# 1. passaggi con un vuoto, nucleo L0
for insieme, nome in ((PERCORSO, "sul percorso (5)"), (None, "tutti (7)")):
    out = []
    for g in "DTL":
        behs = insieme or comportamenti(banco[g])
        pv = sum(int(P(banco[g], b, "L0-nucleo")["pass_vuoto"]) for b in behs)
        np_ = sum(int(P(banco[g], b, "L0-nucleo")["npass"]) for b in behs)
        out.append(f"{pv}/{np_}")
    print(f"  L0 passaggi con un vuoto, {nome}: " + "  ".join(out))
tot = []
for g in "DTL":
    behs = comportamenti(banco[g])
    tot.append(sum(int(P(banco[g], b, "L0-nucleo")["pass_vuoto"]) for b in behs))
tot5 = []
for g in "DTL":
    tot5.append(sum(int(P(banco[g], b, "L0-nucleo")["pass_vuoto"]) for b in PERCORSO))
esito("1. Nucleo (L0): passaggi con un vuoto, D/T/L", "1958 / 1991 / 1999 (su circa 2000)",
      f"7 comportamenti: {tot}; 5 sul percorso: {tot5}", tot5 == [1958, 1991, 1999] or tot == [1958, 1991, 1999])

# 2. quota dei cicli con una regione, nucleo
q = []
for g in "DTL":
    behs = comportamenti(banco[g])
    cr = sum(int(P(banco[g], b, "L0-nucleo")["cicli_regione"]) for b in behs)
    ci = sum(int(P(banco[g], b, "L0-nucleo")["cicli"]) for b in behs)
    cr5 = sum(int(P(banco[g], b, "L0-nucleo")["cicli_regione"]) for b in PERCORSO)
    ci5 = sum(int(P(banco[g], b, "L0-nucleo")["cicli"]) for b in PERCORSO)
    q.append((round(100 * cr / ci, 1), round(100 * cr5 / ci5, 1)))
esito("2. Nucleo (L0): cicli senza osservazione con una regione, %", "19 / 38 / 33",
      f"(7 comportamenti, 5 sul percorso) per D,T,L: {q}",
      all(abs(a - w) <= 1.0 or abs(b - w) <= 1.0 for (a, b), w in zip(q, (19, 38, 33))))

# 3. C-004: cella peggiore sul percorso fino a 3 s, con i due denominatori
for den in ("griglia", "tutti"):
    out = []
    for g in "DTL":
        peggio = None
        for b in PERCORSO:
            for tau in (0.5, 1.0, 2.0, 3.0):
                h = H(banco[g], b, "C-004", tau)
                n = h["n"] - (h["fuori_griglia"] if den == "griglia" else 0)
                if n < 30:
                    continue
                c = h["in90"] / n
                if peggio is None or c < peggio[0]:
                    peggio = (c, int(h["in90"]), int(n), b, tau)
        out.append(peggio)
    testo = "; ".join(f"{g}: {p[1]}/{p[2]}={p[0]:.3f} ({p[3]}, {p[4]} s)" for g, p in zip("DTL", out))
    if den == "griglia":
        esito("3. C-004 (banco): cella peggiore sul percorso fino a 3 s, denominatore «dentro l'area osservata»",
              "D 86/92, T 370/386, L 357/380 (0,935 / 0,959 / 0,939)", testo,
              [(p[1], p[2]) for p in out] == [(86, 92), (370, 386), (357, 380)])
    else:
        print("      con il denominatore «tutti i nascosti»:", testo)

# 4. O1: stessa cella con i due denominatori
h = H(banco["D"], "prosegue", "C-004", 3.0)
esito("4. O1, banco, «prosegue» a 3 s in D: 86/92 (area osservata) e 86/98 (tutti)", "86/92 e 86/98",
      f"in90={int(h['in90'])} n={int(h['n'])} fuori_griglia={int(h['fuori_griglia'])} -> {int(h['in90'])}/{int(h['n']-h['fuori_griglia'])} e {int(h['in90'])}/{int(h['n'])}",
      (int(h["in90"]), int(h["n"] - h["fuori_griglia"]), int(h["n"])) == (86, 92, 98))

# 5. R100 contiene il nascosto: in100 == n in ogni riga H di ogni predittore ritagliato
fuori = 0
righe_h = 0
camp = 0
for g in "DTL":
    for d in banco[g]:
        if d["tipo"] == "H":
            kv = d["kv"]
            righe_h += 1
            n = int(kv["n"]); i100 = int(kv["in100"]); fg = int(kv["fuori_griglia"])
            camp += n
            # chi e' fuori griglia e' "non osservato": conta dentro R100 per definizione del banco
            if i100 != n:
                fuori += n - i100
esito("5. R100 (strato 1) contiene il nascosto nel 100 % (banco, tutte le righe H)", "100 %, 0 fuori",
      f"righe H {righe_h}, campioni {camp}, fuori da R100: {fuori}", fuori == 0)

# 6. R90 su visto libero oltre la fascia e R90 fuori da R100, predittori ritagliati
for pred in ("C-004", "C-005", "C-001+C-008", "C-EST-A", "C-EST-B", "L2r-filtro-ritagliato"):
    s1 = s2 = 0
    for g in "DTL":
        for b in comportamenti(banco[g]):
            p = P(banco[g], b, pred)
            s1 += int(p["R90_su_libero_cicli"]); s2 += int(p["R90_fuori_R100_cicli"])
    print(f"      {pred}: cicli R90 su visto libero oltre la fascia {s1}; cicli R90 fuori da R100 {s2}")
s = 0
for g in "DTL":
    for b in comportamenti(banco[g]):
        p = P(banco[g], b, "C-004")
        s += int(p["R90_su_libero_cicli"]) + int(p["R90_fuori_R100_cicli"])
esito("6. C-004: 0 cicli di R90 su visto libero oltre la fascia, 0 fuori da R100 (banco)", "0 e 0", f"somma {s}", s == 0)

# 7. C-EST su «sosta» a 3 s
out = {}
for g in "DTL":
    for l in ("C-EST-A", "C-EST-B"):
        h = H(banco[g], "sosta", l, 3.0)
        n = h["n"] - h["fuori_griglia"]
        out[(g, l)] = (int(h["in90"]), int(n), round(h["in90"] / n, 3) if n else None)
esito("7. C-EST su «sosta» a 3 s (K-206): D 0,95 e 1,00; T 0,72 e 0,53; L 0,14 e 0,00", "vedi a sinistra", str(out),
      abs(out[("T", "C-EST-A")][2] - 0.72) <= 0.01 and abs(out[("T", "C-EST-B")][2] - 0.53) <= 0.01
      and abs(out[("L", "C-EST-A")][2] - 0.14) <= 0.01 and abs(out[("L", "C-EST-B")][2] - 0.00) <= 0.01)

# 8. attacco 5: prima misura nell'ellisse al 95 % dichiarata, «prosegue»
out = {}
for g in "DTL":
    for l in ("C-EST-A", "C-EST-B"):
        a, b = P(banco[g], "prosegue", l)["porta95"].split("/")
        out[(g, l)] = (int(a), int(b), round(int(a) / int(b), 3) if int(b) else None)
esito("8. Attacco 5 su C-EST (banco, «prosegue»): A 0,28 / 0,30 / 0,00; B 0,997 / 0,71 / 0,00", "vedi a sinistra", str(out),
      all(abs(out[(g, "C-EST-A")][2] - w) <= 0.01 for g, w in zip("DTL", (0.28, 0.30, 0.00)))
      and all(abs(out[(g, "C-EST-B")][2] - w) <= 0.01 for g, w in zip("DTL", (0.997, 0.71, 0.00))))

# 9. C-EST: passaggi con cicli «perso»
out = {}
for g in "DTL":
    for l in ("C-EST-A", "C-EST-B"):
        s = 0
        for d in banco[g]:
            if d["tipo"] == "E" and d["campi"][3] == l and d["campi"][2] in PERCORSO:
                s += int(d["kv"]["pass_perso"])
        s7 = 0
        for d in banco[g]:
            if d["tipo"] == "E" and d["campi"][3] == l:
                s7 += int(d["kv"]["pass_perso"])
        out[(g, l)] = (s, s7)
esito("9. C-EST: passaggi con cicli «perso» (K-201): T 374 e 1312, L 1976 e 1987, D 2 e 2 su circa 2000",
      "vedi a sinistra", "(5 sul percorso, 7 comportamenti) " + str(out),
      any(out[("T", "C-EST-A")][i] == 374 and out[("T", "C-EST-B")][i] == 1312 and out[("L", "C-EST-A")][i] == 1976
          and out[("L", "C-EST-B")][i] == 1987 for i in (0, 1)))

# 10. demo: «metà dell'ombra» scatta prima della ricomparsa
for d in banco["D"]:
    if d["tipo"] == "G" and d["campi"][2] == "prosegue":
        kv = d["kv"]
        esito("10. Nucleo in demo: «metà» scatta prima della ricomparsa in 332 transiti su 355; «previsto» 0,67 s",
              "332/355; 0,667 s (0,60-0,73)",
              f"L0_perso_prima={kv['L0_perso_prima']} ricomparsi={kv['ricomparsi']} durata={kv['L0_durata_previsto_med']} q25={kv['q25']} q75={kv['q75']}",
              (kv["L0_perso_prima"], kv["ricomparsi"], kv["L0_durata_previsto_med"]) == ("332", "355", "0.667"))

print("=" * 100)
print("B. SOLUZIONE (13-soluzione/ris/prova_*.tsv)")
sol = {g: leggi_tsv(f"{F8}/13-soluzione/ris/prova_{g}.tsv") for g in "DTL"}
out = []
for g in "DTL":
    behs = comportamenti(sol[g])
    out.append((sum(int(P(sol[g], b, "sd-1")["pass_vuoto"]) for b in behs),
                sum(int(P(sol[g], b, "sd-1")["npass"]) for b in behs),
                sum(int(P(sol[g], b, "sd-0")["pass_vuoto"]) for b in behs)))
esito("11. sd-1: passaggi con un ciclo senza regione 0 / 0 / 0 su 2716 / 2800 / 2798 (anche sd-0: 0)", "0/2716, 0/2800, 0/2798",
      str(out), [(a, b) for a, b, c in out] == [(0, 2716), (0, 2800), (0, 2798)] and all(c == 0 for a, b, c in out))

h = H(sol["D"], "prosegue", "sd-1", 3.0)
esito("12. O1, soluzione, «prosegue» a 3 s in D: 101/119 (tutti) e 101/105 (area osservata)", "101/119 e 101/105",
      f"in90={int(h['in90'])} n={int(h['n'])} fuori_griglia={int(h['fuori_griglia'])}",
      (int(h["in90"]), int(h["n"]), int(h["n"] - h["fuori_griglia"])) == (101, 119, 105))

for den in ("tutti", "griglia"):
    o = []
    for g in "DTL":
        peggio = None
        for b in PERCORSO:
            for tau in (0.5, 1.0, 2.0, 3.0):
                h = H(sol[g], b, "sd-1", tau)
                n = h["n"] - (h["fuori_griglia"] if den == "griglia" else 0)
                if n < 30:
                    continue
                c = h["in90"] / n
                if peggio is None or c < peggio[0]:
                    peggio = (c, int(h["in90"]), int(n), b, tau)
        o.append(peggio)
    testo = "; ".join(f"{g}: {p[1]}/{p[2]}={p[0]:.3f} ({p[3]}, {p[4]} s)" for g, p in zip("DTL", o))
    if den == "tutti":
        esito("13. sd-1: minimo sul percorso fino a 3 s, denominatore «tutti»: 0,849 / 0,962 / 0,920", "0,849 / 0,962 / 0,920",
              testo, all(abs(p[0] - w) < 0.0006 for p, w in zip(o, (0.849, 0.962, 0.920))))
    else:
        print("      con il denominatore «dentro l'area osservata»:", testo)

out = []
for g in "DTL":
    for d in sol[g]:
        if d["tipo"] == "G" and d["campi"][2] == "prosegue":
            out.append(d["kv"]["C1_riaggancio"])
esito("14. Riaggancio dei «prosegue» nei dati stessi della soluzione (regola del nucleo): 212/331, 336/345, 207/232",
      "212/331, 336/345, 207/232", str(out), out == ["212/331", "336/345", "207/232"])

out = []
for g in "DTL":
    behs = comportamenti(sol[g])
    a = sum(int(P(sol[g], b, "sd-1")["ampio80"]) for b in behs)
    c = sum(int(P(sol[g], b, "sd-1")["cicli"]) for b in behs)
    out.append(round(100 * a / c, 1))
esito("15. sd-1: cicli «ampio» (area > 80 % dell'ombra): 50,4 % in D, 0,0 % in T e L", "50,4 / 0,0 / 0,0", str(out),
      abs(out[0] - 50.4) <= 0.15 and out[1] <= 0.05 and out[2] <= 0.05)

fuori = camp = 0
for g in "DTL":
    for d in sol[g]:
        if d["tipo"] == "H" and d["campi"][3] in ("sd-1", "sd-0"):
            fuori += int(d["kv"]["n"]) - int(d["kv"]["in100"]); camp += int(d["kv"]["n"])
esito("16. R100 contiene il nascosto (soluzione, righe H di sd-0 e sd-1)", "100 %", f"campioni {camp}, fuori {fuori}", fuori == 0)

print("      punto ibrido (sd-1), «prosegue»: passaggi con un passo indietro / passaggi; punto su libero dopo il quinto ciclo (somma 7 comportamenti)")
for g in "DTL":
    p = P(sol[g], "prosegue", "sd-1")
    dopo5 = sum(int(P(sol[g], b, "sd-1")["punto_su_libero_dopo5"]) for b in comportamenti(sol[g]))
    print(f"        {g}: {p['pass_indietro']}/{p['npass']} = {100*int(p['pass_indietro'])/int(p['npass']):.1f} %; dopo5 = {dopo5}; re40 = {p['re40']}/{p['nre']}")

print("=" * 100)
print("C. CONTROPROVE (14-attacco/ris/*.txt)")


def testo(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


t = testo(f"{F8}/14-attacco/ris/tutto_T.txt")
m = re.search(r"^prosegue .*?R90 grezza a 1/2/3/5 s: (\d+/\d+)=\S+ (\d+/\d+)=", t, re.M)
esito("17. «Tutto insieme» (T, corpo esteso, ombra −20 cm, rilevamento 0,7): «prosegue» 136/364 a 1 s e 43/152 a 2 s",
      "136/364, 43/152", f"{m.group(1)}, {m.group(2)}", (m.group(1), m.group(2)) == ("136/364", "43/152"))

out = []
for g in "DTL":
    t = testo(f"{F8}/14-attacco/ris/sess_{g}.txt")
    m = re.search(r"prima_ambigua_al_passaggio=(\d+) ricomparse_dopo=(\d+) riagganciate_dopo=(\d+) pendenti_alla_fine=(\d+)", t)
    out.append(tuple(int(x) for x in m.groups()))
esito("18. Sessione con la regola 2: prima «ambigua» al passaggio 1 (D) e 4 (T); riagganci dopo 0/66 e 0/100; pendenti 87 / 117 / 95",
      "D (1, 66, 0, 87); T (4, 100, 0, 117); L pendenti 95", str(out),
      out[0] == (1, 66, 0, 87) and out[1] == (4, 100, 0, 117) and out[2][3] == 95)

out = []
for g in "DTL":
    t = testo(f"{F8}/14-attacco/ris/base_{g}.txt")
    i = t.index("\nprosegue")
    m = re.search(r"ricomparsi=(\d+) riagganciati=(\d+)", t[i:])
    out.append(f"{m.group(2)}/{m.group(1)}")
esito("19. Riaggancio composto, corpo esteso, «prosegue»: 102/273, 306/397, 250/332", "102/273, 306/397, 250/332", str(out),
      out == ["102/273", "306/397", "250/332"])

t = testo(f"{F8}/14-attacco/ris/fermo_T.txt")
m = re.search(r"a corpo tutto nascosto: (\d+/\d+)=\S+ (\d+/\d+)=\S+ (\d+/\d+)=", t)
esito("20. Parte da fermo accanto al pannello (T), R90 a corpo tutto nascosto: 15/141, 21/134, 14/54", "15/141, 21/134, 14/54",
      ", ".join(m.groups()), m.groups() == ("15/141", "21/134", "14/54"))

t = testo(f"{F8}/14-attacco/ris/base_D.txt")
i = t.index("\nprosegue")
m = re.search(r"ampio_prima_della_ricomparsa=(\d+/\d+)", t[i:])
m2 = re.search(r"tempo al segno ampio \(o alla ricomparsa\), mediana=([0-9.]+)", t[i:])
esito("21. Demo: «ampio» prima della ricomparsa in 269/273 «prosegue»; tempo mediano 1,00 s", "269/273; 1,00 s",
      f"{m.group(1)}; {m2.group(1)} s", m.group(1) == "269/273" and abs(float(m2.group(1)) - 1.0) < 0.006)

fu = 0; nf = 0; vu = 0; celle = 0
for p in sorted(glob.glob(f"{F8}/14-attacco/ris/*.txt")):
    t = testo(p)
    v = re.findall(r"fuori_R100=(\d+)", t)
    if v:
        nf += 1; celle += len(v); fu += sum(int(x) for x in v)
    vu += sum(int(x) for x in re.findall(r" vuoti=(\d+)", t))
esito("22. Controprove: 0 passaggi con il centro nascosto fuori da R100 in 156 celle (63 file); 0 cicli senza regione",
      "0 fuori in 156 celle; 0 vuoti", f"file con il campo {nf}, celle {celle}, fuori_R100 totale {fu}, vuoti totale {vu}",
      fu == 0 and vu == 0 and celle == 156)

t = testo(f"{F8}/14-attacco/ris/tempo_py.txt")
m = re.findall(r"tracce=(\d+) .*?mediana=([0-9.]+) ms p95=([0-9.]+)", t)
esito("23. Costo in Python puro: 0,6 ms (1 traccia), 1,8 ms (3), 5,3 ms mediana e 6,2 al 95º (10)", "0,6; 1,8; 5,3 / 6,2",
      str(m), [(a, b) for a, b, c in m] == [("1", "0.6"), ("3", "1.8"), ("10", "5.3")] and m[2][2] == "6.2")

t = testo(f"{F8}/14-attacco/ris/tutto_T_e0_pd07.txt")
sc = [int(x) for x in re.findall(r"scoperti=(\d+)", t)]
va = [int(x) for x in re.findall(r"validi=(\d+)", t)]
esito("24. Rilevamento 0,7 e maschera esatta: scoperti 130 passaggi su 1581", "130/1581", f"{sum(sc)}/{sum(va)}",
      (sum(sc), sum(va)) == (130, 1581))

print("=" * 100)
print("D. TORNEO (12-torneo/ris)")
t = testo(f"{F8}/12-torneo/ris/a8_estraneo_T.txt")
m = re.search(r"con il primo ancora nascosto (\d+) \| riagganciato dalla regola del nucleo \(entro 0,40 dall'ombra\) (\d+)", t)
esito("25. Estraneo dalla stessa ombra (torneo): la regola del nucleo lo riaggancia in 347 casi su 357", "347/357",
      f"{m.group(2)}/{m.group(1)}", m.groups() == ("357", "347"))

t = testo(f"{F8}/12-torneo/ris/a17_s2.txt")
print("      a17_s2.txt (S2), righe con 'median' o 'ombra':")
for r in t.splitlines():
    if re.search(r"median|ombra|dentro", r, re.I):
        print("        " + r[:230])

print("=" * 100)
print("E. STATISTICA (15-statistica/ris): semi riparati, sd-1, «prosegue» in D con il denominatore «tutti»")
tot = {}
for p in sorted(glob.glob(f"{F8}/15-statistica/ris/semi_D_*x400.tsv")):
    r = leggi_tsv(p)
    for tau in (1.0, 2.0, 3.0, 5.0):
        h = H(r, "prosegue", "sd-1", tau)
        a, b, c = tot.get(tau, (0, 0, 0))
        tot[tau] = (a + int(h["in90"]), b + int(h["n"]), c + int(h["n"] - h["fuori_griglia"]))
print("      ", {k: (v, round(v[0] / v[1], 3), round(v[0] / v[2], 3)) for k, v in tot.items()})
esito("26. Semi riparati, D, «prosegue»: 0,899 a 3 s e 174/221 = 0,787 a 5 s (denominatore «tutti»); 513 nascosti a 3 s",
      "0,899; 174/221; 513", f"3 s: {tot[3.0][0]}/{tot[3.0][1]} = {tot[3.0][0]/tot[3.0][1]:.3f}; 5 s: {tot[5.0][0]}/{tot[5.0][1]}",
      abs(tot[3.0][0] / tot[3.0][1] - 0.899) < 0.0006 and (tot[5.0][0], tot[5.0][1]) == (174, 221) and tot[3.0][1] == 513)

# spostamento: L a 2 e 3 s, minimo sul percorso, denominatore di B
for nome in ("semi_spostato_L_90000x400.tsv", "spostato_L_30000x400.tsv"):
    p = f"{F8}/15-statistica/ris/{nome}"
    if os.path.exists(p):
        r = leggi_tsv(p)
        o = {}
        for lim in (1.0, 2.0, 3.0):
            peggio = None
            for b in PERCORSO:
                for tau in (0.5, 1.0, 2.0, 3.0):
                    if tau > lim:
                        continue
                    h = H(r, b, "sd-1", tau)
                    n = h["n"] - h["fuori_griglia"]
                    if n < 30:
                        continue
                    c = h["in90"] / n
                    if peggio is None or c < peggio[0]:
                        peggio = (round(c, 3), int(h["in90"]), int(n), b, tau)
            o[lim] = peggio
        print(f"      {nome}: minimo sul percorso fino a 1/2/3 s: {o}")
r = leggi_tsv(f"{F8}/15-statistica/ris/semi_spostato_L_90000x400.tsv")
o = {}
for lim in (2.0, 3.0):
    peggio = None
    for b in PERCORSO:
        for tau in (0.5, 1.0, 2.0, 3.0):
            if tau > lim:
                continue
            h = H(r, b, "sd-1", tau)
            n = h["n"] - h["fuori_griglia"]
            if n >= 30 and (peggio is None or h["in90"] / n < peggio):
                peggio = h["in90"] / n
    o[lim] = round(peggio, 3)
esito("27. Camminatori meno regolari della libreria (spostamento dello statistico), L: 0,835 fino a 2 s e 0,801 fino a 3 s",
      "0,835; 0,801", str(o), abs(o[2.0] - 0.835) < 0.0011 and abs(o[3.0] - 0.801) < 0.0011)

print("=" * 100)
print("F. CONTROLLO MIO, indipendente dal codice altrui: i semi contigui di gen.h danno lo stesso flusso spostato di uno")
M64 = (1 << 64) - 1
G = 0x9E3779B97F4A7C15


def u64(s):
    s = (s + G) & M64
    z = s
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & M64
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & M64
    return s, z ^ (z >> 31)


def flusso(seed, geo, beh, stream, n):
    s = (seed * G + geo * 0xD1B54A32D192ED03 + beh * 0x8CB92BA72F3D8DD7 + stream * 0xABCDEF1234567) & M64
    s, _ = u64(s); s, _ = u64(s)
    out = []
    for _ in range(n):
        s, v = u64(s)
        out.append(v)
    return out


a = flusso(9000, ord("T"), 0, 1, 1001)
b = flusso(9001, ord("T"), 0, 1, 1000)
uguali = sum(1 for i in range(1000) if a[i + 1] == b[i])
esito("28. rng_seed di gen.h (riscritto in Python dalle righe 25-40): flusso del seme 9001 = flusso del seme 9000 avanzato di 1",
      "1000 uguali su 1000 (15-statistica/ris/prova_semi.txt)", f"{uguali} su 1000", uguali == 1000)

print("=" * 100)
print("G. ORE (conti sulle cifre scritte nei documenti; le ore sono stime degli autori, non verificate)")
c_min = 0.5 + 1 + 1 + 0.25 + 0.25 + 0.5 + 0.5 + 0.25
c_max = 0.5 + 1 + 2 + 0.25 + 0.25 + 0.5 + 0.5 + 0.25
print(f"      correzioni c1-c8 (fascia 14 ore): {c_min}-{c_max} ore-persona")
m_min = 0.5 + 1 + 2 + 3 + 2 + 4 + 1 + 2
m_max = 0.5 + 1 + 2 + 5 + 3 + 5 + 1 + 2
print(f"      M1-M8 (somma delle righe della tabella 2.11): {m_min}-{m_max} ore-persona; senza M4: {m_min-3}-{m_max-5}")
base = 54 - 4 - 4 - 2 - 1 - 6
print(f"      nucleo tagliato: 54-4-4-2-1-6 = {base}; + 15,5 + 4 = {base+15.5+4}; con sd-0 soltanto: {base+15.5+4-4}")
tot_lo = base + 15.5 + 4 + c_min + 0.25 + 0.5
tot_hi = base + 15.5 + 4 + c_max + 0.25 + 0.5 + 2
print(f"      con c1-c8 e le righe dello statistico (0,25 + 0,5; le camminate fino a 2): {tot_lo}-{tot_hi}; senza M4 (-4): {tot_lo-4}-{tot_hi-4}")
print(f"      disponibili in 14 ore: 3 persone 42, 4 persone 56, 5 persone 70")
esito("29. Bilancio di M: 37 + 15,5 + 4 = 56,5; «circa 5 ore» per c1-c8", "56,5; circa 5", f"{base+15.5+4}; {c_min}-{c_max}",
      base + 15.5 + 4 == 56.5 and 4.0 <= c_min and c_max <= 5.5)

print("=" * 100)
ok = sum(1 for e in ESITI if e[3])
print(f"TOTALE: {ok} cifre (o gruppi di cifre) tornano su {len(ESITI)}")
for e in ESITI:
    if not e[3]:
        print("  NON TORNA:", e[0])
