#!/usr/bin/env python3
"""Elenca il contenuto di un archivio ZIP remoto leggendo solo l'indice finale
con richieste HTTP a intervalli (Range). Non scarica l'archivio, non estrae niente.
Uso: python3 -I elenco_zip_remoto.py URL [max_righe]"""
import sys, io, zipfile, urllib.request

class FileRemoto(io.RawIOBase):
    def __init__(self, url):
        self.url = url; self.pos = 0; self.letti = 0
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0 curl"})
        with urllib.request.urlopen(req, timeout=30) as r:
            self.size = int(r.headers["Content-Length"]); self.url = r.geturl()
        # memoria: ultimo blocco, dove sta l'indice
        self.coda_n = min(self.size, 3_000_000)
        self.coda = self._range(self.size - self.coda_n, self.size - 1)
    def _range(self, a, b):
        req = urllib.request.Request(self.url, headers={"Range": f"bytes={a}-{b}", "User-Agent": "Mozilla/5.0 curl"})
        with urllib.request.urlopen(req, timeout=60) as r:
            d = r.read()
        self.letti += len(d)
        if self.letti > 8_000_000: raise RuntimeError("troppi byte letti: mi fermo")
        return d
    def seekable(self): return True
    def readable(self): return True
    def tell(self): return self.pos
    def seek(self, off, whence=0):
        self.pos = off if whence == 0 else (self.pos + off if whence == 1 else self.size + off)
        return self.pos
    def read(self, n=-1):
        if n < 0: n = self.size - self.pos
        n = min(n, self.size - self.pos)
        if n <= 0: return b""
        ini = self.size - self.coda_n
        if self.pos >= ini:
            d = self.coda[self.pos - ini:self.pos - ini + n]
        else:
            d = self._range(self.pos, self.pos + n - 1)
        self.pos += len(d); return d

url = sys.argv[1]; maxr = int(sys.argv[2]) if len(sys.argv) > 2 else 40
f = FileRemoto(url)
z = zipfile.ZipFile(f)
inf = z.infolist()
tot = sum(i.file_size for i in inf)
print(f"# {url}\n# dimensione archivio {f.size} byte; voci {len(inf)}; dimensione estratta {tot} byte; byte letti {f.letti}")
est = {}
for i in inf:
    e = i.filename.rsplit(".", 1)[-1].lower() if "." in i.filename.rsplit("/", 1)[-1] else "(cartella o senza estensione)"
    est[e] = est.get(e, 0) + 1
print("# estensioni:", est)
visti = set(); n = 0
for i in inf:
    # mostra i primi due file di ogni cartella
    c = i.filename.rsplit("/", 1)[0] if "/" in i.filename else ""
    k = (c, i.filename.rsplit(".", 1)[-1])
    if list(visti).count(k) or sum(1 for v in visti if v == k): continue
    visti.add(k); n += 1
    if n > maxr: break
    print(f"{i.file_size:>12} {i.filename}")
