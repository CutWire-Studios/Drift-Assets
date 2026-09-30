from _broadcast2 import *

W, H = 1080, 1920
F = 150           # 5 s: the active segment fills over the whole clip
IN = 14
TOP_IN = keys((0, [0, -40], EXPO_OUT), (IN, [0, 0]))
BOT_IN = keys((2, [0, 60], EXPO_OUT), (IN + 2, [0, 0]))
SEG_Y, SEG_H = 36, 7
AV = (86, 128)
REPLY = (36, 1752, 820, 108)
RING = [(0, "#FEDA75"), (0.3, "#FA7E1E"), (0.6, "#D62976"), (1, "#962FBF")]


def segments(n=4, x0=24, x1=W - 24, gap=10):
    w = (x1 - x0 - gap * (n - 1)) / n
    return [(x0 + i * (w + gap), w) for i in range(n)]


def grow(x, y, w, h, t0, t1, r):
    return rect(keys((t0, [0, h], LINEAR), (t1, [w, h])), keys((t0, [x, y + h / 2], LINEAR), (t1, [x + w / 2, y + h / 2])),
                r)


def scrims(comp):
    comp.layer("top scrim", [group([rect_tl(0, 0, W, 330), gradient_fill(
        [(0, "#000000", 0.5), (1, "#000000", 0)], (0, 0), (0, 330))], "top")], opacity=fade(0, IN))
    comp.layer("bottom scrim", [group([rect_tl(0, H - 420, W, 420), gradient_fill(
        [(0, "#000000", 0), (1, "#000000", 0.55)], (0, H - 420), (0, H))], "bottom")], opacity=fade(0, IN))


def top_icons(slot):
    dots = [group([ellipse((11, 11), (910 + i * 17, AV[1])), fill(slot=slot)], f"dot{i}") for i in range(3)]
    x = [group([polyline([(994, AV[1] - 17), (1028, AV[1] + 17)]), polyline([(1028, AV[1] - 17), (994, AV[1] + 17)]),
                stroke(slot=slot, width=6)], "close")]
    return dots + x


def bottom_icons(slot, width=6):
    return [group(icon(HEART, 70, (928, REPLY[1] + REPLY[3] / 2)) + [stroke(slot=slot, width=width)], "heart"),
            group(icon(SEND, 62, (1022, REPLY[1] + REPLY[3] / 2)) + [stroke(slot=slot, width=width)], "send")]


AREAS = {"name": (AV[0] + 68, AV[1] - 30, 560, 60), "reply": (REPLY[0] + 50, REPLY[1] + 24, REPLY[2] - 100, 60)}


def modern():
    """Instagram-style story UI: segmented progress, gradient avatar ring, outlined reply pill and icons."""
    comp = Comp("phone-story-frame", W, H, fps=30, frames=F)
    comp.slot("icon", "#FFFFFF")
    comp.slot("secondary", "#9AA0B4")
    segs = segments()
    top = []
    for i, (x, w) in enumerate(segs):
        if i == 0:
            top.append(group([rect_tl(x, SEG_Y, w, SEG_H, 4), fill(slot="icon")], "done"))
        if i == 1:
            top.append(group([grow(x, SEG_Y, w, SEG_H, 0, F, 4), fill(slot="icon")], "active"))
        top.append(group([rect_tl(x, SEG_Y, w, SEG_H, 4), fill(slot="icon", opacity=35)], f"seg{i}"))
    top += top_icons("icon")
    top += [group([ellipse((96, 96), AV), fill(slot="secondary")], "avatar"),
            group([ellipse((104, 104), AV), fill("#000000", 30)], "gap"),
            group([ellipse((114, 114), AV), gradient_fill(RING, (AV[0] - 57, AV[1] + 57), (AV[0] + 57, AV[1] - 57))],
                  "ring")]
    lay(comp, "top", top, off=TOP_IN, opacity=fade(0, 8))
    lay(comp, "bottom", bottom_icons("icon") + [
        group([rect_tl(*REPLY, REPLY[3] / 2), stroke(slot="icon", width=4, opacity=90)], "reply")],
        off=BOT_IN, opacity=fade(2, 10))
    scrims(comp)
    return comp


