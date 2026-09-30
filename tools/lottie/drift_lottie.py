"""Shared output step for Lottie generators: variants, thumbnails, previews and asset.json.

    import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    from drift_lottie import *          # also re-exports everything from lottie_kit

    def make(style):
        comp = Comp("my-asset", 600, 240, frames=60)
        ...
        return comp

    build_asset("call-to-action", "my-asset", "My Asset", "What it is and where text goes.",
                ["tag", ...], [
        Variant("classic", "Classic", make("classic"), "intro-hold", text_area=(...)),
        Variant("outline", "Outline", make("outline"), "intro-hold", text_area=(...)),
    ])

The first variant is the default: plain file names (<id>.json, thumbnail.png, preview.webp,
poster.png) and the asset's top-level fields. Variant <v> gets <id>--<v>.json, thumbnail--<v>.png,
preview--<v>.webp and poster--<v>.png. Every variant, the default included, is listed in
"variants" with its files and whatever it can change (canvas, timing, slots, text areas).
Variants must differ in shape, style or motion, never only in colour (slots cover recolouring).

Flags: --no-preview skips previews/posters; --only=a,b rebuilds just those variants (the others
are kept from the existing asset.json); --sheet also writes a 4x4 contact sheet per variant to
.preview-frames/sheets/ for checking the motion.
"""

import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from lottie_kit import *  # noqa: E402,F401,F403
from lottie_kit import Comp  # noqa: E402

REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
RENDER = os.environ.get("DRIFT_SKOTTIE") or os.path.join(REPO, "tools", "skottie-render", "build", "skottie-render")
STAGE = os.path.join(REPO, ".preview-frames")
LICENSE = "CC-BY-NC-SA-4.0"
PLAYBACKS = ("loop", "intro-hold", "intro-hold-outro")
SLOT_IDS = ("primary", "secondary", "accent", "background", "icon", "outline")
PREVIEW_HEIGHT = 180
PREVIEW_FPS = 20
DEFAULT_BG = "1c1c22"


class Variant:
    """One design of an asset.

    comp: the Comp. playback: loop / intro-hold / intro-hold-outro (the last needs "intro" and
    "outro" markers). text_area: (x, y, w, h) canvas px for the user's main text, or None;
    text_areas: {"name": (x, y, w, h)} when there are several. thumb_t: normalized time of the
    thumbnail/poster frame. bg: thumbnail/preview backdrop RRGGBB (use "e8e8ee" for dark assets).
    region: (x, y, w, h) close-up for the thumbnail of very wide/sparse canvases; pad: thumbnail
    margin as a fraction (default 0.06; use 0 with a tight region).
    description/tags: optional per-variant additions.
    """

    def __init__(self, vid, name, comp, playback, text_area=None, text_areas=None, thumb_t=0.5,
                 bg=None, region=None, pad=None, description=None, tags=None):
        assert isinstance(comp, Comp), "comp must be a lottie_kit.Comp"
        assert playback in PLAYBACKS, f"playback must be one of {PLAYBACKS}"
        assert vid == vid.lower() and vid.replace("-", "").isalnum(), f"variant id {vid!r} must be kebab-case"
        self.id, self.name, self.comp, self.playback = vid, name, comp, playback
        self.text_area, self.text_areas = text_area, text_areas
        self.thumb_t, self.bg, self.region, self.pad = thumb_t, bg or DEFAULT_BG, region, pad
        self.description, self.tags = description, tags


def _hex(rgba):
    return "#" + "".join(f"{round(c * 255):02X}" for c in rgba[:3])


def _rect(r, comp, what):
    r = [round(v) for v in r]
    assert len(r) == 4 and r[2] > 0 and r[3] > 0, f"{what}: bad rect {r}"
    assert r[0] >= 0 and r[1] >= 0 and r[0] + r[2] <= comp.w and r[1] + r[3] <= comp.h, \
        f"{what} {r} is outside the {comp.w}x{comp.h} canvas"
    return r


def _validate(v):
    comp = v.comp
    for sid in comp.slots:
        assert sid in SLOT_IDS, f"slot id {sid!r} is not one of {SLOT_IDS}"
    if v.playback == "intro-hold-outro":
        names = {m["cm"] for m in comp.markers}
        assert {"intro", "outro"} <= names, "intro-hold-outro needs 'intro' and 'outro' markers"
    assert comp.fps == 30, "Drift assets are 30 fps"


def _render(args):
    subprocess.run([RENDER, *args, "--strict"], check=True, stdout=subprocess.DEVNULL)


