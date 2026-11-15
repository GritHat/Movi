"""Dimostrazione MoVi in Unreal: avvia la simulazione (fisica Chaos), muove i droni, fa avvenire la collisione
e collega il nucleo MoVi (movi_core) ai «sensori» della scena. Il tempo rallenta all'evento e la scala è a schermo.
Tutto è simulato: nessun sensore fisico."""
import json, math, os, random, importlib, unreal
import movi_core
importlib.reload(movi_core)

V, R = unreal.Vector, unreal.Rotator
ues = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
GS = unreal.GameplayStatics
FOTO = os.environ.get("MOVI_FOTO", "")          # cartella dei fotogrammi; vuota = non salva
FPS = 30.0                                       # fotogrammi del filmato per secondo
T_E, T_FINE = 3.0, 8.5                           # istante dell'urto e fine, in secondi di simulazione
P_E = (2350.0, 60.0, 50.0)                       # sulla linea fra il portatore e il bersaglio                     # punto dell'urto
VP = (500.0, 0.0, 0.0)                           # velocità del portatore
VA, VB = (250.0, 420.0, 0.0), (250.0, -420.0, 0.0)
CAM = (-1000.0, 1500.0, 650.0)

S = {"t": 0.0, "w": None, "a": None, "movi": None, "evento": False, "n": 0, "foto": 0, "h": None, "attesa": 0.0}
random.seed(11)


def uno(w, tag):
    return GS.get_all_actors_with_tag(w, tag)[0]


def scala_tempo(t):
    return 0.1 if T_E <= t < T_E + 1.5 else (0.45 if T_E + 1.5 <= t < T_E + 2.8 else 1.0)


def bersaglio_vero(t):
    """Vola avanti; durante l'accecamento vira, così la regione serve davvero."""
    x = 1600.0 + 560.0 * t
    y = 150.0 + 40.0 * math.sin(1.3 * t)
    if t > T_E:
        y += 130.0 * (t - T_E) ** 1.5
    return (x, y, 80.0 + 12.0 * math.sin(0.9 * t))


def occluso(p, q, centri, raggio):
    """Vero se il segmento p-q passa entro `raggio` da uno dei centri (nube di fumo)."""
    d = [q[i] - p[i] for i in range(3)]
    L2 = sum(x * x for x in d) or 1.0
    for c in centri:
        u = max(0.0, min(1.0, sum((c[i] - p[i]) * d[i] for i in range(3)) / L2))
        if sum((p[i] + u * d[i] - c[i]) ** 2 for i in range(3)) < raggio * raggio:
            return True
    return False


def prepara(w):
    a = {k: uno(w, "movi_" + k) for k in ("portatore", "bersaglio", "dronea", "droneb", "lampo", "regione", "avviso",
                                           "raggio", "testo_stato", "testo_avviso", "testo_tempo")}
    a["detriti"] = list(GS.get_all_actors_with_tag(w, "movi_detrito"))
    a["fumo"] = list(GS.get_all_actors_with_tag(w, "movi_fumo"))
    a["fumo_m"] = [f.static_mesh_component.create_dynamic_material_instance(0) for f in a["fumo"]]
    a["fumo_v"] = [(random.uniform(-230, 230), random.uniform(-260, 260), random.uniform(-90, 170)) for _ in a["fumo"]]
    a["cattura"] = uno(w, "movi_cattura")
    S["rt"] = unreal.RenderingLibrary.create_render_target2d(w, 2880, 1620, unreal.TextureRenderTargetFormat.RTF_RGBA8)
    a["cattura"].capture_component2d.set_editor_property("texture_target", S["rt"])
    S["a"] = a
    S["movi"] = movi_core.MoVi(list(bersaglio_vero(0.0)), [560.0, 0.0, 0.0])


