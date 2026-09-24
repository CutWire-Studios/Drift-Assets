import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from drift3d import *  # noqa: E402,F403

ID = "clown-nose"
OUT = os.path.join(REPO, "face-props", ID)

reset()
head = reference_head()

bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=0.1, location=(0, -0.2, -0.3))
nose = bpy.context.active_object
nose.name = "ClownNose"
nose.scale = (1.0, 0.97, 0.95)
apply_all(nose)
shade_smooth(nose, 180)
assign(nose, material("ClownRed", "#e0101c", roughness=0.12))

props = [nose]
os.makedirs(OUT, exist_ok=True)
export_glb(os.path.join(OUT, f"{ID}.glb"), props)
write_prop_json(OUT, ID, "Clown Nose", props,
                description="Glossy red clown nose that sits over the tip of the nose.",
                tags=["clown", "nose", "funny", "circus", "red"])
bpy.ops.mesh.primitive_cube_add(size=1, location=(0.06, 0.05, -0.2))
frame = bpy.context.active_object
frame.scale = (0.75, 0.5, 0.8)
frame.hide_render = True
render_prop_thumbnail(os.path.join(OUT, "thumbnail.png"), props, head, region="face")
if "--check" in args():
    render_thumbnail(os.path.join(OUT, "_check.png"), [frame], view=(0.0, -1.0, 0.0), margin=0.85)
