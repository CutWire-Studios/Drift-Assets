from _platforms import Platform, build_platform

# Simple Icons "kick" (CC0; the logo is a trademark of its owner), 24x24 box.
GLYPH = ("M1.333 0h8v5.333H12V2.667h2.667V0h8v8H20v2.667h-2.667v2.666H20V16h2.667v8h-8v-2.667H12v-2.666H9.333V"
         "24h-8Z")

build_platform(Platform(
    "follow-button-kick", "Kick", GLYPH,
    tile="#000000", rim=True, glyph_color="#53FC19", glyph_size=0.46, primary="#53FC19", badge_icon="#000000",
    done="#FFFFFF", tick="#111111", second="outline", tags=["stream"]))
