# Controllo esaustivo-campionato della Proposizione su t_C, separando f(0)<0 e f(0)>=0 (versione 2, accanto alla prima).
import numpy as np, math, json
k2=math.sqrt(-2*math.log(0.1)); k3=2.5002777108094056
def radici(a3,a2,a1,a0):
    c=np.roots([a3,a2,a1,a0]); return sorted(x.real for x in c if abs(x.imag)<1e-7*max(1,abs(x.real)) and x.real>1e-12)
rng=np.random.default_rng(20261115); st={'f0neg':[0,0],'f0pos_due_radici':0,'f0pos_zero_radici':0,'f0pos_altro':0,'f0pos':0}
for _ in range(20000):
    s0=rng.uniform(1,50); sv=rng.uniform(0.1,20); rho=rng.uniform(-0.99,0.99); s0v=rho*s0*sv; q=10**rng.uniform(-2,2)
    R=rng.uniform(1,5)*s0
    for k in (k2,k3):
        a0=s0**2-(R/k)**2; rr=radici(q/3,sv**2,2*s0v,a0)
        if a0<0:
            st['f0neg'][0]+=1; st['f0neg'][1]+= (len(rr)!=1)
        else:
            st['f0pos']+=1
            if len(rr)==2: st['f0pos_due_radici']+=1
            elif len(rr)==0: st['f0pos_zero_radici']+=1
            else: st['f0pos_altro']+=1
print(json.dumps(st))
