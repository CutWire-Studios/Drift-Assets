import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from drift3d import *  # noqa: E402,F403

ID = "loot-gem"
OUT = os.path.join(REPO, "objects", ID)
FPS = 30
FRAMES = 120
N = 8
# (z, radius, angular offset in half-steps); radius 0 = pole
PROFILE = [(-0.58, 0, 0), (-0.3, 0.19, 0.5), (-0.08, 0.3, 0), (0.0, 0.32, 0.5), (0.08, 0.32, 0.5), (0.24, 0.25, 0),
           (0.36, 0.15, 0.5), (0.36, 0, 0)]


def faceted(name, scale, mat):
    bm = bmesh.new()
    rings = []
    for z, r, off in PROFILE:
        if r == 0:
            rings.append(([bm.verts.new((0, 0, z * scale))], off))
            continue
        rings.append(([bm.verts.new((r * scale * math.cos(2 * math.pi * (i + off) / N),
                                     r * scale * math.sin(2 * math.pi * (i + off) / N), z * scale))
                       for i in range(N)], off))
    for (a, oa), (b, ob) in zip(rings, rings[1:]):
        for i in range(N):
            j = (i + 1) % N
            if len(a) == 1:
                bm.faces.new((a[0], b[j], b[i]))
            elif len(b) == 1:
                bm.faces.new((a[i], a[j], b[0]))
            elif oa == ob:
                bm.faces.new((a[i], a[j], b[j], b[i]))
            elif ob > oa:
                bm.faces.new((a[i], a[j], b[i]))
                bm.faces.new((b[i], a[j], b[j]))
            else:
                bm.faces.new((b[i], b[j], a[i]))
                bm.faces.new((a[i], b[j], a[j]))
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    bm.normal_update()
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    assign(ob, mat)
    return ob


def build():
    core_mat = material("GemCore", "#f2c8ff", emission="#d67cff")
    gem_mat = material("GemCrystal", "#7a2cf0", metallic=0.1, roughness=0.08, alpha=0.5)

    outer_mat = material("GemOuter", "#c89bff", roughness=0.05, alpha=0.14)
    core = faceted("Core", 0.58, core_mat)
    crystal = faceted("Crystal", 1.0, gem_mat)
    outer = faceted("Outer", 1.12, outer_mat)
    gem = join([core, crystal, outer], "LootGem")
    lo, hi = world_bbox([gem])
    gem.location = -(lo + hi) / 2
    apply_all(gem)
    return gem


def animate(gem):
    scene = bpy.context.scene
    scene.render.fps = FPS
    scene.frame_start, scene.frame_end = 0, FRAMES
    prefs = bpy.context.preferences.edit
    gem.animation_data_create()
    gem.animation_data.action = bpy.data.actions.new("SpinFloat")
    prefs.keyframe_new_interpolation_type = "LINEAR"
    gem.rotation_euler = (0, 0, 0)
    gem.keyframe_insert("rotation_euler", index=2, frame=0)
    gem.rotation_euler = (0, 0, 2 * math.pi)
    gem.keyframe_insert("rotation_euler", index=2, frame=FRAMES)
    prefs.keyframe_new_interpolation_type = "BEZIER"
    q = FRAMES // 4
    for k in range(5):
        gem.location = (0, 0, -0.05 if k % 2 == 0 else 0.05)
        gem.keyframe_insert("location", index=2, frame=k * q)
    scene.frame_set(0)


reset()
gem = build()
animate(gem)
export_glb(os.path.join(OUT, f"{ID}.glb"), [gem], animations=True)
render_thumbnail(os.path.join(OUT, "thumbnail.png"), [gem], frame=0, view=(0.62, -1.0, 0.3), margin=1.05)
write_asset_json(OUT, ID, "Loot Gem", "object", f"{ID}.glb",
                 description="Faceted purple epic-rarity crystal with a glowing core inside a translucent shell, spinning and floating like a loot drop.",
                 tags=["gem", "crystal", "loot", "epic", "rarity", "game", "gaming", "pickup"],
                 extra={"animation": {"name": "SpinFloat", "duration": FRAMES / FPS, "loop": True}})
