from _platforms import Platform, build_platform

# Simple Icons "linktree" (CC0; the logo is a trademark of its owner), 24x24 box.
GLYPH = ("m13.73635 5.85251 4.00467-4.11665 2.3248 2.3808-4.20064 4.00466h5.9085v3.30473h-5.9365l4.22865 4.107"
         "66-2.3248 2.3338L12.0005 12.099l-5.74052 5.76852-2.3248-2.3248 4.22864-4.10766h-5.9375V8.12132h5.908"
         "5L3.93417 4.11666l2.3248-2.3808 4.00468 4.11665V0h3.4727zm-3.4727 10.30614h3.4727V24h-3.4727z")

build_platform(Platform(
    "follow-button-linktree", "Linktree", GLYPH,
    tile="#43E55E", glyph_color="#000000", glyph_size=0.56, primary="#43E55E", badge_icon="#000000",
    done="#1E2330", second="outline", tags=["link", "bio"]))
