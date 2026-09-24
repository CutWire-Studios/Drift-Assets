import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from drift3d import *  # noqa: E402,F403

ID = "mystery-block"
OUT = os.path.join(REPO, "objects", ID)
FPS = 30
FRAMES = 90
S = 0.8
EDGE_BEVEL = 0.05
INSET = 0.065
RECESS = 0.018
G = 1.15


def mesh_object(name, bm):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    return ob


def block_body(gold, panel):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=S)
    bmesh.ops.bevel(bm, geom=list(bm.edges), offset=EDGE_BEVEL, segments=4, profile=0.5,
                    affect="EDGES", clamp_overlap=True)
    big = [f for f in bm.faces if f.calc_area() > (S - 2 * EDGE_BEVEL) ** 2 * 0.9]
    res = bmesh.ops.inset_individual(bm, faces=big, thickness=INSET, depth=-RECESS)
    ob = mesh_object("Block", bm)
    ob.data.materials.append(gold)
    ob.data.materials.append(panel)
    for p in ob.data.polygons:
        n = p.normal
        c = p.center
        axis = max(range(3), key=lambda i: abs(n[i]))
        if abs(n[axis]) > 0.99 and abs(abs(c[axis]) - (S / 2 - RECESS)) < 1e-4:
            p.material_index = 1
    mod = ob.modifiers.new("Bevel", "BEVEL")
    mod.width = 0.008
    mod.segments = 2
    mod.limit_method = "ANGLE"
    mod.angle_limit = math.radians(30)
    apply_all(ob)
    return ob


