import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from devices_kit import *

PRO = dict(sw=820, sh=1180, rs=34, bt=24, bs=24, bb=24, band=7, rim="#AEB1B8", cam="none", buttons=[(120, 60, "r")])
CLASSIC = dict(sw=770, sh=1030, rs=6, bt=130, bs=34, bb=130, band=8, rim="#D9D9DE", cam="home", buttons=[(150, 50, "r")])

vs = []
for vid, nm, spec, orient, desc in (
        ("pro", "iPad Pro", PRO, "landscape", "iPad Pro with even slim bezels, shown landscape for horizontal video."),
        ("pro-portrait", "iPad Pro, Portrait", PRO, "portrait", "iPad Pro standing upright."),
        ("classic", "Home Button", CLASSIC, "landscape", "Classic iPad with a home button, landscape.")):
    c, scr = phone_variant("ipad-frame", spec, orient)
    vs.append(Variant(vid, nm, c, "intro-hold", text_areas={"screen": scr}, thumb_t=0.95, bg="6a7087", description=desc))
build_asset(CAT, "ipad-frame", "iPad Frame",
            "iPad mockup with a real screen cut-out for your video: modern iPad Pro in landscape or portrait, and the "
            "classic home-button iPad.",
            ["ipad", "tablet", "apple", "mockup", "frame", "device", "screen recording"], vs)
