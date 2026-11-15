# Costruisce progetto_v4d/index.html (video completo, italiano) da progetto_v4c/index.html (letto soltanto) e dai wav di voce/.
# I tempi delle scene vengono dalle durate misurate della voce. Scrive anche tempi.json, i sottotitoli .srt e il copione.
# Uso: python3 costruisci_v4d.py [cartella_consegna]
import json, os, re, subprocess, sys
q = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else q
s = open(os.path.join(q, '..', 'progetto_v4c', 'index.html')).read()
clips = json.load(open(os.path.join(q, 'voce', 'clip.json')))
def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)
RIT = 0.25            # ritardo della voce rispetto all'inizio della clip
cue = {}; t = 0.0; righe = []; wavs = {}
for cid, mn, testo in clips:
    tk = testo
    for x, y in {"MoVi": "Movi", "SDMs": "esse di emme esse", "«": "", "»": "", "’": "'"}.items(): tk = tk.replace(x, y)
    base = cid if open(os.path.join(q, 'voce', cid + '_kokoro.txt')).read() == tk + "\n" else cid + '_v2'
    wavs[cid] = os.path.join(q, 'voce', base + '.wav'); d = dur(wavs[cid])
    cue[cid] = round(t, 2); righe.append([cid, round(t, 2), round(d, 2), testo])
    t += max(mn, d + (1.6 if cid == 'E' else 0.3))
