"""Full-frame "yep, that's me" freeze frame: white flash, faded tint wash and a scratching vinyl record."""

from _memes2 import *

W, H = 1920, 1080
C = (W / 2, H / 2)
F, IN, OUT = 90, 24, 70


def record(R, label_slot="primary"):
    """Vinyl record centred on (0, 0) with radius R: grooves, sheen, label and spindle hole."""
    grooves = [ellipse((2 * R * f, 2 * R * f)) for f in (0.9, 0.8, 0.7, 0.6, 0.5)]
    sheen = [path(bezier([(0, 0), (R * math.cos(a0), R * math.sin(a0)), (R * math.cos(a1), R * math.sin(a1))]),
                  "sheen") for a0, a1 in ((-1.25, -0.85), (1.9, 2.3))]
    return [
        group([ellipse((R * 0.1, R * 0.1)), fill("#141414")], "hole"),
        group([ellipse((R * 0.2, R * 0.2), (R * 0.1, -R * 0.1)), fill("#FFFFFF", 45)], "label-hi"),
        group([ellipse((R * 0.62, R * 0.62)), fill(slot=label_slot)], "label"),
        group([ellipse((R * 0.62, R * 0.62)), stroke("#000000", width=R * 0.04, opacity=40)], "label-edge"),
        group(sheen + [fill("#FFFFFF", 16)], "sheen"),
        group(grooves + [stroke("#3A3A40", width=max(2, R * 0.012))], "grooves"),
        group([ellipse((2 * R, 2 * R)), fill("#16161A")], "disc"),
        group([ellipse((2 * R + R * 0.06, 2 * R + R * 0.06)), fill("#000000", 30)], "rim"),
    ]


def scratch_rot(t0):
    """Back-and-forth scratch rotation that settles."""
    return keys((0, 0, HOLD), (t0, 0, EASE_OUT), (t0 + 3, -55, EASE_IN_OUT), (t0 + 7, 30, EASE_IN_OUT),
                (t0 + 10, -40, EASE_IN_OUT), (t0 + 14, 18, EASE_IN_OUT), (t0 + 17, -12, EASE_IN_OUT),
                (t0 + 22, 0, HOLD), (F, 0))


def scratch_marks(comp, center, R, t0, slot="icon", side=1):
    """Little zigzag scratch squiggles that pop out beside the record."""
    for i, (a, s) in enumerate(((-40, 1.0), (0, 1.2), (40, 1.0))):
        ang = math.radians(a) if side > 0 else math.radians(180 - a)
        p = (center[0] + math.cos(ang) * R * 1.35, center[1] + math.sin(ang) * R * 1.35)
        z = [(-24 * s, 0), (-12 * s, -12 * s), (0, 0), (12 * s, -12 * s), (24 * s, 0)]
        comp.layer(f"scratch{i}", [group([polyline(z), stroke(slot=slot, width=8)], "z")],
                   position=p, rotation=a if side > 0 else -a,
                   scale=keys((t0 + 2 + i * 2, [0, 0], SPRING), (t0 + 10 + i * 2, [100, 100], HOLD),
                              (t0 + 20 + i, [100, 100], BACK_IN), (t0 + 26 + i, [0, 0])),
                   ip=t0 + 2 + i * 2, op=t0 + 27 + i)


def record_rig(comp, center, R, t0, pop_t=4, end=None):
    end = end or F
    rg = comp.null("record-rig", position=center,
                   scale=keys((pop_t, [0, 0], SPRING), (pop_t + 12, [100, 100], HOLD), (OUT, [100, 100], BACK_IN),
                              (OUT + 10, [0, 0])))
    arm = [group([polyline([(R * 1.02, -R * 0.95), (R * 0.95, -R * 0.1), (R * 0.45, R * 0.18)]),
                  stroke("#D8D8DE", width=R * 0.07)], "arm"),
           group([rect((R * 0.18, R * 0.28), (R * 0.45, R * 0.2), R * 0.03), fill("#D8D8DE")], "head"),
           group([ellipse((R * 0.3, R * 0.3), (R * 1.02, -R * 0.95)), fill("#B8B8C0")], "pivot")]
    comp.layer("arm", arm, parent=rg, anchor=(R * 1.02, -R * 0.95), position=(R * 1.02, -R * 0.95),
               rotation=keys((0, 0, HOLD), (t0, 0, EASE_OUT), (t0 + 3, 4, EASE_IN_OUT), (t0 + 10, -3, EASE_IN_OUT),
                             (t0 + 22, 0)))
    comp.layer("record", record(R), parent=rg, rotation=scratch_rot(t0))
    return rg


def flash(comp, strength=92):
    comp.layer("flash", [group([rect((W, H), C), fill("#FFFFFF")], "f")],
               opacity=keys((0, strength, EASE_OUT), (9, 0)), op=10)


def wash(comp, slot, color, op, extra=(), tint=100):
    comp.layer("wash", [group([rect((W, H), C), fill(color, tint, slot=slot)], "tint")] + list(extra),
               opacity=keys((0, 0, EASE_OUT), (6, op, HOLD), (OUT, op, EASE_IN), (F, 0)))


