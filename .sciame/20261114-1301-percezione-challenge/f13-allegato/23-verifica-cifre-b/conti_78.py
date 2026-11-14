# Conti in forma chiusa dei capitoli 7 e 8 e dell'appendice B, rifatti dal solo testo (nessun file del progetto letto).
from math import tan, radians, sqrt, ceil, degrees
from statistics import NormalDist
P=print
P("cap.7 voxel", 60*40*30, 120*80*60, 4*72000, 4*576000, "blocchi", ceil(60/8)*ceil(40/8)*ceil(30/8), ceil(120/8)*ceil(80/8)*ceil(60/8))
P("passi", 60+40+30-2, 120+80+60-2, " N_c", 87*30)
V=4/3*tan(radians(43.5))*tan(radians(29))*27; P("piramide", round(tan(radians(43.5)),4), round(tan(radians(29)),4), round(V,2), round(100*V/72,1), round(72/V,2))
P("risparmio", 2304000-763904, " hash/densa %", round(100*763904/2304000,1), round(100*241664/288000,1), " octree %", round(100*2691008/2304000,1), round(100*377856/288000,1))
P("f=320/tan43.5", round(320/tan(radians(43.5)),1), " k<=", 0.05*337/6, 0.10*337/6, " z fascia alta", round(0.8/tan(radians(14)),2))
P("sigma_a", round(sqrt(6)*0.03*225,2), " 49.1/66.7", round(100*49.1/66.667,1), " 5.44/66.7", round(100*5.44/66.667,1), " 636us/108000 ns", round(636e3/108000,2), " 88.9ms/33.3M ns", round(88.9e6/33.3e6,2))
P("retta nT=152", round(0.33+0.30*152,1), "+quad", round(0.33+0.30*152+1.7e-4*152**2,1), " 320 cicli/15", round(320/15,1), " 16e6*8 MB", 400*400*100*8/1e6, " 3/4", 3/4, " 4/15", round(4/15,3), " zona 2 m", round(2*tan(radians(7.5)),3))
tc,tau,C=0.267,0.155,0.95
for nome,Tr in (("stazione",1.0),("UGV",0.3),("remoto",1.8),("multirotore",0.3),("non vedente",1.5)):
    P("cap.8", nome, "T_ant", round(tc+tau+Tr,3), "v coperta fermo", round((3-C)/(tc+tau+Tr),3))
def ds(v,ve,af,Tr): return (v+ve)*(tc+tau+Tr)+ve*ve/(2*af)+v*ve/af+C
P("d_serve(0): UGV", round(ds(0,1.0,1.5,0.3),3), " multirotore", round(ds(0,3.0,3.0,0.3),3), " non vedente", round(ds(0,1.0,1.0,1.5),3))
t=tc+tau+0.3; P("UGV in moto, v coperta", round((3-C-1.0*t-1/(2*1.5))/(t+1/1.5),3), " margine a 1,4 m/s fermo Tr=1", round(3-(1.4*(tc+tau+1.0)+C),3))
P("fascia", round(0.40/0.355,3), round(0.20/0.355,3), " latenza", 16.7+95+22+21.3, 1024/48, " intervallo", 155-16.7, 155+16.7, " p95", round(155-16.65+0.95*33.3,1), " con 71", 155-95+71, " 0,288*2,5", 0.288*2.5)
N=NormalDist(); r=sqrt(2/3)
P("moto: delta/sigma al 10% e 1%", round((5-N.inv_cdf(0.90))*r,3), round((5-N.inv_cdf(0.99))*r,3), " W", round(13/15,3), " 0,88/W", round(0.88/(13/15),2), " 0,63/W", round(0.63/(13/15),2))
P("posa: (0,10-0,07)/rho gradi a 2,55 / 2,5 / 3 m", round(degrees(0.03/2.55),2), round(degrees(0.03/2.5),2), round(degrees(0.03/3),2), " 0,05/0,133", round(0.05/0.1333,3))
P("app.B: z2", round(1.959964**2,4), " 6000:", round(1e4*3.8415/(6000+3.8415),2), "su 10000")
