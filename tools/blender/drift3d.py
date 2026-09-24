"""Helpers for Blender scripts that build Drift 3D assets (face props and objects).

Run a build script headless (the Blender flatpak's cwd is /app/blender, so always pass absolute
paths; --factory-startup keeps user add-ons such as the MCP server out of the process):

    flatpak run org.blender.Blender -b --factory-startup --python-exit-code 1 \
        --python "$PWD/tools/blender/face-props/aviators.py"

Drift renders .glb with a simple Blinn-Phong shader. Only these material inputs survive:
base colour (factor or UV0 texture), metallic factor, roughness factor, emissive factor, alpha
(OPAQUE/MASK/BLEND) and double-sided. Normal/AO/roughness maps and procedural nodes are ignored,
so build looks from geometry + flat materials. No Draco/meshopt. Keep it under ~100k vertices.
"""

import json
import math
import os
import sys

import bpy
import bmesh
from mathutils import Vector

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LICENSE = "CC-BY-NC-SA-4.0"
THUMB_SIZE = 512
THUMB_BG = (0x1c / 255, 0x1c / 255, 0x22 / 255)


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.render.fps = 30
    return scene


def material(name, color, metallic=0.0, roughness=0.5, emission=None, emission_strength=1.0,
             alpha=1.0, double_sided=False):
    """Principled material with factors only (what Drift reads). color: '#RRGGBB' or (r,g,b) linear."""
    if isinstance(color, str):
        color = srgb_hex(color)
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    if emission is not None:
        e = srgb_hex(emission) if isinstance(emission, str) else emission
        bsdf.inputs["Emission Color"].default_value = (*e, 1.0)
        bsdf.inputs["Emission Strength"].default_value = emission_strength
    if alpha < 1.0:
        bsdf.inputs["Alpha"].default_value = alpha
        try:
            m.surface_render_method = "BLENDED"
        except (AttributeError, TypeError):
            m.blend_method = "BLEND"
    m.use_backface_culling = not double_sided
    return m


