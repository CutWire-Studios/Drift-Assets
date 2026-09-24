import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from drift3d import *  # noqa: E402,F403

ID = "halo"
OUT = os.path.join(REPO, "face-props", ID)

reset()
head = reference_head()

bpy.ops.mesh.primitive_torus_add(major_segments=96, minor_segments=24, major_radius=0.3, minor_radius=0.03,
                                 location=(0, 0.45, 1.05), rotation=(math.radians(20), math.radians(5), 0))
halo = bpy.context.active_object
halo.name = "Halo"
halo.scale = (1.0, 1.0, 0.8)
apply_all(halo)
shade_smooth(halo, 180)
assign(halo, material("HaloGold", "#ffc83d", roughness=0.35, emission="#ffb01f", emission_strength=1.0))

props = [halo]
os.makedirs(OUT, exist_ok=True)
export_glb(os.path.join(OUT, f"{ID}.glb"), props)
write_prop_json(OUT, ID, "Halo", props,
                description="Glowing golden halo floating above the head.",
                tags=["halo", "angel", "glow", "gold", "heaven"])
render_prop_thumbnail(os.path.join(OUT, "thumbnail.png"), props, head, region="head")
if "--check" in args():
    render_thumbnail(os.path.join(OUT, "_check.png"), [head] + props, view=(0.0, -1.0, 0.0), margin=0.95)
