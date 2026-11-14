# Ricalcolo indipendente degli intervalli del capitolo 6 (scipy). Nessun dato del progetto: solo k, N letti dal .tex.
from math import sqrt, ceil
from mini import norm, beta, binom
def wil(k,n,z=1.959964):
    p=k/n; c=(p+z*z/(2*n))/(1+z*z/n); h=z*sqrt(p*(1-p)/n+z*z/(4*n*n))/(1+z*z/n); return c-h,c+h
def cp(k,n,a=0.05):
    lo=0 if k==0 else beta.ppf(a/2,k,n-k+1); hi=1 if k==n else beta.ppf(1-a/2,k+1,n-k); return lo,hi
def zm(m): return norm.ppf(1-0.05/(2*m))
def P(name,k,n,z=1.959964):
    l,u=wil(k,n,z); print(f"{name}: {k}/{n}={k/n:.4f} Wilson[{l:.4f};{u:.4f}] CP[{cp(k,n)[0]:.4f};{cp(k,n)[1]:.4f}]")
print("== esempio Wilson 826/879"); P("es",826,879)
p=826/879; z=1.96; print(" centro",(p+z*z/(2*879))/(1+z*z/879)," z2/2N",z*z/(2*879)," 1+z2/N",1+z*z/879, " radice", sqrt(p*(1-p)/879+z*z/(4*879**2)), " semi", z*sqrt(p*(1-p)/879+z*z/(4*879**2))/(1+z*z/879))
print("== zero su N")
for N in (90,131,400,24835,140,6000,13638,5600,5597,14400,264,10,60,8,115,2400,20000,70400,217861):
    print(N," esatto1coda %.5f%%"%(100*(1-0.05**(1/N)))," Wilson %.5f%%"%(100*3.8415/(N+3.8415)), " 3/N %.5f%%"%(300/N))
print("400/400 inf Wilson",400/(400+3.8415)," esatto 1 coda",0.05**(1/400))
print("== z_m",zm(12),zm(45),zm(60),zm(5),zm(15))
print("90/100 m=1",wil(90,100)," m=12",wil(90,100,zm(12)))
print("== tab numerosita")
for k,n in ((9,10),(27,30),(30,30),(46,50),(90,100)): P("",k,n)
def primo_stabile(p0,p1,alpha=0.05,pot=0.80,nmax=420):
    ok=[]
    for n in range(5,nmax):
        if p1<p0:
            # rifiuta se k<=c, livello P(K<=c|p0)<=alpha
            c=-1
            while binom.cdf(c+1,n,p0)<=alpha: c+=1
            pw=binom.cdf(c,n,p1) if c>=0 else 0
        else:
            c=n+1
            while c-1>=0 and binom.sf(c-2,n,p0)<=alpha: c-=1
            pw=binom.sf(c-1,n,p1) if c<=n else 0
        ok.append((n,c,pw))
    first=next(x for x in ok if x[2]>=pot)
    stab=None
    for i in range(len(ok)-1,-1,-1):
        if ok[i][2]<pot: stab=ok[i+1]; break
    return first,stab
for a,b in ((.9,.8),(.8,.9),(.9,.85),(.85,.9),(.9,.95)):
    print(a,"vs",b,primo_stabile(a,b))
# n=30, H0 0.9 vs 0.8
c=-1
while binom.cdf(c+1,30,0.9)<=0.05: c+=1
print("n=30 soglia k<=",c," potenza",binom.cdf(c,30,0.8))
print("30/30 con p=0.9:",0.9**30)
print("almeno 9 su 10: p=.8",binom.sf(8,10,.8)," p=.9",binom.sf(8,10,.9))
# 82 su 94 esclude 0.80
print("94: P(K>=82|.8)",binom.sf(81,94,.8)," potenza a .9",binom.sf(81,94,.9))
print("296: P(K>=262|.85)",binom.sf(261,296,.85)," potenza .9",binom.sf(261,296,.9))
for k in range(90,101):
    if wil(k,100)[0]>=0.90: print("primo k su 100 con Wilson inf>=0.90:",k,wil(k,100)[0]); break
