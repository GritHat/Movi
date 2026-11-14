#!/usr/bin/env python3
# riconta_insieme.py — sciame-statistico, f12. Riconta dai file grezzi ris/<lancio>.txt (righe "R k=v ...") della prova d'insieme.
# Uso: python -I -B riconta_insieme.py <cartella ris>   (solo lettura; scrive su stdout)
import sys, os, glob, math
from statistics import NormalDist
def wil(k, n, z=1.959964):
    if n == 0: return (float('nan'),) * 2
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c - h) / d, (c + h) / d
def leggi(cart):
    R = []
    for f in sorted(glob.glob(os.path.join(cart, '*.txt'))):
        for riga in open(f, encoding='utf-8', errors='replace'):
            if riga.startswith('R '):
                d = {}
                for t in riga.split()[1:]:
                    if '=' in t:
                        k, v = t.split('=', 1); d[k] = v
                d['file'] = os.path.basename(f)[:-4]; R.append(d)
    return R
I = lambda d, k: int(d[k])
R = leggi(sys.argv[1]); print('righe R lette:', len(R), 'in', len({r['file'] for r in R}), 'file')
# (a) continuita'
for c7 in ('1', '0'):
    A = [r for r in R if r['file'].startswith('a_') and r['file'].endswith('c7' + c7)]
    semi = sum(I(r, 'n') for r in A); val = sum(I(r, 'validi') for r in A); nc = sum(I(r, 'nonconf') for r in A); mn = sum(I(r, 'mai_nasc') for r in A)
    gap = sum(I(r, 'gap_p') for r in A); sc = sum(I(r, 'scop_p') for r in A); ncs = sum(I(r, 'nc_scop') for r in A)
    print(f'(a) c7={c7}: righe {len(A)} semi {semi} = validi {val} + nonconf {nc} + mai_nascosti {mn} (somma {val+nc+mn}); vuoti {gap}; scoperti confermati {sc} + non confermati {ncs} = {sc+ncs} su {val+nc}; Wilson sup {wil(sc+ncs, val+nc)[1]:.5f}; vuoti sup {wil(gap, val+nc)[1]:.5f}')
    for pd in ('0.90', '0.70'):
        for rb in ('0.225', '0.000'):
            B = [r for r in A if r['pd'] == pd and r['rb'] == rb]
            k = sum(I(r, 'scop_p') + I(r, 'nc_scop') for r in B); n = sum(I(r, 'validi') + I(r, 'nonconf') for r in B)
            print(f'     pd={pd} rb={rb}: scoperti {k}/{n} [Wilson {wil(k,n)[0]:.5f}-{wil(k,n)[1]:.5f}]')
tot = sum(I(r, 'validi') + I(r, 'nonconf') for r in R); g = sum(I(r, 'gap_p') for r in R)
print(f'tutti i lanci: passaggi (validi+nonconf) {tot}, solo validi {sum(I(r,"validi") for r in R)}, vuoti {g}; cicli nascosti {sum(I(r,"hid_all") for r in R)}, fuori R100 cicli {sum(I(r,"f100c") for r in R)} passaggi {sum(I(r,"fuori100_p") for r in R)}')
# (b) precisione
perc = ['prosegue', 'rallenta', 'sosta', 'torna', 'sostalunga']
zb = {}
print('(b) celle sul percorso: geo beh s | primaria k/n W | secondaria k/n W W_bonf30 | quota passaggi nel denominatore (n secondaria / semi)')
peggio = {}
for g in 'DTL':
    for r in [r for r in R if r['file'] == f'b_{g}_percorso']:
        for s in '123':
            kp, np_, ks, ns = I(r, 'inD' + s), I(r, 'nD' + s), I(r, 'inT' + s), I(r, 'nT' + s)
            zB = NormalDist().inv_cdf(1 - 0.025 / 30)
            print(f"  {g} {r['beh']:10s} {s} | {kp}/{np_} {wil(kp,np_)[0]:.3f} | {ks}/{ns} {wil(ks,ns)[0]:.3f} {wil(ks,ns,zB)[0]:.3f} | {ns/I(r,'n'):.2f}  prim_bonf {wil(kp,np_,zB)[0]:.3f}")
            for nome, k, n in (('prim', kp, np_), ('sec', ks, ns)):
                peggio.setdefault((g, s, nome), []).append((wil(k, n)[0], wil(k, n, zB)[0], r['beh'], k, n))
