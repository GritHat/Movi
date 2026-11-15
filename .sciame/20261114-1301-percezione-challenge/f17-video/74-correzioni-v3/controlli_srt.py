import re, sys
VIETATE = ["validated", "validat", "guaranteed", "detect and avoid", "threat", "target", "counter-drone", "always", "real time", "real-time", "sub-millisecond", "intercept", "pursue", "chase", "certif", "16 aircraft", "99 %", "99%", "event: collision", "detects the collision", "tested on", "hardware test", "instantly",
          "validato", "garantit", "minaccia", "bersaglio", "sempre", "tempo reale", "intercett", "insegu", "certific", "16 aerei", "rileva la collisione", "istantaneamente", "testato"]
def ts(x):
    h, m, r = x.split(':'); s, ms = r.split(','); return int(h)*3600 + int(m)*60 + int(s) + int(ms)/1000
for p in sys.argv[1:]:
    bl = open(p, encoding='utf-8').read().strip().split('\n\n'); prev = 0; err = []; txt = []
    for k, b in enumerate(bl, 1):
        L = b.split('\n'); a, c = [ts(x.strip()) for x in L[1].split('-->')]
        if L[0].strip() != str(k): err.append(('indice', k))
        if a < prev or c <= a: err.append(('tempo', k))
        prev = c; t = ' '.join(L[2:]); txt.append(t); cps = len(t)/(c-a)
        if cps > 21: err.append(('lettura>21 car/s', k, round(cps, 1)))
    low = ' '.join(txt).lower(); hit = [v for v in VIETATE if v in low]
    print(p, '| cue', len(bl), '| fine ultima', prev, '| errori', err, '| frasi vietate', hit, '| "never"/"mai":', low.count('never'), low.count(' mai '))
