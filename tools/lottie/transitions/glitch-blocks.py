from _common import *

GLITCH = {"primary": "#2B2DFF", "secondary": "#FF2E88", "accent": "#20F0C8"}
OFF = -W * 1.6  # parked off the left edge


def rows(seed, lo=36, hi=150):
    """Random row bands (y, h) covering the frame height, overlapping by 2 px."""
    r = random.Random(seed)
    out, y = [], -20
    while y < H + 20:
        h = r.uniform(lo, hi)
        out.append((y + h / 2, h + 12))
        y += h
    return out


def jumpy(r, t_in, t_out, a_end, b_end, spread=900):
    """Stepped x offsets: park, jump in with two random glitch positions, settle, then jump out."""
    k1 = r.uniform(-spread, spread)
    k2 = r.uniform(-spread / 3, spread / 3)
    o1 = r.uniform(-spread / 3, spread / 3)
    o2 = r.choice([-1, 1]) * r.uniform(spread * 0.6, spread * 1.2)
    ti = min(t_in, a_end - 2)
    to = max(t_out, 0)
    return Anim([(0, [OFF, 0], HOLD), (ti, [k1, 0], HOLD), (ti + 1, [k2, 0], HOLD), (ti + 2, [0, 0], HOLD),
                 (to, [o1, 0], HOLD), (min(to + 1, b_end - 1), [o2, 0], HOLD), (min(to + 2, b_end), [OFF, 0], HOLD),
                 (b_end + 1, [OFF, 0])])


def bars(comp, slot, tm, seed, name="bars"):
    a0, a1, b0, b1 = tm
    r = random.Random(seed)
    groups = []
    for i, (y, h) in enumerate(rows(seed)):
        ti = r.randint(a0 + 1, a1 - 2)
        to = r.randint(b0 + 1, b1 - 2)
        groups.append(group([rect((W + 120, h), position=(CX, y)), fill(slot=slot)], f"row{i}",
                            position=jumpy(r, ti, to, a1, b1)))
    comp.layer(name, groups)


def blocks():
    t = Timing(12, 10, 12)
    comp = base("glitch-blocks", t, GLITCH, ("primary",))
    bars(comp, "primary", t.tm, 7)
    return comp, t


def rgb():
    t = Timing(14, 10, 14)
    comp = base("glitch-blocks--rgb", t, GLITCH, ("primary", "secondary", "accent"))
    for i, (s, tm) in enumerate(stack(t, lag=2)):
        bars(comp, s, tm, 7 + i * 31, name=s)
    return comp, t


def mosaic():
    """A grid of blocks flickers on in random order until the frame is solid, then flickers off."""
    t = Timing(14, 10, 14)
    comp = base("glitch-blocks--mosaic", t, GLITCH, ("primary", "secondary"))
    a0, a1, b0, b1 = t.tm
    r = random.Random(3)
    cols, rws = 12, 7
    cw, ch = W / cols, H / rws
    groups = []
    for c in range(cols):
        for rw in range(rws):
            on = r.randint(a0 + 1, a1 - 3)
            off = r.randint(b0 + 1, b1 - 3)
            flick = [(0, 0, HOLD), (on, 100, HOLD), (on + 1, 0, HOLD), (on + 2, 100, HOLD),
                     (off, 0, HOLD), (off + 1, 100, HOLD), (off + 2, 0, HOLD), (b1, 0)]
            if on + 2 > a1:
                flick = flick[:1] + [(on, 100, HOLD)] + flick[4:]
            slot = "secondary" if r.random() < 0.18 else "primary"
            groups.append(group([rect((cw + 12, ch + 12), position=((c + 0.5) * cw, (rw + 0.5) * ch)),
                                 fill(slot=slot)], f"b{c}-{rw}", opacity=Anim(flick)))
            # a stray sliver echoes some blocks sideways for a moment
            if r.random() < 0.3:
                dx = r.choice([-1, 1]) * cw * r.uniform(0.6, 1.6)
                groups.append(group([rect((cw * r.uniform(0.6, 1.8), ch * r.uniform(0.15, 0.4)),
                                          position=((c + 0.5) * cw + dx, (rw + r.uniform(0.2, 0.8)) * ch)),
                                     fill(slot="secondary")], f"s{c}-{rw}",
                                    opacity=Anim([(0, 0, HOLD), (on - 1, 100, HOLD) if on > 1 else (1, 100, HOLD),
                                                  (on + 1, 0, HOLD), (off + 2, 100, HOLD), (off + 3, 0, HOLD),
                                                  (b1, 0)])))
    # slivers first so they draw on top of the blocks
    groups.sort(key=lambda g: 0 if g["nm"].startswith("s") else 1)
    comp.layer("mosaic", groups)
    return comp, t


VARIANTS = [
    ("blocks", "Glitch Bars", blocks, "Horizontal bars of random height jump in with stepped glitch offsets until the "
                                      "frame is solid, then glitch out."),
    ("rgb", "RGB Split", rgb, "Three colour passes of glitch bars land one after another like a broken RGB signal."),
    ("mosaic", "Mosaic Flicker", mosaic, "A grid of blocks flickers on in random order with stray slivers, then "
                                         "flickers off."),
]

# thumbnail moment, as a fraction of the intro (frame part-covered so the shape reads)
THUMB = {"blocks": 0.5, "rgb": 0.5, "mosaic": 0.45}

build("glitch-blocks", "Glitch Blocks",
      "Digital glitch transition: blocky bars stutter in to cover the shot, hold for the cut, then glitch away "
      "to reveal the next clip.",
      ["glitch", "digital", "blocks", "transition", "tech", "error"],
      [V(v, n, *f(), d, thumb=THUMB[v], **(k[0] if k else {})) for v, n, f, d, *k in VARIANTS])
