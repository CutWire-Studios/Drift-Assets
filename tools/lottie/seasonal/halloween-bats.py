"""Halloween bats: flapping bats flying across the frame, circling a full moon, or hovering (loops)."""

from _common import *

T = 120
FLAP = 12  # frames per wingbeat (divides T)
BAT = "#1B1026"
WING_D = ("M 0 0 Q 18 -26 46 -24 Q 64 -24 78 -10 Q 64 -6 60 8 Q 52 -2 42 12 Q 34 2 24 12 "
          "Q 16 4 4 12 Z")
CUTE_WING_D = "M 0 0 Q 16 -30 44 -26 Q 62 -22 70 -6 Q 58 -4 54 10 Q 44 0 32 12 Q 20 2 4 12 Z"


def mirror_d(d):
    """Mirror an SVG path made of M/Q/L/Z absolute commands left-right."""
    out, toks = [], d.split()
    i = 0
    while i < len(toks):
        t = toks[i]
        if t.isalpha():
            out.append(t)
            i += 1
        else:
            out += [f"{-float(t):g}", toks[i + 1]]
            i += 2
    return " ".join(out)


def wing_group(d, paint, side, t0, t1, ph, name, shoulder=(6, -6), up=-38, down=28, squash=62):
    """A wing that beats about the shoulder: rotation + vertical squash give the flap."""
    sx = shoulder[0] * side
    g = group(S(d if side > 0 else mirror_d(d)) + paint, name)
    rot_keys = osc_keys(t0, t1, FLAP, up * side, down * side, ph)
    scl = osc_keys(t0, t1, FLAP, [100, squash], [100, 100], ph)
    g["it"][-1] = transform(shape=True, anchor=(0, 0), position=(sx, shoulder[1]), rotation=rot_keys, scale=scl)
    return g


def bat_items(style, t0, t1, ph=0.0):
    """Shape items for one bat centred on its body; wings flap between t0 and t1."""
    if style == "cute":
        purple, belly, ink = "#6B3FA0", "#9B72CF", "#22122F"
        wpaint = [fill(purple, slot="primary")]
        items = [
            group([ellipse((7, 7)), fill(WHITE)], "catch-l", position=(-13, -9)),
            group([ellipse((7, 7)), fill(WHITE)], "catch-r", position=(9, -9)),
            group([ellipse((4, 4)), ellipse((4, 4), (22, 0)), fill(WHITE, 80)], "catch2", position=(-7, -2)),
            group([ellipse((16, 19)), fill(ink)], "eye-l", position=(-10, -5)),
            group([ellipse((16, 19)), fill(ink)], "eye-r", position=(12, -5)),
            group(S("M -3 9 L 0 16 L 3 9 Z M 5 9 L 8 16 L 11 9 Z") + [fill(WHITE)], "fangs"),
            group(S("M -6 7 Q 4 13 14 7") + [stroke(ink, 2.8)], "mouth"),
            group([ellipse((12, 7), (-22, 7)), ellipse((12, 7), (26, 7)), fill("#FF7FA8", 70)], "blush"),
            group([ellipse((34, 22), (2, 24)), fill(belly, slot="secondary")], "belly"),
            group(S("M -20 -26 L -18 -46 L -6 -32 Z M 24 -26 L 22 -46 L 10 -32 Z") + [fill("#FF9CC0")],
                  "ear-in"),
            group([ellipse((64, 66), (2, 0)),
                   *S("M -27 -18 L -22 -58 L -2 -30 Z M 31 -18 L 26 -58 L 6 -30 Z"),
                   fill(purple, slot="primary")], "body"),
            wing_group(CUTE_WING_D, wpaint, 1, t0, t1, ph, "wing-r", shoulder=(26, 4), up=-34, down=26),
            wing_group(CUTE_WING_D, wpaint, -1, t0, t1, ph, "wing-l", shoulder=(22, 4), up=-34, down=26),
        ]
        return items
    paint = [fill(BAT, slot="primary")]
    eyes = [group([ellipse((4, 3), (-5, -17)), ellipse((4, 3), (5, -17)), fill("#FFB02E")], "eyes")] \
        if style == "moon" else []
    return eyes + [
        group([ellipse((20, 30), (0, 4)), ellipse((18, 16), (0, -15)),
               *S("M -9 -18 L -6 -33 L -1 -21 Z M 9 -18 L 6 -33 L 1 -21 Z"), *paint], "body"),
        wing_group(WING_D, paint, 1, t0, t1, ph, "wing-r"),
        wing_group(WING_D, paint, -1, t0, t1, ph, "wing-l"),
    ]


