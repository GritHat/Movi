import random, math
random.seed(20261114)
N=10000; dt=0.05; tau=1.0; T=4.0
steps=int(T/dt)
checks=[0.5,1.0,1.5,2.0,2.5,3.0,4.0]
for sa in (0.5,1.0):
    errs={c:[] for c in checks}
    rho=math.exp(-dt/tau); s=sa*math.sqrt(1-rho*rho)
    for _ in range(N):
        # stato vero relativo alla previsione CV: errore di posizione e velocita' partono da zero
        ex=ey=evx=evy=0.0
        ax=random.gauss(0,sa); ay=random.gauss(0,sa)
        for k in range(1,steps+1):
            ex+=evx*dt+0.5*ax*dt*dt; ey+=evy*dt+0.5*ay*dt*dt
            evx+=ax*dt; evy+=ay*dt
            ax=rho*ax+random.gauss(0,s); ay=rho*ay+random.gauss(0,s)
            t=round(k*dt,2)
            if t in errs: errs[t].append(math.hypot(ex,ey))
    out=[]
    for c in checks:
        v=sorted(errs[c]); out.append((c, v[int(0.5*N)], v[int(0.95*N)]))
    print("sigma_a=",sa, " (t, mediana, r95) =", [(c,round(m,2),round(r,2)) for c,m,r in out])
# P2
for name,fov in (("VL53L8CX",45.0),("VL53L7CX",60.0)):
    z=fov/8; w=2*2.0*math.tan(math.radians(z/2))
    print(name,"copertura 3 sensori:",3*fov,"gradi; zona:",round(z,2),"gradi; larghezza zona a 2 m:",round(w,3),"m; zone coperte da 0,5 m:",round(0.5/w,1))
# P4
f=320/math.tan(math.radians(69/2)); om=math.radians(120)
for te in (0.010,0.033,0.002): print("f=",round(f),"px; esposizione",te*1000,"ms -> sfocatura",round(om*te*f,1),"px")
