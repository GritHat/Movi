# tabella.py — legge risultati*.txt e stampa le tabelle. Uso: python3 -I tabella.py risultati.txt
import sys
def leggi(p):
    R = []
    for r in open(p):
        if not r.startswith("rep="): continue
        d = {}
        for kv in r.split():
            k, v = kv.split("=", 1)
            try: d[k] = float(v)
            except ValueError: d[k] = v
        d["nome"] = d["rep"] + (f"{int(d['fasce'])}" if "fasce" in d else "") + (f"_{int(d['portata'])}m" if "portata" in d else "")
        R.append(d)
    return R
R = leggi(sys.argv[1])
def cerca(nome, scena, res, passo):
    for d in R:
        if d["nome"] == nome and d["scena"] == scena and d["res_cm"] == res and d["passo"] == passo: return d
    return None
NOMI = ["polare_3m", "polare_6m", "immagine", "fasce3", "fasce8", "fasce30", "colonne_bit", "densa", "hash8", "hash8_solo_occ", "octree", "octree_pot"]
print("== MEMORIA (byte usati dalla struttura; fra parentesi la memoria residente in piu' del processo, kB) ==")
for res in (10, 5):
    for passo in (4, 1):
        print(f"-- {res} cm, passo {passo}")
        for n in NOMI:
            riga = f"{n:16s}"
            for sc in ("vuota", "rada", "densa", "carico"):
                d = cerca(n, sc, res, passo)
                riga += f" {sc}: " + (f"{int(d['mem_B']):>8d} ({int(d['rss_delta_kB'])} kB) u={int(d['unita'])}" if d else "   --   ")
                if d and "nodi_picco" in d: riga += f" picco={int(d['nodi_picco'])} fine={int(d['nodi_fine_media'])}"
            print(riga)
print("\n== AGGIORNAMENTO ms: media / p95 / p99 / max | primo | ns per passo | raggi | passi ==")
for res in (10, 5):
    for sc in ("vuota", "rada", "densa", "carico"):
        for passo in (1, 2, 4, 8):
            righe = [(n, cerca(n, sc, res, passo)) for n in NOMI]
            if not any(d for _, d in righe): continue
            print(f"-- {sc} {res} cm passo {passo}")
            for n, d in righe:
                if not d: continue
                print(f"{n:16s} {d['agg_media_ms']:8.3f} / {d['agg_p95_ms']:8.3f} / {d['agg_p99_ms']:8.3f} / {d['agg_max_ms']:8.3f} | {d['agg_primo_ms']:7.3f} | "
                      f"{d.get('ns_passo', 0):5.2f} | {int(d['raggi_f']):7d} | {int(d['passi_f']):9d} | max/p50={d['agg_max_ms'] / d['agg_p50_ms']:.2f} | f={int(d['fotogrammi'])}")
print("\n== INTERROGAZIONE 18 settori, microsecondi: media / p95 / max ==")
for res in (10, 5):
    print(f"-- densa, passo 4, {res} cm")
    for n in NOMI:
        d = cerca(n, "densa", res, 4)
        if d: print(f"{n:16s} {d['int_media_us']:9.2f} / {d['int_p95_us']:9.2f} / {d['int_max_us']:9.2f}")
print("\n== CARICO IMPROVVISO (3 -> 200 oggetti al fotogramma 150), passo 4: p50 prima | max prima | fotogramma 150 | p50 dopo | max dopo | unita' 149 -> 150 -> fine | raggi e passi del f.150 ==")
for res in (10, 5):
    print(f"-- {res} cm")
    for n in NOMI:
        d = cerca(n, "carico", res, 4)
        if d: print(f"{n:16s} {d['prima_p50_ms']:8.3f} | {d['prima_max_ms']:8.3f} | {d['t150_ms']:8.3f} | {d['dopo_p50_ms']:8.3f} | {d['dopo_max_ms']:8.3f} | "
                    f"{int(d['unita_149'])} -> {int(d['unita_150'])} -> {int(d['unita_fine'])} | {int(d['raggi150'])} {int(d['passi150'])} | t150/p50={d['t150_ms'] / d['prima_p50_ms']:.2f}")
print("\n== SOMME DI CONTROLLO (uguali fra densa, hash8, octree, octree_pot = stessa uscita) ==")
for res in (10, 5):
    for sc in ("vuota", "rada", "densa", "carico"):
        for passo in (4, 1):
            v = [(n, cerca(n, sc, res, passo)) for n in ("densa", "hash8", "octree", "octree_pot")]
            if all(d for _, d in v): print(sc, res, passo, " ".join(f"{d['somma']:.1f}" for _, d in v), "UGUALI" if len({d['somma'] for _, d in v}) == 1 else "DIVERSE")
