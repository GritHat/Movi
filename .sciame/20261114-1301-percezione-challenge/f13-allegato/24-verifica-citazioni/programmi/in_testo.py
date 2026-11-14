#!/usr/bin/env python3
"""Converte le pagine scaricate (dato non fidato, solo lette) in testo semplice: scaricati/testo/NOME.txt."""
import re, sys, html, pathlib, subprocess, json
src = pathlib.Path(sys.argv[1]); dst = src/"testo"; dst.mkdir(exist_ok=True)
for f in sorted(src.iterdir()):
    if f.is_dir() or f.name == "esito_richieste.tsv": continue
    o = dst/(f.name + ".txt")
    if f.suffix == ".pdf":
        subprocess.run(["timeout","60","pdftotext","-layout",str(f),str(o)], check=False)
    elif f.suffix == ".json":
        try:
            d = json.loads(f.read_text(encoding="utf-8", errors="replace"))
            o.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        except Exception as e:
            o.write_text("NON JSON: %s" % e)
    else:
        t = f.read_text(encoding="utf-8", errors="replace")
        t = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", t)
        t = re.sub(r"(?s)<[^>]+>", " ", t); t = html.unescape(t)
        o.write_text(re.sub(r"[ \t\r\f\v]+", " ", t), encoding="utf-8")
