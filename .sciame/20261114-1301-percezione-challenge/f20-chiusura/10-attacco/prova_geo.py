import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import geometria as G
import numpy as np
for v in ['F6-vicino', 'F3-ang30']:
    t = time.time(); print(G.lavoro((v, 'sda', 4999)), round(time.time()-t, 1))
G.pv4.SCV['F6'] = G.BASE['F6']; R, _ = G.pv4.passaggio_volo('F6', 'sda', 4999); D = G.pv4._G['D']
P1 = D['ver']['aereo1'][1]; P2 = D['ver']['aereo2'][1]; dd = np.linalg.norm(P1-P2, axis=1)
print('F6 nominale dmin', dd.min(), np.argmin(dd)*0.1, 'durata', len(P1)*0.1, 'evento', R.get('evento') is not None)
