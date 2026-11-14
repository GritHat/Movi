# Ricalcolo dei conti in forma chiusa dei capitoli 2-5. Codice mio.
from math import *
d2r=pi/180
h=1.2;th=15*d2r
print("== cap.2")
for Pv in (58,59.0,60,65):
    bm=th+Pv/2*d2r; bp=Pv/2*d2r-th
    print(Pv,"zmin",round(h/tan(bm),3),"a=0.15",round((h-0.15)/tan(bm),3),"a=0.10",round((h-0.10)/tan(bm),3),"tanb+",round(tan(bp),3),"q1.80 da",round(0.6/tan(bp),2))
bm=44*d2r;bp=14*d2r;zmin=h/tan(bm)
Th=tan(43.5*d2r)
print("lat",round(Th*cos(th),3),round(Th*h*sin(th),3),"rho30",round(zmin/cos(30*d2r),2),"rho43.5",round(zmin/cos(43.5*d2r),2))
xs=Th*(zmin*cos(th)+h*sin(th));print("spigolo x",round(xs,3),"phi",round(atan2(xs,zmin)/d2r,1),"rho",round(hypot(xs,zmin),2))
print("f424: zmin/cos44",round(1.2/tan((15+29.5)*d2r)/cos(44*d2r),3))
print("ymax",[ (z,round(h+z*tan(bp),2)) for z in (1.24,1.7,1.9,2.0,2.3,3.0)])
print("vista da",[ (y,round((y-h)/tan(bp),2)) for y in (1.6,1.7,1.8,1.9,2.0)])
print("zmin Pv 55,61:",round(h/tan((15+27.5)*d2r),2),round(h/tan((15+30.5)*d2r),2)," th 14,16:",round(h/tan(43*d2r),2),round(h/tan(45*d2r),2))
print("focali",round(424/tan(43.5*d2r),1),round(240/tan(29*d2r),1),"424->",round(2*atan(1)/d2r,1),round(2*atan(240/424)/d2r,1),"gemini 410.7:",round(2*atan(424/410.7)/d2r,1))
print("disco",round(pi*9,2),"settore",round(0.5*87*d2r*(9-zmin**2),2),round(0.5*87*d2r*(9-zmin**2)/(pi*9)*100,1))
# area esatta
A=0;dz=0.0005;z=zmin+dz/2
while z<3:
    A+=2*min(Th*(z*cos(th)+h*sin(th)),sqrt(9-z*z))*dz;z+=dz
print("area esatta",round(A,2),round(A/(pi*9)*100,1))
print("ombre",round(1.7*1.2/0.9,2),round(1.5*1.2/0.7,2),round(1.5*1.2/0.2,1))
print("amin");
for s in (1.60,1.70,1.75,9):
    print(s,[round(h+zo*min((s-h)/2.3,tan(bp)),2) for zo in (1.15,1.5,1.7,1.8,1.9,2.0)])
print("visibile sopra 1.5:",round(h+0.3*2.3/1.7,2),round(h+0.3*2.3/1.9,2))
print("durata");
for L,zo in ((1,1.7),(1,1.9),(2,1.7),(2,1.9)):
    o=L*2.3/zo; print(L,zo,round(o,2),round(o-0.45,2),[round((o-0.45)/v,2) for v in (1.4,1.0,0.5)])
print("banda")
for db in (1,1.5,2):
    print(db,[(round(b*(3-db)/db*100,1),round(f*b*(1/db-1/3),1)) for b,f in ((0.095,424),(0.05,424),(0.05,410.7))])
print("striscia px a 2 m",424*0.095/2,424*0.05/2,"ritardo",round(0.19/1.2,2))
print("rumore")
for nome,fb,sd,kl in (("D455",424*0.095,0.08,0.005),("D435i",424*0.05,0.08,0.010),("G335",410.7*0.05,None,0.0075)):
    kn=sd/fb if sd else 0.004
    print(nome,round(fb,2),"nom",[round(kn*d*d*100,2) for d in (1,2,3,4)],round(sqrt(0.05/kn),1),"lim",[round(kl*d*d*100,2) for d in (1,2,3,4)],round(sqrt(0.05/kl),1),"sd nom/lim px",round(kn*fb,3),round(kl*fb,3),"quant mm",[round(d*d/32/fb*1000,1) for d in (1,2,3,4)],"q/sqrt12 a 3m",round(9/32/fb*1000/sqrt(12),1))
