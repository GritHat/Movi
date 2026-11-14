#!/usr/bin/env python3
"""Legge l'indice finale di un file ROS bag v2.0 remoto con richieste HTTP a intervalli:
argomenti (topic), tipi dei messaggi, numero di messaggi, durata. Non scarica il file.
Uso: python3 -I indice_bag_remoto.py URL"""
import sys, struct, urllib.request
url = sys.argv[1]
def rng(a, b):
    req = urllib.request.Request(url, headers={"Range": f"bytes={a}-{b}", "User-Agent": "Mozilla/5.0 curl"})
    with urllib.request.urlopen(req, timeout=90) as r: return r.read()
def campi(h):
    d = {}; i = 0
    while i < len(h):
        n = struct.unpack_from("<I", h, i)[0]; i += 4
        k, v = h[i:i+n].split(b"=", 1); d[k.decode()] = v; i += n
    return d
req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0 curl"})
with urllib.request.urlopen(req, timeout=30) as r: size = int(r.headers["Content-Length"])
t = rng(0, 4200)
assert t.startswith(b"#ROSBAG V2.0\n"), t[:20]
hl = struct.unpack_from("<I", t, 13)[0]; f = campi(t[17:17+hl])
ip = struct.unpack("<Q", f["index_pos"])[0]; nc = struct.unpack("<I", f["conn_count"])[0]; nk = struct.unpack("<I", f["chunk_count"])[0]
print(f"# {url}\n# dimensione {size}; index_pos {ip}; connessioni {nc}; blocchi {nk}; byte d'indice {size-ip}")
if size - ip > 6_000_000: sys.exit("indice troppo grande: mi fermo")
x = rng(ip, size - 1); i = 0; conn = {}; cnt = {}; t0 = None; t1 = None
while i < len(x):
    hl = struct.unpack_from("<I", x, i)[0]; i += 4; h = campi(x[i:i+hl]); i += hl
    dl = struct.unpack_from("<I", x, i)[0]; i += 4; dat = x[i:i+dl]; i += dl
    op = h["op"][0]
    if op == 7:
        c = struct.unpack("<I", h["conn"])[0]; ch = campi(dat)
        conn[c] = (h["topic"].decode(), ch.get("type", b"?").decode())
    elif op == 6:
        s = struct.unpack("<II", h["start_time"]); e = struct.unpack("<II", h["end_time"])
        s = s[0] + s[1]*1e-9; e = e[0] + e[1]*1e-9
        t0 = s if t0 is None else min(t0, s); t1 = e if t1 is None else max(t1, e)
        for j in range(0, len(dat), 8):
            c, n = struct.unpack_from("<II", dat, j); cnt[c] = cnt.get(c, 0) + n
print(f"# durata {(t1-t0) if t0 is not None else float('nan'):.2f} s")
for c in sorted(conn):
    tp, ty = conn[c]
    if cnt.get(c, 0) > 3 or "image" in tp or "camera_info" in tp:
        print(f"{cnt.get(c,0):>7} {ty:<34} {tp}")
