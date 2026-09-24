import math
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from drift3d import *  # noqa: E402,F403

ID = "aviator-sunglasses"
OUT = os.path.join(REPO, "face-props", ID)

LENS_CX = 0.235
LENS_Y = -0.17
WRAP = 0.35  # y += WRAP * x^2 so the front bends around the face
# Right-eye lens outline, u = outward from the nose, v = up (head-widths).
LENS = [(-0.17, 0.108), (-0.06, 0.126), (0.06, 0.13), (0.16, 0.122), (0.2, 0.075), (0.207, -0.01),
        (0.185, -0.085), (0.13, -0.15), (0.04, -0.195), (-0.06, -0.212), (-0.135, -0.18),
        (-0.172, -0.1), (-0.185, 0.0), (-0.188, 0.07)]
RIM_R = 0.009


def wrap(x, z, dy=0.0):
    return Vector((x, LENS_Y + WRAP * x * x + dy, z))


def catmull(pts, closed, n=8):
    pts = [Vector(p) for p in pts]
    out = []
    m = len(pts)
    segs = m if closed else m - 1
    for i in range(segs):
        p0 = pts[(i - 1) % m] if closed or i > 0 else pts[0]
        p1, p2 = pts[i], pts[(i + 1) % m]
        p3 = pts[(i + 2) % m] if closed or i + 2 < m else pts[-1]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            out.append(0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    if not closed:
        out.append(pts[-1])
    return out


def link(name, bm, mat):
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(obj)
    assign(obj, mat)
    return obj


def tube(name, pts, radius, mat, closed=False, nr=10):
    bm = bmesh.new()
    n = len(pts)
    tans = []
    for i in range(n):
        a = pts[(i - 1) % n] if closed or i > 0 else pts[i]
        b = pts[(i + 1) % n] if closed or i < n - 1 else pts[i]
        tans.append((b - a).normalized())
    ref = Vector((0, 0, 1)) if abs(tans[0].z) < 0.9 else Vector((1, 0, 0))
    nrm = tans[0].cross(ref).normalized()
    rings = []
    for i in range(n):
        if i:
            nrm = (nrm - tans[i] * nrm.dot(tans[i])).normalized()
        bin_ = tans[i].cross(nrm)
        rings.append([bm.verts.new(pts[i] + (nrm * math.cos(2 * math.pi * k / nr)
                                             + bin_ * math.sin(2 * math.pi * k / nr)) * radius)
                      for k in range(nr)])
    for i in range(n if closed else n - 1):
        a, b = rings[i], rings[(i + 1) % n]
        for k in range(nr):
            bm.faces.new((a[k], a[(k + 1) % nr], b[(k + 1) % nr], b[k]))
    if not closed:
        for ring, end in ((rings[0], pts[0] - tans[0] * radius * 0.6),
                          (rings[-1], pts[-1] + tans[-1] * radius * 0.6)):
            c = bm.verts.new(end)
            for k in range(nr):
                bm.faces.new((ring[k], ring[(k + 1) % nr], c))
    return link(name, bm, mat)


def lens_outline(side):
    return [(side * (LENS_CX + u), v) for u, v in catmull(LENS, True, 10)]


def lens(side, mat):
    outline = lens_outline(side)
    cx = sum(p[0] for p in outline) / len(outline)
    cz = sum(p[1] for p in outline) / len(outline)
    bm = bmesh.new()
    rings = 6
    grid = []
    for r in range(rings + 1):
        s = r / rings
        row = []
        for x, z in outline:
            px, pz = cx + (x - cx) * s * 0.985, cz + (z - cz) * s * 0.985
            row.append(bm.verts.new(wrap(px, pz, -0.018 * (1 - s * s))))
        grid.append(row)
    n = len(outline)
    centre = bm.verts.new(wrap(cx, cz, -0.018))
    for k in range(n):
        bm.faces.new((centre, grid[1][k], grid[1][(k + 1) % n]))
    for r in range(1, rings):
        for k in range(n):
            bm.faces.new((grid[r][k], grid[r + 1][k], grid[r + 1][(k + 1) % n], grid[r][(k + 1) % n]))
    for v in grid[0]:
        bm.verts.remove(v)
    obj = link(f"Lens{side:+d}", bm, mat)
    sol = obj.modifiers.new("Solid", "SOLIDIFY")
    sol.thickness = 0.006
    sol.offset = 0
    apply_all(obj)
    return obj


def build():
    gold = material("AviatorGold", "#e8b84a", metallic=1.0, roughness=0.22)
    glass = material("AviatorLens", "#26303c", metallic=0.85, roughness=0.06)
    pad = material("AviatorPad", "#e9e4dc", roughness=0.3)
    tip = material("AviatorTip", "#1b1714", roughness=0.4)

    metal, lenses, pads, tips = [], [], [], []
    for side in (-1, 1):
        lenses.append(lens(side, glass))
        rim = [wrap(x, z, -0.004) for x, z in lens_outline(side)]
        metal.append(tube(f"Rim{side:+d}", rim, RIM_R, gold, closed=True))

        hinge = wrap(side * (LENS_CX + 0.2), 0.075, 0.005)
        bpy.ops.mesh.primitive_cube_add(size=1, location=hinge + Vector((side * 0.012, 0.012, 0)))
        h = bpy.context.active_object
        h.scale = (0.03, 0.035, 0.028)
        bev = h.modifiers.new("Bevel", "BEVEL")
        bev.width = 0.007
        bev.segments = 3
        assign(h, gold)
        apply_all(h)
        metal.append(h)

        s = side
        temple = catmull([hinge + Vector((s * 0.02, 0.02, 0)), Vector((s * 0.49, 0.05, 0.08)),
                          Vector((s * 0.52, 0.3, 0.1)), Vector((s * 0.525, 0.42, 0.105))], False, 10)
        metal.append(tube(f"Temple{s:+d}", temple, 0.0085, gold))
        curl = catmull([Vector((s * 0.525, 0.4, 0.105)), Vector((s * 0.525, 0.47, 0.095)),
                        Vector((s * 0.52, 0.53, 0.04)), Vector((s * 0.51, 0.56, -0.04)),
                        Vector((s * 0.5, 0.56, -0.1))], False, 10)
        tips.append(tube(f"Tip{s:+d}", curl, 0.012, tip))

        arm_start = wrap(s * 0.07, -0.02, 0.0)
        pad_pos = Vector((s * 0.058, -0.11, -0.09))
        arm = catmull([arm_start, arm_start + Vector((-s * 0.005, 0.03, -0.02)),
                       pad_pos + Vector((s * 0.01, -0.01, 0.02))], False, 8)
        metal.append(tube(f"PadArm{s:+d}", arm, 0.004, gold))
        bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=12, radius=1, location=pad_pos)
        p = bpy.context.active_object
        p.scale = (0.008, 0.02, 0.03)
        p.rotation_euler = (0, 0, math.radians(-s * 35))
        assign(p, pad)
        apply_all(p)
        pads.append(p)

    top = [wrap(-0.2, 0.128), wrap(-0.1, 0.136), wrap(0, 0.138), wrap(0.1, 0.136),
           wrap(0.2, 0.128)]
    metal.append(tube("BrowBar", catmull(top, False, 10), RIM_R, gold))
    bridge = [wrap(-0.055, 0.035), wrap(-0.03, 0.06), wrap(0, 0.068), wrap(0.03, 0.06),
              wrap(0.055, 0.035)]
    metal.append(tube("Bridge", catmull(bridge, False, 8), RIM_R * 0.9, gold))

    objs = [join(metal, "AviatorFrame"), join(lenses, "AviatorLenses"), join(pads, "AviatorPads"),
            join(tips, "AviatorTips")]
    for o in objs:
        apply_all(o)
        shade_smooth(o, 50)
    return objs


if __name__ == "__main__":
    reset()
    head = reference_head()
    props = build()
    os.makedirs(OUT, exist_ok=True)
    render_prop_thumbnail(os.path.join(OUT, "thumbnail.png"), props, head, region="face")
    if "--check" in args():
        render_thumbnail(os.path.join(OUT, "_check.png"), [head] + props, view=(0, -1, 0.05),
                         margin=1.05)
        render_thumbnail(os.path.join(OUT, "_check2.png"), [head] + props, view=(-1, 0, 0.05),
                         margin=1.05)
        render_thumbnail(os.path.join(OUT, "_check3.png"), props, view=(0, -1, 0.0), margin=0.8)
    bpy.data.objects.remove(head, do_unlink=True)
    export_glb(os.path.join(OUT, f"{ID}.glb"), props)
    write_prop_json(OUT, ID, "Aviator Sunglasses", props,
                    description="Classic gold wire-frame aviator sunglasses with dark mirrored "
                                "teardrop lenses, nose pads and temples.",
                    tags=["glasses", "sunglasses", "aviator", "gold", "cool", "pilot"])
