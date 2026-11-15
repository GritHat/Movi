# Costruisce progetto_v4c/index.html da progetto_v4b/index.html (letto soltanto): aggiunge quattro idee ridisegnate
# (cono con ombra, tre risposte, curva della confidenza, griglia dei passaggi). Nessun file del pacchetto esterno è copiato.
import os, re
q=os.path.dirname(os.path.abspath(__file__))
s=open(os.path.join(q,'..','progetto_v4b','index.html')).read()
def r(a,b,n=1):
    global s
    assert s.count(a)==n,(a,s.count(a)); s=s.replace(a,b)
r('data-duration="80"','data-duration="86"',2)
r('const D=80,TH=10,TC=13.5,TZ=17,TP=22,S0=24,ST=4.3,TW=50,TS=54,TR=58,TI=63,TS1=69,TS2=71.8,TS3=74.6,TE=77.4;',
  'const D=86,TK=10,TH=16,TC=19.5,TZ=23,TP=28,S0=30,ST=4.3,TW=56,TS=60,TR=64,TI=69,TS1=75,TS2=77.8,TS3=80.6,TE=83.4;')
# 1. cono del sensore con l'ombra (TK-TH)
K=r'''// ---------- K cono del sensore con l'ombra (TK-TH)
H+=`<g id="gK"><defs><pattern id="hatch" width="18" height="18" patternTransform="rotate(45)" patternUnits="userSpaceOnUse"><rect width="18" height="18" fill="#FFEBD6"/><rect width="7" height="18" fill="#FFC993"/></pattern></defs>
<rect width="1920" height="1080" fill="#F2F7FD"/>${head("kHead",120,140,"Where it has not looked,","MoVi never says clear.",72)}
<g id="kCone"><path d="M300,620 L1760,150 L1760,1090 Z" fill="${BLUE}" fill-opacity=".12"/><path d="M300,620 L1760,150 M300,620 L1760,1090" stroke="${BLUE}" stroke-width="4" stroke-dasharray="18 12" fill="none"/></g>
<path id="kSh" d="M800,500 L1760,236 L1760,912 L800,720 Z" fill="url(#hatch)" stroke="${AMB}" stroke-width="4"/>
<g id="kB" transform="translate(900,610)"><rect x="-100" y="-110" width="200" height="220" rx="14" fill="#9FB3C8" filter="url(#sh)"/><rect x="-70" y="-80" width="140" height="160" rx="8" fill="#B9C8D8"/></g>
<g transform="translate(300,620)">${drone(BLUE)}<text y="70" text-anchor="middle" font-size="26" font-weight="800" fill="${INK}" letter-spacing="2">SENSOR</text></g>
${chip("kSeen",560,330,"SEEN",TEAL,150)}
<g id="kTag" transform="translate(1090,580)"><rect width="610" height="64" rx="14" fill="#fff" filter="url(#sh)"/><text x="305" y="43" text-anchor="middle" font-size="28" font-weight="700" fill="${INK}">possible presence · not seen for 6.8 s</text></g>
</g>`;
'''
r('// ---------- H scena eroe',K+'// ---------- H scena eroe')
# 2. le tre risposte: scheda 4 «State map»
a=s.index('const g4='); b=s.index('\n',a)
s=s[:a]+r'''const g4=[[TEAL,["I see it"],""],[BLUE,["I don’t see it,","but it is here"],"d"],["#8D99AB",["I don’t know"],""]].map((a,i)=>`<rect x="-215" y="${-125+i*105}" width="76" height="60" rx="12" fill="${a[0]}" ${a[2]?`fill-opacity=".25" stroke="${BLUE}" stroke-width="4" stroke-dasharray="10 7"`:""}/>`+a[1].map((t,j)=>`<text x="-118" y="${-85+i*105+(a[1].length>1?j*36-18:0)}" font-size="30" font-weight="700" fill="${INK}">${t}</text>`).join("")).join("");'''+s[b:]
# 3. curva della confidenza nella soggettiva (scheda 3)
r('${tagS("t1",1050,330',r'''<g id="pCurve" transform="translate(570,662)"><rect width="400" height="190" rx="22" fill="#fff" filter="url(#sh)"/><path d="M30,24 L30,112 L370,112" fill="none" stroke="#C9D6E4" stroke-width="3" stroke-linecap="round"/><path id="pCv" d="M30,34 C130,36 170,100 370,106" fill="none" stroke="${BLUE}" stroke-width="6" stroke-linecap="round"/><text x="30" y="142" font-size="19" font-weight="600" fill="${GREY}">C(τ) = 1 − e<tspan dy="-8" font-size="14">−r²/2σ²(τ)</tspan></text><text x="30" y="172" font-size="21" font-weight="700" fill="${BLUE}">a proven formula, not a guess</text></g>
${tagS("t1",1050,330''')
# 4. griglia dei passaggi nella scheda «60/60» delle prove
r('${cap(TI+.4,TI+5.6,',r'''<g id="kg" transform="translate(1016,712)">${Array.from({length:60},(_,i)=>`<rect x="${(i%20)*16}" y="${Math.floor(i/20)*16}" width="12" height="12" rx="3" fill="${AMB}"/>`).join("")}</g>
<text id="kgT" x="1175" y="822" text-anchor="middle" font-size="26" font-weight="700" fill="${INK}">each square is one simulated run</text>
${cap(TI+.4,TI+5.6,''')
# linea del tempo
r('scene("#gA",0,TH);','scene("#gA",0,TH);scene("#gK",TK,TH);')
r('// R\n',r'''// K
fin("#kHead",TK+.3); fin("#kCone",TK+.7); pop("#kSeen",TK+1.4); pop("#kB",TK+1.8); fin("#kSh",TK+2.5,.9); pop("#kTag",TK+3.2);
// curva e griglia
fin("#pCurve",c[2]+.8); hide("#pCurve",c[3]-.3);
tl.fromTo("#kg rect",{autoAlpha:0},{autoAlpha:1,duration:.2,stagger:.03},TI+2); fin("#kgT",TI+2.4);
// R
''')
open(os.path.join(q,'index.html'),'w').write(s)
print('ok')
