"""Write the release index the CutWire marketplace serves Drift Assets from.

    python3 tools/build-index.py OUT_DIR [VERSION]

OUT_DIR receives index.json plus drift-assets.tar.gz (every asset folder, no tools). The index
lists categories in the order Drift shows them and, per asset, its metadata file merged with the
sha256 and size of each shipped file, so the backend and Drift can verify what they fetch.
Standard library only, so CI needs nothing but Python.
"""

import hashlib
import json
import os
import struct
import subprocess
import sys
import tarfile

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Drift's shelf order: what editors reach for most first. Labels are sentence case on purpose.
CATEGORIES = [
    ("lower-thirds", "Lower thirds", "lottie"),
    ("call-to-action", "Call to action", "lottie"),
    ("face-props", "Face props", "face-prop"),
    ("objects", "3D objects", "object"),
    ("callouts", "Callouts", "lottie"),
    ("reactions", "Reactions", "lottie"),
    ("broadcast", "Broadcast", "lottie"),
    ("gaming", "Gaming", "lottie"),
    ("memes", "Memes", "lottie"),
]


def file_entry(asset_dir, name):
    path = os.path.join(asset_dir, name)
    with open(path, "rb") as f:
        data = f.read()
    return {"name": name, "size": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def webp_size(path):
    """Canvas size from a WebP's VP8X chunk (animated WebPs always carry one)."""
    with open(path, "rb") as f:
        head = f.read(30)
    if head[12:16] != b"VP8X":
        raise ValueError(f"{path}: not an extended WebP")
    w = struct.unpack("<I", head[24:27] + b"\0")[0] + 1
    h = struct.unpack("<I", head[27:30] + b"\0")[0] + 1
    return w, h


def asset_dirs(category, kind):
    if kind == "lottie":
        root = os.path.join(REPO, "lottie", category)
    else:
        root = os.path.join(REPO, category)
    return sorted(os.path.join(root, d) for d in os.listdir(root) if os.path.isdir(os.path.join(root, d)))


def build(version):
    categories, assets = [], []
    for sort, (cat_id, label, kind) in enumerate(CATEGORIES):
        categories.append({"id": cat_id, "label": label, "kind": kind, "sort": sort})
        for asset_dir in asset_dirs(cat_id, kind):
            meta_name = "prop.json" if kind == "face-prop" else "asset.json"
            meta = json.load(open(os.path.join(asset_dir, meta_name)))
            main = meta.get("file") or meta["model"]
            files = {
                "meta": file_entry(asset_dir, meta_name),
                "main": file_entry(asset_dir, main),
                "thumbnail": file_entry(asset_dir, "thumbnail.png"),
                "preview": file_entry(asset_dir, "preview.webp"),
            }
            if kind == "lottie":
                files["poster"] = file_entry(asset_dir, "poster.png")
            w, h = webp_size(os.path.join(asset_dir, "preview.webp"))
            assets.append({
                **meta,
                "kind": kind,
                "category": cat_id,
                "path": os.path.relpath(asset_dir, REPO),
                "files": files,
                "preview": {"width": w, "height": h},
            })
    return {"schema": 1, "version": version, "categories": categories, "assets": assets}


def main():
    if not 2 <= len(sys.argv) <= 3:
        sys.exit(__doc__)
    out = sys.argv[1]
    version = sys.argv[2] if len(sys.argv) == 3 else subprocess.run(
        ["git", "-C", REPO, "describe", "--tags", "--always", "--dirty"],
        capture_output=True, text=True, check=True).stdout.strip()
    os.makedirs(out, exist_ok=True)

    index = build(version)
    with open(os.path.join(out, "index.json"), "w") as f:
        json.dump(index, f, indent=1)
        f.write("\n")

    with tarfile.open(os.path.join(out, "drift-assets.tar.gz"), "w:gz") as tar:
        tar.add(os.path.join(out, "index.json"), arcname="index.json")
        for asset in index["assets"]:
            for entry in asset["files"].values():
                name = os.path.join(asset["path"], entry["name"])
                tar.add(os.path.join(REPO, name), arcname=name)
    print(f"{len(index['assets'])} assets in {len(index['categories'])} categories, version {version}")


main()
