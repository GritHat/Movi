# riepilogo.py — legge banco.json e scrive riepilogo_banco.txt (le tabelle della consegna). Nessun calcolo nuovo: somme e filtri.
import sys, os, json
QUI = os.path.dirname(os.path.abspath(__file__))
SUFF = ("_" + sys.argv[1]) if len(sys.argv) > 1 else ""
J = json.load(open(os.path.join(QUI, "banco%s.json" % SUFF)))
R, NF = J["righe"], J["NF"]
REG = ("SC", "RP", "V17", "V18-1", "V18-m", "PR1", "PR2", "PR3", "PR4")
out = []
P = out.append


def somma(filtro, r):
    s = [x for x in R if x["regola"] == r and filtro(x)]
    return (len(s), sum(x["dentro"] for x in s), sum(x["profonde"] for x in s), sum(x["nascoste"] for x in s),
            sum(x["qv"] for x in s), sum(x["fot_viol"] for x in s), len(s) * NF)


P("# riepilogo di banco.json — %d fotogrammi per condizione" % NF)
for titolo, f in (("S1a — le 16 combinazioni x 5 buchi, errore d'inclinazione 0 e ±0,5 gradi", lambda x: x["sedici"] and abs(x["err"]) <= 0.5),
                  ("S1b — le 16 combinazioni x 5 buchi, errore +1 grado (camera piu' in basso di quanto crede)", lambda x: x["sedici"] and x["err"] == 1.0),
                  ("S1c — le 16 combinazioni x 5 buchi, errore -1 grado (camera piu' in alto di quanto crede)", lambda x: x["sedici"] and x["err"] == -1.0),
                  ("S1d — [in piu'] corpo muto, 2 k x 5 buchi, errore 0 e ±0,5", lambda x: "muto" in x["scena"] and abs(x["err"]) <= 0.5),
                  ("S1e — [in piu'] scatola 0,10 m a 2,6-2,9 m, 2 k x 5 buchi, errore 0 e ±0,5", lambda x: "2,6-2,9" in x["scena"] and abs(x["err"]) <= 0.5),
                  ("S1f — le due scene in piu', errore ±1", lambda x: not x["sedici"] and abs(x["err"]) == 1.0)):
    P("\n" + titolo)
    P("regola  condizioni  celle libere: dentro un corpo (di cui oltre 5 cm) | suolo nascosto | q_v >= base del sospeso | fotogrammi con violazione")
    for r in REG:
        n, d, p, na, q, fv, ft = somma(f, r)
        P("%-6s  %4d        %6d (%6d) | %6d | %4d | %5d su %d" % (r, n, d, p, na, q, fv, ft))

P("\nDove cadono V18-m e le varianti prudenti (condizioni con almeno una violazione, errore fra -0,5 e +0,5):")
for x in R:
    if x["regola"] in ("V18-m", "PR1", "PR2", "PR3", "PR4") and abs(x["err"]) <= 0.5 and (x["dentro"] + x["nascoste"] + x["qv"]):
        P("  %-5s k=%.4f %-34s err %+4.1f %-12s dentro %d (prof %d) nasc %d qv %d, fot. %d/%d" % (x["regola"], x["k"], x["scena"], x["err"], x["buchi"], x["dentro"], x["profonde"], x["nascoste"], x["qv"], x["fot_viol"], NF))
P("\nDove cadono V18-m e le varianti prudenti a ±1 grado (solo le righe con celle oltre 5 cm dentro un corpo o suolo nascosto):")
for x in R:
    if x["regola"] in ("V18-m", "PR1", "PR2", "PR3", "PR4") and abs(x["err"]) == 1.0 and (x["profonde"] + x["nascoste"] + x["qv"]):
        P("  %-5s k=%.4f %-34s err %+4.1f %-12s dentro %d (prof %d) nasc %d qv %d, fot. %d/%d" % (x["regola"], x["k"], x["scena"], x["err"], x["buchi"], x["dentro"], x["profonde"], x["nascoste"], x["qv"], x["fot_viol"], NF))

P("\nS2 — stanza vuota, errore 0: mediana per settore (m) | resa (%) | cambi per cella al secondo | «sconosciuto» (%)")
for k in (0.004, 0.01):
    for b in ("nessuno", "sparsi 5 %", "sparsi 30 %", "chiazze 5 %", "chiazze 30 %"):
        riga = "k=%.4f %-12s" % (k, b)
        for r in REG:
            x = [y for y in R if y["regola"] == r and y["k"] == k and y["buchi"] == b and y["scena"] == "stanza vuota" and y["err"] == 0.0][0]
            riga += " | %-5s %.1f m %5.1f %% %.2f/s %5.1f %%" % (r, x["mediana_m"], x["resa"], x["cambi_s"], x["sconosciuto"])
        P(riga + "   [settori-fotogramma %d]" % (x["settori"] * NF))

P("\nInclinazione — stanza vuota, senza buchi e col 5 % sparso: resa (%) e mediana per settore (m) per errore")
for k in (0.004, 0.01):
    for b in ("nessuno", "sparsi 5 %"):
        for e in (-1.0, -0.5, 0.0, 0.5, 1.0):
            riga = "k=%.4f %-10s err %+4.1f" % (k, b, e)
            for r in REG:
                x = [y for y in R if y["regola"] == r and y["k"] == k and y["buchi"] == b and y["scena"] == "stanza vuota" and y["err"] == e][0]
                riga += " | %-5s %5.1f %% %.1f m" % (r, x["resa"], x["mediana_m"])
            P(riga)

P("\nResa media (%) sulle 16 combinazioni, errore 0, per buchi")
for b in ("nessuno", "sparsi 5 %", "sparsi 30 %", "chiazze 5 %", "chiazze 30 %"):
    riga = "%-12s" % b
    for r in REG:
        s = [y["resa"] for y in R if y["regola"] == r and y["buchi"] == b and y["sedici"] and y["err"] == 0.0]
        riga += " | %-5s %5.1f (min %5.1f)" % (r, sum(s) / len(s), min(s))
    P(riga)
P("\nCelle libere sotto un ostacolo sospeso (suolo visto, nessuna quota dichiarata salvo V17), errore 0, tutte le condizioni: " +
  ", ".join("%s %d" % (r, sum(y["sotto_sospeso"] for y in R if y["regola"] == r and y["err"] == 0.0)) for r in REG))
open(os.path.join(QUI, "riepilogo_banco%s.txt" % SUFF), "w").write("\n".join(out) + "\n")

