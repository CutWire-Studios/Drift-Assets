from _toggle import *

BELL = ("M12 22c1.1 0 2-.9 2-2h-4c0 1.1.89 2 2 2zm6-6v-5c0-3.07-1.64-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68"
        "C7.63 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z")


def glyph(s, x, y):
    k = s / 24
    slash = group([polyline([(x + (3.5 - 12) * k, y + (3.5 - 12) * k), (x + (21 - 12) * k, y + (21 - 12) * k)]),
                   stroke(slot="primary", width=4.6 * k)], "gap")
    return [group([polyline([(x + (3.5 - 12) * k, y + (3.5 - 12) * k), (x + (21 - 12) * k, y + (21 - 12) * k)]),
                   stroke(slot="icon", width=2 * k)], "slash")] + fill_glyph(BELL, s, x, y)


build_toggle("mute-bell", "Mute Notifications",
             "Muted notification bell with a slash: a red Control Center-style button, or the bare crossed-out "
             "bell popping in.",
             ["mute", "silent", "bell", "notifications off", "ringer", "toggle", "control center"],
             glyph, "#FF3B30")
