import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from drift3d import *  # noqa: E402,F403

ID = "treasure-chest"
OUT = os.path.join(REPO, "objects", ID)
FPS = 30
FRAMES = 90
W, D, H = 0.92, 0.56, 0.42
R = D / 2
BAND_X = 0.29
LID_MIN = 32


def mesh_object(name, bm):
    bm.normal_update()
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    return ob


def rounded_box(name, size, loc, bevel, mat, segs=3):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = size
    bpy.ops.object.transform_apply(scale=True)
    mod = ob.modifiers.new("Bevel", "BEVEL")
    mod.width = bevel
    mod.segments = segs
    assign(ob, mat)
    apply_all(ob)
    return ob


def arc_slab(name, x0, x1, r0, r1, a0, a1, mat, seg=24, bevel=0.0):
    """Solid annular sector around the X axis (lid space: axis at y=-R, z=0; a=0 front, a=pi back)."""
    bm = bmesh.new()
    n = max(2, int(seg * (a1 - a0) / math.pi) + 1)
    rings = []
    for x in (x0, x1):
        outer, inner = [], []
        for k in range(n + 1):
            a = a0 + (a1 - a0) * k / n
            outer.append(bm.verts.new((x, -R - r1 * math.cos(a), r1 * math.sin(a))))
            inner.append(bm.verts.new((x, -R - r0 * math.cos(a), r0 * math.sin(a))))
        rings.append((outer, inner))
    (o0, i0), (o1, i1) = rings
    for k in range(n):
        bm.faces.new((o0[k], o0[k + 1], o1[k + 1], o1[k]))
        bm.faces.new((i0[k], i1[k], i1[k + 1], i0[k + 1]))
        bm.faces.new((o0[k], i0[k], i0[k + 1], o0[k + 1]))
        bm.faces.new((o1[k], o1[k + 1], i1[k + 1], i1[k]))
    for k in (0, n):
        bm.faces.new((o0[k], o1[k], i1[k], i0[k]))
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    ob = mesh_object(name, bm)
    if bevel:
        mod = ob.modifiers.new("Bevel", "BEVEL")
        mod.width = bevel
        mod.segments = 2
        mod.limit_method = "ANGLE"
        mod.angle_limit = math.radians(40)
    assign(ob, mat)
    apply_all(ob)
    return ob


def coin(loc, normal, mat, rng):
    bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=0.045, depth=0.012, location=(0, 0, 0))
    c = bpy.context.active_object
    c.rotation_euler = (0, 0, rng.uniform(0, math.pi))
    apply_all(c)
    c.rotation_euler = Vector((0, 0, 1)).rotation_difference(Vector(normal).normalized()).to_euler()
    c.location = loc
    assign(c, mat)
    apply_all(c)
    return c


def gem(loc, size, mat, rot):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=4, radius=size, location=(0, 0, 0))
    g = bpy.context.active_object
    for v in g.data.vertices:
        if v.co.z > size * 0.5:
            v.co.z = size * 0.45
    g.scale = (1, 1, 0.8)
    g.rotation_euler = rot
    g.location = loc
    assign(g, mat)
    apply_all(g)
    return g


def mound_height(x, y):
    hx, hy = W / 2 - 0.03, D / 2 - 0.03
    d = (x / hx) ** 2 + ((y + 0.02) / (hy - 0.02)) ** 2
    h = 0.012 + 0.16 * max(0.0, 1 - d) ** 0.7
    clear = 0.75 * (R - y) * math.tan(math.radians(LID_MIN))
    return min(h, clear)


