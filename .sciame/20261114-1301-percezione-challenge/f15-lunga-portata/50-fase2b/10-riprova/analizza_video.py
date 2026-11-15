"""analizza_video.py - per ogni registro di prototipo/uscite/video: durata, frequenza, e i secondi in cui succede
qualcosa (oggetti nascosti, avvisi accesi e spenti, eventi, detriti, sensori non affidabili, zone non verificate).
Uso: <venv>/bin/python -I -B analizza_video.py -> analisi_video.json (stampa un riassunto). Sola lettura."""
import glob
import json
import os
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
VID = os.path.abspath(os.path.join(QUI, "..", "..", "..", "..", "..", "prototipo", "uscite", "video"))


def intervalli(ts, passo=0.5):
    out = []
    for t in ts:
        if out and t - out[-1][1] <= passo + 1e-6:
            out[-1][1] = t
        else:
            out.append([t, t])
    return out


def analizza(f):
    L = [json.loads(x) for x in open(f, encoding="utf-8")]
    testa, fr, ria = L[0], [x for x in L if x.get("tipo") == "fotogramma"], L[-1]
    t = [x["t"] for x in fr]
    A = {"fotogrammi": len(fr), "t0": t[0], "t1": t[-1], "durata_s": round(t[-1] - t[0], 2),
         "frequenza_hz": round((len(fr) - 1) / (t[-1] - t[0]), 2) if len(fr) > 1 else None,
         "nucleo": testa.get("lunga_portata", {}).get("nucleo"), "passaggio": testa.get("lunga_portata", {}).get("passaggio"),
         "riassunto": {k: v for k, v in ria.items() if k != "tipo"}}
    nasc = {}
    for x in fr:
        for o in (x.get("verita") or {}).get("oggetti", []):
            if not o["visibile"] and not o["id"].startswith("fr"):
                nasc.setdefault(o["id"], []).append(x["t"])
    A["nascosti"] = {k: intervalli(v) for k, v in nasc.items()}
    acc = {}
    for x in fr:
        for a in x["avvisi"]:
            acc.setdefault(a["id_traccia"], []).append(x["t"])
    A["avvisi"] = {str(k): intervalli(v) for k, v in acc.items()}
    ev = {}
    for x in fr:
        for e in x["eventi"]:
            ev.setdefault(e["tipo"], []).append(x["t"])
    A["eventi"] = {k: {"primo": v[0], "n": len(v), "ultimo": v[-1]} for k, v in ev.items()}
    det = [x["t"] for x in fr if x.get("detriti")]
    A["detriti"] = None if not det else {"da": det[0], "a": det[-1],
                                         "impronta_raggio_m": next(x["detriti"]["impronta_raggio_m"] for x in fr if x.get("detriti")),
                                         "tracce_avvisate_fine": len(fr[-1]["detriti"]["tracce_avvisate"]) if fr[-1].get("detriti") else None}
    na = {}
    for x in fr:
        for s in x.get("affidabilita_per_sensore", []):
            if s["stato"] != "affidabile":
                na.setdefault(s["sensore"] + ":" + s["stato"], []).append(x["t"])
    A["sensori_non_affidabili"] = {k: intervalli(v) for k, v in na.items()}
    zn = {}
    for x in fr:
        for z in x.get("zona_non_verificata_per_classe", []):
            zn.setdefault(z["classe"], []).append(x["t"])
    A["zona_non_verificata_per_classe"] = {k: [v[0], v[-1], len(v)] for k, v in zn.items()}
    lib = {}
    for x in fr:
        for c in x.get("libero_per_classi", []):
            lib.setdefault(c, []).append(x["t"])
    A["libero_per_classi"] = {k: intervalli(v, 2.5) for k, v in lib.items()}
    cel = [(x["t"], x["celle"]["conteggi"].get("libero", 0)) for x in fr if x["celle"].get("conteggi")]
    A["celle_libere_pianta"] = cel[:: max(1, len(cel) // 12)]
    return A


if __name__ == "__main__":
    out = {}
    for f in sorted(glob.glob(os.path.join(VID, "*", "registro.jsonl"))):
        nome = os.path.basename(os.path.dirname(f))
        try:
            out[nome] = analizza(f)
            c = os.path.join(os.path.dirname(f), "convalida.txt")
            out[nome]["convalida"] = open(c).read().strip().splitlines()[-1] if os.path.exists(c) else None
            vv = glob.glob(os.path.join(os.path.dirname(f), "viste", "*.mp4")) + glob.glob(os.path.join(os.path.dirname(f), "viste", "*.gif"))
            out[nome]["filmati"] = [os.path.relpath(v, VID) for v in vv]
        except Exception as x:                      # registro interrotto: lo si dice
            out[nome] = {"errore": repr(x)}
    json.dump(out, open(os.path.join(QUI, "analisi_video.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for k, v in out.items():
        print("==", k, json.dumps(v, ensure_ascii=False)[:1500])
