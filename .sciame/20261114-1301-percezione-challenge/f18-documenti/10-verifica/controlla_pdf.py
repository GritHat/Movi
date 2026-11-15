"""Cerca nel testo estratto dal PDF riferimenti interni, frasi da non dire e cifre superate (VERDETTO_2C)."""
import re, subprocess, sys
INTERNI = [r'sciame', r'arbitr', r'coordinator', r'\bK-?\d{3}', r'\bH\d+\b', r'\bF\d{1,2}\b', r'verdett', r'\bfase 2[bc]?\b',
           r'\.md\b', r'\bv[123]\b', r'riprova', r'controprova', r'agent[ie] ', r'\bruol[oi]\b', r'falsificat', r'\bnucleo v']
NONDIRE = [r'validat', r'tempo reale', r'certificabil', r'detect and avoid', r'122 droni', r'zero falsi', r'contiene sempre',
           r'46 km', r'59 km', r'si restring', r'avvisa solo', r'tutte le correzioni', r'mai libero ciò che non ha',
           r'individua chi', r'ingaggi', r'neutralizz', r'abbatt', r'counter', r'threat', r'sempre entro']
SUPERATE = [r'163', r'85 su 85', r'49 su 60', r'49/60', r'42\s?km', r'74\s?km', r'oltre 10\s?km', r'36 su 60', r'24 su 30',
            r'2,2 s', r'12,5 s', r'dichiarata completa per impostazione', r'come fa oggi il prototipo', r'665 s',
            r'copre il sito', r'troppo ampia', r'enorme']
def main(pdf):
    t = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True, timeout=60).stdout
    t1 = re.sub(r'-\n\s*', '', t)
    righe = t1.split('\n')
    for nome, lista in (('INTERNI', INTERNI), ('NONDIRE', NONDIRE), ('SUPERATE', SUPERATE)):
        n = 0
        for i, r in enumerate(righe):
            for p in lista:
                if re.search(p, r, re.I if nome != 'SUPERATE' else 0):
                    n += 1; print(f'{nome}\t{p}\triga {i+1}\t{r.strip()[:150]}')
        print(f'## {nome}: {n}')
main(sys.argv[1])
