#!/usr/bin/env python3
"""Utilità della voce guida di MoVi (usate da genera_voce.sh).

  compila <lingua> <modello.txt> <cifre.json> <detto.txt> <kokoro.txt>
      Sostituisce {{CHIAVE}} con cifre[CHIAVE].voce_<l> (se stato in sostenuto/verificato/limite e non null),
      altrimenti con voce_senza_<l> (stringa vuota = frase tolta). Scrive il testo DETTO (sottotitoli) e il testo
      per KOKORO (con le sostituzioni di pronuncia). Si ferma se restano segnaposto o termini vietati.
  tempi <tempi_kokoro.json> <detto.txt> <uscita.json>
      Riporta il testo di ogni frase alla grafia vera (stesse frasi, stesso ordine) e aggiunge il paragrafo (scena).
  scene <wav> <tempi.json> <cartella> <prefisso> <piano_durate_csv>
      Taglia un WAV per scena (dalla prima all'ultima frase, più 0,15 s), stampa la tabella delle scene e la durata
      complessiva del montaggio con la regola di rimonta.py: max(piano, 0,4 + voce + 0,6).
"""
import json, re, subprocess, sys

USA = ("sostenuto", "verificato", "limite")
VIETATI = ["free", "clear", "predicted", "prediction", "gone", "probable", "target", "threat", "engage", "intercept",
           "lock", "hostile", "test range", "validated", "certified", "compliant", "guaranteed", "detect and avoid",
           "real-time", "real time", "counter-drone", "military"]


def paragrafi(testo):
    blocchi = [b.strip() for b in re.split(r"\n\s*\n", testo) if b.strip()]
    return [[f for f in re.split(r"(?<=[.!?…])\s+", " ".join(b.split())) if f] for b in blocchi
            if not re.fullmatch(r"\[pausa\s+([0-9.]+)\]", b)]


def compila(l, modello, cifre, detto, kokoro):
    C = json.load(open(cifre, encoding="utf-8"))
    cf, pr = C["cifre"], C.get("pronuncia", {}).get(l, {})
    usate = []

    def f(m):
        k = m.group(1)
        c = cf.get(k)
        if c is None:
            sys.exit(f"cifra sconosciuta: {k}")
        if c.get("stato") in USA and c.get(f"voce_{l}"):
            usate.append(k)
            return c[f"voce_{l}"]
        return c.get(f"voce_senza_{l}") or ""

    t = re.sub(r"\{\{([^}]+)\}\}", f, open(modello, encoding="utf-8").read())
    t = "\n".join(re.sub(r"[ \t]+", " ", r).strip() for r in t.split("\n")) + "\n"
    if re.search(r"\[(CIFRA|STATO|k\]|n\]|DA FORNIRE)|\{\{", t):
        sys.exit("segnaposto rimasti nel testo")
    if l == "en":
        bassa = t.lower()
        trovati = [v for v in VIETATI if re.search(r"\b" + re.escape(v) + r"\b", bassa)]
        if trovati:
            sys.exit(f"termini vietati: {trovati}")
    open(detto, "w", encoding="utf-8").write(t)
    k = t
    for a, b in pr.items():
        if a.startswith("_"):
            continue
        k = re.sub(r"\b" + re.escape(a) + r"\b", b, k)
    open(kokoro, "w", encoding="utf-8").write(k)
    pd, pk = paragrafi(t), paragrafi(k)
    assert [len(p) for p in pd] == [len(p) for p in pk], "la pronuncia ha cambiato le frasi"
    parole = len(re.findall(r"\S+", t))
    print(json.dumps({"lingua": l, "parole": parole, "scene": len(pd), "parole_per_scena": [len(" ".join(p).split()) for p in pd],
                      "cifre_usate": usate}, ensure_ascii=False))


def tempi(tk, detto, uscita):
    T = json.load(open(tk, encoding="utf-8"))
    frasi = [(i, f) for i, p in enumerate(paragrafi(open(detto, encoding="utf-8").read())) for f in p]
    assert len(frasi) == len(T), f"{len(frasi)} frasi contro {len(T)} tempi"
    for (i, f), x in zip(frasi, T):
        x["testo"], x["scena"] = f, i + 1
    json.dump(T, open(uscita, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def scene(wav, tj, cartella, pref, piano):
    T = json.load(open(tj, encoding="utf-8"))
    P = [float(x) for x in piano.split(",")]
    tot, righe = 0.0, []
    for s in sorted({x["scena"] for x in T}):
        fr = [x for x in T if x["scena"] == s]
        a, b = max(0.0, fr[0]["inizio"] - 0.15), fr[-1]["fine"] + 0.15
        out = f"{cartella}/{pref}_scena{s}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-af", f"atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS",
                        "-c:a", "pcm_s16le", out], check=True)
        voce = fr[-1]["fine"] - fr[0]["inizio"]
        pl = P[s - 1] if s - 1 < len(P) else 0
        d = max(pl, 0.4 + voce + 0.6)
        tot += d
        par = sum(len(x["testo"].split()) for x in fr)
        righe.append((s, pl, voce, d, par, par / voce * 60))
    print("scena | piano s | voce s | scena s | parole | parole/min")
    for r in righe:
        print("%d | %.1f | %.2f | %.2f | %d | %.0f%s" % (*r, "  <-- sfora il piano" if r[3] > r[1] + 1e-6 else ""))
    print("TOTALE montaggio (max(piano, 0,4+voce+0,6)): %.2f s" % tot)


if __name__ == "__main__":
    c, *a = sys.argv[1:]
    {"compila": compila, "tempi": tempi, "scene": scene}[c](*a)
