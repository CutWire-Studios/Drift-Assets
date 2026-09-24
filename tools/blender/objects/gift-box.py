import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from drift3d import *  # noqa: E402,F403

ID = "gift-box"
OUT = os.path.join(REPO, "objects", ID)
FPS = 30
FRAMES = 90
BOX_W, BOX_H = 0.66, 0.46
LID_W, LID_H = 0.72, 0.13
RIB = 0.12
TAU = 2 * math.pi


def rounded_box(name, size, loc, bevel, mat, segs=3):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = size
    bpy.ops.object.transform_apply(scale=True)
    mod = ob.modifiers.new("Bevel", "BEVEL")
    mod.width = bevel
    mod.segments = segs
    assign(ob, mat)
    apply_all(ob)
    return ob


def strip_object(name, rows, thickness, mat):
    """Ribbon strip through (left, right) point pairs, thickened and softened."""
    bm = bmesh.new()
    vs = [(bm.verts.new(a), bm.verts.new(b)) for a, b in rows]
    for (a0, b0), (a1, b1) in zip(vs, vs[1:]):
        bm.faces.new((a0, b0, b1, a1))
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    so = ob.modifiers.new("Solidify", "SOLIDIFY")
    so.thickness = thickness
    so.offset = 0
    sub = ob.modifiers.new("Sub", "SUBSURF")
    sub.levels = 1
    assign(ob, mat)
    apply_all(ob)
    return ob


def bow_loop(name, side, mat):
    """Ribbon loop in the XZ plane leaving the knot and curling back to it; width along Y."""
    rows = []
    n = 48
    for k in range(n + 1):
        a = TAU * k / n
        x = 0.16 * (1 - math.cos(a)) * side
        z = 0.1 * math.sin(a)
        xr, zr = x, z + 0.45 * abs(x)
        w = 0.17 * (0.4 + 0.6 * math.sin(a / 2) ** 0.6) / 2
        rows.append(((xr, -w, zr + 0.06), (xr, w, zr + 0.06)))
    return strip_object(name, rows, 0.018, mat)


def tail(name, angle, mat):
    rows = []
    n = 10
    L = 0.3
    dx, dy = math.sin(angle), -math.cos(angle)
    px, py = math.cos(angle), math.sin(angle)
    for k in range(n + 1):
        t = k / n
        cx, cy = dx * L * t, dy * L * t
        cz = 0.012 + 0.03 * math.sin(math.pi * t) * 0.6
        w = RIB * 0.42
        cut = 0.06 if k == n else 0
        rows.append(((cx - px * w - dx * cut, cy - py * w - dy * cut, cz),
                     (cx + px * w, cy + py * w, cz)))
    return strip_object(name, rows, 0.012, mat)



def build():
    red = material("GiftRed", "#d8203a", roughness=0.4)
    red_dark = material("GiftRedDeep", "#b3152c", roughness=0.4)
    gold = material("GiftRibbon", "#ffc23a", metallic=0.6, roughness=0.28)

    body = [rounded_box("Body", (BOX_W, BOX_W, BOX_H), (0, 0, BOX_H / 2), 0.02, red_dark),
            rounded_box("BandX", (BOX_W + 0.012, RIB, BOX_H - 0.004), (0, 0, BOX_H / 2), 0.006, gold, 2),
            rounded_box("BandY", (RIB, BOX_W + 0.012, BOX_H - 0.004), (0, 0, BOX_H / 2), 0.006, gold, 2)]
    box = join(body, "GiftBox")

    lid_parts = [rounded_box("Lid", (LID_W, LID_W, LID_H), (0, 0, LID_H / 2), 0.025, red),
                 rounded_box("LidBandX", (LID_W + 0.012, RIB, LID_H + 0.01), (0, 0, LID_H / 2), 0.008, gold, 2),
                 rounded_box("LidBandY", (RIB, LID_W + 0.012, LID_H + 0.01), (0, 0, LID_H / 2), 0.008, gold, 2)]
    bow = []
    for side in (-1, 1):
        lp = bow_loop(f"Loop{side}", side, gold)
        lp.location.z = LID_H
        apply_all(lp)
        bow.append(lp)
    for ang in (math.radians(-28), math.radians(32)):
        t = tail(f"Tail{ang:.2f}", ang, gold)
        t.location.z = LID_H
        apply_all(t)
        bow.append(t)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.055, location=(0, 0, LID_H + 0.06))
    knot = bpy.context.active_object
    knot.scale = (1.0, 1.15, 0.85)
    assign(knot, gold)
    apply_all(knot)
    lid = join(lid_parts + bow + [knot], "GiftLid")
    shade_smooth(box, 35)
    shade_smooth(lid, 35)

    lid.parent = box
    lid.location = (0, 0, BOX_H - 0.04)
    bpy.context.view_layer.update()
    lo, hi = world_bbox([box, lid])
    c = (lo + hi) / 2
    box.location = (-c.x, -c.y, -c.z)
    return box, lid


