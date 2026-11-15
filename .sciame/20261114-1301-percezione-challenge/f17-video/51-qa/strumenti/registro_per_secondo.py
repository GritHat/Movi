"""QA: per ogni secondo intero delle scene «Simulation», lo stato del registro _v3 al tempo corrispondente.
Uso: python3 -I registro_per_secondo.py <scene_tempi.js> <radice_repo> <cartella_ocr>
Stampa: t_video, scena, t_reg, tracce (id:stato:non_vista_da), n avvisi possibile_presenza, eventi, detriti, e i gettoni OCR."""
import json, sys, os, re, bisect
st = open(sys.argv[1]).read(); st = json.loads(st[st.index('{'):st.rindex('}')+1])
root = sys.argv[2]; ocr = sys.argv[3]
cache = {}
def reg(name):
    if name in cache: return cache[name]
    f = os.path.join(root, 'video/progetto', st['registri'][name]['file'])
    f = os.path.normpath(f)
    fr = [json.loads(l) for l in open(f) if '"fotogramma"' in l[:40]]
    fr.sort(key=lambda d: d['t']); cache[name] = ([d['t'] for d in fr], fr); return cache[name]
for sc in st['scene']:
    if sc.get('onesta') != 'sim': continue
    for k in range(int(sc['inizio'])+1, int(sc['inizio']+sc['durata'])+1):
        t = k - sc['inizio']
        seg = [s for s in sc.get('segmenti', []) if s['da'] <= t < s['a']]
        if not seg: print(f"{k:4d} s{sc['n']} (fuori segmento)"); continue
        s = seg[0]; tr = s['t_reg'] + (t - s['da'])*s['velocita']
        ts, fr = reg(s['registro']); i = max(0, bisect.bisect_right(ts, tr)-1); d = fr[i]
        tracce = ' '.join(f"{x.get('id')}:{x.get('stato')}:{x.get('non_vista_da_s')}" for x in d.get('tracce') or [])
        av = sum(1 for a in d.get('avvisi') or [] if 'presenza' in str(a.get('tipo')))
        ev = ','.join(f"{e.get('tipo')}@{e.get('da_s')}" for e in d.get('eventi') or [])
        det = d.get('detriti') or {}
        aff = ','.join(f"{a.get('sensore')}:{a.get('stato')}" for a in d.get('affidabilita_per_sensore') or [] if a.get('stato') not in ('ok','affidabile'))
        lib = len(d.get('libero_per_classi') or [])
        o = open(os.path.join(ocr, f"f_{k+1:03d}.txt")).read() if os.path.exists(os.path.join(ocr, f"f_{k+1:03d}.txt")) else ''
        tok = ' '.join(re.findall(r"(?:NOT SEEN[^A-Z]{0,12}|SEEN|POSSIBLE PRESENCE[^A-Za-z]{0,6}|EVENT[^a-z]{0,40}|RELIABILITY LOST[^a-z]{0,10}|radius [0-9.,]+ ?k?m)", o))
        print(f"{k:4d} s{sc['n']} reg={d['t']:6.2f} tr=[{tracce}] pp={av} ev=[{ev}] det_r={det.get('raggio_volume_m')} imp={det.get('impronta_raggio_m')} aff=[{aff}] lib={lib} || OCR: {tok[:200]}")
