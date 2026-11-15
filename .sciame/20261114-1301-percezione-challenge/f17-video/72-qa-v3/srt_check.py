import re,sys
s=open(sys.argv[1],encoding='utf-8').read()
bl=[b for b in s.strip().split('\n\n')]
cues=[];prev=0;err=[]
def ts(x):
    h,m,r=x.split(':');sec,ms=r.split(',');return int(h)*3600+int(m)*60+int(sec)+int(ms)/1000
for k,b in enumerate(bl,1):
    L=b.split('\n')
    if L[0].strip()!=str(k): err.append(('indice',k,L[0]))
    a,c=[ts(x.strip()) for x in L[1].split('-->')]
    if a<prev or c<=a: err.append(('tempo',k))
    prev=c; cues.append((a,c,' '.join(L[2:])))
    cps=len(' '.join(L[2:]))/(c-a)
    if cps>21 or (c-a)<1.0: err.append(('lettura',k,round(cps,1),round(c-a,2)))
print('cue',len(cues),'fine ultima',cues[-1][1],'errori',err)
import os
ok=0;ko=[]
for i in range(1,88):
    t=(i-1)*2+1
    act=[c for c in cues if c[0]<=t<=c[1]]
    o=open(f'{sys.argv[2]}/f_{i:03d}.txt',encoding='utf-8',errors='ignore').read().replace('\n',' ')
    o=re.sub(r'\s+',' ',o)
    if not act: continue
    w=act[0][2].split()[:3]
    if ' '.join(w) in o: ok+=1
    else: ko.append((t,' '.join(w)))
print('fotogrammi con sottotitolo atteso trovato',ok,'non trovato',ko)
