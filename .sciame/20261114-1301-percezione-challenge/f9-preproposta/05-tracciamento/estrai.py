#!/usr/bin/env python3
# estrai.py FILE chiave1 chiave2 ... : stampa, per scenario e braccio, i contatori che contengono una delle chiavi
import sys
f = sys.argv[1]; keys = sys.argv[2:]; mode = ''
for l in open(f):
    l = l.rstrip('\n')
    if l.startswith('==') or l.startswith('#'):
        print(l); continue
    if l.startswith(' ['):
        mode = l[2:14].strip()
    its = [x for x in l.replace('porte alla prima occasione: ', '').split('] ')[-1].strip().split(' ; ') if any(k in x for k in keys)]
    if its:
        print('   %-12s %s' % (mode, ' ; '.join(its)))
