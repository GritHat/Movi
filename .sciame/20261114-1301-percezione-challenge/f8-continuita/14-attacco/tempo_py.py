# tempo_py.py — costo di un ciclo di sd-1 (C-004 fronte + scia, 3 lisciature, 90 % per scenario) in Python PURO, geometria T.
# numpy non e' installato: questa e' la misura senza numpy (limite alto per una squadra che lo usa: non verificato).
import math, random, time, sys
DT=1/15; CELL=0.10; HD=0.0707; HFOV=math.radians(43.5); YP=2.0; W=1.0; YS=4.0; RMAX=6.0; TA=(W/2)/YP; BAND=0.20; NM=400; KH=90
def dwedge(x,y,yp,t):
    ax=abs(x)
    if y>=yp and ax<=y*t: return 0.0
    cx=yp*t; n=math.sqrt(1+t*t); qx=ax-cx; qy=y-yp; al=(qx*t+qy)/n
    dray=math.hypot(qx,qy) if al<=0 else abs(qx-qy*t)/n
    dbot=abs(yp-y) if ax<=cx else math.hypot(qx,qy)
    return min(dray,dbot)
GX=math.ceil((RMAX*math.sin(HFOV)+0.05)*10)/10; NX=round(2*GX/CELL); NY=round(RMAX/CELL)
dom=[False]*(NX*NY); aidx=[-1]*(NX*NY); A=[]
for j in range(NY):
    for i in range(NX):
        x=-GX+(i+0.5)*CELL; y=(j+0.5)*CELL; c=j*NX+i
        dom[c]= y>0 and math.hypot(x,y)<=RMAX and abs(math.atan2(x,y))<=HFOV
        if dom[c] and dwedge(x,y,YP,TA)-HD<=BAND: aidx[c]=len(A); A.append(c)
NA=len(A); NB=[]
for a,c in enumerate(A):
    i=c%NX; j=c//NX; nb=[]
    for dj in (-1,0,1):
        for di in (-1,0,1):
            ii=i+di; jj=j+dj
            if 0<=ii<NX and 0<=jj<NY and aidx[jj*NX+ii]>=0: nb.append(aidx[jj*NX+ii])
    NB.append(nb)
rnd=random.Random(7); NLIB=200; LA=[]; LC=[]
for s in range(NLIB):
    ea=rnd.gauss(0,0.12); ec=rnd.gauss(0,0.10); LA.append([ea*i*DT+rnd.gauss(0,0.02) for i in range(KH+1)]); LC.append([ec*i*DT+rnd.gauss(0,0.02) for i in range(KH+1)])
class Trk:
    def __init__(s,q):
        s.p0x=-(TA*YS+0.3)-0.01*q; s.p0y=YS; s.v0x=0.6+0.04*q; s.v0y=0.05; sp=math.hypot(s.v0x,s.v0y); s.ux=s.v0x/sp; s.uy=s.v0y/sp
        s.w=[1.0]*NM; s.frz=[10**6]*NM
        for j in range(NM//2,NM):
            u=((j-NM//2+0.5)*0.6180339887)%1.0; s.frz[j]=int(u*KH)
def smooth(src):
    out=[0.0]*NA
    for a in range(NA):
        v=src[a]
        if v>0.0:
            nb=NB[a]; sh=v/len(nb)
            for b in nb: out[b]+=sh
    return out
def step(t,i):
    d=[[0.0]*NA,[0.0]*NA]; S=[0.0,0.0]; w=t.w; half=NM//2
    for j in range(NM):
        ii=i
        if j>=half and ii>t.frz[j]: ii=t.frz[j]
        lj=(j%half)%NLIB; al=LA[lj][ii]; cr=LC[lj][ii]
        x=t.p0x+t.v0x*ii*DT+t.ux*al-t.uy*cr; y=t.p0y+t.v0y*ii*DT+t.uy*al+t.ux*cr
        ci=int((x+GX)//CELL); cj=int(y//CELL)
        if ci<0 or ci>=NX or cj<0 or cj>=NY: continue
        c=cj*NX+ci
        if not dom[c]: continue
        a=aidx[c]
        if a<0: w[j]*=0.1; continue
        s=1 if j>=half else 0; d[s][a]+=w[j]; S[s]+=w[j]
    reg=set()
    for s in (0,1):
        if S[s]<=0: continue
        src=d[s]
        for q in range(3): src=smooth(src)
        cells=[(v,a) for a,v in enumerate(src) if v>0.0]; cells.sort(reverse=True); tot=sum(v for v,_ in cells); cum=0.0
        for v,a in cells:
            if cum>=0.9*tot: break
            reg.add(a); cum+=v
    if not reg: reg=set(range(NA))
    return reg
for nt in (1,3,10):
    tm=[]
    for rep in range(3 if nt<10 else 2):
        T=[Trk(q) for q in range(nt)]
        for i in range(1,76):
            t0=time.perf_counter()
            for t in T: step(t,i)
            tm.append((time.perf_counter()-t0)*1e3)
    tm.sort(); print(f"TEMPO_PY geo=T tracce={nt} celle_A={NA} cicli={len(tm)} mediana={tm[len(tm)//2]:.1f} ms p95={tm[int(0.95*len(tm))]:.1f} ms max={tm[-1]:.1f} ms  (python {sys.version.split()[0]}, puro)")
