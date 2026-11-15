# Costruisce progetto_v4b/index.html da progetto_v4/index.html (letto soltanto): scena eroe con «come funziona».
import os
q=os.path.dirname(os.path.abspath(__file__))
s=open(os.path.join(q,'..','progetto_v4','index.html')).read()
def cut(a,b): return s[s.index(a):s.index(b)]
P1=s[:s.index('// ---------- H scena eroe')]
P3=cut('// ---------- I infografica','document.getElementById("stage").innerHTML=H;')
def r(t,a,b):
    assert t.count(a)>=1,a; return t.replace(a,b)
P1=r(P1,'data-duration="62"','data-duration="80"')
P1=r(P1,'cap(0.6,6.6,','cap(0.4,4.8,'); P1=r(P1,'cap(7.4,13.6,','cap(5.4,9.6,')
P1=r(P1,'let H="";','const D=80,TH=10,TC=13.5,TZ=17,TP=22,S0=24,ST=4.3,TW=50,TS=54,TR=58,TI=63,TS1=69,TS2=71.8,TS3=74.6,TE=77.4;\nconst c=[0,1,2,3,4,5,6].map(i=>S0+i*ST);\nlet H="";')
P3=r(P3,'${cap(36.6,45.6,','${cap(TI+.4,TI+5.6,')
NEW=r'''// ---------- H scena eroe, campo largo (TH-TZ e TW-TR)
const tbadge=(id,x,y)=>`<g ${id?`id="${id}"`:""} transform="translate(${x},${y})"><rect width="370" height="92" rx="46" fill="${INK}"/><circle cx="50" cy="46" r="20" fill="none" stroke="#fff" stroke-width="5"/><path d="M50,34 L50,46 L59,52" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round"/><text x="88" y="60" font-size="40" font-weight="800" fill="#fff">time ×0.05</text></g>`;
let smoke="",deb="",fire="";
for(let i=0;i<16;i++){const a=rnd()*6.28,r=60+rnd()*330;smoke+=`<circle class="smk" data-x="${(Math.cos(a)*r*1.25).toFixed(0)}" data-y="${(Math.sin(a)*r*0.7).toFixed(0)}" data-s="${(1.2+rnd()*1.6).toFixed(2)}" r="95" fill="${i%3?'#8D99AB':'#6B778A'}"/>`;}
for(let i=0;i<9;i++){const a=rnd()*6.28,r=30+rnd()*120;fire+=`<circle class="fir" data-x="${(Math.cos(a)*r).toFixed(0)}" data-y="${(Math.sin(a)*r).toFixed(0)}" r="${(50+rnd()*50).toFixed(0)}" fill="${i%2?'#FFB020':'#FF6A1A'}"/>`;}
for(let i=0;i<18;i++){const a=i/18*6.28+rnd()*0.3,r=380+rnd()*420;deb+=`<path class="deb" data-x="${(Math.cos(a)*r).toFixed(0)}" data-y="${(Math.sin(a)*r*0.75).toFixed(0)}" data-r="${(rnd()*500-250).toFixed(0)}" d="M-14,-8 L12,-12 L16,6 L-6,13 Z" fill="${INK}"/>`;}
H+=`<g id="gH"><g id="spd">${[0,1,2,3,4,5,6].map(i=>`<rect x="${200+i*260}" y="${140+((i*197)%700)}" width="${180+i*20}" height="6" rx="3" fill="#fff" opacity=".9"/>`).join("")}</g>
<line id="sight" x1="560" y1="740" x2="1390" y2="340" stroke="${BLUE}" stroke-width="5" stroke-dasharray="4 18" stroke-linecap="round"/>
<g id="hJet" transform="translate(1440,320)">${jet(INK)}</g>
<g id="d1">${drone("#34506F")}</g><g id="d2">${drone("#34506F")}</g>
<g id="boom" transform="translate(1000,540)"><g id="debs">${deb}</g><g id="fires">${fire}</g><g id="smokes" opacity=".93">${smoke}</g><circle id="flash" r="120" fill="#fff"/></g>
${region("hReg",1440,320,170,120)}
<text id="hRegT" x="1440" y="105" text-anchor="middle" font-size="36" font-weight="700" fill="${BLUE}">MoVi: the target is in here</text>
<g id="frag"><path d="M-22,-12 L18,-18 L24,10 L-10,20 Z" fill="${RED}"/></g>
<g id="hCar" transform="translate(480,780)"><circle id="ringS" r="112" fill="${AMB}" fill-opacity=".14" stroke="${AMB}" stroke-width="9"/><circle id="ring" r="120" fill="none" stroke="${AMB}" stroke-width="18"/>${drone(BLUE)}</g>
${chip("cCam",120,90,"CAMERAS  ·  BLINDED",GREY,400)}${chip("cRad",540,90,"RADAR  ·  BLINDED",GREY,360)}
${chip("cWarn",200,570,"WARNING SENT",AMB,300)}
${tbadge("tscale",50,915)}
<g id="hStats"><rect width="1920" height="1080" fill="#F7FAFE" opacity=".94"/>
 <text x="960" y="170" text-anchor="middle" font-size="34" font-weight="700" fill="${GREY}" letter-spacing="3">SENSORS BLINDED BY THE EXPLOSION · SIMULATED RUNS</text>
 <g id="st1"><text x="520" y="470" text-anchor="middle" font-size="230" font-weight="800" fill="${BLUE}" letter-spacing="-6">59<tspan fill="${INK}" font-size="120"> of 59</tspan></text><text x="520" y="560" text-anchor="middle" font-size="38" font-weight="600" fill="${INK}">carrier warned before the first fragment</text><text x="520" y="612" text-anchor="middle" font-size="28" font-weight="600" fill="${TEAL}">promising result · correction under test</text></g>
 <g id="st2"><text x="1400" y="470" text-anchor="middle" font-size="230" font-weight="800" fill="${BLUE}" letter-spacing="-6">60<tspan fill="${INK}" font-size="120"> of 60</tspan></text><text x="1400" y="560" text-anchor="middle" font-size="38" font-weight="600" fill="${INK}">target region kept through the smoke</text><text x="1400" y="612" text-anchor="middle" font-size="28" font-weight="600" fill="${TEAL}">never called “clear” where the drone or a fragment was</text></g></g>
${cap(TH+.3,TC-.3,"A drone follows a fast object.")}${cap(TC+.4,TZ-.3,"Two drones collide right next to it. Time slows down.")}${cap(TW+.5,TS-.3,"Warned before the first fragment passes.")}${cap(TS+.5,TR-.3,"It never calls “clear” what it has not observed.")}</g>`;
// ---------- Z primo piano: i sensori si attivano (TZ-TP)
const icons=[`<circle cx="0" cy="18" r="6" fill="${INK}"/><path d="M-15,6 A19,19 0 0 1 15,6"/><path d="M-28,-5 A36,36 0 0 1 28,-5"/>`,`<rect x="-28" y="-16" width="56" height="38" rx="8"/><circle r="11" cy="3"/><rect x="-10" y="-25" width="20" height="9" rx="3"/>`,`<path d="M-18,24 q-11,-12 0,-24 q11,-12 0,-24"/><path d="M0,24 q-11,-12 0,-24 q11,-12 0,-24"/><path d="M18,24 q-11,-12 0,-24 q11,-12 0,-24"/>`];
const names=["RADAR","CAMERA","INFRARED"];
H+=`<g id="gZ"><rect width="1920" height="1080" fill="#F2F7FD"/>${head("zHead",120,140,"The sensors wake up.","One core listens.",72)}
<g transform="translate(330,600) scale(2.4)">${drone(BLUE)}</g>
${[0,1,2].map(i=>{const y=360+i*240;return `<path class="flow" id="fa${i}" d="M520,600 C660,600 660,${y} 776,${y}" fill="none" stroke="${BLUE}" stroke-width="6" stroke-dasharray="14 14" stroke-linecap="round"/><path class="flow" id="fb${i}" d="M904,${y} C1090,${y} 1090,600 1232,600" fill="none" stroke="${BLUE}" stroke-width="6" stroke-dasharray="14 14" stroke-linecap="round"/><g id="sn${i}" transform="translate(840,${y})"><circle r="64" fill="#fff" filter="url(#sh)"/><g fill="none" stroke="${INK}" stroke-width="6" stroke-linecap="round">${icons[i]}</g><text y="104" text-anchor="middle" font-size="26" font-weight="800" fill="${INK}" letter-spacing="2">${names[i]}</text></g>`;}).join("")}
<g id="core" transform="translate(1390,600)"><circle r="156" fill="${INK}"/><circle id="coreRing" r="126" fill="none" stroke="#fff" stroke-width="5" stroke-dasharray="10 12" opacity=".6"/><text y="8" text-anchor="middle" font-size="64" font-weight="800" fill="#fff">MoVi</text><text y="54" text-anchor="middle" font-size="30" font-weight="600" fill="#BFD6F6">core</text></g>
${tbadge("",50,915)}</g>`;
// ---------- P soggettiva: i componenti uno alla volta (TP-TW)
const spill=(i,x,txt)=>`<g id="sp${i}" transform="translate(${x},172)"><rect width="150" height="50" rx="25" fill="#fff" filter="url(#sh)"/><circle class="sdot" cx="26" cy="25" r="9" fill="${TEAL}"/><text x="46" y="33" font-size="22" font-weight="700" fill="${INK}">${txt}</text></g>`;
const tagS=(id,x,y,w,txt,cc)=>`<g id="${id}" transform="translate(${x},${y})"><rect width="${w}" height="46" rx="10" fill="${cc}"/><text x="${w/2}" y="32" text-anchor="middle" font-size="22" font-weight="700" fill="#fff" letter-spacing="1">${txt}</text></g>`;
const mat=(id)=>{let m=`<g id="${id}">`;for(let i=0;i<4;i++)for(let j=0;j<4;j++){const o=i==j?.95:(Math.abs(i-j)==1?.36:.14);m+=`<rect class="mc" data-o="${o}" x="${-136+j*70}" y="${-136+i*70}" width="62" height="62" rx="12" fill="${BLUE}"/>`;}return m+`</g><text y="186" text-anchor="middle" font-size="22" font-weight="600" fill="${GREY}">uncertainty matrix · illustrative</text>`;};
const cardP=(i,title,sub,line,g)=>`<g id="pc${i}" transform="translate(1340,190)"><rect width="520" height="620" rx="36" fill="#fff" filter="url(#sh)"/><rect width="520" height="14" rx="7" fill="${BLUE}"/><text x="40" y="62" font-size="24" font-weight="700" fill="${GREY}" letter-spacing="3">${i} / 6</text><text x="40" y="122" font-size="48" font-weight="800" fill="${INK}" letter-spacing="-1">${title}</text><text x="40" y="160" font-size="24" font-weight="600" fill="${GREY}">${sub}</text><text x="40" y="216" font-size="34" font-weight="700" fill="${BLUE}">${line}</text><g transform="translate(260,410)">${g}</g></g>`;
const g1=`<g stroke="${GREY}" stroke-width="4" fill="none"><path d="M-150,-90 C-60,-90 -40,0 60,0"/><path d="M-150,0 L60,0"/><path d="M-150,90 C-60,90 -40,0 60,0"/></g><circle cx="-150" cy="-90" r="24" fill="${BLUE}"/><circle cx="-150" cy="0" r="24" fill="${TEAL}"/><circle cx="-150" cy="90" r="24" fill="${AMB}"/><circle cx="110" cy="0" r="62" fill="${INK}"/><circle cx="110" cy="0" r="40" fill="none" stroke="#fff" stroke-width="4" stroke-dasharray="8 9"/>`;
const g4=[[TEAL,"seen",""],[BLUE,"not seen: a region","d"],["#8D99AB","unknown",""]].map((a,i)=>`<rect x="-210" y="${-115+i*90}" width="76" height="54" rx="12" fill="${a[0]}" ${a[2]?`fill-opacity=".25" stroke="${BLUE}" stroke-width="4" stroke-dasharray="10 7"`:""}/><text x="-112" y="${-77+i*90}" font-size="32" font-weight="700" fill="${INK}">${a[1]}</text>`).join("");
const g5=`<text y="30" text-anchor="middle" font-size="150" font-weight="800" fill="${BLUE}" letter-spacing="-4">59<tspan font-size="70" fill="${INK}"> of 59</tspan></text><text y="92" text-anchor="middle" font-size="28" font-weight="700" fill="${INK}">simulated runs</text><text y="132" text-anchor="middle" font-size="24" font-weight="600" fill="${TEAL}">correction under test</text>`;
const g6=`<circle id="r6" r="140" fill="url(#reg)" stroke="${BLUE}" stroke-width="5" stroke-dasharray="18 12"/><circle r="16" fill="${INK}"/>`;
const psm=[[-90,-20,80],[-20,-70,90],[60,-40,85],[110,20,75],[40,60,90],[-50,60,80],[0,0,100],[-120,40,60]];
H+=`<g id="gP"><rect width="1920" height="1080" fill="url(#sky)"/><path d="M0,770 L1920,700 L1920,1080 L0,1080 Z" fill="#DCE9E4"/><path d="M0,770 L1920,700" stroke="#B9CFC7" stroke-width="3"/>
${cloud("pcl",1080,300,0.4)}
<g id="pTgt" transform="translate(760,450)" fill="${INK}"><rect x="-78" y="-4" width="156" height="8" rx="4"/><ellipse rx="20" ry="17"/><rect x="-4" y="-46" width="8" height="36" rx="3"/><rect x="-30" y="-46" width="60" height="6" rx="3"/></g>
<g id="pSm" transform="translate(250,500)"><circle cx="-10" cy="20" r="80" fill="#FF6A1A"/><circle cx="50" cy="-10" r="70" fill="#FFB020"/>${psm.map((p,i)=>`<circle cx="${p[0]}" cy="${p[1]}" r="${p[2]}" fill="${i%3?'#8D99AB':'#6B778A'}"/>`).join("")}${[[-170,-90],[150,-110],[190,80],[-150,120],[20,-170]].map(p=>`<path transform="translate(${p[0]},${p[1]})" d="M-14,-8 L12,-12 L16,6 L-6,13 Z" fill="${INK}"/>`).join("")}</g>
${region("pReg",760,450,95,65)}
${tagS("pTag",880,366,130,"TARGET",INK)}
<g id="pFrag"><path d="M-22,-12 L18,-18 L24,10 L-10,20 Z" fill="${RED}"/></g>
<path d="M80,210 L80,150 L140,150 M1220,150 L1280,150 L1280,210 M80,800 L80,860 L140,860 M1220,860 L1280,860 L1280,800" fill="none" stroke="${INK}" stroke-width="5" opacity=".4" stroke-linecap="round"/>
<rect id="pWarn" x="80" y="150" width="1200" height="710" rx="24" fill="none" stroke="${AMB}" stroke-width="18"/>
<text x="84" y="124" font-size="24" font-weight="700" fill="${GREY}" letter-spacing="3">VIEW FROM THE DRONE THAT CARRIES MOVI</text>
${spill(0,110,"RADAR")}${spill(1,275,"CAMERA")}${spill(2,440,"IR")}${tagS("pBl",606,174,150,"BLINDED",RED)}
<g id="pConf" transform="translate(110,780)"><text font-size="22" font-weight="700" fill="${GREY}" letter-spacing="3">CONFIDENCE</text><rect y="14" width="420" height="26" rx="13" fill="#fff" stroke="#C9D6E4" stroke-width="2"/><rect id="pBar" y="14" width="420" height="26" rx="13" fill="${BLUE}"/></g>
${tagS("t1",1050,330,110,"SEEN",TEAL)}${tagS("t2",600,232,320,"NOT SEEN · A REGION",BLUE)}${tagS("t3",430,650,170,"UNKNOWN","#5B6B82")}
${chip("pChip",920,772,"WARNING SENT",AMB,300)}
${cardP(1,"Fusion","radar · camera · infrared","three sensors, one picture",g1)}${cardP(2,"Estimate","Kalman filter","predicts where it can be",mat("m2"))}${cardP(3,"Sensors blinded","the uncertainty grows","confidence falls, honestly",mat("m3"))}${cardP(4,"State map","every place has a state","never calls it clear",g4)}${cardP(5,"Warning","to the vehicle that carries it","warns at once",g5)}${cardP(6,"Reacquire","the sensors come back","picks it up again",g6)}
${tbadge("",50,915)}${cap(TP+.4,S0+3.6,"Through the eyes of the drone that carries MoVi.")}</g>`;
// ---------- R architettura (TR-TI)
const blk=(i,t1,t2,sub,cc)=>`<g id="ab${i}" transform="translate(${70+i*362},430)"><rect width="300" height="210" rx="28" fill="#fff" filter="url(#sh)"/><rect width="300" height="12" rx="6" fill="${cc}"/><text x="150" y="${t2?80:100}" text-anchor="middle" font-size="32" font-weight="800" fill="${INK}">${t1}</text>${t2?`<text x="150" y="120" text-anchor="middle" font-size="32" font-weight="800" fill="${INK}">${t2}</text>`:""}<text x="150" y="170" text-anchor="middle" font-size="23" font-weight="600" fill="${GREY}">${sub}</text></g>`+(i<4?`<path id="aa${i}" d="M${70+i*362+314},535 l34,0 m-13,-13 l13,13 l-13,13" stroke="${BLUE}" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`:"");
H+=`<g id="gR"><rect width="1920" height="1080" fill="#F7FAFE"/>${head("rHead",120,150,"How it works:","one pipeline, five layers.",72)}
${blk(0,"Sensors","","radar · camera · infrared",BLUE)}${blk(1,"Fusion","","one shared picture",TEAL)}${blk(2,"Multi-model","estimator","IMM Kalman",BLUE)}${blk(3,"State map","","seen · region · unknown",TEAL)}${blk(4,"Warning","","to the vehicle, at once",AMB)}
${pill("rHw",620,740,680,"Dedicated-hardware ready, by design",TEAL)}</g>`;
'''
TL=r'''document.getElementById("stage").innerHTML=H;
// ================= linea del tempo
window.__timelines = window.__timelines || {};
const tl = gsap.timeline({ paused: true });
const O="50% 50%";
const scene=(id,t0,t1)=>{if(t0>0){gsap.set(id,{autoAlpha:0});tl.to(id,{autoAlpha:1,duration:.5},t0);}if(t1<D)tl.to(id,{autoAlpha:0,duration:.5},t1);};
const fin=(id,t,d=.6)=>tl.fromTo(id,{autoAlpha:0},{autoAlpha:1,duration:d},t);
const pop=(id,t)=>tl.fromTo(id,{autoAlpha:0,scale:.3,transformOrigin:O},{autoAlpha:1,scale:1,duration:.6,ease:"back.out(2)"},t);
const hide=(id,t)=>tl.to(id,{autoAlpha:0,duration:.4},t);
caps.forEach(([a,b],i)=>{tl.fromTo("#cap"+i,{autoAlpha:0},{autoAlpha:1,duration:.4},a);tl.to("#cap"+i,{autoAlpha:0,duration:.3},b);});
scene("#gSky",0,TR);scene("#gA",0,TH);scene("#gH",TH,TR);scene("#gZ",TZ,TP);scene("#gP",TP,TW);scene("#gR",TR,TI);scene("#gI",TI,TS1);scene("#gS1",TS1,TS2);scene("#gS2",TS2,TS3);scene("#gS3",TS3,TE);scene("#gEnd",TE,D);
tl.to("#cl1",{x:"-=500",duration:TR,ease:"none"},0).to("#cl2",{x:"-=700",duration:TR,ease:"none"},0).to("#cl3",{x:"-=900",duration:TR,ease:"none"},0);
// A
tl.fromTo("#aDrone",{x:-200,y:640},{x:1180,y:560,duration:2.6,ease:"power2.out"},0);
tl.to("#aDrone",{y:"+=14",duration:1,yoyo:true,repeat:7,ease:"sine.inOut"},2.6);
tl.fromTo("#aCloud",{x:2500,y:600},{x:1200,y:610,duration:2.2,ease:"power2.out"},1.2);
fin("#aHead",2.6); hide("#aHead",4.9);
tl.fromTo("#aReg",{autoAlpha:0,scale:.4,transformOrigin:O},{autoAlpha:1,scale:1.6,duration:1,ease:"power2.out"},5.4); tl.to("#aReg",{scale:2.5,duration:3.6,ease:"none"},6.4);
fin("#bHead",5.2); fin("#aRegT",6); fin("#p1",6.4); fin("#p2",7.2); fin("#p3",8);
// H campo largo
tl.fromTo("#spd",{x:1900},{x:-2200,duration:3.5,ease:"none"},TH); hide("#spd",TC-.1);
gsap.set("#flash,#frag,#ring,#pFrag,#pWarn",{autoAlpha:0});
tl.fromTo("#d1",{x:1900,y:980},{x:1040,y:560,duration:3.5,ease:"power1.in"},TH);
tl.fromTo("#d2",{x:200,y:120},{x:960,y:520,duration:3.5,ease:"power1.in"},TH);
tl.to("#hCar",{y:"+=16",duration:1.1,yoyo:true,repeat:43,ease:"sine.inOut"},TH);
pop("#tscale",TC-.1);
tl.fromTo("#flash",{scale:.2,autoAlpha:1,transformOrigin:O},{scale:5,autoAlpha:0,duration:1.2,ease:"power2.out",immediateRender:false},TC);
tl.to("#d1",{x:"+=90",y:"+=120",rotation:70,autoAlpha:0,transformOrigin:O,duration:3},TC).to("#d2",{x:"-=90",y:"+=140",rotation:-80,autoAlpha:0,transformOrigin:O,duration:3},TC);
document.querySelectorAll(".fir").forEach((e,i)=>{gsap.set(e,{scale:0,transformOrigin:O});tl.to(e,{x:+e.dataset.x,y:+e.dataset.y,scale:1.5,duration:2.2,ease:"power2.out"},TC+i*.06).to(e,{autoAlpha:0,scale:2,duration:3},TC+2.4);});
document.querySelectorAll(".smk").forEach((e,i)=>{gsap.set(e,{scale:0,transformOrigin:O});tl.to(e,{x:+e.dataset.x,y:+e.dataset.y,scale:+e.dataset.s,duration:7,ease:"power2.out"},TC+.3+i*.1);});
document.querySelectorAll(".deb").forEach((e)=>{gsap.set(e,{autoAlpha:0});tl.set(e,{autoAlpha:1},TC+.1).to(e,{x:+e.dataset.x,y:+e.dataset.y,rotation:+e.dataset.r,transformOrigin:O,duration:42,ease:"power1.out"},TC+.1);});
tl.to("#smokes",{x:160,y:-60,duration:30,ease:"none"},TC+1);
tl.to("#sight",{stroke:"#9AA5B8",autoAlpha:.35,duration:1},TC+1.5);
tl.to("#hJet",{autoAlpha:0,duration:1.5},TC+1.8);
pop("#cCam",TW+.2); pop("#cRad",TW+.4);
tl.fromTo("#hReg",{autoAlpha:0,scale:.6,transformOrigin:O},{autoAlpha:1,scale:1.35,duration:.8,ease:"back.out(1.6)"},TW+.3); fin("#hRegT",TW+.5);
tl.fromTo("#frag",{x:850,y:600,rotation:0,scale:1.8,autoAlpha:1,transformOrigin:O},{x:340,y:756,rotation:220,duration:3.6,ease:"none",immediateRender:false},TW+.2);
pop("#cWarn",TW+.8); fin("#ringS",TW+.8,.3);
tl.fromTo("#ring",{scale:.7,autoAlpha:1,transformOrigin:O},{scale:1.7,autoAlpha:0,duration:1,repeat:2,ease:"power1.out",immediateRender:false},TW+.8);
fin("#hStats",TS); fin("#st1",TS+.3); fin("#st2",TS+1.3);
// Z
fin("#zHead",TZ+.3);
[0,1,2].forEach(i=>{pop("#sn"+i,TZ+.8+i*.6);fin("#fa"+i,TZ+.9+i*.6);fin("#fb"+i,TZ+2.7+i*.2);});
pop("#core",TZ+2.6);
tl.to(".flow",{strokeDashoffset:-168,duration:5.5,ease:"none"},TZ);
tl.to("#coreRing",{rotation:90,transformOrigin:O,duration:5.5,ease:"none"},TZ);
// P
[0,1,2].forEach(i=>pop("#sp"+i,TP+.6+i*.3));
for(let i=1;i<=6;i++){fin("#pc"+i,c[i-1],.5); if(i<6)tl.to("#pc"+i,{autoAlpha:0,duration:.3},c[i]-.3);}
tl.to("#pTgt",{y:"+=8",duration:1.2,yoyo:true,repeat:9,ease:"sine.inOut"},TP);
pop("#pTag",c[0]+.6);
tl.fromTo("#pReg",{autoAlpha:0,scale:.5,transformOrigin:O},{autoAlpha:1,scale:1,duration:.9,ease:"back.out(1.6)"},c[1]+1.2);
tl.fromTo("#m2 .mc",{opacity:0},{opacity:(i,e)=>+e.dataset.o,duration:.4,stagger:.08},c[1]+.4);
gsap.set("#pBar",{scaleX:.92,transformOrigin:"0% 50%"}); fin("#pConf",c[1]+1.4);
gsap.set("#m3 .mc",{opacity:(i,e)=>+e.dataset.o});
tl.to("#m3 .mc",{opacity:(i,e)=>Math.min(1,+e.dataset.o+.5),duration:3.4,ease:"none"},c[2]+.4);
tl.fromTo("#m3",{scale:.8,transformOrigin:O},{scale:1.08,duration:3.4,ease:"none"},c[2]+.4);
tl.to("#pSm",{x:730,y:470,scale:1.35,transformOrigin:O,duration:3.2,ease:"power1.inOut"},c[2]+.2);
hide("#pTag",c[2]+1); tl.to("#pTgt",{autoAlpha:0,duration:1.4},c[2]+1.4);
tl.to(".sdot",{fill:RED,duration:.5},c[2]+1.6); pop("#pBl",c[2]+1.7);
tl.to("#pReg",{scale:2.2,duration:3.4,ease:"none"},c[2]+.6);
tl.to("#pBar",{scaleX:.42,duration:3.6,ease:"none"},c[2]+.4);
pop("#t1",c[3]+.5); pop("#t2",c[3]+1.2); pop("#t3",c[3]+1.9); hide("#t1,#t2,#t3",c[4]-.3);
tl.fromTo("#pWarn",{autoAlpha:0},{autoAlpha:1,duration:.5,repeat:4,yoyo:true,immediateRender:false},c[4]+.2);
pop("#pChip",c[4]+.4);
tl.fromTo("#pFrag",{x:700,y:480,scale:.6,rotation:0,autoAlpha:1,transformOrigin:O},{x:250,y:790,scale:3.2,rotation:160,duration:3.4,ease:"power1.in",immediateRender:false},c[4]+.4);
hide("#pFrag",c[4]+3.8); hide("#pWarn",c[5]+.2); hide("#pChip",c[5]+.2);
tl.to("#pSm",{autoAlpha:.12,x:520,duration:2.6},c[5]+.3);
tl.to(".sdot",{fill:TEAL,duration:.5},c[5]+1); hide("#pBl",c[5]+1);
tl.to("#pTgt",{autoAlpha:1,duration:1},c[5]+1.2);
tl.to("#pReg",{scale:.9,duration:2.6,ease:"power1.inOut"},c[5]+1);
tl.to("#pBar",{scaleX:.9,duration:2.6,ease:"power1.inOut"},c[5]+1);
tl.fromTo("#r6",{scale:1,transformOrigin:O},{scale:.3,duration:2.6,ease:"power1.inOut"},c[5]+1);
// R
fin("#rHead",TR+.3); [0,1,2,3,4].forEach(i=>{pop("#ab"+i,TR+.6+i*.5); if(i<4)fin("#aa"+i,TR+.9+i*.5);}); fin("#rHw",TR+3.3);
// I
fin("#iHead",TI+.3); ["#k1","#k2","#k3","#k4"].forEach((k,i)=>fin(k,TI+.7+i*.5));
// S1
fin("#s1Head",TS1+.2); tl.fromTo("#s1Car",{x:-200,y:860},{x:640,y:860,duration:1.8,ease:"power2.out"},TS1+.1);
tl.fromTo("#s1Reg",{autoAlpha:0,scale:.5,transformOrigin:O},{autoAlpha:1,scale:1.15,duration:.8,ease:"back.out(1.6)"},TS1+.8);
pop("#s1W",TS1+1.3); tl.to("#s1Ped",{y:"+=110",duration:1.4,ease:"power1.inOut"},TS1+1.3);
// S2
fin("#s2Head",TS2+.2); tl.to("#s2Car",{x:1700,duration:1.8,ease:"power2.out"},TS2+.1);
tl.fromTo("#s2Reg",{autoAlpha:0,scale:.5,transformOrigin:O},{autoAlpha:1,scale:1.1,duration:.8,ease:"back.out(1.6)"},TS2+.7);
tl.fromTo("#s2R",{scale:.5,autoAlpha:1,transformOrigin:O},{scale:1.7,autoAlpha:0,duration:.8,repeat:1,ease:"power1.out"},TS2+1);
// S3
fin("#s3Head",TS3+.2); tl.to("#s3Deb",{x:-70,y:20,duration:2.8,ease:"none"},TS3); tl.to("#s3F",{x:"-=120",y:"+=20",rotation:140,transformOrigin:O,duration:2.8,ease:"none"},TS3);
tl.fromTo("#s3Reg",{autoAlpha:0,scale:.5,transformOrigin:O},{autoAlpha:1,scale:1.3,duration:.9,ease:"back.out(1.6)"},TS3+.7); tl.to("#s3Reg",{x:"-=70",duration:2,ease:"none"},TS3+.8);
tl.fromTo("#s3R",{scale:.5,autoAlpha:1,transformOrigin:O},{scale:1.8,autoAlpha:0,duration:.8,repeat:1,ease:"power1.out"},TS3+1);
// fine
pop("#eLogo",TE+.3); fin("#eT1",TE+.8); fin("#eT2",TE+1.3);
tl.to({}, {duration:0.01}, D-.01);
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''
open(os.path.join(q,'index.html'),'w').write(P1+NEW+P3+TL)
print('ok')
