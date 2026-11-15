"""Costruisce nell'editor di Unreal il livello della dimostrazione MoVi (scena «scorta», F7r):
drone portatore, bersaglio veloce più avanti, due droni che collidono di lato, detriti con fisica, fumo, e le zone di MoVi.
Stile del video: colori chiari, forme semplici, materiali piatti."""
import random
import unreal

eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
at = unreal.AssetToolsHelpers.get_asset_tools()
mel = unreal.MaterialEditingLibrary
eal = unreal.EditorAssetLibrary
V, R = unreal.Vector, unreal.Rotator

les.new_level("/Game/MoVi/Demo_%d" % unreal.MathLibrary.random_integer(100000))

def materiale(nome, traslucido):
    p = "/Game/MoVi/" + nome + "2"
    nome = nome + "2"
    if eal.does_asset_exist(p):
        return eal.load_asset(p)
    m = at.create_asset(nome, "/Game/MoVi", unreal.Material, unreal.MaterialFactoryNew())
    m.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_UNLIT)
    m.set_editor_property("two_sided", True)
    c = mel.create_material_expression(m, unreal.MaterialExpressionVectorParameter, -400, 0)
    c.set_editor_property("parameter_name", "Colore")
    mel.connect_material_property(c, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    if traslucido:
        m.set_editor_property("blend_mode", unreal.BlendMode.BLEND_TRANSLUCENT)
        o = mel.create_material_expression(m, unreal.MaterialExpressionScalarParameter, -400, 300)
        o.set_editor_property("parameter_name", "Opacita")
        o.set_editor_property("default_value", 0.3)
        mel.connect_material_property(o, "", unreal.MaterialProperty.MP_OPACITY)
    mel.recompile_material(m)
    eal.save_asset(p)
    return m

M_PIENO, M_VELO = materiale("M_Pieno", False), materiale("M_Velo", True)

def materiale_3d():
    """Materiale illuminato: colore di base più una quota di luce propria che fa da luce d'ambiente."""
    p = "/Game/MoVi/M_Solido3"
    if eal.does_asset_exist(p):
        return eal.load_asset(p)
    m = at.create_asset("M_Solido3", "/Game/MoVi", unreal.Material, unreal.MaterialFactoryNew())
    c = mel.create_material_expression(m, unreal.MaterialExpressionVectorParameter, -600, 0)
    c.set_editor_property("parameter_name", "Colore")
    mel.connect_material_property(c, "", unreal.MaterialProperty.MP_BASE_COLOR)
    k = mel.create_material_expression(m, unreal.MaterialExpressionConstant, -600, 300)
    k.set_editor_property("r", 0.45)
    x = mel.create_material_expression(m, unreal.MaterialExpressionMultiply, -300, 200)
    mel.connect_material_expressions(c, "", x, "A"); mel.connect_material_expressions(k, "", x, "B")
    mel.connect_material_property(x, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    r = mel.create_material_expression(m, unreal.MaterialExpressionConstant, -300, 500)
    r.set_editor_property("r", 0.55)
    mel.connect_material_property(r, "", unreal.MaterialProperty.MP_ROUGHNESS)
    mel.recompile_material(m); eal.save_asset(p)
    return m

M_3D = materiale_3d()

def istanza(nome, colore, opacita=None, piatto=False):
    p = "/Game/MoVi/" + nome
    mi = eal.load_asset(p) if eal.does_asset_exist(p) else at.create_asset(
        nome, "/Game/MoVi", unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
    mel.set_material_instance_parent(mi, M_VELO if opacita is not None else (M_PIENO if piatto else M_3D))
    mel.set_material_instance_vector_parameter_value(mi, "Colore", unreal.LinearColor(*colore, 1.0))
    if opacita is not None:
        mel.set_material_instance_scalar_parameter_value(mi, "Opacita", opacita)
    eal.save_asset(p)
    return mi

BLU = istanza("MI_Blu", (0.04, 0.30, 1.0)); NAVY = istanza("MI_Navy", (0.03, 0.06, 0.14))
GRIGIO = istanza("MI_Grigio", (0.25, 0.28, 0.33)); ROSSO = istanza("MI_Rosso", (0.85, 0.12, 0.10))
SUOLO = istanza("MI_Suolo", (0.72, 0.80, 0.78)); CIELO = istanza("MI_Cielo", (0.55, 0.78, 1.25), piatto=True)
BIANCO = istanza("MI_Bianco", (1, 1, 1)); ARANCIO = istanza("MI_Arancio", (1.0, 0.45, 0.05))
V_REGIONE = istanza("MI_VeloRegione", (0.10, 0.35, 1.0), 0.28)
V_AVVISO = istanza("MI_VeloAvviso", (1.0, 0.45, 0.05), 0.16)
V_FUMO = istanza("MI_VeloFumo", (0.30, 0.33, 0.38), 0.62)
V_LAMPO = istanza("MI_VeloLampo", (1.0, 0.85, 0.35), 0.9)

FORME = {k: unreal.load_asset("/Engine/BasicShapes/" + k) for k in ("Cube", "Sphere", "Cylinder", "Cone", "Plane")}

def pezzo(etichetta, forma, pos, scala, mat, tag=None, rot=(0, 0, 0), fisica=False, nascosto=False, collisione=False):
    a = eas.spawn_actor_from_class(unreal.StaticMeshActor, V(*pos), R(*rot))
    a.set_actor_label(etichetta)
    c = a.static_mesh_component
    c.set_static_mesh(FORME[forma]); c.set_material(0, mat)
    a.set_actor_scale3d(V(*scala) if isinstance(scala, tuple) else V(scala, scala, scala))
    c.set_mobility(unreal.ComponentMobility.MOVABLE)
    c.set_editor_property("cast_shadow", False)
    if not (fisica or collisione):
        c.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
    if fisica:   # fisica attiva da subito, senza gravità: i detriti aspettano fermi, in alto, fino all'urto
        c.set_collision_enabled(unreal.CollisionEnabled.QUERY_AND_PHYSICS)
        c.set_simulate_physics(True)
        c.set_enable_gravity(False)
    if nascosto:
        a.set_actor_hidden_in_game(True)
    if tag:
        a.tags = [tag]
    return a

def drone(nome, pos, mat, tag):
    """Corpo, due bracci e quattro rotori, attaccati a un corpo solo: si muove come un pezzo."""
    K = 2.6
    corpo = pezzo(nome, "Cube", pos, (0.9 * K, 0.5 * K, 0.22 * K), mat, tag)
    x, y, z = pos
    for i, (dx, dy) in enumerate(((55 * K, 55 * K), (55 * K, -55 * K), (-55 * K, 55 * K), (-55 * K, -55 * K))):
        r = pezzo("%s_rotore%d" % (nome, i), "Cylinder", (x + dx, y + dy, z + 14 * K), (0.55 * K, 0.55 * K, 0.05), GRIGIO)
        r.attach_to_actor(corpo, "", unreal.AttachmentRule.KEEP_WORLD, unreal.AttachmentRule.KEEP_WORLD,
                          unreal.AttachmentRule.KEEP_WORLD, False)
    for i, ry in enumerate((45, -45)):
        b = pezzo("%s_braccio%d" % (nome, i), "Cube", (x, y, z + 6 * K), (1.7 * K, 0.1, 0.08), GRIGIO, rot=(0, 0, ry))
        b.attach_to_actor(corpo, "", unreal.AttachmentRule.KEEP_WORLD, unreal.AttachmentRule.KEEP_WORLD,
                          unreal.AttachmentRule.KEEP_WORLD, False)
    return corpo

# cielo (sfera piatta attorno alla scena), suolo, qualche nuvola
pezzo("Cielo", "Sphere", (4000, 0, 0), 900.0, CIELO)
random.seed(3)
for i in range(26):
    x, y = random.uniform(-3000, 12000), random.choice((-1, 1)) * random.uniform(1500, 6000)
    z, sc = random.uniform(-2600, 1800), random.uniform(4, 11)
    for j, (dx, dz, k) in enumerate(((0, 0, 1.0), (sc * 55, -20, 0.8), (-sc * 55, -30, 0.7), (sc * 15, sc * 25, 0.6))):
        pezzo("Nuvola%d_%d" % (i, j), "Sphere", (x + dx, y, z + dz), (sc * k, sc * k * 0.8, sc * k * 0.55), BIANCO)
sole = eas.spawn_actor_from_class(unreal.DirectionalLight, V(0, 0, 3000), R(0, -48, 35))
sole.set_actor_label("Sole")
sole.light_component.set_mobility(unreal.ComponentMobility.MOVABLE)
sole.light_component.set_intensity(3.2)
sole.light_component.set_cast_shadows(False)

drone("Portatore", (0, 0, 0), BLU, "movi_portatore")
drone("Bersaglio", (1600, 150, 80), NAVY, "movi_bersaglio")
drone("DroneA", (1600, -1200, 50), GRIGIO, "movi_dronea")
drone("DroneB", (1600, 1320, 50), GRIGIO, "movi_droneb")

# detriti: fermi e nascosti nel punto dell'urto, la fisica li prende all'evento
random.seed(7)
for i in range(36):
    s = random.uniform(0.3, 0.7)
    pezzo("Detrito%02d" % i, "Cube", (1000 + 600 * (i % 6), -6000 + 600 * (i // 6), 5000),
          (s, s * random.uniform(0.5, 1.5), s * random.uniform(0.4, 1.0)), ROSSO if i < 3 else NAVY, "movi_detrito",
          rot=(random.uniform(0, 90), random.uniform(0, 90), 0), fisica=True, nascosto=True)
for i in range(12):
    pezzo("Fumo%d" % i, "Sphere", (2350, 60, 50), 0.3, V_FUMO, "movi_fumo", nascosto=True)
pezzo("Lampo", "Sphere", (2350, 60, 50), 0.5, V_LAMPO, "movi_lampo", nascosto=True)

# zone di MoVi
_reg = pezzo("RegioneBersaglio", "Sphere", (1600, 150, 80), 0.6, V_REGIONE, "movi_regione")
_reg.static_mesh_component.set_editor_property("translucency_sort_priority", 10)   # la regione si vede anche attraverso il fumo
pezzo("SferaAvviso", "Sphere", (0, 0, 0), 1.0, V_AVVISO, "movi_avviso", nascosto=True)
pezzo("RaggioSensore", "Cube", (800, 75, 40), (16, 0.03, 0.03), V_REGIONE, "movi_raggio")

def testo(etichetta, pos, t, size, colore, tag):
    a = eas.spawn_actor_from_class(unreal.TextRenderActor, V(*pos), R(0, 0, 135))
    a.set_actor_label(etichetta)
    c = a.text_render
    c.set_text(t); c.set_world_size(size); c.set_text_render_color(unreal.Color(*colore))
    c.set_horizontal_alignment(unreal.HorizTextAligment.EHTA_CENTER)
    a.tags = [tag]
    return a

testo("TestoStato", (1600, 150, 260), "VISTO", 130, (10, 60, 200, 255), "movi_testo_stato")
testo("TestoAvviso", (0, 0, 190), "", 80, (230, 110, 10, 255), "movi_testo_avviso")
testo("TestoTempo", (0, 0, -150), "tempo x1", 80, (10, 20, 40, 255), "movi_testo_tempo")

cat = eas.spawn_actor_from_class(unreal.SceneCapture2D, V(-700, 1500, 520), R(0, -14, -48))
cat.set_actor_label("Cattura"); cat.tags = ["movi_cattura"]
cc = cat.capture_component2d
cc.set_editor_property("capture_every_frame", False)
cc.set_editor_property("capture_on_movement", False)
cc.set_editor_property("capture_source", unreal.SceneCaptureSource.SCS_FINAL_COLOR_LDR)
cc.set_editor_property("fov_angle", 75.0)
ues = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
pp = eas.spawn_actor_from_class(unreal.PostProcessVolume, V(0, 0, 0), R(0, 0, 0))
pp.set_actor_label("EsposizioneFissa")
pp.set_editor_property("unbound", True)
st = pp.get_editor_property("settings")
for k, v in (("override_auto_exposure_method", True), ("auto_exposure_method", unreal.AutoExposureMethod.AEM_MANUAL),
             ("override_auto_exposure_bias", True), ("auto_exposure_bias", 0.0),
             ("override_auto_exposure_apply_physical_camera_exposure", True),
             ("auto_exposure_apply_physical_camera_exposure", False),
             ("override_bloom_intensity", True), ("bloom_intensity", 0.0),
             ("override_vignette_intensity", True), ("vignette_intensity", 0.0)):
    st.set_editor_property(k, v)
pp.set_editor_property("settings", st)
ues.set_level_viewport_camera_info(V(-1000, 1500, 650), R(0, -16, -45))
les.save_current_level()
print("scena costruita:", len(eas.get_all_level_actors()), "attori")