def passo(dt_muro):
    w = ues.get_game_world()
    if w is None:
        S["attesa"] += dt_muro
        if S["attesa"] > 20.0 and S["h"]:
            unreal.unregister_slate_post_tick_callback(S["h"]); S["h"] = None
        return
    if S["a"] is None:
        prepara(w)
    a, t = S["a"], S["t"]
    k = scala_tempo(t)
    dt = k / FPS                                  # passo fisso: un fotogramma del filmato per passo, moto fluido
    GS.set_global_time_dilation(w, max(0.0002, min(20.0, dt / max(dt_muro, 1e-3))))   # la fisica avanza dello stesso passo
    t += dt
    S["t"] = t

    port = (VP[0] * t, 0.0, 0.0)
    vero = bersaglio_vero(t)
    a["portatore"].set_actor_location(V(*port), False, False)
    a["bersaglio"].set_actor_location(V(*vero), False, False)
    tau = t - T_E
    if tau < 0:
        a["dronea"].set_actor_location(V(*[P_E[i] + VA[i] * tau for i in range(3)]), False, False)
        a["droneb"].set_actor_location(V(*[P_E[i] + VB[i] * tau for i in range(3)]), False, False)
    elif not S["evento"]:                        # urto: i due droni spariscono, i detriti passano alla fisica
        S["evento"] = True
        for d in (a["dronea"], a["droneb"]):
            d.set_actor_hidden_in_game(True)
            for f in d.get_attached_actors():
                f.set_actor_hidden_in_game(True)
        vm = [(VA[i] + VB[i]) / 2 for i in range(3)]
        for i, d in enumerate(a["detriti"]):
            c = d.static_mesh_component
            d.set_actor_hidden_in_game(False)
            d.set_actor_location(V(P_E[0] + random.uniform(-260, 260), P_E[1] + random.uniform(-260, 260),
                                   P_E[2] + random.uniform(-260, 260)), False, True)
            c.set_enable_gravity(True)
            c.wake_all_rigid_bodies()
            u = [random.gauss(0, 1) for _ in range(3)]
            n = math.sqrt(sum(x * x for x in u)) or 1.0
            v = random.uniform(250, 900)
            if i < 3:                             # tre frammenti rossi verso il portatore
                dp = [port[j] + VP[j] * 0.9 - P_E[j] + random.uniform(-60, 60) for j in range(3)]
                n, u, v = math.sqrt(sum(x * x for x in dp)), dp, 820.0
            S.setdefault("vel", []).append((c, V(*[vm[j] + v * u[j] / n for j in range(3)])))
            c.set_physics_linear_velocity(V(*[vm[j] + v * u[j] / n for j in range(3)]), False)
            c.set_physics_angular_velocity_in_degrees(V(random.uniform(-600, 600), random.uniform(-600, 600), 0), False)
        a["lampo"].set_actor_hidden_in_game(False)
        for f in a["fumo"]:
            f.set_actor_hidden_in_game(False)
    if S["evento"] and S.get("rilanci", 0) < 3:      # dopo il teletrasporto la velocità va ridata per qualche passo
        S["rilanci"] = S.get("rilanci", 0) + 1
        for c, v in S.get("vel", []):
            c.set_physics_linear_velocity(v, False)
    centri = []
    if tau >= 0:
        a["lampo"].set_actor_scale3d(V(*[1.0 + 30.0 * tau] * 3))
        if tau > 0.28:
            a["lampo"].set_actor_hidden_in_game(True)
        dirada = max(0.0, min(1.0, (1.7 - tau) / 0.5))       # il fumo si dirada in fretta, prima che i sensori tornino
        for f, mm in zip(a["fumo"], a["fumo_m"]):
            mm.set_scalar_parameter_value("Opacita", 0.62 * dirada)
            if dirada <= 0.0:
                f.set_actor_hidden_in_game(True)
        for f, fv in zip(a["fumo"], a["fumo_v"]):
            c = [P_E[i] + fv[i] * min(tau, 1.6) + (430.0 * tau if i == 0 else 0.0) for i in range(3)]   # la nube resta davanti al portatore
            f.set_actor_location(V(*c), False, False)
            f.set_actor_scale3d(V(*[min(7.5, 0.8 + 7.0 * tau)] * 3))
            centri.append(c)

    # sensori simulati: il radar satura per i detriti vicini, la camera è accecata dal lampo e dal fumo
    radar_ok = not (0.0 <= tau < 1.7)
    camera_ok = not (0.0 <= tau < 1.9) and not (tau < 1.7 and occluso(port, vero, centri, 400.0))
    misura = [vero[i] + random.gauss(0, 14.0) for i in range(3)] if (radar_ok or camera_ok) else None
    r = S["movi"].passo(t, dt, misura, radar_ok, camera_ok)

    # ciò che MoVi dichiara, mostrato nella scena
    visto = r["stato"] == "visto"
    a["regione"].set_actor_location(V(*r["pos"]), False, False)
    a["regione"].set_actor_scale3d(V(*[max(2.4, r["raggio"] / 50.0)] * 3))
    for kk in ("testo_stato", "testo_avviso", "testo_tempo"):
        a[kk].text_render.set_text("")
    m = [(port[i] + r["pos"][i]) / 2 for i in range(3)]
    d = [r["pos"][i] - port[i] for i in range(3)]
    L = math.sqrt(sum(x * x for x in d))
    a["raggio"].set_actor_hidden_in_game(not visto)
    a["raggio"].set_actor_location(V(*m), False, False)
    a["raggio"].set_actor_rotation(R(0, math.degrees(math.asin(d[2] / L)), math.degrees(math.atan2(d[1], d[0]))), False)
    a["raggio"].set_actor_scale3d(V(L / 100.0, 0.04, 0.04))
    avviso = r["avviso"] and tau < 2.8
    a["avviso"].set_actor_hidden_in_game(not avviso)
    a["avviso"].set_actor_location(V(*port), False, False)
    a["avviso"].set_actor_scale3d(V(*[min(11.0, 3.0 + 9.0 * max(tau, 0.0))] * 3))
    vicino = min([math.dist(port, (lambda p: (p.x, p.y, p.z))(x.get_actor_location())) for x in a["detriti"]] or [9e9])
    # camera: gira attorno al drone per mostrare la scena in 3D; durante l'accecamento passa in soggettiva
    pov = 0.75 <= tau < 2.75
    if pov:
        cam = (port[0] + 150.0, port[1], port[2] + 70.0)
        dd = [r["pos"][i] - cam[i] for i in range(3)]
        LL = math.sqrt(sum(x * x for x in dd))
        rot = R(0, math.degrees(math.asin(dd[2] / LL)), math.degrees(math.atan2(dd[1], dd[0])) - 9.0)
    else:
        ang = math.radians(112.0 - 7.0 * t)                  # l'angolo cambia nel tempo: orbita
        raggio_cam = 2500.0
        cam = (port[0] + 1000.0 + raggio_cam * math.cos(ang), port[1] + raggio_cam * math.sin(ang), port[2] + 700.0 + 30.0 * t)
        mira = (port[0] + 1000.0, port[1] + 60.0, port[2] - 120.0)   # a metà fra il portatore e il bersaglio
        dd = [mira[i] - cam[i] for i in range(3)]
        LL = math.sqrt(sum(x * x for x in dd))
        rot = R(0, math.degrees(math.asin(dd[2] / LL)), math.degrees(math.atan2(dd[1], dd[0])))
    ues.set_level_viewport_camera_info(V(*cam), rot)
    a["cattura"].set_actor_location_and_rotation(V(*cam), rot, False, True)
    a["avviso"].set_actor_hidden_in_game((not avviso) or pov)
    tr = S["movi"].traccia
    S["riga"] = {"t": round(t, 3), "tau": round(tau, 3), "k": k, "pov": pov, "stato": r["stato"], "conf": r["confidenza"],
                 "raggio": r["raggio"], "avviso": bool(avviso), "radar": r["radar"], "camera": r["camera"],
                 "vicino_m": vicino / 100.0, "P": [[x.a, x.b, x.c] for x in tr.assi[:2]], "non_visto_da": r["non_visto_da"]}

    S["n"] += 1
    if FOTO and S["n"] % 1 == 0:
        a["cattura"].capture_component2d.capture_scene()
        unreal.RenderingLibrary.export_render_target(w, S["rt"], FOTO, "f_%05d.png" % S["foto"])
        open(FOTO + "/stato.jsonl", "a").write(json.dumps(dict(S["riga"], f=S["foto"])) + "\n")
        S["foto"] += 1
    if t >= T_FINE:
        unreal.unregister_slate_post_tick_callback(S["h"]); S["h"] = None
        GS.set_global_time_dilation(w, 1.0)
        les.editor_request_end_play()
        unreal.log("MoVi demo: fine, %d passi, %d fotogrammi" % (S["n"], S["foto"]))


def sicuro(dt):
    try:
        passo(dt)
    except Exception:
        import traceback
        open(os.path.dirname(os.path.abspath(movi_core.__file__)) + "/_errore.txt", "w").write(traceback.format_exc())
        if S["h"]:
            unreal.unregister_slate_post_tick_callback(S["h"]); S["h"] = None
        les.editor_request_end_play()


S["h"] = unreal.register_slate_post_tick_callback(sicuro)
les.editor_play_simulate()
print("demo avviata")
