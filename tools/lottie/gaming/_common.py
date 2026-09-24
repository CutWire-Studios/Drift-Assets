import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools" / "lottie"))
from lottie_kit import *  # noqa: E402,F401,F403
from lottie_kit import group, rect, fill, bezier, path  # noqa: E402

RENDER = ROOT / "tools" / "skottie-render" / "build" / "skottie-render"


def box(x, y, w, h, color="#FFFFFF", r=0, slot=None, opacity=100, name="box"):
    """Filled rectangle from its top-left corner."""
    return group([rect((w, h), (x + w / 2, y + h / 2), r), fill(color, opacity, slot=slot)], name)


def pixel_paths(cells, px, origin=(0, 0), name="pixels"):
    """Trace a set of (col, row) grid cells into merged outline paths (holes wind the other way).

    One polygon per connected region, so touching pixels have no anti-aliasing seams.
    """
    cells = set(cells)
    edges = {}
    for c, r in cells:
        # clockwise in screen space; edges shared with a neighbour cancel out
        for a, b in (((c, r), (c + 1, r)), ((c + 1, r), (c + 1, r + 1)),
                     ((c + 1, r + 1), (c, r + 1)), ((c, r + 1), (c, r))):
            if (b, a) in edges:
                del edges[(b, a)]
            else:
                edges[(a, b)] = True
    nxt = {}
    for a, b in edges:
        nxt.setdefault(a, []).append(b)
    loops = []
    while nxt:
        start = next(iter(nxt))
        pts, cur, prev_dir = [start], start, None
        while True:
            outs = nxt[cur]
            if len(outs) > 1 and prev_dir is not None:
                # at a diagonal pinch, turn right (keeps regions separate)
                dx, dy = prev_dir
                right = (-dy, dx)
                outs.sort(key=lambda b: (b[0] - cur[0], b[1] - cur[1]) != right)
            b = outs.pop(0)
            if not outs:
                del nxt[cur]
            prev_dir = (b[0] - cur[0], b[1] - cur[1])
            cur = b
            if cur == start:
                break
            pts.append(cur)
        # drop collinear vertices
        n = len(pts)
        keep = []
        for i in range(n):
            p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
            if (p1[0] - p0[0]) * (p2[1] - p1[1]) != (p1[1] - p0[1]) * (p2[0] - p1[0]):
                keep.append(p1)
        ox, oy = origin
        loops.append([(ox + x * px, oy + y * px) for x, y in keep])
    return [path(bezier(l, closed=True), f"{name}{i}") for i, l in enumerate(loops)]


def grid_cells(rows, ch):
    """Cells of an ASCII-art grid where the character equals `ch`."""
    return [(c, r) for r, line in enumerate(rows) for c, k in enumerate(line) if k == ch]


def _hex(rgba):
    return "#" + "".join(f"{round(c * 255):02X}" for c in rgba[:3])


def finish(comp, asset_id, name, description, tags, playback, text_area=None,
           thumb_t=0.5, bg=None, region=None, category="gaming", text_areas=None):
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
    if text_areas:
        meta["textAreas"] = text_areas
    (out / "asset.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(js)
