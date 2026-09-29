from _platforms import Platform, build_platform

# Simple Icons "substack" (CC0; the logo is a trademark of its owner), 24x24 box.
GLYPH = ("M22.539 8.242H1.46V5.406h21.08v2.836zM1.46 10.812V24L12 18.11 22.54 24V10.812H1.46zM22.54 0H1.46v2.8"
         "36h21.08V0z")

build_platform(Platform(
    "follow-button-substack", "Substack", GLYPH,
    tile="#FF6719", glyph_size=0.46, primary="#FF6719", second="outline", verb="Subscribe", tags=["newsletter"]))
