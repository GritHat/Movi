#!/usr/bin/env python3
# Toglie dal .bib le voci mai citate, aggiunge l'anno dove manca, toglie dalla nota l'indirizzo ripetuto.
import re, glob, os, sys
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
citate = set()
for f in glob.glob(os.path.join(base, 'capitoli', '*.tex')) + [os.path.join(base, 'allegato_tecnico.tex')]:
    for m in re.finditer(r'\\cite[tp]?\*?(?:\[[^\]]*\])*\{([^}]*)\}', open(f, encoding='utf-8').read()):
        citate.update(k.strip() for k in m.group(1).split(','))
p = os.path.join(base, 'allegato.bib'); t = open(p, encoding='utf-8').read()
voci = re.split(r'(?=^@)', t, flags=re.M); out = []; tolte = []; anni = []; url = []
chiavi = set()
for v in voci:
    m = re.match(r'@(\w+)\{([^,]+),', v)
    if not m: out.append(v); continue
    k = m.group(2).strip(); chiavi.add(k)
    if k not in citate: tolte.append(k); continue
    u = re.search(r'^\s*url\s*=\s*\{(.*)\},?\s*$', v, flags=re.M)
    if u and ('\\url{' + u.group(1) + '}') in v:
        v2 = v.replace('\\url{' + u.group(1) + '}, ', '').replace('\\url{' + u.group(1) + '},', '')
        if v2 != v: url.append(k); v = v2
    if not re.search(r'^\s*year\s*=', v, flags=re.M):
        a = '2022' if k == 'st-um3038' else 's.d.'
        v = re.sub(r'^(@\w+\{[^,]+,\n)', r'\1  year = {' + a + '},\n', v, count=1); anni.append(k)
    out.append(v)
open(p, 'w', encoding='utf-8').write(''.join(out))
print('citate:', len(citate), '| nel bib prima:', len(chiavi), '| tolte:', len(tolte), sorted(tolte))
print('citate ma assenti:', sorted(citate - chiavi))
print('anno aggiunto:', len(anni), sorted(anni)); print('nota senza indirizzo ripetuto:', len(url))
