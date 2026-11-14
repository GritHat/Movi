# riconta_arbitro.py — ogni cifra che il verdetto prende da torneo, attacco, verifica e registro, cercata nel file dei risultati.
# Sola lettura. Rifare: python3 -I -B riconta_arbitro.py   (dalla cartella 16-verdetto)
import re, os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
C = [
 ("11-torneo/risultati_scenB.txt", r"Q3c\s+147\s+0\s+0\s+0\s+0\s+0\s+0\s+0\s+0\s+97\.1\s+0\.48", "Q3c: 0 su 147, resa 97,1 %, 0,48 ms"),
 ("11-torneo/risultati_scenB.txt", r"VOa\s+147.*83\.0\s+6\.24", "VOa: 83,0 %, 6,24 ms"),
 ("11-torneo/risultati_scenB.txt", r"S10\(B\+M\)\s+147.*30\.6", "S10 resa 30,6 %"),
 ("11-torneo/risultati_a5.txt", r"N0-suolo\s+13\s+438", "N0 438"),
 ("11-torneo/risultati_a5.txt", r"N1-suolo\s+13\s+14\s+13", "N1 14 (base 13)"),
 ("11-torneo/risultati_a5c.txt", r"N1-suolo\s+87\s+87\s+87\s+3967\s+1186", "N1 1186 punti"),
 ("11-torneo/risultati_a5c.txt", r"Q3c\s+87\s+36\s+0\s+495", "Q3c 0 profondi, 495 di bordo"),
 ("11-torneo/risultati_a5c.txt", r"Q3\s+87\s+45\s+44", "Q3 44 su 87"),
 ("11-torneo/risultati_statica.txt", r"liberi 146901, di cui falsi 80505", "due vie 80505 su 146901"),
 ("11-torneo/risultati_a2.txt", r"decadimento verso il libero\s+fotogrammi con un voxel del corpo «libero»: 830", "830 (su 897)"),
 ("11-torneo/risultati_a2.txt", r"nascosto: 897", "897"),
 ("11-torneo/risultati_a3.txt", r"scritti 22240, persi 14448", "14448 su 22240"),
 ("11-torneo/risultati_a3.txt", r"nascosto 134, fuori regione 132", "132 su 134"),
 ("11-torneo/risultati_a4.txt", r"in 144 fotogrammi su 150", "144 su 150"),
 ("11-torneo/risultati_a9.txt", r"VO\s+71006", "71006"),
 ("11-torneo/risultati_a9.txt", r"N1-suolo\s+732 \(\s*0\)\s+744 \(\s*2\)\s+727", "744 e 727"),
 ("11-torneo/risultati_a10.txt", r"tetto 300 blocchi: mediana 33\.46 ms, p95 69\.56, massimo 69\.84", "33 ms, 70 max"),
 ("11-torneo/risultati_a10.txt", r"Q3c 0\.57/0\.86/1\.19\(2\.11\)", "rapporto 2,11"),
 ("11-torneo/risultati_a10.txt", r"Q3c 0\.57/0\.86/1\.19\(2\.09\)", "rapporto 2,09"),
 ("11-torneo/risultati_a10.txt", r"Q3c 0\.56/0\.86/1\.20\(2\.13\)", "rapporto 2,13; massimo 1,20 ms"),
 ("11-torneo/risultati_a8.txt", r"Q3c\s+654 su 800", "vetro 654 su 800"),
 ("11-torneo/risultati_a6.txt", r"Q3c\s+0 \(\s*0\)\s+1225", "posa 1225"),
 ("11-torneo/risultati_s10.txt", r"scena 0.*S10\(B\+M\+A\) 0 ;", "S10 con fascia alta 0 su 2610"),
 ("11-torneo/risultati_s10.txt", r"scena 3[^\n]*\n[^\n]*S10\(B\+M\) 32 ;[^\n]*N1 0", "scatola 10 cm: S10 32, N1 0"),
 ("11-torneo/risultati_s10.txt", r"scena 1[^\n]*\n[^\n]*N1 68", "N1 68 celle con la barra"),
 ("11-torneo/risultati_s10.txt", r"3170\)\n## S10 scena 5[^\n]*\n[^\n]*S10\(B\+M\) 67", "67 celle, 3170 pixel"),
 ("11-torneo/risultati_k106.txt", r"sparsi  5 %, a chiazze  0 %: Q1 61\.1 % ; Q3 91\.9 % ; Q3c 87\.7 % ; P 0\.1 % ; S10 0\.0 %", "5 % sparso: Q3c 87,7; S10 0,0"),
 ("11-torneo/risultati_k106.txt", r"sparsi  0 %, a chiazze  5 %: Q1 90\.9 % ; Q3 97\.0 % ; Q3c 92\.0 %", "chiazze 5 %: 92,0"),
 ("11-torneo/risultati_k105.txt", r"da un soggetto qualsiasi 537", "537"),
 ("11-torneo/risultati_k105.txt", r"libero conservato col margine: 0\.4 %", "0,4 %"),
 ("11-torneo/risultati_k102.txt", r"fotogrammi[^\n]*: 31 \(pixel validi medi 2552\)\n[^\n]*N alla lettera 0", "K-102: 0 su 31"),
 ("11-torneo/risultati_s11.txt", r"caso b[^\n]*200 corse su 200", "S11 b 200 su 200"),
 ("11-torneo/risultati_s11.txt", r"caso c[^\n]*153 corse su 200", "S11 c 153 su 200"),
 ("11-torneo/risultati_scenA.txt", r"celle N note 1444", "1444 (su 1460)"),
 ("11-torneo/risultati_scenA.txt", r"celle N note 1460", "1460"),
 ("11-torneo/risultati_pp.txt", r"dopo la copertura: fotogrammi nascosto 60 ; fuori regione: cuneo 60, V12 60, rec 0", "PP3 60/60/0"),
 ("14-attacco/risultati_av2_av3_av8.txt", r"pixel validi sulla barra: 1404", "1404 pixel"),
 ("14-attacco/risultati_av2_av3_av8.txt", r"32\.9 a fotogramma su 33", "32,9 su 33"),
 ("14-attacco/risultati_av2_av3_av8.txt", r"d=3 m: quota piu' alta con stato\(\)==LIBERO 0\.55 m ; la frase dichiara 1\.95", "senza fondale 0,55 contro 1,95"),
 ("14-attacco/risultati_av2_av3_av8.txt", r"d=2 m: quota piu' alta con stato\(\)==LIBERO 0\.95 m ; la frase dichiara 1\.70", "0,95 contro 1,70"),
 ("14-attacco/risultati_av2_av3_av8.txt", r"pannello alto 1\.65 m: pixel del soggetto\s+0", "0 pixel da 1,65 m"),
 ("14-attacco/risultati_av1.txt", r"0\.00\s+0\.0040\s+1391\s+0\.0", "resa 0,0 % a quota 0"),
 ("14-attacco/risultati_av4.txt", r"\(a\) cassa 1 m, persona dietro\s+k=0\.0040 pixel validi\s+2862 \| regola scritta: e' primo ritorno in 0/10", "AV4 0 su 10"),
 ("14-attacco/risultati_av4.txt", r"avversario-2 accetta il soggetto in 10/10", "V-019 10 su 10"),
 ("14-attacco/risultati_av4.txt", r"media dei pixel 0\.271 m, punto medio dei bordi 0\.179 m", "errore 0,18-0,27 m"),
 ("14-attacco/risultati_av5_av6_av7.txt", r"T=2\.0 s[^\n]*fuori regione in 60/60 \| riscritta: 1620 celle \(100 % del non osservato\), fuori in 0/60[^\n]*: 30", "AV5 60/60, 100 %, 0/60, 30 cicli"),
 ("14-attacco/risultati_av5_av6_av7.txt", r"0\.10 \[dopo\]\s+-1\.0\s+21\s+21\.0", "soglia 10 cm, 1 grado: 21 su 21"),
 ("14-attacco/risultati_av5_av6_av7.txt", r"restano per f8 e integrazione 4\.0 ore-persona", "4,0 ore"),
 ("14-attacco/risultati_av5_av6_av7.txt", r"restano per f8 e integrazione 1\.5 ore-persona", "1,5 ore"),
 ("14-attacco/risultati_av5_av6_av7.txt", r"restano per f8 e integrazione -9\.8 ore-persona", "-9,8 con 4"),
 ("14-attacco/risultati_av10.txt", None, "AV10: 16 righe con 0 celle"),
 ("15-verifica/risultati_vq3c.txt", None, "V: Q3c 0 profondi in 10 condizioni"),
 ("15-verifica/risultati_vq3c.txt", r"\(e\) soggetti muti[\s\S]*?N1 \(suolo visto in 1 di 3[^\n]*F  58 su 90 ; prof    558", "N1 58 su 90"),
 ("15-verifica/risultati_vq3c.txt", r"\(e\) soggetti muti[\s\S]*?validazione-1, senza memoria\): F  32 su 90", "V-021 32 su 90"),
 ("15-verifica/risultati_vq3c.txt", r"\(s5\)[\s\S]*?Q3c sulle celle \(h 0,10 m\): settori-fotogramma 180 ; estensione mediana 1\.4 m", "settori 1,4 m"),
 ("15-verifica/risultati_vq3c.txt", r"\(s5\)[\s\S]*?impronta, k = 1 \(validazione-2\): settori-fotogramma 180 ; estensione mediana 3\.0 m", "V-018 3,0 m"),
 ("15-verifica/risultati_vq3c.txt", r"\(a\) senza buchi[\s\S]*?Q3c  F   0 su 90 ; prof       0 ; bordo      0 ; resa  88\.4", "resa 88,4"),
 ("15-verifica/risultati_vq3c.txt", r"\(s0\)[\s\S]*?Q3c  F   0 su 90 ; prof       0 ; bordo      0 ; resa  91\.8", "resa 91,8"),
 ("15-verifica/risultati_vq3c.txt", r"\(b\) sparsi 5 %[\s\S]*?Q3c  F   0 su 90 ; prof       0 ; bordo      0 ; resa  79\.4", "resa 79,4"),
 ("15-verifica/risultati_vq3c.txt", r"\(s5\)[\s\S]*?Q3c  F   0 su 90 ; prof       0 ; bordo      0 ; resa  83\.1", "resa 83,1"),
 ("15-verifica/risultati_vq3c.txt", r"\(c\) sparsi 30 %[\s\S]*?Q3c  F   0 su 90 ; prof       0 ; bordo      0 ; resa   8\.0", "resa 8,0"),
 ("15-verifica/risultati_vq3c.txt", r"\(d\) chiazze 30 %[\s\S]*?impronta del suolo, k = 1 pixel \(validazione-2\): F   0 su 90 ; prof      0 ; resa  63\.8 % ; cambi 4\.55", "V-018 a chiazze: 4,55 cambi"),
 ("15-verifica/risultati_vq3c.txt", r"\(d\) chiazze 30 %[\s\S]*?impronta, k = 1 \(validazione-2\): settori-fotogramma 18 ; estensione mediana 1\.5 m", "V-018 a chiazze: 1,5 m"),
 ("04-requisiti/risultati_eventi.txt", r"mancato: 103 \(51\.5 %\)", "eventi mancati 103 su 200"),
 ("04-requisiti/risultati_eventi.txt", r"B3 braccio ingenuo[\s\S]*?\{'USCITA': 200\}", "braccio ingenuo 200"),
 ("04-requisiti/risultati_eventi.txt", r"B4[\s\S]*?'SCOMPARSA_in_fascia': 25", "scomparse spurie 25 su 200 = 12,5 %"),
]
ok = 0
for f, pat, nome in C:
    t = open(os.path.join(R, f), encoding="utf-8").read()
    if f.endswith("av10.txt"):
        r = len(re.findall(r"quota verificata: 0 in 10 fot", t)) == 16 and len(t.strip().splitlines()) == 16
    elif pat is None:
        r = len(re.findall(r"Q3c  F   0 su 90 ; prof       0", t)) == 10
    else:
        r = re.search(pat, t) is not None
    ok += r
    print(("torna    " if r else "NON TORNA"), f, "|", nome)
t = open(os.path.join(R, "04-requisiti/risultati_eventi.txt"), encoding="utf-8").read()
v = re.findall(r'violazioni \(evento "osservato" senza vista vera, o sosta a soggetto nascosto\): 0', t)
print("registro: blocchi con 0 violazioni:", len(v), "(200 scene l'uno)")
print("cifre cercate:", len(C), "; tornano:", ok)
