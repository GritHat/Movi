import random, math
rnd=random.Random(3); gate=[]
dt=0.1; sig=0.05; pD=0.95; q=0.5; N=400; NP=200; FOV=3.5; SH=1.0
def vis(y): return abs(y)<=FOV and abs(y)>SH
def scen(kind):
    y=-3.0; v=1.3; out=[]; t=0; sa=rnd.uniform(-0.6,0.6); sT=rnd.uniform(2,4); stp=0.0; done=False
    while t<14:
        t+=dt
        if kind in('ii','iii') and not done and y>=sa:
            if kind=='iii': out.append(None); continue
            stp+=dt
            if stp>=sT: done=True
        else: y+=v*dt
        out.append(y if y<=FOV else None)
    return out
def run(kind,pol):
    tr=scen(kind); m=None; alive=False; unseen=0.0; ve=0.0; part=None; r=1.0
    kept=None; ghost=0.0; entered=False; life=None; tlost=None
    for k,y in enumerate(tr):
        det=(y is not None) and vis(y) and rnd.random()<pD
        z=y+rnd.gauss(0,sig) if det else None
        if (y is not None and abs(y)<=SH) or (y is None and kind=='iii'): entered=True
        if m is None:
            if det: m=[z,1.0]; P=[sig*sig,0.0,1.0]; alive=True
            continue
        if not alive:
            if det and entered and kept is None: kept=False
            continue
        a,b,c=P; m=[m[0]+m[1]*dt,m[1]]; P=[a+2*b*dt+c*dt*dt+q*dt**3/3,b+c*dt+q*dt*dt/2,c+q*dt]
        if part is not None:
            for p in part:
                if rnd.random()<0.3*dt: p[1]=0.0          # modo sosta
                p[0]+=p[1]*dt+rnd.gauss(0,math.sqrt(q*dt**3/3)); p[1]+=rnd.gauss(0,math.sqrt(q*dt)) if p[1]!=0.0 or rnd.random()<0.3*dt else 0.0
        if det:
            if entered and kept is None:
                kept=True
                if part is not None: gate.append(min(abs(z-p[0]) for p in part))
                else: gate.append(abs(z-m[0])/math.sqrt(P[0]+sig*sig))
            if part is not None: m=[z,1.0]; P=[sig*sig,0.0,1.0]; part=None; r=1.0
            else:
                a,b,c=P; S=a+sig*sig; k1=a/S; k2=b/S; d=z-m[0]; m=[m[0]+k1*d,m[1]+k2*d]; P=[a-k1*a,b-k1*b,c-k2*b]
            unseen=0; ve=0
        else:
            if tlost is None: tlost=k
            unseen+=dt
            if pol=='F1' and unseen>1.0: alive=False
            if pol=='F5' and unseen>5.0: alive=False
            if pol=='OAm':
                if vis(m[0]): ve+=dt
                if ve>0.3 or unseen>10: alive=False
            if pol=='OAp':
                if part is None:
                    a,b,c=P; sa_=math.sqrt(a); part=[]
                    for _ in range(NP):
                        e1=rnd.gauss(0,1); e2=rnd.gauss(0,1); dp=sa_*e1
                        part.append([m[0]+dp, m[1]+(b/a)*dp+math.sqrt(max(c-b*b/a,1e-9))*e2])
                w=[(1-pD) if vis(p[0]) else 1.0 for p in part]; s=sum(w)/NP
                r=r*s/(1-r+r*s)
                part=[list(p) for p in rnd.choices(part,weights=w,k=NP)]
                m=[sum(p[0] for p in part)/NP,sum(p[1] for p in part)/NP]
                if r<0.05 or unseen>10: alive=False
            if alive and kind=='iii' and vis(m[0]): ghost+=dt
        if not alive and life is None and tlost is not None: life=(k-tlost)*dt
    return kept,ghost,life
print("pol scen tenuta n fantasma_in_zona_visibile_s vita_dopo_perdita_s(solo tracce chiuse)")
for pol in ('F5','OAp'):
    for kind in ('i','ii','iii'):
        res=[run(kind,pol) for _ in range(N)]
        k=[x[0] for x in res if x[0] is not None]; l=[x[2] for x in res if x[2] is not None]
        g=sorted(gate); gate.clear()
        print('  scarto alla ricomparsa (OAp: m dalla particella piu vicina; F5: sigma) mediana/max:', (round(g[len(g)//2],2),round(g[-1],2)) if g else None)
        print(pol,kind, round(sum(k)/len(k),3) if k else 'n/a', len(k), round(sum(x[1] for x in res)/N,2), round(sum(l)/len(l),2) if l else 'mai chiusa', len(l))
