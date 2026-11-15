#!/usr/bin/env python3
"""v9 (montaggio finale, 2026-11-15): scene/scene_v9.json, registri veri _v3, testi v9, JS v9, sottotitoli della lingua principale
dai tempi della SUA voce (l'altra lingua distribuita sulle finestre della principale), uscite *_v9, --finale che rifiuta
anche «DEV DATA» e i registri di sviluppo. Uso: python3 -I strumenti/monta_v9.py --lingua en|it --voce V.wav --voce-altra W.wav [--finale]
Prima: v8 = v7 con i JS v8 (revisione del regista). v7 (animatic con voce): come monta_v6.py, ma legge scene/scene_v7.json (durate già sulla voce, NON tempi/scene_tempi.json),
applica cifre.json -> righe_schermo (null = riga tolta, chiave = testo della cifra) e i valori «@CHIAVE» dei testi v7,
scrive i sottotitoli EN e IT dai tempi della voce guida (sottotitoli/movi_{en,it}_v7.srt, assets/data/sottotitoli.js) e
usa componenti_v7.js e motore_v7.js. Uso: python3 -I strumenti/monta_v7.py --voce video/voce/voce_guida_en_v4.wav [--lingua en]

Monta il progetto HyperFrames: dai file di scena, dei tempi, dei testi e del marchio scrive
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


def spezza_cue(testo, a, b, maxc=42):
    """Una frase -> uno o più cue da al più 2 righe di maxc caratteri; il tempo si divide per numero di caratteri."""
    righe, cur = [], ""
    for p in testo.split():
        if len((cur + " " + p).strip()) > maxc:
            righe.append(cur.strip()); cur = p
        else:
            cur += " " + p
    if cur.strip():
        righe.append(cur.strip())
    blocchi = ["\n".join(righe[i:i + 2]) for i in range(0, len(righe), 2)]
    tot = sum(len(x) for x in blocchi) or 1
    out, t = [], a
    for x in blocchi:
        d = (b - a) * len(x) / tot
        out.append({"a": round(t, 3), "b": round(t + d, 3), "testo": x})
        t += d
    return out


def srt(cues):
    def ts(s):
        ms = int(round(s * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s_, ms = divmod(ms, 1000)
        return f"{h:02d}:{m:02d}:{s_:02d},{ms:03d}"
    return "\n".join(f"{i}\n{ts(c['a'])} --> {ts(c['b'])}\n{c['testo']}\n" for i, c in enumerate(cues, 1))


def sottotitoli(voce, voce_altra, lingua, scene):
    """Principale: ogni frase al suo tempo vero, spostata col suo paragrafo (scena.inizio + voce_da - inizio del paragrafo).
    Altra lingua: le sue frasi di ogni scena distribuite sulla finestra della voce principale di quella scena, in
    proporzione alla loro durata nella sua voce (sincronia per paragrafo, non per parola)."""
    altra = "it" if lingua == "en" else "en"
    TE = carica(voce + ".tempi.json")
    TI = carica(voce_altra + ".tempi.json") if voce_altra else []
    out = {lingua: [], altra: []}
    for sc in scene:
        q = [x for x in TE if x["scena"] == sc["n"]]
        if not q: continue
        base = sc["inizio"] + sc.get("voce_da", 0.4) - q[0]["inizio"]
        for x in q:
            out[lingua] += spezza_cue(x["testo"], x["inizio"] + base, x["fine"] + base)
        qi = [x for x in TI if x["scena"] == sc["n"]]
        if qi:
            a0, a1 = q[0]["inizio"] + base, q[-1]["fine"] + base
            i0, i1 = qi[0]["inizio"], qi[-1]["fine"]
            k = (a1 - a0) / (i1 - i0)
            for x in qi:
                out[altra] += spezza_cue(x["testo"], a0 + (x["inizio"] - i0) * k, a0 + (x["fine"] - i0) * k)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lingua", default=None)
    ap.add_argument("--finale", action="store_true")
    ap.add_argument("--voce", required=True)
    ap.add_argument("--voce-altra", default=None)
    ap.add_argument("--scene", required=True)
    a = ap.parse_args()
    S = carica(a.scene)
    lingua = a.lingua or S.get("lingua", "en")
    pt = os.path.join(R, "tempi", "NON_USATO_IN_V7.json")
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
    # v6: testi aggiunti per la revisione visiva (file nuovi accanto) e cifre da cifre.json (unica fonte)
    for l in ("en", "it"):
        for vv in ("v6", "v7", "v9", "v10"):
            pe = os.path.join(R, "testi", f"schermo_{l}_{vv}_extra.json")
            if os.path.exists(pe):
                T[l].update({k: v for k, v in carica(pe).items() if not k.startswith("_")})
    CFJ = carica(os.path.join(R, "cifre.json")); CF = CFJ["cifre"]
    AMMESSI = ("sostenuto", "verificato", "limite")
    for l in ("en", "it"):
        for k, v in (CFJ.get("righe_schermo") or {}).items():
            if k.startswith("_"): continue
            if v is None: T[l][k] = None
            else:
                c = CF[v]; assert c.get("stato") in AMMESSI and c.get(l), (k, v, c.get("stato"))
                T[l][k] = c[l]
        for k, v in list(T[l].items()):
            if isinstance(v, str) and v.startswith("@"):
                c = CF[v[1:]]; assert c.get("stato") in AMMESSI and c.get(l), (k, v)
                T[l][k] = c[l]
    def riempi(v, l):
        if isinstance(v, str):
            def f(m):
                c = CF.get(m.group(1))
                if c and c.get("stato") in ("sostenuto", "verificato") and c.get(l):
                    return c[l]
                return m.group(0)
            m0 = re.match(r"^\[(STATO[^\]]*)\]", v)   # una riga che comincia con [STATO-…] è sostituita per intero
            if m0:
                c = CF.get(m0.group(1))
                if c and c.get("stato") in ("sostenuto", "verificato") and c.get(l):
                    return c[l]
            return SEGNAPOSTO.sub(f, v)
        if isinstance(v, list): return [riempi(x, l) for x in v]
        if isinstance(v, dict): return {k: riempi(x, l) for k, x in v.items()}
        return v
    for l in ("en", "it"):
        T[l] = riempi(T[l], l)
    psub = os.path.join(R, "assets", "data", "sottotitoli.js")
    SUB = sottotitoli(a.voce, a.voce_altra, lingua, scene)
    if os.path.exists(psub):
        os.makedirs(os.path.join(R, "versioni"), exist_ok=True)
        shutil.copy2(psub, os.path.join(R, "versioni", f"sottotitoli.js.{time.strftime('%Y%m%d-%H%M%S')}"))
    scrivi(psub, "window.__SUB = " + json.dumps({"en": SUB["en"], "it": SUB["it"], "stimati": False,
                                                  "fonte": {lingua: a.voce, "altra": a.voce_altra}}, ensure_ascii=False) + ";\n")
    for l in ("en", "it"):
        ps = os.path.join(R, "..", "sottotitoli", f"movi_{l}_v10_{lingua}.srt")
        os.makedirs(os.path.dirname(ps), exist_ok=True)
        if os.path.exists(ps):
            shutil.copy2(ps, ps + f".{time.strftime('%Y%m%d-%H%M%S')}")
        scrivi(ps, srt(SUB[l]))
    scrivi(os.path.join(R, "tempi", f"voce_v10_{lingua}.json"), json.dumps({"voce": a.voce, "scene": [
        {"id": sc["id"], "inizio": sc["inizio"], "durata": sc["durata"], "voce_da": sc.get("voce_da", 0.4)} for sc in scene]}, indent=1))

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
        dump = json.dumps(T, ensure_ascii=False) + json.dumps(scene, ensure_ascii=False)
        if "DEV DATA" in dump or "SVILUPPO" in dump:
            guai.append("«DEV DATA» o «SVILUPPO» nei testi o nelle scene")
        for k, v in reg.items():
            if "SVILUPPO" in str(v.get("file")) or "dati_sviluppo" in str(v.get("file")):
                guai.append(f"registro {k} da dati_sviluppo")
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
<script src="assets/js/componenti_v10.js"></script>
<script src="assets/js/motore_v10.js"></script>
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
