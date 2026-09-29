"""Render animated-preview frames for the 3D assets from their exported .glb files.

    flatpak run org.blender.Blender -b --factory-startup --python-exit-code 1 \
        --python "$PWD/tools/blender/render-previews.py" -- OUT_DIR [ID ...]

Writes OUT_DIR/<id>/0000.png... at PREVIEW_SIZE; tools/build-previews.py encodes them. The .glb is
re-imported rather than rebuilt, so previews never change the shipped models. Objects play their
loop animation; face props turn the mannequin's head from side to side. Framing (view, margin,
face/head region) is read from each asset's build script so it matches the still thumbnail.
"""

import glob
import json
import math
import os
import re
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drift3d import REPO, args, reference_head, render_prop_thumbnail, render_thumbnail, reset  # noqa: E402

PREVIEW_SIZE = 256
FPS = 20
PROP_SECONDS = 3.0
PROP_YAW = math.radians(35)


def script_source(kind, asset_id):
    with open(os.path.join(REPO, "tools", "blender", kind, f"{asset_id}.py")) as f:
        return f.read()


def floats(text):
    return tuple(float(v) for v in text.split(","))


def import_glb(path):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    return [o for o in bpy.data.objects if o not in before and o.type == "MESH"]


def render_object(asset_dir, out):
    meta = json.load(open(os.path.join(asset_dir, "asset.json")))
    src = script_source("objects", meta["id"])
    call = re.search(r"render_thumbnail\((.*?)\)\n", src, re.S).group(1)
    view = re.search(r"view=\(([^)]*)\)", call)
    margin = re.search(r"margin=([\d.]+)", call)
    frame = re.search(r"frame=(\d+)", call)

    reset()
    bpy.context.scene.render.fps = 30
    targets = import_glb(os.path.join(asset_dir, meta["file"]))
    view = floats(view.group(1)) if view else (0.0, -1.0, 0.25)
    source_frames = round(meta["animation"]["duration"] * 30)
    count = round(meta["animation"]["duration"] * FPS)
    shots = [(os.path.join(out, f"{i:04d}.png"), round(i * source_frames / count), view) for i in range(count)]
    render_thumbnail(shots[0][0], targets, frame=int(frame.group(1)) if frame else 0, view=view,
                     margin=float(margin.group(1)) if margin else 1.25, shots=shots, size=PREVIEW_SIZE)


def render_prop(asset_dir, out):
    meta = json.load(open(os.path.join(asset_dir, "prop.json")))
    region = "face" if 'region="face"' in script_source("face-props", meta["id"]) else "head"

    reset()
    props = import_glb(os.path.join(asset_dir, meta["model"]))
    head = reference_head()
    count = round(PROP_SECONDS * FPS)
    shots = []
    for i in range(count):
        # Starts and ends at the thumbnail's three-quarter angle so the loop has no seam.
        a = math.atan2(-0.45, 1.0) + PROP_YAW * math.sin(2 * math.pi * i / count)
        shots.append((os.path.join(out, f"{i:04d}.png"), None, (math.sin(a), -math.cos(a), 0.15)))
    render_prop_thumbnail(shots[0][0], props, head, region=region, shots=shots, size=PREVIEW_SIZE)


def main():
    a = args()
    out_root, only = a[0], set(a[1:])
    for kind, render in (("objects", render_object), ("face-props", render_prop)):
        for asset_dir in sorted(glob.glob(os.path.join(REPO, kind, "*"))):
            asset_id = os.path.basename(asset_dir)
            if only and asset_id not in only:
                continue
            if re.search(r"build_(object|prop)_variants\(", script_source(kind, asset_id)):
                continue  # the variant builders render their own previews
            out = os.path.join(out_root, asset_id)
            os.makedirs(out, exist_ok=True)
            render(asset_dir, out)


main()
