#!/usr/bin/env python3
"""Controllo di parametri_sensori.json (solo libreria standard).
Uso: python3 -I controlla_parametri.py parametri_sensori.json
Verifica: (1) ogni chiave di ogni profilo ha la sua provenienza; (2) i valori derivati (k, sottopixel,
ricerca della disparita') tornano con le formule dichiarate; poi stampa le tabelle usate in MODELLO_SENSORE.md."""
import json, math, sys

p = json.load(open(sys.argv[1], encoding="utf-8"))
err = []

def controlla_provenienza(nome, prof, esenti=()):
    prov = prof.get("provenienza", {})
    for k in prof:
        if k == "provenienza" or k in esenti:
            continue
        if k not in prov:
            err.append(f"{nome}: manca la provenienza di '{k}'")
    for k, v in prov.items():
        if not (v[:2] in ("D:", "M:", "C:", "I:") or v in ("D", "M", "C", "I") or v[:2] in ("D ", "I ", "C ", "M ")):
            err.append(f"{nome}: provenienza di '{k}' senza tipo: {v[:30]}")

cam = p["camere_profondita"]
for n, c in cam.items():
    controlla_provenienza(n, c)
controlla_provenienza("comuni", p["modello_camera_stereo_attiva"]["comuni"],
                      esenti=("vetro_specchio_nota", "sfocatura_moto"))
controlla_provenienza("tempo", p["modello_camera_stereo_attiva"]["tempo"])
for n in ("vl53l7cx", "vl53l8cx"):
    controlla_provenienza(n, p["tof_multizona"][n])
for n in ("rplidar_c1", "ld19"):
    controlla_provenienza(n, p["lidar_2d"][n])

# conta i tipi di provenienza
conta = {"D": 0, "M": 0, "C": 0, "I": 0}
def conta_prov(d):
    for v in d.get("provenienza", {}).values():
        conta[v[0]] += 1
for c in cam.values(): conta_prov(c)
conta_prov(p["modello_camera_stereo_attiva"]["comuni"]); conta_prov(p["modello_camera_stereo_attiva"]["tempo"])
for n in ("modello", "vl53l7cx", "vl53l8cx"): conta_prov(p["tof_multizona"][n])
for n in ("modello", "rplidar_c1", "ld19"): conta_prov(p["lidar_2d"][n])

print("== camere: valori derivati ==")
for n, c in cam.items():
    fB = c["fx"] * c["base_m"]
    for tag in ("nominale", "limite"):
        k = c[f"sottopixel_{tag}_px"] / fB
        if abs(k - c[f"k_{tag}"]) / c[f"k_{tag}"] > 0.01:
            err.append(f"{n}: k_{tag} = {c[f'k_{tag}']} ma sottopixel/(fx*B) = {k:.6f}")
    dmax = fB / c["z_min_m"]
    if abs(dmax - c["ricerca_disparita_px"]) > 15:
        err.append(f"{n}: fx*B/z_min = {dmax:.0f} px contro ricerca_disparita {c['ricerca_disparita_px']}")
    hf = 2 * math.degrees(math.atan(c["cx"] / c["fx"])); vf = 2 * math.degrees(math.atan(c["cy"] / c["fy"]))
    print(f"{n}: fx*B = {fB:.2f} px*m; fx*B/z_min = {dmax:.0f} px; campo dagli intrinseci {hf:.1f} x {vf:.1f} gradi "
          f"(dichiarato {c['campo_profondita_gradi']}); 1 px a 2 m = {2000/c['fx']:.1f} mm")
    r = []
    for z in (1, 2, 3, 4):
        r.append(f"{z} m: {100*c['k_nominale']*z*z:.1f} / {100*c['k_limite']*z*z:.1f}")
    print("   sigma_z nominale / limite [cm]  " + "; ".join(r))
    print("   passo di quantizzazione a 3 m (1/32 px): %.1f mm" % (1000 * 9 / fB / 32))
    print("   banda al bordo sinistro [px] a 1/2/3 m: " + ", ".join(f"{fB/z:.0f}" for z in (1, 2, 3)))
    for zo, zs in ((1.0, 3.0), (1.5, 3.0), (2.0, 3.0), (1.0, 2.0)):
        print(f"   occlusione: ostacolo {zo} m, sfondo {zs} m: {fB*(1/zo-1/zs):.1f} px = {100*c['base_m']*(zs-zo)/zo:.1f} cm sullo sfondo")

print("== Ahn 2019 (D435) contro il nominale ==")
c = cam["realsense_d435i"]
for z in (1.0, 2.0, 2.1, 3.0):
    a = 0.001063 + 0.0007278 * z + 0.003949 * z * z
    print(f"z = {z} m: Ahn {100*a:.2f} cm; nominale {100*c['k_nominale']*z*z:.2f} cm; rapporto {a/(c['k_nominale']*z*z):.2f}; "
          f"sottopixel equivalente {a*c['fx']*c['base_m']/z/z:.3f} px" + ("  (estrapolato)" if z > 2.1 else ""))
z, th = 2.0, math.radians(75)
print("termine angolare di Ahn a 2 m e 75 gradi: %.2f m" % (0.022 * z**1.5 * th / (math.pi/2 - th)**2))

print("== suolo visto da 1,2 m: angolo d'incidenza (dalla normale al suolo) ==")
for r in (1.24, 2.0, 2.08, 2.5, 3.0):
    print(f"distanza al suolo {r} m: incidenza {math.degrees(math.atan(r/1.2)):.1f} gradi; distanza in linea d'aria {math.hypot(r,1.2):.2f} m")

print("== ToF multizona: sigma = accuratezza/2,7 ==")
for n in ("vl53l7cx", "vl53l8cx"):
    t = p["tof_multizona"][n]
    for modo in ("4x4", "8x8"):
        a = t["accuratezza_2_7_sigma_frazione_oltre_0_2m"][modo]
        print(f"{n} {modo}: passo {t['modi'][modo]['passo_zona_gradi']} gradi; lato della zona a 2 m = "
              f"{200*math.tan(math.radians(t['modi'][modo]['passo_zona_gradi']/2)):.0f} cm; sigma buio bianco {100*a['buio']['bianco_88']/2.7:.1f} % "
              f"(a 2 m: {200*a['buio']['bianco_88']/2.7:.1f} cm); sigma 5 klx grigio 17 % {100*a['luce_5klx']['grigio_17']/2.7:.1f} %")

print("== LiDAR 2D ==")
for n in ("rplidar_c1", "ld19"):
    l = p["lidar_2d"][n]
    pts = 360 / l["risoluzione_angolare_gradi"]
    print(f"{n}: {pts:.0f} punti per giro ({l['frequenza_campioni_hz']/l['frequenza_giri_hz']:.0f} da campioni/giri); passo a 3 m = "
          f"{300*math.radians(l['risoluzione_angolare_gradi']):.1f} cm; punti su una persona larga 0,5 m a 3 m: "
          f"{0.5/(3*math.radians(l['risoluzione_angolare_gradi'])):.0f}")

print("== provenienza: D, M, C, I ==", conta)
print("ERRORI:", len(err))
for e in err: print("  -", e)
sys.exit(1 if err else 0)
