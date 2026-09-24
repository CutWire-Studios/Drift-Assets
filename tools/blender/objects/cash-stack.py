import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from drift3d import *  # noqa: E402,F403

ID = "cash-stack"
OUT = os.path.join(REPO, "objects", ID)
FPS = 30
FRAMES = 120
BOB = 0.03

L, WD = 0.78, 0.34
SHEETS = 7
SHEET_T = 0.012
BUNDLE_T = SHEETS * SHEET_T


def box(size, loc, bevel=0.0, segments=2):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    ob = bpy.context.active_object
    ob.scale = size
    apply_all(ob)
    if bevel:
        m = ob.modifiers.new("Bevel", "BEVEL")
        m.width = bevel
        m.segments = segments
        m.limit_method = "NONE"
        apply_all(ob)
    return ob


def disc(rx, ry, h, loc, verts=48):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=1, depth=h, location=loc)
    ob = bpy.context.active_object
    ob.scale = (rx, ry, 1)
    apply_all(ob)
    return ob


def frame(lx, ly, t, h, z):
    return [box((lx, t, h), (0, ly / 2 - t / 2, z)), box((lx, t, h), (0, -ly / 2 + t / 2, z)),
            box((t, ly - 2 * t, h), (lx / 2 - t / 2, 0, z)), box((t, ly - 2 * t, h), (-lx / 2 + t / 2, 0, z))]


def by_normal(ob, top_mat, side_mat):
    ob.data.materials.clear()
    ob.data.materials.append(top_mat)
    ob.data.materials.append(side_mat)
    for p in ob.data.polygons:
        p.material_index = 0 if abs(p.normal.z) > 0.7 else 1
    return ob


def bundle(rng, m):
    parts = []
    for i in range(SHEETS):
        z = SHEET_T * (i + 0.5)
        sh = box((L, WD, SHEET_T), (rng.uniform(-0.004, 0.004), rng.uniform(-0.003, 0.003), z),
                 bevel=0.0035)
        sh.rotation_euler.z = rng.uniform(-0.006, 0.006)
        apply_all(sh)
        parts.append(by_normal(sh, m["note"], m["edge"]))

    top = BUNDLE_T
    h = 0.0025
    for ob in frame(L - 0.04, WD - 0.04, 0.018, h, top + h / 2):
        parts.append(assign(ob, m["ink"]))
    for ob in frame(L - 0.085, WD - 0.085, 0.006, h, top + h / 2):
        parts.append(assign(ob, m["ink"]))
    for sx in (-1, 1):
        x = sx * 0.19
        parts.append(assign(disc(0.08, 0.092, h * 2, (x, 0, top + h)), m["ink"]))
        parts.append(assign(disc(0.066, 0.078, h * 3, (x, 0, top + h * 1.5)), m["light"]))
        parts.append(assign(disc(0.036, 0.046, h * 4, (x, 0, top + h * 2)), m["ink"]))
        for sy in (-1, 1):
            parts.append(assign(disc(0.026, 0.026, h * 2, (sx * 0.32, sy * 0.105, top + h), verts=32),
                                m["light"]))

    band_w = 0.11
    band = box((band_w, WD + 0.012, BUNDLE_T + 0.01), (0, 0, BUNDLE_T / 2), bevel=0.003)
    parts.append(assign(band, m["band"]))
    parts.append(assign(box((band_w * 0.45, WD * 0.55, 0.004), (0, 0, BUNDLE_T + 0.006)), m["label"]))
    return join(parts, "Bundle")


def build():
    m = {
        "note": material("NoteGreen", "#6fae5a", roughness=0.75),
        "edge": material("PaperEdge", "#d3e3bd", roughness=0.85),
        "ink": material("NoteInk", "#2f6b33", roughness=0.7),
        "light": material("NoteLight", "#b5d99a", roughness=0.7),
        "band": material("Band", "#8a55c7", roughness=0.55),
        "label": material("BandLabel", "#f3e6c4", roughness=0.6),
    }
    rng = random.Random(7)
    placement = [(0.0, 0.0, 4), (0.02, -0.015, -7), (-0.025, 0.01, 3), (0.015, 0.02, -10)]
    bundles = []
    for k, (dx, dy, rot) in enumerate(placement):
        b = bundle(rng, m)
        b.location = (dx, dy, k * (BUNDLE_T + 0.008))
        b.rotation_euler.z = math.radians(rot)
        apply_all(b)
        bundles.append(b)
    obj = join(bundles, "CashStack")
    lo, hi = world_bbox([obj])
    c = (lo + hi) / 2
    for v in obj.data.vertices:
        v.co -= c
    shade_smooth(obj, 30)
    return obj


def animate(obj):
    scene = bpy.context.scene
    scene.render.fps = FPS
    scene.frame_start, scene.frame_end = 0, FRAMES
    obj.animation_data_create()
    obj.animation_data.action = bpy.data.actions.new("SpinBob")
    obj.rotation_euler = (0, 0, 0)
    obj.keyframe_insert("rotation_euler", index=2, frame=0)
    obj.rotation_euler = (0, 0, 2 * math.pi)
    obj.keyframe_insert("rotation_euler", index=2, frame=FRAMES)
    for f in range(FRAMES + 1):
        obj.location = (0, 0, BOB * math.sin(4 * math.pi * f / FRAMES))
        obj.keyframe_insert("location", index=2, frame=f)
    for fc in obj.animation_data.action.layers[0].strips[0].channelbags[0].fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"
    obj.rotation_euler = (0, 0, 0)
    obj.location = (0, 0, 0)


reset()
stack = build()
animate(stack)
export_glb(os.path.join(OUT, f"{ID}.glb"), [stack], animations=True)
render_thumbnail(os.path.join(OUT, "thumbnail.png"), [stack], frame=0, view=(0.6, -1.0, 0.75),
                 margin=1.1)
write_asset_json(OUT, ID, "Cash Stack", "object", f"{ID}.glb",
                 description="Pile of four banded bundles of green banknotes, slowly spinning and bobbing like a game money pickup.",
                 tags=["cash", "money", "banknotes", "stack", "pickup", "gaming", "spin"],
                 extra={"animation": {"name": "SpinBob", "duration": FRAMES / FPS, "loop": True}})
