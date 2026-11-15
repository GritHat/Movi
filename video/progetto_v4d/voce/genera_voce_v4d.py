# Genera un wav per ogni clip di clip.json con Kokoro (im_nicola, it, velocità 1.0), in locale. Non sovrascrive i wav esistenti.
# Uso: python3 genera_voce_v4d.py [id ...]   (senza argomenti: tutte le clip che mancano)
import json, os, subprocess, sys
q = os.path.dirname(os.path.abspath(__file__))
V = os.path.normpath(os.path.join(q, "..", "..", "..", ".sciame", "20261114-1301-percezione-challenge", "f17-video", "00-strumenti", "voce"))
PY = os.path.join(V, "venv-kokoro", "bin", "python")
PRON = {"MoVi": "Movi", "SDMs": "esse di emme esse", "«": "", "»": "", "’": "'"}
solo = set(sys.argv[1:])
for cid, _, testo in json.load(open(os.path.join(q, "clip.json"))):
    if solo and cid not in solo: continue
    t = testo
    for a, b in PRON.items(): t = t.replace(a, b)
    v1 = os.path.join(q, cid + "_kokoro.txt")
    base = cid if (not os.path.exists(v1) or open(v1).read() == t + "\n") else cid + "_v2"
    wav = os.path.join(q, base + ".wav")
    if os.path.exists(wav): continue
    txt = os.path.join(q, base + "_kokoro.txt"); open(txt, "w").write(t + "\n")
    subprocess.run([PY, os.path.join(V, "script", "kokoro_tts.py"), "--testo", txt, "--voce", "im_nicola", "--lingua", "it",
                    "--velocita", "1.0", "--pausa-frase", "0.05", "--pausa-paragrafo", "0.3", "--uscita", wav],
                   check=True, timeout=120, stdout=subprocess.DEVNULL)
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", wav], capture_output=True, text=True).stdout)
    print(cid, round(d, 2), flush=True)
