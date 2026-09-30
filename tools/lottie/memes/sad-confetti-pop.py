"""A single sad little party popper that puffs out weak confetti and droops: the anticlimax pop."""

from _memes2 import *

W, H = 520, 520
F = 66
BASE = (160, 380)      # popper's bottom (the pull end)
PL = 200              # popper length
AIM = 38              # degrees from vertical, leaning right
POP = 20
FLOOR = 470


def popper_pts(l=PL, w=104):
    """Cone pointing up (-y) with its tip at the base pivot (0, 0) and mouth at y=-l."""
    return [(0, 0), (w / 2, -l), (-w / 2, -l)]


def cone(stripe_slot, body_slot, outline=None, l=PL, w=104, face="#2A1A22"):
    shp = polyline(popper_pts(l, w), closed=True)
    stripes = []
    for f in (0.28, 0.86):
        y = -l * f
        hw = w / 2 * f
        stripes.append(polyline([(-hw, y), (hw, y - 14), (hw * 1.02, y - 30), (-hw * 1.02, y - 16)], closed=True))
    items = [group([ellipse((w, 24), (0, -l)), fill("#000000", 45)], "mouth")]
    if outline:
        items.append(group([shp, round_corners(6), stroke(slot=outline, width=8)], "ink"))
    items += [group(stripes + [fill(slot=stripe_slot)], "stripes"),
              group([shp, round_corners(6), fill(slot=body_slot)], "body")]
    return items


def face_layer(comp, popper, color):
    """Glum face riding on the cone but kept upright."""
    rk = droop_rot()
    comp.layer("face", sad_face(color, y=0), parent=popper, position=(0, -PL * 0.56),
               rotation=keys(*[(t, -v, e) for t, v, e in rk.keys]))


def sad_face(color, line=False, y=-PL * 0.5):
    """Tiny glum face on the cone (cone-local coords)."""
    eyes = [ellipse((10, 12), (-13, y)), ellipse((10, 12), (13, y))]
    return [group([arc_path(10, 210, 330, (0, y + 24)), stroke(color, width=4)], "frown"),
            group(eyes + [fill(color)], "eyes"),
            group([polyline([(-20, y - 11), (-8, y - 17)]), polyline([(20, y - 11), (8, y - 17)]),
                   stroke(color, width=3.5)], "brows")]


def droop_rot():
    return keys((0, AIM - 6, EASE_OUT), (POP - 6, AIM + 6, EASE_IN), (POP, AIM - 4, EASE_OUT), (POP + 6, AIM, EASE_IN_OUT),
                (POP + 20, AIM + 40, EASE_IN_OUT), (POP + 30, AIM + 66, (0.3, 1.4, 0.6, 1)), (POP + 40, AIM + 60))


def squash():
    return keys((0, [0, 0], SPRING), (10, [100, 100], EASE_IN_OUT), (POP - 6, [100, 100], EASE_IN),
                (POP - 1, [110, 86], EASE_OUT), (POP + 2, [92, 108], EASE_IN_OUT), (POP + 8, [100, 100]))


def mouth_at(rot):
    a = math.radians(rot)
    return (BASE[0] + PL * math.sin(a), BASE[1] - PL * math.cos(a))


def weak_confetti(comp, n, seed, shapes_fn, spread=70, up=(60, 120)):
    """Pieces leave the mouth at POP, barely rise, then flutter down and settle on the floor."""
    rng = random.Random(seed)
    m = mouth_at(AIM)
    for i in range(n):
        vx = rng.uniform(-0.4, 1.0) * spread
        h = rng.uniform(*up)
        land_x = m[0] + vx * 1.6 + rng.uniform(-30, 30)
        spin = rng.uniform(-400, 400)
        fall = rng.uniform(34, 42)
        wob = rng.uniform(0, TAU)
        rest_rot = rng.uniform(-40, 40)

        def fn(u, vx=vx, h=h, land_x=land_x, spin=spin, fall=fall, wob=wob, rest_rot=rest_rot):
            p = clamp(u / 12)
            if u <= 12:
                x = m[0] + vx * ease_out(p, 2)
                y = m[1] - h * ease_out(p, 2)
            else:
                q = clamp((u - 12) / fall)
                x = m[0] + vx + (land_x - m[0] - vx) * q + 16 * math.sin(q * 9 + wob) * (1 - q)
                y = (m[1] - h) + (FLOOR - (m[1] - h)) * (q ** 1.6)
            sx = 100 * abs(math.cos(u * 0.35 + wob)) if u < 12 + fall else 100
            return {"position": [x, y], "rotation": spin * clamp(u / (12 + fall)) + rest_rot,
                    "scale": [max(sx, 18), 100]}
        comp.layer(f"bit{i}", shapes_fn(i), ip=POP, op=F, **{k: sampled(lambda t, k=k: fn(t - POP)[k], POP, F, 2)
                                                             for k in ("position", "rotation", "scale")})


