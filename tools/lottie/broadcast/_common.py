import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools" / "lottie"))
from lottie_kit import *  # noqa: E402,F401,F403
from lottie_kit import group, rect, fill  # noqa: E402

RENDER = ROOT / "tools" / "skottie-render" / "build" / "skottie-render"


def box(x, y, w, h, color="#FFFFFF", r=0, slot=None, opacity=100, name="box"):
    """Filled rectangle from its top-left corner."""
    return group([rect((w, h), (x + w / 2, y + h / 2), r), fill(color, opacity, slot=slot)], name)


def _hex(rgba):
    return "#" + "".join(f"{round(c * 255):02X}" for c in rgba[:3])


def finish(comp, category, asset_id, name, description, tags, playback, text_area=None,
           thumb_t=0.5, bg=None, region=None):
    out = ROOT / "lottie" / category / asset_id
    out.mkdir(parents=True, exist_ok=True)
    js = out / f"{asset_id}.json"
    comp.save(js)
    cmd = [str(RENDER), str(js), str(out / "thumbnail.png"), "--size", "512", "--t", str(thumb_t),
           "--strict"]
    if bg:
        cmd += ["--bg", bg]
    if region:
        cmd += ["--region", ",".join(map(str, region)), "--pad", "0"]
    subprocess.run(cmd, check=True)
    meta = {
        "schema": 1, "id": asset_id, "name": name, "type": "lottie", "category": category,
        "file": js.name, "thumbnail": "thumbnail.png", "license": "CC-BY-NC-SA-4.0",
        "description": description, "tags": tags, "width": comp.w, "height": comp.h,
        "fps": comp.fps, "duration": round(comp.frames / comp.fps, 3), "playback": playback,
        "slots": {k: _hex(v["p"]["k"]) for k, v in comp.slots.items()},
        "textArea": text_area,
    }
    (out / "asset.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(js)
