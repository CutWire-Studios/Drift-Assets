from _common import *

BURN = {"primary": "#1A0D08", "secondary": "#E8441C", "accent": "#FFB43A"}
WOB = 0.3
NP = 16


def reach(p):
    return max(math.hypot(x - p[0], y - p[1]) for x in (0, W) for y in (0, H))


def cell_reach(spots):
    """For each spot, the farthest frame point that is closer to it than to any other spot (Voronoi reach)."""
    need = [0.0] * len(spots)
    for x in range(-20, W + 21, 20):
        for y in range(-20, H + 21, 20):
            d = [math.hypot(x - p[0], y - p[1]) for p in spots]
            i = d.index(min(d))
            need[i] = max(need[i], d[i])
    return need


def ratio(seed, f):
    """Smallest radius of the blob outline at frame f, as a fraction of its nominal radius."""
    pts = blob_points(NP, 1.0, seed, wobble=WOB, phase=f * 0.18)
    return min(math.hypot(*p) for p in pts)


def burn_blob(seed, r, f):
    return smooth_closed(blob_points(NP, r, seed, wobble=WOB, phase=f * 0.18))


def blob_anim(seed, t0, t1, rmax, curve, stepped=False, rate=0.18):
    """Blob outline growing from nothing to rmax; stepped=True jerks every other frame like a projector."""
    keys = []
    for f in list(range(t0, t1, 2)) + [t1]:  # a key every other frame keeps the file small
        u = (f - t0) / (t1 - t0)
        if stepped:
            u = (f - t0 - (f - t0) % 2) / (t1 - t0) if f < t1 else 1
        keys.append((f, burn_blob(seed, rmax * curve(u), f), HOLD if stepped else LINEAR))
    return Anim(keys)


def spots_items(spots, t0, t1, grow, curve, stepped, seed0, need):
    return [path(blob_anim(seed0 + i, t0 + d, t1, (need[i] / ratio(seed0 + i, t1) + 60) * grow, curve, stepped),
                 f"b{i}") for i, (p, d) in enumerate(spots)]


def burn(comp, spots, tm, curve, stepped=False, tones=("primary", "secondary", "accent"), glow=(1.1, 1.22)):
    """Film burns in from `spots` [(pos, delay)] with glowing edges, then burns through to reveal."""
    a0, a1, b0, b1 = tm
    local = [((p[0], p[1]), d) for p, d in spots]
    need = cell_reach([p for p, _ in spots])

    def moved(items, spots_):
        return [group([it], f"at{i}", position=spots_[i][0]) for i, it in enumerate(items)]

    # intro: core over glow rings; each blob drawn about its own spot
    for k, (slot, g) in enumerate(zip(tones, (1.0,) + glow)):
        items = moved(spots_items([((0, 0), d) for _, d in local], a0, a1, g, curve, stepped, 10, need), local)
        comp.layer(f"burn-in-{slot}", [group(items + [fill(slot=slot)], "blobs")], op=b0 + 1)
    # outro: holes burn through the core; glow rings ride just outside the holes
    holes = lambda g: moved(spots_items([((0, 0), d) for _, d in local], b0, b1, g, curve, stepped, 40, need), local)
    for k, (slot, g) in enumerate(zip(tones[1:], glow)):
        comp.layer(f"hole-matte-{slot}", [group(holes(1.0) + [fill()], "holes")], ip=b0)
        comp.layer(f"glow-{slot}", [group(holes(g) + [fill(slot=slot)], "glow")], ip=b0, matte="alpha_inverted")
    comp.layer("hole-matte", [group(holes(1.0) + [fill()], "holes")], ip=b0)
    comp.layer("film", [cover_rect(), fill(slot=tones[0])], ip=b0, matte="alpha_inverted")


SPOTS = [((330, 260), 0), ((1560, 230), 2), ((1640, 860), 1), ((520, 880), 3), ((980, 560), 4)]


def spots():
    t = Timing(16, 10, 16)
    comp = base("film-burn-shapes", t, BURN, ("primary", "secondary", "accent"))
    burn(comp, SPOTS, t.tm, zoom_curve(GENTLE, 1.5))
    return comp, t


def flicker():
    t = Timing(14, 8, 14)
    comp = base("film-burn-shapes--flicker", t, BURN, ("primary", "secondary", "accent"))
    burn(comp, [((1500, 300), 0), ((420, 780), 2), ((1100, 700), 3)], t.tm, zoom_curve(GENTLE, 1.5), stepped=True,
         glow=(1.14, 1.3))
    return comp, t


def corner():
    """Flat single-colour burn: one ragged edge creeps in from a corner and burns out from the opposite one."""
    t = Timing(16, 10, 16)
    comp = base("film-burn-shapes--corner", t, {"primary": "#FF7A1A"}, ("primary",))
    a0, a1, b0, b1 = t.tm
    p_in, p_out = (-80, H + 80), (W + 80, -80)
    rin = reach(p_in) / ratio(3, a1) + 60
    comp.layer("burn-in", [group([path(blob_anim(3, a0, a1, rin, zoom_curve(GENTLE, 2.0))), fill(slot="primary")],
                                 "blob", position=p_in)], op=b0 + 1)
    rout = reach(p_out) / ratio(8, b1) + 60
    comp.layer("hole-matte", [group([path(blob_anim(8, b0, b1, rout, zoom_curve(GENTLE, 2.0))), fill()], "blob",
                                    position=p_out)], ip=b0)
    comp.layer("film", [cover_rect(), fill(slot="primary")], ip=b0, matte="alpha_inverted")
    return comp, t


VARIANTS = [
    ("spots", "Burn Spots", spots, "Burn holes with glowing orange edges spread from five spots until the frame is "
                                   "scorched, then burn through."),
    ("flicker", "Projector Flicker", flicker, "Jerky, stepped burn growth like a stuck projector, with wider "
                                              "glowing edges."),
    ("corner", "Flat Corner Burn", corner, "One flat-colour ragged edge creeps in from a corner and burns out from "
                                           "the opposite one."),
]

# thumbnail moment, as a fraction of the intro (frame part-covered so the shape reads)
THUMB = {"spots": 0.5, "flicker": 0.5, "corner": 0.55}

build("film-burn-shapes", "Film Burn Shapes",
      "Film burn transition: burn holes with glowing edges spread over the shot, hold on the scorched frame for the "
      "cut, then burn through to reveal the next clip.",
      ["film", "burn", "retro", "vintage", "transition", "fire"],
      [V(v, n, *f(), d, thumb=THUMB[v], **(k[0] if k else {})) for v, n, f, d, *k in VARIANTS])
