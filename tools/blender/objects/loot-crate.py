import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from drift3d import *  # noqa: E402,F403

ID = "loot-crate"
OUT = os.path.join(REPO, "objects", ID)
FPS = 30
FRAMES = 120
W, D, H = 0.92, 0.6, 0.56
SEAM = 0.4
E = 0.05


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


def shell(olive, panel):
    """Box with every face inset into a recessed panel."""
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1)
    for v in bm.verts:
        v.co = Vector((v.co.x * W, v.co.y * D, v.co.z * H + H / 2))
    faces = list(bm.faces)
    bmesh.ops.inset_individual(bm, faces=faces, thickness=0.055, depth=-0.018)
    ob = mesh_object("Shell", bm)
    ob.data.materials.append(olive)
    ob.data.materials.append(panel)
    for p in ob.data.polygons:
        c, n = p.center, p.normal
        axis = max(range(3), key=lambda i: abs(n[i]))
        half = (W / 2, D / 2, H / 2)[axis]
        coord = c[axis] - (H / 2 if axis == 2 else 0)
        if abs(n[axis]) > 0.99 and abs(abs(coord) - (half - 0.018)) < 1e-4:
            p.material_index = 1
    mod = ob.modifiers.new("Bevel", "BEVEL")
    mod.width = 0.006
    mod.segments = 2
    mod.limit_method = "ANGLE"
    mod.angle_limit = math.radians(30)
    apply_all(ob)
    return ob


def slanted_bar(name, x, z, w, h, slant, y, mat):
    bm = bmesh.new()
    pts = [(x - w / 2 - slant, z - h / 2), (x + w / 2 - slant, z - h / 2),
           (x + w / 2 + slant, z + h / 2), (x - w / 2 + slant, z + h / 2)]
    bot = [bm.verts.new((px, y, pz)) for px, pz in pts]
    top = [bm.verts.new((px, y - 0.006, pz)) for px, pz in pts]
    bm.faces.new(bot[::-1])
    bm.faces.new(top)
    for i in range(4):
        j = (i + 1) % 4
        bm.faces.new((bot[i], bot[j], top[j], top[i]))
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    ob = mesh_object(name, bm)
    assign(ob, mat)
    return ob


def tube(name, pts, radius, mat):
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = radius
    cu.bevel_resolution = 3
    cu.use_fill_caps = True
    sp = cu.splines.new("POLY")
    sp.points.add(len(pts) - 1)
    for p, c in zip(sp.points, pts):
        p.co = (*c, 1)
    ob = bpy.data.objects.new(name, cu)
    bpy.context.scene.collection.objects.link(ob)
    for o in bpy.context.selected_objects:
        o.select_set(False)
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.convert(target="MESH")
    ob = bpy.context.active_object
    assign(ob, mat)
    return ob


