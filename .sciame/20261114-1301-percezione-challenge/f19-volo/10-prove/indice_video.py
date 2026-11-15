"""indice_video.py - scrive INDICE.md dei registri per fotogramma di prototipo/uscite/video_volo (che cosa succede, a
quali secondi), leggendo SOLO i registri. Uso: python -I -B indice_video.py <cartella>"""
import json
import os
import sys

NOMI = {"F1": "aereo in avvicinamento e drone non cooperante (quasi collisione a 41 m)",
        "F2": "salita nella cella di pioggia, aereo leggero non cooperante",
        "F3": "collisione fra due droni veloci (40 e 35 m/s): frammenti, caduta",
        "F4": "avaria non contenuta di un aereo a 135 m/s: fiammata, fumo, frammenti",
        "F5": "evento impulsivo: tutti gli ottici ciechi 3 s, resta solo il radar",
        "F6": "controllo: due aerei separati, nessun evento"}


def main(cart):
    out = ["# Registri per fotogramma degli scenari di volo F1-F6 (per il video)", "",
           "Stato: **simulato** (nessun sensore fisico, etichette a mano). Configurazione «sda» (sensori allo stato dell'arte, "
           "latenze dell'elaborazione dedicata STIMATE per analogia, non misurate). Passaggio idx 0, seme dichiarato prima in "
           "f19-volo/10-prove/PREVISIONI.md. Regole degli eventi v3 con l inviluppo di 210 m/s anche nell insieme di presenza del nucleo (configurazione v3i, correzione a posteriori). Un "
           "fotogramma ogni 0,1 s. Campi nuovi per riga: `tracce[].confidenza_C` (probabilità che l'oggetto sia nella porta "
           "di raggio `porta_m` intorno alla previsione), `r99_m`, `insieme_presenza_r_m`, `non_vista_da_s`, `evento` "
           "(tipo, volume V con raggio in pianta e quote, impronta con campioni ispezionati), `affidabilita_sensori`, "
           "`verita` (solo per il montaggio: il sistema non la vede), `avviso_prossimita` [t, tra quanti s, distanza minima prevista].",
           "Convalida: `python -I -B prototipo/prove/convalida_volo.py prototipo/uscite/video_volo/registro_F*.jsonl`.", ""]
    for e in ("F1", "F2", "F3", "F4", "F5", "F6"):
        p = os.path.join(cart, "registro_%s.jsonl" % e)
        if not os.path.exists(p):
            continue
        righe = [json.loads(x) for x in open(p, encoding="utf-8")]
        testa, R = righe[0]["intestazione"], righe[1:]
        out += ["## %s — %s" % (e, NOMI[e]), "", "File: `registro_%s.jsonl` (%d fotogrammi, da %.1f a %.1f s)." % (e, len(R), R[0]["t"], R[-1]["t"]), ""]
        mom = []
        prox = next((r for r in R if r["avviso_prossimita"]), None)
        if prox:
            a = prox["avviso_prossimita"]
            mom.append("%.1f s: avviso di prossimità (distanza minima prevista %.0f m fra %.0f s)" % (prox["t"], a[2], a[1]))
        ev = next((r for r in R if r["evento"]), None)
        if ev:
            x = ev["evento"]
            mom.append("%.1f s: «evento: %s», si apre il volume V e l'impronta (R = %.0f m); «%s»" % (ev["t"], x["tipo"], x["impronta"]["R_m"], x["parola"]))
        persi = {}
        for r in R:
            for s, st in r["affidabilita_sensori"].items():
                if st != "affidabile" and s not in persi:
                    persi[s] = r["t"]
        for s, t in sorted(persi.items(), key=lambda z: z[1]):
            mom.append("%.1f s: «affidabilità persa: %s»" % (t, s))
        # perdite di continuita' piu' lunghe (traccia non vista), con la curva di C
        per = {}
        for r in R:
            for tr in r["tracce"]:
                if tr["parola"] != "vista" and tr["confidenza_C"] is not None and tr["oggetto_vero"]:
                    per.setdefault((tr["id"], tr["oggetto_vero"]), []).append((r["t"], tr["non_vista_da_s"], tr["confidenza_C"], tr["r99_m"], tr["insieme_presenza_r_m"]))
        lunghe = sorted(per.items(), key=lambda kv: -len(kv[1]))[:3]
        for (tid, ogg), xs in lunghe:
            if len(xs) < 5:
                continue
            pts = [xs[0], xs[len(xs) // 2], xs[-1]]
            mom.append("perdita di continuità, traccia %d (%s): da %.1f a %.1f s; C = %s; r99 = %s m; insieme di presenza = %s m"
                       % (tid, ogg, xs[0][0], xs[-1][0], " → ".join("%.2f a τ %.1f s" % (q[2], q[1]) for q in pts),
                          " → ".join("%.0f" % q[3] for q in pts), " → ".join("%.0f" % q[4] for q in pts)))
        out += ["- " + x for x in (mom or ["nessun momento notevole (atteso per il controllo)"])]
        out += ["", "Riassunto del passaggio: `%s`" % json.dumps(testa["riassunto"], ensure_ascii=False, default=float)[:600], ""]
    open(os.path.join(cart, "INDICE.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("\n".join(out)[:6000])


if __name__ == "__main__":
    main(sys.argv[1])
