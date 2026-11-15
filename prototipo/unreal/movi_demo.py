"""Dimostrazione MoVi in Unreal: avvia la simulazione (fisica Chaos), muove i droni, fa avvenire la collisione
e collega il nucleo MoVi (movi_core) ai «sensori» della scena. Il tempo rallenta all'evento e la scala è a schermo.
Tutto è simulato: nessun sensore fisico."""
import math, os, random, importlib, unreal
import movi_core
importlib.reload(movi_core)

V, R = unreal.Vector, unreal.Rotator
ues = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
GS = unreal.GameplayStatics
FOTO = os.environ.get("MOVI_FOTO", "")          # cartella dei fotogrammi; vuota = non salva
T_E, T_FINE = 3.0, 8.5                           # istante dell'urto e fine, in secondi di simulazione
P_E = (1950.0, -800.0, 60.0)                     # punto dell'urto
VP = (500.0, 0.0, 0.0)                           # velocità del portatore
VA, VB = (90.0, 340.0, 0.0), (430.0, -150.0, 0.0)
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
    a["fumo_v"] = [(random.uniform(-90, 90), random.uniform(-90, 90), random.uniform(20, 110)) for _ in a["fumo"]]
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
    GS.set_global_time_dilation(w, k)
    dt = min(dt_muro, 0.05) * k
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
            d.set_actor_location(V(P_E[0] + random.uniform(-90, 90), P_E[1] + random.uniform(-90, 90),
                                   P_E[2] + random.uniform(-90, 90)), False, True)
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
        for f, fv in zip(a["fumo"], a["fumo_v"]):
            c = [P_E[i] + fv[i] * tau + (VA[i] + VB[i]) / 2 * min(tau, 1.5) * 0.4 for i in range(3)]
            f.set_actor_location(V(*c), False, False)
            f.set_actor_scale3d(V(*[min(3.2, 0.6 + 3.5 * tau)] * 3))
            centri.append(c)

    # sensori simulati: il radar satura per i detriti vicini, la camera è accecata dal lampo e dal fumo
    radar_ok = not (0.0 <= tau < 1.7)
    camera_ok = not (0.0 <= tau < 2.1) and not occluso(port, vero, centri, 230.0)
    misura = [vero[i] + random.gauss(0, 14.0) for i in range(3)] if (radar_ok or camera_ok) else None
    r = S["movi"].passo(t, dt, misura, radar_ok, camera_ok)

    # ciò che MoVi dichiara, mostrato nella scena
    visto = r["stato"] == "visto"
    a["regione"].set_actor_location(V(*r["pos"]), False, False)
    a["regione"].set_actor_scale3d(V(*[max(2.4, r["raggio"] / 50.0)] * 3))
    a["testo_stato"].set_actor_location(V(r["pos"][0], r["pos"][1], r["pos"][2] + 150 + max(120.0, r["raggio"])), False, False)
    a["testo_stato"].text_render.set_text(
        "VISTO" if visto else "NON VISTO · È QUI DENTRO · confidenza %d %%" % round(100 * r["confidenza"]))
    a["testo_stato"].text_render.set_text_render_color(unreal.Color(200, 60, 10, 255) if visto else unreal.Color(255, 110, 10, 255))
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
    a["testo_avviso"].set_actor_location(V(port[0], port[1], port[2] + 330), False, False)
    a["testo_avviso"].text_render.set_text(
        ("AVVISO INVIATO · evento vicino · radar %s · camera %s" % (r["radar"], r["camera"])) if avviso else
        ("sensori ripristinati · bersaglio ripreso" if tau > 2.8 else ""))
    a["testo_tempo"].set_actor_location(V(port[0], port[1], port[2] - 170), False, False)
    a["testo_tempo"].text_render.set_text(("tempo x%.2f" % k).replace(".", ",") +
                                          ("   frammento più vicino %d m" % round(vicino / 100) if 0 <= tau < 2.8 else ""))
    ues.set_level_viewport_camera_info(V(port[0] + CAM[0], port[1] + CAM[1], CAM[2]), R(0, -16, -45))

    S["n"] += 1
    if FOTO and S["n"] % 1 == 0:
        unreal.AutomationLibrary.take_high_res_screenshot(1280, 720, "%s/f_%05d.png" % (FOTO, S["foto"]))
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
