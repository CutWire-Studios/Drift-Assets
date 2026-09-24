import math
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from drift3d import *  # noqa: E402,F403
from mathutils import Euler, Matrix  # noqa: E402

ID = "cowboy-hat"
OUT = os.path.join(REPO, "face-props", ID)

RX, RY = 0.485, 0.575      # crown opening half-axes
CROWN_H = 0.52
BRIM_X, BRIM_Y = 0.27, 0.25
CURL = 0.3
PLACE = (0.0, 0.52, 0.47)
TILT = (math.radians(4), math.radians(-3), 0)
PROFILE = [(1.0, 0.0), (0.975, 0.3), (0.95, 0.6), (0.925, 0.86), (0.89, 0.96), (0.8, 1.0),
           (0.55, 1.02), (0.25, 1.03), (0.0, 1.03)]


def catmull(pts, n):
    pts = [Vector(p) for p in pts]
    out = []
    for i in range(len(pts) - 1):
        p0, p1, p2 = pts[max(i - 1, 0)], pts[i], pts[i + 1]
        p3 = pts[min(i + 2, len(pts) - 1)]
        for k in range(n):
            t = k / n
            out.append(0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(pts[-1])
    return out


def crown_point(theta, r, z, push=0.0):
    """Crown surface point for profile radius-scale r and height fraction z."""
    x = (RX * r + push) * math.cos(theta)
    y = (RY * r + push) * math.sin(theta)
    zz = z * CROWN_H
    top = max(0.0, min(1.0, (z - 0.55) / 0.45))
    # front pinch: dents either side of the front, growing toward the top
    for c in (-math.pi / 2 - 0.55, -math.pi / 2 + 0.55):
        d = (theta - c + math.pi) % (2 * math.pi) - math.pi
        k = math.exp(-(d / 0.42) ** 2) * top ** 1.2 * r
        x -= math.cos(theta) * 0.12 * k
        y -= math.sin(theta) * 0.05 * k
    # cattleman crease down the middle of the top, deeper toward the front
    fb = 0.75 - 0.25 * max(-1.0, min(1.0, y / RY))
    zz -= 0.085 * math.exp(-(x / 0.13) ** 2) * top ** 2 * fb * min(1.0, (1 - r) * 4 + 0.25)
    return Vector((x, y, zz))


def link(name, bm, mat):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(obj)
    assign(obj, mat)
    return obj


def grid_obj(name, rows, mat, closed_centre=None):
    """rows: list of vertex rings (same length, closed around)."""
    bm = bmesh.new()
    vr = [[bm.verts.new(p) for p in row] for row in rows]
    n = len(rows[0])
    for j in range(len(vr) - 1):
        for i in range(n):
            bm.faces.new((vr[j][i], vr[j][(i + 1) % n], vr[j + 1][(i + 1) % n], vr[j + 1][i]))
    if closed_centre is not None:
        c = bm.verts.new(closed_centre)
        for i in range(n):
            bm.faces.new((vr[-1][i], vr[-1][(i + 1) % n], c))
    return link(name, bm, mat)


def solidify(obj, t, offset=0.0, bevel=0.0):
    s = obj.modifiers.new("Solid", "SOLIDIFY")
    s.thickness = t
    s.offset = offset
    s.use_even_offset = True
    if bevel:
        b = obj.modifiers.new("Bevel", "BEVEL")
        b.width = bevel
        b.segments = 3
        b.limit_method = "ANGLE"
    apply_all(obj)
    return obj


def build():
    felt = material("CowboyFelt", "#6a4127", roughness=0.85)
    leather = material("CowboyBand", "#3a2417", roughness=0.55)
    silver = material("CowboyConcho", "#d9dde3", metallic=1.0, roughness=0.25)
    na = 128

    prof = catmull(PROFILE, 6)
    rows = [[crown_point(2 * math.pi * i / na, p.x, p.y) for i in range(na)] for p in prof[:-1]]
    crown = grid_obj("Crown", rows, felt, closed_centre=crown_point(0, 0, prof[-1].y))
    solidify(crown, 0.014, -1.0)

    brim_rows = []
    nr = 18
    for j in range(nr + 1):
        d = j / nr
        row = []
        for i in range(na):
            th = 2 * math.pi * i / na
            side = math.cos(th) ** 2
            x = (RX * 0.97 + BRIM_X * d) * math.cos(th)
            y = (RY * 0.97 + BRIM_Y * d) * math.sin(th)
            z = CURL * side ** 1.5 * d ** 1.8 - 0.06 * (1 - side) * d ** 1.5 + 0.005
            if math.sin(th) < 0:
                z -= 0.015 * (1 - side) * d
            row.append(Vector((x, y, z)))
        brim_rows.append(row)
    brim = grid_obj("Brim", brim_rows, felt)
    solidify(brim, 0.02, 0.0, bevel=0.008)

    band_rows = [[crown_point(2 * math.pi * i / na, r, z, push=0.009) for i in range(na)]
                 for r, z in ((1.0, 0.01), (0.99, 0.1), (0.985, 0.19))]
    band = grid_obj("Band", band_rows, leather)
    solidify(band, 0.008, 0.0, bevel=0.003)

    th = math.pi
    p = crown_point(th, 0.99, 0.1, push=0.024)
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.045, depth=0.012, location=p,
                                        rotation=(0, math.radians(90), 0))
    concho = bpy.context.active_object
    b = concho.modifiers.new("Bevel", "BEVEL")
    b.width = 0.005
    b.segments = 3
    assign(concho, silver)
    apply_all(concho)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=10, radius=0.019,
                                         location=p + Vector((-0.008, 0, 0)))
    stud = bpy.context.active_object
    stud.scale = (0.6, 1, 1)
    assign(stud, silver)
    silver_parts = join([concho, stud], "CowboyConcho")

    objs = [join([crown, brim], "CowboyHat"), band, silver_parts]
    m = Matrix.Translation(PLACE) @ Euler(TILT).to_matrix().to_4x4()
    for o in objs:
        apply_all(o)
        o.matrix_world = m
        apply_all(o)
        shade_smooth(o, 60)
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
        render_thumbnail(os.path.join(OUT, "_check3.png"), props, view=(-0.3, -0.5, 1.0),
                         margin=0.9)
    bpy.data.objects.remove(head, do_unlink=True)
    export_glb(os.path.join(OUT, f"{ID}.glb"), props)
    write_prop_json(OUT, ID, "Cowboy Hat", props,
                    description="Brown felt cowboy hat with curled brim sides, a pinched cattleman "
                                "crown, leather band and silver concho.",
                    tags=["cowboy", "hat", "western", "rodeo", "country", "felt"])
