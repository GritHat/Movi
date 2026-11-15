# Esempio calcolato per il capitolo: C(tau), t_C, r_0.9 e insieme di presenza; controllo dell'unicita' della radice.
import numpy as np, json, math
from math import erf, sqrt, exp, pi
def s2(t,s0,s0v,sv,q): return s0**2+2*s0v*t+sv**2*t**2+q*t**3/3
def C2(t,r,*a): return 1-exp(-r**2/(2*s2(t,*a)))
def C3(t,r,*a):
    k=r/sqrt(s2(t,*a)); return erf(k/sqrt(2))-sqrt(2/pi)*k*exp(-k*k/2)
k2=sqrt(-2*math.log(0.1))
# k3 per bisezione
lo,hi=0.1,10
for _ in range(200):
    m=(lo+hi)/2
    if erf(m/sqrt(2))-sqrt(2/pi)*m*exp(-m*m/2)<0.9: lo=m
    else: hi=m
k3=(lo+hi)/2
par=dict(s0=7.5,s0v=0.0,sv=2.0,q=4.0)   # ipotesi illustrativa: aereo, radar 7,5 m, sigma_v 2 m/s, q 4 m^2/s^3
a=(par['s0'],par['s0v'],par['sv'],par['q'])
r=100.0
def tC(r,k,*a):
    c=np.roots([a[3]/3,a[2]**2,2*a[1],a[0]**2-(r/k)**2]); c=[x.real for x in c if abs(x.imag)<1e-9 and x.real>0]; return c
out={'k2_09':k2,'k3_09':k3,'parametri':par,'r':r}
out['tC_2D']=tC(r,k2,*a); out['tC_3D']=tC(r,k3,*a)
out['tabella']=[dict(tau=t,C2=C2(t,r,*a),C3=C3(t,r,*a),r09_2D=k2*sqrt(s2(t,*a)),r09_3D=k3*sqrt(s2(t,*a)),r_pres=3.4*7.5+210*t) for t in [1,2,5,10,20,30]]
# controllo unicita' con covarianza incrociata negativa (convessita')
rng=np.random.default_rng(20261115); viol=0; n=0
for _ in range(20000):
    s0=rng.uniform(1,50); sv=rng.uniform(0.1,20); rho=rng.uniform(-0.99,0.99); s0v=rho*s0*sv; q=10**rng.uniform(-2,2)
    R=rng.uniform(1,5)*s0
    for k in (k2,k3):
        n+=1
        if len(tC(R,k,s0,s0v,sv,q))!=1: viol+=1
out['unicita']=dict(casi=n,violazioni=viol)
print(json.dumps(out,indent=1))
