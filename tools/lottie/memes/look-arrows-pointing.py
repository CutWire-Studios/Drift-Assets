"""Several red arrows fly in and converge on one spot: the classic "look at this" thumbnail arrows."""

from _memes2 import *

W, H = 900, 720
C = (W / 2, H / 2)
F = 45
# (direction from the spot in degrees, arrow length, delay)
ARROWS = [(200, 190, 0), (238, 160, 3), (305, 200, 6), (338, 170, 2), (140, 170, 5), (32, 180, 8)]
TIP_R = 120


def arrow_shape(length, hw=78, hl=70, bw=30, taper=True):
    """Arrow pointing +x with its tip at (0, 0); the tail tapers for a thumbnail-arrow look."""
    tb = bw * 0.55 if taper else bw
    return polyline([(0, 0), (-hl, -hw / 2), (-hl + 4, -bw / 2), (-length, -tb / 2), (-length, tb / 2),
                     (-hl + 4, bw / 2), (-hl, hw / 2)], closed=True)


def placed(a, r=TIP_R):
    ar = math.radians(a)
    return [C[0] + r * math.cos(ar), C[1] + r * math.sin(ar)]


def fly(a, d, t0=2, dist=260):
    return keys((t0 + d, placed(a, TIP_R + dist), (0.15, 0.9, 0.35, 1.05)), (t0 + d + 10, placed(a, TIP_R - 14), EASE_IN_OUT),
                (t0 + d + 16, placed(a, TIP_R + 6), EASE_IN_OUT), (t0 + d + 21, placed(a)))


def classic():
    """Solid red arrows with a white outline and soft shadow fly in with overshoot."""
    comp = base("look-arrows-pointing", W, H, F)
    comp.slot("primary", "#FF2B2B")
    comp.slot("outline", "#FFFFFF")
    for i, (a, ln, d) in enumerate(ARROWS):
        shp = arrow_shape(ln)
        comp.layer(f"arrow{i}", [group([shp, round_corners(4), fill("#FFFFFF", 30)], "hi", scale=(100, 40),
                                       position=(0, -10)),
                                 group([shp, round_corners(4), fill(slot="primary")], "fill"),
                                 group([shp, round_corners(4), stroke(slot="outline", width=12)], "rim"),
                                 group([shp, round_corners(4), stroke("#000000", width=12, opacity=30),
                                        fill("#000000", 30)], "shadow", position=(6, 8))],
                   position=fly(a, d), rotation=a + 180,
                   opacity=keys((2 + d, 0, EASE_OUT), (5 + d, 100)), ip=2 + d)
    return comp


def handdrawn():
    """Red marker arrows draw themselves on, then a scribbled circle rings the spot."""
    comp = base("look-arrows-pointing--marker", W, H, F)
    comp.slot("primary", "#F0262B")
    rng = random.Random(5)
    # scribbled ring (two loose loops)
    pts = []
    for i in range(19):
        a = -2.4 + i * TAU * 1.12 / 18
        r = 92 + 5 * math.sin(i * 0.9) + i * 1.1
        pts.append((C[0] + r * 1.18 * math.cos(a), C[1] + r * math.sin(a)))
    comp.layer("ring", [group([smooth_path(pts, closed=False, tension=0.5),
                               trim(end=keys((22, 0, EASE_IN_OUT), (38, 100))),
                               stroke(slot="primary", width=12)], "ring")])
    for i, (a, ln, d) in enumerate(ARROWS):
        ar = math.radians(a)
        tip = placed(a, TIP_R + 40)
        tail = placed(a, TIP_R + 40 + ln * 1.1)
        # a slightly bowed shaft
        mid = [(tip[0] + tail[0]) / 2 + math.sin(ar) * 16 * (1 if i % 2 else -1),
               (tip[1] + tail[1]) / 2 - math.cos(ar) * 16 * (1 if i % 2 else -1)]
        shaft = smooth_path([tail, mid, tip], closed=False, tension=0.8)
        back = ar
        head = [(tip[0] + 44 * math.cos(back + 0.5), tip[1] + 44 * math.sin(back + 0.5)), tip,
                (tip[0] + 44 * math.cos(back - 0.5), tip[1] + 44 * math.sin(back - 0.5))]
        t0 = 2 + d * 1.4
        comp.layer(f"arrow{i}", [group([polyline(head), trim(end=keys((t0 + 8, 0, EASE_OUT), (t0 + 12, 100))),
                                        stroke(slot="primary", width=12)], "head"),
                                 group([shaft, trim(end=keys((t0, 0, EASE_IN_OUT), (t0 + 9, 100))),
                                        stroke(slot="primary", width=12)], "shaft")],
                   anchor=tip, position=keys((t0 + 12, tip, EASE_OUT), (t0 + 15, placed(a, TIP_R + 30), EASE_IN_OUT),
                                             (t0 + 20, tip)))
    return comp


def bold3d():
    """Chunky extruded 3D-pop arrows that stamp in with a scale bounce and a dark side face."""
    comp = base("look-arrows-pointing--3d", W, H, F)
    comp.slot("primary", "#FF3A2E")
    comp.slot("secondary", "#A3140F")
    comp.slot("accent", "#FFD23F")
    for i, (a, ln, d) in enumerate(ARROWS):
        shp = arrow_shape(ln, hw=100, hl=82, bw=44, taper=False)
        ar = math.radians(a + 180)
        # extrusion offset is fixed in screen space (down-right), so rotate it into the arrow's frame
        ex, ey = 10, 14
        lx, ly = ex * math.cos(-ar) - ey * math.sin(-ar), ex * math.sin(-ar) + ey * math.cos(-ar)
        depth = [group([shp, round_corners(6), fill(slot="secondary")], f"d{k}", position=(lx * k / 3, ly * k / 3))
                 for k in (3, 2, 1)]
        comp.layer(f"arrow{i}", [group([shp, round_corners(6), fill(slot="primary")], "face")] + depth,
                   position=placed(a, TIP_R + 10), rotation=a + 180,
                   scale=keys((2 + d, [0, 0], SPRING), (2 + d + 14, [100, 100])), ip=2 + d)
    comp.layer("spot", [group([ellipse((34, 34), C), fill(slot="accent")], "dot"),
                        group([ellipse((70, 70), C), stroke(slot="accent", width=6, opacity=60)], "ring")],
               anchor=C, position=C, scale=keys((14, [0, 0], SPRING), (26, [100, 100])), ip=14)
    return comp


build_asset(CAT, "look-arrows-pointing", "Look Here Arrows",
            "Several red thumbnail arrows fly in and converge on one spot. Put the thing everyone should look at "
            "in the middle.",
            ["arrows", "look", "pointing", "thumbnail", "red arrow", "meme", "highlight"], [
    Variant("classic", "Classic", classic(), "intro-hold", thumb_t=1.0,
            description="Solid red tapered arrows with a white outline and shadow that fly in with overshoot."),
    Variant("marker", "Marker", handdrawn(), "intro-hold", thumb_t=1.0,
            description="Hand-drawn marker arrows draw on, then a scribbled circle rings the spot."),
    Variant("3d", "3D Pop", bold3d(), "intro-hold", thumb_t=1.0,
            description="Chunky extruded arrows stamp in with a bounce around a glowing dot."),
])
