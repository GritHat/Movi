"""Consegna finale (copia di 81-qa/controlla.py): verde, OCR (etichetta e lessico) su un fotogramma ogni 2 s. Uso: python3 -I controlla.py <cartella> <lingua_tess>"""
import sys, os, re, subprocess, json

cart, lang = sys.argv[1], sys.argv[2]
VIET = [r"validat", r"guarant", r"detect and avoid", r"threat", r"target", r"counter.?drone", r"\balways\b",
        r"\bnever\b", r"sub.?milli", r"real.?time", r"detects the collision", r"intercept", r"engage", r"hostile",
        r"weapon", r"pursu", r"chase", r"certif", r"validat", r"garantit", r"minaccia", r"bersaglio", r"sempre",
        r"\bmai\b", r"tempo reale", r"anti.?drone", r"intercett", r"\bfree\b", r"\blibero\b", r"\bclear\b",
        r"\bsafe\b", r"sicuro"]
out = {}
for f in sorted(os.listdir(cart)):
    if not f.endswith(".png"):
        continue
    p = os.path.join(cart, f)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, timeout=60).stdout
    n_verde = sum(1 for r, g, b in zip(raw[0::3], raw[1::3], raw[2::3]) if g > 90 and g > r + 40 and g > b + 40)
    txt = subprocess.run(["tesseract", p, "-", "-l", lang, "--psm", "11"], capture_output=True, text=True,
                         timeout=60).stdout
    t = " ".join(txt.split())
    eti = bool(re.search(r"SIMULAT|SCHEMATIC|SIMULAZ|SCHEMATIC", t, re.I))
    hits = sorted({m.group(0).lower() for v in VIET for m in re.finditer(v, t, re.I)})
    out[f] = {"t_s": (int(f[1:4]) - 1) * 2, "verde_px": n_verde, "etichetta": eti, "parole": hits, "testo": t}
json.dump(out, open(os.path.join(cart, "..", "ocr_" + os.path.basename(cart.rstrip('/')) + ".json"), "w"),
          ensure_ascii=False, indent=1)
for f, v in out.items():
    if v["verde_px"] > 0 or not v["etichetta"] or v["parole"]:
        print(f, v["t_s"], "verde", v["verde_px"], "eti", v["etichetta"], v["parole"])
print("totale", len(out), "senza etichetta", sum(not v["etichetta"] for v in out.values()),
      "con verde>200", sum(v["verde_px"] > 200 for v in out.values()))