D = round(max(t, 167.0), 2)
assert D <= 174.0, ("troppo lungo", D)
print("durata", D)
def chunks(text, n=54):
    out = []
    for sent in re.findall(r'[^.?!:;]+[.?!:;]?', text):
        sent = sent.strip()
        while len(sent) > n:
            parti = -(-len(sent) // n); meta = len(sent) / parti   # taglio vicino a una frazione intera, meglio su una virgola
            cand = [m.start() + 1 for m in re.finditer(', ', sent) if abs(m.start() + 1 - meta) <= 10 and m.start() + 1 <= n]
            if not cand: cand = [m.start() for m in re.finditer(' ', sent) if m.start() <= n]
            k = min(cand, key=lambda x: abs(x - meta))
            out.append(sent[:k].strip()); sent = sent[k:].strip()
        if sent: out.append(sent)
    m = []
    for c in out:
        if m and len(m[-1]) + len(c) + 1 <= n and (len(c) < 16 or len(m[-1]) < 16): m[-1] += ' ' + c
        else: m.append(c)
    return m
subs = []
for cid, t0, d, testo in righe:
    cs = chunks(testo); tot = sum(len(c) + 3 for c in cs); a = t0 + RIT
    for c in cs:
        b = a + d * (len(c) + 3) / tot; subs.append([round(a, 2), round(b - 0.04, 2), c]); a = b
json.dump({"durata": D, "ritardo_voce": RIT, "wav": wavs, "clip": righe, "sottotitoli": subs}, open(os.path.join(q, 'tempi.json'), 'w'), ensure_ascii=False, indent=1)
def ts(x): h = int(x // 3600); m = int(x % 3600 // 60); return "%02d:%02d:%06.3f" % (h, m, x % 60)
srt = "".join("%d\n%s --> %s\n%s\n\n" % (i + 1, ts(a).replace('.', ','), ts(b).replace('.', ','), c) for i, (a, b, c) in enumerate(subs))
open(os.path.join(OUT, 'MoVi_pitch_IT_v4.srt'), 'w').write(srt)

def r(a, b, n=1):
    global s
    assert s.count(a) == n, (a, s.count(a)); s = s.replace(a, b)
def rblock(a, b, new):
    global s
    i = s.index(a); j = s.index(b, i); s = s[:i] + new + s[j:]
C = cue
r('data-duration="86"', 'data-duration="%s"' % D, 2); r('data-fps="24"', 'data-fps="30"')
r('const D=86,TK=10,TH=16,TC=19.5,TZ=23,TP=28,S0=30,ST=4.3,TW=56,TS=60,TR=64,TI=69,TS1=75,TS2=77.8,TS3=80.6,TE=83.4;',
  'const D=%s,T2=%s,TK=%s,TF=%s,TF2=%s,TF3=%s,TH=%s,TC=%s,TZ=%s,TP=%s,S0=0,ST=0,TW=%s,TS=%s,TR=%s,TI=%s,TE=%s;\nconst TU=%s;\nconst TS2=TU[0],TS1=TU[3],TS3=TU[5];\nconst SUBS=%s;'
  % (D, C['A2'], C['K'], C['F1'], C['F2'], C['F3'], C['H1'], C['H2'], C['Z'], C['P0'], C['W'], C['S'], C['R'], C['I'], C['E'],
     json.dumps([C['U%d' % i] for i in range(1, 9)]), json.dumps(subs, ensure_ascii=False)))
r('const c=[0,1,2,3,4,5,6].map(i=>S0+i*ST);', 'const c=%s;' % json.dumps([C['P%d' % i] for i in range(1, 7)] + [C['W']]))
r('const cap=(t0,t1,txt)=>{caps.push([t0,t1]);return', 'const cap=(t0,t1,txt)=>{return "";caps.push([t0,t1]);return')
r('"Un satellite che trova","il frammento pericoloso nella nube."', '"Un satellite che trova","il frammento fra i detriti."')
r('tagS("t2",600,232,320,"NON VISTO · UNA REGIONE"', 'tagS("t2",555,232,410,"NON VISTO · UNA REGIONE"')
r('<g id="pCurve" transform="translate(570,662)">', '<g id="pCurve" transform="translate(650,590) scale(1.5)">')

# ---- architettura più grande e centrata
rblock('// ---------- R architettura', '// ---------- I infografica', r'''// ---------- R architettura (TR-TI)
const blk=(i,t1,t2,sub,cc)=>`<g id="ab${i}" transform="translate(${60+i*366},390)"><rect width="336" height="300" rx="32" fill="#fff" filter="url(#sh)"/><rect width="336" height="16" rx="8" fill="${cc}"/><text x="168" y="${t2?118:142}" text-anchor="middle" font-size="42" font-weight="800" fill="${INK}">${t1}</text>${t2?`<text x="168" y="166" text-anchor="middle" font-size="42" font-weight="800" fill="${INK}">${t2}</text>`:""}<text x="168" y="236" text-anchor="middle" font-size="27" font-weight="600" fill="${GREY}">${sub}</text></g>`+(i<4?`<path id="aa${i}" d="M${60+i*366+340},540 l22,0 m-10,-10 l10,10 l-10,10" stroke="${BLUE}" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`:"");
H+=`<g id="gR"><rect width="1920" height="1080" fill="#F7FAFE"/>${head("rHead",120,150,"Come funziona:","una catena, cinque strati.",72)}
${blk(0,"Sensori","","radar · camera · IR",BLUE)}${blk(1,"Fusione","","un solo quadro",TEAL)}${blk(2,"Stimatore","a più modelli","IMM Kalman",BLUE)}${blk(3,"Mappa a stati","","tre stati",TEAL)}${blk(4,"Avviso","","al veicolo, subito",AMB)}
${pill("rHw",600,780,720,"Pronto per hardware dedicato, per progetto",TEAL)}</g>`;
''')

# ---- scene nuove: caso 1 (volo veloce) e cinque casi d'uso
NEW = r'''// ---------- F caso 1: volo ad alta velocità (TF-TH)
const badge=(id,x,y)=>`<g id="${id}" transform="translate(${x},${y})"><circle r="40" fill="${AMB}"/><text y="18" text-anchor="middle" font-size="54" font-weight="800" fill="#fff">!</text></g>`;
const lanes=`<g fill="#fff">${[0,1,2,3,4,5,6,7].map(i=>`<rect x="${60+i*250}" y="864" width="130" height="12" rx="6"/>`).join("")}</g>`;
H+=`<g id="gF"><rect width="1920" height="1080" fill="url(#sky)"/>${cloud("fc1",1500,900,0.8)}${cloud("fc2",330,930,0.6)}
<g id="fSpd">${[0,1,2,3,4,5].map(i=>`<rect x="${i*330}" y="${250+((i*173)%520)}" width="${200+i*20}" height="6" rx="3" fill="#fff" opacity=".9"/>`).join("")}</g>
${head("fHead",120,150,"Primo caso: volo veloce.","Un’avaria improvvisa.",72)}
<g transform="translate(560,610)">${[[0,0,70],[-70,-14,80],[-150,-30,92],[-240,-40,100],[-330,-60,108],[-420,-70,112],[-110,30,70],[-290,10,90],[-470,-20,100]].map((p,i)=>`<circle class="fsk" cx="${p[0]}" cy="${p[1]}" r="${p[2]}" fill="${i%3?'#8D99AB':'#6B778A'}"/>`).join("")}</g>
<g id="fDeb">${[[-260,150,160],[-380,-190,-200],[-120,230,90],[-520,60,240]].map(p=>`<path class="fdb" data-x="${600+p[0]}" data-y="${610+p[1]}" data-r="${p[2]}" d="M-14,-8 L12,-12 L16,6 L-6,13 Z" fill="${INK}"/>`).join("")}</g>
<g id="fJet" transform="translate(760,540) scale(2.3)">${jet(INK)}</g>
<g transform="translate(610,610)">${[[0,0,62,'#FF6A1A'],[-50,-10,52,'#FFB020'],[30,16,40,'#FFB020'],[-20,26,44,'#FF6A1A']].map(p=>`<circle class="ffr" cx="${p[0]}" cy="${p[1]}" r="${p[2]}" fill="${p[3]}"/>`).join("")}</g>
<circle id="fFlash" cx="610" cy="610" r="120" fill="#fff"/>
${region("fReg",300,830,120,90)}
<g id="fRed"><path d="M-22,-12 L18,-18 L24,10 L-10,20 Z" fill="${RED}"/></g>
${chip("fTag",130,690,"MAI «LIBERO» QUI",BLUE,340)}
<g id="fCard" transform="translate(1290,270)"><rect width="540" height="420" rx="36" fill="#fff" filter="url(#sh)"/><rect width="540" height="14" rx="7" fill="${BLUE}"/><text x="40" y="66" font-size="24" font-weight="700" fill="${GREY}" letter-spacing="3">CASO 1 · VOLO VELOCE</text><text x="270" y="230" text-anchor="middle" font-size="150" font-weight="800" fill="${BLUE}" letter-spacing="-4">60<tspan font-size="70" fill="${INK}"> su 60</tspan></text><text x="270" y="310" text-anchor="middle" font-size="32" font-weight="700" fill="${INK}">evento dichiarato entro 1 s</text><text x="270" y="360" text-anchor="middle" font-size="26" font-weight="600" fill="${TEAL}">prove simulate</text></g>
${chip("fCam",1290,730,"CAMERE  ·  NON AFFIDABILI",GREY,540)}
${tbadge("fBadge",50,915)}</g>`;
// ---------- casi d'uso nuovi
H+=`<g id="gS4"><rect width="1920" height="1080" fill="#F2F7FD"/><rect y="820" width="1920" height="260" fill="#DDE6F0"/>
${tag}${head("s4Head",120,270,"Un braccio robotico","che si ferma prima dell’operatore.",68)}
${region("s4Reg",1500,720,150,180)}<g transform="translate(1500,780)">${person(TEAL)}</g>
<g transform="translate(1040,820)"><g transform="rotate(-25)"><rect x="-24" y="-310" width="48" height="320" rx="24" fill="${BLUE}"/><g transform="translate(0,-300)"><g id="s4B"><rect x="-19" y="-250" width="38" height="262" rx="19" fill="#34506F"/><path d="M-32,-250 L-32,-292 L-15,-292 L-15,-264 L15,-264 L15,-292 L32,-292 L32,-250 Z" fill="${INK}"/></g><circle r="30" fill="${INK}"/></g></g><circle r="38" cy="-10" fill="${INK}"/><rect x="-110" y="-30" width="220" height="50" rx="12" fill="${INK}"/></g>
${badge("s4W",1250,560)}</g>`;
H+=`<g id="gS5"><rect width="1920" height="1080" fill="#F2FBF8"/><rect y="820" width="1920" height="260" fill="#DDE6F0"/>
${tag}${head("s5Head",120,270,"Un muletto automatico","che sa di chi è dietro lo scaffale.",68)}
<g transform="translate(1450,780)">${person(TEAL)}</g>
<g transform="translate(1300,820)"><rect x="-160" y="-440" width="320" height="440" rx="8" fill="#9FB3C8"/>${[0,1,2].map(i=>`<rect x="-140" y="${-420+i*145}" width="280" height="120" rx="6" fill="#DCE6F0"/><rect x="-120" y="${-380+i*145}" width="90" height="80" rx="6" fill="#C2A77A"/><rect x="-10" y="${-360+i*145}" width="110" height="60" rx="6" fill="#D4BC92"/>`).join("")}</g>
${region("s5Reg",1450,720,140,180)}
<g id="s5F"><rect x="-150" y="-140" width="215" height="105" rx="18" fill="${BLUE}"/><path d="M-120,-140 L-104,-240 L8,-240 L30,-140" stroke="${INK}" stroke-width="12" fill="none" stroke-linejoin="round"/><rect x="72" y="-270" width="16" height="270" fill="${INK}"/><rect x="72" y="-44" width="135" height="13" rx="4" fill="${INK}"/><circle cx="-100" cy="-32" r="34" fill="${INK}"/><circle cx="26" cy="-32" r="34" fill="${INK}"/><circle cx="-100" cy="-32" r="13" fill="#fff"/><circle cx="26" cy="-32" r="13" fill="#fff"/>${badge("s5W",-40,-320)}</g></g>`;
H+=`<g id="gS6"><rect width="1920" height="1080" fill="#F2F7FD"/><rect y="760" width="1920" height="220" fill="#DDE6F0"/>${lanes}
${tag}${head("s6Head",120,270,"Una pattuglia","che non perde l’auto dietro l’angolo.",68)}
<g id="s6C" transform="translate(1000,850)">${car("#34506F")}</g>
<rect x="1240" y="400" width="560" height="540" fill="#C9D6E4"/><g fill="#fff">${[0,1,2,3,4,5,6,7].map(i=>`<rect x="${1300+(i%4)*120}" y="${460+Math.floor(i/4)*170}" width="76" height="100" rx="8"/>`).join("")}</g>
${region("s6Reg",1520,860,210,95)}
<g id="s6P">${car(BLUE)}<rect x="-34" y="-86" width="68" height="16" rx="7" fill="${TEAL}"/>${badge("s6W",0,-150)}</g></g>`;
H+=`<g id="gS7"><rect width="1920" height="1080" fill="url(#sky)"/>
<g stroke="#9DB7D6" stroke-width="4" stroke-linecap="round">${Array.from({length:44},(_,i)=>{const x=(i*97)%1900,y=(i*211)%860+110;return `<path d="M${x},${y} l-14,44"/>`;}).join("")}</g>
${tag}${head("s7Head",120,270,"Un drone veloce","che trova l’ostacolo nel fumo.",68)}
<rect x="1380" y="400" width="46" height="680" fill="#34506F"/><rect x="1296" y="480" width="214" height="20" rx="8" fill="#34506F"/>
<g>${[[1250,660,150],[1400,580,170],[1540,680,150],[1400,780,170],[1150,760,120],[1620,540,110]].map((p,i)=>`<circle cx="${p[0]}" cy="${p[1]}" r="${p[2]}" fill="${i%2?'#8D99AB':'#6B778A'}" opacity=".95"/>`).join("")}</g>
${region("s7Reg",1400,650,140,210)}
<g id="s7D">${drone(BLUE)}${badge("s7W",0,-100)}</g></g>`;
H+=`<g id="gS8"><rect width="1920" height="1080" fill="#F2F7FD"/><rect y="720" width="1920" height="360" fill="#CFE4FB"/>
${tag}${head("s8Head",120,270,"Una nave","che non perde la barca nella nebbia.",68)}
<g transform="translate(1460,720)"><path d="M-80,-4 L80,-4 L58,36 L-58,36 Z" fill="#34506F"/><path d="M0,-110 L0,-10 L66,-20 Z" fill="#fff" stroke="#34506F" stroke-width="6" stroke-linejoin="round"/></g>
${cloud("s8f1",1380,760,1.5)}${cloud("s8f2",1680,660,1.0)}
${region("s8Reg",1460,700,180,115)}
<g id="s8S"><path d="M-270,-10 L250,-10 L196,76 L-226,76 Z" fill="${BLUE}"/><rect x="-160" y="-84" width="210" height="76" rx="8" fill="${INK}"/><rect x="-100" y="-136" width="84" height="54" rx="6" fill="#34506F"/>${badge("s8W",0,-210)}</g></g>`;
'''
r('// ---------- chiusura', NEW + '// ---------- chiusura')

# ---- ordine delle scene nel DOM e sottotitoli impressi
r('document.getElementById("stage").innerHTML=H;', r'''document.getElementById("stage").innerHTML=H;
{const st=document.getElementById("stage");["gSky","gA","gK","gF","gH","gZ","gP","gR","gI","gS2","gS4","gS5","gS1","gS6","gS3","gS7","gS8","gEnd"].forEach(id=>st.appendChild(document.getElementById(id)));
let sh="";SUBS.forEach((u,i)=>{const w=u[2].length*17.5+60;sh+=`<g id="sb${i}"><rect x="${960-w/2}" y="950" width="${w}" height="60" rx="14" fill="#fff" fill-opacity=".92"/><text x="960" y="991" text-anchor="middle" font-size="34" font-weight="600" fill="${INK}">${u[2]}</text></g>`;});
st.insertAdjacentHTML("beforeend",`<g id="gSub">${sh}</g>`);}''')

# ---- linea del tempo
r('const scene=(id,t0,t1)=>{if(t0>0){gsap.set(id,{autoAlpha:0});tl.to(id,{autoAlpha:1,duration:.5},t0);}if(t1<D)tl.to(id,{autoAlpha:0,duration:.5},t1);};',
  'const scene=(id,t0,t1,fade)=>{if(t0>0){gsap.set(id,{autoAlpha:0});tl.to(id,{autoAlpha:1,duration:.5},t0);}if(t1<D){if(fade)tl.to(id,{autoAlpha:0,duration:.5},t1);else tl.set(id,{autoAlpha:0},t1+.5);}};')
i = s.index('scene("#gSky",0,TR);'); j = s.index('\n', i)
s = s[:i] + r'''scene("#gSky",0,TR);scene("#gA",0,TK);scene("#gK",TK,TF);scene("#gF",TF,TH,1);scene("#gH",TH,TR);scene("#gZ",TZ,TP);scene("#gP",TP,TW,1);scene("#gR",TR,TI);scene("#gI",TI,TU[0]);
["#gS2","#gS4","#gS5","#gS1","#gS6","#gS3","#gS7","#gS8"].forEach((id,k)=>scene(id,TU[k],k<7?TU[k+1]:TE));scene("#gEnd",TE,D);
SUBS.forEach((u,k)=>{gsap.set("#sb"+k,{autoAlpha:0});tl.set("#sb"+k,{autoAlpha:1},u[0]);tl.set("#sb"+k,{autoAlpha:0},u[1]);});''' + s[j:]
rblock('// A\n', '// H campo largo', r'''// A
tl.fromTo("#aDrone",{x:-200,y:640},{x:1180,y:560,duration:2.6,ease:"power2.out"},0);
tl.to("#aDrone",{y:"+=14",duration:1,yoyo:true,repeat:26,ease:"sine.inOut"},2.6);
tl.fromTo("#aCloud",{x:2500,y:600},{x:1200,y:610,duration:2.2,ease:"power2.out"},1.2);
fin("#aHead",3.2); hide("#aHead",T2-.3);
tl.fromTo("#aReg",{autoAlpha:0,scale:.4,transformOrigin:O},{autoAlpha:1,scale:1.6,duration:1,ease:"power2.out"},T2+3); tl.to("#aReg",{scale:2.5,duration:Math.max(1,TK-T2-4),ease:"none"},T2+4);
fin("#bHead",T2+.2); fin("#aRegT",T2+4); fin("#p1",T2+4.5); fin("#p2",T2+6.5); fin("#p3",T2+8.5);
''')
r('duration:3.5,ease:"none"},TH)', 'duration:3.5,ease:"none"},TC-3.5)')
r('duration:3.5,ease:"power1.in"},TH)', 'duration:3.5,ease:"power1.in"},TC-3.5)', 2)
r('repeat:43', 'repeat:75'); r('duration:42,ease:"power1.out"', 'duration:62,ease:"power1.out"')
r('duration:5.5,ease:"none"},TZ)', 'duration:TP-TZ+.5,ease:"none"},TZ)', 2)
r('repeat:9,ease:"sine.inOut"},TP)', 'repeat:40,ease:"sine.inOut"},TP)')
r('pop("#tscale",TC-.1);', 'gsap.set("#tscale",{autoAlpha:0});tl.set("#tscale",{autoAlpha:0},0);tl.fromTo("#tscale",{autoAlpha:0},{autoAlpha:1,duration:.4,immediateRender:false},TC-.1);')
r('// fine\n', r'''// F caso 1
{const FX=TF2-1.5;
tl.fromTo("#fSpd",{x:1900},{x:-2400,duration:FX-TF+.6,ease:"none"},TF); hide("#fSpd",FX+.3);
tl.to("#fJet",{y:"+=12",duration:1.3,yoyo:true,repeat:24,ease:"sine.inOut"},TF);
fin("#fHead",TF+.3); hide("#fHead",TF2+.3);
gsap.set("#fFlash,#fRed",{autoAlpha:0});
tl.fromTo("#fFlash",{scale:.2,autoAlpha:1,transformOrigin:O},{scale:4.5,autoAlpha:0,duration:1.2,ease:"power2.out",immediateRender:false},FX);
document.querySelectorAll(".ffr").forEach((e,i)=>{gsap.set(e,{scale:0,transformOrigin:O});tl.to(e,{scale:1,duration:.8,ease:"back.out(2)"},FX+i*.08);tl.to(e,{scale:1.18,duration:1.1,yoyo:true,repeat:16,ease:"sine.inOut"},FX+1+i*.2);});
document.querySelectorAll(".fsk").forEach((e,i)=>{gsap.set(e,{scale:0,transformOrigin:O});tl.to(e,{scale:1,duration:5,ease:"power2.out"},FX+.3+i*.3);});
document.querySelectorAll(".fdb").forEach((e)=>{gsap.set(e,{autoAlpha:0,x:610,y:610});tl.set(e,{autoAlpha:1},FX+.1).to(e,{x:+e.dataset.x,y:+e.dataset.y,rotation:+e.dataset.r,transformOrigin:O,duration:16,ease:"power1.out"},FX+.1);});
tl.fromTo("#fRed",{x:610,y:610,scale:1.8,rotation:0,autoAlpha:1,transformOrigin:O},{x:300,y:830,rotation:200,duration:TF3-FX+.6,ease:"power1.out",immediateRender:false},FX+.1);
pop("#fBadge",TF2); pop("#fCard",TF2+1.8); pop("#fCam",TF2+(TF3-TF2)*.62);
tl.fromTo("#fReg",{autoAlpha:0,scale:.5,transformOrigin:O},{autoAlpha:1,scale:1.2,duration:.8,ease:"back.out(1.6)"},TF3+.5); pop("#fTag",TF3+1);}
// casi d'uso nuovi
{const uc=(n,t,mover,x0,x1,y)=>{fin("#s"+n+"Head",t+.2); if(mover)tl.fromTo(mover,{x:x0,y:y},{x:x1,y:y,duration:1.8,ease:"power2.out"},t+.1); tl.fromTo("#s"+n+"Reg",{autoAlpha:0,scale:.5,transformOrigin:O},{autoAlpha:1,scale:1.1,duration:.8,ease:"back.out(1.6)"},t+.8); pop("#s"+n+"W",t+1.4);};
uc(4,TU[1],null); tl.fromTo("#s4B",{rotation:35,svgOrigin:"0 0"},{rotation:100,svgOrigin:"0 0",duration:1.4,ease:"power2.out"},TU[1]+.1);
uc(5,TU[2],"#s5F",-260,800,820);
uc(6,TU[4],"#s6P",-200,640,850); tl.fromTo("#s6C",{x:1000,y:850},{x:1520,y:850,duration:1.5,ease:"power1.inOut"},TU[4]+.1);
uc(7,TU[6],"#s7D",-200,780,650);
uc(8,TU[7],"#s8S",-320,620,720);}
// fine
''')
# riga sull'indagine di R&D del committente (chiesta dall'utente), sotto le schede dell'infografica
_k = '">ogni quadratino è una prova simulata</text>'
assert s.count(_k) == 1
s = s.replace(_k, _k + '\n<g id="kRD"><rect x="510" y="872" width="900" height="64" rx="32" fill="#fff" stroke="${BLUE}" stroke-width="3"/><text x="960" y="914" text-anchor="middle" font-size="30" font-weight="700" fill="${INK}">+ indagine sui progetti di R&amp;D del committente</text></g>')
open(os.path.join(q, 'index.html'), 'w').write(s)

# ---- copione
cop = ["# MoVi pitch IT v4 — copione", "",
 "Video: `video/consegna/MoVi_pitch_IT_v4.mp4`, durata %.2f s. Voce: Kokoro `im_nicola`, velocità 1,0. Tutto ciò che si vede è un'illustrazione; tutte le cifre sono di simulazione (riga fissa a schermo «PROTOTIPO SIMULATO · ILLUSTRAZIONE»)." % D, "",
 "Si rigenera con: `python3 video/progetto_v4d/voce/genera_voce_v4d.py`, poi `sh video/progetto_v4d/fai_tutto.sh`.", "",
 "## Voce e tempi", "", "| clip | inizio (s) | durata voce (s) | testo |", "|---|---|---|---|"]
cop += ["| %s | %.2f | %.2f | %s |" % (a, b + RIT, c, d) for a, b, c, d in righe]
cop += ["", "## Cifre dette o scritte, con la fonte", "",
 "Registro: `video/consegna/MoVi_registro_cifre_final.md` (chiave fra parentesi quadre).", "",
 "| cifra | dove | fonte |", "|---|---|---|",
 "| 60 su 60: evento dichiarato e camere dichiarate non affidabili entro 1 s | caso 1 (voce e scheda); scheda «60/60» delle prove | [V-2] 60/60, simulato, innesco ottimista |",
 "| mai «libero» dove c'è un frammento | caso 1 (voce e etichetta), senza cifra | [V-1] 0/200 e 0/60, simulato |",
 "| 59 su 59: drone avvisato prima del primo frammento | scena eroe (scheda 5, voce, quadro delle cifre) | [F7R-C1-AVVISO] 59/59, simulato, correzione in prova: detto a voce e scritto |",
 "| 60 su 60: regione del bersaglio mantenuta | quadro delle cifre, voce | [F7R-C1-LIBERO] regione mantenuta 60/60, «libero» 0/60, simulato |",
 "| 200/200 avvisato in tempo, lunga portata | prove | [LP-1] 200/200, simulato |",
 "| oltre 100 pagine, oltre 400 riferimenti | prove, voce | messaggio del commit 9976563 («documento tecnico v3 (108 pagine)… 410 riferimenti»): non ricontati qui |",
 "", "## Illustrativo, non un dato", "",
 "- «non visto da 6,8 s» nella scena del cono: valore d'esempio.",
 "- Matrice 4×4, curva della confidenza e barra: illustrative, senza valori. La formula `C(τ) = 1 − e^(−r²/2σ²(τ))` viene dal pacchetto esterno: non verificata qui sulle fonti del progetto.",
 "- «Pronto per hardware dedicato, per progetto»: intenzione di progetto, non una prova su hardware.",
 "- Gli otto casi d'uso finali sono applicazioni possibili (etichetta su ogni tavola), non risultati.",
 "", "## Non incluso", "",
 "- La riga «Indagine sui progetti di R&D del committente» e la frase corrispondente nella voce: il sistema dei permessi ha negato due volte il comando che la conteneva, e la conferma dell'utente è arrivata solo tramite il coordinatore. Nei documenti del progetto l'indagine non risulta.", ""]
open(os.path.join(OUT, 'MoVi_copione_v4.md'), 'w').write("\n".join(cop))
print('ok', len(subs), 'sottotitoli')
