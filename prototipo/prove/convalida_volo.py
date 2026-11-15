#!/usr/bin/env python3
"""Convalida dei registri per fotogramma degli scenari di volo F1-F6 (uscite/video_volo/registro_F*.jsonl), scritti da
.sciame/.../f19-volo/10-prove/prove_volo.py --registro. Opzione NUOVA accanto a `movi.sh convalida` (che non cambia).

Uso:  python -I -B prove/convalida_volo.py uscite/video_volo/registro_F3.jsonl [altri ...]
Controlla, per ogni riga: (1) campi obbligatori (t, tracce, evento, affidabilita_sensori, verita); (2) confidenza C in
[0, 1] e r99, insieme di presenza >= 0; (3) mai 'vista' con non_vista_da_s oltre la soglia di perdita dichiarata nella
parola; (4) durante una perdita della stessa traccia C non cresce (la confidenza si perde, non si inventa) a meno di
1e-3 (errore di quadratura); (5) un evento aperto resta aperto (nessun «libero» implicito: la parola dei detriti non
sparisce finche' l'impronta non e' tutta ispezionata); (6) un sensore con affidabilita' persa non torna affidabile.
Esce con 3 se una riga viola una regola. Stato: controllo di forma e di principio; non dice nulla sulla verita'."""
import json
import sys

OBBL = ("t", "tracce", "evento", "affidabilita_sensori", "verita")


def convalida(percorso):
    err, n = [], 0
    ultimaC, evento_aperto, persi = {}, None, set()
    with open(percorso, encoding="utf-8") as f:
        testa = json.loads(f.readline())
        if "intestazione" not in testa:
            err.append("manca l'intestazione")
        for riga in f:
            n += 1
            r = json.loads(riga)
            for k in OBBL:
                if k not in r:
                    err.append("t=%s: manca %s" % (r.get("t"), k))
            for tr in r.get("tracce", []):
                C = tr.get("confidenza_C")
                if C is not None and not (0.0 <= C <= 1.0):
                    err.append("t=%s traccia %s: C fuori da [0,1]" % (r["t"], tr["id"]))
                if tr.get("r99_m", 0) < 0 or tr.get("insieme_presenza_r_m", 0) < 0:
                    err.append("t=%s traccia %s: raggio negativo" % (r["t"], tr["id"]))
                vista = tr["parola"] == "vista"
                if not vista and C is not None:
                    prec = ultimaC.get(tr["id"])
                    if prec is not None and prec[0] < tr["non_vista_da_s"] and C > prec[1] + 1e-3:
                        err.append("t=%s traccia %s: C cresce durante la perdita (%.4f -> %.4f)" % (r["t"], tr["id"], prec[1], C))
                    ultimaC[tr["id"]] = (tr["non_vista_da_s"], C)
                else:
                    ultimaC.pop(tr["id"], None)
            ev = r.get("evento")
            if evento_aperto is not None and ev is None:
                err.append("t=%s: l'evento aperto a %s e' sparito" % (r["t"], evento_aperto))
            if ev is not None:
                evento_aperto = ev["t_dichiarato"]
                isp = ev["impronta"]["ispezionati"]
                if isp[0] < isp[1] and "non verificata" not in ev["parola"]:
                    err.append("t=%s: impronta non tutta ispezionata ma la parola non dice 'non verificata'" % r["t"])
            for s, st in r.get("affidabilita_sensori", {}).items():
                if s in persi and st == "affidabile":
                    err.append("t=%s: %s torna affidabile senza ripristino dichiarato" % (r["t"], s))
                if st != "affidabile":
                    persi.add(s)
    return n, err


def main(argv):
    cattivo = False
    for p in argv[1:]:
        n, err = convalida(p)
        print("%s: %d fotogrammi, %d violazioni" % (p, n, len(err)))
        for e in err[:10]:
            print("  ", e)
        cattivo |= bool(err)
    return 3 if cattivo else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
