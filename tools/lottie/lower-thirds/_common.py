"""Shared helpers for the lower-thirds generators."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools" / "lottie"))

from lottie_kit import *  # noqa: E402,F401,F403
from lottie_kit import HOLD, SNAP_OUT, Anim  # noqa: E402

CATEGORY = "lower-thirds"
RENDER = ROOT / "tools" / "skottie-render" / "build" / "skottie-render"
SCRATCH = Path("/tmp/claude-1000/lt")

FPS = 30
FRAMES = 150
OUTRO = 120  # outro marker start; runs to FRAMES

EXPO_OUT = (0.16, 1.0, 0.3, 1.0)
QUART_OUT = (0.25, 1.0, 0.5, 1.0)
EXPO_IN = (0.7, 0.0, 0.84, 0.0)
CUBIC_IN = (0.55, 0.0, 0.8, 0.2)
INOUT = (0.76, 0.0, 0.24, 1.0)
SOFT_OUT = (0.22, 0.61, 0.36, 1.0)


def io(a, b, t0, t1, t2, t3, ein=EXPO_OUT, eout=EXPO_IN):
    """a -> b over t0..t1, hold b, b -> a over t2..t3."""
    return Anim([(t0, a, ein), (t1, b, HOLD), (t2, b, eout), (t3, a, eout)])


def keys(*k):
    return Anim(list(k))


def _hex(c):
    return "#" + "".join(f"{round(v * 255):02X}" for v in c[:3])


def build(comp, aid, name, description, tags, text_areas, thumb_t=0.5, bg=None,
          playback="intro-hold-outro", intro_end=None, region=None):
    """text_areas: {"name": [x,y,w,h], ...}; the first entry becomes asset.json textArea."""
    if playback == "intro-hold-outro":
        comp.marker("intro", 0, intro_end)
        comp.marker("outro", OUTRO, comp.frames - OUTRO)
    out = ROOT / "lottie" / CATEGORY / aid
    out.mkdir(parents=True, exist_ok=True)
    js = out / f"{aid}.json"
    comp.save(js)
    SCRATCH.mkdir(parents=True, exist_ok=True)
    subprocess.run([str(RENDER), str(js), str(SCRATCH / f"{aid}-sheet.png"), "--sheet", "4",
                    "--strict", "--size", "1600"], check=True, stdout=subprocess.DEVNULL)
    cmd = [str(RENDER), str(js), str(out / "thumbnail.png"), "--size", "512", "--t", str(thumb_t)]
    if bg:
        cmd += ["--bg", bg]
    if region:
        cmd += ["--region", ",".join(map(str, region)), "--pad", "0.03"]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
    areas = list(text_areas.values())
    meta = {
        "schema": 1, "id": aid, "name": name, "type": "lottie", "category": CATEGORY,
        "file": f"{aid}.json", "thumbnail": "thumbnail.png", "license": "CC-BY-NC-SA-4.0",
        "description": description, "tags": tags,
        "width": comp.w, "height": comp.h, "fps": comp.fps, "duration": comp.frames / comp.fps,
        "playback": playback,
        "slots": {k: _hex(v["p"]["k"]) for k, v in comp.slots.items()},
        "textArea": areas[0] if areas else None,
    }
    if len(areas) > 1:
        meta["textAreas"] = text_areas
    with open(out / "asset.json", "w") as f:
        json.dump(meta, f, indent=2)
        f.write("\n")
    print("built", aid)
