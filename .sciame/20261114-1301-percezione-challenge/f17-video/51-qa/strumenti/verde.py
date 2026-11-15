"""QA Q11 (indipendente dallo script del montaggio): legge il video a 1 fps come rgb24 da stdin (1920x1080)
e conta per fotogramma i pixel con tinta 90-160 gradi, saturazione > 0,30, valore > 0,15.
Se il conteggio totale di un fotogramma è <= 50, nessuna area connessa può superare 50 px."""
import sys, numpy as np
W,H=1920,1080; n=0; out=[]
while True:
    b=sys.stdin.buffer.read(W*H*3)
    if len(b)<W*H*3: break
    a=np.frombuffer(b,np.uint8).reshape(H,W,3).astype(np.float32)/255
    mx=a.max(2); mn=a.min(2); d=mx-mn; s=np.where(mx>0,d/np.maximum(mx,1e-6),0)
    r,g,bb=a[...,0],a[...,1],a[...,2]
    h=np.where(mx==g,60*((bb-r)/np.maximum(d,1e-6))+120,-1)
    m=(h>=90)&(h<=160)&(s>0.30)&(mx>0.15)&(d>0)
    out.append((int(m.sum()),n)); n+=1
out.sort(reverse=True); print('fotogrammi',n,'peggiori (pixel, secondo):',out[:5]); print('fotogrammi con > 50 px:',sum(1 for o in out if o[0]>50))