s=lambda d:0.00106+0.00073*d+0.00395*d*d
print("ahn 2m",round(s(2)*100,2),"rapporto",round(s(2)/(0.08/21.2*4),2),"px eq",round(s(2)*21.2/4,3),"3m",round(s(3)*100,1))
print("incidenza",[round(atan(r/h)/d2r) for r in (1.24,2.08,3)],"px",round(2/446.8*1000,1),round(3/446.8*1000,1),"5px a 3m",round(5*3/446.8*100,1),round(5*6/446.8*100,1),"1cm entro",round(0.01*446.8/5,2),"f424",round(5*3/424*100,1),"blur",1.5*8,1.5*30)
print("posa 1°",[round((r*sin(d2r)+h*(1-cos(d2r)))*100,1) for r in (2,2.8,3)],"2°: rho",round(0.07/(2*d2r),2),"a=.10",[round(0.03/r/d2r,2) for r in (2,2.55,3)],"a=.15 a 2m",round(0.08/2/d2r,1),"a=.12@2.55",round(0.05/2.55/d2r,2),"a=.15@2.55",round(0.08/2.55/d2r,2),"15cm@2.0-2.15",round(0.08/2.15/d2r,1),round(0.08/2.0/d2r,1))
print("tof",round(2*2*tan(3.75*d2r)*100,1),round(2*2*tan(2.8125*d2r)*100,1),"diag",round(2*2*tan(3.75*d2r)*100*sqrt(2)),round(2*2*tan(2.8125*d2r)*100*sqrt(2)),"campo",round(4*tan(30*d2r),2),round(4*tan(22.5*d2r),2),"zone",round(0.5/(2*4*tan(3.75*d2r)),2),round(0.5/(2*4*tan(2.8125*d2r)),2),"obl",round(hypot(1.2,2),2),"area",round(3*.5*pi/3*4,2),round(3*.5*pi/3*4/(pi*9)*100,1),round(3*.5*pi/3*.25/(pi*9)*100,1))
print("lidar",round(3*0.72*d2r*100,1),round(3*0.8*d2r*100,1),"punti",round(0.5/(3*0.72*d2r),1),round(0.5/(3*0.8*d2r),1),"gamba 5m",round(0.12/(5*0.72*d2r),1),round(0.12/(5*0.8*d2r),1),"passo",360/450)
print("== cap.3")
print(87*30,"posa",round(3*0.5*d2r*100,1),round(3*d2r*100,1),round(3*2*d2r*100,1),"logodds",round(log(0.7/0.3),3),round(log(0.1192/0.8808),3),"incl",round(0.03/2.5/d2r,2),round(0.03/3/d2r,2),"quota con 1°",round((0.10-2.5*d2r)*100,1),round((0.10-3*d2r)*100,1),"2Δ·2.5",round(2/15*2.5,2),"cella a 2m cm",round(2*d2r*100,1))
print("== cap.4")
from statistics import NormalDist as ND
Phi=ND().cdf
fb=424*0.05
print("sz",[round(0.08*d*d/fb*100,2) for d in (2,3,4)],"st",[round(d*d2r/sqrt(12)*100,2) for d in (2,3,4)])
sd=sqrt(2/3);print("sdelta",round(sd,4),"soglia",round(5*sd,2),"cm",round(5*sd*1.51,1),round(5*sd*1.01,1),"Pfa",2*(1-Phi(5)),"unione",2*13*2*(1-Phi(5)))
Tw=13/15
for nome,sig in (("nom2",0.0151),("nom3",0.0340),("pess3",0.09),("sev3",0.1125)):
    print(nome,round(5*sd*sig/Tw,3),round((5+1.2816)*sd*sig/Tw,3),"P(0.5)",round(Phi(0.5*Tw/(sd*sig)-5),3))
print("soglia dimezzata Pfa",2*(1-Phi(2.5)))
from math import comb
B=lambda n,p,k:sum(comb(n,i)*p**i*(1-p)**(n-i) for i in range(k,n+1))
print("non conf",[round((1-B(n,0.9,3))*100,1) for n in (3,4,5)],"rit",[(j,round((j-1)*.81*.1**(j-2),4)) for j in (2,3,4)],"media s",round(sum(j*(j-1)*.81*.1**(j-2) for j in (2,3,4))/sum((j-1)*.81*.1**(j-2) for j in (2,3,4))/15,3), round(sum(j*(j-1)*.81*.1**(j-2) for j in (2,3,4))/15,3))
print("ralpha",[round(sqrt(-2*log(1-a)),3) for a in (.5,.9,.95)],"gamma",round(-2*log(.01),3))
def staz(q,D=1/15,r=0.05):
    a,b,c=1.0,0.0,1.0
    for _ in range(20000):
        am=a+2*D*b+D*D*c+q*D**3/3; bm=b+D*c+q*D*D/2; cm=c+q*D
        S=am+r*r; a=am-am*am/S; b=bm-am*bm/S; c=cm-bm*bm/S
    return [[a,b],[b,c]]
