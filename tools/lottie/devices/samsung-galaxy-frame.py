import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from devices_kit import *

S = dict(sw=720, sh=1560, rs=64, bt=12, bs=12, bb=12, band=6, rim="#2B2D33", cam="punch", hole=30, hole_y=36,
         buttons=[(420, 80, "r"), (540, 150, "r")])
ULTRA = dict(sw=720, sh=1560, rs=26, bt=10, bs=10, bb=10, band=7, rim="#8C8F96", cam="punch", hole=26, hole_y=32,
             buttons=[(400, 80, "r"), (520, 140, "r")])

vs = []
for vid, nm, spec, orient, desc in (
        ("s-series", "S Series", S, "portrait", "Galaxy S: flat display with soft corners and a centred punch-hole camera."),
        ("ultra", "Ultra", ULTRA, "portrait", "Galaxy Ultra: squarer corners, slim bezels and a titanium-grey rim."),
        ("landscape", "Landscape", S, "landscape", "The Galaxy S turned sideways for horizontal video.")):
    c, scr = phone_variant("samsung-galaxy-frame", spec, orient)
    vs.append(Variant(vid, nm, c, "intro-hold", text_areas={"screen": scr}, thumb_t=0.95, bg="6a7087", description=desc))
build_asset(CAT, "samsung-galaxy-frame", "Samsung Galaxy Frame",
            "Samsung Galaxy phone mockup with a punch-hole camera and a real screen cut-out for your video, in S, Ultra "
            "and landscape versions.",
            ["samsung", "galaxy", "android", "phone", "mockup", "frame", "device", "smartphone", "screen recording"], vs)
