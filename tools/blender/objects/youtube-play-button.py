import math
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from drift3d import *  # noqa: E402,F403

ID = "youtube-play-button"
OUT = os.path.join(REPO, "objects", ID)
FPS, FRAMES = 30, 90

scene = reset()
scene.render.fps = FPS
scene.frame_start, scene.frame_end = 0, FRAMES

S = 1.0 / 28.57  # YouTube icon viewBox units -> 1 unit wide
W, H = 28.57 * S / 2, 20.0 * S / 2


def slab(name, pts, extrude, bevel, z):
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "2D"
    cu.fill_mode = "BOTH"
    cu.extrude = extrude
    cu.bevel_depth = bevel
    cu.bevel_resolution = 4
    cu.resolution_u = 1
    sp = cu.splines.new("POLY")
    sp.points.add(len(pts) - 1)
    for p, (x, y) in zip(sp.points, pts):
        p.co = (x, y, 0, 1)
    sp.use_cyclic_u = True
    ob = bpy.data.objects.new(name, cu)
    scene.collection.objects.link(ob)
    ob.location.z = z
    bpy.context.view_layer.objects.active = ob
    for o in bpy.context.selected_objects:
        o.select_set(False)
    ob.select_set(True)
    bpy.ops.object.convert(target="MESH")
    ob = bpy.context.active_object
    return ob


# YouTube's rounded body is close to a superellipse (squircle) with bulging sides
N = 160
body_pts = []
for i in range(N):
    t = 2 * math.pi * i / N
    c, s = math.cos(t), math.sin(t)
    n = 4.2
    x = W * math.copysign(abs(c) ** (2 / n), c)
    y = H * math.copysign(abs(s) ** (2 / n), s)
    body_pts.append((x, y))

T = 0.075
BEV = 0.035
body = slab("Body", body_pts, T, BEV, 0)
shade_smooth(body, 35)
assign(body, material("YouTubeRed", "#FF0000", roughness=0.28))

# play triangle from the official mark (viewBox 28.57x20): (11.43,5.71) (18.85,10) (11.43,14.29)
tri = [((x - 14.285) * S, (10 - y) * S) for x, y in ((11.43, 5.71), (18.85, 10.0), (11.43, 14.29))]
play = slab("Play", tri, 0.024, 0.008, T + BEV + 0.006)
shade_smooth(play, 35)
assign(play, material("PlayWhite", "#FFFFFF", roughness=0.25))

obj = join([body, play], "YouTubePlay")
obj.rotation_euler = (math.pi / 2, 0, 0)
apply_all(obj)

obj.rotation_mode = "XYZ"
for f in range(FRAMES + 1):
    u = 2 * math.pi * f / FRAMES
    obj.rotation_euler = (math.radians(4) * math.sin(2 * u), 0, math.radians(25) * math.sin(u))
    obj.location = (0, 0, 0.035 * math.sin(2 * u))
    obj.keyframe_insert("rotation_euler", frame=f)
    obj.keyframe_insert("location", frame=f)
for fc in obj.animation_data.action.layers[0].strips[0].channelbags[0].fcurves:
    for kp in fc.keyframe_points:
        kp.interpolation = "LINEAR"
obj.animation_data.action.name = "Sway"

os.makedirs(OUT, exist_ok=True)
export_glb(os.path.join(OUT, f"{ID}.glb"), [obj], animations=True)
render_thumbnail(os.path.join(OUT, "thumbnail.png"), [obj], frame=0, view=(0.55, -1.0, 0.3), margin=1.08)
write_asset_json(OUT, ID, "YouTube Play Button", "object", f"{ID}.glb",
                 description="3D YouTube play button logo with bevelled edges, gently swaying and bobbing.",
                 tags=["youtube", "play", "logo", "subscribe", "video", "social"],
                 extra={"animation": {"name": "Sway", "duration": FRAMES / FPS, "loop": True}})
