import math
import os
import random
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from drift3d import *  # noqa: E402,F403

ID = "disco-ball"
OUT = os.path.join(REPO, "objects", ID)
FPS, FRAMES = 30, 120

scene = reset()
scene.render.fps = FPS
scene.frame_start, scene.frame_end = 0, FRAMES
random.seed(7)

R = 0.42
CZ = -0.08
mats = [
    material("Silver", "#c9ced6", metallic=0.55, roughness=0.12),
    material("White", "#f4f6fa", metallic=0.35, roughness=0.08),
    material("IceBlue", "#a9d8ff", metallic=0.5, roughness=0.1),
    material("Pink", "#ffb8e0", metallic=0.5, roughness=0.1),
    material("Glint", "#ffffff", roughness=0.05, emission="#ffffff", emission_strength=1.0),
    material("Grout", "#2a2c33", metallic=0.3, roughness=0.6),
    material("Cap", "#9aa0aa", metallic=0.9, roughness=0.3),
]


def sph(lat, lon, r):
    return Vector((r * math.cos(lat) * math.cos(lon), r * math.cos(lat) * math.sin(lon), CZ + r * math.sin(lat)))


mesh = bpy.data.meshes.new("Ball")
bm = bmesh.new()
rings = 28
dlat = math.pi / rings
gap = 0.1
depth = 0.01
for i in range(rings):
    la0 = -math.pi / 2 + i * dlat
    la1 = la0 + dlat
    if i == rings - 1:
        continue  # top pole hidden under the cap
    mid = (la0 + la1) / 2
    n = max(4, round(2 * math.pi * math.cos(mid) / dlat))
    dlon = 2 * math.pi / n
    off = random.random() * dlon
    for j in range(n):
        lo0 = off + j * dlon
        lo1 = lo0 + dlon
        a0 = la0 + dlat * gap / 2
        a1 = la1 - dlat * gap / 2
        o0 = lo0 + dlon * gap / 2
        o1 = lo1 - dlon * gap / 2
        if i == 0:
            a0 = la0
        corners = [(a0, o0), (a0, o1), (a1, o1), (a1, o0)]
        # flat tile: project corners onto the tangent plane through the tile centre
        c = sph(mid, (lo0 + lo1) / 2, R)
        nrm = (c - Vector((0, 0, CZ))).normalized()
        outer = []
        for la, lo in corners:
            p = sph(la, lo, R)
            p = p - nrm * (p - c).dot(nrm)
            outer.append(p)
        inner = [p - nrm * depth for p in outer]
        vo = [bm.verts.new(p) for p in outer]
        vi = [bm.verts.new(p) for p in inner]
        r = random.random()
        mi = 4 if r < 0.035 else (0 if r < 0.52 else 1 if r < 0.78 else 2 if r < 0.91 else 3)
        f = bm.faces.new(vo)
        f.material_index = mi
        for k in range(4):
            s = bm.faces.new((vo[k], vi[k], vi[(k + 1) % 4], vo[(k + 1) % 4]))
            s.material_index = mi
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
bm.to_mesh(mesh)
bm.free()
ball = bpy.data.objects.new("Ball", mesh)
scene.collection.objects.link(ball)
for m in mats[:5]:
    ball.data.materials.append(m)

bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=R - depth * 0.6, location=(0, 0, CZ))
grout = bpy.context.active_object
shade_smooth(grout, 80)
assign(grout, mats[5])

top = CZ + R
bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.075, depth=0.05, location=(0, 0, top - 0.005))
cap = bpy.context.active_object
bev = cap.modifiers.new("b", "BEVEL")
bev.width, bev.segments = 0.012, 3
bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.045, depth=0.03, location=(0, 0, top + 0.035))
cap2 = bpy.context.active_object
b2 = cap2.modifiers.new("b", "BEVEL")
b2.width, b2.segments = 0.008, 2
bpy.ops.mesh.primitive_torus_add(major_radius=0.03, minor_radius=0.009, major_segments=24, minor_segments=8,
                                 location=(0, 0, top + 0.08), rotation=(math.pi / 2, 0, 0))
loop = bpy.context.active_object
parts = [cap, cap2, loop]
# chain: alternating links up to the top
z = top + 0.12
k = 0
while z < 0.58:
    bpy.ops.mesh.primitive_torus_add(major_radius=0.022, minor_radius=0.006, major_segments=16, minor_segments=6,
                                     location=(0, 0, z), rotation=(math.pi / 2, 0, (math.pi / 2) * (k % 2)))
    lk = bpy.context.active_object
    lk.scale = (1, 1.45, 1)
    parts.append(lk)
    z += 0.042
    k += 1
for p in parts:
    apply_all(p)
    shade_smooth(p, 50)
hw = join(parts, "Hardware")
assign(hw, mats[6])

for o in (ball, grout, hw):
    apply_all(o)
obj = join([ball, grout, hw], "DiscoBall")
obj.location = (0, 0, 0)

obj.rotation_mode = "XYZ"
obj.rotation_euler = (0, 0, 0)
obj.keyframe_insert("rotation_euler", index=2, frame=0)
obj.rotation_euler = (0, 0, 2 * math.pi)
obj.keyframe_insert("rotation_euler", index=2, frame=FRAMES)
for fc in obj.animation_data.action.layers[0].strips[0].channelbags[0].fcurves:
    for kp in fc.keyframe_points:
        kp.interpolation = "LINEAR"
obj.animation_data.action.name = "Spin"

os.makedirs(OUT, exist_ok=True)
export_glb(os.path.join(OUT, f"{ID}.glb"), [obj], animations=True)
render_thumbnail(os.path.join(OUT, "thumbnail.png"), [obj], frame=0, view=(0.55, -1.0, 0.3), margin=0.95)
write_asset_json(OUT, ID, "Disco Ball", "object", f"{ID}.glb",
                 description="Mirror-tiled disco ball hanging from a short chain, slowly spinning.",
                 tags=["disco", "party", "dance", "music", "retro", "night"],
                 extra={"animation": {"name": "Spin", "duration": FRAMES / FPS, "loop": True}})
