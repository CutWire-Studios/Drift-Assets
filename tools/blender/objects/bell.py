import math
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from drift3d import *  # noqa: E402,F403
from mathutils import Matrix  # noqa: E402

ID = "bell"
OUT = os.path.join(REPO, "objects", ID)
FPS, FRAMES = 30, 60

scene = reset()
scene.render.fps = FPS
scene.frame_start, scene.frame_end = 0, FRAMES

gold = material("Gold", "#ffc233", metallic=0.75, roughness=0.28)
gold_in = material("GoldInner", "#a86a12", metallic=0.3, roughness=0.5)
clapper_mat = material("Clapper", "#ffd766", metallic=0.35, roughness=0.25)


def lathe(name, prof, steps=72, inside=None):
    """Revolve an (r, z) polyline about Z. Normals face away from the point `inside` (radially if None)."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    vs = [bm.verts.new((r, 0, z)) for r, z in prof]
    edges = [bm.edges.new((vs[i], vs[i + 1])) for i in range(len(vs) - 1)]
    bmesh.ops.spin(bm, geom=vs + edges, cent=(0, 0, 0), axis=(0, 0, 1), angle=2 * math.pi, steps=steps,
                   use_merge=True)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
    for f in bm.faces:
        c = f.calc_center_median()
        away = c - Vector(inside) if inside else Vector((c.x, c.y, 0))
        if f.normal.dot(away) < 0:
            f.normal_flip()
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    scene.collection.objects.link(o)
    shade_smooth(o, 50)
    return o


def smooth_curve(pts, n=6):
    """Catmull-Rom resample of a polyline (keeps endpoints)."""
    out = []
    P = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in range(2)))
    out.append(pts[-1])
    return out


outer = smooth_curve([(0.0, 0.33), (0.1, 0.325), (0.19, 0.3), (0.25, 0.24), (0.275, 0.14), (0.285, 0.02),
                      (0.3, -0.1), (0.34, -0.19), (0.4, -0.245), (0.445, -0.27)])
lip = [(0.46, -0.285), (0.462, -0.305), (0.45, -0.322), (0.425, -0.325)]
inner = smooth_curve([(0.405, -0.305), (0.36, -0.27), (0.305, -0.2), (0.265, -0.09), (0.25, 0.04),
                      (0.23, 0.17), (0.17, 0.25), (0.08, 0.28), (0.0, 0.285)])
body = lathe("BellBody", outer + lip + inner)
bpy.ops.object.select_all(action="DESELECT")
bm = bmesh.new()
bm.from_mesh(body.data)
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
for f in bm.faces:
    c = f.calc_center_median()
    f.material_index = 1 if f.normal.dot(Vector((c.x, c.y, 0))) < 0 or f.normal.z < -0.7 and c.z > -0.3 else 0
bm.to_mesh(body.data)
bm.free()
body.data.materials.append(gold)
body.data.materials.append(gold_in)

# raised band around the waist
band = lathe("Band", smooth_curve([(0.296, -0.075), (0.312, -0.068), (0.318, -0.05), (0.312, -0.032), (0.29, -0.025)], 3))
assign(band, gold)

# top knob and hanging loop
knob = lathe("Knob", smooth_curve([(0.0, 0.39), (0.03, 0.385), (0.05, 0.37), (0.06, 0.345), (0.07, 0.325), (0.09, 0.315)], 4), 48, inside=(0, 0, 0.3))
assign(knob, gold)
bpy.ops.mesh.primitive_torus_add(major_radius=0.055, minor_radius=0.018, major_segments=40, minor_segments=12,
                                 location=(0, 0, 0.44), rotation=(math.pi / 2, 0, 0))
loop = bpy.context.active_object
shade_smooth(loop, 80)
assign(loop, gold)

# clapper: rod + ball peeking below the lip
bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.016, depth=0.6, location=(0, 0, -0.1))
rod = bpy.context.active_object
assign(rod, gold_in)
bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.085, location=(0, 0, -0.45))
ball = bpy.context.active_object
shade_smooth(ball, 80)
assign(ball, clapper_mat)

parts = [body, band, knob, loop, rod, ball]
lo, hi = world_bbox(parts)
c = (lo + hi) / 2
for o in parts:
    o.location -= c
    apply_all(o)
obj = join(parts, "Bell")
pivot = Vector((0, 0, 0.44)) - c  # swing about the hanging loop

obj.rotation_mode = "XYZ"
for f in range(FRAMES + 1):
    u = 2 * math.pi * f / FRAMES
    a = math.radians(15) * math.sin(u)
    rot = Matrix.Rotation(a, 3, "Y")
    obj.rotation_euler = (0, a, 0)
    obj.location = pivot - rot @ pivot
    obj.keyframe_insert("rotation_euler", frame=f)
    obj.keyframe_insert("location", frame=f)
for fc in obj.animation_data.action.layers[0].strips[0].channelbags[0].fcurves:
    for kp in fc.keyframe_points:
        kp.interpolation = "LINEAR"
obj.animation_data.action.name = "Ring"

os.makedirs(OUT, exist_ok=True)
export_glb(os.path.join(OUT, f"{ID}.glb"), [obj], animations=True)
render_thumbnail(os.path.join(OUT, "thumbnail.png"), [obj], frame=10, view=(0.5, -1.0, 0.0), margin=0.92)
write_asset_json(OUT, ID, "Notification Bell", "object", f"{ID}.glb",
                 description="Gold notification bell with clapper, swinging as it rings.",
                 tags=["bell", "notification", "subscribe", "youtube", "alert", "gold"],
                 extra={"animation": {"name": "Ring", "duration": FRAMES / FPS, "loop": True}})