def minimal():
    """Clean story UI: one continuous hairline progress bar, small avatar and a frosted reply bar."""
    comp = Comp("phone-story-frame--minimal", W, H, fps=30, frames=F)
    comp.slot("icon", "#FFFFFF")
    comp.slot("secondary", "#C8CCD8")
    x0, x1 = 24, W - 24
    top = [group([grow(x0, SEG_Y, x1 - x0, 5, 0, F, 3), fill(slot="icon")], "progress"),
           group([rect_tl(x0, SEG_Y, x1 - x0, 5, 3), fill(slot="icon", opacity=28)], "track")]
    top += top_icons("icon")
    top += [group([ellipse((88, 88), AV), fill(slot="secondary")], "avatar"),
            group([ellipse((96, 96), AV), fill(slot="icon")], "rim")]
    lay(comp, "top", top, off=TOP_IN, opacity=fade(0, 8))
    cam = (REPLY[0] + 60, REPLY[1] + REPLY[3] / 2)
    bottom = [group([rect_tl(cam[0] - 20, cam[1] - 14, 40, 30, 6), stroke(slot="icon", width=5)], "cam"),
              group([ellipse((14, 14), (cam[0], cam[1] + 1)), stroke(slot="icon", width=4)], "lens"),
              group([rect_tl(cam[0] - 8, cam[1] - 20, 16, 8, 2), fill(slot="icon")], "top"),
              group([ellipse((84, 84), cam), fill(slot="icon", opacity=22)], "cam bg"),
              group([rect_tl(*REPLY, 30), fill(slot="icon", opacity=20)], "reply")]
    bottom += bottom_icons("icon")
    lay(comp, "bottom", bottom, off=BOT_IN, opacity=fade(2, 10))
    scrims(comp)
    return comp


def neon():
    """Glowing story UI: neon progress segments, pulsing neon avatar ring and a neon reply bar."""
    comp = Comp("phone-story-frame--neon", W, H, fps=30, frames=F)
    comp.slot("primary", "#FF3FD2")
    comp.slot("secondary", "#3FE7FF")
    segs = segments()
    y = SEG_Y + SEG_H / 2
    top = []
    for i, (x, w) in enumerate(segs):
        line = polyline([(x + 4, y), (x + w - 4, y)])
        if i == 0:
            top += glow_strokes([line], slot="secondary", width=6, widths=(22, 12), ops=(10, 22))
        if i == 1:
            top += glow_strokes([line], slot="secondary", width=6, widths=(22, 12), ops=(10, 22),
                                extra=[trim(end=keys((0, 0, LINEAR), (F, 100)))])
        top.append(group([line, stroke(slot="secondary", width=6, opacity=22)], f"seg{i}"))
    top += [group([ellipse((96, 96), AV), fill("#1A1030", 80)], "avatar")]
    lay(comp, "top", top, off=TOP_IN, opacity=fade(0, 8))
    pulse = wave_keys(F // 5 * 5, [100, 60] * 5)
    lay(comp, "ring", glow_strokes([ellipse((108, 108), AV)], slot="primary", width=6), off=TOP_IN,
        opacity=pulse)
    lay(comp, "top icons", glow_strokes([polyline([(994, AV[1] - 17), (1028, AV[1] + 17)]),
                      polyline([(1028, AV[1] - 17), (994, AV[1] + 17)])], slot="secondary", width=5, core=False,
                     widths=(16,), ops=(18,)), off=TOP_IN, opacity=fade(0, 8))
    reply = rect_tl(*REPLY, REPLY[3] / 2)
    lay(comp, "bottom", glow_strokes([reply], slot="primary", width=5) +
        glow_strokes(icon(HEART, 70, (928, REPLY[1] + REPLY[3] / 2)), slot="secondary", width=5, core=False,
                     widths=(18,), ops=(20,)) +
        glow_strokes(icon(SEND, 62, (1022, REPLY[1] + REPLY[3] / 2)), slot="secondary", width=5, core=False,
                     widths=(18,), ops=(20,)) +
        [group([reply, fill("#12081F", 45)], "reply tint")], off=BOT_IN, opacity=fade(2, 10))
    scrims(comp)
    return comp


build_asset(CAT, "phone-story-frame", "Phone Story Frame",
            "Full-screen vertical story overlay: animated progress segments, an avatar circle and a reply bar "
            "around a transparent centre. Add the account name next to the avatar and a reply prompt in the bar.",
            ["story", "instagram", "vertical", "phone", "frame", "social", "progress", "overlay"], [
    V("modern", "Classic Story", modern(), "intro-hold", text_area=AREAS["name"], text_areas=AREAS,
            thumb_t=0.5, bg="56607a",
            description="Segmented progress, gradient avatar ring, outlined reply pill with heart and send icons."),
    V("minimal", "Minimal", minimal(), "intro-hold", text_area=AREAS["name"], text_areas=AREAS, thumb_t=0.5,
            bg="56607a",
            description="One continuous hairline progress bar, small avatar and a frosted reply bar with a camera button."),
    V("neon", "Neon", neon(), "intro-hold", text_area=AREAS["name"], text_areas=AREAS, thumb_t=0.5,
            bg="1a1428",
            description="Glowing progress segments, a pulsing neon avatar ring and a neon reply bar."),
])
