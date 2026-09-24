import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from drift3d import *  # noqa: E402,F403

ID = "devil-horns"
OUT = os.path.join(REPO, "face-props", ID)


ROOT_Y = 0.2


def bezier(p0, p1, p2, p3, t):
    u = 1 - t
    return u ** 3 * p0 + 3 * u * u * t * p1 + 3 * u * t * t * p2 + t ** 3 * p3


def sweep(name, pts, radius, ring=32, hint=Vector((0, 1, 0)), lobe=None):
    """Tube along pts; radius(i, t, theta) -> r. Closed base cap, pointed tip."""
    n = len(pts)
    verts, faces = [], []
    for i, p in enumerate(pts):
        t = i / (n - 1)
        tan = (pts[min(i + 1, n - 1)] - pts[max(i - 1, 0)]).normalized()
        nrm = (hint - tan * hint.dot(tan)).normalized()
        bin_ = tan.cross(nrm)
        for k in range(ring):
            a = 2 * math.pi * k / ring
            r = radius(i, t, a)
            verts.append(p + (nrm * math.cos(a) + bin_ * math.sin(a)) * r)
    for i in range(n - 1):
        for k in range(ring):
            a, b = i * ring + k, i * ring + (k + 1) % ring
            faces.append((a, b, b + ring, a + ring))
    verts.append(pts[0] - (pts[1] - pts[0]).normalized() * 0.0)
    c0 = len(verts) - 1
    for k in range(ring):
        faces.append((c0, (k + 1) % ring, k))
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v) for v in verts], [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    return ob


def horn(side, head):
    s = side
    # Root the horn just under the skull surface at the top-front of the head.
    ok, hit, _, _ = head.ray_cast(Vector((0.2 * s, ROOT_Y, 3)), Vector((0, 0, -1)))
    delta = Vector((0.2 * s, ROOT_Y, hit.z - 0.074)) - Vector((0.2 * s, 0.33, 0.44))
    p0 = Vector((0.2 * s, 0.33, 0.44)) + delta
    p1 = Vector((0.31 * s, 0.27, 0.56)) + delta
    p2 = Vector((0.37 * s, 0.2, 0.82)) + delta
    p3 = Vector((0.21 * s, 0.17, 0.87)) + delta
    N = 90
    pts = [bezier(p0, p1, p2, p3, (i / (N - 1)) ** 0.9) for i in range(N)]
    base_r = 0.088

    def radius(i, t, a):
        taper = (1 - t) ** 0.85
        tip = math.sqrt(max(0.0, 1 - ((t - 1) / 0.035) ** 2)) * 0.006 if t > 0.965 else 0.0
        ridge = 1 + 0.07 * math.cos(6 * a + s * t * 9.0)
        return max(base_r * taper * ridge, tip, 0.0015 if i < N - 1 else 0.0)

    ob = sweep(f"Horn{'R' if s > 0 else 'L'}", pts, radius, ring=40, hint=Vector((-s, 1, 0)))
    return ob


reset()
head = reference_head()
red = material("DevilRed", "#d4101c", roughness=0.18)
horns = []
for s in (-1, 1):
    h = horn(s, head)
    shade_smooth(h, 180)
    assign(h, red)
    horns.append(h)

props = horns
os.makedirs(OUT, exist_ok=True)
export_glb(os.path.join(OUT, f"{ID}.glb"), props)
write_prop_json(OUT, ID, "Devil Horns", props,
                description="Glossy red curved devil horns rising from the top of the forehead.",
                tags=["devil", "horns", "halloween", "demon", "red"])
render_prop_thumbnail(os.path.join(OUT, "thumbnail.png"), props, head, region="head")
if "--check" in args():
    render_thumbnail(os.path.join(OUT, "_check.png"), [head] + props, view=(0.0, -1.0, 0.0), margin=1.0)
