import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from drift3d import *  # noqa: E402,F403
from mathutils import Matrix  # noqa: E402

ID = "mustache"
OUT = os.path.join(REPO, "face-props", ID)

# Right half in the front plane (x, z), from the philtrum out to the curled tip.
HALF = [(0.0, -0.49), (0.05, -0.497), (0.1, -0.52), (0.15, -0.535), (0.195, -0.525), (0.228, -0.497),
        (0.238, -0.463), (0.225, -0.437), (0.202, -0.433), (0.19, -0.447), (0.197, -0.459)]


def catmull(pts, steps):
    pts = [pts[0]] + pts + [pts[-1]]
    out = []
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = (Vector(p) for p in pts[i - 1:i + 3])
        for k in range(steps):
            t = k / steps
            out.append(0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(Vector(pts[-2]))
    return out


SURFACE_GAP = 0.024  # centreline sits this far in front of the muzzle surface


def seat(path2d, head):
    """Depth per sample from the reference head's muzzle, smoothed so the curls wrap gently."""
    ys = []
    for p in path2d:
        ok, loc, _, _ = head.ray_cast(Vector((p.x, -2, p.y)), Vector((0, 1, 0)))
        ys.append(loc.y - SURFACE_GAP)
    for _ in range(12):
        ys = [ys[0]] + [(ys[i - 1] + 2 * ys[i] + ys[i + 1]) / 4 for i in range(1, len(ys) - 1)] + [ys[-1]]
    return ys


def build(head):
    half = catmull(HALF, 14)
    # arc length fraction per sample
    L = [0.0]
    for a, b in zip(half, half[1:]):
        L.append(L[-1] + (b - a).length)
    u_half = [v / L[-1] for v in L]
    path2d = [Vector((-p.x, p.y)) for p in reversed(half[1:])] + half
    us = list(reversed(u_half[1:])) + u_half
    pts = [Vector((p.x, y, p.y)) for p, y in zip(path2d, seat(path2d, head))]

    def r_of(u):
        grow = min(1.0, u / 0.22)
        grow = grow * grow * (3 - 2 * grow)
        return (0.032 + 0.024 * grow) * (1 - u) ** 0.75

    ring = 36
    verts, faces = [], []
    n = len(pts)
    for i in range(1, n - 1):
        tan = (pts[i + 1] - pts[i - 1]).normalized()
        hint = Vector((0, 1, 0))
        nrm = (hint - tan * hint.dot(tan)).normalized()
        bin_ = tan.cross(nrm)
        r = r_of(us[i])
        for k in range(ring):
            a = 2 * math.pi * k / ring
            ca, sa = math.cos(a), math.sin(a)
            rr = r * (1 + 0.035 * math.cos(9 * a))
            dn = 0.62 * rr * ca * (0.8 if ca > 0 else 1.0)  # flatter against the lip
            verts.append(pts[i] + nrm * dn + bin_ * rr * sa)
    m = n - 2
    for i in range(m - 1):
        for k in range(ring):
            a, b = i * ring + k, i * ring + (k + 1) % ring
            faces.append((a, b, b + ring, a + ring))
    verts.append(pts[0])
    s0 = len(verts) - 1
    verts.append(pts[-1])
    s1 = len(verts) - 1
    for k in range(ring):
        faces.append((s0, (k + 1) % ring, k))
        faces.append((s1, (m - 1) * ring + k, (m - 1) * ring + (k + 1) % ring))
    me = bpy.data.meshes.new("Mustache")
    me.from_pydata([tuple(v) for v in verts], [], faces)
    me.update()
    ob = bpy.data.objects.new("Mustache", me)
    bpy.context.scene.collection.objects.link(ob)
    return ob


reset()
head = reference_head()
mus = build(head)
# The mannequin's muzzle sits lower and further back than a tracked upper lip, so the final
# placement is the one tuned on real footage (Drift params scale 0.4, offsetY -0.31, offsetZ 0.1):
# 0.4 head-widths wide, centred just under the nose and in front of the eye plane.
FIT_WIDTH, FIT_CENTRE = 0.4, Vector((0.0, -0.1, -0.31))
lo, hi = world_bbox([mus])
k = FIT_WIDTH / (hi - lo).x
mus.data.transform(Matrix.Translation(FIT_CENTRE) @ Matrix.Scale(k, 4) @ Matrix.Translation(-(lo + hi) / 2))
shade_smooth(mus, 180)
assign(mus, material("MustacheBlack", "#110e0c", roughness=0.42))

props = [mus]
os.makedirs(OUT, exist_ok=True)
export_glb(os.path.join(OUT, f"{ID}.glb"), props)
write_prop_json(OUT, ID, "Handlebar Mustache", props,
                description="Black handlebar mustache with curled tips, sitting on the upper lip.",
                tags=["mustache", "moustache", "handlebar", "gentleman", "funny"])
bpy.ops.mesh.primitive_cube_add(size=1, location=(0.06, 0.05, -0.2))
frame = bpy.context.active_object
frame.scale = (0.75, 0.5, 0.8)
frame.hide_render = True
render_prop_thumbnail(os.path.join(OUT, "thumbnail.png"), props, head, region="face")
if "--check" in args():
    render_thumbnail(os.path.join(OUT, "_check.png"), [frame], view=(0.0, -1.0, 0.0), margin=0.85)
