from _platforms import Platform, build_platform

# Simple Icons "youtubeshorts" (CC0; the logo is a trademark of its owner), 24x24 box.
GLYPH = ("m18.931 9.99-1.441-.601 1.717-.913a4.48 4.48 0 0 0 1.874-6.078 4.506 4.506 0 0 0-6.09-1.874L4.792 5."
         "929a4.504 4.504 0 0 0-2.402 4.193 4.521 4.521 0 0 0 2.666 3.904c.036.012 1.442.6 1.442.6l-1.706.901a"
         "4.51 4.51 0 0 0-2.369 3.967A4.528 4.528 0 0 0 6.93 24c.725 0 1.437-.174 2.08-.508l10.21-5.406a4.494 "
         "4.494 0 0 0 2.39-4.192 4.525 4.525 0 0 0-2.678-3.904ZM9.597 15.19V8.824l6.007 3.184z")

build_platform(Platform(
    "follow-button-youtube-shorts", "YouTube Shorts", GLYPH,
    kind="knockout", shape="custom", path_fill="#FF0000", backing=[("ellipse", 12.4, 12, 9, 9)],
    primary="#FF0000", secondary="#272727", glass_bg="3a1414", badge_at=(46, 54), verb="Subscribe",
    tags=["youtube", "shorts"]))
