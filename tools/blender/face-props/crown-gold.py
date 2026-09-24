import math
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from drift3d import *  # noqa: E402,F403
from mathutils import Euler, Matrix  # noqa: E402

ID = "crown-gold"
OUT = os.path.join(REPO, "face-props", ID)

RX, RY = 0.36, 0.40     # base ellipse half-axes
BAND_H = 0.12
PEAK_H = 0.22
FLARE = 0.35              # radius grows by this fraction per unit height
N_PEAKS = 5
PLACE = (0.0, 0.5, 0.65)
TILT = (math.radians(-6), math.radians(-9), 0)


def ring_point(theta, z):
    f = 1 + FLARE * z
    return Vector((RX * f * math.cos(theta), RY * f * math.sin(theta), z))


def crown_height(theta):
    step = 2 * math.pi / N_PEAKS
    phi = (theta + math.pi / 2) % step
    u = abs(phi - step if phi > step / 2 else phi) / (step / 2)
    return BAND_H + PEAK_H * (1 - u) ** 1.7


def peak_angles():
    return [-math.pi / 2 + i * 2 * math.pi / N_PEAKS for i in range(N_PEAKS)]


def crown_wall(mat):
    na, nz = 200, 14
    bm = bmesh.new()
    rows = []
    for i in range(na):
        th = 2 * math.pi * i / na
        h = crown_height(th)
        rows.append([bm.verts.new(ring_point(th, h * j / (nz - 1))) for j in range(nz)])
    for i in range(na):
        a, b = rows[i], rows[(i + 1) % na]
        for j in range(nz - 1):
            bm.faces.new((a[j], b[j], b[j + 1], a[j + 1]))
    me = bpy.data.meshes.new("CrownWall")
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new("CrownWall", me)
    bpy.context.scene.collection.objects.link(obj)
    sol = obj.modifiers.new("Solid", "SOLIDIFY")
    sol.thickness = 0.022
    sol.offset = -1.0
    sol.use_even_offset = True
    bev = obj.modifiers.new("Bevel", "BEVEL")
    bev.width = 0.005
    bev.segments = 2
    bev.limit_method = "ANGLE"
    assign(obj, mat)
    apply_all(obj)
    return obj


def ellipse_tube(name, z, radius, mat, grow=0.0):
    na, nr = 160, 12
    bm = bmesh.new()
    rings = []
    for i in range(na):
        th = 2 * math.pi * i / na
        c = ring_point(th, z)
        out = Vector((c.x, c.y, 0)).normalized()
        c = c + out * grow
        rings.append([bm.verts.new(c + (out * math.cos(2 * math.pi * k / nr)
                                        + Vector((0, 0, 1)) * math.sin(2 * math.pi * k / nr)) * radius)
                      for k in range(nr)])
    for i in range(na):
        a, b = rings[i], rings[(i + 1) % na]
        for k in range(nr):
            bm.faces.new((a[k], a[(k + 1) % nr], b[(k + 1) % nr], b[k]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(obj)
    assign(obj, mat)
    return obj


def sphere(name, loc, r, mat, scale=(1, 1, 1), seg=24, rings=16):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=rings, radius=r, location=loc)
    o = bpy.context.active_object
    o.name = name
    o.scale = scale
    assign(o, mat)
    return o


def outward(theta):
    n = Vector((math.cos(theta) / RX, math.sin(theta) / RY, 0)).normalized()
    return n


def gem(name, theta, z, r, mat, gold, bezel=True):
    p = ring_point(theta, z)
    n = outward(theta)
    n = (n + Vector((0, 0, -FLARE * 0.3))).normalized()
    parts = []
    g = sphere(name, (0, 0, 0), r, mat, scale=(1, 1, 0.55))
    g.location = p + n * 0.012
    g.rotation_euler = n.to_track_quat("Z", "Y").to_euler()
    parts.append(g)
    if bezel:
        bpy.ops.mesh.primitive_torus_add(major_radius=r * 1.02, minor_radius=r * 0.2,
                                         major_segments=32, minor_segments=8)
        t = bpy.context.active_object
        t.name = name + "Bezel"
        t.location = p + n * 0.012
        t.rotation_euler = n.to_track_quat("Z", "Y").to_euler()
        assign(t, gold)
        parts.append(t)
    return parts


def build():
    gold = material("CrownGold", "#f5c542", metallic=1.0, roughness=0.28)
    red = material("GemRed", "#e0102f", roughness=0.08, emission="#5a0010", emission_strength=0.4)
    blue = material("GemBlue", "#1f63ff", roughness=0.08, emission="#001a5a", emission_strength=0.4)

    gold_parts = [crown_wall(gold),
                  ellipse_tube("RimLow", 0.0, 0.018, gold, grow=0.012),
                  ellipse_tube("RimHigh", BAND_H, 0.014, gold, grow=0.012)]
    gems_red, gems_blue = [], []
    for i, th in enumerate(peak_angles()):
        tip = ring_point(th, BAND_H + PEAK_H) + outward(th) * 0.011
        gold_parts.append(sphere(f"Ball{i}", tip, 0.028, gold))
        big = gem(f"Gem{i}", th, BAND_H / 2, 0.042, red if i % 2 == 0 else blue, gold)
        (gems_red if i % 2 == 0 else gems_blue).append(big[0])
        gold_parts += big[1:]
        small = gem(f"Pearl{i}", th + math.pi / N_PEAKS, BAND_H / 2, 0.02,
                    blue if i % 2 == 0 else red, gold, bezel=False)
        (gems_blue if i % 2 == 0 else gems_red).append(small[0])
        gold_parts.append(sphere(f"Stud{i}", ring_point(th, BAND_H + 0.06) + outward(th) * 0.013,
                                 0.016, gold, scale=(1, 1, 1)))

    objs = [join(gold_parts, "CrownGold"), join(gems_red, "CrownGemsRed"),
            join(gems_blue, "CrownGemsBlue")]
    m = Matrix.Translation(PLACE) @ Euler(TILT).to_matrix().to_4x4()
    for o in objs:
        apply_all(o)
        o.matrix_world = m
        apply_all(o)
        shade_smooth(o, 40)
    return objs


if __name__ == "__main__":
    reset()
    head = reference_head()
    props = build()
    os.makedirs(OUT, exist_ok=True)
    render_prop_thumbnail(os.path.join(OUT, "thumbnail.png"), props, head, region="head")
    if "--check" in args():
        render_thumbnail(os.path.join(OUT, "_check.png"), [head] + props, view=(0, -1, 0.05),
                         margin=1.05)
        render_thumbnail(os.path.join(OUT, "_check2.png"), [head] + props, view=(-1, 0, 0.05),
                         margin=1.05)
        render_thumbnail(os.path.join(OUT, "_check3.png"), props, view=(1, -0.3, 0.2),
                         margin=0.7)
    bpy.data.objects.remove(head, do_unlink=True)
    export_glb(os.path.join(OUT, f"{ID}.glb"), props)
    write_prop_json(OUT, ID, "Gold Crown", props,
                    description="Polished gold five-point royal crown set with red and blue "
                                "cabochon gems, worn at a slight tilt.",
                    tags=["crown", "king", "queen", "royal", "gold", "hat", "jewel"])
