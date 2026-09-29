"""Regenerate the asset tables in README.md from the asset metadata.

    python3 tools/build-readme.py

Rewrites everything between the "<!-- assets:begin -->" and "<!-- assets:end -->" markers: one
section per Lottie category (in the index's shelf order), then face props and 3D objects, each a
4-column grid of default thumbnails with the id and the number of designs. Standard library only.
"""

import glob
import importlib.util
import json
import os

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BEGIN, END = "<!-- assets:begin -->", "<!-- assets:end -->"
COLS = 4


def categories():
    spec = importlib.util.spec_from_file_location("build_index_src", os.path.join(REPO, "tools", "build-index.py"))
    src = open(spec.origin).read()
    start = src.index("CATEGORIES = [")
    end = src.index("]\n", start) + 1
    ns = {}
    exec(src[start:end], ns)
    return ns["CATEGORIES"]


def cell(rel_dir, meta):
    n = len(meta.get("variants") or [None])
    designs = f" · {n} designs" if n > 1 else ""
    return f'<img src="{rel_dir}/thumbnail.png" width="160"><br>`{meta["id"]}`{designs}'


def grid(entries):
    lines = ["|" + "   |" * COLS, "|" + "---|" * COLS]
    for i in range(0, len(entries), COLS):
        lines.append("| " + " | ".join(entries[i:i + COLS]) + " |")
    return lines


def section(root, meta_name):
    out = []
    for d in sorted(glob.glob(os.path.join(REPO, root, "*"))):
        mpath = os.path.join(d, meta_name)
        if os.path.isfile(mpath):
            out.append(cell(os.path.relpath(d, REPO), json.load(open(mpath))))
    return out


def main():
    lines = []
    lottie_cats = [c for c in categories() if c[2] == "lottie"]
    total = {"lottie": 0, "face-prop": 0, "object": 0}
    lines.append("## Lottie animations")
    for cat_id, label, _ in lottie_cats:
        cells = section(os.path.join("lottie", cat_id), "asset.json")
        if not cells:
            continue
        total["lottie"] += len(cells)
        lines += ["", f"### {label}", ""] + grid(cells)
    for title, root, meta_name, kind in (("Face props", "face-props", "prop.json", "face-prop"),
                                         ("3D objects", "objects", "asset.json", "object")):
        cells = section(root, meta_name)
        total[kind] = len(cells)
        lines += ["", f"## {title}", ""] + grid(cells)
    summary = (f"{total['lottie']} Lottie animations, {total['face-prop']} face props and "
               f"{total['object']} 3D objects; most come in several designs.")

    path = os.path.join(REPO, "README.md")
    text = open(path).read()
    a, b = text.index(BEGIN) + len(BEGIN), text.index(END)
    text = text[:a] + "\n" + summary + "\n\n" + "\n".join(lines) + "\n\n" + text[b:]
    with open(path, "w") as f:
        f.write(text)
    print(summary)


main()
