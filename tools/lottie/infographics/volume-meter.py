from _common import *

F = 72                      # 2.4 s loop


def level_keys(seed, n=6, lo=0.25, hi=1.0):
    rnd = random.Random(seed)
    return [rnd.uniform(lo, hi) if i % 2 == 0 else rnd.uniform(lo * 0.6, (lo + hi) / 2) for i in range(n)]


def level_fn(vals, e=EASE_IN_OUT):
    """Level at frame f of a seamless loop through vals (evenly spaced, back to vals[0])."""
    v = list(vals) + [vals[0]]
    step = F / (len(v) - 1)

    def fn(f):
        f = f % F
        k = min(int(f // step), len(v) - 2)
        u = (f - k * step) / step
        return lerp(v[k], v[k + 1], ease_eval(e, u))
    return fn


def peaks(fn, fall=0.012):
    """Peak-hold marker per frame for a loop (settled over two cycles, last == first)."""
    p, out = 0.0, []
    for f in range(3 * F):
        p = max(p - fall, fn(f))
        if f >= 2 * F:
            out.append(p)
    out.append(out[0])
    return out


# ---------------------------------------------------------------- bars (flat)

def bars():
    """Equalizer: rounded bars bounce to the beat with peak-hold caps that drift down."""
    W, H = 720, 400
    comp = Comp("volume-meter", W, H, fps=30, frames=F)
    slots(comp, FLAT | {"primary": "#5B6CFF", "accent": "#FF6B8A"}, "primary", "accent", "background")
    n, bw, gap = 9, 50, 20
    base, hmax = 300, 250
    x0 = W / 2 - (n * bw + (n - 1) * gap) / 2 + bw / 2
    for i in range(n):
        vals = level_keys(i * 7 + 1, 6, 0.2 + 0.25 * math.sin(math.pi * i / (n - 1)), 1.0)
        cx = x0 + i * (bw + gap)
        body = rect((bw, hmax), (cx, base - hmax / 2), 14)
        sk = [[100, 100 * v] for v in vals]
        comp.layer(f"bar{i}", [group([body, fill(slot="primary")], "b")], anchor=(cx, base), position=(cx, base),
                   scale=loop(F, sk, EASE_IN_OUT))
        pk = peaks(level_fn(vals))
        comp.layer(f"peak{i}", [group([rect((bw, 10), (cx, 0), 5), fill(slot="accent")], "p")],
                   position=anim([(f, [0, base - hmax * pk[f] - 16], LINEAR) for f in range(0, F + 1, 2)]
                                 + ([(F, [0, base - hmax * pk[-1] - 16], LINEAR)] if F % 2 else [])))
        comp.layer(f"slot{i}", [group([rect((bw, hmax), (cx, base - hmax / 2), 14), fill(slot="background",
                                                                                     opacity=8)], "s")])
    comp.layer("floor", [box(x0 - bw / 2 - 10, base + 14, (n - 1) * (bw + gap) + bw + 20, 4, slot="background",
                             opacity=30, r=2)])
    return comp, {"label": (W / 2 - 220, base + 34, 440, 56)}


# ---------------------------------------------------------------- analog VU

def vu():
    """Analog VU meter: cream face, printed scale with a red zone and a needle that swings to the music."""
    W, H = 640, 480
    comp = Comp("volume-meter--vu", W, H, fps=30, frames=F)
    slots(comp, FLAT | {"background": "#F6EEDC", "outline": "#2A2A30", "primary": "#E8413B", "accent": "#34343C"},
          "background", "outline", "primary", "accent")
    fc = (W / 2, 210)
    pivot = (W / 2, 330)
    R = 190
    a0, a1, ared = -140, -40, -62
    vals = [0.35, 0.8, 0.5, 0.95, 0.4, 0.7, 0.55, 0.88]
    rot = [lerp(a0, a1, v) + 90 for v in vals]
    comp.layer("needle-cap", [group([ellipse((34, 34), pivot), fill(slot="accent")], "c")])
    comp.layer("needle", [group([polyline([(pivot[0], pivot[1] + 18), (pivot[0], pivot[1] - R - 6)]),
                                 stroke(slot="primary", width=4)], "n")],
               anchor=pivot, position=pivot, rotation=loop(F, rot, (0.3, 0.0, 0.2, 1.0)))
    ticks = []
    for k in range(11):
        a = lerp(a0, a1, k / 10)
        ln = 24 if k % 5 == 0 else 14
        ticks.append(polyline([pt(pivot, R, a), pt(pivot, R - ln, a)]))
    comp.layer("scale", [group(ticks + [stroke(slot="outline", width=3)], "ticks"),
                         group([arc_path(R, a0, ared, pivot), stroke(slot="outline", width=3)], "arc"),
                         group([arc_path(R - 6, ared, a1, pivot), stroke(slot="primary", width=14, cap="butt")], "red"),
                         group([arc_path(R - 60, a0 + 10, a1 - 10, pivot), stroke(slot="outline", width=2,
                                                                                  opacity=35)], "inner")])
    face = rect((560, 330), fc, 28)
    comp.layer("glass-matte", [group([rect((560, 330), fc, 28), fill()], "m")])
    comp.layer("glass", [group([polyline([(fc[0] - 280, fc[1] - 165), (fc[0] + 60, fc[1] - 165),
                                          (fc[0] - 120, fc[1] + 165), (fc[0] - 280, fc[1] + 165)], closed=True),
                                fill("#FFFFFF", 14)], "sheen")], matte="alpha")
    comp.layer("face", [group([face, gradient_fill([(0, "#FFFFFF", 0.0), (1, "#000000", 0.12)], (0, fc[1] - 165),
                                                   (0, fc[1] + 165))], "shade"),
                        group([face, fill(slot="background")], "f"),
                        group([rect((588, 358), fc, 38), fill(slot="accent")], "bezel"),
                        group([rect((588, 358), (fc[0], fc[1] + 12), 38), fill("#000000", 26)], "sh")])
    return comp, {"label": (fc[0] - 200, 408, 400, 56)}


# ---------------------------------------------------------------- neon LED

def neon():
    """LED signal meter: columns of neon segments light up green, amber and red as the level bounces."""
    W, H = 720, 460
    comp = Comp("volume-meter--neon", W, H, fps=30, frames=F)
    slots(comp, NEON | {"primary": "#3DFF8B", "accent": "#FFD23D", "secondary": "#FF3D6E"},
          "primary", "accent", "secondary", "background", "outline")
    cols, rows = 10, 11
    sw, sh, gx, gy = 42, 16, 16, 9
    base = 360
    x0 = W / 2 - (cols * sw + (cols - 1) * gx) / 2 + sw / 2
    for i in range(cols):
        fn = level_fn(level_keys(i * 11 + 3, 6, 0.25 + 0.2 * math.sin(math.pi * i / (cols - 1)), 1.0),
                      (0.2, 0.0, 0.3, 1.0))
        cx = x0 + i * (sw + gx)
        for r in range(rows):
            cy = base - r * (sh + gy)
            s = "primary" if r < 7 else ("accent" if r < 9 else "secondary")
            thr = (r + 0.5) / rows
            ks, prev = [], None
            for f in range(0, F + 1):
                on = 100 if fn(f) >= thr else 0
                if on != prev:
                    ks.append((f, on, HOLD))
                    prev = on
            if ks[-1][0] != F:
                ks.append((F, ks[0][1], HOLD))
            seg = rect((sw, sh), (cx, cy), 4)
            if len(ks) > 1:
                comp.layer(f"led{i}-{r}", soft_glow([seg], slot=s, spread=(10, 20), ops=(24, 8)), opacity=anim(ks))
            elif ks[0][1]:
                comp.layer(f"led{i}-{r}", soft_glow([seg], slot=s, spread=(10, 20), ops=(24, 8)))
            comp.layer(f"off{i}-{r}", [group([seg, fill(slot=s, opacity=12)], "o")])
    neon_panel(comp, 16, 16, W - 32, H - 32, r=30)
    return comp, {"label": (W / 2 - 220, base + 26, 440, 44)}


b, ba = bars()
v, va = vu()
n, na = neon()
build_asset(CAT, "volume-meter", "Volume Meter",
            "A looping audio level meter that bounces to an imaginary beat. Put a caption such as the track or "
            "speaker name in the 'label' area.",
            ["volume", "audio", "meter", "equalizer", "vu", "sound", "music", "signal"], [
    V("bars", "Equalizer Bars", b, "loop", text_area=ba["label"], text_areas=ba, thumb_t=0.3,
      description="Rounded equalizer bars bounce with peak-hold caps drifting down."),
    V("vu", "Analog VU", v, "loop", text_area=va["label"], text_areas=va, thumb_t=0.3,
      description="Retro analog VU meter: cream face, red zone and a swinging needle."),
    V("neon", "Neon LED", n, "loop", text_area=na["label"], text_areas=na, thumb_t=0.3,
      description="Dark panel with columns of neon LED segments lighting green, amber and red."),
])
