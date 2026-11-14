# Sostituti in puro Python di scipy.stats (scipy non e' installato; niente rete): binomiale esatta, Beta a parametri interi, normale.
from math import comb, lgamma, log, exp
from statistics import NormalDist
class _N:
    def ppf(self,p): return NormalDist().inv_cdf(p)
norm=_N()
def _pmf(i,n,p):
    if p<=0: return 1.0 if i==0 else 0.0
    if p>=1: return 1.0 if i==n else 0.0
    return exp(lgamma(n+1)-lgamma(i+1)-lgamma(n-i+1)+i*log(p)+(n-i)*log(1-p))
class _B:
    def cdf(self,k,n,p):
        if k<0: return 0.0
        if k>=n: return 1.0
        return min(1.0,sum(_pmf(i,n,p) for i in range(0,int(k)+1)))
    def sf(self,k,n,p):
        if k<0: return 1.0
        if k>=n: return 0.0
        return min(1.0,sum(_pmf(i,n,p) for i in range(int(k)+1,n+1)))
binom=_B()
class _Beta:
    # Beta(a,b) con a,b interi: cdf(x)=P(Bin(a+b-1,x)>=a)
    def cdf(self,x,a,b): return binom.sf(a-1,a+b-1,x)
    def sf(self,x,a,b): return 1-self.cdf(x,a,b)
    def ppf(self,q,a,b):
        lo,hi=0.0,1.0
        for _ in range(60):
            m=(lo+hi)/2
            if self.cdf(m,a,b)<q: lo=m
            else: hi=m
        return (lo+hi)/2
beta=_Beta()
