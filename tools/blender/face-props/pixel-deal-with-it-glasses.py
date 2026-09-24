import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from drift3d import *  # noqa: E402,F403

ID = "pixel-deal-with-it-glasses"
OUT = os.path.join(REPO, "face-props", ID)

P = 0.04          # voxel size in head-widths
FRONT_Y = -0.165  # front face of the frame
TEMPLE_LEN = 14   # voxels back toward the ears

# 26 columns, row 0 on top. '#' black, 'w' white highlight.
ROWS = [
    "##########################",
    ".########################.",
    "..##ww######..##ww######..",
    "..####ww####..####ww####..",
    "...#########..#########...",
    "....#######....#######....",
]


def voxel_mesh(cells, name, mats):
    """cells: {(i, j, k): mat_index}; i = x, j = z (up), k = y (back). Emits only exposed faces."""
    bm = bmesh.new()
    dirs = [((1, 0, 0), [(1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 0, 1)]),
            ((-1, 0, 0), [(0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 1, 0)]),
            ((0, 1, 0), [(0, 1, 0), (0, 1, 1), (1, 1, 1), (1, 1, 0)]),
            ((0, -1, 0), [(0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1)]),
            ((0, 0, 1), [(0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)]),
            ((0, 0, -1), [(0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 0)])]
    ncols = len(ROWS[0])
    x0 = -ncols * P / 2
    z0 = 0.11
    for (i, j, k), mi in cells.items():
        for (di, dj, dk), corners in dirs:
            if (i + di, j + dj, k + dk) in cells:
                continue
            vs = [bm.verts.new((x0 + (i + a) * P, FRONT_Y + (k + c) * P, z0 - (j + b) * P))
                  for a, b, c in corners]
            f = bm.faces.new(vs)
            f.material_index = mi
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(obj)
    for m in mats:
        me.materials.append(m)
    bev = obj.modifiers.new("Bevel", "BEVEL")
    bev.width = 0.005
    bev.segments = 2
    bev.limit_method = "ANGLE"
    bev.harden_normals = False
    apply_all(obj)
    shade_smooth(obj, 35)
    return obj


def build():
    black = material("PixelBlack", "#0b0b0d", roughness=0.35)
    white = material("PixelWhite", "#ffffff", roughness=0.5)
    cells = {}
    for j, row in enumerate(ROWS):
        for i, ch in enumerate(row):
            if ch != ".":
                cells[(i, j, 0)] = 1 if ch == "w" else 0
    last = len(ROWS[0]) - 1
    for k in range(1, TEMPLE_LEN + 1):
        cells[(0, 0, k)] = 0
        cells[(last, 0, k)] = 0
    return [voxel_mesh(cells, "DealWithItGlasses", [black, white])]


if __name__ == "__main__":
    reset()
    head = reference_head()
    props = build()
    os.makedirs(OUT, exist_ok=True)
    head.hide_render = False
    render_prop_thumbnail(os.path.join(OUT, "thumbnail.png"), props, head, region="face")
    if "--check" in args():
        render_thumbnail(os.path.join(OUT, "_check.png"), [head] + props, view=(0, -1, 0.05),
                         margin=1.05)
        render_thumbnail(os.path.join(OUT, "_check2.png"), [head] + props, view=(-1, 0, 0.05),
                         margin=1.05)
    bpy.data.objects.remove(head, do_unlink=True)
    export_glb(os.path.join(OUT, f"{ID}.glb"), props)
    write_prop_json(OUT, ID, "Pixel Deal With It Glasses", props,
                    description="8-bit 'deal with it' meme sunglasses built from black voxel blocks "
                                "with white highlight pixels.",
                    tags=["glasses", "sunglasses", "meme", "pixel", "8-bit", "deal with it", "funny"])
