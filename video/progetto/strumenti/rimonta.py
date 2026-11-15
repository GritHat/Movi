#!/usr/bin/env python3
"""RIMONTA i tempi delle scene sulla voce e genera i sottotitoli .srt in inglese e in italiano.

Ingressi
  --voce-en  WAV di kokoro_tts.py (bm_george) con accanto <WAV>.tempi.json  [inizio, fine, testo per frase]
  --voce-it  facoltativo, WAV di im_nicola con il suo .tempi.json
  --testo-en / --testo-it  i testi dati a Kokoro (un paragrafo per scena, righe vuote fra i paragrafi; i paragrafi
             «[pausa X]» non hanno frasi). Default: f17-video/22-sintesi/voce_{en,it}_v2.txt
  --stima    senza WAV: tempi STIMATI (129 parole/min EN, 135 IT, pause 0,35/0,8 s come lo script). Serve solo per
             l'animatic: i sottotitoli escono marcati «stimati» e monta.py --finale li rifiuta.
  --guida en|it  la lingua che decide le durate delle scene (default en)
  --anticipo 0.4 --coda 0.6   s fra l'inizio della scena e la voce; s di respiro dopo l'ultima frase del paragrafo

Che cosa fa
  1. Divide i testi in paragrafi e frasi con LA STESSA regola di kokoro_tts.py e associa ogni voce di .tempi.json alla
     sua frase (controlla che i testi coincidano; se no si ferma).
  2. Scena k = paragrafo k. Durata = max(durata del piano, anticipo + durata del paragrafo + coda). Nessuna voce
     si accelera; se la somma esce da 165–175 s lo dice (Q1).
  3. Allunga l'ultimo segmento di registro della scena se la scena si allunga, e controlla che i registri
     (scene/scene.json -> registri) coprano la finestra; altrimenti avvisa «ultimo stato tenuto».
  4. Scrive tempi/scene_tempi.json, sottotitoli/movi_{en,it}.srt (≤ 2 righe da 42 caratteri), assets/data/sottotitoli.js
     e, con il WAV, tempi/voce_montata_{en,it}.wav: ogni paragrafo spostato all'inizio della sua scena (ffmpeg).
  5. Rilancia registri_a_js.py e monta.py.
  Le versioni precedenti dei file scritti si copiano in versioni/ prima di riscriverli (nessun file si cancella).

Uso:  python3 -I strumenti/rimonta.py --voce-en …/voce_en.wav [--voce-it …/voce_it.wav]
      python3 -I strumenti/rimonta.py --stima
"""
import argparse, json, os, re, shutil, subprocess, sys, time

QUI = os.path.dirname(os.path.abspath(__file__))
R = os.path.dirname(QUI)
SINTESI = os.path.normpath(os.path.join(R, "..", "..", ".sciame", "20261114-1301-percezione-challenge", "f17-video", "22-sintesi"))
WPM = {"en": 129.0, "it": 135.0}
P_FRASE, P_PAR, BORDO = 0.35, 0.8, 0.15


def paragrafi(p):
    blocchi = [b.strip() for b in re.split(r"\n\s*\n", open(p, encoding="utf-8").read()) if b.strip()]
    out = []
    for b in blocchi:
        if re.fullmatch(r"\[pausa\s+([0-9.]+)\]", b):
            continue
        out.append([f for f in re.split(r"(?<=[.!?…])\s+", " ".join(b.split())) if f])
    return out


def tempi_stimati(par, lingua):
    t, out = BORDO, []
    for k, frasi in enumerate(par):
        for i, f in enumerate(frasi):
            if out:
                t += P_PAR if i == 0 else P_FRASE
            d = len(f.split()) * 60.0 / WPM[lingua]
            out.append({"inizio": round(t, 3), "fine": round(t + d, 3), "testo": f, "par": k})
            t += d
    return out


