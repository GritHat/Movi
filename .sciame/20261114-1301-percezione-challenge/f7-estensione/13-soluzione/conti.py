# Conti di sciame-architetto (f7, fase f3). Rifare: python3 -I conti.py
import math
H=1.2; tilt=15.0; vfov=58.0
up=math.radians(vfov/2-tilt); dn=math.radians(vfov/2+tilt)
print("bordo alto +%.1f gradi, bordo basso -%.1f gradi"%(math.degrees(up),math.degrees(dn)))
print("PA1 suolo visto da r = %.3f m"%(H/math.tan(dn)))
print("PA1 ostacolo 0,15 m fuori campo sotto r = %.3f m"%((H-0.15)/math.tan(dn)))
print("PA1 quota 1,8 m vista da r = %.3f m"%((1.8-H)/math.tan(up)))
print("PA1 quota 2,0 m vista da r = %.3f m"%((2.0-H)/math.tan(up)))
print("PA1 tetto del campo: 1,2 + %.4f r ; a 1,24 m %.2f, a 2 m %.2f, a 3 m %.2f"%(math.tan(up),H+math.tan(up)*1.24,H+math.tan(up)*2,H+math.tan(up)*3))
for h,d in ((1.0,1.5),(0.5,1.5),(0.3,1.7),(0.4,1.7),(0.5,2.0),(1.0,1.83)):
    print("PA2 occlusore alto %.2f m a %.2f m: ombra al suolo fino a %.2f m"%(h,d,d*H/(H-h)))
# pannello: altezza minima perche' l'ombra copra un adulto di 1,8 m a 2,3 m, pannello a 1,7-1,9 m
for dp in (1.15,1.7,1.9):
    print("pannello a %.2f m: per nascondere 1,8 m a 2,3 m serve altezza >= %.2f m; tetto campo li' %.2f m"%(dp,H+(1.8-H)*dp/2.3,H+math.tan(up)*dp))
# S10: quota bassa minima 0,15 m contro 0,07 m del nucleo
print("S10 fascia alta fino a 2,0 m vista intera solo oltre %.2f m (griglia fino a 3 m)"%((2.0-H)/math.tan(up)))
# ore
for n in (3,4,5): print("persone %d: 14 h = %d ore-persona; +4 h = %d"%(n,14*n,4*n))
# altezza del pannello: che cosa resta in vista a 2,3 m sopra il bordo del pannello
tetto=H+math.tan(up)*2.3
for hp in (1.5,1.6,1.7):
    for dp in (1.7,1.9):
        print("pannello alto %.2f m a %.2f m: a 2,3 m si vede sopra %.3f m di quota (tetto del campo a 2,3 m: %.3f m)"%(hp,dp,H+(hp-H)*2.3/dp,tetto))
for dp in (1.7,1.9): print("altezza minima del pannello a %.2f m perche' niente resti in vista a 2,3 m: %.2f m"%(dp,H+(tetto-H)*dp/2.3))
