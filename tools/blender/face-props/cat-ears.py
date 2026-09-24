import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from drift3d import *  # noqa: E402,F403

ID = "cat-ears"
OUT = os.path.join(REPO, "face-props", ID)

# Headband runs over the reference head in the plane y = BAND_Y.
BAND_Y = 0.32
BAND_ZC, BAND_GAP = -0.05, 0.012
EAR_PHI = math.radians(24)
EAR_W, EAR_H, CUP = 0.145, 0.33, 0.05


def ear_width(v, w):
    return w * (1 - v) ** 0.62 * (1 + 0.35 * v)


def ear_sheet(name, w, h, v0, y_off, nu=11, nv=15):
    """Grid in ear space (x across, z up); front follows the cupped outer-ear surface."""
    verts, faces = [], []
    for i in range(nv):
        v = v0 + (1 - v0) * i / (nv - 1)
        for j in range(nu):
            u = -1 + 2 * j / (nu - 1)
            x, z = u * ear_width(v, w), v * h - 0.03
            uo = x / max(ear_width(min(z / EAR_H, 0.999), EAR_W), 1e-4)
            y = CUP * (1 - min(uo * uo, 1)) * (1 - 0.65 * z / EAR_H) + y_off
            verts.append((x, y, z))
    for i in range(nv - 1):
        for j in range(nu - 1):
            a = i * nu + j
            faces.append((a, a + nu, a + nu + 1, a + 1))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    return ob


def thicken(ob, thickness, offset, levels=2):
    s = ob.modifiers.new("Solidify", "SOLIDIFY")
    s.thickness = thickness
    s.offset = offset
    s.use_even_offset = True
    d = ob.modifiers.new("Subsurf", "SUBSURF")
    d.levels = d.render_levels = levels
    apply_all(ob)
    return ob


def band_point(head, phi):
    """Headband centreline point and outward normal (in the band plane) on the reference skull."""
    d = Vector((math.sin(phi), 0, math.cos(phi)))
    c = Vector((0, BAND_Y, BAND_ZC))
    ok, hit, nrm, _ = head.ray_cast(c + d * 3, -d)
    n = Vector((nrm.x, 0, nrm.z)).normalized()
    return hit + n * BAND_GAP, n


def place_ear(obs, side, head):
    phi = EAR_PHI * side
    p, n = band_point(head, phi)
    beta = math.atan2(n.x, n.z)
    p = p - n * 0.025
    for ob in obs:
        ob.rotation_euler = (math.radians(-6), beta * 0.6, math.radians(-16) * side)
        ob.location = p
        apply_all(ob)


def headband(head):
    N, ring = 160, 20
    a0 = math.radians(105)
    pts = [band_point(head, -a0 + 2 * a0 * i / (N - 1))[0] for i in range(N)]
    for _ in range(6):
        pts = [pts[0]] + [(pts[i - 1] + 2 * pts[i] + pts[i + 1]) / 4 for i in range(1, N - 1)] + [pts[-1]]
    verts, faces = [], []
    for i, p in enumerate(pts):
        t = i / (N - 1)
        e = min(t, 1 - t) / 0.012
        k_end = math.sqrt(max(0.0, 1 - (1 - e) ** 2)) if e < 1 else 1.0
        tan = (pts[min(i + 1, N - 1)] - pts[max(i - 1, 0)]).normalized()
        nrm = Vector((0, 1, 0))
        bin_ = tan.cross(nrm)
        for k in range(ring):
            a = 2 * math.pi * k / ring
            verts.append(p + nrm * math.cos(a) * 0.024 * max(k_end, 0.15)
                         + bin_ * math.sin(a) * 0.011 * max(k_end, 0.15))
    for i in range(N - 1):
        for k in range(ring):
            a, b = i * ring + k, i * ring + (k + 1) % ring
            faces.append((a, b, b + ring, a + ring))
    verts += [tuple(pts[0]), tuple(pts[-1])]
    s0, s1 = len(verts) - 2, len(verts) - 1
    for k in range(ring):
        faces.append((s0, (k + 1) % ring, k))
        faces.append((s1, (N - 1) * ring + k, (N - 1) * ring + (k + 1) % ring))
    me = bpy.data.meshes.new("Headband")
    me.from_pydata([tuple(v) for v in verts], [], faces)
    ob = bpy.data.objects.new("Headband", me)
    bpy.context.scene.collection.objects.link(ob)
    return ob


reset()
head = reference_head()
fur = material("CatFur", "#2f2a35", roughness=0.8)
pink = material("CatInner", "#f59cb6", roughness=0.6)
band_mat = material("CatBand", "#25212a", roughness=0.35)

props = []
for side in (-1, 1):
    outer = thicken(ear_sheet(f"Ear{side}", EAR_W, EAR_H, 0.0, 0.0), 0.032, 1)
    inner = thicken(ear_sheet(f"EarInner{side}", EAR_W * 0.64, EAR_H * 0.74, 0.12, -0.004), 0.012, -1)
    place_ear([outer, inner], side, head)
    assign(outer, fur)
    assign(inner, pink)
    props += [outer, inner]
band = headband(head)
assign(band, band_mat)
props.append(band)
for ob in props:
    shade_smooth(ob, 180)

os.makedirs(OUT, exist_ok=True)
export_glb(os.path.join(OUT, f"{ID}.glb"), props)
write_prop_json(OUT, ID, "Cat Ears", props,
                description="Cat ears with pink inners on a thin headband.",
                tags=["cat", "ears", "kitty", "cute", "headband"])
render_prop_thumbnail(os.path.join(OUT, "thumbnail.png"), props, head, region="head")
if "--check" in args():
    render_thumbnail(os.path.join(OUT, "_check.png"), [head] + props, view=(0.0, -1.0, 0.0), margin=0.95)
