import math
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from drift3d import *  # noqa: E402,F403

ID = "like-thumb"
OUT = os.path.join(REPO, "objects", ID)
FPS, FRAMES = 30, 60

scene = reset()
scene.render.fps = FPS
scene.frame_start, scene.frame_end = 0, FRAMES

hand_mat = material("HandBlue", "#1f7bff", roughness=0.22)
cuff_mat = material("CuffWhite", "#f3f6fb", roughness=0.25)
button_mat = material("CuffButton", "#0f4fbf", roughness=0.3)


def rbox(x0, x1, z0, z1, depth, r, rot=0.0, y=0.0, seg=5):
    """Rounded box spanning x0..x1, z0..z1 (XZ plane, front = -Y), corner radius r."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=((x0 + x1) / 2, y, (z0 + z1) / 2))
    o = bpy.context.active_object
    o.scale = (x1 - x0, depth, z1 - z0)
    apply_all(o)
    b = o.modifiers.new("b", "BEVEL")
    b.width = r
    b.segments = seg
    b.limit_method = "NONE"
    o.rotation_euler = (0, rot, 0)
    apply_all(o)
    shade_smooth(o, 70)
    return o


D = 0.30  # hand thickness
parts = []
# palm
parts.append(rbox(-0.2, 0.12, -0.36, 0.08, D, 0.09))
# curled fingers: four rolls stacked on the right, index on top
for i, (x1, z0) in enumerate(((0.36, -0.03), (0.34, -0.14), (0.32, -0.25), (0.28, -0.36))):
    parts.append(rbox(-0.02, x1, z0, z0 + 0.118, D * 0.92, 0.055, y=-0.005))
# thumb, angled up and slightly back
parts.append(rbox(-0.13, 0.04, -0.08, 0.43, D * 0.8, 0.08, rot=math.radians(-9), y=0.01))
hand = join(parts, "Hand")
assign(hand, hand_mat)

cuff = rbox(-0.42, -0.2, -0.4, 0.1, D * 1.1, 0.05)
assign(cuff, cuff_mat)
bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=10, radius=0.028, location=(-0.31, -D * 0.55 - 0.005, -0.3))
btn = bpy.context.active_object
btn.scale = (1, 0.45, 1)
apply_all(btn)
shade_smooth(btn, 80)
assign(btn, button_mat)

objs = [hand, cuff, btn]
lo, hi = world_bbox(objs)
c = (lo + hi) / 2
for o in objs:
    o.location -= c
    apply_all(o)
obj = join(objs, "LikeThumb")

obj.rotation_mode = "XYZ"
for f in range(FRAMES + 1):
    t = f / FRAMES
    p = min(max((t - 0.08) / 0.62, 0.0), 1.0)
    decay = (1 - p) ** 2
    s = 1 + 0.2 * math.sin(2.5 * math.pi * p) * decay
    tilt = math.radians(-16) * math.sin(2 * math.pi * p) * (1 - p)
    obj.scale = (s, s, s)
    obj.rotation_euler = (0, tilt, 0)
    obj.location = (0, 0, 0.05 * math.sin(math.pi * p) * (1 - p))
    for prop in ("scale", "rotation_euler", "location"):
        obj.keyframe_insert(prop, frame=f)
for fc in obj.animation_data.action.layers[0].strips[0].channelbags[0].fcurves:
    for kp in fc.keyframe_points:
        kp.interpolation = "LINEAR"
obj.animation_data.action.name = "Pop"

os.makedirs(OUT, exist_ok=True)
export_glb(os.path.join(OUT, f"{ID}.glb"), [obj], animations=True)
render_thumbnail(os.path.join(OUT, "thumbnail.png"), [obj], frame=0, view=(0.5, -1.0, 0.25), margin=1.0)
write_asset_json(OUT, ID, "Like Thumb", "object", f"{ID}.glb",
                 description="Chunky glossy blue thumbs-up icon that tilts and pops.",
                 tags=["like", "thumbs-up", "youtube", "social", "approve", "call-to-action"],
                 extra={"animation": {"name": "Pop", "duration": FRAMES / FPS, "loop": True}})
