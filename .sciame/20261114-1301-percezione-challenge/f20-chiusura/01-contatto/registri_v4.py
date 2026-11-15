"""registri_v4.py - registro per fotogramma di F3 col nucleo v4 e la regola di contatto v4c, nella cartella data, con
suffisso _v4 (i registri della fase 3 restano). Stesso passaggio dei registri della fase 3: idx 0, configurazione sda
(idx 0 e' un seme di SVILUPPO: il registro e' illustrativo, non una misura). Senza sovrascrivere: se il file esiste, esce.
Uso: python -I -B registri_v4.py CARTELLA [F3 ...]"""
import json
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("VOLO_REGOLA", "v4c")
import prove_volo_v4 as P  # noqa: E402

cart = sys.argv[1]
for e in (sys.argv[2:] or ["F3"]):
    dst = os.path.join(cart, "registro_%s_v4.jsonl" % e)
    if os.path.exists(dst):
        print("esiste, non sovrascrivo:", dst)
        continue
    R, reg = P.passaggio_volo(e, "sda", 0, 3.0 if e == "F5" else None, registro=True)
    with open(dst, "x", encoding="utf-8") as f:
        f.write(json.dumps({"intestazione": {"scenario": e, "nome": P.SCV[e]["nome"], "configurazione": "sda (stato dell'arte, latenze STIMATE)",
                                             "nucleo": "v4 (= v3i, inviluppo 210 m/s) + regola di contatto v4c, f20-chiusura/01-contatto/prove_volo_v4.py",
                                             "seme": "SeedSequence(20261119, spawn_key=(%d, 0|2, 0))" % (200 + int(e[1])), "idx": 0,
                                             "stato": "simulato; nessun sensore fisico; etichette a mano; Doppler simulato (ipotesi sigma 0,5 m/s); idx 0 = seme di sviluppo",
                                             "riassunto": {k: R[k] for k in ("evento", "ritardo_evento_s", "falso_evento", "avviso_prossimita", "innesco_v4c",
                                                                             "t_primo_frammento_a_terra", "affidabilita_persa", "salute_cicli") if k in R}}},
                           ensure_ascii=False, default=float) + "\n")
        for riga in reg:
            f.write(json.dumps(riga, ensure_ascii=False, default=float) + "\n")
    print(e, len(reg), "fotogrammi", R.get("ritardo_evento_s"), R.get("innesco_v4c"))
