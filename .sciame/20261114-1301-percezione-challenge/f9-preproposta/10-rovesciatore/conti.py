# conti.py — sciame-rovesciatore f9: conti di controllo (nessun caso). python3 conti.py
import math
# P9: uniforme sul cuneo d'ombra della demo (pannello 1 m a 1,8 m, portata 3 m, sensore in 0)
n=0;sx=sxx=sz=szz=0.0;step=0.005
z=1.8
while z<3.0:
    half=0.5*z/1.8; x=-half
    while x<=half:
        if math.hypot(x,z)<=3.0:
            n+=1;sx+=x;sxx+=x*x;sz+=z;szz+=z*z
        x+=step
    z+=step
mx=sx/n;mz=sz/n;vx=sxx/n-mx*mx;vz=szz/n-mz*mz
print(f"P9 cuneo demo: area {n*step*step:.2f} m2, sigma_x {math.sqrt(vx):.2f} m, sigma_z {math.sqrt(vz):.2f} m, raggio efficace {math.sqrt(vx+vz):.2f} m (soglia della preproposta 0,8 m)")
# quanto deve essere largo un pannello perche' l'uniforme sull'ombra superi 0,8 m (solo trasversale, sulla linea dell'attore)
print(f"   uniforme su un segmento: sigma = L/sqrt(12); sigma 0,8 m chiede L = {0.8*math.sqrt(12):.2f} m d'ombra")
# H2: distanza d'arresto con v_k = alpha v_{k-1} a 15 Hz
for a in (0.80,0.90,0.95):
    print("H2 alpha",a,"distanza d'arresto (m) a 0,5 / 1,2 / 1,4 m/s:",[round(v/15*a/(1-a),2) for v in (0.5,1.2,1.4)],
          " decelerazione iniziale a 1,2 m/s:",round(1.2*(1-a)*15,1),"m/s2")
print("   meta' ombra sulla linea dell'attore: 0,64 m (0,84 m dall'ultima misura con C6)")
# striscia di libero falso che azzera tutta la massa: larghezza >= v*dt
for v in (0.5,1.2,1.4): print(f"striscia critica a {v} m/s: {100*v/15:.1f} cm (una cella da 1 grado a 2,3 m = {100*2.3*math.radians(1):.1f} cm)")
# uscita dal lato lontano: dal punto a 2,3 m al bordo della portata (3 m) lungo il raggio
for v in (0.5,1.2,1.4): print(f"uscita radiale 2,3 -> 3,0 m a {v} m/s: {0.7/v:.2f} s")
# S1: media di T_cycle su 15 cicli
print("S1 media su 15 cicli: 12 cicli a 40 ms + 3 a 100 ms ->", (12*40+3*100)/15, "ms (soglia 55; il 20 % dei cicli supera 66,6 ms)")
print("S1 media: 14 cicli a 40 ms + 1 singhiozzo di 300 ms ->", round((14*40+300)/15,1), "ms (supera 55 per un solo ciclo anomalo)")
# S1: ciclo limite. Configurazione piena costa 58 ms, ridotta 40 ms; regole della tabella 1.2 (riduci se >55, piena se <45); isteresi 2,5 s
t=0.0;cfg='piena';last=-1e9;sw=0
while t<60:
    T=58 if cfg=='piena' else 40
    want='ridotta' if T>55 else ('piena' if T<45 else cfg)
    if want!=cfg and t-last>=2.5: cfg=want;last=t;sw+=1
    t+=0.5   # valutazione a 2 Hz
print("S1 ciclo limite: cambi di configurazione in 60 s con isteresi di 2,5 s =",sw)
# S8: quota dell'estensione 0,5-3 m mai osservata (anello cieco fino a 1,24 m, numero del nucleo)
print("S8: anello cieco 0,5-1,24 m su 0,5-3 m =", round((1.24-0.5)/(3-0.5)*100,1), "% dell'estensione radiale")
