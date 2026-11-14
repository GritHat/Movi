#!/usr/bin/env python3
"""riconta_arbitro.py - riconteggio dell'arbitro sulle uscite di f12 (sola lettura; nessun codice altrui importato).
Uso: python -I -B riconta_arbitro.py <cartella f12-integrazione>"""
import sys, os, glob, json, math, collections
F = sys.argv[1]
def wil(k, n, z=1.959964):
    if n == 0: return float('nan')
    p = k/n; d = 1+z*z/n; c = p+z*z/(2*n); h = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n)); return (c-h)/d
def wup(k, n, z=1.959964):
    p = k/n; d = 1+z*z/n; c = p+z*z/(2*n); h = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n)); return (c+h)/d
# ---------- 1. prova d'insieme (righe R)
R = []
for f in sorted(glob.glob(os.path.join(F, '02-prova-insieme/ris/*.txt'))):
    for ln in open(f, encoding='utf-8'):
        if ln.startswith('R '):
            d = {}
            for tok in ln.split()[1:]:
                k, _, v = tok.partition('=')
                try: d[k] = float(v) if ('.' in v or 'nan' in v) else int(v)
                except ValueError: d[k] = v
            d['file'] = os.path.basename(f)[:-4]; R.append(d)
print('1. PROVA D\'INSIEME: file con righe R:', len({r['file'] for r in R}), 'righe R:', len(R))
PERC = ('prosegue', 'rallenta', 'sosta', 'torna', 'sostalunga')
print('   comportamenti visti:', sorted({r['beh'] for r in R}))
for c7 in (1, 0):
    rows = [r for r in R if r['file'].startswith('a_') and r['c7'] == c7]
    den = sum(r['n']-r['mai_nasc'] for r in rows)
    print(f"   a) c7={c7}: lanciati {sum(r['n'] for r in rows)}, nascosti {den}, vuoti {sum(r['gap_p'] for r in rows)}, "
          f"scoperti conf {sum(r['scop_p'] for r in rows)} + non conf {sum(r['nc_scop'] for r in rows)}")
rows = [r for r in R if r['file'].startswith('a_') and r['c7'] == 1]
print(f'      limite sup. Wilson 95 % di 0 su 6000 camminatori distinti: {1e4*wup(0, 6000):.2f} su 10 000; di 0 su 23 402: {1e4*wup(0, 23402):.2f}')
tutti = sum(r['validi'] for r in R); print('   tutti i lanci: validi', tutti, ' vuoti', sum(r['gap_p'] for r in R), ' fuori R100 (passaggi)', sum(r['fuori100_p'] for r in R))
for g in 'DTL':
    rr = [r for r in R if r['file'] == f'b_{g}_percorso']
    peg = {}
    for h in (1, 2, 3):
        for mis, (kn, kk) in {'sec': ('nT', 'inT'), 'prim': ('nD', 'inD')}.items():
            for r in rr:
                n, k = r[f'{kn}{h}'], r[f'{kk}{h}']
                w = wil(k, n)
                key = (mis, 'fino a 2 s' if h < 3 else '3 s')
                if n >= 400 and (key not in peg or w < peg[key][0]): peg[key] = (w, k, n, r['beh'], h)
    print(f'   b) {g}: comportamenti', [r['beh'] for r in rr], '| celle peggiori (n>=400):',
          {k: f'{v[1]}/{v[2]}={v[0]:.3f} ({v[3]}, {v[4]} s)' for k, v in sorted(peg.items())})
    sopra = sum(1 for r in rr for h in (1, 2, 3) if r[f'nT{h}'] >= 400 and wil(r[f'inT{h}'], r[f'nT{h}']) >= (0.90 if h < 3 else 0.85))
    print(f'      {g}: celle secondarie sopra soglia: {sopra} su {len(rr)*3}')
for g in 'DTL':
    for c1 in ('si', 'no'):
        rr = [r for r in R if r['file'] == f'd_{g}_c1{c1}']
        k = sum(r['es_id'] for r in rr); n = sum(r['es_id']+r['es_amb'] for r in rr)
        print(f'   d) estraneo {g} c1={c1}: identita\' sbagliata {k}/{n} = {k/n:.3f}' if n else f'   d) {g} {c1}: n=0')
for g in 'DTL':
    rr = [r for r in R if r['file'].startswith(f'a_{g}_') and r['c7'] == 1 and r['beh'] in PERC]
    k = sum(r['riagg'] for r in rr); n = sum(r['ricomp'] for r in rr)
    print(f'   f) riaggancio {g} (a_, c7=1): {k}/{n} = {k/n:.4f}, Wilson inf {wil(k, n):.3f}')