print('    z di Bonferroni per 30 celle:', round(NormalDist().inv_cdf(1 - 0.025 / 30), 3))
for g in 'DTL':
    for nome in ('prim', 'sec'):
        for s in '123':
            v = [x for x in peggio[(g, s, nome)]]; so = 0.90 if s in '12' else 0.85
            v4 = [x for x in v if x[4] >= 400]
            m = min(v4) if v4 else None
            print(f'  {g} {nome} {s} s: celle n>=400: {len(v4)}/5; sopra soglia {so}: Wilson {sum(x[0]>=so for x in v4)}, Bonferroni {sum(x[1]>=so for x in v4)}; peggiore {m}')
for g in 'DTL':
    for s in '123':
        rr = [r for r in R if r['file'] == f'b_{g}_percorso']
        ks = sum(I(r, 'inT' + s) for r in rr); ns = sum(I(r, 'nT' + s) for r in rr); kp = sum(I(r, 'inD' + s) for r in rr); np_ = sum(I(r, 'nD' + s) for r in rr); se = sum(I(r, 'n') for r in rr)
        print(f'  {g} insieme {s} s: primaria {kp}/{np_}={kp/np_:.3f} W {wil(kp,np_)[0]:.3f}; secondaria {ks}/{ns}={ks/ns:.3f} W {wil(ks,ns)[0]:.3f}; nel denominatore {ns}/{se}={ns/se:.2f}; primaria/secondaria {np_/ns:.2f}')
# (f) identita'
for g in 'DTL':
    rr = [r for r in R if r['file'] == f'b_{g}_percorso']; k = sum(I(r, 'riagg') for r in rr); n = sum(I(r, 'ricomp') for r in rr)
    print(f'(f) {g}: riagganci {k}/{n}={k/n:.4f} W {wil(k,n)[0]:.4f}; mancati per distanza {sum(I(r,"f_dist") for r in rr)} bordo {sum(I(r,"f_bordo") for r in rr)} M7 {sum(I(r,"amb_m7") for r in rr)}')
# (d) estraneo
for g in 'DTL':
    for c in ('si', 'no'):
        rr = [r for r in R if r['file'] == f'd_{g}_c1{c}']
        s = {k: sum(I(r, k) for r in rr) for k in ('es_n', 'es_id', 'es_ril', 'es_amb', 'es_na', 'es_mai', 'es_ampio', 'n')}
        print(f"(d) {g} c1={c}: {s}  id/n={s['es_id']/max(1,s['es_n']):.3f} W {wil(s['es_id'],s['es_n'])[0]:.3f}-{wil(s['es_id'],s['es_n'])[1]:.3f}")
# (c) K-215
for r0 in sorted({r['file'] for r in R if r['file'].startswith('c_')}):
    rr = [r for r in R if r['file'] == r0]
    out = []
    for s in '123':
        k = sum(I(r, 'inT' + s) for r in rr); n = sum(I(r, 'nT' + s) for r in rr); out.append(f'{k}/{n}={k/n:.3f}[{wil(k,n)[0]:.3f}]')
    sc = sum(I(r, 'scop_p') + I(r, 'nc_scop') for r in rr); nn = sum(I(r, 'validi') + I(r, 'nonconf') for r in rr)
    print('(c)', r0, ' '.join(out), f'scoperti {sc}/{nn}')