def treasure(gold_pile, gold, ruby, emerald, sapphire):
    parts = []
    nx, ny = 24, 14
    hx, hy = W / 2 - 0.02, D / 2 - 0.02
    bm = bmesh.new()
    grid = [[bm.verts.new((-hx + 2 * hx * i / nx, -hy + 2 * hy * j / ny, 0)) for i in range(nx + 1)]
            for j in range(ny + 1)]
    for j in range(ny + 1):
        for i in range(nx + 1):
            v = grid[j][i]
            v.co.z = H + mound_height(v.co.x, v.co.y)
    for j in range(ny):
        for i in range(nx):
            bm.faces.new((grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]))
    pile = mesh_object("Pile", bm)
    assign(pile, gold_pile)
    parts.append(pile)

    rng = random.Random(11)
    for _ in range(60):
        x = rng.uniform(-hx + 0.04, hx - 0.04)
        y = rng.uniform(-hy + 0.03, hy - 0.08)
        e = 0.01
        z = H + mound_height(x, y)
        gx = (mound_height(x + e, y) - mound_height(x - e, y)) / (2 * e)
        gy = (mound_height(x, y + e) - mound_height(x, y - e)) / (2 * e)
        n = Vector((-gx + rng.uniform(-0.5, 0.5), -gy + rng.uniform(-0.5, 0.5), 1))
        parts.append(coin((x, y, z + 0.004), n, gold, rng))
    for x, y in ((-0.3, -D / 2 + 0.005), (0.12, -D / 2 + 0.0), (0.36, -D / 2 + 0.01)):
        parts.append(coin((x, y, H + 0.012), (rng.uniform(-0.15, 0.15), -0.25, 1), gold, rng))
    for loc, size, mat, rot in (((-0.12, -0.1, 0.0), 0.06, ruby, (0.3, 0.2, 0.4)),
                                ((0.2, -0.04, 0.0), 0.05, emerald, (-0.2, 0.3, 0.9)),
                                ((0.05, 0.02, 0.0), 0.045, sapphire, (0.4, -0.3, 0.2)),
                                ((-0.33, 0.0, 0.0), 0.04, emerald, (0.1, 0.5, 1.4))):
        z = H + mound_height(loc[0], loc[1]) + size * 0.55
        parts.append(gem((loc[0], loc[1], z), size, mat, rot))
    return parts


def build():
    wood_a = material("ChestWoodA", "#7c4420", roughness=0.7)
    wood_b = material("ChestWoodB", "#6a3819", roughness=0.7)
    wood_dark = material("ChestWoodDark", "#2e190c", roughness=0.8)
    steel = material("ChestSteel", "#4a4f57", metallic=0.7, roughness=0.38)
    brass = material("ChestBrass", "#d9a53a", metallic=0.8, roughness=0.32)
    iron = material("ChestIron", "#2a2622", metallic=0.4, roughness=0.5)
    gold_pile = material("ChestGoldPile", "#e8a82a", metallic=0.8, roughness=0.42)
    gold = material("ChestCoin", "#ffc53d", metallic=0.85, roughness=0.28)
    ruby = material("ChestRuby", "#ff2a55", roughness=0.15, emission="#d0103a")
    emerald = material("ChestEmerald", "#2cf08a", roughness=0.15, emission="#0aa04a")
    sapphire = material("ChestSapphire", "#3a8cff", roughness=0.15, emission="#1450d0")
    spark = material("ChestSparkle", "#fff6c8", emission="#fff0b0")

    parts = [rounded_box("Core", (W - 0.02, D - 0.02, H - 0.01), (0, 0, H / 2), 0.01, wood_dark, 1)]
    rows = 3
    rh = H / rows
    for k in range(rows):
        parts.append(rounded_box(f"Plank{k}", (W, D, rh - 0.014), (0, 0, rh * (k + 0.5)), 0.012,
                                 wood_a if k % 2 else wood_b, 2))
    for x in (-BAND_X, BAND_X):
        parts.append(rounded_box(f"Band{x}", (0.07, D + 0.03, H + 0.016), (0, 0, H / 2), 0.01, steel, 2))
        parts[-1].location.x = x
        apply_all(parts[-1])
    parts.append(rounded_box("RimTop", (W + 0.03, D + 0.03, 0.05), (0, 0, H - 0.02), 0.012, steel, 2))
    parts.append(rounded_box("RimBottom", (W + 0.03, D + 0.03, 0.05), (0, 0, 0.025), 0.012, steel, 2))
    for sx in (-1, 1):
        for sy in (-1, 1):
            parts.append(rounded_box(f"Corner{sx}{sy}", (0.07, 0.07, H + 0.01),
                                     (sx * (W / 2 - 0.02), sy * (D / 2 - 0.02), H / 2), 0.014, brass, 2))
    parts.append(rounded_box("LockPlate", (0.15, 0.03, 0.17), (0, -D / 2 - 0.02, H - 0.1), 0.02, brass, 3))
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.018, depth=0.02, location=(0, -D / 2 - 0.03, H - 0.09),
                                        rotation=(math.pi / 2, 0, 0))
    kh = bpy.context.active_object
    assign(kh, iron)
    apply_all(kh)
    parts.append(kh)
    parts.append(rounded_box("KeySlot", (0.018, 0.02, 0.05), (0, -D / 2 - 0.03, H - 0.115), 0.004, iron, 1))
    for x in (-BAND_X, BAND_X):
        for z in (0.1, H - 0.1):
            bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.014,
                                                 location=(x, -D / 2 - 0.016, z))
            st = bpy.context.active_object
            assign(st, iron)
            apply_all(st)
            parts.append(st)
    parts += treasure(gold_pile, gold, ruby, emerald, sapphire)
    body = join(parts, "Chest")
    shade_smooth(body, 35)

    lid_parts = [arc_slab("LidCore", -W / 2 + 0.01, W / 2 - 0.01, 0.0, R - 0.03, 0, math.pi, wood_dark, 32)]
    planks = 5
    for k in range(planks):
        a0 = math.pi * k / planks + 0.012
        a1 = math.pi * (k + 1) / planks - 0.012
        lid_parts.append(arc_slab(f"LidPlank{k}", -W / 2, W / 2, R - 0.05, R, a0, a1,
                                  wood_a if k % 2 else wood_b, 10, 0.006))
    for x in (-BAND_X, BAND_X):
        lid_parts.append(arc_slab(f"LidBand{x}", x - 0.035, x + 0.035, R - 0.03, R + 0.014, -0.02, math.pi + 0.02,
                                  steel, 32, 0.006))
    for sx in (-1, 1):
        x = sx * (W / 2 - 0.005)
        lid_parts.append(arc_slab(f"LidRim{sx}", x - 0.025, x + 0.025, R - 0.035, R + 0.014, -0.02, math.pi + 0.02,
                                  steel, 32, 0.006))
    lid_parts.append(rounded_box("LidFront", (W + 0.03, 0.035, 0.05), (0, -D - 0.005, 0.02), 0.012, steel, 2))
    lid_parts.append(rounded_box("Hasp", (0.1, 0.025, 0.13), (0, -D - 0.018, -0.02), 0.018, brass, 3))
    lid = join(lid_parts, "ChestLid")
    shade_smooth(lid, 35)
    lid.parent = body
    lid.location = (0, R, H + 0.005)
    lid.rotation_euler = (math.radians(-LID_MIN), 0, 0)

    sp = []
    for axis, length in (((1, 0, 0), 0.09), ((0, 0, 1), 0.09), ((0, 1, 0), 0.05)):
        for sign in (-1, 1):
            bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.014, radius2=0, depth=length,
                                            location=(0, 0, length / 2))
            c = bpy.context.active_object
            apply_all(c)
            c.rotation_euler = Vector((0, 0, 1)).rotation_difference(Vector(axis) * sign).to_euler()
            assign(c, spark)
            apply_all(c)
            sp.append(c)
    sparkle = join(sp, "Sparkle")
    sparkle.parent = body
    sparkle.location = (-0.12, -0.13, H + mound_height(-0.12, -0.1) + 0.11)

    bpy.context.view_layer.update()
    lo, hi = world_bbox([body, lid])
    c = (lo + hi) / 2
    body.location = -c
    return body, lid, sparkle