def classic():
    """Flash, warm sepia wash with soft vignette and a vinyl record scratching in the corner."""
    comp = base("record-scratch-freeze", W, H, F, IN, OUT)
    comp.slot("primary", "#E8433A")
    comp.slot("icon", "#FFFFFF")
    comp.slot("secondary", "#6E4A22")
    flash(comp)
    R = 200
    pos = (W - 290, H - 270)
    scratch_marks(comp, pos, R, 6, side=-1)
    record_rig(comp, pos, R, 6)
    comp.layer("record-shadow", [group([ellipse((2 * R, 2 * R)), fill("#000000", 35)], "s")],
               position=(pos[0] + 10, pos[1] + 16),
               scale=keys((4, [0, 0], SPRING), (16, [100, 100], HOLD), (OUT, [100, 100], BACK_IN), (OUT + 10, [0, 0])))
    wash(comp, "secondary", "#6E4A22", 100, [vignette(W, H, 0.55, 0.4)], tint=38)
    return comp


def letterbox():
    """Black cinema bars slam in over a cool grey wash; the record scratches in the bottom bar."""
    comp = base("record-scratch-freeze--letterbox", W, H, F, IN, OUT)
    comp.slot("primary", "#2F8CFF")
    comp.slot("background", "#07070A")
    comp.slot("secondary", "#5A6272")
    flash(comp, 85)
    BAR = 150
    R = 124
    pos = (190, H - BAR / 2 - 40)
    record_rig(comp, pos, R, 8)
    for i, (y0, y1) in enumerate(((-BAR / 2, BAR / 2), (H + BAR / 2, H - BAR / 2))):
        comp.layer(f"bar{i}", [group([rect((W + 20, BAR), (W / 2, 0)), fill(slot="background")], "bar")],
                   position=keys((0, [0, y0], EXPO_OUT), (8, [0, y1], HOLD), (OUT, [0, y1], EASE_IN), (F, [0, y0])))
    comp.layer("wash", [group([rect((W, H), C), fill(slot="secondary")], "tint")],
               opacity=keys((0, 0, EASE_OUT), (6, 42, HOLD), (OUT, 42, EASE_IN), (F, 0)))
    return comp, (380, H - BAR + 40, W - 700, BAR - 80)


def polaroid():
    """A thick instant-photo border snaps in with a tilt over a faded wash; the record sits on it like a sticker."""
    comp = base("record-scratch-freeze--polaroid", W, H, F, IN, OUT)
    comp.slot("primary", "#FFC23D")
    comp.slot("outline", "#F6F2E8")
    comp.slot("secondary", "#C9A77A")
    flash(comp)
    M, BOT = 70, 190
    inner = (W - 2 * M, H - M - BOT)
    icen = (W / 2, M + inner[1] / 2)
    tilt = keys((0, -5, EXPO_OUT), (12, 1.2, EASE_IN_OUT), (22, -1.5, HOLD), (OUT, -1.5, EASE_IN), (F, -4))
    sc = keys((0, [118, 118], EXPO_OUT), (12, [100, 100], HOLD), (OUT, [100, 100], EASE_IN), (F, [118, 118]))
    opk = keys((0, 0, EASE_OUT), (5, 100, HOLD), (OUT, 100, EASE_IN), (F, 0))
    frame = comp.null("frame", anchor=C, position=C, rotation=tilt, scale=sc)
    R = 150
    rg = record_rig(comp, (W - M - 190, H - BOT - 20), R, 8)
    comp.layers[-3]["parent"] = frame  # record-rig null rides on the frame
    comp.layer("border", [group([rect((W * 1.6, H * 1.6), C), rect(inner, icen, 6), fill(slot="outline", even_odd=True)],
                                "paper"),
                          group([rect(inner, icen, 6), stroke("#000000", width=10, opacity=18)], "inset")],
               parent=frame, opacity=opk)
    comp.layer("wash", [group([rect((W, H), C), fill(slot="secondary")], "tint")],
               opacity=keys((0, 0, EASE_OUT), (6, 36, HOLD), (OUT, 36, EASE_IN), (F, 0)))
    return comp, (M + 40, H - BOT + 40, W - 2 * M - 480, BOT - 80)


lb, lb_area = letterbox()
pol, pol_area = polaroid()
build_asset(CAT, "record-scratch-freeze", "Record Scratch Freeze",
            "Full-frame \"yep, that's me\" freeze-frame look: a white flash, a faded tint wash and a vinyl record "
            "that scratches back and forth. Pause your clip under it; some designs leave a strip for a caption.",
            ["freeze frame", "record scratch", "vinyl", "yep thats me", "meme", "flashback", "pause"], [
    Variant("classic", "Sepia Corner", classic(), "intro-hold-outro", thumb_t=0.3,
            description="Flash, warm sepia wash with a soft vignette and the record scratching in the corner."),
    Variant("letterbox", "Letterbox", lb, "intro-hold-outro", thumb_t=0.3, text_area=lb_area,
            description="Black cinema bars slam in over a cool grey wash; the record scratches in the bottom bar "
                        "beside a caption strip."),
    Variant("polaroid", "Instant Photo", pol, "intro-hold-outro", thumb_t=0.3, text_area=pol_area,
            description="A thick instant-photo border snaps in with a tilt; caption space on the wide bottom edge."),
])
