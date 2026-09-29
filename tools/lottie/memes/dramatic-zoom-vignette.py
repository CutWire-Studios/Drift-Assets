"""Full-frame dramatic zoom: vignette closes in while radial speed lines snap towards the centre."""

from _memes2 import *

W, H = 1920, 1080
C = (W / 2, H / 2)
F, IN, OUT = 75, 12, 60
R_EDGE = 1180


def flicker(n_sets, t0, t1, every=2, fade_in=None, out=None):
    """Opacity keys per set: set i is visible on its own beat between t0 and t1."""
    res = []
    for i in range(n_sets):
        k = [(0, 0, HOLD)]
        t = t0
        j = 0
        while t < t1:
            k.append((t, 100 if j % n_sets == i else 0, HOLD))
            t += every
            j += 1
        k.append((t1, 100 if i == 0 else 0, HOLD if i else EASE_IN))
        k.append((F, 0))
        res.append(keys(*k))
    return res


def classic():
    """Dark vignette closes in with a punch and white anime speed lines flicker around the subject."""
    comp = base("dramatic-zoom-vignette", W, H, F, IN, OUT)
    comp.slot("primary", "#FFFFFF")
    zoom = keys((0, [170, 170], EXPO_OUT), (IN, [100, 100], LINEAR), (OUT, [96, 96], EXPO_IN), (F, [150, 150]))
    ops = flicker(3, 4, OUT)
    for i in range(3):
        comp.layer(f"lines{i}", [group(speed_lines(*C, 110, 400, R_EDGE, 26, seed=10 + i) + [fill(slot="primary")],
                                       "lines")],
                   anchor=C, position=C, scale=zoom, opacity=ops[i])
    comp.layer("ring", [group([ellipse((900, 900), C), stroke("#FFFFFF", width=anim([(4, 30, EASE_OUT), (16, 2)]))],
                              "ring")],
               anchor=C, position=C, scale=keys((4, [220, 220], EXPO_OUT), (16, [80, 80])),
               opacity=keys((4, 0, HOLD), (5, 60, EASE_IN), (16, 0)), ip=4, op=17)
    comp.layer("vignette", [vignette(W, H, 0.82, 0.3, mid=(0.62, "#000000", 0.38))],
               anchor=C, position=C,
               scale=keys((0, [190, 190], EXPO_OUT), (IN, [100, 100], LINEAR), (OUT, [100, 100], EASE_IN), (F, [180, 180])),
               opacity=keys((0, 0, EASE_OUT), (6, 100, HOLD), (OUT, 100, EASE_IN), (F, 0)))
    return comp


def iris():
    """Hard cinematic iris squeezes the frame down to a spotlight, with a bright rim and inward zoom rings."""
    comp = base("dramatic-zoom-vignette--iris", W, H, F, IN + 4, OUT)
    comp.slot("outline", "#FFFFFF")
    r = keys((0, [C[0] + 1250, C[1]], EXPO_OUT), (IN + 4, [C[0] + 580, C[1]], LINEAR),
             (OUT, [C[0] + 560, C[1]], EXPO_IN), (F, [C[0] + 1300, C[1]]))
    # inward zoom rings (whoosh)
    for i in range(4):
        t0 = 2 + i * 3
        comp.layer(f"whoosh{i}", [group([ellipse((1000, 1000), C), stroke(slot="outline", width=6, opacity=70)], "r")],
                   anchor=C, position=C, scale=keys((t0, [230, 230], EASE_IN), (t0 + 12, [90, 90])),
                   opacity=keys((t0, 0, LINEAR), (t0 + 4, 100, EASE_IN), (t0 + 12, 0)), ip=t0, op=t0 + 13)
    rim_s = keys((0, [260, 260], EXPO_OUT), (IN + 4, [100, 100], LINEAR), (OUT, [96, 96], EXPO_IN), (F, [276, 276]))
    comp.layer("rim", [group([ellipse((1000, 1000), C), stroke(slot="outline", width=5, opacity=90)], "rim"),
                       group([ellipse((1000, 1000), C), stroke(slot="outline", width=30, opacity=14)], "halo")],
               anchor=C, position=C, scale=rim_s,
               opacity=keys((0, 0, EASE_OUT), (8, 100, HOLD), (OUT, 100, EASE_IN), (F - 4, 0)))
    comp.layer("pulse", [group([ellipse((1000, 1000), C), stroke(slot="outline", width=3)], "p")],
               anchor=C, position=C, scale=keys((IN + 4, [100, 100], EASE_OUT), (IN + 30, [122, 122])),
               opacity=keys((IN + 4, 80, EASE_OUT), (IN + 30, 0)), ip=IN + 4, op=IN + 31)
    comp.layer("iris", [group([rect((W + 40, H + 40), C),
                               gradient_fill([(0, "#000000", 0), (0.84, "#000000", 0), (1, "#000000", 0.8)], C, r,
                                             radial=True)], "iris")],
               opacity=keys((0, 0, EASE_OUT), (5, 100, HOLD), (OUT, 100, EASE_IN), (F, 0)))
    return comp


def manga():
    """Dense black manga focus lines slam in and jitter every other frame; no vignette."""
    comp = base("dramatic-zoom-vignette--manga", W, H, F, IN, OUT)
    comp.slot("primary", "#0B0B0F")
    comp.slot("accent", "#E3262E")
    zoom = keys((0, [150, 150], EXPO_OUT), (IN - 4, [100, 100], LINEAR), (OUT, [100, 100], EXPO_IN), (F, [160, 160]))
    ops = flicker(2, 2, OUT, every=2)
    for i in range(2):
        comp.layer(f"focus{i}", [group(speed_lines(*C, 190, 470, R_EDGE, 16, seed=30 + i, wobble=0.35)
                                       + [fill(slot="primary")], "lines")],
                   anchor=C, position=C, scale=zoom, opacity=ops[i], rotation=i * 0.6)
    # a few thick accent streaks
    comp.layer("accent", [group(speed_lines(*C, 12, 560, R_EDGE, 46, seed=44, jitter=0.2)
                                + [fill(slot="accent")], "streaks")],
               anchor=C, position=C, scale=zoom,
               opacity=keys((0, 0, HOLD), (2, 100, HOLD), (OUT, 100, EASE_IN), (F - 5, 0)))
    return comp


build_asset(CAT, "dramatic-zoom-vignette", "Dramatic Zoom Vignette",
            "Full-frame dramatic zoom overlay: the edges darken and radial speed lines snap in around the "
            "centre, holding the tension before snapping back out. Keep your subject in the clear middle.",
            ["dramatic", "zoom", "speed lines", "vignette", "anime", "meme", "focus"], [
    Variant("classic", "Anime Lines", classic(), "intro-hold-outro", thumb_t=0.3,
            description="Dark vignette closes in and white anime speed lines flicker around the subject."),
    Variant("iris", "Iris Spotlight", iris(), "intro-hold-outro", thumb_t=0.3,
            description="A hard iris squeezes the frame to a spotlight with a bright rim and inward zoom rings."),
    Variant("manga", "Manga Focus", manga(), "intro-hold-outro", thumb_t=0.3, bg="e8e8ee",
            description="Dense black manga focus lines with red accent streaks that jitter; no darkening."),
])