def animate(box, lid):
    scene = bpy.context.scene
    scene.render.fps = FPS
    scene.frame_start, scene.frame_end = 0, FRAMES
    bpy.context.preferences.edit.keyframe_new_interpolation_type = "BEZIER"
    act = bpy.data.actions.new("Hop")
    for o in (box, lid):
        o.animation_data_create()
        o.animation_data.action = act
    base_box = box.location.copy()
    base_lid = lid.location.copy()
    # frame: (box squash z, box rock deg), (lid lift, lid squash z, lid tilt deg)
    keys = {
        0: ((1.0, 0), (0.0, 1.0, 0)),
        8: ((0.92, 0), (0.0, 1.0, 0)),
        15: ((1.05, 0), (0.12, 1.1, 3)),
        23: ((1.0, 0), (0.2, 1.03, -2)),
        31: ((1.0, 0), (0.0, 1.0, 0)),
        34: ((0.94, 0), (0.0, 0.82, 0)),
        39: ((1.03, 6), (0.0, 1.06, 0)),
        45: ((0.99, -5), (0.0, 0.97, 0)),
        51: ((1.0, 3.5), (0.0, 1.0, 0)),
        57: ((1.0, -2), (0.0, 1.0, 0)),
        63: ((1.0, 0.8), (0.0, 1.0, 0)),
        69: ((1.0, 0), (0.0, 1.0, 0)),
        FRAMES: ((1.0, 0), (0.0, 1.0, 0)),
    }
    for fr, ((bsz, rock), (lift, lsz, tilt)) in keys.items():
        bxy = 1 / math.sqrt(bsz)
        box.scale = (bxy, bxy, bsz)
        box.rotation_euler = (0, math.radians(rock), 0)
        box.location = base_box
        lxy = 1 / math.sqrt(lsz)
        lid.scale = (lxy, lxy, lsz)
        lid.rotation_euler = (0, math.radians(tilt), 0)
        lid.location = base_lid + Vector((0, 0, lift))
        box.keyframe_insert("scale", frame=fr)
        box.keyframe_insert("rotation_euler", index=1, frame=fr)
        lid.keyframe_insert("scale", frame=fr)
        lid.keyframe_insert("rotation_euler", index=1, frame=fr)
        lid.keyframe_insert("location", index=2, frame=fr)
    scene.frame_set(0)


reset()
box, lid = build()
animate(box, lid)
export_glb(os.path.join(OUT, f"{ID}.glb"), [box, lid], animations=True)
render_thumbnail(os.path.join(OUT, "thumbnail.png"), [box, lid], frame=0, view=(0.6, -1.0, 0.55), margin=1.1)
write_asset_json(OUT, ID, "Gift Box", "object", f"{ID}.glb",
                 description="Red gift box with a gold ribbon and bow; the lid hops up and settles while the box wiggles.",
                 tags=["gift", "present", "box", "birthday", "surprise", "giveaway"],
                 extra={"animation": {"name": "Hop", "duration": FRAMES / FPS, "loop": True}})
