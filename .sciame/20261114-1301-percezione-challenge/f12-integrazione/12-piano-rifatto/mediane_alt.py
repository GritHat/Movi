# Mediane della fine di ogni compito del calendario alternativo senza cancello (ALTn), nei tre modelli.
# Rifare: <venv>/bin/python -B mediane_alt.py > mediane_alt.txt   (importa rifai_mc.py che gli sta accanto)
import numpy as np
import rifai_mc as m
c = m.compiti_alt('F4', False)
r = {n: m.simula(c, m.MIE, ip)[0] for n, ip in (('leggero', m.LEGGERO), ('medio', m.MEDIO), ('duro', m.DURO))}
print("compito chi   fine mediana (h): leggero / medio / duro   | 80o percentile medio")
for cid, chi, _ in c:
    print(f"{cid:<5s} {'+'.join(chi) if len(chi) < 5 else 'tutti':<6s} {np.median(r['leggero'][cid]):5.1f} / {np.median(r['medio'][cid]):5.1f} / "
          f"{np.median(r['duro'][cid]):5.1f}   | {np.percentile(r['medio'][cid], 80):5.1f}")
