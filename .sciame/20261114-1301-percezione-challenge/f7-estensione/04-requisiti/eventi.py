#!/usr/bin/env python3
"""Strato minimo di eventi sopra gli stati del nucleo: controllo della logica (sciame-requisiti, f7).

Rifare:  timeout 120 python3 -I eventi.py > risultati_eventi.txt
Python puro, seme fissato. Tre parti separate:
  1. NUCLEO RIDOTTO  - una riduzione delle regole di SOLUZIONE_V2.md (B5), NON il nucleo;
  2. ESTRATTORE      - legge solo il flusso di stati (mai la verita');
  3. ORACOLO         - confronta gli eventi con il copione vero della scena.
"""
import math, random, statistics, sys, time

HZ = 15.0; DT = 1 / HZ
FOV = math.radians(87 / 2); RMIN = 1.24; RMAX = 3.0
FASCIA = 0.40; YP = 1.7; YL = 2.3; T_PREV = 0.65; SIGMA = 0.03
LETTURA2 = len(sys.argv) > 1 and sys.argv[1] == '2'   # [dopo] seconda lettura, scritta dopo il lancio 1


# ------------------------------------------------------------------ geometria (comune)
def in_campo(p):
    r = math.hypot(p[0], p[1])
    return RMIN <= r <= RMAX and abs(math.atan2(p[0], p[1])) <= FOV

def in_ombra(p, xc):
    return p[1] > YP and (xc - 0.5) <= p[0] * YP / p[1] <= (xc + 0.5)

