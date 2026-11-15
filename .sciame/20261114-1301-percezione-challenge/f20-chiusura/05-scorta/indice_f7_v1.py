"""indice_f7.py - scrive INDICE_F7.md accanto ai registri F7 (file nuovo, modo 'x'). Uso: python -I -B indice_f7.py DIR"""
import json
import os
import sys

d = sys.argv[1]
righe = ["# Registri per fotogramma dello scenario F7 «scorta» (per il video)", "",
         "Stato: **simulato** (nessun sensore fisico, etichette a mano, sensori da ipotesi dichiarate). Configurazione «sda», "
         "passaggio idx 0 dei semi di valutazione 20261121. Scritti da `.sciame/20261114-1301-percezione-challenge/f20-chiusura/"
         "05-scorta/scorta_f7.py --registro`. Rapporto: `f20-chiusura/05-scorta/SCORTA.md`. Solo osservazione e avviso: "
         "«seguire» vuol dire mantenere la traccia. Campi nuovi: `tracce[].ruolo`, `identita`, `r90_m`; `evento.volume`; "
         "`avviso_portatore`; `posa_stimata` (navigazione inerziale con rumore e deriva). `verita` serve solo al montaggio.",
         "Convalida: `python -I -B prototipo/prove/convalida_volo.py prototipo/uscite/video_volo/registro_F7_*.jsonl`.", ""]
for v in ("lato", "davanti", "dietro", "vira", "F7c"):
    p = os.path.join(d, "registro_F7_%s.jsonl" % v)
    with open(p, encoding="utf-8") as f:
        h = json.loads(f.readline())["intestazione"]
        n = sum(1 for _ in f)
    righe.append("- `registro_F7_%s.jsonl` (%d fotogrammi): %s" % (v, n, json.dumps(h["riassunto"], ensure_ascii=False)))
with open(os.path.join(d, "INDICE_F7.md"), "x", encoding="utf-8") as f:
    f.write("\n".join(righe) + "\n")
print("\n".join(righe))
