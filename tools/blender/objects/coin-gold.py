import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from drift3d import *  # noqa: E402,F403

ID = "coin-gold"
OUT = os.path.join(REPO, "objects", ID)
FPS = 30
FRAMES = 60
SEG = 256
R = 0.5


def coin_body():
    """Coin revolved around Z (faces along Z), reeded edge, raised rim, recessed field."""
    half = 0.06
    prof = [(0, 0.036), (0.36, 0.036), (0.375, 0.038), (0.39, 0.05), (0.405, 0.058),
            (0.44, half), (0.47, half), (0.485, half - 0.006), (R, half - 0.018),
            (R, -(half - 0.018)), (0.485, -(half - 0.006)), (0.47, -half), (0.44, -half),
            (0.405, -0.058), (0.39, -0.05), (0.375, -0.038), (0.36, -0.036), (0, -0.036)]
    bm = bmesh.new()
    rings = []
    for idx, (r, z) in enumerate(prof):
        if r == 0:
            rings.append([bm.verts.new((0, 0, z))])
            continue
        reeded = r == R
        ring = []
        for i in range(SEG):
            a = 2 * math.pi * i / SEG
            rr = r - (0.005 if reeded and i % 2 else 0)
            ring.append(bm.verts.new((rr * math.cos(a), rr * math.sin(a), z)))
        rings.append(ring)
    for a, b in zip(rings, rings[1:]):
        for i in range(SEG):
            j = (i + 1) % SEG
            if len(a) == 1:
                bm.faces.new((a[0], b[i], b[j]))
            elif len(b) == 1:
                bm.faces.new((a[j], a[i], b[0]))
            else:
                bm.faces.new((a[j], a[i], b[i], b[j]))
    bm.normal_update()
    me = bpy.data.meshes.new("CoinBody")
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("CoinBody", me)
    bpy.context.scene.collection.objects.link(ob)
    return ob


def star(name, z0, height, sign, r_out=0.27, r_in=0.115):
    """Faceted 5-point star: short wall, then a pyramid rising to a centre point."""
    bm = bmesh.new()
    pts = []
    for k in range(10):
        a = math.pi / 2 + k * math.pi / 5
        r = r_out if k % 2 == 0 else r_in
        pts.append((r * math.cos(a), r * math.sin(a)))
    wall = height * 0.3
    bot = [bm.verts.new((x, y, z0 - sign * 0.004)) for x, y in pts]
    top = [bm.verts.new((x, y, z0 + sign * wall)) for x, y in pts]
    tip = bm.verts.new((0, 0, z0 + sign * height))
    for i in range(10):
        j = (i + 1) % 10
        f = (bot[i], bot[j], top[j], top[i])
        bm.faces.new(f if sign > 0 else f[::-1])
        f = (top[i], top[j], tip)
        bm.faces.new(f if sign > 0 else f[::-1])
    bm.normal_update()
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    return ob


def ring(name, r, width, z, h, sign):
    bm = bmesh.new()
    seg = 128
    prof = [(r - width / 2, 0), (r - width / 4, h), (r + width / 4, h), (r + width / 2, 0)]
    rings = [[bm.verts.new((pr * math.cos(2 * math.pi * i / seg), pr * math.sin(2 * math.pi * i / seg),
                            z + sign * ph)) for i in range(seg)] for pr, ph in prof]
    for a, b in zip(rings, rings[1:]):
        for i in range(seg):
            j = (i + 1) % seg
            f = (a[i], a[j], b[j], b[i])
            bm.faces.new(f if sign > 0 else f[::-1])
    bm.normal_update()
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    return ob


def build():
    gold = material("CoinGold", "#ffc53d", metallic=0.85, roughness=0.3)
    gold_field = material("CoinField", "#e8a52a", metallic=0.85, roughness=0.38)
    gold_bright = material("CoinStar", "#ffcf4a", metallic=0.85, roughness=0.22)

    body = coin_body()
    body.data.materials.append(gold)
    body.data.materials.append(gold_field)
    for p in body.data.polygons:
        c = p.center
        if math.hypot(c.x, c.y) < 0.37:
            p.material_index = 1
    parts = [body]
    for sign in (1, -1):
        s = star(f"Star{sign}", sign * 0.035, 0.04, sign)
        assign(s, gold_bright)
        rg = ring(f"Ring{sign}", 0.33, 0.014, sign * 0.035, 0.006, sign)
        assign(rg, gold_bright)
        parts += [s, rg]
    for o in parts:
        apply_all(o)
    coin = join(parts, "Coin")
    shade_smooth(coin, 30)
    coin.rotation_euler = (math.pi / 2, 0, 0)
    apply_all(coin)
    return coin


def animate(obj):
    scene = bpy.context.scene
    scene.render.fps = FPS
    scene.frame_start, scene.frame_end = 0, FRAMES
    bpy.context.preferences.edit.keyframe_new_interpolation_type = "LINEAR"
    obj.animation_data_create()
    obj.animation_data.action = bpy.data.actions.new("Spin")
    obj.rotation_euler = (0, 0, 0)
    obj.keyframe_insert("rotation_euler", index=2, frame=0)
    obj.rotation_euler = (0, 0, 2 * math.pi)
    obj.keyframe_insert("rotation_euler", index=2, frame=FRAMES)


reset()
coin = build()
animate(coin)
export_glb(os.path.join(OUT, f"{ID}.glb"), [coin], animations=True)
render_thumbnail(os.path.join(OUT, "thumbnail.png"), [coin], frame=0, view=(0.62, -1.0, 0.35))
write_asset_json(OUT, ID, "Gold Coin", "object", f"{ID}.glb",
                 description="Thick gold coin with a raised rim, embossed stars on both faces and a reeded edge, spinning fast.",
                 tags=["coin", "gold", "money", "reward", "currency", "spin"],
                 extra={"animation": {"name": "Spin", "duration": FRAMES / FPS, "loop": True}})
