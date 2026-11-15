import sys,glob,numpy as np
from PIL import Image
n=0
for p in sorted(glob.glob(sys.argv[1]+'/*.png')):
    a=np.asarray(Image.open(p).convert('RGB')).astype(int)
    R,G,B=a[...,0],a[...,1],a[...,2]
    m=(G>R+40)&(G>B+40)&(G>90)
    if m.sum()>20: n+=1; print('VERDE',p,int(m.sum()))
print('fotogrammi con verde:',n)
