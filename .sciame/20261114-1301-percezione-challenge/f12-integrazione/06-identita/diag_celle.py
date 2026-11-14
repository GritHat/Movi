import dataclasses, os, sys
import numpy as np
np.set_printoptions(linewidth=250)
sys.argv, argv = sys.argv[:1], sys.argv[1:]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prova as P
K = P.K
from catena import Catena
nome, kk, a0, a1, r0, r1 = argv[0], int(argv[1]), int(argv[2]), int(argv[3]), int(argv[4]), int(argv[5])
sorg = K.SorgenteCartella(os.path.join(K.SEQ_SIM, nome))
cat = Catena(sorg.meta, K.Parametri())
for k, (i, t, prof) in enumerate(sorg):
    cat.ciclo(i, t, prof)
    if k == kk:
        print(nome, "k", k, "n_ostacolo: righe = azimut", a0 - 90, "…", a1 - 90, "gradi; colonne = anelli", r0, "…", r1)
        print(cat.mappa_ciclo.n_ostacolo[a0:a1 + 1, r0:r1 + 1])
        break
