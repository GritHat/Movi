# conti_arbitro.py — conti dell'arbitro per il verdetto dell'estensione f7. Python puro, nessun dato esterno.
# Rifare: python3 -I -B conti_arbitro.py
import math
H=1.2; pitch=15.0; vfov=58.0
up=math.tan(math.radians(vfov/2-pitch)); dn=math.tan(math.radians(vfov/2+pitch))
print("PA7 tetto del campo: 1,2 + %.4f*d" % up)
for d in (1.7,1.9,2.0,2.3,3.0): print("   d=%.1f m: %.3f m" % (d, H+up*d))
print("   quota 1,8 m vista da d >= %.2f m ; quota 2,0 m da %.2f m" % ((1.8-H)/up,(2.0-H)/up))
print("   suolo visto da %.3f m ; ostacolo di 0,15 m in campo da %.3f m (e' una DISTANZA)" % (H/dn,(H-0.15)/dn))
print("   pannello che nasconde tutto cio' che gli sta dietro (cima sul raggio piu' alto): a 1,7 m %.3f, a 1,9 m %.3f, a 2,0 m %.3f" % (H+up*1.7,H+up*1.9,H+up*2.0))
for ha in (1.75,1.90):
    for dp in (1.7,1.9):
        print("   attore alto %.2f a 2,3 m, pannello a %.1f m: serve alto >= %.3f m" % (ha,dp,min(H+up*dp, H+(ha-H)*dp/2.3)))
print()
print("PA6 occlusione completa: pannello largo L a dp, attore largo 0,45 m a 2,3 m, di traverso")
for L in (1.0,2.0):
    for dp in (1.7,1.8,1.9):
        om=L*2.3/dp; tr=om-0.45
        print("   L=%.1f dp=%.1f: ombra %.2f m, tratto del tutto nascosto %.2f m: %.2f s a 1,4 m/s, %.2f s a 1,0, %.2f s a 0,5" % (L,dp,om,tr,tr/1.4,tr/1.0,tr/0.5))
print("   campo orizzontale (87 gradi) a 1,8 m: %.2f m ; a 2,3 m: %.2f m" % (2*1.8*math.tan(math.radians(43.5)),2*2.3*math.tan(math.radians(43.5))))
for dp in (1.8,):
    om=2.0*2.3/dp; lato=(2*2.3*math.tan(math.radians(43.5))-om)/2
    print("   L=2,0 a 1,8 m, centrato: resta in vista %.2f m per lato a 2,3 m (meno il corpo: %.2f m) = %.2f s a 1,0 m/s prima dell'ombra" % (lato,lato-0.45,(lato-0.45)/1.0))
print()
print("PA5 ore (stime altrui, non verificate): blocchi del nucleo B1..B9 = 3,6,6,5,9,4,3,6,12")
B=dict(B1=3,B2=6,B3=6,B4=5,B5=9,B6=4,B7=3,B8=6,B9=12)
print("   somma %d ; catena B1..B5,B7,B8 %d ; senza B1 %d ; nucleo senza B6 %d" % (sum(B.values()), sum(B[k] for k in "B1 B2 B3 B4 B5 B7 B8".split()), sum(B[k] for k in "B2 B3 B4 B5 B7 B8".split()), sum(B.values())-4))
acc=2+40/60.0   # accettazione H0-H13, due persone
for n in (5,4,3):
    cap=14*n
    for f7 in (8.0,10.5):
        # conto semplice della decisione: capienza - (nucleo senza etichetta) - aggiunte f7
        semplice=cap-50-f7
        # conto dell'avversario: tutto prima dell'accettazione, che sta dentro le 14 ore
        t_int=14-acc; capi=n*t_int; resto_b9=12-2*acc
        avv=capi-3-resto_b9-35-f7
        # variante [arb.]: registro e testi (4-5 ore delle aggiunte f7) fatti dalle n-2 persone libere durante l'accettazione
        sposta=min(5.0 if f7>10 else 4.0, (n-2)*acc)
        var=avv+sposta
        print("   %d persone, f7 %.1f: capienza %d ; conto semplice (decisione) %.1f ; con l'accettazione dentro (avversario) %.1f ; con registro e testi durante l'accettazione [arb.] %.1f" % (n,f7,cap,semplice,avv,var))
    print("      rami paralleli necessari per stare in %.2f ore d'orologio con 35 ore in fila: %.2f" % (t_int,35/t_int))
# accettazione ridotta alla prima ora (H0-H6), due persone
for n in (5,4,3):
    for f7 in (8.0,10.5):
        t_int=13.0; capi=n*t_int; resto_b9=12-2*1.0
        print("   accettazione ridotta a 1 ora, %d persone, f7 %.1f: restano %.1f ore-persona" % (n,f7,capi-3-resto_b9-35-f7))
print()
print("Probabilita' che i 9 pixel del 3x3 siano tutti validi con buchi sparsi indipendenti: 5 %%: %.3f ; 10 %%: %.3f ; 30 %%: %.3f" % (0.95**9,0.9**9,0.7**9))
print("Dieci esiti buoni su dieci: limite superiore al 95 %% del tasso di fallimento %.3f ; per il 5 %% servono %d prove" % (1-0.05**(1/10), math.ceil(math.log(0.05)/math.log(0.95))))