def animate(body, lid, sparkle):
    scene = bpy.context.scene
    scene.render.fps = FPS
    scene.frame_start, scene.frame_end = 0, FRAMES
    bpy.context.preferences.edit.keyframe_new_interpolation_type = "BEZIER"
    act = bpy.data.actions.new("LidGlint")
    for o in (lid, sparkle):
        o.animation_data_create()
        o.animation_data.action = act
    for fr, ang in ((0, LID_MIN), (24, 41), (42, 39), (62, LID_MIN + 1), (69, LID_MIN + 3.5),
                    (77, LID_MIN), (FRAMES, LID_MIN)):
        lid.rotation_euler = (math.radians(-ang), 0, 0)
        lid.keyframe_insert("rotation_euler", index=0, frame=fr)
    tiny = 0.001
    for fr, s, spin in ((0, tiny, 0), (26, tiny, -40), (34, 1.5, -15), (40, 0.8, 5), (46, 1.4, 25),
                        (56, tiny, 40), (FRAMES, tiny, 0)):
        sparkle.scale = (s, s, s)
        sparkle.rotation_euler = (0, math.radians(spin), 0)
        sparkle.keyframe_insert("scale", frame=fr)
        sparkle.keyframe_insert("rotation_euler", index=1, frame=fr)
    scene.frame_set(0)


reset()
body, lid, sparkle = build()
animate(body, lid, sparkle)
export_glb(os.path.join(OUT, f"{ID}.glb"), [body, lid, sparkle], animations=True)
render_thumbnail(os.path.join(OUT, "thumbnail.png"), [body, lid], frame=36, view=(0.6, -1.0, 0.6), margin=1.1)
write_asset_json(OUT, ID, "Treasure Chest", "object", f"{ID}.glb",
                 description="Wooden treasure chest with brass bands and a lock plate, overflowing with gold coins and glowing gems; the ajar lid lifts and settles as a sparkle glints.",
                 tags=["treasure", "chest", "gold", "loot", "reward", "game", "gaming"],
                 extra={"animation": {"name": "LidGlint", "duration": FRAMES / FPS, "loop": True}})
