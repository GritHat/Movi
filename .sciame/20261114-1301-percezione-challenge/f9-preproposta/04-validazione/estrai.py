#!/usr/bin/env python3
# Estrae tabelle compatte dai file ris_*.txt del banco (sola lettura dei risultati).
import re, sys, glob
def leggi(f):
    d = {}; b = None
    for r in open(f, encoding='utf-8'):
        r = r.rstrip('\n')
        m = re.match(r'== ([\w-]+): passaggi (\d+), traccia entrata in occlusione (\d+)', r)
        if m: b = m.group(1); d[b] = {'np': int(m.group(2)), 'ntrk': int(m.group(3)), 'bin': {}}; continue
        if b is None: continue
        x = d[b]
        if r.startswith('(e)'):
            n = re.findall(r'-?\d+\.\d+|\bnan\b', r); x['e'] = n  # stima, perso, senza, pass_full, nuc_fr, nuc_full
        elif 'passaggi a «perso»' in r: x['perso'] = re.findall(r'-?\d+\.?\d*|\bnan\b', r)
        elif r.startswith('(a)'): x['a'] = r
        elif 'massa grezza' in r: x['M'] = re.findall(r'-?\d+\.\d+|\bnan\b', r)
        elif 'sosta dominante in' in r: x['dom'] = re.findall(r'[+-]?\d+\.?\d*|\bnan\b', r)
        elif re.match(r'    \d\.\d s ', r):
            p = r.replace('|', ' ').split(); x['bin'][p[0]] = p[2:]
        elif r.startswith('(c)'): x['c'] = re.findall(r'-?\d+\.?\d*|\bnan\b', r)
        elif 'al fotogramma della ricomparsa' in r: x['ck'] = re.findall(r'-?\d+\.\d+|\bnan\b', r.replace('1,73', ''))
        elif 'al fotogramma prima' in r: x['cp'] = re.findall(r'-?\d+\.\d+|\bnan\b', r)
        elif r.startswith('(d)'): x['d'] = re.findall(r'-?\d+\.?\d*|\bnan\b', r)
        elif 'dopo porta violata' in r: x['g'] = re.findall(r'\d+', r)
        elif 'uno-due:' in r: x['due'] = re.findall(r'\d+', r)
    return d
SEZ = 'ebca'
args = sys.argv[1:]
if args and args[0].startswith('-s'): SEZ = args[0][2:]; args = args[1:]
files = args or sorted(glob.glob('ris_*.txt'))
for f in files:
    d = leggi(f); print('\n#####', f)
    if 'e' in SEZ: print('comportamento   | (e) stima% perso% senza% tutta% | nucleo fr% tutta% | perso: n_sig n_coll t | sosta dom n/ntrk, mediana vs tutto-visibile, vs bordo')
    for b, x in (d.items() if 'e' in SEZ else []):
        e = x.get('e', ['nan']*6); p = x.get('perso', ['nan']*3); dm = x.get('dom', [])
        print(f"{b:15s} | {e[0]:>5} {e[1]:>5} {e[2]:>5} {e[3]:>5} | {e[4]:>5} {e[5]:>5} | {p[0]:>4} {p[1]:>3} {p[2]:>5} | {dm[0] if dm else '-':>4}/{x['ntrk']} {dm[3] if len(dm)>3 else '-':>6} {dm[8] if len(dm)>8 else '-':>6}")
    if 'b' in SEZ: print('(b) per fascia: n | stima% | err med/p95 | sig_eff | 1sig 2sig reg95 | reg95>meta\' | nucleo mostrata%/contiene%')
    for b, x in (d.items() if 'b' in SEZ else []):
        for t, p in x['bin'].items():
            # p: n stima perso senza errmed errp95 seff in1 in2 in173 hdr wf w50 mlow nuc nucc
            print(f"  {b:14s} {t}s n {p[0]:>4} | {p[1]:>5} | {p[4]:>6}/{p[5]:>6} | {p[6]:>6} | {p[7]:>5} {p[8]:>5} {p[10]:>5} | {p[12]:>5} | {p[14]:>5}/{p[15]:>5}")
    if 'c' in SEZ: print('(c) ricomparsa: n con stima (senza traccia, gia\' perso) t_occ | err med p95 sig_eff | k: 1sig [..] 2sig [lo;hi] reg95 [lo;hi] | k-1: 2sig reg95 sosta-dom% nucleo-area% | porta dentro% violata% KF95% geo-nucleo% | fantasma a fine/violata')
    for b, x in (d.items() if 'c' in SEZ else []):
        if 'c' not in x or x['c'][0] == '0': continue
        c = x['c']; ck = x['ck']; cp = x['cp']; dd = x['d']; g = x.get('g', [])
        print(f"  {b:14s} n {c[0]:>4} ({c[1]},{c[2]}) t {c[3]} | {c[4]} {c[6]} {c[7]} | {ck[0]} [{ck[1]};{ck[2]}] {ck[3]} [{ck[4]};{ck[5]}] {ck[9]} [{ck[10]};{ck[11]}] | {cp[1]} {cp[4]} {cp[5]} {cp[6]} | {dd[2]} {dd[4]} {dd[6]} {dd[9]} | {g[0] if g else '-'}/{g[1] if g else '-'}")
    for b, x in d.items():
        if 'due' in x: print('  uno-due: mai visto per primo', x['due'][0], '| identita\' passata senza segnale', x['due'][1], '| possibile presenza caduta con A nascosto: passaggi', x['due'][2], 'fotogrammi', x['due'][3])
    if 'a' in SEZ: print('(a) / M')
    for b, x in (d.items() if 'a' in SEZ else []):
        a = re.findall(r'-?\d+\.?\d*|\bnan\b', x.get('a', '')); m = x.get('M', [])
        # a: n_est, 95, estlib, 95(skip)...
        print(f"  {b:14s} {x.get('a','')[4:]}  | M<0.05: {m}")
