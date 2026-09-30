import math
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from drift3d import *  # noqa: E402,F403
from mathutils import Euler, Matrix  # noqa: E402

ID = "party-hat"
OUT = os.path.join(REPO, "face-props", ID)

R_BASE = 0.22
HEIGHT = 0.6
N_AROUND = 108
N_UP = 48
STRIPES = 12          # multiple of 3 (pink / teal / yellow)
TWIST = 2 * math.pi * 0.55
PLACE = (0.13, 0.44, 0.80)
TILT = (math.radians(-8), math.radians(22), 0)


def new_obj(name, bm, mats):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(obj)
    for m in mats:
        me.materials.append(m)
    return obj


def cone(mats):
    bm = bmesh.new()
    rows = []
    for j in range(N_UP):
        h = HEIGHT * j / N_UP
        r = R_BASE * (1 - j / N_UP)
        rows.append([bm.verts.new((r * math.cos(a), r * math.sin(a), h))
                     for a in (2 * math.pi * i / N_AROUND + TWIST * j / N_UP for i in range(N_AROUND))])
    apex = bm.verts.new((0, 0, HEIGHT))
    per = N_AROUND // STRIPES
    for j in range(N_UP):
        for i in range(N_AROUND):
            i2 = (i + 1) % N_AROUND
            if j < N_UP - 1:
                f = bm.faces.new((rows[j][i], rows[j][i2], rows[j + 1][i2], rows[j + 1][i]))
            else:
                f = bm.faces.new((rows[j][i], rows[j][i2], apex))
            f.material_index = (i // per) % 3
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    obj = new_obj("PartyHatCone", bm, mats)
    sol = obj.modifiers.new("Solid", "SOLIDIFY")
    sol.thickness = 0.012
    sol.offset = -1.0
    apply_all(obj)
    return obj


def ruffle(mat):
    na, nr = 192, 12
    bm = bmesh.new()
    rings = []
    for i in range(na):
        a = 2 * math.pi * i / na
        out = Vector((math.cos(a), math.sin(a), 0))
        c = out * (R_BASE + 0.004) + Vector((0, 0, 0.012))
        tr = 0.024 * (1 + 0.3 * math.cos(18 * a))
        rings.append([bm.verts.new(c + (out * math.cos(2 * math.pi * k / nr) * 1.0
                                        + Vector((0, 0, 1)) * math.sin(2 * math.pi * k / nr) * 0.85) * tr)
                      for k in range(nr)])
    for i in range(na):
        a, b = rings[i], rings[(i + 1) % na]
        for k in range(nr):
            bm.faces.new((a[k], a[(k + 1) % nr], b[(k + 1) % nr], b[k]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return new_obj("PartyHatRuffle", bm, [mat])


def pompom(mat):
    parts = []
    centre = Vector((0, 0, HEIGHT + 0.045))
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=12, radius=0.07, location=centre)
    parts.append(bpy.context.active_object)
    n = 30
    golden = math.pi * (3 - math.sqrt(5))
    for i in range(n):
        z = 1 - 2 * (i + 0.5) / n
        r = math.sqrt(1 - z * z)
        d = Vector((r * math.cos(golden * i), r * math.sin(golden * i), z))
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=0.034,
                                             location=centre + d * 0.06)
        parts.append(bpy.context.active_object)
    for p in parts:
        assign(p, mat)
    return join(parts, "PartyHatPompom")


def star(mat, points=5, r_out=0.085, r_in=0.038, depth=0.035):
    """Puffy 5-point star standing upright on the cone tip."""
    bm = bmesh.new()
    front, back = [], []
    for k in range(points * 2):
        a = math.pi / 2 + math.pi * k / points
        r = r_out if k % 2 == 0 else r_in
        front.append(bm.verts.new((r * math.cos(a), -depth / 2, r * math.sin(a))))
        back.append(bm.verts.new((r * math.cos(a), depth / 2, r * math.sin(a))))
    cf = bm.verts.new((0, -depth * 1.1, 0))
    cb = bm.verts.new((0, depth * 1.1, 0))
    n = len(front)
    for k in range(n):
        bm.faces.new((cf, front[k], front[(k + 1) % n]))
        bm.faces.new((cb, back[(k + 1) % n], back[k]))
        bm.faces.new((front[k], back[k], back[(k + 1) % n], front[(k + 1) % n]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    obj = new_obj("PartyHatStar", bm, [mat])
    obj.location = (0, 0, HEIGHT + 0.07)
    return obj


def trim_ring(mat):
    bpy.ops.mesh.primitive_torus_add(major_radius=R_BASE + 0.004, minor_radius=0.014, major_segments=96,
                                     minor_segments=10, location=(0, 0, 0.012))
    return assign(bpy.context.active_object, mat)


def build(opts=None):
    style = (opts or {}).get("style", "classic")
    pink = material("PartyPink", "#ff4fa3", roughness=0.45)
    teal = material("PartyTeal", "#17c3b2", roughness=0.45)
    yellow = material("PartyYellow", "#ffd23f", roughness=0.45)
    white = material("PartyWhite", "#fff6fb", roughness=0.8)
    if style == "star":
        gold = material("PartyGold", "#f5c542", metallic=0.9, roughness=0.3)
        navy = material("PartyNavy", "#26235e", roughness=0.4)
        purple = material("PartyPurple", "#7b4bff", roughness=0.4)
        objs = [cone([navy, purple, navy]), trim_ring(gold), star(gold)]
    else:
        objs = [cone([pink, teal, yellow]), ruffle(white), pompom(white)]
    m = Matrix.Translation(PLACE) @ Euler(TILT).to_matrix().to_4x4()
    for o in objs:
        apply_all(o)
        o.matrix_world = m
        apply_all(o)
        shade_smooth(o, 50)
    return objs


if __name__ == "__main__":
    build_prop_variants(ID, "Party Hat", "Cone party hat perched on top of the head at a jaunty angle.",
                        ["party", "hat", "birthday", "celebration", "cone", "fun"], [
        ("classic", "Pom-Pom Stripes", {"style": "classic",
                                        "description": "Striped pink, teal and yellow cone party hat with a fluffy pom-pom."}),
        ("star", "Gold Star", {"style": "star",
                               "description": "Navy and purple swirl cone with a gold trim and a gold star on top."}),
    ], build, region="head")