def puff(comp, color="#FFFFFF", op=70):
    m = mouth_at(AIM)
    blobs = [ellipse((d, d), (x, y)) for x, y, d in ((-14, 0, 26), (4, -10, 32), (18, 2, 24))]
    comp.layer("puff", [group(blobs + [fill(color, op)], "p")], position=m, rotation=AIM,
               scale=keys((POP, [20, 20], EXPO_OUT), (POP + 10, [100, 100], EASE_IN), (POP + 18, [120, 120])),
               opacity=keys((POP, 100, EASE_IN), (POP + 18, 0)), ip=POP, op=POP + 19)


def sweat(comp, color="#7FC8FF"):
    """A little sweat drop beside the popper once it droops."""
    d = path(bezier([(0, -18), (11, 4), (0, 14), (-11, 4)], [(0, 0), (0, -8), (7, 0), (0, 7)],
                    [(0, 0), (0, 7), (-7, 0), (0, -8)]), "drop")
    comp.layer("sweat", [group([d, fill(color)], "d")],
                position=keys((POP + 30, [BASE[0] + 60, BASE[1] - 110], EASE_IN), (F, [BASE[0] + 56, BASE[1] - 84])),
                scale=keys((POP + 30, [0, 0], SPRING), (POP + 40, [100, 100])), ip=POP + 30)


def classic():
    """Striped party popper: a pathetic puff, a few confetti bits flutter down and it droops."""
    comp = base("sad-confetti-pop", W, H, F)
    comp.slot("primary", "#FF5A8A")
    comp.slot("secondary", "#FFD23F")
    comp.slot("accent", "#3DB2FF")
    cols = ["#FF5A8A", "#FFD23F", "#3DB2FF", "#7BE08A", "#B98CFF"]
    sweat(comp)
    weak_confetti(comp, 7, 4, lambda i: [group([rect((24, 13), (0, 0), 3) if i % 2 else ellipse((16, 16)),
                                               fill(cols[i % len(cols)])], "c")])
    puff(comp)
    popper = comp._ind + 2
    face_layer(comp, popper, "#2A1A22")
    comp.layer("popper", cone("secondary", "primary"), position=BASE, rotation=droop_rot(), scale=squash())
    comp.layer("shadow", [group([ellipse((140, 18)), fill("#000000", 25)], "s")], position=(BASE[0] + 110, FLOOR + 8),
               scale=keys((0, [0, 0], SPRING), (10, [100, 100])))
    return comp


