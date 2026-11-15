"""confronta_un_passaggio.py - UN passaggio A1 'alta' (indice 0) di prove_lp con il nucleo v1 e con v2, regole di
prove_lp (v1 o v2). Un passaggio solo: esistenza, non frequenza. Uso: python -I -B confronta_un_passaggio.py"""
import json, os, sys, types
sys.dont_write_bytecode = True
QUI = os.path.dirname(os.path.abspath(__file__)); F15 = os.path.dirname(os.path.dirname(QUI))
sys.path[:0] = [QUI, os.path.join(F15, "04-moto"), os.path.join(F15, "10-simulatore")]
import movi_lp as m1, movi_lp_v2 as m2
out = {}
for nome, mod, reg in (("v1", m1, None), ("v2_regole_v1", m2, None), ("v2_regole_v2", m2, os.path.join(QUI, "regole_lunga_portata_v2.json"))):
    for k in [k for k in sys.modules if k in ("prove_lp", "movi_lp_import")]:
        del sys.modules[k]
    sys.modules["movi_lp_import"] = types.SimpleNamespace(nucleo=mod)
    import prove_lp as P
    if reg:
        P.REG = mod.carica_regole(reg)
    R = P.passaggio("A1", "alta", 0, chiamante=sys.argv[1] if len(sys.argv) > 1 else "interfaccia")
    out[nome] = {k: v for k, v in R.items() if not isinstance(v, (list, dict)) or k.startswith("libero")}
json.dump(out, open(os.path.join(QUI, "confronta_un_passaggio_esito.json"), "w"), ensure_ascii=False, indent=1, default=str)
for k in out["v1"]:
    print("%-28s" % k, *("%-22s" % str(out[n].get(k))[:22] for n in out))
