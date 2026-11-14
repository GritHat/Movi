"""Conti di contorno per scenari_eventi.json: tempi, portate utili col meteo (SEGNAPOSTO EV-D), distanze d'avviso.
Uso: python3 -I conti_eventi.py > conti_eventi_esito.txt. Solo libreria standard."""
import json, math, os
QUI = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(QUI, "regole_eventi.json")))
sc = json.load(open(os.path.join(QUI, "scenari_eventi.json")))
sen = json.load(open(os.path.join(QUI, "..", "..", "02-sensori", "parametri_lunga_portata.json")))["sensori"]
lp = json.load(open(os.path.join(QUI, "..", "..", "04-moto", "regole_lunga_portata.json")))

print("== tempi dei tratti (s) ==")
for s in sc["scenari"]:
    for o in s["oggetti"]:
        t = o["t0"]; riga = []
        for a, b, v in zip(o["punti"], o["punti"][1:], o["v"]):
            t += math.dist(a, b) / v; riga.append(round(t, 1))
        print(s["id"], o["id"], riga)

print("== E1/E5: separazione minima fra A e B (m) e istante ==")
def pos(o, t):
    t -= o["t0"]
    for a, b, v in zip(o["punti"], o["punti"][1:], o["v"]):
        d = math.dist(a, b) / v
        if t <= d: return [a[k] + (b[k] - a[k]) * max(t, 0) / d for k in range(3)]
        t -= d
    return o["punti"][-1]
for sid in ("E1", "E5"):
    s = next(x for x in sc["scenari"] if x["id"] == sid)
    A, B = s["oggetti"][0], s["oggetti"][1]
    m = min((math.dist(pos(A, i * 0.05), pos(B, i * 0.05)), i * 0.05) for i in range(0, 400 if sid == "E5" else 301))
    print(sid, round(m[0], 2), "m a t =", round(m[1], 2))
    for d_ris in (10.0, 20.0):
        tt = [i * 0.05 for i in range(0, 600) if math.dist(pos(A, i * 0.05), pos(B, i * 0.05)) < d_ris and (sid == "E5" or i * 0.05 <= 15)]
        print("   sotto", d_ris, "m da t =", round(tt[0], 2), "a t =", round(tt[-1], 2))

print("== portata del radar per il 'libero' (Pd cumulata 0.99 in 5 passate, Swerling 1, Pfa 1e-6: modello di 02-sensori e movi_lp.Sensore.portata) ==")
pd1 = 1 - (1 - 0.99) ** (1 / 5); snr = math.log(1e-6) / math.log(pd1) - 1; snr_ref = math.log(1e-6) / math.log(0.5) - 1
k = (snr_ref / snr) ** 0.25
print("Pd per passata", round(pd1, 3), "SNR richiesto", round(snr, 1), "SNR rif (Pd 0.5)", round(snr_ref, 1), "fattore sulla portata di scheda", round(k, 3))
Rref = sen["radar_sorveglianza_droni"]["portata_ref_m"][0]; Rstr = sen["radar_sorveglianza_droni"]["portata_strumentata_m"][0][0]
classi = {"frammento_minimo (1e-4 m2)": 1e-4, "multirotore_piccolo (0.01)": 0.01, "aereo_leggero (2)": 2.0, "aereo_linea (20)": 20.0}
R = {c: min(Rref * k * (r / 0.01) ** 0.25, Rstr) for c, r in classi.items()}
for c in R: print("  radar_sorveglianza_droni, sereno,", c, round(R[c]), "m")
ottici = {"camera_eo_ottica_lunga": {"multirotore_piccolo (0.01)": 2000.0, "aereo_leggero (2)": 15000.0}, "camera_termica_ottica_lunga": {"multirotore_piccolo (0.01)": 1200.0, "aereo_leggero (2)": 41700.0}}
print("  (ottici: 'portata_pratica' EO e 'geometrica' termica di 02-sensori; la termica e' un limite superiore)")

print("== EV-D: portata utile per condizione (m) = min(f*R, c*visibilita') ==")
D = reg["EV-D_meteo"]
av = lp["avviso"]; inv_v = max(lp["classi"][c]["v_max"] for c in lp["scenari"]["aeroporto_e_droni"]["classi_ammesse"])
p = av["profili_ricevente"]["operatore_di_sito"]
d_inv = inv_v * (av["tau_lat_s"] + p["T_r"] + p["T_man"]) + av["w_m"]
d_multi = lp["classi"]["multirotore_piccolo"]["v_max"] * (av["tau_lat_s"] + p["T_r"] + p["T_man"]) + av["w_m"]
print("d_avv operatore di sito: inviluppo aeroporto_e_droni (v_max", inv_v, ") =", round(d_inv), "m; solo multirotore =", round(d_multi), "m")
for cond, cv in D["condizioni"].items():
    for cl in ("multirotore_piccolo (0.01)", "aereo_leggero (2)"):
        r_rad = D["f"]["radar_sorveglianza_droni"][cond] * R[cl]
        r_eo = min(D["f"]["camera_eo_ottica_lunga"][cond] * ottici["camera_eo_ottica_lunga"][cl], D["c"]["camera_eo_ottica_lunga"] * cv["visibilita_m"])
        r_ir = min(D["f"]["camera_termica_ottica_lunga"][cond] * ottici["camera_termica_ottica_lunga"][cl], D["c"]["camera_termica_ottica_lunga"] * cv["visibilita_m"])
        tutti = max(r_rad, r_eo, r_ir); senza = max(r_eo, r_ir)
        print(f"  {cond:22s} {cl:28s} radar {r_rad:6.0f}  EO {r_eo:6.0f}  termica {r_ir:6.0f} | libero fino a {tutti:6.0f} (senza radar {senza:6.0f}) | tempestivo (inviluppo {d_inv:.0f} m): {'si' if tutti >= d_inv else 'NO'}; senza radar: {'si' if senza >= d_inv else 'NO'}")

print("== E2: distanza d'avviso del mezzo1 verso un ostacolo fermo ==")
print("  12*(1+2.5) + 12^2/(2*1.5) + 50 =", 12 * 3.5 + 144 / 3 + 50, "m")
print("== E1: caduta libera da 80 m senza resistenza:", round(math.sqrt(2 * 80 / 9.81), 2), "s; con v_t=15 m/s (da fermo):", round(15 / 9.81 * math.acosh(math.exp(9.81 * 80 / 225)), 2), "s")
