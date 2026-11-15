"""Riconto dell'arbitro (fase 2): rilegge i file dei risultati e ricalcola i Wilson con codice proprio.
Uso: python -I riconto.py <cartella f15-lunga-portata>"""
import json, math, sys, os

B = sys.argv[1]
Z = 1.959963984540054


def wil(k, n):
    if not n:
        return (None, None)
    p = k / n
    d = 1 + Z * Z / n
    c = (p + Z * Z / (2 * n)) / d
    h = Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / d
    return (round(max(0, c - h), 3), round(min(1, c + h), 3))


def r(f):
    return json.load(open(os.path.join(B, f)))


def kn(x):
    return f"{x[0]}/{x[1]} {wil(x[0], x[1])}"


for modo in ("interfaccia", "prudente"):
    d = r(f"11-prove/risultati_lp_{modo}.json")
    print(f"== {modo}: n per riga {d['n_per_scenario_config']}")
    tot_pass_senza = [0, 0]
    for k, v in d["scenari"].items():
        t = v["tempestivo"]; p = v["passaggi_con_ciclo_senza_regione"]; fa = v["cicli_nascosti_fuori_avviso"]
        lib = v.get("libero_su_oggetto", {})
        tot_pass_senza[0] += p[0]; tot_pass_senza[1] += p[1]
        libs = "; ".join(f"{c} {x[0]}/{x[1]}" for c, x in lib.items())
        print(f"{k:8s} tempestivo {kn(t)} | passaggi con ciclo senza regione {kn(p)} | "
              f"cicli fuori avviso {fa[0]}/{fa[1]} | d_conf {v['d_conf_m_mediana_p5']} rich {v['d_richiesta_m']} | "
              f"libero su oggetto {libs} | scambi {v['scambi'][0]}/{v['scambi'][1]} | errori {v['errori']}")
    print(f"   totale passaggi con ciclo senza regione: {tot_pass_senza[0]}/{tot_pass_senza[1]} {wil(*tot_pass_senza)}")

e = r("11-prove/risultati_eventi.json")["risultati"]
print("== eventi")
for k, v in e.items():
    s = f"{k:8s} n {v['n']} dichiarato {v['evento_dichiarato'][2]}/{v['evento_dichiarato'][3]} entro2s {kn(v['entro_2s'][:2])} " \
        f"falsi {kn(v['falsi_eventi'][:2])} fuori_avviso {v['fuori_avviso']} tracce_perse_senza_avviso {v['tracce_perse_senza_avviso']} " \
        f"libero_su_oggetto {v['libero_su_oggetto']} salute_dichiarata {v['salute_dichiarata']}"
    if v["frammenti_dentro_V"][1]:
        s += f" frammenti_dentro_V {kn(v['frammenti_dentro_V'][:2])}"
    print(s)

c = r("21-statistica/compara.json")
print("== traiettorie, divisione per mezzo (compara.json)")
for cl, dd in c.items():
    for D, x in dd.items():
        m = x.get("mezzo")
        if not m:
            continue
        fa = x.get("fuori_avv_mezzo")
        fas = f" fuori avviso {fa['k']}/{fa['n']} (mezzi con caso {fa['mezzi_con_almeno_un_caso']}/{fa['mezzi']})" if fa else ""
        print(f"{cl:6s} D={D:>3s} dentro {m['k']}/{m['n']} = {m['k']/m['n']:.3f} mezzi {m['mezzi']} "
              f"boot {[round(b,2) for b in m['boot']]} wilson_mezzi {[round(b,2) for b in m['wilson_mezzi']]}{fas}")

a = r("20-attacco/attacchi_esito.json")
print("== attacchi: chiavi", {k: (list(v.keys())[:6] if isinstance(v, dict) else type(v).__name__) for k, v in a.items()})