def streamer():
    """The popper coughs out one limp streamer that uncurls and flops down, plus a single dot."""
    comp = base("sad-confetti-pop--streamer", W, H, F)
    comp.slot("primary", "#3DB2FF")
    comp.slot("secondary", "#FFFFFF")
    comp.slot("accent", "#FF5A8A")
    m = mouth_at(AIM)

    rk = droop_rot().keys

    def rot_at(t):
        for (t0, v0, _), (t1, v1, _) in zip(rk, rk[1:]):
            if t0 <= t <= t1:
                return v0 + (v1 - v0) * smooth((t - t0) / (t1 - t0))
        return rk[-1][1]

    def strm(t):
        # a short curl leaves the mouth, then goes limp and hangs from wherever the mouth is
        e = ease_out(clamp((t - POP) / 30), 2)
        r = math.radians(rot_at(t))
        m = mouth_at(rot_at(t))
        d = (math.sin(r), -math.cos(r))
        n = (-d[1], d[0])
        ln = 50 + 110 * e
        pts = []
        for j in range(7):
            f = j / 6
            out = f * ln * (1 - 0.75 * e)
            curl = math.sin(f * TAU) * 18 * (1 - e)
            pts.append((m[0] + d[0] * out + n[0] * curl + e * f * 12,
                        m[1] + d[1] * out + n[1] * curl + e * (f ** 1.3) * ln))
        return smooth_bez(pts, closed=False)
    ks = [(t, strm(t), LINEAR) for t in range(POP, POP + 44, 2)] + [(POP + 44, strm(POP + 44), LINEAR)]
    comp.layer("streamer", [group([path(Anim(ks)), trim(end=keys((POP, 0, EXPO_OUT), (POP + 10, 100))),
                                   stroke(slot="accent", width=12)], "s")], ip=POP)
    weak_confetti(comp, 1, 9, lambda i: [group([ellipse((16, 16)), fill("#FFD23F")], "c")], spread=30, up=(40, 50))
    puff(comp, op=50)
    popper = comp._ind + 2
    face_layer(comp, popper, "#2A1A22")
    comp.layer("popper", cone("secondary", "primary"), position=BASE, rotation=droop_rot(), scale=squash())
    comp.layer("shadow", [group([ellipse((140, 18)), fill("#000000", 25)], "s")], position=(BASE[0] + 110, FLOOR + 8),
               scale=keys((0, [0, 0], SPRING), (10, [100, 100])))
    return comp


def line():
    """Monochrome line art: outlined popper, a scribbly little puff and outlined confetti bits."""
    comp = base("sad-confetti-pop--line", W, H, F)
    comp.slot("outline", "#FFFFFF")
    sweat(comp, "#FFFFFF")
    shapes = [lambda: [rect((20, 12), (0, 0), 2)], lambda: [ellipse((14, 14))],
              lambda: [polyline([(0, -9), (8, 7), (-8, 7)], closed=True)]]
    weak_confetti(comp, 6, 6, lambda i: [group(shapes[i % 3]() + [stroke(slot="outline", width=4)], "c")])
    m = mouth_at(AIM)
    lines = [polyline([(0, -30), (0, -52)]), polyline([(-20, -24), (-30, -42)]), polyline([(20, -24), (30, -42)])]
    comp.layer("pff", [group(lines + [trim(start=keys((POP + 4, 0, EASE_IN), (POP + 14, 100)),
                                           end=keys((POP, 0, EXPO_OUT), (POP + 6, 100))),
                                      stroke(slot="outline", width=5)], "l")],
               position=m, rotation=AIM, ip=POP, op=POP + 15)
    shp = polyline(popper_pts(), closed=True)
    stripes = [polyline([(-52 * f, -PL * f), (52 * f, -PL * f - 14)]) for f in (0.25, 0.8)]
    popper = comp._ind + 2
    face_layer(comp, popper, "#FFFFFF")
    comp.layer("popper", [group([ellipse((104, 24), (0, -PL)), stroke(slot="outline", width=6)], "mouth"),
                          group(stripes + [stroke(slot="outline", width=5)], "stripes"),
                          group([shp, round_corners(6), stroke(slot="outline", width=7)], "cone")],
               position=BASE, rotation=droop_rot(), scale=squash())
    comp.layer("floor", [group([polyline([(60, FLOOR + 10), (460, FLOOR + 10)]),
                                stroke(slot="outline", width=4, opacity=40, dashes=[20, 14])], "f")],
               opacity=keys((0, 0, EASE_OUT), (10, 100)))
    return comp


build_asset(CAT, "sad-confetti-pop", "Sad Confetti Pop",
            "A single sad little party popper that puffs out a few weak bits of confetti and then droops. For "
            "every anticlimactic celebration.",
            ["party popper", "confetti", "sad", "anticlimax", "celebration", "meme", "fail"], [
    Variant("classic", "Classic", classic(), "intro-hold", thumb_t=0.62,
            description="Striped popper: a pathetic puff, a few confetti bits flutter down and it droops."),
    Variant("streamer", "Limp Streamer", streamer(), "intro-hold", thumb_t=1.0,
            description="One limp streamer uncurls and flops out, plus a single lonely dot."),
    Variant("line", "Line Art", line(), "intro-hold", thumb_t=0.62,
            description="Monochrome outline popper with a scribbly puff and outlined confetti."),
])