for q in (0.2,0.1,0.05):
    P=staz(q);sp=lambda t:sqrt(P[0][0]+2*t*P[0][1]+t*t*P[1][1]+q*t**3/3)
    print(q,"Ppp",round(sqrt(P[0][0])*100,1),"Pvv",round(sqrt(P[1][1]),3),[round(sp(t),3) for t in (.5,1,2,3)],"r95",[round(2.448*sp(t),2) for t in (.5,1,2,3)],"r90",[round(2.146*sp(t),2) for t in (.5,1,2,3)])
    if q==0.2:
        def bis(f,a,b):
            for _ in range(60):
                m=(a+b)/2
                if f(a)*f(m)<=0:b=m
                else:a=m
            return a
        print("r95=1 a",round(bis(lambda t:2.448*sp(t)-1,.1,3),2),"r95=2 a",round(bis(lambda t:2.448*sp(t)-2,.1,3),2))
print("sigma_a",[round(sqrt(6)*0.03*f*f,1) for f in (30,15,10)],"8cm@30",round(sqrt(6)*0.08*900),"1.5cm@30",round(sqrt(6)*0.015*900,1),"nominale=3cm a",round(sqrt(0.03*fb/0.08),2))
# LS accelerazione costante su 0,5 s a 30 Hz
from fractions import Fraction as Fr
def inv3(M):
    M=[r[:]+[Fr(int(i==j)) for j in range(3)] for i,r in enumerate(M)]
    for i in range(3):
        p=M[i][i];M[i]=[x/p for x in M[i]]
        for k in range(3):
            if k!=i:
                f=M[k][i];M[k]=[x-f*y for x,y in zip(M[k],M[i])]
    return [r[3:] for r in M]
for n in (15,16):
    ts=[Fr(i,30) for i in range(n)];rows=[[Fr(1),t,t*t/2] for t in ts]
    M=[[sum(r[i]*r[j] for r in rows) for j in range(3)] for i in range(3)]
    print("LS n",n,round(sqrt(float(inv3(M)[2][2]))*0.03,2))
class binom:
    pmf=staticmethod(lambda k,n,p:comb(n,k)*p**k*(1-p)**(n-k))
    cdf=staticmethod(lambda k,n,p:sum(comb(n,i)*p**i*(1-p)**(n-i) for i in range(0,int(k)+1)))
    sf=staticmethod(lambda k,n,p:sum(comb(n,i)*p**i*(1-p)**(n-i) for i in range(int(k)+1,n+1)))
    @staticmethod
    def ppf(q,n,p):
        c=0
        for i in range(n+1):
            c+=comb(n,i)*p**i*(1-p)**(n-i)
            if c>=q:return i
print("Bin(219,.9)",round(219*.9,1),round(sqrt(219*.09),1),binom.ppf(.025,219,.9),binom.ppf(.975,219,.9),"P>=214",binom.sf(213,219,.9),"P<=174",binom.cdf(174,219,.9),"P>=207",binom.sf(206,219,.9))
print("rapporto quantili",round(sqrt(log(10)/log(2)),2),"attraversa 3m",round(3/4,2),round(3/14,2))
print("== cap.5")
for ta,tau,e,D in ((0,.150,0,1/15),(.1333,.155,0,0),(.1333,.155,0,1/15),(.1333,.155,.2,1/15),(0,.155,0,1/15)):
    T=ta+tau+D;print(round(T,3),round((0.4-e)/T,2),"2.5*T",round(2.5*T,2))
T=0.355;print("fasce",[(v,round(v*T,2)) for v in (2.5,2.0,4.5,8.0,8.3,13.9,15.4,16.7,4.0,4.8)],"scoperto",round(4.0*T-2.5*T,2))
ds=lambda v:v*(0.267+0.155+1.0)+0.95
print("vel coperta",round((3-0.95)/1.422,2),"3/0.422",round(3/0.422,1))
for n,vt,vm in (("piedi",1.4,2.5),("agv",1.0,2.0),("carrello",2.2,4.5),("corsa",3.0,8.0),("trattore",1.7,8.3),("auto urb",8.3,13.9),("rullaggio",9.0,15.4),("treno",11.0,16.7),("bici",4.3,8.3),("monop",4.2,5.6),("auto lav",2.8,8.3),("traino",1.4,4.2),("tram",5.6,13.9),("manovra",4.2,8.3),("multirotore",3.0,19.0)):
    print(n,round(ds(vt),2),round(ds(vm),2),"tip<=1.44",vt<=1.44,"max<=1.44",vm<=1.44,"tip>7.1",vt>7.1,"max>7.1",vm>7.1,"vmax>=4.8",vm>=4.8)
print("ritaglio",1-0.05/0.23,1-0.05/0.08,"1-e^-1/2",1-exp(-.5),"k95",sqrt(-2*log(.05)),"9cm",0.09/1.4,"2.6-(0.89-0.40)",2.6-0.49, "3-0.89",3-0.89,"3-1.7",3-1.7)
print("criterio 30: P(resp|0.5)",binom.cdf(23,30,.5),"P(resp|0.9)",binom.cdf(23,30,.9))
print("esaustivo",2**16,2**15, "(2^4)^4",16**4,"(2^5)^3",32**3)
