from _toggle import *

D = ("M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z")
build_toggle("airplane-mode", "Airplane Mode",
             "Airplane mode toggle: an orange Control Center-style button that switches on, or the bare plane "
             "glyph popping in.",
             ["airplane", "flight", "travel", "offline", "status bar", "control center", "toggle"],
             lambda s, x, y: fill_glyph(D, s, x, y), "#FF9F0A")
