import math
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from drift3d import *  # noqa: E402,F403

ID = "emoji-face"
OUT = os.path.join(REPO, "objects", ID)
FPS, FRAMES = 30, 120

scene = reset()
scene.render.fps = FPS
scene.frame_start, scene.frame_end = 0, FRAMES

skin = material("EmojiYellow", "#ffc629", roughness=0.18)
dark = material("FeatureBrown", "#3a2414", roughness=0.15)
shine = material("EyeShine", "#ffffff", roughness=0.1)
blush = material("Blush", "#ff7b8c", roughness=0.35)

R = 0.48


def surf(lon, lat, r=R):
    """Point on the face sphere; lon/lat in degrees, lon 0 / lat 0 = straight at the camera (-Y)."""
    lo, la = math.radians(lon), math.radians(lat)
    return Vector((r * math.cos(la) * math.sin(lo), -r * math.cos(la) * math.cos(lo), r * math.sin(la)))


def orient(o, lon, lat):
    n = surf(lon, lat, 1.0)
    o.rotation_mode = "QUATERNION"
    o.rotation_quaternion = n.to_track_quat("-Y", "Z")


bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=R)
head = bpy.context.active_object
shade_smooth(head, 80)
assign(head, skin)
parts = [head]

for side in (-1, 1):
    lon, lat = 17 * side, 13
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1)
    eye = bpy.context.active_object
    eye.scale = (0.062, 0.05, 0.095)
    eye.location = surf(lon, lat, R - 0.012)
    orient(eye, lon, lat)
    shade_smooth(eye, 80)
    assign(eye, dark)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.022)
    hl = bpy.context.active_object
    hl.location = surf(lon - 2.5, lat + 3.2, R + 0.03)
    shade_smooth(hl, 80)
    assign(hl, shine)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.011)
    hl2 = bpy.context.active_object
    hl2.location = surf(lon + 2.2, lat - 3.5, R + 0.027)
    shade_smooth(hl2, 80)
    assign(hl2, shine)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=1)
    ch = bpy.context.active_object
    ch.scale = (0.075, 0.012, 0.045)
    ch.location = surf(37 * side, -5, R - 0.003)
    orient(ch, 37 * side, -5)
    shade_smooth(ch, 80)
    assign(ch, blush)
    parts += [eye, hl, ch, hl2]

# smile: a tube hugging the sphere, rounded ends
cu = bpy.data.curves.new("Smile", "CURVE")
cu.dimensions = "3D"
cu.bevel_depth = 0.03
cu.bevel_resolution = 6
cu.resolution_u = 4
sp = cu.splines.new("POLY")
N = 32
ends = []
sp.points.add(N - 1)
for i, p in enumerate(sp.points):
    s = -1 + 2 * i / (N - 1)
    lon = 25 * s
    lat = -17 - 14 * (1 - s * s)
    v = surf(lon, lat, R + 0.004)
    p.co = (*v, 1)
    if i in (0, N - 1):
        ends.append(v)
smile_o = bpy.data.objects.new("Smile", cu)
scene.collection.objects.link(smile_o)
bpy.context.view_layer.objects.active = smile_o
for o in bpy.context.selected_objects:
    o.select_set(False)
smile_o.select_set(True)
bpy.ops.object.convert(target="MESH")
smile = bpy.context.active_object
shade_smooth(smile, 80)
assign(smile, dark)
parts.append(smile)
for v in ends:
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.03, location=v)
    cap = bpy.context.active_object
    shade_smooth(cap, 80)
    assign(cap, dark)
    parts.append(cap)

for o in parts:
    apply_all(o)
obj = join(parts, "EmojiFace")

obj.rotation_mode = "XYZ"
for f in range(FRAMES + 1):
    u = 2 * math.pi * f / FRAMES
    obj.rotation_euler = (math.radians(9) * math.sin(2 * u), 0, math.radians(28) * math.sin(u))
    obj.keyframe_insert("rotation_euler", frame=f)
for fc in obj.animation_data.action.layers[0].strips[0].channelbags[0].fcurves:
    for kp in fc.keyframe_points:
        kp.interpolation = "LINEAR"
obj.animation_data.action.name = "LookAround"

os.makedirs(OUT, exist_ok=True)
export_glb(os.path.join(OUT, f"{ID}.glb"), [obj], animations=True)
render_thumbnail(os.path.join(OUT, "thumbnail.png"), [obj], frame=12, view=(0.45, -1.0, 0.25), margin=0.8)
write_asset_json(OUT, ID, "Emoji Face", "object", f"{ID}.glb",
                 description="Glossy yellow smiley face with 3D eyes and smile, looking around.",
                 tags=["emoji", "smile", "happy", "face", "reaction", "social"],
                 extra={"animation": {"name": "LookAround", "duration": FRAMES / FPS, "loop": True}})
