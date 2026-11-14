#!/usr/bin/env python3
"""Arbitro f9: il piano minimo del pianificatore (piano_mc.py, copia identica, md5 nel VERDETTO)
ricondotto a 14 ore di orologio. Cambiano SOLO: le ore disponibili e l'ora da cui la camera esiste.
Durate, grafo, ordine «due corsie» e semi sono quelli del pianificatore.
Rifare:  PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 -B piano_14h.py > risultati_piano_14h.txt
Ipotesi mie (non verificate): ore utili per persona nelle 14 ore di orologio = triangolare (11; 12,5; 14);
nessuna chiusura sottratta (la chiusura sta nelle 4 ore di raffinamento); camera disponibile dall'ora T_CAM.
"""
import random
import statistics
import piano_mc as pm

ORE14 = (11.0, 12.5, 14.0)
DUE_CORSIE = {**pm.CLASSE, "N4r": 1, "N5": 1, "C1": 1, "N4": 1}


def calendario_tcam(piano, durate, n_persone, ranghi, t_cam):
    """Come pm.calendario, ma nessun compito che usa la camera parte prima di t_cam."""
    fine, in_corso, da_fare = {}, {}, set(piano)
    t, camera_libera = 0.0, True
    while da_fare or in_corso:
        pronti = [k for k in da_fare if all(q in fine for q in piano[k]["pred"])]
        pronti.sort(key=lambda k: (pm.CLASSE.get(k, 3), -ranghi[k], k))
        for k in pronti:
            if len(in_corso) >= n_persone:
                break
            if piano[k]["cam"]:
                if t < t_cam or not camera_libera:
                    continue
                camera_libera = False
            in_corso[k] = t + durate[k]
            da_fare.discard(k)
        if not in_corso:
            assert t < t_cam, "stallo"
            t = t_cam
            continue
        prossimo = min(in_corso.values())
        if t < t_cam < prossimo:
            t = t_cam
            continue
        k_fine = min(in_corso, key=lambda k: (in_corso[k], k))
        t = in_corso.pop(k_fine)
        fine[k_fine] = t
        if piano[k_fine]["cam"]:
            camera_libera = True
    return fine


def main():
    rng0 = random.Random(pm.SEME)
    disp = [rng0.triangular(ORE14[0], ORE14[2], ORE14[1]) for _ in range(pm.N_ESTRAZIONI)]
    print(f"# piano_14h.py, seme {pm.SEME}, {pm.N_ESTRAZIONI} estrazioni per cella, piano MIN e MED, ordine «due corsie»")
    print(f"# ore utili nelle 14 ore: triangolare {ORE14}; mediana {statistics.median(disp):.2f} h")
    # autocontrollo: con t_cam = 0 il mio calendario deve dare le stesse ore di fine di quello del pianificatore
    pm.CLASSE.clear(); pm.CLASSE.update(DUE_CORSIE)
    piano = pm.costruisci(pm.MIN, "posseduto"); ranghi = pm.rango(piano)
    rng = random.Random(pm.SEME + 4); diff = 0.0
    for _ in range(500):
        dur = pm.estrai(piano, rng)
        a = pm.calendario(piano, dur, 4, ranghi); b = calendario_tcam(piano, dur, 4, ranghi, 0.0)
        diff = max(diff, max(abs(a[k] - b[k]) for k in piano))
    print(f"# autocontrollo (t_cam = 0 contro il calendario del pianificatore, 500 estrazioni): scarto massimo {diff:.2e} h -> {'torna' if diff < 1e-9 else 'NON TORNA'}")
    print("# colonne: mediana / 80-esimo percentile (ore di lavoro, k = 1) | P(chiusa entro le ore utili, k = 1) | P(entro 14,0 h) | k*(80 %)")
    casi = [("MIN", pm.MIN, "assente", 0.0, "nessun sensore per tutte le 14 ore (dati registrati o simulati)"),
            ("MIN", pm.MIN, "nuovo", 5.5, "sensore mai provato, disponibile dall'ora 5,5"),
            ("MIN", pm.MIN, "posseduto", 0.0, "riferimento: sensore posseduto dall'ora 0 (caso del pianificatore)"),
            ("MED", pm.MED, "nuovo", 5.5, "piano con seconda ipotesi, livelli e massimo avvicinamento; sensore dall'ora 5,5")]
    for nome, spec, sens, tcam, descr in casi:
        piano = pm.costruisci(spec, sens); ranghi = pm.rango(piano)
        for n in (3, 4, 5):
            rng = random.Random(pm.SEME + n)
            pt = {t: [] for t, _ in pm.TAPPE}
            for _ in range(pm.N_ESTRAZIONI):
                dur = pm.estrai(piano, rng)
                fine = calendario_tcam(piano, dur, n, ranghi, tcam)
                for t, chiavi in pm.TAPPE:
                    ks = list(piano) if chiavi is None else [k for k in chiavi if k in piano]
                    pt[t].append(max(fine[k] for k in ks))
            print(f"-- {nome}, {descr}, N = {n}")
            for t, _ in pm.TAPPE:
                p_w = sum(1 for a, m in zip(disp, pt[t]) if m <= a) / pm.N_ESTRAZIONI
                p_14 = sum(1 for m in pt[t] if m <= 14.0) / pm.N_ESTRAZIONI
                # k* : per tcam > 0 la camera non scala con k; qui k* e' il quantile del rapporto, indicativo
                ks = pm.quantile([a / m for a, m in zip(disp, pt[t])], 0.20)
                print(f"   {t:34s} {statistics.median(pt[t]):5.1f} / {pm.quantile(pt[t], 0.8):5.1f} h | {100*p_w:5.1f} % | {100*p_14:5.1f} % | k* {ks:4.2f}")


if __name__ == "__main__":
    main()