def glyph_outline(width):
    """Outline of an original chunky '?' hook+stem, in (u, v) face coordinates."""
    cx, cy, r = 0.0, 0.085, 0.105
    centre = []
    n = 22
    a0, a1 = math.radians(165), math.radians(-38)
    for k in range(n + 1):
        a = a0 + (a1 - a0) * k / n
        centre.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    p0 = centre[-1]
    t0 = (math.sin(a1), -math.cos(a1))
    p3 = (0.0, -0.075)
    c1 = (p0[0] + t0[0] * 0.045, p0[1] + t0[1] * 0.045)
    c2 = (p3[0], p3[1] + 0.1)
    for k in range(1, 9):
        t = k / 8
        m = 1 - t
        centre.append(tuple(m ** 3 * p0[i] + 3 * m * m * t * c1[i] + 3 * m * t * t * c2[i] + t ** 3 * p3[i]
                            for i in range(2)))
    centre.append((0.0, -0.1))
    hw = width / 2

    def normal(i):
        a = centre[max(i - 1, 0)]
        b = centre[min(i + 1, len(centre) - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(dx, dy)
        return (-dy / ln, dx / ln)

    left = [(p[0] + normal(i)[0] * hw, p[1] + normal(i)[1] * hw) for i, p in enumerate(centre)]
    right = [(p[0] - normal(i)[0] * hw, p[1] - normal(i)[1] * hw) for i, p in enumerate(centre)]
    sx, sy = centre[0]
    nx, ny = normal(0)
    base = math.atan2(ny, nx)
    cap = [(sx + hw * math.cos(base + math.pi - math.pi * k / 8), sy + hw * math.sin(base + math.pi - math.pi * k / 8))
           for k in range(1, 8)]
    return left, right, cap, (sx, sy)


def glyph(name, width, depth, mat, du=0.0, dv=0.0, dot=True):
    """'?' on the front face (-Y) extruded toward -Y from the panel plane."""
    y0 = -(S / 2 - RECESS) + 0.002
    bm = bmesh.new()
    left, right, cap, start = glyph_outline(width)

    def vert(p):
        return bm.verts.new((G * p[0] + du, y0, G * p[1] + dv))

    lv = [vert(p) for p in left]
    rv = [vert(p) for p in right]
    hub = vert(start)
    bm.faces.new((lv[0], lv[1], rv[1], rv[0], hub))
    for i in range(1, len(lv) - 1):
        bm.faces.new((lv[i], lv[i + 1], rv[i + 1], rv[i]))
    fan = [rv[0]] + [vert(p) for p in cap] + [lv[0]]
    for a, b in zip(fan, fan[1:]):
        bm.faces.new((hub, a, b))
    bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=1e-6)
    if dot:
        d = G * width * 1.12
        cz = G * -0.19 + dv
        ring = []
        for k in range(24):
            a = 2 * math.pi * k / 24
            ring.append(bm.verts.new((du + d / 2 * math.cos(a), y0, cz + d / 2 * math.sin(a))))
        bm.faces.new(ring)
    bm.normal_update()
    for f in bm.faces:
        if f.normal.y > 0:
            f.normal_flip()
    ob = mesh_object(name, bm)
    so = ob.modifiers.new("Solid", "SOLIDIFY")
    so.thickness = depth
    so.offset = 1
    bv = ob.modifiers.new("Bevel", "BEVEL")
    bv.width = min(0.012, depth * 0.4)
    bv.segments = 3
    bv.limit_method = "ANGLE"
    bv.angle_limit = math.radians(40)
    assign(ob, mat)
    apply_all(ob)
    return ob


def rivet(loc, normal, mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.028, location=(0, 0, 0))
    r = bpy.context.active_object
    r.scale = (1, 1, 0.55)
    apply_all(r)
    r.rotation_euler = Vector((0, 0, 1)).rotation_difference(Vector(normal)).to_euler()
    r.location = loc
    assign(r, mat)
    apply_all(r)
    return r


def build():
    gold = material("BlockGold", "#f6ae22", metallic=0.35, roughness=0.32)
    panel = material("BlockPanel", "#ec961a", metallic=0.3, roughness=0.4)
    glyph_mat = material("BlockGlyph", "#fff4d6", roughness=0.35)
    shadow = material("BlockGlyphShadow", "#8a3f0a", roughness=0.5)
    rivet_mat = material("BlockRivet", "#b4600f", metallic=0.55, roughness=0.3)

    parts = [block_body(gold, panel)]
    front = [glyph("Glyph", 0.078, 0.042, glyph_mat), glyph("GlyphShadow", 0.078, 0.022, shadow, 0.018, -0.018)]
    front_one = join(front, "GlyphFront")
    for k in range(1, 4):
        cp = front_one.copy()
        cp.data = front_one.data.copy()
        bpy.context.scene.collection.objects.link(cp)
        cp.rotation_euler = (0, 0, k * math.pi / 2)
        apply_all(cp)
        parts.append(cp)
    parts.append(front_one)

    off = S / 2 - EDGE_BEVEL - INSET / 2
    surf = S / 2 - 0.004
    for axis, sign in ((0, 1), (0, -1), (1, 1), (1, -1), (2, 1)):
        others = [i for i in range(3) if i != axis]
        for a in (-1, 1):
            for b in (-1, 1):
                p = [0, 0, 0]
                p[axis] = sign * surf
                p[others[0]] = a * off
                p[others[1]] = b * off
                n = [0, 0, 0]
                n[axis] = sign
                parts.append(rivet(tuple(p), tuple(n), rivet_mat))
    blk = join(parts, "MysteryBlock")
    shade_smooth(blk, 35)
    return blk


def animate(blk):
    scene = bpy.context.scene
    scene.render.fps = FPS
    scene.frame_start, scene.frame_end = 0, FRAMES
    bpy.context.preferences.edit.keyframe_new_interpolation_type = "BEZIER"
    blk.animation_data_create()
    blk.animation_data.action = bpy.data.actions.new("BumpHop")
    # frame: (lift, squash z, roll deg)
    keys = {0: (0.0, 1.0, 0), 15: (0.03, 1.0, 0), 30: (0.0, 1.0, 0), 36: (0.0, 0.85, 0),
            42: (0.2, 1.1, 0), 48: (0.28, 1.0, 0), 54: (0.2, 1.03, 0), 60: (0.0, 0.86, 0),
            65: (0.025, 1.05, 3), 70: (0.0, 0.97, -2), 76: (0.0, 1.01, 1), 82: (0.0, 1.0, 0),
            FRAMES: (0.0, 1.0, 0)}
    for fr, (lift, sz, roll) in keys.items():
        sxy = 1 / math.sqrt(sz)
        blk.scale = (sxy, sxy, sz)
        blk.location = (0, 0, lift - S / 2 * (1 - sz))
        blk.rotation_euler = (0, math.radians(roll), 0)
        blk.keyframe_insert("scale", frame=fr)
        blk.keyframe_insert("location", index=2, frame=fr)
        blk.keyframe_insert("rotation_euler", index=1, frame=fr)
    scene.frame_set(0)


reset()
blk = build()
animate(blk)
export_glb(os.path.join(OUT, f"{ID}.glb"), [blk], animations=True)
render_thumbnail(os.path.join(OUT, "thumbnail.png"), [blk], frame=0, view=(0.62, -1.0, 0.45), margin=1.1)
write_asset_json(OUT, ID, "Mystery Block", "object", f"{ID}.glb",
                 description="Golden riveted block with a raised question mark on every side; it bobs, then bumps up with a squash and stretch.",
                 tags=["mystery", "question", "block", "game", "retro", "pickup", "gaming"],
                 extra={"animation": {"name": "BumpHop", "duration": FRAMES / FPS, "loop": True}})
