# py_puro.py — quanto costa lo stesso lavoro in Python puro (nessuna libreria), scritto da capo da sciame-prestazioni.
# Uso: timeout 110 taskset -c 2 python3 -I py_puro.py
# Scena: pavimento + parete di fondo a 5,95 m + una cassa da 1 m; camera 640x480 letta a passo 4 (19 200 pixel).
import math, time
W, H, PASSO = 640, 480, 4
CAMZ = 1.2; CT = math.cos(math.radians(15)); ST = math.sin(math.radians(15))
FX = (W / 2) / math.tan(math.radians(87 / 2)); FY = (H / 2) / math.tan(math.radians(58 / 2))
pix = []                                   # (dirx, diry, dirz, profondita' z in metri)
for v in range(PASSO // 2, H, PASSO):
    b = (v + 0.5 - H / 2) / FY; dx = CT - b * ST; dz = -ST - b * CT
    for u in range(PASSO // 2, W, PASSO):
        dy = -(u + 0.5 - W / 2) / FX
        t = 5.95 / dx
        if dz < 0: t = min(t, CAMZ / -dz)
        tx0, tx1 = 2.7 / dx, 3.7 / dx                       # cassa: x 2,7-3,7; y -1,5..-0,5; z 0-1
        ty = sorted((-1.5 / dy, -0.5 / dy)) if dy else (-1e9, 1e9)
        tz = sorted((-CAMZ / dz, (1 - CAMZ) / dz)) if dz else (-1e9, 1e9)
        a = max(tx0, ty[0], tz[0]); c = min(tx1, ty[1], tz[1])
        if a <= c and 0 < a < t: t = a
        pix.append((dx, dy, dz, t))
NA, NR = 87, 30
azb = [int(math.degrees(math.atan2(p[1], p[0])) + 43.5) for p in pix]
rh = [math.hypot(p[0], p[1]) for p in pix]

def polare(f, suolo):
    rmin = [1e9] * NA
    for i, (dx, dy, dz, z) in enumerate(pix):
        a = azb[i]
        if a < 0 or a >= NA: continue
        r = z * rh[i]
        if r >= 3.0: continue
        h = CAMZ + z * dz
        if h >= 0.07:
            if h <= 2.0 and r < rmin[a]: rmin[a] = r
        elif h > -0.07: suolo[a * NR + int(r * 10)] = f
    stato = [0] * (NA * NR)
    for a in range(NA):
        ro = int(rmin[a] * 10) if rmin[a] < 3.0 else NR
        for r in range(NR):
            k = a * NR + r
            stato[k] = (1 if suolo[k] and suolo[k] + 2 >= f else 0) if r < ro else (2 if r == ro else 3)
    return stato

NX, NY, NZ, INV = 60, 40, 30, 10.0
def voxel(f, seen, occ):
    passi = 0
    for dx, dy, dz, z in pix:
        px, py, pz = z * dx, z * dy, max(CAMZ + z * dz, 0.001)
        te = 1.0; dentro = True
        ddx, ddy, ddz = px - 1e-4, py - 1e-4, pz - CAMZ - 1e-4
        if px >= 6.0: te = min(te, (6.0 - 1e-4) / ddx); dentro = False
        if py >= 2.0: te = min(te, (2.0 - 1e-4) / ddy); dentro = False
        elif py <= -2.0: te = min(te, (-2.0 - 1e-4) / ddy); dentro = False
        if pz >= 3.0: te = min(te, (3.0 - CAMZ - 1e-4) / ddz); dentro = False
        if not dentro: te *= 0.9999
        gx0, gy0, gz0 = 1e-4 * INV, (1e-4 + 2.0) * INV, (CAMZ + 1e-4) * INV
        gx1, gy1, gz1 = gx0 + ddx * te * INV, gy0 + ddy * te * INV, gz0 + ddz * te * INV
        ix, iy, iz = int(gx0), int(gy0), int(gz0)
        ex, ey, ez = min(max(int(gx1), 0), NX - 1), min(max(int(gy1), 0), NY - 1), min(max(int(gz1), 0), NZ - 1)
        nx, ny, nz = abs(ex - ix), abs(ey - iy), abs(ez - iz)
        sx = 1 if ex > ix else -1; sy = 1 if ey > iy else -1; sz = 1 if ez > iz else -1
        gdx, gdy, gdz = gx1 - gx0, gy1 - gy0, gz1 - gz0
        tdx = abs(1 / gdx) if nx else 1e30; tdy = abs(1 / gdy) if ny else 1e30; tdz = abs(1 / gdz) if nz else 1e30
        tmx = ((ix + 1 - gx0) if sx > 0 else (gx0 - ix)) * tdx if nx else 1e30
        tmy = ((iy + 1 - gy0) if sy > 0 else (gy0 - iy)) * tdy if ny else 1e30
        tmz = ((iz + 1 - gz0) if sz > 0 else (gz0 - iz)) * tdz if nz else 1e30
        n = nx + ny + nz; passi += n
        for _ in range(n):
            k = (iz * NY + iy) * NX + ix
            if seen[k] != f: seen[k] = f; occ[k] = 0
            if tmx <= tmy and tmx <= tmz:
                ix += sx; nx -= 1; tmx = tmx + tdx if nx else 1e30
            elif tmy <= tmz:
                iy += sy; ny -= 1; tmy = tmy + tdy if ny else 1e30
            else:
                iz += sz; nz -= 1; tmz = tmz + tdz if nz else 1e30
        k = (iz * NY + iy) * NX + ix
        seen[k] = f; occ[k] = 1 if dentro else 0
    return passi

def misura(nome, fn, n=7):
    ts = []
    for f in range(1, n + 1):
        a = time.perf_counter(); r = fn(f); ts.append((time.perf_counter() - a) * 1e3)
    ts.sort(); return nome, ts[0], ts[len(ts) // 2], ts[-1], r

suolo = [0] * (NA * NR); seen = [0] * (NX * NY * NZ); occ = [0] * (NX * NY * NZ)
import sys
print("python", sys.version.split()[0], "pixel letti", len(pix))
nome, mn, md, mx, _ = misura("polare_py 1x0,1m 3m", lambda f: polare(f, suolo))
print(f"{nome}: min={mn:.2f} mediana={md:.2f} max={mx:.2f} ms")
nome, mn, md, mx, passi = misura("voxel_denso_py 10cm", lambda f: voxel(f, seen, occ))
print(f"{nome}: min={mn:.1f} mediana={md:.1f} max={mx:.1f} ms passi={passi} ns_passo={md * 1e6 / passi:.0f}")