def _files(asset_id, vid, default):
    if default:
        return f"{asset_id}.json", "thumbnail.png", "preview.webp", "poster.png"
    return f"{asset_id}--{vid}.json", f"thumbnail--{vid}.png", f"preview--{vid}.webp", f"poster--{vid}.png"


def poster_time(category, playback):
    """The poster is the moment the asset is fully on screen: the end of an intro, otherwise mid-way.
    Transitions are solid mid-way, so theirs is taken part-way through the cover-in."""
    if category == "transitions":
        return "0.2"
    return "0.95" if playback == "intro-hold" else "0.5"


def render_preview(json_path, poster, preview, playback, thumb_bg, region=None, tag="x", category=None):
    """Animated preview (canvas aspect clamped 1:1..4:1, 180 px tall) + a still poster."""
    frames = os.path.join(STAGE, tag)
    shutil.rmtree(frames, ignore_errors=True)
    os.makedirs(frames)
    poster_t = poster_time(category, playback)
    args = [json_path, poster, "--frames", frames, "--height", str(PREVIEW_HEIGHT), "--fps", str(PREVIEW_FPS),
            "--t", poster_t, "--bg", thumb_bg]
    if region:
        args += ["--region", ",".join(str(round(c)) for c in region)]
    _render(args)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", str(PREVIEW_FPS),
                    "-i", os.path.join(frames, "%04d.png"), "-c:v", "libwebp_anim", "-q:v", "75",
                    "-loop", "0", preview], check=True)


def build_asset(category, asset_id, name, description, tags, variants):
    argv = sys.argv[1:]
    previews = "--no-preview" not in argv
    sheet = "--sheet" in argv
    only = next((set(a.split("=", 1)[1].split(",")) for a in argv if a.startswith("--only=")), None)
    assert variants, "at least one variant"
    ids = [v.id for v in variants]
    assert len(ids) == len(set(ids)), f"duplicate variant ids {ids}"
    assert asset_id == asset_id.lower() and asset_id.replace("-", "").isalnum(), "asset id must be kebab-case"

    out = os.path.join(REPO, "lottie", category, asset_id)
    os.makedirs(out, exist_ok=True)
    meta_path = os.path.join(out, "asset.json")
    old = {}
    if only and os.path.exists(meta_path):
        old = {e["id"]: e for e in json.load(open(meta_path)).get("variants", [])}

    entries = []
    for i, v in enumerate(variants):
        default = i == 0
        jname, tname, pname, poname = _files(asset_id, v.id, default)
        if only and v.id not in only:
            entries.append(old[v.id])
            continue
        _validate(v)
        comp = v.comp
        jpath = os.path.join(out, jname)
        comp.save(jpath)
        targs = [jpath, os.path.join(out, tname), "--size", "512", "--t", str(v.thumb_t), "--bg", v.bg]
        if v.region:
            targs += ["--region", ",".join(str(round(c)) for c in v.region)]
        if v.pad is not None:
            targs += ["--pad", str(v.pad)]
        _render(targs)
        if sheet:
            os.makedirs(os.path.join(STAGE, "sheets"), exist_ok=True)
            _render([jpath, os.path.join(STAGE, "sheets", f"{asset_id}--{v.id}.png"), "--sheet", "4",
                     "--bg", v.bg])
        if previews:
            render_preview(jpath, os.path.join(out, poname), os.path.join(out, pname), v.playback, v.bg,
                           tag=f"{asset_id}--{v.id}", category=category)
        entry = {
            "id": v.id, "name": v.name, "file": jname, "thumbnail": tname, "preview": pname, "poster": poname,
            "width": comp.w, "height": comp.h, "duration": round(comp.frames / comp.fps, 3),
            "playback": v.playback, "slots": {k: _hex(s["p"]["k"]) for k, s in comp.slots.items()},
            "textArea": _rect(v.text_area, comp, "text_area") if v.text_area else None,
        }
        if v.text_areas:
            entry["textAreas"] = {k: _rect(r, comp, f"text_areas[{k}]") for k, r in v.text_areas.items()}
        if v.description:
            entry["description"] = v.description
        if v.tags:
            entry["tags"] = list(v.tags)
        entries.append(entry)
        print("built", os.path.relpath(jpath, REPO))

    d = entries[0]
    meta = {
        "schema": 1, "id": asset_id, "name": name, "type": "lottie", "category": category,
        "file": d["file"], "thumbnail": d["thumbnail"], "license": LICENSE, "description": description,
        "tags": list(tags), "width": d["width"], "height": d["height"], "fps": 30, "duration": d["duration"],
        "playback": d["playback"], "slots": d["slots"], "textArea": d["textArea"],
    }
    if "textAreas" in d:
        meta["textAreas"] = d["textAreas"]
    meta["variants"] = entries
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)
        f.write("\n")
