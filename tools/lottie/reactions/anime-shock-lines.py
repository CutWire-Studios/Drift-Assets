"""Anime shock lines: manga reaction marks. Radial focus lines that flicker around a clear centre,
jagged shock bolts that jolt out beside a head, or gloomy despair lines hanging down (loop)."""

from _reactions2 import *

T = 60
W, H = 500, 500
C = (250, 250)
INK = "#141414"
BOLT = "#FFE14D"


def radial(comp):
    comp.slot("primary", INK)
    r = rng(2)
    sets = 4
    for s in range(sets):
        shapes = []
        for k in range(46):
            a = TAU * (k + r.uniform(-0.35, 0.35)) / 46
            r_in = r.uniform(150, 205)
            wdt = r.uniform(3, 9)
            ca, sa = math.cos(a), math.sin(a)
            nx, ny = -sa, ca
            p_in = (ca * r_in, sa * r_in)
            p_out = (ca * 380, sa * 380)
            shapes.append(path(bezier([p_in, (p_out[0] + nx * wdt, p_out[1] + ny * wdt),
                                       (p_out[0] - nx * wdt, p_out[1] - ny * wdt)])))
        keys = []
        for t in range(0, T, 3):
            keys.append((t, 100 if (t // 3) % sets == s else 0, HOLD))
        keys.append((T, keys[0][1], HOLD))
        comp.layer(f"lines{s}", [group(shapes + [fill(INK, slot="primary")])], position=C,
                   opacity=anim(keys),
                   scale=sampled(lambda t: [100 + 4 * math.sin(TAU * t / 15)] * 2, 0, T, 3))


BOLT_D = "M -10 -44 L 14 -44 L 4 -12 L 20 -12 L -12 46 L -4 6 L -20 6 Z"


def spikes(comp):
    comp.slot("primary", INK)
    comp.slot("accent", BOLT)
    # three bolts fanning out on each side of a head-sized clear centre
    for side in (-1, 1):
        for k, (a, sc) in enumerate(((-150, 0.9), (-180, 1.1), (-210, 0.85))):
            ang = a if side < 0 else 180 - a
            pos = (C[0] + math.cos(math.radians(ang)) * 170, C[1] - 20 + math.sin(math.radians(ang)) * 150)
            rot_ = ang - 90  # the bolt's tip (+y) points away from the centre

            def s_fn(t, k=k, sc=sc):
                u = t % 30
                v = back_out(clamp((u - k * 2) / 7), 2.4) if u < 22 else 1 - smooth((u - 22) / 6)
                return [100 * sc * v] * 2

            comp.layer(f"bolt{side}{k}", [group(S(BOLT_D) + [stroke(INK, 7, slot="primary"),
                                                            fill(BOLT, slot="accent")])],
                       position=sampled(lambda t, pos=pos: (pos[0] + 2.5 * math.sin(TAU * t / 4),
                                                            pos[1] + 2 * math.cos(TAU * t / 3)), 0, T),
                       rotation=rot_, scale=sampled(s_fn, 0, T))
    # small tension ticks above
    for k, x in enumerate((-40, 0, 40)):
        comp.layer(f"tick{k}", [group(S(capsule_d((0, -18), (0, 18), 6)) + [fill(INK, slot="primary")])],
                   position=(C[0] + x, 96 + abs(x) * 0.4), rotation=x * 0.5,
                   scale=sampled(lambda t, k=k: [100, 100 * (back_out(clamp(((t % 30) - 1 - k) / 6), 2.2)
                                                             if (t % 30) < 22 else 1 - smooth(((t % 30) - 22) / 6))], 0, T))


def gloom(comp):
    comp.slot("primary", "#4B3F8F")
    r = rng(6)
    n = 13
    for k in range(n):
        x = 70 + (W - 140) * k / (n - 1) + r.uniform(-6, 6)
        ln = r.uniform(170, 290) * (1 - 0.35 * abs(k - (n - 1) / 2) / ((n - 1) / 2))
        w_ = r.uniform(5, 9)
        ph = r.uniform(0, 1)
        line = [path(bezier([(0, 0), (0, ln)], closed=False)),
                trim(end=sampled(lambda t, ph=ph: 100 * (0.78 + 0.22 * math.sin(TAU * (t / T + ph))), 0, T, 3)),
                stroke("#4B3F8F", w_, slot="primary")]
        comp.layer(f"gloom{k}", [group(line)], position=(x, 36),
                   rotation=sampled(lambda t, ph=ph: 1.2 * math.sin(TAU * (t / T * 2 + ph)), 0, T, 3),
                   opacity=sampled(lambda t, ph=ph: 70 + 30 * math.sin(TAU * (t / T + ph + 0.25)), 0, T, 3))
    # a darker wash behind the lines
    comp.layer("wash", [group([ellipse((W - 30, 560)),
                               gradient_fill([(0, "#2B2455", 0.6), (0.6, "#2B2455", 0.25), (1, "#2B2455", 0)],
                                             (0, -120), (0, 280), radial=True)])],
               position=(W / 2, 0))


def make(style):
    comp = Comp("anime-shock-lines", W, 330 if style == "gloom" else H, frames=T)
    {"radial": radial, "spikes": spikes, "gloom": gloom}[style](comp)
    return comp


build3("anime-shock-lines", "Anime Shock Lines",
       "Manga reaction marks for shocked, stunned or crushed moments; place your subject or text in "
       "the clear centre. Seamless loop.",
       ["anime", "manga", "shock", "speed lines", "surprise", "gloom", "reaction"], make, [
           ("radial", "Focus Lines", "loop", 0.5, "Flickering radial speed lines around a clear centre.",
            "e8e8ee"),
           ("spikes", "Shock Bolts", "loop", 0.3, "Jagged bolts jolting out on both sides of a head.",
            "e8e8ee"),
           ("gloom", "Gloom Lines", "loop", 0.5, "Despair lines hanging down with a dark wash.",
            "e8e8ee"),
       ])
