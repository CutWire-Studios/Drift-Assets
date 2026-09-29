"""Lint every asset against the rules in CONTRIBUTING.md.

    python3 tools/check-assets.py [--counts] [PATH_OR_ID ...]

Checks metadata and files (variants included), unique kebab-case ids, a generator script per
asset, 512x512 thumbnails, Lottie content rules (no text/image layers, expressions, 3D, fonts;
30 fps; known slot ids) and .glb rules (no Draco/meshopt, under 50k vertices, objects carry exactly
one animation, face props none). Exits 1 on any problem. Standard library only, so CI can run it.
"""

import glob
import json
import os
import re
import struct
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SLOT_IDS = {"primary", "secondary", "accent", "background", "icon", "outline"}
PLAYBACKS = {"loop", "intro-hold", "intro-hold-outro"}
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_VERTS = 50000

problems = []


def bad(where, msg):
    problems.append(f"{os.path.relpath(where, REPO)}: {msg}")


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", head[16:24])


def glb_json(path):
    with open(path, "rb") as f:
        data = f.read()
    if data[:4] != b"glTF":
        raise ValueError("not a GLB")
    length, ctype = struct.unpack("<II", data[12:20])
    if ctype != 0x4E4F534A:
        raise ValueError("first chunk is not JSON")
    return json.loads(data[20:20 + length])


def check_glb(path, kind):
    try:
        g = glb_json(path)
    except (OSError, ValueError) as e:
        bad(path, f"unreadable glb ({e})")
        return
    ext = set(g.get("extensionsUsed", []))
    for e in ("KHR_draco_mesh_compression", "EXT_meshopt_compression", "KHR_meshopt_compression"):
        if e in ext:
            bad(path, f"uses {e}; Drift rejects compressed meshes")
    verts = sum(g["accessors"][p["attributes"]["POSITION"]]["count"]
                for m in g.get("meshes", []) for p in m["primitives"] if "POSITION" in p["attributes"])
    if verts > MAX_VERTS:
        bad(path, f"{verts} vertices (budget {MAX_VERTS})")
    anims = g.get("animations", [])
    if kind == "object" and len(anims) != 1:
        bad(path, f"objects need exactly one animation, found {len(anims)}")
    if kind == "face-prop" and anims:
        bad(path, "face props must be static (Drift does not play their animations)")
    for img in g.get("images", []):
        if img.get("uri"):
            bad(path, "external image uri; embed textures")


def walk_lottie(node, where, path):
    if isinstance(node, list):
        for n in node:
            walk_lottie(n, where, path)
    elif isinstance(node, dict):
        if isinstance(node.get("x"), str) and ("k" in node or "a" in node):
            bad(path, f"expression in {where}")
        for v in node.values():
            if isinstance(v, (dict, list)):
                walk_lottie(v, where, path)


def check_lottie_json(path, fps_expected=30):
    try:
        doc = json.load(open(path))
    except (OSError, ValueError) as e:
        bad(path, f"unreadable json ({e})")
        return None
    if doc.get("fr") != fps_expected:
        bad(path, f"fps {doc.get('fr')} (must be 30)")
    if doc.get("ddd"):
        bad(path, "3D composition")
    if doc.get("fonts") or doc.get("chars"):
        bad(path, "fonts/chars")
    for a in doc.get("assets", []):
        if a.get("p") or a.get("u"):
            bad(path, "image asset")
    layers = list(doc.get("layers", []))
    for a in doc.get("assets", []):
        layers += a.get("layers", [])
    for layer in layers:
        name = layer.get("nm", layer.get("ind"))
        if layer.get("ty") == 5:
            bad(path, f"text layer {name!r}")
        if layer.get("ty") == 2:
            bad(path, f"image layer {name!r}")
        if layer.get("ddd"):
            bad(path, f"3D layer {name!r}")
        walk_lottie(layer, f"layer {name!r}", path)
    for sid in doc.get("slots", {}):
        if sid not in SLOT_IDS:
            bad(path, f"slot id {sid!r} not in {sorted(SLOT_IDS)}")
    return doc


def need(asset_dir, name, what):
    if not name:
        bad(asset_dir, f"missing {what} field")
        return False
    if not os.path.isfile(os.path.join(asset_dir, name)):
        bad(asset_dir, f"{what} file {name!r} not found")
        return False
    return True


def check_thumb(asset_dir, name):
    if need(asset_dir, name, "thumbnail"):
        size = png_size(os.path.join(asset_dir, name))
        if size != (512, 512):
            bad(asset_dir, f"{name} is {size}, must be 512x512 PNG")


def check_variants(asset_dir, meta, kind):
    variants = meta.get("variants")
    if variants is None:
        return [None]
    if not variants:
        bad(asset_dir, "empty variants list")
        return [None]
    ids = [v.get("id") for v in variants]
    if len(set(ids)) != len(ids):
        bad(asset_dir, f"duplicate variant ids {ids}")
    for v in variants:
        if not v.get("id") or not KEBAB.match(v["id"]):
            bad(asset_dir, f"variant id {v.get('id')!r} is not kebab-case")
        if not v.get("name"):
            bad(asset_dir, f"variant {v.get('id')!r} has no name")
    main_key = "model" if kind == "face-prop" else "file"
    d = variants[0]
    if d.get(main_key) != meta.get(main_key) or d.get("thumbnail") != meta.get("thumbnail"):
        bad(asset_dir, "first variant must be the default (same files as the top level)")
    return variants


