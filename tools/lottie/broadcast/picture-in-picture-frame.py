from _broadcast2 import *

W, H = 820, 540
F = 90
INTRO, OUTRO = 20, 74
FW, FH = 640, 360
X0, Y0 = 100, 76
PIV = (X0 + FW, Y0 + FH)  # corner the window grows from (bottom-right)
WIN = rect_tl(X0, Y0, FW, FH, 28)


def base(name):
    c = Comp(name, W, H, fps=30, frames=F)
    c.marker("intro", 0, INTRO)
    c.marker("outro", OUTRO, F - OUTRO)
    return c


def corner_pop(t0=0):
    return keys((t0, [0, 0], OVERSHOOT), (t0 + 18, [100, 100], HOLD), (OUTRO, [100, 100], BACK_IN), (OUTRO + 12, [0, 0]))


def shadow(parent, comp, shape, opacity=100):
    """Soft drop shadow outside the frame only (strokes), so the window stays see-through."""
    comp.layer("shadow", [group([shape, stroke("#000000", width=w, opacity=o)], f"s{w}", position=(0, 8))
                          for w, o in ((12, 22), (26, 10), (44, 5))], parent=parent, opacity=opacity)


def modern():
    """Rounded white-bordered window pops out of the bottom-right corner with a name pill on its edge."""
    comp = base("picture-in-picture-frame")
    comp.slot("outline", "#FFFFFF")
    comp.slot("primary", "#FF3D6E")
    win = rig(comp, "window", PIV, scale=corner_pop())
    pill = (X0 + 24, Y0 + FH - 30, 300, 64)
    comp.layer("pill", [group([rect_tl(*pill, 32), fill(slot="primary")], "pill"),
                        group([rect_tl(pill[0], pill[1] + 5, pill[2], pill[3], 32), fill("#000000", 22)], "sh")],
               parent=win, anchor=(pill[0], pill[1] + 32), position=(pill[0], pill[1] + 32),
               scale=keys((8, [0, 100], EXPO_OUT), (22, [100, 100], HOLD), (OUTRO - 4, [100, 100], EXPO_IN),
                          (OUTRO + 4, [0, 100])))
    comp.layer("border", [group([WIN, stroke(slot="outline", width=9)], "b")], parent=win)
    shadow(win, comp, WIN)
    return comp, (pill[0] + 26, pill[1] + 10, pill[2] - 52, pill[3] - 20)


def neon():
    """Glowing neon window frame with bright corner accents, flickering on as it pops from the corner."""
    comp = base("picture-in-picture-frame--neon")
    comp.slot("primary", "#35F0FF")
    comp.slot("accent", "#FF3DD8")
    win = rig(comp, "window", PIV, scale=corner_pop())
    flick = keys((0, 100, HOLD), (5, 30, HOLD), (7, 100, HOLD), (10, 50, HOLD), (12, 100, HOLD), (F, 100))
    x1, y1 = X0 + FW, Y0 + FH
    comp.layer("corners", glow_strokes(corners(X0 - 14, Y0 - 14, x1 + 14, y1 + 14, 70), slot="accent", width=6,
                                       widths=(20, 12), ops=(12, 24)), parent=win, opacity=flick)
    pill = (X0 + 30, Y0 + FH - 34, 280, 60)
    comp.layer("pill", glow_strokes([rect_tl(*pill, 30)], slot="accent", width=4, core=False, widths=(16,), ops=(22,))
               + [group([rect_tl(*pill, 30), fill("#0E0716", 90)], "fill")], parent=win,
               opacity=keys((0, 0, HOLD), (14, 0, HOLD), (15, 100, HOLD), (17, 30, HOLD), (19, 100, HOLD), (F, 100)))
    comp.layer("frame", glow_strokes([WIN], slot="primary", width=7), parent=win, opacity=flick)
    return comp, (pill[0] + 26, pill[1] + 10, pill[2] - 52, pill[3] - 20)


def window():
    """Desktop-app style window: square frame with a coloured title bar and control dots, sliding from the corner."""
    comp = base("picture-in-picture-frame--window")
    comp.slot("primary", "#2B2F3A")
    comp.slot("outline", "#2B2F3A")
    comp.slot("icon", "#FFFFFF")
    bar = 56
    top = Y0 - 10
    win = rig(comp, "window", PIV, scale=keys((0, [30, 30], EXPO_OUT), (16, [100, 100], HOLD), (OUTRO, [100, 100],
                                                                                                 EXPO_IN),
                                               (OUTRO + 12, [30, 30])),
              off=keys((0, [60, 40], EXPO_OUT), (16, [0, 0], HOLD), (OUTRO, [0, 0], EXPO_IN), (OUTRO + 12, [60, 40])))
    dots = [group([ellipse((18, 18), (X0 + FW - 30 - i * 30, top + bar / 2)), fill(c)], f"d{i}")
            for i, c in enumerate(("#FF5F57", "#FEBC2E", "#28C840"))]
    comp.layer("chrome", dots + [
        group([rect_tl(X0, top + bar - 2, FW, 2), fill("#000000", 30)], "line"),
        group([path(bezier([(X0, top + bar), (X0, top + 14), (X0 + 14, top), (X0 + FW - 14, top), (X0 + FW, top + 14),
                            (X0 + FW, top + bar)],
                           [(0, 0), (0, 0), (-7.7, 0), (0, 0), (0, -7.7), (0, 0)],
                           [(0, 0), (0, -7.7), (0, 0), (7.7, 0), (0, 0), (0, 0)])), fill(slot="primary")], "bar")],
        parent=win, opacity=fade(0, 6, OUTRO + 6, OUTRO + 12))
    frame = rect_tl(X0, top + bar, FW, FH - bar + 10)
    comp.layer("frame", [group([frame, stroke(slot="outline", width=8, join="miter")], "f")], parent=win,
               opacity=fade(0, 6, OUTRO + 6, OUTRO + 12))
    shadow(win, comp, rect_tl(X0, top, FW, FH + 10, 14), opacity=fade(0, 6, OUTRO + 6, OUTRO + 12))
    return comp, (X0 + 24, top + 10, FW - 160, bar - 20)


m, mt = modern()
n, nt = neon()
w, wt = window()
build_asset(CAT, "picture-in-picture-frame", "Picture In Picture Frame",
            "Picture-in-picture window frame with a transparent inside that pops out from its corner, holds "
            "(stretchable) and tucks away. Place your second video inside and a name in the label.",
            ["picture in picture", "pip", "frame", "window", "webcam", "facecam", "reaction", "border"], [
    V("modern", "Rounded", m, "intro-hold-outro", text_area=mt, thumb_t=0.5, bg="56607a",
      description="Rounded white-bordered window with a soft shadow and a colour name pill on its edge."),
    V("neon", "Neon", n, "intro-hold-outro", text_area=nt, thumb_t=0.5, bg="1b1528",
      description="Glowing neon frame with bright corner accents that flickers on as it pops."),
    V("window", "App Window", w, "intro-hold-outro", text_area=wt, thumb_t=0.5, bg="56607a",
      description="Desktop-app style window with a title bar and control dots, sliding out from the corner."),
])
