# Conti di sciame-interfacce per 22-schermo-finale: solo libreria standard, nessun dato letto.
from math import sqrt, comb, tan, radians, atan, degrees
def wilson(k, n, z=1.959964):
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h
def coda(k, n, p):  # P(X >= k)
    return sum(comb(n, i) * p**i * (1 - p)**(n - i) for i in range(k, n + 1))
print("== Q3 Wilson 95 %")
for k, n in [(27, 30), (30, 30), (46, 50), (45, 50), (942, 1045), (87, 100), (82, 94), (96, 100), (36, 46), (83, 90), (2939, 3038), (29, 30), (28, 30), (0, 90), (79, 90), (41, 45)]:
    a, b = wilson(k, n); print(f"{k:5d}/{n:<5d} {a:.3f} {b:.3f}")
print("== Q4 binomiale esatta, una coda, p0 = 0,80")
for k, n in [(87, 100), (86, 100), (82, 94), (81, 94), (46, 50), (45, 50), (28, 30), (27, 30)]:
    print(f"P(X>={k} | n={n}, p=0,80) = {coda(k, n, 0.80):.4f}   potenza se p=0,90: {coda(k, n, 0.90):.3f}")
print("== Q5 alzato: camera 1,2 m, 15 gradi in basso, campo verticale 58 (e 59) gradi")
for fov in (58.0, 59.0):
    su = radians(fov / 2 - 15)
    print(f"campo {fov}: bordo alto a 2,3 m = {1.2 + 2.3 * tan(su):.3f} m; testa 1,70 vista da {(1.70 - 1.2) / tan(su):.2f} m; 1,80 da {(1.80 - 1.2) / tan(su):.2f} m")
    giu = radians(fov / 2 + 15); print(f"   suolo visto al centro da {1.2 / tan(giu):.2f} m")
for hp in (1.7, 1.8):
    for dp in (1.7, 1.8, 1.9):
        print(f"pannello alto {hp} m a {dp} m: a 2,3 m nascosto fino a {1.2 + (hp - 1.2) * 2.3 / dp:.2f} m; altezza minima per nascondere 1,70 m: {1.2 + 0.5 * dp / 2.3:.2f} m")
print("== Q6 pianta: pannello largo 1 m")
for dp in (1.7, 1.8, 1.9):
    print(f"pannello a {dp} m: ombra sulla linea a 2,3 m = {1.0 * 2.3 / dp:.2f} m; attore {2.3 - dp:.1f} m dietro; nascosto per intero (corpo 0,45 m) a 0,5 m/s: {(2.3 / dp - 0.45) / 0.5:.1f} s")
print("campo orizzontale 87 gradi: larghezza a 2,3 m =", round(2 * 2.3 * tan(radians(43.5)), 2), "m; ma portata 3 m: mezza corda a 2,3 m =", round(sqrt(9 - 2.3**2), 2), "m")
print("== Q8 durate")
cinque = {"apertura": 25, "1 pavimento vuoto": 35, "2 passa dietro": 60, "3 si ferma e torna": 50, "4 sensore coperto": 30, "5 tabellone e costo": 70, "chiusura": 30}
tre = {"apertura": 20, "2 passa dietro": 45, "3 si ferma e torna": 35, "4 sensore coperto": 20, "5 tabellone": 40, "chiusura": 20}
print("5 minuti:", sum(cinque.values()), "s;  3 minuti:", sum(tre.values()), "s")
