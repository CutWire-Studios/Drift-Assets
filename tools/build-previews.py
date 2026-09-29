"""Build the animated previews Drift's marketplace plays on hover.

    .venv/bin/python tools/build-previews.py [--skip-3d] [ID ...]

Per asset this writes, next to thumbnail.png:
  preview.webp  looping animated WebP. Lottie at the canvas aspect (1:1..4:1) and PREVIEW_HEIGHT
                tall; 3D assets square. Objects play their loop, face props turn the head.
  poster.png    Lottie only: a still at the preview's size, shown before the preview plays.

Frames are staged under .preview-frames/ (gitignored). Needs ffmpeg with libwebp_anim, the
skottie-render build (see CONTRIBUTING.md) and, unless --skip-3d, Blender (the flatpak, or the
binary named by $DRIFT_BLENDER). Lottie variants listed in asset.json get preview--<v>.webp and
poster--<v>.png. 3D assets built with drift3d's variant builders render their own previews in their
build script, so they are skipped here.
"""

import glob
import json
import os
import shutil
import subprocess
import sys

from PIL import Image

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
STAGE = os.path.join(REPO, ".preview-frames")
SKOTTIE = os.environ.get("DRIFT_SKOTTIE") or os.path.join(REPO, "tools", "skottie-render", "build", "skottie-render")
BLENDER = [os.environ["DRIFT_BLENDER"]] if os.environ.get("DRIFT_BLENDER") else ["flatpak", "run", "org.blender.Blender"]
PREVIEW_HEIGHT = 180
LOTTIE_FPS = 20
QUALITY = 75


def encode(frames_dir, out, fps):
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", str(fps),
                    "-i", os.path.join(frames_dir, "%04d.png"),
                    "-c:v", "libwebp_anim", "-q:v", str(QUALITY), "-loop", "0", out], check=True)


def thumbnail_background(asset_dir, thumbnail="thumbnail.png"):
    """The thumbnail's backdrop, so a preview sits on the same colour as its still."""
    r, g, b, *_ = Image.open(os.path.join(asset_dir, thumbnail)).convert("RGB").getpixel((1, 1))
    return f"{r:02x}{g:02x}{b:02x}"


def build_lottie(asset_dir):
    meta = json.load(open(os.path.join(asset_dir, "asset.json")))
    script = os.path.join(REPO, "tools", "lottie", meta["category"], f"{meta['id']}.py")
    if "variants" in meta and os.path.exists(script):
        # drift_lottie generators render their own previews with the right backdrop and poster time.
        subprocess.run([sys.executable, script], check=True, stdout=subprocess.DEVNULL)
        return
    variants = meta.get("variants") or [{"id": "default", "file": meta["file"], "thumbnail": "thumbnail.png",
                                         "preview": "preview.webp", "poster": "poster.png"}]
    for v in variants:
        frames = os.path.join(STAGE, f"{meta['id']}--{v['id']}")
        shutil.rmtree(frames, ignore_errors=True)
        os.makedirs(frames)
        # The poster is the moment the asset is fully on screen: the end of an intro, otherwise mid-way.
        # Transitions are a solid colour mid-way, so theirs is part-way through the cover-in.
        poster_t = "0.95" if v.get("playback", meta.get("playback")) == "intro-hold" else "0.5"
        if meta.get("category") == "transitions":
            poster_t = "0.2"
        subprocess.run([SKOTTIE, os.path.join(asset_dir, v["file"]), os.path.join(asset_dir, v["poster"]),
                        "--frames", frames, "--height", str(PREVIEW_HEIGHT), "--fps", str(LOTTIE_FPS),
                        "--t", poster_t, "--bg", thumbnail_background(asset_dir, v["thumbnail"]), "--strict"],
                       check=True, stdout=subprocess.DEVNULL)
        encode(frames, os.path.join(asset_dir, v["preview"]), LOTTIE_FPS)


def build_3d(ids):
    script = os.path.join(REPO, "tools", "blender", "render-previews.py")
    subprocess.run([*BLENDER, "-b", "--factory-startup", "--python-exit-code", "1",
                    "--python", script, "--", STAGE, *ids], check=True, stdout=subprocess.DEVNULL)
    for kind in ("objects", "face-props"):
        for asset_dir in sorted(glob.glob(os.path.join(REPO, kind, "*"))):
            frames = os.path.join(STAGE, os.path.basename(asset_dir))
            if (not ids or os.path.basename(asset_dir) in ids) and os.path.isdir(frames):
                encode(frames, os.path.join(asset_dir, "preview.webp"), 20)


def main():
    argv = sys.argv[1:]
    skip_3d = "--skip-3d" in argv
    ids = [a for a in argv if not a.startswith("--")]
    os.makedirs(STAGE, exist_ok=True)

    for asset_dir in sorted(glob.glob(os.path.join(REPO, "lottie", "*", "*"))):
        if not ids or os.path.basename(asset_dir) in ids:
            build_lottie(asset_dir)
            print("preview", os.path.relpath(asset_dir, REPO))

    three_d = [i for i in ids if glob.glob(os.path.join(REPO, "objects", i)) + glob.glob(os.path.join(REPO, "face-props", i))]
    if not skip_3d and (not ids or three_d):
        build_3d(three_d)
        print("previews for 3D assets")


main()
