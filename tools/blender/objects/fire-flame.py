import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from drift3d import *  # noqa: E402,F403

ID = "fire-flame"
OUT = os.path.join(REPO, "objects", ID)
FPS = 30
FRAMES = 60
TAU = 2 * math.pi


def teardrop(bm, R, H, depth, wave, phase, tilt=0.0, offset=(0, 0, 0), rings=40, seg=40, m=1.3):
    """Teardrop with a round bottom (z=0) and a pointed, wavy tip (z=H). Adds geometry to bm."""
    ox, oy, oz = offset
    ct, st = math.cos(tilt), math.sin(tilt)
    verts = []
    for k in range(rings + 1):
        t = math.pi * k / rings
        z = H * (1 + math.cos(t)) / 2
        u = z / H
        r = R * math.sin(t) * math.sin(t / 2) ** m
        bend = wave * u ** 2.2 * math.sin(TAU * 0.9 * u + phase)
        ring = []
        for i in range(seg if 0 < k < rings else 1):
            a = TAU * i / seg
            x = r * math.cos(a) + bend
            y = depth * r * math.sin(a)
            xr, zr = x * ct + z * st, -x * st + z * ct
            ring.append(bm.verts.new((xr + ox, y + oy, zr + oz)))
        verts.append(ring)
    for a, b in zip(verts, verts[1:]):
        n = max(len(a), len(b))
        for i in range(n):
            j = (i + 1) % n
            if len(a) == 1:
                bm.faces.new((a[0], b[j], b[i]))
            elif len(b) == 1:
                bm.faces.new((a[i], a[j], b[0]))
            else:
                bm.faces.new((a[i], a[j], b[j], b[i]))


def layer(name, mat, lobes, base_z, y):
    bm = bmesh.new()
    for lobe in lobes:
        teardrop(bm, **lobe)
    bm.normal_update()
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = (0, y, base_z)
    shade_smooth(ob, 180)
    assign(ob, mat)
    return ob


def flame_mat(name, hex_):
    return material(name, hex_, roughness=0.45, emission=hex_, emission_strength=0.75)


def build():
    outer = layer("FlameOuter", flame_mat("FlameOrange", "#ff5a14"), [
        dict(R=0.46, H=1.0, depth=0.7, wave=0.12, phase=0.3),
        dict(R=0.24, H=0.62, depth=0.6, wave=-0.06, phase=0.0, tilt=math.radians(-32), offset=(-0.13, 0, 0.1)),
        dict(R=0.22, H=0.5, depth=0.6, wave=0.05, phase=1.0, tilt=math.radians(34), offset=(0.14, 0, 0.1)),
    ], 0.0, 0.0)
    mid = layer("FlameMid", flame_mat("FlameYellow", "#ffae1a"), [
        dict(R=0.33, H=0.74, depth=0.6, wave=-0.08, phase=0.8),
        dict(R=0.16, H=0.42, depth=0.55, wave=0.04, phase=0.0, tilt=math.radians(28), offset=(0.08, 0, 0.08)),
    ], 0.02, -0.12)
    inner = layer("FlameInner", flame_mat("FlameCore", "#fff3b0"), [
        dict(R=0.2, H=0.46, depth=0.55, wave=0.05, phase=0.2),
    ], 0.04, -0.22)
    layers = [outer, mid, inner]
    lo, hi = world_bbox(layers)
    c = (lo + hi) / 2
    for o in layers:
        o.location -= c
    return layers


def animate(layers):
    scene = bpy.context.scene
    scene.render.fps = FPS
    scene.frame_start, scene.frame_end = 0, FRAMES
    bpy.context.preferences.edit.keyframe_new_interpolation_type = "LINEAR"
    act = bpy.data.actions.new("Flicker")
    params = [  # (harmonics for height flicker, sway amplitude deg, phase)
        ((2, 0.06, 3, 0.04), 4.0, 0.0),
        ((3, 0.07, 5, 0.04), 6.0, 1.7),
        ((4, 0.08, 5, 0.05), 8.0, 3.1),
    ]
    for ob, ((h1, a1, h2, a2), sway, p) in zip(layers, params):
        ob.animation_data_create()
        ob.animation_data.action = act
        for fr in range(FRAMES + 1):
            ph = (fr % FRAMES) / FRAMES
            s = a1 * math.sin(TAU * h1 * ph + p) + a2 * math.sin(TAU * h2 * ph + 2 * p)
            w = 0.03 * math.sin(TAU * 3 * ph + p + 1.0)
            ob.scale = (1 - 0.45 * s + w, 1 - 0.3 * s, 1 + s)
            ob.rotation_euler = (0, math.radians(sway) * (0.7 * math.sin(TAU * ph + p)
                                                          + 0.3 * math.sin(TAU * 2 * ph + 2 * p)), 0)
            ob.keyframe_insert("scale", frame=fr)
            ob.keyframe_insert("rotation_euler", index=1, frame=fr)


reset()
layers = build()
animate(layers)
export_glb(os.path.join(OUT, f"{ID}.glb"), layers, animations=True)
render_thumbnail(os.path.join(OUT, "thumbnail.png"), layers, frame=0, view=(0.45, -1.0, 0.3), margin=1.1)
write_asset_json(OUT, ID, "Fire Flame", "object", f"{ID}.glb",
                 description="Stylised layered flame (orange, yellow and a hot core) that wobbles and flickers.",
                 tags=["fire", "flame", "hot", "lit", "burn", "trending"],
                 extra={"animation": {"name": "Flicker", "duration": FRAMES / FPS, "loop": True}})