# ---------------------------------------------------------------- full-frame swarm

def swarm():
    W, H = 1920, 1080
    comp = Comp("halloween-bats", W, H, frames=T)
    comp.slot("primary", BAT)
    r = rng(13)
    n = 16
    for i in range(n):
        life = r.uniform(70, 110)
        t0 = (i * T / n + r.uniform(0, 5)) % T
        d = r.random()
        sz = lerp(0.9, 2.0, d)
        dirn = 1 if i % 4 else -1
        y0 = r.uniform(120, H - 180)
        y1 = y0 + r.uniform(-260, 160)
        amp = r.uniform(20, 60)
        ph = r.random()
        fp = r.choice((0, 0.25, 0.5, 0.75))

        def fn(u, life=life, y0=y0, y1=y1, amp=amp, ph=ph, sz=sz, dirn=dirn):
            k = u / life
            x = lerp(-140, W + 140, k) if dirn > 0 else lerp(W + 140, -140, k)
            y = lerp(y0, y1, smooth(k)) + amp * math.sin(TAU * (k * 1.6 + ph))
            tilt = 10 * math.cos(TAU * (k * 1.6 + ph)) * dirn
            return {"position": (x, y), "rotation": tilt, "scale": (100 * sz * dirn, 100 * sz)}

        starts = [t0] + ([t0 - T] if t0 + life > T else [])
        for s in starts:
            keys = {k: sampled(lambda t, k=k, s=s: fn(min(max(t - s, 0), life))[k], s, s + life, 3)
                    for k in ("position", "rotation", "scale")}
            comp.layer(f"bat{i}", bat_items("swarm", s, s + life, fp), ip=s, op=s + life, **keys)
    return comp


# ---------------------------------------------------------------- moon + circling bats