def srgb_hex(h):
    h = h.lstrip("#")

    def lin(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    return tuple(lin(int(h[i:i + 2], 16)) for i in (0, 2, 4))


def assign(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    return obj


def apply_all(obj):
    """Apply modifiers and transforms so the exported mesh is what you see."""
    bpy.context.view_layer.objects.active = obj
    for o in bpy.context.selected_objects:
        o.select_set(False)
    obj.select_set(True)
    for mod in list(obj.modifiers):
        bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return obj


def join(objs, name):
    for o in bpy.context.selected_objects:
        o.select_set(False)
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    objs[0].name = name
    return objs[0]


def shade_smooth(obj, angle_deg=40):
    for o in bpy.context.selected_objects:
        o.select_set(False)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    try:
        bpy.ops.object.shade_auto_smooth(angle=math.radians(angle_deg))
    except (AttributeError, RuntimeError):
        bpy.ops.object.shade_smooth()
    return obj


def mesh_objects(exclude=()):
    return [o for o in bpy.context.scene.objects if o.type == "MESH" and o.name not in exclude]


def world_bbox(objs):
    pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    return lo, hi


def export_glb(path, objects=None, animations=False):
    """Export to glTF binary (+Y up). Blender Z-up/-Y-forward maps to glTF +Y up/+Z toward viewer.

    Drift plays one animation per file: with several animated nodes, give them all one shared
    action (one slot per node), or the exporter writes one glTF animation per node.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    for o in bpy.context.selected_objects:
        o.select_set(False)
    objs = objects if objects is not None else mesh_objects()
    for o in objs:
        o.select_set(True)
    bpy.ops.export_scene.gltf(
        filepath=path, export_format="GLB", use_selection=True, export_apply=True,
        export_yup=True, export_animations=animations, export_draco_mesh_compression_enable=False,
        export_cameras=False, export_lights=False, export_extras=False)
    print("wrote", path)


# ---------------------------------------------------------------- face-prop head space
#
# Model face props in HEAD SPACE, 1 Blender unit = 1 head-width (the tracked face-oval width):
#   origin = midpoint between the eyes, +X = subject's left on screen (image right),
#   +Z = toward the forehead (glTF +Y), -Y = toward the camera (glTF +Z).
# Reference proportions (head-widths): pupils x=±0.22, z=0; nose tip y=-0.2, z=-0.35;
# mouth z=-0.55; chin z=-0.85; brow z=+0.12; hairline z=+0.55; crown z=+0.85;
# ears x=±0.5, z≈-0.15..+0.1, y≈+0.45; face front plane y≈-0.05 at the eyes.
# Drift hides prop parts behind an ellipsoid (half-axes 0.5 x 0.5*ry/rx x 0.575, centred at the
# eye midpoint and pushed back 0.575), so temples/backs of hats are occluded automatically.

HEAD_REF = {"pupil_x": 0.22, "nose_y": -0.2, "nose_z": -0.35, "mouth_z": -0.55, "chin_z": -0.85,
            "brow_z": 0.12, "hairline_z": 0.55, "crown_z": 0.85, "ear_x": 0.5, "ear_y": 0.45}


def reference_head(name="RefHead"):
    """Neutral mannequin head in head space, for fitting and thumbnails. Never export it.

    Skull reaches HEAD_REF crown_z; the nose starts near eye level; a muzzle fills the mouth
    area so lip-level props have a surface to sit on.
    """
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=32, radius=0.5)
    h = bpy.context.active_object
    h.name = name
    h.scale = (1.0, 1.15, 1.3)
    h.location = (0, 0.5, -0.05)
    apply_all(h)
    # Stretch the upper half into a fuller dome whose top is at crown_z.
    for v in h.data.vertices:
        t = (v.co.z + 0.05) / 0.65
        if t > 0:
            r = math.sqrt(max(1 - t * t, 0))
            r2 = max(1 - t ** 2.4, 0) ** (1 / 2.4)
            s = r2 / r if r > 1e-6 else 1
            v.co.x *= s
            v.co.y = 0.5 + (v.co.y - 0.5) * s
            v.co.z = -0.05 + t * (HEAD_REF["crown_z"] + 0.05)
    parts = [h]
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=16, radius=0.11)
    nose = bpy.context.active_object
    nose.scale = (0.7, 1.0, 1.9)
    nose.location = (0, -0.1, -0.24)
    nose.rotation_euler = (math.radians(-15), 0, 0)
    parts.append(nose)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.3)
    muzzle = bpy.context.active_object
    muzzle.scale = (0.8, 0.45, 0.75)
    muzzle.location = (0, 0.12, -0.47)
    parts.append(muzzle)
    for x in (-0.5, 0.5):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=12, radius=0.12)
        ear = bpy.context.active_object
        ear.scale = (0.35, 0.8, 1.2)
        ear.location = (x, 0.45, -0.05)
        parts.append(ear)
    head = join(parts, name)
    shade_smooth(head, 60)
    assign(head, material("RefHeadMat", "#8a8f99", roughness=0.7))
    return head


def write_prop_json(dir_path, asset_id, name, prop_objs, description="", tags=(), extra=None):
    """Write prop.json with the Drift face-model params that put the prop exactly where it was modelled.

    Drift re-centres a face-prop model on its AABB centre and scales it to 1 head-width in X.
    Undo that: scale = authored X extent, offset = authored AABB centre (both in head-widths,
    converted to glTF axes: x, y=blender z, z=-blender y).
    """
    lo, hi = world_bbox(prop_objs)
    ext = hi - lo
    c = (lo + hi) / 2
    params = {"scale": round(ext.x, 4), "offsetX": round(c.x, 4), "offsetY": round(c.z, 4),
              "offsetZ": round(-c.y, 4), "rotX": 0, "rotY": 0, "rotZ": 0, "occlusion": True}
    if extra:
        params.update(extra)
    data = {"schema": 1, "id": asset_id, "name": name, "type": "face-prop", "model": f"{asset_id}.glb",
            "thumbnail": "thumbnail.png", "license": LICENSE, "description": description,
            "tags": list(tags), "anchor": "eyes", "params": params}
    with open(os.path.join(dir_path, "prop.json"), "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    print("wrote", os.path.join(dir_path, "prop.json"), params)


def write_asset_json(dir_path, asset_id, name, kind, file, description="", tags=(), extra=None):
    data = {"schema": 1, "id": asset_id, "name": name, "type": kind, "file": file,
            "thumbnail": "thumbnail.png", "license": LICENSE, "description": description,
            "tags": list(tags)}
    if extra:
        data.update(extra)
    with open(os.path.join(dir_path, "asset.json"), "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


# ---------------------------------------------------------------- thumbnails

def render_thumbnail(path, targets, frame=None, view=(0.0, -1.0, 0.25), margin=1.25, lens=50,
                     transparent=False):
    """Render a square THUMB_SIZE PNG framing `targets` (mesh objects) with a 3-point light rig.

    view: direction from the subject toward the camera (Blender axes). Adds and later removes
    its own camera and lights.
    """
    scene = bpy.context.scene
    if frame is not None:
        scene.frame_set(frame)
    lo, hi = world_bbox(targets)
    centre = (lo + hi) / 2
    radius = max((hi - lo).length / 2, 1e-3)

    cam_data = bpy.data.cameras.new("ThumbCam")
    cam_data.lens = lens
    cam = bpy.data.objects.new("ThumbCam", cam_data)
    scene.collection.objects.link(cam)
    fov = 2 * math.atan(cam_data.sensor_width / (2 * lens))
    dist = radius * margin / math.sin(fov / 2)
    d = Vector(view).normalized()
    cam.location = centre + d * dist
    cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
    cam_data.clip_start = dist / 100
    cam_data.clip_end = dist * 10
    scene.camera = cam

    added = [cam]
    for nm, energy, off in (("Key", 4.0, (-1.0, -1.2, 1.4)), ("Fill", 1.5, (1.3, -0.8, 0.3)),
                            ("Rim", 3.0, (0.4, 1.4, 1.2))):
        ld = bpy.data.lights.new(nm, "AREA")
        ld.energy = energy * (dist ** 2) * 18
        ld.size = radius * 2
        lo_ = bpy.data.objects.new(nm, ld)
        scene.collection.objects.link(lo_)
        lo_.location = centre + Vector(off) * dist
        lo_.rotation_euler = (centre - lo_.location).to_track_quat("-Z", "Y").to_euler()
        added.append(lo_)

    world = scene.world or bpy.data.worlds.new("World")
    scene.world = world
    world.use_nodes = True
    bg = next(n for n in world.node_tree.nodes if n.type == "BACKGROUND")
    bg.inputs["Color"].default_value = (*[c ** 2.2 for c in THUMB_BG], 1)
    bg.inputs["Strength"].default_value = 0.6

    r = scene.render
    r.resolution_x = r.resolution_y = THUMB_SIZE
    r.resolution_percentage = 100
    r.film_transparent = transparent
    r.image_settings.file_format = "PNG"
    r.image_settings.color_mode = "RGBA"
    for engine in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"):
        try:
            r.engine = engine
            break
        except TypeError:
            continue
    try:
        scene.view_settings.view_transform = "Standard"
    except TypeError:
        pass
    r.filepath = path
    bpy.ops.render.render(write_still=True)
    print("wrote", path)

    for o in added:
        bpy.data.objects.remove(o, do_unlink=True)


def render_prop_thumbnail(path, props, head, region="head", view=(-0.45, -1.0, 0.15)):
    """Standard face-prop thumbnail: the prop on the mannequin, front three-quarter view.

    Eyes and a mouth are added only for the render (the fitting head stays featureless so
    ray-cast fitting is unaffected). region "face" frames the face for small props such as
    glasses, noses and mustaches; "head" frames the whole head plus the prop.
    """
    dark = material("ThumbFeature", "#23252c", roughness=0.25)
    temp = []

    def on_surface(x, z, depth):
        ok, loc, _, _ = head.ray_cast(Vector((x, -3, z)), Vector((0, 1, 0)))
        return (x, (loc.y if ok else 0.0) + depth, z)

    for x in (-HEAD_REF["pupil_x"], HEAD_REF["pupil_x"]):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.05,
                                             location=on_surface(x * 0.9, 0.0, 0.004))
        eye = bpy.context.active_object
        eye.scale = (1.0, 0.45, 1.15)
        temp.append(assign(shade_smooth(eye, 180), dark))
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.1,
                                         location=on_surface(0, HEAD_REF["mouth_z"] - 0.07, 0.006))
    mouth = bpy.context.active_object
    mouth.scale = (0.85, 0.2, 0.16)
    temp.append(assign(shade_smooth(mouth, 180), dark))

    if region == "face":
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.0, -0.3))
        box = bpy.context.active_object
        box.scale = (1.05, 0.5, 1.05)
        box.hide_render = True
        temp.append(box)
        targets = [box] + props
    else:
        targets = [head] + props
    render_thumbnail(path, targets, view=view, margin=0.95 if region == "head" else 0.8)
    for o in temp:
        bpy.data.objects.remove(o, do_unlink=True)


def args():
    """Script arguments after `--`."""
    return sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