def build():
    olive = material("CrateOlive", "#5b6b3b", roughness=0.6)
    panel = material("CratePanel", "#4b5930", roughness=0.65)
    steel = material("CrateSteel", "#9aa1a9", metallic=0.75, roughness=0.35)
    dark = material("CrateDarkSteel", "#3a3f46", metallic=0.6, roughness=0.45)
    stencil = material("CrateStencil", "#e6d79a", roughness=0.7)
    glow = material("CrateGlow", "#40f0ff", emission="#22d8ff")

    parts = [shell(olive, panel)]
    for sx in (-1, 1):
        for sy in (-1, 1):
            parts.append(rounded_box(f"EdgeV{sx}{sy}", (E, E, H), (sx * (W / 2 - E / 2 + 0.008), sy * (D / 2 - E / 2 + 0.008), H / 2),
                                     0.012, steel, 2))
    for sy in (-1, 1):
        for z in (E / 2 - 0.008, H - E / 2 + 0.008):
            parts.append(rounded_box(f"EdgeX{sy}{z:.2f}", (W, E, E), (0, sy * (D / 2 - E / 2 + 0.008), z), 0.012, steel, 2))
    for sx in (-1, 1):
        for z in (E / 2 - 0.008, H - E / 2 + 0.008):
            parts.append(rounded_box(f"EdgeY{sx}{z:.2f}", (E, D, E), (sx * (W / 2 - E / 2 + 0.008), 0, z), 0.012, steel, 2))
    for sx in (-1, 1):
        for sy in (-1, 1):
            for z in (0.035, H - 0.035):
                parts.append(rounded_box(f"Cap{sx}{sy}{z:.2f}", (0.085, 0.085, 0.085),
                                         (sx * (W / 2 - 0.03), sy * (D / 2 - 0.03), z), 0.022, dark, 3))

    parts.append(rounded_box("SeamBand", (W + 0.012, D + 0.012, 0.075), (0, 0, SEAM), 0.01, dark, 2))
    parts.append(rounded_box("GlowStrip", (W - 0.14, D + 0.026, 0.03), (0, 0, SEAM), 0.008, glow, 2))
    parts.append(rounded_box("GlowStripSide", (W + 0.026, D - 0.14, 0.03), (0, 0, SEAM), 0.008, glow, 2))
    for sx in (-1, 1):
        for sy in (-1, 1):
            parts.append(rounded_box(f"Latch{sx}{sy}", (0.08, 0.035, 0.13),
                                     (sx * 0.3, sy * (D / 2 + 0.018), SEAM), 0.012, steel, 3))

    yf = -D / 2 + 0.018
    for k in range(6):
        parts.append(slanted_bar(f"Stripe{k}", -0.25 + k * 0.1, 0.17, 0.045, 0.15, 0.04, yf, stencil))
    parts.append(slanted_bar("StripeBar", 0.0, 0.275, 0.6, 0.022, 0.0, yf, stencil))
    parts.append(slanted_bar("StripeBar2", 0.0, 0.065, 0.6, 0.022, 0.0, yf, stencil))
    for cx in (-0.12, 0.0, 0.12):
        for sx in (-1, 1):
            parts.append(slanted_bar(f"Chev{cx}{sx}", cx + sx * 0.026, 0.472, 0.026, 0.05, -sx * 0.024, yf, stencil))
    parts.append(rounded_box("LidPanel", (W - 0.24, D - 0.24, 0.03), (0, 0, H + 0.005), 0.012, olive, 2))
    for x in (-0.18, 0.18):
        parts.append(rounded_box(f"LidRib{x}", (0.05, D - 0.1, 0.035), (x, 0, H + 0.01), 0.012, dark, 2))

    for sx in (-1, 1):
        x = sx * (W / 2 + 0.01)
        pts = [(x, -0.12, 0.3), (x + sx * 0.05, -0.12, 0.3), (x + sx * 0.05, 0.12, 0.3), (x, 0.12, 0.3)]
        h = tube(f"Handle{sx}", pts, 0.016, dark)
        apply_all(h)
        parts.append(h)
        for y in (-0.12, 0.12):
            parts.append(rounded_box(f"HMount{sx}{y}", (0.02, 0.05, 0.07), (x, y, 0.3), 0.008, steel, 2))
    for y in (-0.2, 0.2):
        parts.append(rounded_box(f"Skid{y}", (W - 0.04, 0.07, 0.045), (0, y, -0.02), 0.015, dark, 2))

    crate = join(parts, "LootCrate")
    shade_smooth(crate, 35)
    lo, hi = world_bbox([crate])
    crate.location = -(lo + hi) / 2
    apply_all(crate)
    return crate


def animate(crate):
    scene = bpy.context.scene
    scene.render.fps = FPS
    scene.frame_start, scene.frame_end = 0, FRAMES
    bpy.context.preferences.edit.keyframe_new_interpolation_type = "LINEAR"
    crate.animation_data_create()
    crate.animation_data.action = bpy.data.actions.new("Sway")
    for fr in range(FRAMES + 1):
        t = 2 * math.pi * fr / FRAMES
        crate.rotation_euler = (math.radians(3) * math.sin(2 * t), math.radians(2.5) * math.sin(t + 0.6),
                                math.radians(22) * math.sin(t))
        crate.location = (0, 0, 0.035 * math.sin(2 * t))
        crate.keyframe_insert("rotation_euler", frame=fr)
        crate.keyframe_insert("location", index=2, frame=fr)
    scene.frame_set(0)


reset()
crate = build()
animate(crate)
export_glb(os.path.join(OUT, f"{ID}.glb"), [crate], animations=True)
render_thumbnail(os.path.join(OUT, "thumbnail.png"), [crate], frame=0, view=(0.62, -1.0, 0.5), margin=1.1)
write_asset_json(OUT, ID, "Loot Crate", "object", f"{ID}.glb",
                 description="Olive military supply-drop crate with steel edges, stencil stripes and a glowing cyan strip, gently swaying and bobbing.",
                 tags=["loot", "crate", "supply-drop", "military", "box", "game", "gaming"],
                 extra={"animation": {"name": "Sway", "duration": FRAMES / FPS, "loop": True}})
