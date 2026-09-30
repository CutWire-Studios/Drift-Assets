from _broadcast2 import *

W, H = 1920, 1080
F = 120   # each of the four tiles speaks for one second
SEG = F // 4


def tiles(m=36, g=20, bottom=36):
    tw, th = (W - 2 * m - g) / 2, (H - m - bottom - g) / 2
    return [(m + (i % 2) * (tw + g), m + (i // 2) * (th + g), tw, th) for i in range(4)]


def speaking(i, on=100, off=0, fade_f=4):
    """Opacity that is `on` while tile i speaks (tile 0 speaks at the loop seam, so it wraps)."""
    t0, t1 = i * SEG, (i + 1) * SEG
    if i == 0:
        return keys((0, on, HOLD), (t1 - fade_f, on, EASE_IN_OUT), (t1, off, HOLD), (F - fade_f, off, EASE_IN_OUT),
                    (F, on))
    return keys((0, off, HOLD), (t0 - fade_f, off, EASE_IN_OUT), (t0, on, HOLD), (t1 - fade_f, on, EASE_IN_OUT),
                (t1, off, HOLD), (F, off))


def level_bars(x, y, slot, i, s=1.0):
    """Three little voice-level bars bouncing next to the name, only visible while speaking."""
    out = []
    for k in range(3):
        vals = [[100, v] for v in ((30, 100, 55, 85, 40, 95), (80, 35, 100, 50, 90, 30), (45, 90, 30, 100, 60, 70))[k]]
        out.append(group([polyline([(0, -14 * s), (0, 14 * s)]), stroke(slot=slot, width=6 * s)], f"lv{k}",
                         position=(x + k * 11 * s, y), scale=wave_keys(F, vals * 5, EASE_IN_OUT)))
    return out


def muted_mic(c, s, slot="accent"):
    cap, rest = mic_shapes(s, *c)
    return [group([polyline([(c[0] - 26 * s, c[1] - 44 * s), (c[0] + 26 * s, c[1] + 30 * s)]),
                   stroke(slot=slot, width=7 * s)], "slash"),
            group([cap] + rest + [stroke(slot=slot, width=6 * s)], "mic")]


def name_tag(comp, i, t, slot_bg, style="modern"):
    x, y, w, h = t
    ph = 58
    px, py = x + 20, y + h - 20 - ph
    mic_c = (px + 34, py + ph / 2 + 3)
    if i == 2:
        mic = muted_mic(mic_c, 0.34)
    else:
        mic = mic_icon(0.34, *mic_c, slot="icon", width=4.5)
    shapes = mic
    if style != "minimal":
        shapes += [group([rect_tl(px, py, 360, ph, ph / 2), fill(slot=slot_bg, opacity=70)], "pill")]
    if i != 2:
        comp.layer(f"level{i}", level_bars(px + 324, py + ph / 2, "primary", i, 0.9), opacity=speaking(i))
    comp.layer(f"tag{i}", shapes)
    return (round(px + 64), round(py + 8), 236, ph - 16)


def modern():
    """Video-call app chrome: rounded tiles on a dark surround, name pills, toolbar and a green speaker ring."""
    comp = Comp("video-call-grid-frame", W, H, fps=30, frames=F)
    comp.slot("primary", "#35D07F")
    comp.slot("background", "#1B1C22")
    comp.slot("icon", "#FFFFFF")
    comp.slot("accent", "#FF4D4D")
    ts = tiles(bottom=140)
    areas = {}
    for i, t in enumerate(ts):
        areas[f"name{i + 1}"] = name_tag(comp, i, t, "background")
        r = rect_tl(*t, 24)
        comp.layer(f"ring{i}", [group([r, stroke(slot="primary", width=8)], "ring"),
                                group([r, stroke(slot="primary", width=26, opacity=18)], "glow")],
                   opacity=speaking(i))
    # toolbar
    ty = H - 70
    btn = []
    for k, x in enumerate((W / 2 - 250, W / 2 - 130, W / 2 - 10)):
        btn.append(group([ellipse((84, 84), (x, ty)), fill("#FFFFFF", 14)], f"btn{k}"))
    btn += mic_icon(0.42, W / 2 - 250, ty + 4, slot="icon", width=3)
    btn += [group([rect_tl(W / 2 - 130 - 22, ty - 14, 30, 28, 5), polyline([(W / 2 - 130 + 8, ty - 4),
                                                                             (W / 2 - 130 + 22, ty - 12),
                                                                             (W / 2 - 130 + 22, ty + 12),
                                                                             (W / 2 - 130 + 8, ty + 4)], closed=True),
                   fill(slot="icon")], "cam"),
            group([rect_tl(W / 2 - 10 - 22, ty - 16, 44, 30, 4), stroke(slot="icon", width=4)], "share"),
            group([polyline([(W / 2 - 10, ty + 6), (W / 2 - 10, ty - 8)]), polyline([(W / 2 - 18, ty), (W / 2 - 10, ty - 8),
                                                                                    (W / 2 - 2, ty)]),
                   stroke(slot="icon", width=4)], "arrow"),
            group([path(arc(26, 200, 340, (W / 2 + 180, ty + 18))), stroke(slot="icon", width=9)], "handset"),
            group([rect((150, 76), (W / 2 + 180, ty), 38), fill(slot="accent")], "end")]
    comp.layer("toolbar", btn)
    comp.layer("surround", [group([rect((W + 4, H + 4), (W / 2, H / 2))] + [rect_tl(*t, 24) for t in ts] +
                                  [fill(slot="background", even_odd=True)], "bg")])
    return comp, areas


def minimal():
    """No chrome: thin outlines around four tiles, small mic icons, and a thick ring that jumps to the speaker."""
    comp = Comp("video-call-grid-frame--minimal", W, H, fps=30, frames=F)
    comp.slot("primary", "#FFFFFF")
    comp.slot("icon", "#FFFFFF")
    comp.slot("accent", "#FF4D4D")
    comp.slot("outline", "#FFFFFF")
    ts = tiles(m=40, g=16, bottom=40)
    areas = {}
    for i, t in enumerate(ts):
        areas[f"name{i + 1}"] = name_tag(comp, i, t, None, "minimal")
        r = rect_tl(*t, 14)
        comp.layer(f"ring{i}", [group([r, stroke(slot="primary", width=10)], "ring")], opacity=speaking(i))
        comp.layer(f"edge{i}", [group([r, stroke(slot="outline", width=3, opacity=60)], "edge")])
    comp.layer("tags shade", [group([rect_tl(t[0], t[1] + t[3] - 110, t[2], 110, 14), gradient_fill(
        [(0, "#000000", 0), (1, "#000000", 0.45)], (0, t[1] + t[3] - 110), (0, t[1] + t[3]))], f"sh{i}")
        for i, t in enumerate(ts)])
    return comp, areas


def neon():
    """Neon grid: dim glowing tile outlines, the active speaker's tile lights up and pulses."""
    comp = Comp("video-call-grid-frame--neon", W, H, fps=30, frames=F)
    comp.slot("primary", "#3DF2FF")
    comp.slot("secondary", "#B04DFF")
    comp.slot("background", "#0C0A14")
    comp.slot("icon", "#FFFFFF")
    comp.slot("accent", "#FF3D7A")
    ts = tiles(m=44, g=28, bottom=44)
    areas = {}
    pulse = wave_keys(F, [100, 65] * 8)
    for i, t in enumerate(ts):
        areas[f"name{i + 1}"] = name_tag(comp, i, t, "background", "neon")
        r = rect_tl(*t, 30)
        comp.layer(f"lit{i}", glow_strokes([r], slot="primary", width=7), opacity=speaking(i))
        comp.layer(f"lit pulse{i}", [group([r, stroke(slot="primary", width=60, opacity=10)], "wide", opacity=pulse)],
                   opacity=speaking(i))
        comp.layer(f"dim{i}", glow_strokes([r], slot="secondary", width=4, core=False, widths=(16,), ops=(18,)))
    comp.layer("surround", [group([rect((W + 4, H + 4), (W / 2, H / 2))] + [rect_tl(*t, 30) for t in ts] +
                                  [fill(slot="background", even_odd=True, opacity=80)], "bg")])
    return comp, areas


m, ma = modern()
mi, mia = minimal()
n, na = neon()
build_asset(CAT, "video-call-grid-frame", "Video Call Grid Frame",
            "Full-frame 2x2 video-call overlay with transparent tiles: name tags with mic icons and a speaking "
            "ring that moves from tile to tile. Put four clips under the tiles and the names in name1-4.",
            ["video call", "zoom", "meeting", "grid", "webcam", "call", "interview", "overlay"], [
    V("modern", "App Chrome", m, "loop", text_area=ma["name1"], text_areas=ma, thumb_t=0.1, bg="7a8499",
      description="Rounded tiles on a dark surround with name pills, a call toolbar and a green speaker ring."),
    V("minimal", "Minimal", mi, "loop", text_area=mia["name1"], text_areas=mia, thumb_t=0.35, bg="7a8499",
      description="No chrome: thin outlines, small mic icons and a thick ring that jumps to the speaker."),
    V("neon", "Neon", n, "loop", text_area=na["name1"], text_areas=na, thumb_t=0.6, bg="7a8499",
      description="Dim neon tile outlines; the speaker's tile lights up in a second colour and pulses."),
])
