"""Static, slot-coloured OS status-bar glyphs drawn in canvas coordinates (used by status bars and phone frames)."""

from ui_kit import *


def cell_bars(x, base, h, slot="icon", n=4, filled=4):
    """n rising bars, total height h, ending at x + width. Returns (shapes, width)."""
    bw = h * 0.22
    gap = h * 0.12
    out = []
    for i in range(n):
        bh = h * (0.4 + 0.6 * i / (n - 1))
        out.append(group([rect_tl(x + i * (bw + gap), base - bh, bw, bh, bw * 0.3),
                          fill(slot=slot, opacity=100 if i < filled else 35)], f"cell{i}"))
    return out, n * bw + (n - 1) * gap


def wifi(cx, base, w, slot="icon"):
    """iOS-style fan: three bands + wedge; w = overall width. Returns (shapes, width)."""
    h = w * 0.72
    th = w * 0.13
    out = []
    for i, r in enumerate((w * 0.5 - th / 2, w * 0.34 - th / 2 + 0.0, w * 0.18 - th / 2)):
        out.append(group([arc_path(r, 225, 315, (cx, base)), stroke(slot=slot, width=th, cap="butt")], f"wifi{i}"))
    out.append(group([ellipse((th * 1.5, th * 1.5), (cx, base - th * 0.35)), fill(slot=slot)], "wifi-dot"))
    return out, w


def battery(x, y, w, h, level=0.8, slot="icon", pct=False):
    """iOS-style battery; (x, y) top-left. Returns (shapes, width incl. cap)."""
    pad = h * 0.12
    out = [
        group([rect_tl(x + w + h * 0.1, y + h * 0.33, h * 0.12, h * 0.34, h * 0.06), fill(slot=slot, opacity=45)], "cap"),
        group([rect_tl(x + pad, y + pad, (w - 2 * pad) * level, h - 2 * pad, h * 0.2), fill(slot=slot)], "level"),
        group([rect_tl(x, y, w, h, h * 0.3), stroke(slot=slot, width=max(h * 0.08, 1.5), opacity=45)], "tray"),
    ]
    return out, w + h * 0.22


def time_text(s, x, base, size, weight=600, anchor="l", slot="icon"):
    return label(s, x, base, size, weight, slot=slot, anchor=anchor, name="time")


# ---- line icons (stroke, slot-coloured), centred on (cx, cy) with half-size s -------------------

def _st(items, slot, w, opacity=100, name="icon"):
    return group(items + [stroke(slot=slot, width=w, opacity=opacity)], name)


def chevron(cx, cy, s, direction="left", slot="icon", w=3, opacity=100):
    d = -1 if direction == "left" else 1
    return _st([polyline([(cx - d * s * 0.5, cy - s), (cx + d * s * 0.5, cy), (cx - d * s * 0.5, cy + s)])], slot, w, opacity, "chevron")


def plus(cx, cy, s, slot="icon", w=3, opacity=100):
    return _st([polyline([(cx - s, cy), (cx + s, cy)]), polyline([(cx, cy - s), (cx, cy + s)])], slot, w, opacity, "plus")


def cross(cx, cy, s, slot="icon", w=3, opacity=100):
    return _st([polyline([(cx - s, cy - s), (cx + s, cy + s)]), polyline([(cx + s, cy - s), (cx - s, cy + s)])], slot, w, opacity, "x")


def minus(cx, cy, s, slot="icon", w=3, opacity=100):
    return _st([polyline([(cx - s, cy), (cx + s, cy)])], slot, w, opacity, "minus")


def square(cx, cy, s, slot="icon", w=3, r=0, opacity=100):
    return _st([rect((2 * s, 2 * s), (cx, cy), r)], slot, w, opacity, "square")


def dots3(cx, cy, gap, r, slot="icon", vertical=True, opacity=100):
    items = []
    for k in (-1, 0, 1):
        items.append(ellipse((2 * r, 2 * r), (cx, cy + k * gap) if vertical else (cx + k * gap, cy)))
    return group(items + [fill(slot=slot, opacity=opacity)], "dots")


def magnifier(cx, cy, s, slot="icon", w=3, opacity=100):
    return _st([ellipse((s * 1.5, s * 1.5), (cx - s * 0.15, cy - s * 0.15)),
                polyline([(cx + s * 0.55, cy + s * 0.55), (cx + s * 0.95, cy + s * 0.95)])], slot, w, opacity, "search")


def lock(cx, cy, s, slot="icon", w=2.5, opacity=100):
    return group([rect((s * 1.3, s * 0.95), (cx, cy + s * 0.3), s * 0.18), fill(slot=slot, opacity=opacity),
                  ], "lock-body"), _st([arc_path(s * 0.42, 180, 360, (cx, cy - s * 0.12)),
                                        polyline([(cx - s * 0.42, cy - s * 0.12), (cx - s * 0.42, cy + s * 0.05)]),
                                        polyline([(cx + s * 0.42, cy - s * 0.12), (cx + s * 0.42, cy + s * 0.05)])],
                                       slot, w, opacity, "lock-shackle")


def reload(cx, cy, s, slot="icon", w=3, opacity=100):
    return _st([arc_path(s, -60, 230, (cx, cy)),
                polyline([(cx + s * 0.5, cy - s * 1.15), (cx + s * 0.5 + s * 0.25, cy - s * 0.55), (cx - s * 0.1, cy - s * 0.55)])],
               slot, w, opacity, "reload")


