"""riconto_scene_v3.py (sciame-arbitro): celle «libero» mostrate e tolte, e primo evento, per ogni scena _v3."""
import json, sys, glob, os
for d in sorted(glob.glob(os.path.join(sys.argv[1], "*_v3"))):
    lib = tolte = nfr = 0; ev = None; vc = json.load(open(os.path.join(d, "valida_video_controprova.txt")))
    for l in open(os.path.join(d, "registro.jsonl")):
        r = json.loads(l)
        if r.get("tipo") != "fotogramma": continue
        nfr += 1; c = r.get("celle") or {}
        lib += (c.get("conteggi") or {}).get("libero", 0); t = c.get("libere_tolte_dentro_avviso", 0)
        tolte += t if isinstance(t, (int, float)) else 0
        if ev is None:
            for k in ("eventi_improvvisi", "eventi", "evento"):
                if r.get(k): ev = (r["t"], json.dumps(r[k])[:200]); break
    print(os.path.basename(d), "fotogrammi", nfr, "libero mostrate", lib, "tolte", tolte, "controprova", {k: v.get("conteggi") for k, v in vc.items()}, "primo evento", ev)
