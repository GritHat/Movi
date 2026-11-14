# stampa il nucleo veloce (0-3) meno occupato, guardando anche il gemello SMT (+12); campione di 0,4 s
import time
def snap():
    d={}
    for l in open('/proc/stat'):
        if l.startswith('cpu') and l[3].isdigit():
            p=l.split(); v=list(map(int,p[1:])); d[int(p[0][3:])]=(sum(v), v[3]+v[4])
    return d
a=snap(); time.sleep(0.4); b=snap()
def busy(c):
    t=b[c][0]-a[c][0]; i=b[c][1]-a[c][1]; return 1-i/max(t,1)
print(min(range(4), key=lambda c: busy(c)+busy(c+12)))
