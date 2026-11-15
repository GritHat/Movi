#!/usr/bin/env python3
"""MoVi video v3 FINALE: scrive index.html (HyperFrames). Prima copia l'index.html esistente in versioni/ (nome con l'ora).
Uso (da progetto_v3): python3 -I strumenti/monta_finale.py tempi/scene_finale_<l>.js [lingua]"""
import json, sys, datetime, os, shutil
tj = sys.argv[1]; lang = sys.argv[2] if len(sys.argv) > 2 else "en"
tot = json.load(open(tj.replace(".js", ".json")))["totale"]
ora = datetime.datetime.now()
if os.path.exists("index.html"):
    dst = f"versioni/index.{ora.strftime('%Y%m%d-%H%M%S')}.html"
    if not os.path.exists(dst): shutil.copy2("index.html", dst)
html = f"""<!doctype html>
<!-- GENERATO da strumenti/monta_finale.py il {ora.isoformat(timespec='seconds')}: non modificare a mano. Video v3c ({lang}), da strumenti/monta_v3c.py. Durata: {tot} s. -->
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=1920, height=1080">
<title>MoVi v3c</title>
<style>
  @font-face {{ font-family: "InterLocale"; src: url("assets/fonts/InterVariable.woff2") format("woff2"); font-weight: 100 900; }}
  @font-face {{ font-family: "JBMonoLocale"; src: url("assets/fonts/JetBrainsMono-Regular.woff2") format("woff2"); font-weight: 400; }}
  @font-face {{ font-family: "JBMonoLocale"; src: url("assets/fonts/JetBrainsMono-Bold.woff2") format("woff2"); font-weight: 700; }}
  html, body {{ margin: 0; padding: 0; background: #0B0F17; width: 1920px; height: 1080px; overflow: hidden; }}
  #tela svg {{ display: block; }}
</style>
<script src="assets/vendor/gsap.min.js"></script>
<script src="assets/marchio/marchio.js"></script>
<script src="assets/data/cifre_v3c.js"></script>
<script src="assets/data/volo_v3c.js"></script>
<script src="{tj}"></script>
<script src="assets/js/motore_v3c.js"></script>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{tot}" data-width="1920" data-height="1080" data-fps="30">
  <div id="tela" class="clip" data-start="0" data-duration="{tot}"><svg id="svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080"></svg></div>
</div>
<script>
  window.__timelines = window.__timelines || {{}};
  const tl = gsap.timeline({{ paused: true }});
  const svg = document.getElementById("svg"), orologio = {{ t: 0 }};
  function disegna(t) {{ svg.innerHTML = window.MoViMotore.disegna(Math.min(t, {tot} - 1e-4)); }}
  tl.to(orologio, {{ t: {tot}, duration: {tot}, ease: "none", onUpdate: () => disegna(orologio.t) }}, 0);
  disegna(0);
  window.__timelines["main"] = tl;
</script>
</body>
</html>
"""
open("index.html", "w", encoding="utf-8").write(html)
print("index.html", tot, "s")
