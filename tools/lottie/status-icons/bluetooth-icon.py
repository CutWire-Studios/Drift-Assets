from _toggle import *

pts = [(7, 7), (17, 17), (12, 22), (12, 2), (17, 7), (7, 17)]
build_toggle("bluetooth-icon", "Bluetooth Icon",
             "Bluetooth rune that switches on: a Control Center-style button that turns blue, or the bare glyph "
             "popping in with a ring.",
             ["bluetooth", "wireless", "connect", "pairing", "status bar", "control center", "toggle"],
             lambda s, x, y: stroke_glyph(pts, s, x, y, 2.1), "#0A84FF")