def tempi_veri(par, wav):
    T = json.load(open(wav + ".tempi.json", encoding="utf-8"))
    frasi = [(k, f) for k, fr in enumerate(par) for f in fr]
    if len(frasi) != len(T):
        sys.exit(f"{wav}: {len(T)} frasi nel .tempi.json, {len(frasi)} nel testo: il testo non è quello dato a Kokoro")
    for (k, f), x in zip(frasi, T):
        if " ".join(f.split()) != " ".join(x["testo"].split()):
            sys.exit(f"{wav}: frase diversa:\n  testo: {f}\n  voce:  {x['testo']}")
        x["par"] = k
    return T


def finestre(T, n):
    w = []
    for k in range(n):
        q = [x for x in T if x["par"] == k]
        w.append((q[0]["inizio"], q[-1]["fine"]) if q else None)
    return w


def spezza_cue(testo, a, b, maxc=42):
    """Una frase -> uno o più cue da al più 2 righe di maxc caratteri; il tempo si divide per numero di caratteri."""
    parole, righe, cur = testo.split(), [], ""
    for p in parole:
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


def conserva(p):
    if os.path.exists(p):
        d = os.path.join(R, "versioni"); os.makedirs(d, exist_ok=True)
        shutil.copy2(p, os.path.join(d, f"{os.path.basename(p)}.{time.strftime('%Y%m%d-%H%M%S')}"))