print("potenza 96/100: .95",binom.sf(95,100,.95)," .97",binom.sf(95,100,.97))
print("neff 40/(1+9*.2)",40/(1+9*.2))
print("== taratura Beta")
for nc in (30,100):
    k=ceil(0.9*(nc+1)); print(nc,k,beta.ppf(0.05,k,nc+1-k))
okn=[]
for nc in range(5,400):
    k=ceil(0.9*(nc+1))
    if k>nc: okn.append((nc,False)); continue
    okn.append((nc, beta.sf(0.85,k,nc+1-k)>=0.95))
print("primo nc:",next(n for n,o in okn if o)," stabile da:", max(n for n,o in okn if not o)+1, " primo k<=nc:", next(nc for nc in range(1,50) if ceil(0.9*(nc+1))<=nc))
print("== osservazione nonvale"); P("",323,342);P("",283,339);P("",226,282)
print("== tabelle")
for nm,k,n in (("fuoriPres passaggi",0,24835),("chiusa 928",928,23402),("chiusa 24",24,23402),("1/5704",1,5704),("17/5704",17,5704),("0/14400",0,14400),("13/4800",13,4800),("0/131",0,131),("0/300 cond",0,300),("15/90",15,90),("1958/1958",1958,1958),("1991/2000",1991,2000),("1999/2000",1999,2000),("0/13638",0,13638),("0/5600",0,5600),("0/5597",0,5597),("0/24835",0,24835),("0/6000",0,6000),
 ("826/879",826,879),("461/513",461,513),("461/480",461,480),("437/472",437,472),("711/774",711,774),("1222/1265",1222,1265),("666/698",666,698),("2125/2279",2125,2279),("1754/1922",1754,1922),("942/1045",942,1045),("1257/1388",1257,1388),("845/984",845,984),
 ("174/221",174,221),("15/141",15,141),("21/134",21,134),("14/54",14,54),("36/46",36,46),("83/90",83,90),("1216/1244",1216,1244),
 ("400/400",400,400),("10711/10757",10711,10757),("9228/9240",9228,9240),("6772/6967",6772,6967),("0/90",0,90),("176/180",176,180),("174/180",174,180),("0/10",0,10),("1/10",1,10),("2/10",2,10),("6/10",6,10),("2400/2400",2400,2400),("1457/3029",1457,3029),("2567/3609",2567,3609),("2393/3540",2393,3540),("3027/3041",3027,3041),("3493/3616",3493,3616),("3239/3546",3239,3546),("12/12",12,12),("19/20",19,20),("0/264",0,264),("27/30",27,30),
 ("2000/2000",2000,2000),("0.8585*2000",1717,2000),("0.266*2000",532,2000),("0/400",0,400),("79/90",79,90),("0/60",0,60),("45/60",45,60),("115/115",115,115),("0/8",0,8),("214/219",214,219),("219/219",219,219),("0.795*219",174,219),("0.534*219",117,219),("0/140",0,140),("140/140",140,140),("10/10",10,10)):
    P(nm,k,n)
print("z45 su 826/879",wil(826,879,zm(45))," z15:",wil(1222,1265,zm(15)),wil(666,698,zm(15)),wil(2125,2279,zm(15)),wil(1754,1922,zm(15)),"z5 942/1045",wil(942,1045,zm(5)))
print("limite 1 coda 0/20000:",1-0.05**(1/20000))
print("== aggiunte")
for m in (15,30): print("z",m,zm(m),[round(wil(k,n,zm(m))[0],4) for k,n in ((1222,1265),(666,698),(2125,2279),(1754,1922),(942,1045))])
for k,n in ((1991,2000),(461,513),(1222,1265),(46,50),(30,30),(4,9152),(1,5704),(214,219)): print(k,n,["%.5f"%x for x in wil(k,n)])
print("z60 a 5 decimali",zm(60))