def share(cx, cy, s, slot="icon", w=3, opacity=100):
    return _st([polyline([(cx - s * 0.6, cy - s * 0.1), (cx - s * 0.6, cy + s * 0.9), (cx + s * 0.6, cy + s * 0.9),
                          (cx + s * 0.6, cy - s * 0.1)]),
                polyline([(cx, cy + s * 0.5), (cx, cy - s * 0.9)]),
                polyline([(cx - s * 0.4, cy - s * 0.5), (cx, cy - s * 0.9), (cx + s * 0.4, cy - s * 0.5)])],
               slot, w, opacity, "share")


def star_icon(cx, cy, s, slot="icon", w=3, opacity=100):
    return group([star(5, s, s * 0.45, (cx, cy), -18), stroke(slot=slot, width=w, opacity=opacity, join="round")], "star")


def hamburger(cx, cy, s, slot="icon", w=3, opacity=100):
    return _st([polyline([(cx - s, cy + k * s * 0.7), (cx + s, cy + k * s * 0.7)]) for k in (-1, 0, 1)], slot, w, opacity, "menu")


# ---- filled glyphs (Material icon paths, Apache-2.0), 24-unit boxes -------------------------------

GLYPH = {
    "back": "M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z",
    "call": "M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z",
    "video": "M17 10.5V7c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-3.5l4 4v-11l-4 4z",
    "mic": "M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5.3-3c0 3-2.54 5.1-5.3 5.1S6.7 14 6.7 11H5c0 3.41 2.72 6.23 6 6.72V21h2v-3.28c3.28-.48 6-3.3 6-6.72h-1.7z",
    "camera": "M9 2L7.17 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2h-3.17L15 2H9zm3 15c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8.2c-1.77 0-3.2 1.43-3.2 3.2s1.43 3.2 3.2 3.2 3.2-1.43 3.2-3.2-1.43-3.2-3.2-3.2z",
    "clip": "M16.5 6v11.5c0 2.21-1.79 4-4 4s-4-1.79-4-4V5c0-1.38 1.12-2.5 2.5-2.5s2.5 1.12 2.5 2.5v10.5c0 .55-.45 1-1 1s-1-.45-1-1V6H10v9.5c0 1.38 1.12 2.5 2.5 2.5s2.5-1.12 2.5-2.5V5c0-2.21-1.79-4-4-4S7 2.79 7 5v12.5c0 3.04 2.46 5.5 5.5 5.5s5.5-2.46 5.5-5.5V6h-1.5z",
    "thumb": "M1 21h4V9H1v12zm22-11c0-1.1-.9-2-2-2h-6.31l.95-4.57.03-.32c0-.41-.17-.79-.44-1.06L14.17 1 7.59 7.59C7.22 7.95 7 8.45 7 9v10c0 1.1.9 2 2 2h9c.83 0 1.54-.5 1.84-1.22l3.02-7.05c.09-.23.14-.47.14-.73v-2z",
    "heart": "M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z",
    "send": "M2.01 21L23 12 2.01 3 2 10l15 2-15 2z",
    "image": "M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z",
    "info": "M11 7h2v2h-2zm0 4h2v6h-2zm1-9C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z",
    "play": "M8 5v14l11-7z",
    "pause": "M6 19h4V5H6v14zm8-14v14h4V5h-4z",
    "skip-next": "M6 18l8.5-6L6 6v12zM16 6v12h2V6h-2z",
    "skip-prev": "M6 6h2v12H6zm3.5 6l8.5 6V6z",
    "shuffle": "M10.59 9.17L5.41 4 4 5.41l5.17 5.17 1.42-1.41zM14.5 4l2.04 2.04L4 18.59 5.41 20 17.96 7.46 20 9.5V4h-5.5zm.33 9.41l-1.41 1.41 3.13 3.13L14.5 20H20v-5.5l-2.04 2.04-3.13-3.13z",
    "repeat": "M7 7h10v3l4-4-4-4v3H5v6h2V7zm10 10H7v-3l-4 4 4 4v-3h12v-6h-2v4z",
    "bookmark": "M17 3H7c-1.1 0-1.99.9-1.99 2L5 21l7-3 7 3V5c0-1.1-.9-2-2-2z",
    "comment": "M21.99 4c0-1.1-.89-2-1.99-2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14l4 4-.01-18z",
    "share": "M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92 1.61 0 2.92-1.31 2.92-2.92s-1.31-2.92-2.92-2.92z",
    "music": "M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z",
    "more": "M6 10c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm12 0c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm-6 0c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z",
    "repost": "M7 7h10v3l4-4-4-4v3H5v6h2V7zm10 10H7v-3l-4 4 4 4v-3h12v-6h-2v4z",
    "chart": "M5 9.2h3V19H5zM10.6 5h2.8v14h-2.8zm5.6 8H19v6h-2.8z",
    "volume": "M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z",
    "settings": "M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z",
    "fullscreen": "M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z",
    "plus-circle": "M13 7h-2v4H7v2h4v4h2v-4h4v-2h-4V7zm-1-5C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z",
    "emoji": "M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm3.5-9c.83 0 1.5-.67 1.5-1.5S16.33 8 15.5 8 14 8.67 14 9.5s.67 1.5 1.5 1.5zm-7 0c.83 0 1.5-.67 1.5-1.5S9.33 8 8.5 8 7 8.67 7 9.5 7.67 11 8.5 11zm3.5 6.5c2.33 0 4.31-1.46 5.11-3.5H6.89c.8 2.04 2.78 3.5 5.11 3.5z",
}


def glyph(name, size, cx, cy, slot="icon", opacity=100, color=None, rotation=0):
    """Filled Material-style glyph centred on (cx, cy), `size` px square."""
    s = size / 24
    shapes = svg_shapes(GLYPH[name], s, (cx - 12 * s, cy - 12 * s), name)
    f = fill(color, opacity) if color else fill(slot=slot, opacity=opacity)
    return group(shapes + [f], name, anchor=(cx, cy), position=(cx, cy), rotation=rotation)
