import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from devices_kit import *

P = dict(sw=720, sh=1560, rs=78, bt=18, bs=18, bb=18, band=8, rim="#9CA3AA", cam="punch", hole=32, hole_y=40,
         buttons=[(300, 150, "r"), (480, 70, "r")])
PRO = dict(sw=720, sh=1600, rs=70, bt=14, bs=14, bb=14, band=7, rim="#D9D4C8", cam="punch", hole=30, hole_y=36,
           buttons=[(300, 150, "r"), (480, 70, "r")])

vs = []
for vid, nm, spec, orient, desc in (
        ("pixel", "Pixel", P, "portrait", "Pixel: rounded display, even bezels and a centred camera hole with an aluminium rim."),
        ("pixel-pro", "Pixel Pro", PRO, "portrait", "Pixel Pro: taller display, thinner bezels and a champagne rim."),
        ("landscape", "Landscape", P, "landscape", "The Pixel turned sideways for horizontal video.")):
    c, scr = phone_variant("google-pixel-frame", spec, orient)
    vs.append(Variant(vid, nm, c, "intro-hold", text_areas={"screen": scr}, thumb_t=0.95, bg="6a7087", description=desc))
build_asset(CAT, "google-pixel-frame", "Google Pixel Frame",
            "Google Pixel phone mockup with a centred camera hole and a real screen cut-out for your video, in Pixel, "
            "Pixel Pro and landscape versions.",
            ["pixel", "google", "android", "phone", "mockup", "frame", "device", "smartphone", "screen recording"], vs)
