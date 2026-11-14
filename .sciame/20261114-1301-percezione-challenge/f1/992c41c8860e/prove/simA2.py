import random, math
rnd=random.Random(1)
dt=0.1; sig=0.05; N=6000
def truth(n):
    sp=max(0.3,rnd.gauss(1.3,0.3)); th=rnd.uniform(0,2*math.pi); x=y=0.0; st=False; out=[]
    for k in range(n):
        if rnd.random()<0.1*dt: st=not st
        if rnd.random()<0.2*dt: th+=rnd.uniform(-math.pi/2,math.pi/2)
        if not st: x+=sp*math.cos(th)*dt; y+=sp*math.sin(th)*dt
        out.append((x,y))
    return out
def pred(m,P,q):
    p,v=m; a,b,c=P  # P=[[a,b],[b,c]]
    return (p+v*dt,v),(a+2*b*dt+c*dt*dt+q*dt**3/3, b+c*dt+q*dt*dt/2, c+q*dt)
def upd(m,P,z):
    p,v=m; a,b,c=P; S=a+sig*sig; k1=a/S; k2=b/S; r=z-p
    return (p+k1*r,v+k2*r),(a-k1*a,b-k1*b,c-k2*b)
print("q T RMS r95vero cop99 d2medio(atteso 2)")
for q in (0.5,):
    for T in (1.0,1.2,1.3,1.5):
        nv=30; no=int(round(T/dt)); errs=[]; ins=0; d2s=0
        for _ in range(N):
            tr=truth(nv+no+1)
            ms=[(tr[0][i]+rnd.gauss(0,sig),0.0) for i in (0,1)]; P=(sig*sig,0.0,4.0)
            for k in range(1,nv):
                for i in (0,1): ms[i],Pn=pred(ms[i],P,q); ms[i],Pu=upd(ms[i],Pn,tr[k][i]+rnd.gauss(0,sig))
                P=Pu
            for k in range(no+1):
                for i in (0,1): ms[i],Pn=pred(ms[i],P,q)
                P=Pn
            t=tr[nv+no]; S=P[0]+sig*sig
            d2=sum((t[i]+rnd.gauss(0,sig)-ms[i][0])**2 for i in (0,1))/S
            errs.append(math.hypot(t[0]-ms[0][0],t[1]-ms[1][0])); ins+=d2<9.21; d2s+=d2
        errs.sort()
        print(q,T,round(math.sqrt(sum(e*e for e in errs)/N),2),round(errs[int(.95*N)],2),round(ins/N,3),round(d2s/N,2), "sigma_pos_dichiarata",round(math.sqrt(P[0]),2))
