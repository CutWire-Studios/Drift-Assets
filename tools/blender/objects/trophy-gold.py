import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from drift3d import *  # noqa: E402,F403

ID = "trophy-gold"
OUT = os.path.join(REPO, "objects", ID)
FPS = 30
FRAMES = 120


def lathe(name, profile, seg=64):
    """Revolve [(r, z), ...] around Z. Points with r == 0 become single pole vertices."""
    bm = bmesh.new()
    rings = []
    for r, z in profile:
        if r == 0:
            rings.append([bm.verts.new((0, 0, z))])
        else:
            rings.append([bm.verts.new((r * math.cos(2 * math.pi * i / seg),
                                        r * math.sin(2 * math.pi * i / seg), z)) for i in range(seg)])
    for a, b in zip(rings, rings[1:]):
        for i in range(seg):
            j = (i + 1) % seg
            if len(a) == 1 and len(b) == 1:
                continue
            if len(a) == 1:
                bm.faces.new((a[0], b[j], b[i]))
            elif len(b) == 1:
                bm.faces.new((a[i], a[j], b[0]))
            else:
                bm.faces.new((a[i], a[j], b[j], b[i]))
    me = bpy.data.meshes.new(name)
    bm.normal_update()
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    return ob


def rounded_box(name, size, loc, bevel, segs=3):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = size
    bpy.ops.object.transform_apply(scale=True)
    mod = ob.modifiers.new("Bevel", "BEVEL")
    mod.width = bevel
    mod.segments = segs
    return ob


def tube(name, pts, radius, res=12):
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = radius
    cu.bevel_resolution = res // 4
    cu.use_fill_caps = True
    sp = cu.splines.new("NURBS")
    sp.points.add(len(pts) - 1)
    for p, c in zip(sp.points, pts):
        p.co = (*c, 1)
    sp.use_endpoint_u = True
    sp.order_u = 4
    sp.resolution_u = 10
    ob = bpy.data.objects.new(name, cu)
    bpy.context.scene.collection.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
    for o in bpy.context.selected_objects:
        o.select_set(False)
    ob.select_set(True)
    bpy.ops.object.convert(target="MESH")
    return bpy.context.active_object


def build():
    gold = material("TrophyGold", "#ffc53d", metallic=0.85, roughness=0.3)
    gold_dark = material("TrophyGoldDeep", "#d9921f", metallic=0.85, roughness=0.35)
    base_mat = material("TrophyBase", "#24222b", metallic=0.1, roughness=0.35)
    base_trim = material("TrophyBaseTrim", "#3a3744", metallic=0.2, roughness=0.3)

    parts = []

    b1 = rounded_box("Base1", (0.56, 0.56, 0.12), (0, 0, 0.06), 0.02)
    assign(b1, base_mat)
    b2 = rounded_box("Base2", (0.46, 0.46, 0.1), (0, 0, 0.17), 0.018)
    assign(b2, base_trim)
    b3 = rounded_box("Base3", (0.36, 0.36, 0.06), (0, 0, 0.25), 0.015)
    assign(b3, base_mat)
    plaque = rounded_box("Plaque", (0.34, 0.02, 0.08), (0, -0.28, 0.06), 0.006, 2)
    assign(plaque, gold)
    plaque_in = rounded_box("PlaqueInset", (0.3, 0.01, 0.052), (0, -0.2895, 0.06), 0.003, 1)
    assign(plaque_in, gold_dark)
    parts += [b1, b2, b3, plaque, plaque_in]

    stem = lathe("Stem", [
        (0, 0.28), (0.14, 0.28), (0.145, 0.29), (0.14, 0.30), (0.10, 0.31), (0.07, 0.33),
        (0.05, 0.36), (0.045, 0.40), (0.05, 0.42), (0.075, 0.435), (0.08, 0.45), (0.075, 0.465),
        (0.05, 0.48), (0.04, 0.51), (0.04, 0.54), (0.05, 0.56), (0.09, 0.575), (0.0, 0.58)])
    assign(stem, gold)
    parts.append(stem)

    prof = []
    for k in range(17):
        a = k / 16 * math.pi / 2
        prof.append((0.06 + 0.2 * math.sin(a) ** 0.9, 0.57 + 0.33 * (1 - math.cos(a)) * 0.9))
    top = prof[-1][1]
    prof += [(0.268, top + 0.03), (0.285, top + 0.045), (0.28, top + 0.06), (0.262, top + 0.065),
             (0.245, top + 0.05), (0.24, top + 0.03)]
    inner = []
    for k in range(16, -1, -1):
        a = k / 16 * math.pi / 2
        inner.append((0.02 + 0.2 * math.sin(a) ** 0.9 - 0.005, 0.60 + 0.30 * (1 - math.cos(a)) * 0.95))
    prof += inner + [(0, 0.60)]
    cup = lathe("Cup", [(0, 0.565)] + prof, seg=72)
    assign(cup, gold)
    parts.append(cup)

    band = lathe("Band", [(0.252, 0.735), (0.262, 0.742), (0.264, 0.76), (0.262, 0.778), (0.252, 0.785)], seg=72)
    band.scale = (1, 1, 1)
    band_mesh = band.data
    for v in band_mesh.vertices:
        rr = math.hypot(v.co.x, v.co.y)
        tgt = 0.06 + 0.2 * math.sin(math.acos(max(-1, min(1, 1 - (v.co.z - 0.57) / (0.33 * 0.9))))) ** 0.9
        s = (tgt + (rr - 0.252)) / rr
        v.co.x *= s
        v.co.y *= s
    assign(band, gold_dark)
    parts.append(band)

    for sx in (-1, 1):
        h = tube(f"Handle{sx}", [
            (sx * 0.24, 0, 0.86), (sx * 0.34, 0, 0.9), (sx * 0.42, 0, 0.84), (sx * 0.40, 0, 0.72),
            (sx * 0.30, 0, 0.64), (sx * 0.19, 0, 0.62)], 0.022)
        assign(h, gold)
        parts.append(h)

    for o in parts:
        apply_all(o)
    trophy = join(parts, "Trophy")
    shade_smooth(trophy, 35)
    lo, hi = world_bbox([trophy])
    c = (lo + hi) / 2
    for v in trophy.data.vertices:
        v.co -= c
    return trophy


def animate(obj):
    scene = bpy.context.scene
    scene.render.fps = FPS
    scene.frame_start, scene.frame_end = 0, FRAMES
    bpy.context.preferences.edit.keyframe_new_interpolation_type = "LINEAR"
    act = bpy.data.actions.new("Spin")
    obj.animation_data_create()
    obj.animation_data.action = act
    obj.rotation_euler = (0, 0, 0)
    obj.keyframe_insert("rotation_euler", index=2, frame=0)
    obj.rotation_euler = (0, 0, 2 * math.pi)
    obj.keyframe_insert("rotation_euler", index=2, frame=FRAMES)


reset()
trophy = build()
animate(trophy)
export_glb(os.path.join(OUT, f"{ID}.glb"), [trophy], animations=True)
render_thumbnail(os.path.join(OUT, "thumbnail.png"), [trophy], frame=0, view=(0.55, -1.0, 0.45))
write_asset_json(OUT, ID, "Gold Trophy", "object", f"{ID}.glb",
                 description="Gold trophy cup with handles on a dark stepped base with a plaque, slowly spinning.",
                 tags=["trophy", "award", "winner", "gold", "cup", "prize"],
                 extra={"animation": {"name": "Spin", "duration": FRAMES / FPS, "loop": True}})
