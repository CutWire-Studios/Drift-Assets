from _toggle import *

D = ("M12 3a9 9 0 1 0 9 9c0-.46-.04-.92-.1-1.36a5.389 5.389 0 0 1-4.4 2.26 5.403 5.403 0 0 1-3.14-9.8c-.44-.06-.9-.1-1.36-.1z")
build_toggle("do-not-disturb", "Do Not Disturb",
             "Do Not Disturb / focus mode toggle: a purple crescent-moon button that switches on, or the bare "
             "moon glyph popping in.",
             ["moon", "focus", "dnd", "sleep", "silent", "night", "control center", "toggle"],
             lambda s, x, y: fill_glyph(D, s, x, y), "#5E5CE6")