# ---------- 2. libero della cella
print('2. LIBERO DELLA CELLA')
for nome in ('banco.json', 'banco_semi2.json'):
    d = json.load(open(os.path.join(F, '03-libero', nome)))
    NF = d['NF']; reg = collections.Counter(r['regola'] for r in d['righe'])
    print('   ', nome, 'NF', NF, 'righe', len(d['righe']), 'regole', dict(reg))
    for regola in sorted(reg):
        rr = [r for r in d['righe'] if r['regola'] == regola and abs(r['err']) <= 0.5]
        cond = len(rr); viol = sum(r['fot_viol'] for r in rr); celle = sum(r['dentro']+r['nascoste'] for r in rr)
        r1 = [r for r in d['righe'] if r['regola'] == regola and abs(r['err']) > 0.5]
        print(f"      {regola:8s} |err|<=0,5: condizioni {cond}, fotogrammi {cond*NF}, fot. con violazione {viol}, celle {celle}"
              f" | |err|=1: cond {len(r1)}, fot. viol {sum(r['fot_viol'] for r in r1)}")
    for r in d['righe']:
        if r['scena'] == 'stanza vuota' and r['buchi'] != 'nessuno' and r['regola'] == 'PR4' and r['err'] in (0.0, 0.5) and '5' in str(r['buchi']) and '30' not in str(r['buchi']):
            print(f"      PR4 stanza vuota k={r['k']} err={r['err']} buchi={r['buchi']}: mediana {r['mediana_m']:.1f} m, resa {r['resa']:.1f} %, sconosciuto {r['sconosciuto']}")
# ---------- 3. identita' e controprova
print('3. IDENTITA\' (06) E CONTROPROVA (07), configurazione tutte_p, D435i nominale')
def leggi(p):
    return [json.loads(l) for l in open(p, encoding='utf-8') if l.strip()]
tot = collections.Counter()
for nome in ('06-identita/risultati/nuovi424.jsonl', '06-identita/risultati/nuovi848.jsonl',
             '07-controprova-identita/risultati/ultimi424_replica.jsonl', '07-controprova-identita/risultati/ultimi848_replica.jsonl'):
    righe = [r for r in leggi(os.path.join(F, nome)) if r.get('conf') == 'tutte_p' and r.get('profilo') == 'd435i' and r.get('livello') == 'nominale']
    out = {}
    for t in ('a12', 'a05', 'b'):
        rr = [r for r in righe if r.get('tipo') == t]
        out[t] = (sum(1 for r in rr if r.get('continuita_pulita')), len(rr))
    lar = righe[0]['larghezza'] if righe else '?'
    k = sum(v[0] for v in out.values()); n = sum(v[1] for v in out.values()); tot[lar, 'k'] += k; tot[lar, 'n'] += n
    pass_ = [r for r in righe if 'cella_centro_nascosto' in r]
    nas = sum(r['nascosti'] for r in pass_); fuori = sum(r['nascosti']-r['cella_centro_nascosto']['possibile_presenza']-r['cella_centro_nascosto']['occupato'] for r in pass_)
    lib = sum(r['cella_centro_nascosto']['libero'] for r in pass_); lio = sum(r.get('libero_in_ombra', 0) for r in righe)
    print(f"   {nome.split('/')[-1]:28s} {lar} px: {out} somma {k}/{n}; nascosti {nas}, non in avviso ne' occupato {fuori}, su libero {lib}; libero in ombra {lio}; acceso alla fine {sum(1 for r in pass_ if r.get('avviso_acceso_alla_fine'))}/{len(pass_)}")
for lar in (424, 848):
    k, n = tot[lar, 'k'], tot[lar, 'n']
    if n: print(f'   somma autore + replica a {lar} px: {k}/{n} = {k/n:.3f}  Wilson 95 % [{wil(k, n):.3f}; {wup(k, n):.3f}]')
for nome in ('att_rotto', 'att_estraneo', 'att_geometria', 'att_persona', 'att_rumore', 'att_bordo2'):
    righe = [r for r in leggi(os.path.join(F, '07-controprova-identita/risultati', nome+'.jsonl')) if r.get('conf') == 'tutte_p']
    grp = collections.defaultdict(list)
    for r in righe: grp[r.get('gruppo', r.get('tipo'))].append(r)
    for g, rr in sorted(grp.items()):
        s = f"   {nome}: {g}: n={len(rr)}"
        if any('continuita_pulita' in r for r in rr): s += f", continuita' {sum(1 for r in rr if r.get('continuita_pulita'))}"
        if any('gruppo_sul_bersaglio' in r for r in rr): s += f", gruppo sul bersaglio {sum(r['gruppo_sul_bersaglio'] for r in rr)}/{sum(r['fotogrammi'] for r in rr)}"
        altri = sorted({k for r in rr for k in r if 'rimo' in k or 'avviso' in k or 'estr' in k or 'identita' in k})
        for k in altri:
            vals = collections.Counter(json.dumps(r.get(k), ensure_ascii=False)[:40] for r in rr); s += f"; {k}: {dict(vals.most_common(3))}"
        print(s[:420])