def scrivi(p, s):
    conserva(p)
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voce-en"); ap.add_argument("--voce-it")
    ap.add_argument("--testo-en", default=os.path.join(SINTESI, "voce_en_v2.txt"))
    ap.add_argument("--testo-it", default=os.path.join(SINTESI, "voce_it_v2.txt"))
    ap.add_argument("--stima", action="store_true")
    ap.add_argument("--guida", default="en", choices=("en", "it"))
    ap.add_argument("--anticipo", type=float, default=0.4)
    ap.add_argument("--coda", type=float, default=0.6)
    a = ap.parse_args()
    if not a.stima and not a.voce_en:
        sys.exit("serve --voce-en (o --stima)")
    S = json.load(open(os.path.join(R, "scene", "scene.json"), encoding="utf-8"))
    n = len(S["scene"])
    par = {"en": paragrafi(a.testo_en), "it": paragrafi(a.testo_it)}
    for l in par:
        if len(par[l]) != n:
            sys.exit(f"testo {l}: {len(par[l])} paragrafi, {n} scene")
    T, stimati = {}, {}
    for l in ("en", "it"):
        wav = getattr(a, f"voce_{l}")
        if wav and not a.stima:
            T[l], stimati[l] = tempi_veri(par[l], wav), False
        else:
            T[l], stimati[l] = tempi_stimati(par[l], l), True
    W = {l: finestre(T[l], n) for l in T}

    # durate: la lingua guida decide; l'altra si controlla
    nuove, t, avvisi = [], 0.0, []
    for k, sc in enumerate(S["scene"]):
        w = W[a.guida][k]
        serve = a.anticipo + (w[1] - w[0]) + a.coda if w else 0
        d = round(max(sc["durata"], serve), 3)
        altra = "it" if a.guida == "en" else "en"
        wa = W[altra][k]
        if wa and a.anticipo + (wa[1] - wa[0]) + a.coda > d + 1e-6:
            avvisi.append(f"scena {sc['n']}: la voce {altra} ({wa[1] - wa[0]:.2f} s) non entra in {d:.2f} s: applicare i tagli del piano §2")
        segs = [dict(g) for g in sc.get("segmenti") or []]
        if segs and d > sc["durata"]:
            segs[-1]["a"] = round(segs[-1]["a"] + d - sc["durata"], 3)
        nuove.append({"id": sc["id"], "n": sc["n"], "inizio": round(t, 3), "durata": d, "segmenti": segs or None,
                      "voce": {l: (None if not W[l][k] else {"da": W[l][k][0], "a": W[l][k][1]}) for l in W}})
        t += d
    tot = round(t, 3)
    if not (165.0 <= tot <= 175.0):
        avvisi.append(f"durata totale {tot} s fuori da 165–175 s (Q1)")

    # copertura dei registri
    for sc in nuove:
        for g in sc["segmenti"] or []:
            m = S["registri"][g["registro"]]
            p = os.path.normpath(os.path.join(R, m["file"]))
            if not os.path.exists(p):
                avvisi.append(f"scena {sc['n']}: registro {g['registro']} mancante ({m['file']})"); continue
            ultimo = None
            with open(p, encoding="utf-8") as f:
                for riga in f:
                    if '"fotogramma"' in riga[:40]:
                        ultimo = json.loads(riga)["t"]
            serve = g["t_reg"] + (g["a"] - g["da"]) * g["velocita"]
            if ultimo is not None and serve > ultimo + 1e-6:
                avvisi.append(f"scena {sc['n']}: {g['registro']} finisce a {ultimo:.2f} s, servono {serve:.2f} s: ultimo stato tenuto")
            if m.get("stato") == "sviluppo":
                avvisi.append(f"scena {sc['n']}: {g['registro']} è un registro DI SVILUPPO (non per il video finale)")

    # sottotitoli: ogni frase spostata all'inizio della sua scena + anticipo
    SUB = {}
    for l in ("en", "it"):
        cues = []
        for k, sc in enumerate(nuove):
            w = W[l][k]
            if not w:
                continue
            base = sc["inizio"] + a.anticipo - w[0]
            for x in [x for x in T[l] if x["par"] == k]:
                cues += spezza_cue(x["testo"], x["inizio"] + base, x["fine"] + base)
        SUB[l] = cues
        os.makedirs(os.path.join(R, "sottotitoli"), exist_ok=True)
        suff = "_STIMATI" if stimati[l] else ""
        scrivi(os.path.join(R, "sottotitoli", f"movi_{l}{suff}.srt"), srt(cues))
    est = any(stimati.values())
    scrivi(os.path.join(R, "assets", "data", "sottotitoli.js"),
           "window.__SUB = " + json.dumps({"en": SUB["en"], "it": SUB["it"], "stimati": est,
                                            "fonte": {l: ("stima" if stimati[l] else getattr(a, f"voce_{l}")) for l in stimati}},
                                           ensure_ascii=False) + ";\n")
    scrivi(os.path.join(R, "tempi", "scene_tempi.json"),
           json.dumps({"generato": time.strftime("%Y-%m-%dT%H:%M:%S"), "stimati": est, "guida": a.guida, "anticipo": a.anticipo,
                       "durata": tot, "scene": nuove, "avvisi": avvisi}, ensure_ascii=False, indent=1))

    # voce montata (solo con i WAV veri): un atrim+adelay per paragrafo, poi amix
    for l in ("en", "it"):
        wav = getattr(a, f"voce_{l}")
        if not wav or a.stima:
            continue
        rami, k_ = [], 0
        for k, sc in enumerate(nuove):
            w = W[l][k]
            if not w:
                continue
            da, aa = max(0.0, w[0] - 0.05), w[1] + 0.1
            ms = int(round((sc["inizio"] + a.anticipo - (w[0] - da)) * 1000))
            rami.append(f"[0:a]atrim={da:.3f}:{aa:.3f},asetpts=PTS-STARTPTS,adelay={ms}:all=1[p{k_}]"); k_ += 1
        filtro = ";".join(rami) + ";" + "".join(f"[p{i}]" for i in range(k_)) + f"amix=inputs={k_}:normalize=0:duration=longest,apad,atrim=0:{tot}[v]"
        out = os.path.join(R, "tempi", f"voce_montata_{l}.wav")
        conserva(out)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-filter_complex", filtro, "-map", "[v]", "-ar", "48000",
                        "-c:a", "pcm_s16le", out], check=True, timeout=300)
        print(f"voce montata {l}: {out}")

    print(f"durata {tot} s ({'STIMATA' if est else 'dalla voce'}); scene:")
    for sc in nuove:
        print(f"  {sc['n']}  {sc['inizio']:7.2f}  {sc['durata']:6.2f} s")
    for x in avvisi:
        print("AVVISO:", x)
    for cmd in (["registri_a_js.py"], ["monta.py"]):
        subprocess.run([sys.executable, "-I", os.path.join(QUI, cmd[0])], check=True, timeout=300)
    return 0


if __name__ == "__main__":
    sys.exit(main())
