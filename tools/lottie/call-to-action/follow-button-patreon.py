from _platforms import Platform, build_platform

# Simple Icons "patreon" (CC0; the logo is a trademark of its owner), 24x24 box.
GLYPH = ("M22.957 7.21c-.004-3.064-2.391-5.576-5.191-6.482-3.478-1.125-8.064-.962-11.384.604C2.357 3.231 1.093"
         " 7.391 1.046 11.54c-.039 3.411.302 12.396 5.369 12.46 3.765.047 4.326-4.804 6.068-7.141 1.24-1.662 2"
         ".836-2.132 4.801-2.618 3.376-.836 5.678-3.501 5.673-7.031Z")

build_platform(Platform(
    "follow-button-patreon", "Patreon", GLYPH,
    tile="#000000", rim=True, glyph_size=0.52, primary="#FF424D", second="outline", verb="Join",
    tags=["membership"]))
