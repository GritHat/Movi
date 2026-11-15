#!/usr/bin/env python3
"""Monta il progetto HyperFrames: dai file di scena, dei tempi, dei testi e del marchio scrive
  tempi/scene_tempi.js   (window.__SCENE: scene con inizio e durata, registri e loro stato)
  testi/testi.js         (window.__TESTI = {en, it}; window.__LINGUA)
  assets/marchio/marchio.js  (wordmark come data URI, dai SVG di video/marchio copiati in assets/marchio)
  index.html             (composizione radice; la versione precedente si COPIA in versioni/ prima di riscriverla)
Se manca assets/data/sottotitoli.js ne scrive uno vuoto.

Uso:  python3 -I strumenti/monta.py [--lingua en|it] [--finale]
  --finale  rifiuta il montaggio se un registro in uso è «sviluppo», se un testo a schermo o un sottotitolo contiene
            ancora [CIFRA…], [STATO…], [k], [n], [DA FORNIRE] (Q24) o se i sottotitoli sono stimati.
"""
import argparse, base64, json, os, re, shutil, sys, time

QUI = os.path.dirname(os.path.abspath(__file__))
R = os.path.dirname(QUI)
SEGNAPOSTO = re.compile(r"\[(CIFRA[^\]]*|STATO[^\]]*|k|n|DA FORNIRE)\]")


def carica(p):
    return json.load(open(p, encoding="utf-8"))


def scrivi(p, s):
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lingua", default=None)
    ap.add_argument("--finale", action="store_true")
    a = ap.parse_args()
    S = carica(os.path.join(R, "scene", "scene.json"))
    lingua = a.lingua or S.get("lingua", "en")
    pt = os.path.join(R, "tempi", "scene_tempi.json")
    tempi = {s["id"]: s for s in carica(pt)["scene"]} if os.path.exists(pt) else {}
    t, scene = 0.0, []
    for sc in S["scene"]:
        x = dict(sc)
        if sc["id"] in tempi:
            x["durata"] = tempi[sc["id"]]["durata"]
            if tempi[sc["id"]].get("segmenti"):
                x["segmenti"] = tempi[sc["id"]]["segmenti"]
        x["inizio"] = round(t, 4)
        t += x["durata"]
        scene.append(x)
    D = round(t, 4)
    usati = {g["registro"] for sc in scene for g in sc.get("segmenti") or []} | {sc["intest_da"] for sc in scene if sc.get("intest_da")}
    reg = {k: {kk: v.get(kk) for kk in ("stato", "etichetta_sensore", "file")} for k, v in S["registri"].items() if k in usati}

    T = {l: carica(os.path.join(R, "testi", f"schermo_{l}.json")) for l in ("en", "it")}
    psub = os.path.join(R, "assets", "data", "sottotitoli.js")
    if not os.path.exists(psub):
        scrivi(psub, "window.__SUB = {en: null, it: null, stimati: false};\n")

    if a.finale:
        guai = [f"registro {k} in stato «sviluppo»" for k, v in reg.items() if v["stato"] == "sviluppo"]
        for l, d in T.items():
            for k, v in d.items():
                if not k.startswith("_") and SEGNAPOSTO.search(json.dumps(v, ensure_ascii=False)):
                    guai.append(f"testo {l}:{k} con segnaposto")
        sub = open(psub, encoding="utf-8").read()
        if SEGNAPOSTO.search(sub):
            guai.append("sottotitoli con segnaposto")
        if "stimati: true" in sub or '"stimati": true' in sub:
            guai.append("sottotitoli con tempi stimati")
        if guai:
            print("MONTAGGIO FINALE RIFIUTATO:\n  " + "\n  ".join(guai), file=sys.stderr)
            return 2

    scrivi(os.path.join(R, "tempi", "scene_tempi.js"),
           "window.__SCENE = " + json.dumps({"fps": S["fps"], "durata": D, "registri": reg, "scene": scene}, ensure_ascii=False) + ";\n")
    scrivi(os.path.join(R, "testi", "testi.js"),
           "window.__TESTI = " + json.dumps(T, ensure_ascii=False) + ";\nwindow.__LINGUA = " + json.dumps(lingua) + ";\n")
    wm = open(os.path.join(R, "assets", "marchio", "movi_wordmark.svg"), "rb").read()
    scrivi(os.path.join(R, "assets", "marchio", "marchio.js"),
           "window.__MARCHIO = " + json.dumps({"wordmark": "data:image/svg+xml;base64," + base64.b64encode(wm).decode()}) + ";\n")

    dati = "".join(f'<script src="assets/data/{k}.js"></script>\n' for k in sorted(usati)
                   if os.path.exists(os.path.join(R, "assets", "data", f"{k}.js")))
    marcatori = "".join(f'  <div id="scena_{sc["id"]}" class="clip" data-start="{sc["inizio"]}" data-duration="{sc["durata"]}"></div>\n' for sc in scene)
    html = f"""<!doctype html>
<!-- GENERATO da strumenti/monta.py il {time.strftime('%Y-%m-%dT%H:%M:%S')}: non modificare a mano. Lingua: {lingua}. Durata: {D} s. -->
<html lang="{lingua}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=1920, height=1080">
<title>MoVi</title>
<style>
  @font-face {{ font-family: "InterLocale"; src: url("assets/fonts/InterVariable.woff2") format("woff2"); font-weight: 100 900; }}
  @font-face {{ font-family: "JBMonoLocale"; src: url("assets/fonts/JetBrainsMono-Regular.woff2") format("woff2"); font-weight: 400; }}
  @font-face {{ font-family: "JBMonoLocale"; src: url("assets/fonts/JetBrainsMono-Bold.woff2") format("woff2"); font-weight: 700; }}
  html, body {{ margin: 0; padding: 0; background: #0B0F17; width: 1920px; height: 1080px; overflow: hidden; }}
  #tela svg {{ display: block; }}
</style>
<script src="assets/vendor/gsap.min.js"></script>
<script src="tempi/scene_tempi.js"></script>
<script src="testi/testi.js"></script>
<script src="assets/marchio/marchio.js"></script>
{dati}<script src="assets/data/sottotitoli.js"></script>
<script src="assets/js/componenti.js"></script>
<script src="assets/js/motore.js"></script>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1920" data-height="1080" data-fps="{S['fps']}">
  <div id="tela" class="clip" data-start="0" data-duration="{D}"><svg id="svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080"></svg></div>
{marcatori}</div>
<script>
  window.__timelines = window.__timelines || {{}};
  const tl = gsap.timeline({{ paused: true }});
  const svg = document.getElementById("svg"), orologio = {{ t: 0 }};
  function disegna(t) {{ svg.innerHTML = window.MoViMotore.disegna(Math.min(t, {D} - 1e-4)); }}
  tl.to(orologio, {{ t: {D}, duration: {D}, ease: "none", onUpdate: () => disegna(orologio.t) }}, 0);
  disegna(0);
  window.__timelines["main"] = tl;
</script>
</body>
</html>
"""
    pi = os.path.join(R, "index.html")
    if os.path.exists(pi):
        os.makedirs(os.path.join(R, "versioni"), exist_ok=True)
        shutil.copy2(pi, os.path.join(R, "versioni", f"index.{time.strftime('%Y%m%d-%H%M%S')}.html"))
    scrivi(pi, html)
    print(f"index.html: {len(scene)} scene, {D} s, lingua {lingua}, registri {sorted(usati)}")
    for sc in scene:
        print(f"  {sc['n']}  {sc['inizio']:7.2f}–{sc['inizio'] + sc['durata']:7.2f}  {sc['durata']:5.2f} s  {sc['tipo']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
