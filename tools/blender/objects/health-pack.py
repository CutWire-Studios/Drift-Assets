import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from drift3d import *  # noqa: E402,F403

ID = "health-pack"
OUT = os.path.join(REPO, "objects", ID)
FPS = 30
FRAMES = 120
W, D, H = 0.84, 0.36, 0.58
SEAM_Z = 0.42


def rounded_box(name, size, loc, bevel, mat, segs=4):
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


def tube(name, pts, radius, mat):
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = radius
    cu.bevel_resolution = 4
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


def cross(name, y, sign, mat, plate_mat):
    """Raised red cross on a soft white plate; sign=-1 front (-Y), +1 back."""
    arm, thick, depth = 0.3, 0.1, 0.035
    cz = SEAM_Z / 2 + 0.01
    plate = rounded_box(name + "Plate", (0.4, 0.02, 0.36), (0, y + sign * 0.006, cz), 0.03, plate_mat, 4)
    y0 = y + sign * (0.012 + depth / 2)
    a = rounded_box(name + "V", (thick, depth, arm), (0, y0, cz), 0.014, mat, 3)
    b = rounded_box(name + "H", (arm, depth, thick), (0, y0, cz), 0.014, mat, 3)
    return [plate, a, b]


def build():
    white = material("KitWhite", "#f4f3ef", roughness=0.42)
    shell = material("KitShell", "#dcdcd8", roughness=0.5)
    red = material("KitRed", "#e0192e", roughness=0.35)
    red_dark = material("KitRedDark", "#a80f20", roughness=0.4)
    steel = material("KitSteel", "#b8bec8", metallic=0.8, roughness=0.3)
    grip = material("KitGrip", "#2d3139", roughness=0.55)

    parts = [
        rounded_box("Base", (W, D, SEAM_Z), (0, 0, SEAM_Z / 2), 0.07, white, 5),
        rounded_box("Lid", (W, D, H - SEAM_Z - 0.01), (0, 0, SEAM_Z + (H - SEAM_Z + 0.01) / 2), 0.07, white, 5),
        rounded_box("Seam", (W + 0.016, D + 0.016, 0.05), (0, 0, SEAM_Z), 0.02, red_dark, 3),
    ]
    parts += cross("CrossF", -D / 2, -1, red, shell)
    parts += cross("CrossB", D / 2, 1, red, shell)
    for sx in (-1, 1):
        x = sx * (W / 2 + 0.004)
        cz = SEAM_Z / 2 + 0.01
        parts.append(rounded_box(f"SideV{sx}", (0.03, 0.06, 0.2), (x, 0, cz), 0.01, red, 2))
        parts.append(rounded_box(f"SideH{sx}", (0.03, 0.2, 0.06), (x, 0, cz), 0.01, red, 2))
    for sx in (-1, 1):
        x = sx * 0.29
        parts.append(rounded_box(f"Latch{sx}", (0.1, 0.04, 0.12), (x, -D / 2 - 0.01, SEAM_Z), 0.012, steel, 3))
        parts.append(rounded_box(f"LatchB{sx}", (0.1, 0.04, 0.12), (x, D / 2 + 0.01, SEAM_Z), 0.012, steel, 3))
        parts.append(rounded_box(f"Mount{sx}", (0.08, 0.1, 0.035), (sx * 0.2, 0, H + 0.012), 0.012, steel, 3))
    for sx in (-1, 1):
        for sz in (0.055, H - 0.055):
            for sy in (-1, 1):
                parts.append(rounded_box(f"Corner{sx}{sy}{sz:.2f}", (0.115, 0.115, 0.115),
                                         (sx * (W / 2 - 0.045), sy * (D / 2 - 0.045), sz), 0.045, red_dark, 4))

    r, h = 0.05, 0.13
    pts = [(-0.2, 0, H + 0.02)]
    for k in range(9):
        a = math.pi - k * (math.pi / 2) / 8
        pts.append((-0.2 + r + r * math.cos(a), 0, H + h - r + r * math.sin(a)))
    for k in range(9):
        a = math.pi / 2 - k * (math.pi / 2) / 8
        pts.append((0.2 - r + r * math.cos(a), 0, H + h - r + r * math.sin(a)))
    pts.append((0.2, 0, H + 0.02))
    handle = tube("Handle", pts, 0.024, grip)
    apply_all(handle)
    parts.append(handle)

    kit = join(parts, "HealthPack")
    shade_smooth(kit, 35)
    lo, hi = world_bbox([kit])
    c = (lo + hi) / 2
    kit.location = -c
    apply_all(kit)
    return kit


def animate(kit):
    scene = bpy.context.scene
    scene.render.fps = FPS
    scene.frame_start, scene.frame_end = 0, FRAMES
    kit.animation_data_create()
    kit.animation_data.action = bpy.data.actions.new("SpinBob")
    prefs = bpy.context.preferences.edit
    prefs.keyframe_new_interpolation_type = "LINEAR"
    kit.rotation_euler = (0, 0, 0)
    kit.keyframe_insert("rotation_euler", index=2, frame=0)
    kit.rotation_euler = (0, 0, 2 * math.pi)
    kit.keyframe_insert("rotation_euler", index=2, frame=FRAMES)
    prefs.keyframe_new_interpolation_type = "BEZIER"
    for fr in range(0, FRAMES + 1, FRAMES // 4):
        kit.location = (0, 0, -0.045 if (fr // (FRAMES // 4)) % 2 == 0 else 0.045)
        kit.keyframe_insert("location", index=2, frame=fr)
    scene.frame_set(0)


reset()
kit = build()
animate(kit)
export_glb(os.path.join(OUT, f"{ID}.glb"), [kit], animations=True)
render_thumbnail(os.path.join(OUT, "thumbnail.png"), [kit], frame=0, view=(0.62, -1.0, 0.45), margin=1.1)
write_asset_json(OUT, ID, "Health Pack", "object", f"{ID}.glb",
                 description="Game-style first-aid kit with red crosses, a carry handle and steel latches, slowly spinning and bobbing like a pickup.",
                 tags=["health", "medkit", "first-aid", "game", "pickup", "gaming"],
                 extra={"animation": {"name": "SpinBob", "duration": FRAMES / FPS, "loop": True}})
