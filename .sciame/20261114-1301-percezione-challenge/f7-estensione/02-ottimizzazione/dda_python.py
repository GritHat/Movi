# P12: lancio dei raggi denso in Python puro (nessuna libreria), 10 cm, 160x120 raggi, suolo + parete di fondo.
# Uso: timeout 110 python3 dda_python.py
import math, time
VS=0.1; NX,NY,NZ=60,40,30; W,H=160,120
SO=(0.001,2.001,1.201)
th=math.tan(math.radians(87/2)); tv=math.tan(math.radians(58/2)); cp=math.cos(math.radians(15)); sp=math.sin(math.radians(15))
rays=[]
for v in range(H):
    for u in range(W):
        x=1.0; y=-th*(2*(u+0.5)/W-1); z=-tv*(2*(v+0.5)/H-1)
        xr=x*cp+z*sp; zr=-x*sp+z*cp; n=math.sqrt(xr*xr+y*y+zr*zr); d=(xr/n,y/n,zr/n)
        te=1e30
        for k,roi in enumerate((6.0,4.0,3.0)):
            if d[k]>0: te=min(te,(roi-SO[k])/d[k])
            elif d[k]<0: te=min(te,(0-SO[k])/d[k])
        t=(5.95-SO[0])/d[0]
        if d[2]<0: t=min(t,-SO[2]/d[2])
        rays.append((d,te-1e-7,t))
L=[0]*(NX*NY*NZ); TAU=[0]*(NX*NY*NZ)
def frame(f):
    steps=0
    ox,oy,oz=SO; ix0=int(ox/VS); iy0=int(oy/VS); iz0=int(oz/VS)
    for d,tex,t in rays:
        hit = t<tex; tend = t if hit else tex
        ix,iy,iz=ix0,iy0,iz0
        dx,dy,dz=d
        sx=1 if dx>0 else -1; sy=1 if dy>0 else -1; sz=1 if dz>0 else -1
        tdx=VS/abs(dx) if dx else 1e30; tdy=VS/abs(dy) if dy else 1e30; tdz=VS/abs(dz) if dz else 1e30
        tmx=((ix+1)*VS-ox)/dx if dx>0 else ((ix*VS-ox)/dx if dx<0 else 1e30)
        tmy=((iy+1)*VS-oy)/dy if dy>0 else ((iy*VS-oy)/dy if dy<0 else 1e30)
        tmz=((iz+1)*VS-oz)/dz if dz>0 else ((iz*VS-oz)/dz if dz<0 else 1e30)
        ok=True
        while True:
            tn = tmx if (tmx<tmy and tmx<tmz) else (tmy if tmy<tmz else tmz)
            if tn>=tend: break
            i=(ix*NY+iy)*NZ+iz; steps+=1
            l=L[i]-40; L[i]= -200 if l<-200 else l; TAU[i]=f
            if tmx<=tmy and tmx<=tmz:
                ix+=sx; tmx+=tdx
                if ix<0 or ix>=NX: ok=False; break
            elif tmy<=tmz:
                iy+=sy; tmy+=tdy
                if iy<0 or iy>=NY: ok=False; break
            else:
                iz+=sz; tmz+=tdz
                if iz<0 or iz>=NZ: ok=False; break
        if not ok: continue
        i=(ix*NY+iy)*NZ+iz; steps+=1
        if hit:
            l=L[i]+85; L[i]=350 if l>350 else l
        else:
            l=L[i]-40; L[i]= -200 if l<-200 else l
        TAU[i]=f
    return steps
ts=[]
for f in range(1,6):
    a=time.perf_counter(); s=frame(f); ts.append((time.perf_counter()-a)*1e3)
ts.sort()
print(f"python_puro densa 10cm raggi={W*H} passi/fot={s} ms: min={ts[0]:.1f} mediana={ts[2]:.1f} max={ts[-1]:.1f}")