def _dseg(p, a, b):
    ax, ay = a; bx, by = b; dx, dy = bx - ax, by - ay
    u = max(0.0, min(1.0, ((p[0] - ax) * dx + (p[1] - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(p[0] - ax - u * dx, p[1] - ay - u * dy)

def dist_ombra(p, xc):
    if in_ombra(p, xc):
        return 0.0
    a = (xc - 0.5, YP); b = (xc + 0.5, YP); k = 4.0 / YP
    return min(_dseg(p, a, b), _dseg(p, a, (a[0] * k, a[1] * k)), _dseg(p, b, (b[0] * k, b[1] * k)))

def in_rett(p, z):
    return z[0] <= p[0] <= z[1] and z[2] <= p[1] <= z[3]


# ------------------------------------------------------------------ 1. nucleo ridotto
class NucleoRidotto:
    """Stati per traccia: osservato / non_confermato / previsto / perso. Regione di possibile presenza
    (cuneo dell'occlusore + fascia) accesa da quando la traccia entra nell'ombra a quando e' rivista."""
    def __init__(self, xc):
        self.xc = xc; self.prox = 1; self.tr = None; self.cand = 0; self.vuoti = 0; self.storia = []; self.pend = []

    def passo(self, t, mis, coperto):
        chiuse = []
        self.vuoti = self.vuoti + 1 if coperto else 0
        aff = self.vuoti < 2                      # 2 fotogrammi senza dato: affidabilita' persa
        tr = self.tr
        if not aff:
            if tr and tr['stato'] in ('osservato', 'non_confermato'):
                chiuse.append((tr['id'], 'affidabilita')); self.tr = tr = None
            self.cand = 0
        elif mis is not None:
            if tr and tr['stato'] in ('previsto', 'perso'):
                if dist_ombra(mis, self.xc) <= FASCIA:        # riaggancio solo accanto all'ombra d'ingresso
                    tr.update(stato='osservato', pos=mis, t_mis=t, nc=0); self.storia = [(t, mis)]
                elif LETTURA2:                                # [dopo] la pendente resta, nasce una traccia nuova
                    self.cand += 1
                    if self.cand >= 4:
                        self.pend.append(tr)
                        self.tr = tr = dict(id=self.prox, stato='osservato', pos=mis, t_mis=t, nc=0)
                        self.prox += 1; self.cand = 0; self.storia = [(t, mis)]
            elif tr:
                tr.update(stato='osservato', pos=mis, t_mis=t, nc=0); self.storia.append((t, mis))
            else:
                self.cand += 1
                if self.cand >= 4:                            # visto almeno 4 fotogrammi
                    self.tr = tr = dict(id=self.prox, stato='osservato', pos=mis, t_mis=t, nc=0)
                    self.prox += 1; self.cand = 0; self.storia = [(t, mis)]
        elif tr:
            if tr['stato'] == 'osservato':
                if dist_ombra(tr['pos'], self.xc) <= FASCIA:  # ultima misura accanto all'ombra dell'occlusore
                    tr['stato'] = 'previsto'
                else:
                    tr['stato'] = 'non_confermato'; tr['nc'] = 1
            elif tr['stato'] == 'non_confermato':
                tr['nc'] += 1
                if tr['nc'] > 3:
                    chiuse.append((tr['id'], 'non_piu_rilevato')); self.tr = tr = None
            elif tr['stato'] == 'previsto' and t - tr['t_mis'] >= T_PREV:
                tr['stato'] = 'perso'
        vel = None
        if tr and tr['stato'] == 'osservato':
            self.storia = [s for s in self.storia if t - s[0] <= 1.0]
            if t - self.storia[0][0] >= 0.8:
                (t0, p0), (t1, p1) = self.storia[0], self.storia[-1]
                vel = math.hypot(p1[0] - p0[0], p1[1] - p0[1]) / (t1 - t0)
        tracce = [dict(tr, vel=vel)] if tr else []
        regioni = [dict(id=tr['id'], eta=t - tr['t_mis'], chiave=self.xc)] if tr and tr['stato'] in ('previsto', 'perso') else []
        for q in self.pend:                               # [dopo] pendenti rimaste senza riaggancio: mai tolte
            q['stato'] = 'perso'; tracce.append(dict(q, vel=None)); regioni.append(dict(id=q['id'], eta=t - q['t_mis'], chiave=self.xc))
        return dict(t=t, aff_ok=aff, causa=None if aff else 'sensore', tracce=tracce, regioni=regioni, chiuse=chiuse)


# >>> ESTRATTORE
K = 3; T_PERM = 5.0; V_SOSTA = 0.2; T_SOSTA = 2.0

class Eventi:
    """Legge un fotogramma di stati alla volta e restituisce gli eventi. Ogni evento porta l'ora e lo
    stato della conoscenza: 'osservato', 'previsto' o 'sconosciuto'. Regola unica: un evento 'osservato'
    nasce solo in un fotogramma in cui la traccia ha una misura; cio' che accade senza misura non e'
    mai 'uscita' ne' 'ingresso': e' 'possibile presenza', 'permanenza non osservata' o 'non noto'."""
    def __init__(self, zone, in_regione, k_nasc=K, ingenuo=False):
        self.zone = zone; self.in_regione = in_regione; self.k_nasc = k_nasc; self.ingenuo = ingenuo
        self.aff_ok = True; self.tr = {}; self.reg = {}; self.tocca = {}

    def _ev(self, out, t, tipo, stato, traccia=None, zona=None, **altro):
        out.append(dict(t=t, tipo=tipo, stato=stato, traccia=traccia, zona=zona, **altro))

    def _zone_toccate(self, chiave):
        if chiave not in self.tocca:                      # griglia 5x5 per zona, una volta per regione
            self.tocca[chiave] = [n for n, z in self.zone.items() if any(
                self.in_regione(chiave, (z[0] + (z[1] - z[0]) * i / 4, z[2] + (z[3] - z[2]) * j / 4))
                for i in range(5) for j in range(5))]
        return self.tocca[chiave]

    def passo(self, f):
        out = []; t = f['t']
        if self.aff_ok and not f['aff_ok']:
            self._ev(out, t, 'AFFIDABILITA_PERSA', 'sconosciuto', causa=f['causa'])
            for tid, s in self.tr.items():
                for n, st in s['zona'].items():
                    if st == 'oss':
                        s['zona'][n] = 'ignoto'; self._ev(out, t, 'IN_ZONA_NON_NOTO', 'sconosciuto', tid, n)
        elif f['aff_ok'] and not self.aff_ok:
            self._ev(out, t, 'AFFIDABILITA_RITROVATA', 'osservato')
        self.aff_ok = f['aff_ok']
        if not self.aff_ok:
            return out                                    # a sensore cieco non nasce nessun altro evento
        for tid, causa in f['chiuse']:
            s = self.tr.pop(tid, None)
            self._ev(out, t, 'TRACCIA_CHIUSA', 'sconosciuto', tid, causa=causa)
            for n, st in (s['zona'].items() if s else ()):
                if st == 'oss':
                    self._ev(out, t, 'IN_ZONA_NON_NOTO', 'sconosciuto', tid, n)
        for tr in f['tracce']:
            tid = tr['id']
            s = self.tr.setdefault(tid, dict(zona={n: 'fuori' for n in self.zone}, dentro={n: 0 for n in self.zone},
                                             fuori={n: 0 for n in self.zone}, nasc=0, emessa=False, t_nasc=None,
                                             t_fermo=None, sosta=False))
            if tr['stato'] == 'osservato':
                if s['emessa']:
                    self._ev(out, t, 'RICOMPARSA', 'osservato', tid, durata=t - s['t_nasc'])
                    for n, st in s['zona'].items():
                        if st == 'non_oss':
                            s['zona'][n] = 'oss' if in_rett(tr['pos'], self.zone[n]) else 'fuori'
                s['nasc'] = 0; s['emessa'] = False
                for n, z in self.zone.items():
                    if in_rett(tr['pos'], z):
                        s['dentro'][n] += 1; s['fuori'][n] = 0
                    else:
                        s['fuori'][n] += 1; s['dentro'][n] = 0
                    if s['zona'][n] in ('fuori', 'ignoto') and s['dentro'][n] >= K:
                        visto_fuori = s['zona'][n] == 'fuori' and s.get('vf_' + n, False)
                        s['zona'][n] = 'oss'
                        self._ev(out, t, 'INGRESSO' if visto_fuori else 'PRESENTE', 'osservato', tid, n)
                    elif s['zona'][n] == 'oss' and s['fuori'][n] >= K:
                        s['zona'][n] = 'fuori'; self._ev(out, t, 'USCITA', 'osservato', tid, n)
                    if s['fuori'][n] >= 1:
                        s['vf_' + n] = True
                if tr['vel'] is not None and tr['vel'] < V_SOSTA:
                    s['t_fermo'] = t if s['t_fermo'] is None else s['t_fermo']
                    if not s['sosta'] and t - s['t_fermo'] >= T_SOSTA:
                        s['sosta'] = True
                        zona = next((n for n, st in s['zona'].items() if st == 'oss'), None)
                        self._ev(out, t, 'SOSTA', 'osservato', tid, zona, da=s['t_fermo'])
                elif tr['vel'] is not None:
                    s['t_fermo'] = None; s['sosta'] = False
            elif tr['stato'] in ('previsto', 'perso'):
                s['nasc'] += 1
                if self.ingenuo:                          # braccio che deve fallire
                    for n, st in s['zona'].items():
                        if st == 'oss':
                            s['zona'][n] = 'fuori'; self._ev(out, t, 'USCITA', 'osservato', tid, n)
                if s['nasc'] >= self.k_nasc and not s['emessa']:
                    s['emessa'] = True; s['t_nasc'] = tr['t_mis']
                    self._ev(out, t, 'SCOMPARSA', 'previsto', tid, ultima_misura=tr['t_mis'])
                    for n, st in s['zona'].items():
                        if st == 'oss':
                            s['zona'][n] = 'non_oss'      # NON e' un'uscita
        vive = set()
        for r in f['regioni']:
            vive.add(r['id'])
            s = self.tr.get(r['id'])
            if not s or not s['emessa']:
                continue
            g = self.reg.setdefault(r['id'], dict(annunciata=False, perm=False))
            if not g['annunciata']:
                g['annunciata'] = True
                for n in self._zone_toccate(r['chiave']):
                    self._ev(out, t, 'POSSIBILE_PRESENZA_IN_ZONA', 'sconosciuto', r['id'], n)
            if not g['perm'] and r['eta'] >= T_PERM:
                g['perm'] = True
                self._ev(out, t, 'PERMANENZA_NON_OSSERVATA', 'sconosciuto', r['id'], eta=r['eta'],
                         nota='puo aver lasciato l area')
        for tid in [k for k in self.reg if k not in vive]:
            del self.reg[tid]
        return out
# <<< ESTRATTORE


# ------------------------------------------------------------------ 3. scene e oracolo
def scena(seme, tipo, pd):
    rng = random.Random(seme)
    v = rng.uniform(0.5, 1.4); xc = rng.uniform(-0.05, 0.05); xs = xc * YL / YP
    pos = []; x = -2.4
    def cammina(fino):
        nonlocal x
        while x < fino:
            pos.append((x, YL)); x += v * DT
    t_stop = None
    if tipo in ('T', 'C'):
        cammina(2.4)
    elif tipo == 'S':
        cammina(xs); pos += [(x, YL)] * int(rng.uniform(1, 20) * HZ); cammina(2.4)
    elif tipo == 'L':
        cammina(xs); r = math.hypot(x, YL); ux, uy = x / r, YL / r
        while r < 3.4:
            pos.append((ux * r, uy * r)); r += v * DT
        pos += [(ux * r, uy * r)] * int(12 * HZ)
    elif tipo == 'V':
        cammina(1.55); t_stop = len(pos) * DT; pos += [(x, YL)] * int(4 * HZ); cammina(2.4)
    n = len(pos); cop = [False] * n; tc = tu = None
    if tipo == 'C':
        i0 = rng.randrange(0, n - int(2 * HZ) - 1); tc = i0 * DT; tu = (i0 + int(2 * HZ)) * DT
        for i in range(i0, i0 + int(2 * HZ)):
            cop[i] = True
    vis = [in_campo(p) and not in_ombra(p, xc) for p in pos]
    mis = [(p[0] + rng.gauss(0, SIGMA), p[1] + rng.gauss(0, SIGMA)) if vis[i] and not cop[i] and rng.random() < pd else None
           for i, p in enumerate(pos)]
    xl = (xc - 0.5) * YL / YP; xr = (xc + 0.5) * YL / YP
    zone = {'Z0': (-1.8, -1.3, 2.0, 2.6), 'ZM': (xl - 0.5, xr + 0.5, 2.0, 2.6), 'Z1': (1.3, 1.8, 2.0, 2.6)}
    return dict(tipo=tipo, v=v, xc=xc, pos=pos, vis=vis, cop=cop, mis=mis, zone=zone, tc=tc, tu=tu, t_stop=t_stop)


def copione(sc):
    """Eventi veri della scena, dalla sola verita' (posizione, occlusione geometrica, copertura)."""
    att = []; pos, vis, cop, xc = sc['pos'], sc['vis'], sc['cop'], sc['xc']
    for n, z in sc['zone'].items():
        for i in range(1, len(pos)):
            a, b = in_rett(pos[i - 1], z), in_rett(pos[i], z)
            oss = all(vis[j] and not cop[j] for j in range(i, min(len(pos), i + K + 1))) if LETTURA2 else vis[i]
            if b and not a and oss:                           # [dopo] attesa solo se osservabile per K+1 fotogrammi
                att.append((i * DT, 'INGRESSO', n))
            if a and not b and oss:
                att.append((i * DT, 'USCITA', n))
    th = next((i for i in range(1, len(pos)) if in_ombra(pos[i], xc) and vis[i - 1]), None)
    tr = next((i for i in range(th + 1, len(pos)) if vis[i]), None) if th else None
    if th:
        att.append((th * DT, 'SCOMPARSA', None))
        durata = (tr - th) * DT if tr else 1e9
        if tr:
            att.append((tr * DT, 'RICOMPARSA', None))
        if durata >= T_PERM + 0.5:
            att.append((th * DT + T_PERM, 'PERMANENZA_NON_OSSERVATA', None))
    if sc['tc'] is not None:
        att += [(sc['tc'], 'AFFIDABILITA_PERSA', None), (sc['tu'], 'AFFIDABILITA_RITROVATA', None)]
    if sc['t_stop'] is not None:
        att.append((sc['t_stop'] + T_SOSTA, 'SOSTA', 'Z1'))
    return att, th, tr


def gira(sc, k_nasc=K, ingenuo=False, tempi=None):
    nuc = NucleoRidotto(sc['xc'])
    est = Eventi(sc['zone'], lambda xc, p: in_campo(p) and dist_ombra(p, xc) <= FASCIA, k_nasc, ingenuo)
    ev = []; sc['avviso'] = []
    for i in range(len(sc['pos'])):
        f = nuc.passo(i * DT, sc['mis'][i], sc['cop'][i])
        sc['avviso'].append((f['aff_ok'], bool(f['regioni'])))
        t0 = time.perf_counter_ns(); e = est.passo(f); t1 = time.perf_counter_ns()
        if tempi is not None:
            tempi.append((t1 - t0) / 1e6)
        ev += e
    return ev, est


CONTATI = ('INGRESSO', 'PRESENTE', 'USCITA', 'SCOMPARSA', 'RICOMPARSA', 'PERMANENZA_NON_OSSERVATA', 'SOSTA', 'TRACCIA_CHIUSA')

def giudica(sc, ev):
    att, th, tr = copione(sc); pos, vis, cop = sc['pos'], sc['vis'], sc['cop']
    amb = (sc['tc'] - 0.5, sc['tu'] + 1.0) if sc['tc'] is not None else None
    usati = set(); mancati = []; ritardi = []
    for (t, tipo, zona) in att:
        if amb and amb[0] <= t <= amb[1] and not tipo.startswith('AFF'):
            continue
        tipi = ('INGRESSO', 'PRESENTE') if tipo == 'INGRESSO' else (tipo,)
        tol = 1.5 if tipo != 'SOSTA' else 1.5
        c = [(e['t'], j) for j, e in enumerate(ev) if j not in usati and e['tipo'] in tipi
             and (zona is None or e['zona'] == zona) and t - 0.25 <= e['t'] <= t + tol]
        if c:
            te, j = min(c); usati.add(j); ritardi.append((tipo, te - t, ev[j]['tipo']))
        else:
            mancati.append((tipo, zona))
    viol = []; false_uscite = 0; spuri = []
    for j, e in enumerate(ev):
        i = min(len(pos) - 1, round(e['t'] / DT))
        if e['stato'] == 'osservato' and e['traccia'] is not None and (not vis[i] or cop[i]):
            viol.append(e['tipo'])
        if e['tipo'] == 'USCITA':
            z = sc['zone'][e['zona']]
            if z[0] + 0.15 <= pos[i][0] <= z[1] - 0.15 and z[2] <= pos[i][1] <= z[3]:
                false_uscite += 1
        if e['tipo'] == 'SOSTA' and not vis[i]:
            viol.append('SOSTA_NASCOSTA')
        if j not in usati and e['tipo'] in CONTATI:
            if amb and sc['tc'] <= e['t'] <= sc['tu'] + 1.5:
                continue
            if LETTURA2 and e['tipo'] == 'TRACCIA_CHIUSA' and not vis[i]:
                continue                                  # [dopo] chiusura a soggetto davvero fuori vista: attesa
            if LETTURA2 and e['tipo'] == 'PERMANENZA_NON_OSSERVATA' and th and ((tr or 10**9) - th) * DT >= T_PERM - 0.5 and not vis[i]:
                continue                                  # [dopo] banda di 0,5 s attorno alla soglia
            dove = ''
            if e['tipo'] == 'SCOMPARSA':
                iu = round(e['ultima_misura'] / DT)
                dove = '_campo_aperto' if dist_ombra(pos[iu], sc['xc']) > FASCIA else '_in_fascia'
            spuri.append(e['tipo'] + dove)
    muti = sum(1 for i in range(len(pos)) if in_ombra(pos[i], sc['xc']) and math.hypot(*pos[i]) <= RMAX
               and sc['avviso'][i][0] and not sc['avviso'][i][1])
    return dict(mancati=mancati, ritardi=ritardi, viol=viol, false_uscite=false_uscite, spuri=spuri, th=th, tr=tr, muti=muti)


def p95(v):
    v = sorted(v); return v[min(len(v) - 1, math.ceil(0.95 * len(v)) - 1)] if v else float('nan')


def braccio(nome, pd, k_nasc, ingenuo, tipi, per_tipo, seme0, tempi=None):
    print(f'\n== {nome}: Pd={pd}, conferma scomparsa={k_nasc} fotogrammi, ingenuo={ingenuo}, {per_tipo} scene per tipo {tipi}')
    tot = 0; scene_manc = 0; manc = {}; rit = {}; viol = {}; fu_scene = 0; fu_scene_sl = 0; n_sl = 0
    muti = {}; spuri_scene = {}; sp_tot = {}; presente = 0; ingresso = 0; l_tot = 0; l_ok = 0; sosta_ok = 0; sosta_n = 0
    for it, tipo in enumerate(tipi):
        for s in range(per_tipo):
            sc = scena(seme0 + 1000 * it + s, tipo, pd); ev, est = gira(sc, k_nasc, ingenuo, tempi)
            g = giudica(sc, ev); tot += 1
            scene_manc += bool(g['mancati'])
            for m in g['mancati']:
                manc[m[0]] = manc.get(m[0], 0) + 1
            for (tp, d, come) in g['ritardi']:
                rit.setdefault(tp, []).append(d)
                presente += come == 'PRESENTE'; ingresso += come == 'INGRESSO'
            for vl in g['viol']:
                viol[vl] = viol.get(vl, 0) + 1
            fu_scene += g['false_uscite'] > 0
            if g['muti'] >= 15:
                muti[tipo] = muti.get(tipo, 0) + 1
            if tipo in ('S', 'L'):
                n_sl += 1; fu_scene_sl += g['false_uscite'] > 0
            for sp in set(g['spuri']):
                spuri_scene[sp] = spuri_scene.get(sp, 0) + 1
            for sp in g['spuri']:
                sp_tot[sp] = sp_tot.get(sp, 0) + 1
            if tipo == 'L':
                l_tot += 1
                usc = [e for e in ev if e['tipo'] == 'USCITA' and e['zona'] == 'ZM']
                perm = [e for e in ev if e['tipo'] == 'PERMANENZA_NON_OSSERVATA']
                stato_zm = [s_['zona']['ZM'] for s_ in est.tr.values()]
                l_ok += (not usc) and bool(perm) and 'non_oss' in stato_zm and 'oss' not in stato_zm
            if tipo == 'V':
                sosta_n += 1; sosta_ok += not any(m[0] == 'SOSTA' for m in g['mancati'])
    print(f'scene {tot}; scene con almeno un evento del copione mancato: {scene_manc} ({100 * scene_manc / tot:.1f} %); mancati per tipo: {manc}')
    for tp in sorted(rit):
        v = rit[tp]
        print(f'  ritardo {tp:26s} N={len(v):4d} mediana {statistics.median(v):.3f} s  p95 {p95(v):.3f} s  max {max(v):.3f} s')
    print(f'  ingressi trovati come INGRESSO: {ingresso}; come PRESENTE (ingresso non osservato): {presente}')
    print(f'  violazioni (evento "osservato" senza vista vera, o sosta a soggetto nascosto): {viol if viol else 0}')
    print(f'  scene con almeno una USCITA falsa (soggetto dentro la zona di oltre 0,15 m): {fu_scene} su {tot}; nei tipi S e L: {fu_scene_sl} su {n_sl}')
    print(f'  scene con almeno un evento spurio, per tipo: {spuri_scene if spuri_scene else 0}; totale eventi spuri: {sp_tot if sp_tot else 0}')
    print(f'  scene con il soggetto nascosto in portata per >= 1 s, affidabilita\' dichiarata buona e NESSUN avviso di possibile presenza, per tipo: {muti if muti else 0}')
    if l_tot:
        print(f'  tipo L (esce dalla portata restando in ombra): nessuna USCITA, PERMANENZA emessa, zona ancora "non osservato" a fine scena: {l_ok} su {l_tot}')
    if sosta_n:
        print(f'  tipo V: SOSTA osservata trovata entro 2 s + 1,5 s: {sosta_ok} su {sosta_n}')


def carico(n_tracce, n_zone, n_reg, n_fot, seme):
    rng = random.Random(seme)
    zone = {f'Z{i}': (-1.8 + 0.45 * i, -1.4 + 0.45 * i, 1.6, 2.8) for i in range(n_zone)}
    est = Eventi(zone, lambda xc, p: in_campo(p) and dist_ombra(p, xc) <= FASCIA)
    tr = [dict(id=i + 1, stato='osservato', pos=(rng.uniform(-1.9, 1.9), rng.uniform(1.5, 2.9)), t_mis=0.0, vel=0.5) for i in range(n_tracce)]
    tempi = []; n_ev = 0
    for k in range(n_fot):
        t = k * DT
        for x in tr:
            u = rng.random()
            if x['stato'] == 'osservato':
                x['pos'] = (max(-1.9, min(1.9, x['pos'][0] + rng.gauss(0, 0.06))), max(1.5, min(2.9, x['pos'][1] + rng.gauss(0, 0.06))))
                x['t_mis'] = t; x['vel'] = abs(rng.gauss(0.5, 0.4))
                if u < 0.02: x['stato'] = 'previsto'
            elif u < 0.05: x['stato'] = 'osservato'
            elif x['stato'] == 'previsto' and t - x['t_mis'] > T_PREV: x['stato'] = 'perso'
        nasc = [x for x in tr if x['stato'] != 'osservato'][:n_reg]
        f = dict(t=t, aff_ok=(k % 400) not in range(390, 400), causa='sensore', tracce=tr, chiuse=[],
                 regioni=[dict(id=x['id'], eta=t - x['t_mis'], chiave=0.01 * (x['id'] % 5)) for x in nasc])
        t0 = time.perf_counter_ns(); e = est.passo(f); t1 = time.perf_counter_ns()
        tempi.append((t1 - t0) / 1e6); n_ev += len(e)
    return tempi, n_ev


def righe_estrattore():
    src = open(__file__, encoding='utf-8').read().split('# >>> ESTRATTORE')[1].split('# <<< ESTRATTORE')[0]
    return sum(1 for r in src.splitlines() if r.strip() and not r.strip().startswith('#'))


if __name__ == '__main__':
    print('eventi.py - controllo della logica dello strato eventi; Python', sys.version.split()[0],
          '- SECONDA LETTURA [dopo]' if LETTURA2 else '- lettura del lancio 1')
    tipi = ('T', 'S', 'L', 'V', 'C'); tempi = []
    braccio('B1/B2 rilevamento certo', 1.0, K, False, tipi, 40, 20261114, tempi)
    braccio('B4 rilevamento 0,9, con conferma', 0.9, K, False, tipi, 40, 30261114)
    braccio('B7 rilevamento 0,9, senza conferma', 0.9, 1, False, tipi, 40, 30261114)
    braccio('B3 braccio ingenuo (deve fallire)', 1.0, K, True, ('S', 'L'), 100, 40261114)
    print(f'\n== B5 costo. Righe dell\'estrattore (non vuote, non commento): {righe_estrattore()}')
    print(f'1 traccia, 3 zone, {len(tempi)} fotogrammi: mediana {statistics.median(tempi) * 1000:.1f} us, p95 {p95(tempi) * 1000:.1f} us, max {max(tempi) * 1000:.1f} us')
    tc, n_ev = carico(20, 8, 5, 3000, 7)
    print(f'20 tracce, 8 zone, 5 regioni, {len(tc)} fotogrammi ({n_ev} eventi): mediana {statistics.median(tc) * 1000:.1f} us, p95 {p95(tc) * 1000:.1f} us, max {max(tc) * 1000:.1f} us; ciclo a 15 Hz = 66667 us')
