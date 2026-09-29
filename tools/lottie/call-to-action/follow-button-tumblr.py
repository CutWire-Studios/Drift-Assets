from _platforms import Platform, build_platform

# Simple Icons "tumblr" (CC0; the logo is a trademark of its owner), 24x24 box.
GLYPH = ("M14.563 24c-5.093 0-7.031-3.756-7.031-6.411V9.747H5.116V6.648c3.63-1.313 4.512-4.596 4.71-6.469C9.84"
         ".051 9.941 0 9.999 0h3.517v6.114h4.801v3.633h-4.82v7.47c.016 1.001.375 2.371 2.207 2.371h.09c.631-.0"
         "2 1.486-.205 1.936-.419l1.156 3.425c-.436.636-2.4 1.374-4.156 1.404h-.178l.011.002z")

build_platform(Platform(
    "follow-button-tumblr", "Tumblr", GLYPH,
    tile="#36465D", rim=True, glyph_size=0.52, primary="#00B8FF", glass_bg="3d5a80", tags=["blog"]))
