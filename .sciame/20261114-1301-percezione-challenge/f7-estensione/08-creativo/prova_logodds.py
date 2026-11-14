# prova_logodds.py — sciame-creativo, f7. Un raggio, mappa a log-odds con i parametri predefiniti di OctoMap.
# Uso: python3 prova_logodds.py     (deterministico, nessun numero casuale)
import math
LH, LM = math.log(0.7/0.3), math.log(0.4/0.6)
LMIN, LMAX = math.log(0.1192/0.8808), math.log(0.971/0.029)
HZ, SPESSORE, PARTENZA, ARRIVO = 15.0, 0.30, 4.0, 1.0
print(f"colpo {LH:+.3f}, mancato {LM:+.3f}, limiti {LMIN:+.3f} / {LMAX:+.3f}; da saturo libero servono {math.ceil(-LMIN/LH)} colpi per superare 0,5; da saturo occupato {math.ceil(LMAX/-LM)} mancati per scendere sotto 0,5")
for vox in (0.05, 0.10):
    for v in (0.2, 0.5, 1.0, 1.5):
        n = int(6.0/vox); L = [LMIN]*n          # tutto gia' visto libero fino a saturazione
        fot = occ = 0; dentro_tot = dentro_liberi = 0; t = 0.0
        while True:
            faccia = PARTENZA - v*t
            if faccia < ARRIVO: break
            k = int(faccia/vox)
            for i in range(k): L[i] = max(LMIN, L[i]+LM)      # il raggio attraversa: mancato
            L[k] = min(LMAX, L[k]+LH)                          # il raggio finisce qui: colpo
            fot += 1; occ += L[k] > 0
            for i in range(k+1, min(n, int((faccia+SPESSORE)/vox)+1)):   # voxel dentro il corpo, non visibili
                dentro_tot += 1; dentro_liberi += L[i] < 0
            t += 1/HZ
        # scia: fotogrammi in cui restano 'occupati' voxel ormai vuoti dietro... (non misurata qui)
        print(f"voxel {vox:.2f} m, v {v:.1f} m/s: fotogrammi {fot}, faccia vista 'occupata' {occ} ({100*occ/fot:.0f} %); voxel-fotogramma dentro il corpo {dentro_tot}, di cui tenuti 'liberi' {dentro_liberi} ({100*dentro_liberi/max(1,dentro_tot):.0f} %)")
