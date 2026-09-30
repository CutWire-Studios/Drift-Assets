from _common import *

NPTS = 12
WOB = 0.28
RMAX = (HALF_DIAG + 60) / (1 - WOB * 1.4)  # smallest wobble dip still clears the corners


def blob_shape(r, f, seed):
    return smooth_closed(blob_points(NPTS, r, seed, wobble=WOB, phase=f * 0.22), tension=1.0)


def blob(comp, slot, tm, seed=3, ease=SMOOTH, name="blob", center=C):
    """Wobbling liquid blob swells out to fill the frame; a blob-shaped hole then opens to reveal."""
    a0, a1, b0, b1 = tm
    grow = sampled(a0, a1, lambda u, f: blob_shape(RMAX * u, f, seed), ease)
    comp.layer(name + "-in", [group([path(Anim(grow)), fill(slot=slot)], "blob")], position=center, op=b0 + 1)
    open_ = sampled(b0, b1, lambda u, f: blob_shape(RMAX * 1.15 * u, f, seed + 7), ease)
    comp.layer(name + "-out", [hole_group([path(Anim(open_))], slot)], position=center, ip=b0)


def flat():
    t = Timing(15, 10, 15)
    comp = base("liquid-blob", t, {"primary": "#7B4DFF"})
    blob(comp, "primary", t.tm)
    return comp, t


def stacked():
    t = Timing(16, 10, 16)
    comp = base("liquid-blob--stacked", t, "violet", ("primary", "secondary", "accent"))
    for i, (s, tm) in enumerate(stack(t, lag=3)):
        blob(comp, s, tm, seed=11 + i * 5, name=s)
    return comp, t


# ---------------------------------------------------------------- drip

def drip_sheet(seed):
    """Paint sheet (local coords, bottom edge at y=0) with gooey drips hanging below it."""
    r = random.Random(seed)
    items = [rect((W + 400, 1500), position=(0, -750))]
    x = -W / 2 - 140
    while x < W / 2 + 140:
        w = r.uniform(90, 200)
        ln = r.choice([r.uniform(60, 140), r.uniform(160, 380)])
        items.append(rect((w, ln + w), position=(x, ln / 2 - w / 4), roundness=w / 2))
        # soft neck where the drip leaves the sheet
        items.append(ellipse((w * 1.9, w * 0.9), position=(x, 0)))
        x += w + r.uniform(20, 120)
    return items


def drip(comp, slot, tm, seed, ease=SMOOTH, name="drip"):
    """Sheet with drips pours down from the top; the outro keeps it pouring off the bottom."""
    top = -40 - 420     # bottom edge above the frame incl. longest drip
    cover = H + 40      # sheet's bottom edge (the drip line) just below the frame
    end = H + 1500 + 160  # whole sheet (1500 tall, plus top bumps) below the frame
    comp.layer(name, [group(drip_sheet(seed) + [fill(slot=slot)], "sheet")],
               position=io(tm, [CX, top], [CX, cover], [CX, end], ease))
    # rounded top edge: bulges riding on the sheet's upper edge so the outro edge looks liquid too
    r = random.Random(seed + 1)
    bumps = []
    x = -W / 2 - 200
    while x < W / 2 + 200:
        w = r.uniform(220, 420)
        bumps.append(ellipse((w, r.uniform(90, 200)), position=(x, -1500)))
        x += w * 0.7
    comp.layer(name + "-top", [group(bumps + [fill(slot=slot)], "bumps")],
               position=io(tm, [CX, top], [CX, cover], [CX, end], ease))


def pour():
    t = Timing(16, 10, 16)
    comp = base("liquid-blob--drip", t, "cherry", ("primary", "secondary"))
    a0, a1, b0, b1 = t.tm
    drip(comp, "primary", (a0 + 3, a1, b0, b1 - 3), 5, name="primary")
    drip(comp, "secondary", (a0, a1 - 3, b0 + 3, b1), 9, name="secondary")
    return comp, t


VARIANTS = [
    ("blob", "Blob", flat, "One wobbling blob swells out of the centre, then a blob-shaped hole opens to reveal."),
    ("stacked", "Stacked Blobs", stacked, "Three blobs in accent, secondary and primary swell one after another and "
                                          "open in reverse."),
    ("drip", "Paint Drip", pour, "Two layers of paint pour down from the top with gooey drips and flow off the "
                                 "bottom."),
]

# thumbnail moment, as a fraction of the intro (frame part-covered so the shape reads)
THUMB = {"blob": 0.38, "stacked": 0.42, "drip": 0.5}

build("liquid-blob", "Liquid Blob",
      "Gooey liquid transition: a wobbling blob swells over the shot, holds for the cut, then opens up onto the "
      "next clip.",
      ["liquid", "blob", "goo", "organic", "transition", "morph"],
      [V(v, n, *f(), d, thumb=THUMB[v], **(k[0] if k else {})) for v, n, f, d, *k in VARIANTS])