def moon():
    W = H = 720
    comp = Comp("halloween-bats--moon", W, H, frames=T)
    comp.slot("primary", BAT)
    comp.slot("secondary", "#FFE7A3")
    c = (W / 2, H / 2)
    R = 190
    # bats orbit on a tilted ellipse; the far half passes behind the moon
    orbit = [(0.0, 1.6), (1 / 3, 1.35), (2 / 3, 1.75)]
    front, back = [], []
    for j, (ph, sz) in enumerate(orbit):
        def pos(t, ph=ph):
            a = TAU * (t / T + ph)
            return (c[0] + 270 * math.cos(a), c[1] + 70 * math.sin(a) - 50 * math.sin(2 * a) + 10)

        def depth(t, ph=ph):
            return math.sin(TAU * (t / T + ph))  # +1 near (front), -1 far

        for part, lst in (("front", front), ("back", back)):
            sign = 1 if part == "front" else -1

            def vis(t, depth=depth, sign=sign):
                return 100 if depth(t) * sign > 0 else 0
            keys = [(t, vis(t), HOLD) for t in range(0, T + 1)]
            ks = [keys[0]] + [k for a, k in zip(keys, keys[1:]) if k[1] != a[1]]
            ks.append((T, keys[0][1], HOLD))
            lst.append(dict(name=f"bat{j}-{part}", ph=ph, sz=sz, pos=pos, depth=depth, op=Anim(ks)))

    def add(b):
        comp.layer(b["name"], bat_items("moon", 0, T, b["ph"] * 4 % 1), position=looped(b["pos"], T, 2),
                   scale=looped(lambda t, b=b: [(-1 if math.cos(TAU * (t / T + b["ph"])) > 0 else 1) *
                                                100 * b["sz"] * (1 + 0.28 * b["depth"](t)),
                                                100 * b["sz"] * (1 + 0.28 * b["depth"](t))], T, 2),
                   rotation=looped(lambda t, b=b: 12 * math.sin(TAU * (2 * t / T + b["ph"])), T, 3),
                   opacity=b["op"])

    for b in front:
        add(b)
    # moon with craters and a soft breathing glow
    craters = [((-60, -50), 58), ((50, 40), 42), ((-20, 80), 30), ((70, -70), 24), ((-95, 35), 20)]
    comp.layer("moon", [
        group([ellipse((d, d), p) for p, d in craters] + [fill("#C9A95A", 45)], "craters"),
        group([ellipse((2 * R, 2 * R)), shade_overlay((-R, -R, R, R), 0.8, light=(0.3, 0.28), dark="#8A6A20")],
              "shade"),
        group([ellipse((2 * R, 2 * R)), fill("#FFE7A3", slot="secondary")], "disc"),
    ], position=c)
    comp.layer("moon-glow", [glow(R * 1.7, "#FFE7A3", 100, falloff=((0, 0.55), (0.55, 0.28), (1, 0)))],
               position=c, opacity=looped(lambda t: 55 + 15 * wave(t, T, 2), T, 4))
    for b in back:
        add(b)
    return comp


# ---------------------------------------------------------------- cute hovering trio

def cute():
    W, H = 820, 480
    comp = Comp("halloween-bats--cute", W, H, frames=T)
    comp.slot("primary", "#6B3FA0")
    comp.slot("secondary", "#9B72CF")
    spots = [((W * 0.5, 190), 1.7, 0.0), ((W * 0.19, 290), 1.25, 0.33), ((W * 0.81, 280), 1.3, 0.66)]
    for j, (p, s, ph) in enumerate(spots):
        comp.layer(f"bat{j}", bat_items("cute", 0, T, ph % 1),
                   position=looped(lambda t, p=p, ph=ph: (p[0] + 22 * wave(t, T, 1, ph),
                                                          p[1] + 18 * wave(t, T, 2, ph + 0.25)), T, 2),
                   rotation=looped(lambda t, ph=ph: 7 * wave(t, T, 1, ph + 0.25), T, 3),
                   scale=(100 * s, 100 * s))
        comp.layer(f"shadow{j}", [ellipse((90 * s, 14 * s)), fill("#000000", 16)],
                   position=(p[0], p[1] + 95 * s + 30),
                   scale=looped(lambda t, ph=ph: [100 - 14 * wave(t, T, 2, ph + 0.25)] * 2, T, 3))
    return comp


build("halloween-bats", "Halloween Bats",
      "Flapping bats for Halloween edits: a swarm flying across the whole frame, bats circling a full moon, "
      "or a cute hovering trio. Seamless loops.",
      ["halloween", "bats", "spooky", "night", "moon", "october", "flying"], [
          Variant("swarm", "Swarm", swarm(), "loop", thumb_t=0.25, bg="e8e8ee", region=(160, 140, 860, 800), pad=0,
                  description="Full-frame transparent overlay of silhouette bats flapping across in wavy flight."),
          Variant("moon", "Full Moon", moon(), "loop", thumb_t=0.1,
                  description="Glowing full moon with three silhouette bats circling in front of and behind it."),
          Variant("cute", "Cute Trio", cute(), "loop", thumb_t=0.3,
                  description="Three cute purple cartoon bats with big eyes and tiny fangs, hovering and flapping."),
      ])
