import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from drift3d import *  # noqa: E402,F403

ID = "heart"
OUT = os.path.join(REPO, "objects", ID)
FPS = 30
FRAMES = 48
DEPTH = 1.9  # smaller than the classic 9/4 = puffier


def f(x, y, z):
    return (x * x + DEPTH * y * y + z * z - 1) ** 3 - x * x * z ** 3 - 0.05 * y * y * z ** 3


def build():
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=6, radius=1)
    h = bpy.context.active_object
    h.name = "Heart"
    centre = Vector((0, 0, 0.1))
    for v in h.data.vertices:
        d = v.co.normalized()
        v.co = centre + d * radius_from(centre, d)
        v.co.z *= 1.1
    sm = h.modifiers.new("Smooth", "SMOOTH")
    sm.factor = 0.8
    sm.iterations = 6
    apply_all(h)
    shade_smooth(h, 180)
    assign(h, material("HeartRed", "#e8132f", metallic=0.0, roughness=0.18))
    lo, hi = world_bbox([h])
    c = (lo + hi) / 2
    s = 1.0 / max(hi - lo)
    for v in h.data.vertices:
        v.co = (v.co - c) * s
    return h


def radius_from(c, d):
    lo, hi = 0.0, 2.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if f(*(c + d * mid)) < 0:
            lo = mid
        else:
            hi = mid
    return lo


def bump(ph, c, k):
    return math.exp(k * (math.cos(2 * math.pi * (ph - c)) - 1))


def animate(obj):
    scene = bpy.context.scene
    scene.render.fps = FPS
    scene.frame_start, scene.frame_end = 0, FRAMES
    bpy.context.preferences.edit.keyframe_new_interpolation_type = "LINEAR"
    obj.animation_data_create()
    obj.animation_data.action = bpy.data.actions.new("Heartbeat")
    for fr in range(FRAMES + 1):
        ph = (fr % FRAMES) / FRAMES
        beat = 0.14 * bump(ph, 0.12, 40) + 0.09 * bump(ph, 0.34, 40)
        obj.scale = (1 + beat, 1 + beat * 0.8, 1 + beat)
        obj.rotation_euler = (0, math.radians(4) * math.sin(2 * math.pi * ph),
                              math.radians(7) * math.sin(2 * math.pi * ph + 0.6))
        obj.keyframe_insert("scale", frame=fr)
        obj.keyframe_insert("rotation_euler", frame=fr)


def build_pixel():
    """Voxel heart: the classic 7x6 pixel-art heart extruded into chunky cubes with bevelled edges."""
    rows = [".XX.XX.", "XXXXXXX", "XXXXXXX", ".XXXXX.", "..XXX..", "...X..."]
    red = material("PixelRed", "#e8132f", roughness=0.35)
    shine = material("PixelShine", "#ff8a98", roughness=0.3)
    cubes = []
    s = 1.0 / 7
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch != "X":
                continue
            bpy.ops.mesh.primitive_cube_add(size=s * 0.96, location=((c - 3) * s, 0, (2.5 - r) * s))
            cube = bpy.context.active_object
            bev = cube.modifiers.new("Bevel", "BEVEL")
            bev.width = s * 0.08
            bev.segments = 2
            assign(cube, shine if (r, c) in ((1, 1), (1, 2), (2, 1)) else red)
            cubes.append(cube)
    h = join(cubes, "PixelHeart")
    apply_all(h)
    return h


def animate_spin(obj, frames):
    """One full turn with a small bob; linear so the loop is seamless."""
    scene = bpy.context.scene
    scene.frame_start, scene.frame_end = 0, frames
    bpy.context.preferences.edit.keyframe_new_interpolation_type = "LINEAR"
    obj.animation_data_create()
    obj.animation_data.action = bpy.data.actions.new("Spin")
    for fr in range(frames + 1):
        ph = fr / frames
        obj.rotation_euler = (0, 0, 2 * math.pi * ph)
        obj.location = (0, 0, 0.04 * math.sin(2 * math.pi * ph))
        obj.keyframe_insert("rotation_euler", frame=fr)
        obj.keyframe_insert("location", frame=fr)


def make(opts):
    if opts["style"] == "classic":
        h = build()
        animate(h)
        return [h], "Heartbeat", FRAMES
    if opts["style"] == "chrome":
        h = build()
        assign(h, material("HeartChrome", "#ff8fa3", metallic=0.9, roughness=0.28))
        animate_spin(h, 72)
        return [h], "Spin", 72
    h = build_pixel()
    animate(h)
    return [h], "Heartbeat", FRAMES


build_object_variants(ID, "Heart", "Puffy heart for likes, love and Valentine's edits.",
                      ["heart", "love", "like", "valentine", "red"], [
    ("classic", "Glossy Heartbeat", {"style": "classic",
                                     "description": "Glossy puffy red heart with a double-pulse heartbeat and a gentle sway."}),
    ("chrome", "Rose Metal Spin", {"style": "chrome",
                               "description": "Rose-metal heart turning a full circle with a slight bob."}),
    ("pixel", "Pixel Heart", {"style": "pixel", "view": (0.45, -1.0, 0.25),
                              "description": "Chunky voxel pixel-art heart with a heartbeat pulse."}),
], build=make, view=(0.5, -1.0, 0.3), margin=1.1)