def check_asset(asset_dir, kind, category, seen):
    aid = os.path.basename(asset_dir)
    meta_name = "prop.json" if kind == "face-prop" else "asset.json"
    mpath = os.path.join(asset_dir, meta_name)
    if not os.path.isfile(mpath):
        bad(asset_dir, f"missing {meta_name}")
        return
    try:
        meta = json.load(open(mpath))
    except ValueError as e:
        bad(mpath, f"invalid json ({e})")
        return
    if not KEBAB.match(aid):
        bad(asset_dir, "id is not kebab-case")
    if aid in seen:
        bad(asset_dir, f"id also used by {seen[aid]}")
    seen[aid] = os.path.relpath(asset_dir, REPO)
    if meta.get("id") != aid:
        bad(mpath, f"id {meta.get('id')!r} does not match folder")
    if meta.get("type") != kind:
        bad(mpath, f"type {meta.get('type')!r}, expected {kind!r}")
    for k in ("name", "description", "license"):
        if not meta.get(k):
            bad(mpath, f"missing {k}")
    if not meta.get("tags"):
        bad(mpath, "no tags")

    if kind == "lottie":
        script = os.path.join(REPO, "tools", "lottie", category, f"{aid}.py")
        if meta.get("category") != category:
            bad(mpath, f"category {meta.get('category')!r}, expected {category!r}")
    else:
        script = os.path.join(REPO, "tools", "blender", "face-props" if kind == "face-prop" else "objects", f"{aid}.py")
    if not os.path.isfile(script):
        bad(asset_dir, f"no generator script {os.path.relpath(script, REPO)}")

    variants = check_variants(asset_dir, meta, kind)
    for v in variants:
        src = meta if v is None else {**meta, **v}
        preview = src.get("preview") if v is not None else "preview.webp"
        check_thumb(asset_dir, src.get("thumbnail"))
        need(asset_dir, preview, "preview")
        if kind == "lottie":
            poster = src.get("poster") if v is not None else "poster.png"
            need(asset_dir, poster, "poster")
            if need(asset_dir, src.get("file"), "file"):
                doc = check_lottie_json(os.path.join(asset_dir, src["file"]))
                if doc:
                    if (doc["w"], doc["h"]) != (src.get("width"), src.get("height")):
                        bad(asset_dir, f"{src['file']}: canvas {doc['w']}x{doc['h']} != metadata "
                                       f"{src.get('width')}x{src.get('height')}")
                    if set(doc.get("slots", {})) != set(src.get("slots", {})):
                        bad(asset_dir, f"{src['file']}: slots differ from metadata")
                    if src.get("playback") not in PLAYBACKS:
                        bad(asset_dir, f"{src['file']}: playback {src.get('playback')!r}")
                    if src.get("playback") == "intro-hold-outro":
                        names = {m.get("cm") for m in doc.get("markers", [])}
                        if not {"intro", "outro"} <= names:
                            bad(asset_dir, f"{src['file']}: intro-hold-outro needs intro/outro markers")
                    for r in [src.get("textArea")] + list((src.get("textAreas") or {}).values()):
                        if r and (r[0] < 0 or r[1] < 0 or r[0] + r[2] > doc["w"] or r[1] + r[3] > doc["h"]):
                            bad(asset_dir, f"{src['file']}: text area {r} outside canvas")
        elif kind == "face-prop":
            if need(asset_dir, src.get("model"), "model"):
                check_glb(os.path.join(asset_dir, src["model"]), kind)
            p = src.get("params") or {}
            for k in ("scale", "offsetX", "offsetY", "offsetZ"):
                if not isinstance(p.get(k), (int, float)):
                    bad(asset_dir, f"params.{k} missing")
        else:
            if need(asset_dir, src.get("file"), "file"):
                check_glb(os.path.join(asset_dir, src["file"]), kind)
            a = src.get("animation") or {}
            if not a.get("loop") or not a.get("duration"):
                bad(asset_dir, "animation {name, duration, loop: true} missing")


def main():
    argv = sys.argv[1:]
    show_counts = "--counts" in argv
    only = [a for a in argv if not a.startswith("--")]
    seen, counts = {}, {"lottie": 0, "face-prop": 0, "object": 0}
    variants = {"lottie": 0, "face-prop": 0, "object": 0}
    dirs = [(d, "lottie", d.split(os.sep)[-2]) for d in sorted(glob.glob(os.path.join(REPO, "lottie", "*", "*")))]
    dirs += [(d, "face-prop", None) for d in sorted(glob.glob(os.path.join(REPO, "face-props", "*")))]
    dirs += [(d, "object", None) for d in sorted(glob.glob(os.path.join(REPO, "objects", "*")))]
    for d, kind, cat in dirs:
        if not os.path.isdir(d):
            continue
        counts[kind] += 1
        mname = "prop.json" if kind == "face-prop" else "asset.json"
        try:
            variants[kind] += len(json.load(open(os.path.join(d, mname))).get("variants") or [None])
        except (OSError, ValueError):
            pass
        rel = os.path.relpath(d, REPO)
        if only and not any(o == os.path.basename(d) or rel.startswith(o.rstrip("/")) for o in only):
            seen[os.path.basename(d)] = rel
            continue
        check_asset(d, kind, cat, seen)
    for p in problems:
        print(p)
    if show_counts or not problems:
        for k in counts:
            print(f"{k}: {counts[k]} assets, {variants[k]} designs")
    if problems:
        print(f"{len(problems)} problem(s)")
        sys.exit(1)


main()
