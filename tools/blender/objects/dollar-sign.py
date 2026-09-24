import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from drift3d import *  # noqa: E402,F403

ID = "dollar-sign"
OUT = os.path.join(REPO, "objects", ID)
FPS = 30
FRAMES = 60
BOB = 0.04

RX, RY, W = 0.25, 0.2, 0.17
DEPTH = 0.085
BEVEL = 0.03


def s_centerline(n=64):
    """Centre line of the S: top bowl counter-clockwise from the upper-right terminal down to the
    spine, then the bottom bowl clockwise round to the lower-left terminal."""
    pts = []
    a0, a1 = math.radians(18), math.radians(270)
    for i in range(n + 1):
        a = a0 + (a1 - a0) * i / n
        pts.append((RX * math.cos(a), RY + RY * math.sin(a)))
    a0, a1 = math.radians(90), math.radians(-162)
    for i in range(1, n + 1):
        a = a0 + (a1 - a0) * i / n
        pts.append((RX * math.cos(a), -RY + RY * math.sin(a)))
    return pts


def stroke_outline(pts, w):
    left, right = [], []
    for i, (x, y) in enumerate(pts):
        px, py = pts[max(i - 1, 0)]
        nx_, ny_ = pts[min(i + 1, len(pts) - 1)]
        tx, ty = nx_ - px, ny_ - py
        ln = math.hypot(tx, ty)
        nx, ny = -ty / ln, tx / ln
        left.append((x + nx * w / 2, y + ny * w / 2))
        right.append((x - nx * w / 2, y - ny * w / 2))
    return left + right[::-1]


def rounded_bar(w, h, seg=12):
    r = w / 2
    pts = []
    for cy, a0 in ((h / 2 - r, 0), (-h / 2 + r, math.pi)):
        for i in range(seg + 1):
            a = a0 + math.pi * i / seg
            pts.append((r * math.cos(a), cy + r * math.sin(a)))
    return pts


def extruded(name, outline, depth, bevel):
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "2D"
    cu.fill_mode = "BOTH"
    cu.extrude = depth - bevel
    cu.bevel_mode = "ROUND"
    cu.bevel_depth = bevel
    cu.bevel_resolution = 4
    cu.offset = -bevel
    sp = cu.splines.new("POLY")
    sp.points.add(len(outline) - 1)
    for p, (x, y) in zip(sp.points, outline):
        p.co = (x, y, 0, 1)
    sp.use_cyclic_u = True
    ob = bpy.data.objects.new(name, cu)
    bpy.context.scene.collection.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
    for o in bpy.context.selected_objects:
        o.select_set(False)
    ob.select_set(True)
    bpy.ops.object.convert(target="MESH")
    ob = bpy.context.active_object
    ob.rotation_euler = (math.pi / 2, 0, 0)
    apply_all(ob)
    return ob


def build():
    face = material("DollarFace", "#2ecc40", roughness=0.3, emission="#0c4a15")
    side = material("DollarSide", "#1c9e2e", roughness=0.35, emission="#083510")
    bar_face = material("DollarBar", "#5be36a", roughness=0.28, emission="#0f5a1c")

    s = extruded("S", stroke_outline(s_centerline(), W), DEPTH, BEVEL)
    bar = extruded("Bar", rounded_bar(0.11, 1.14), DEPTH * 0.8, BEVEL * 0.8)
    for ob, front in ((s, face), (bar, bar_face)):
        ob.data.materials.append(front)
        ob.data.materials.append(side)
        for p in ob.data.polygons:
            p.material_index = 0 if abs(p.normal.y) > 0.9 else 1
    obj = join([s, bar], "DollarSign")
    shade_smooth(obj, 35)
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
        obj.location = (0, 0, BOB * math.sin(2 * math.pi * f / FRAMES))
        obj.keyframe_insert("location", index=2, frame=f)
    for fc in obj.animation_data.action.layers[0].strips[0].channelbags[0].fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"
    obj.rotation_euler = (0, 0, 0)
    obj.location = (0, 0, 0)


reset()
sign = build()
animate(sign)
export_glb(os.path.join(OUT, f"{ID}.glb"), [sign], animations=True)
render_thumbnail(os.path.join(OUT, "thumbnail.png"), [sign], frame=0, view=(0.55, -1.0, 0.3))
write_asset_json(OUT, ID, "Dollar Sign", "object", f"{ID}.glb",
                 description="Chunky bevelled green dollar sign with a soft glow, spinning and bobbing like a game money pickup.",
                 tags=["dollar", "money", "cash", "pickup", "gaming", "green", "spin"],
                 extra={"animation": {"name": "SpinBob", "duration": FRAMES / FPS, "loop": True}})
