#!/usr/bin/env python3
# semi_insieme.py — sciame-statistico, f12. Rifa' in numpy il generatore di insieme.c (mix64, rseed, r64: copiati dalle righe 44-49)
# e cerca flussi sovrapposti (uguali a meno di uno spostamento) fra TUTTI i flussi usati dalla prova, non solo fra semi vicini.
import numpy as np, sys
M = np.uint64
def mix64(z):
    z = z ^ (z >> M(33)); z = z * M(0xff51afd7ed558ccd); z = z ^ (z >> M(33)); z = z * M(0xc4ceb9fe1a85ec53); z = z ^ (z >> M(33)); return z
def passo(x):
    x = x ^ (x >> M(12)); x = x ^ (x << M(25)); x = x ^ (x >> M(27)); return x
def rseed(a, b, c):
    s = mix64(mix64(a ^ M(0x6A09E667F3BCC909)) + M(3) * mix64(b * M(0x10001) + M(0x3243F6A8885A308D)) + M(5) * mix64(c + M(0x13198A2E03707344)))
    s = np.where(s == 0, M(1), s)
    for _ in range(8): s = passo(s)
    return s
np.seterr(over='ignore')
SEED0, SSTR, LIB0 = 7000000000, 1000003, 9000000000
NS, L = 4000, 40
semi = (SEED0 + SSTR * np.arange(NS, dtype=np.int64)).astype(M)
lib = (LIB0 + SSTR * np.arange(200, dtype=np.int64)).astype(M)
stati, eti = [], 0
for geo in b'DTL':
    for beh in range(9):
        for base in (0, 1000, 2000, 3000):   # traiettoria, rumore di misura, rilevamento, estraneo (riga 101, 224, 228 di insieme.c)
            stati.append(rseed(semi, M(base + beh), M(geo)))
        stati.append(rseed(lib, M(beh), M(geo)))
S = np.concatenate(stati); n0 = S.size
print('flussi distinti per seme, comportamento, geometria e ruolo:', n0, '; stati iniziali distinti:', np.unique(S).size)
tutti = np.empty((L, n0), dtype=M); x = S.copy()
for i in range(L):
    tutti[i] = x; x = passo(x)
u = np.unique(tutti.ravel()).size
print(f'stati visitati nei primi {L} passi: {tutti.size}; distinti: {u}; sovrapposizioni (flussi uguali a meno di uno spostamento entro {L-1} passi): {tutti.size - u}')
# controllo positivo: 1000 flussi piu' gli stessi spostati di uno: il metodo deve vederli tutti
a = S[:1000]; b = passo(a); t = np.empty((L, 2000), dtype=M); x = np.concatenate([a, b])
for i in range(L):
    t[i] = x; x = passo(x)
print('controllo positivo (1000 flussi e gli stessi spostati di uno): stati ripetuti', t.size - np.unique(t.ravel()).size, '(attesi', 1000 * (L - 1), ')')
# semi contigui (+1) e correlazione delle uniformi fra semi vicini
def unif(s, n=64):
    out = np.empty((n, s.size)); x = s.copy()
    for i in range(n):
        x = passo(x); out[i] = ((x * M(0x2545F4914F6CDD1D)) >> M(11)).astype(np.float64) / 9007199254740992.0
    return out
A = unif(rseed(semi[:-1], M(0), M(ord('T')))); B = unif(rseed(semi[1:], M(0), M(ord('T')))); C = unif(rseed(semi[:-1] + M(1), M(0), M(ord('T'))))
for nome, Y in (('passo 1000003', B), ('contigui +1', C)):
    r = np.corrcoef(A.ravel(), Y.ravel())[0, 1]; rl = max(abs(np.corrcoef(A[:-k].ravel(), Y[k:].ravel())[0, 1]) for k in range(1, 9))
    print(f'correlazione fra uniformi di semi vicini ({nome}, {A.size} coppie, errore tipo {1/np.sqrt(A.size):.4f}): r={r:+.4f}; massimo |r| a spostamenti 1..8: {rl:.4f}')
print('media e varianza delle uniformi (attese 0,5 e 0,0833):', round(A.mean(), 4), round(A.var(), 4))
# collisioni esatte fra semi di prova e di libreria
print('semi di prova uguali a semi di libreria:', np.intersect1d(semi, lib).size)
