"""Shared helpers for the reactions category generators."""

import json
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools" / "lottie"))

from lottie_kit import *  # noqa: E402,F401,F403
from lottie_kit import LINEAR, Anim  # noqa: E402

RENDER = ROOT / "tools" / "skottie-render" / "build" / "skottie-render"


def sampled(fn, t0, t1, step=1, easing=LINEAR):
    """Keys sampled from fn(t) at t0, t0+step, ..., t1 (t1 always included)."""
    ts, t = [], t0
    while t < t1 - 1e-6:
        ts.append(round(t, 3))
        t += step
    ts.append(t1)
    return Anim([(t, fn(t), easing) for t in ts])


def particle(comp, name, shapes, t0, life, total, fn, step=1, wrap=True, **static):
    """A short-lived layer whose transform comes from fn(u) -> dict(position=, scale=, rotation=,
    opacity=) for local time u in [0, life]. If it outlives the comp and wrap is set, a copy
    shifted back by `total` frames keeps a loop seamless."""
    starts = [t0] + ([t0 - total] if wrap and t0 + life > total else [])
    for s in starts:
        keys = {}
        for k in fn(0):
            keys[k] = sampled(lambda t, k=k, s=s: fn(min(max(t - s, 0), life))[k], s, s + life, step)
        comp.layer(name, shapes, ip=s, op=s + life, **static, **keys)


def _hex(rgba):
    return "#" + "".join(f"{round(c * 255):02X}" for c in rgba[:3])


def build(comp, category, aid, name, description, tags, playback, thumb_t, bg=None, text_area=None):
    out = ROOT / "lottie" / category / aid
    out.mkdir(parents=True, exist_ok=True)
    js = out / f"{aid}.json"
    comp.save(js)
    cmd = [str(RENDER), str(js), str(out / "thumbnail.png"), "--size", "512", "--t", str(thumb_t),
           "--strict"]
    if bg:
        cmd += ["--bg", bg]
    subprocess.run(cmd, check=True)
    meta = {
        "schema": 1, "id": aid, "name": name, "type": "lottie", "category": category,
        "file": f"{aid}.json", "thumbnail": "thumbnail.png", "license": "CC-BY-NC-SA-4.0",
        "description": description, "tags": tags, "width": comp.w, "height": comp.h,
        "fps": comp.fps, "duration": round(comp.frames / comp.fps, 3), "playback": playback,
        "slots": {k: _hex(v["p"]["k"]) for k, v in comp.slots.items()}, "textArea": text_area,
    }
    (out / "asset.json").write_text(json.dumps(meta, indent=2) + "\n")
    print("wrote", out)
