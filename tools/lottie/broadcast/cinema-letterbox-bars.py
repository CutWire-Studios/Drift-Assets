from _broadcast2 import *

W, H = 1920, 1080
F = 90
INTRO, OUTRO = 24, 66
BAR = round((H - W / 2.39) / 2, 1)  # 2.39:1 picture between the bars
CAPTION = (360, round(H - BAR + 30), 1200, round(BAR - 60))
TITLE = (360, 30, 1200, round(BAR - 60))
FILM_AREAS = {"title": (360, 58, 1200, round(BAR - 80)), "caption": (360, round(H - BAR + 22), 1200, round(BAR - 80))}


def base(name):
    c = Comp(name, W, H, fps=30, frames=F)
    c.marker("intro", 0, INTRO)
    c.marker("outro", OUTRO, F - OUTRO)
    return c


def slide(sign, ein=INOUT, eout=INOUT, t0=0, t1=INTRO, t2=OUTRO, t3=F):
    d = -BAR * sign
    return keys((t0, [0, d], ein), (t1, [0, 0], HOLD), (t2, [0, 0], eout), (t3, [0, d]))


def classic():
    """Plain black bars glide in from top and bottom to a 2.39:1 frame, hold, then glide out."""
    comp = base("cinema-letterbox-bars")
    comp.slot("background", "#000000")
    comp.layer("top", [box(0, 0, W, BAR, slot="background")], position=slide(1))
    comp.layer("bottom", [box(0, H - BAR, W, BAR, slot="background")], position=slide(-1))
    return comp


def accent():
    """Bars snap in with a small overshoot and a thin accent line draws out from the centre along each edge."""
    comp = base("cinema-letterbox-bars--accent")
    comp.slot("background", "#050505")
    comp.slot("accent", "#E3B04B")
    for name, y, sign in (("top", BAR - 2, 1), ("bottom", H - BAR + 2, -1)):
        pos = keys((0, [0, -BAR * sign], EXPO_OUT), (16, [0, 6 * sign], EASE_IN_OUT), (INTRO, [0, 0], HOLD),
                   (OUTRO + 6, [0, 0], EXPO_IN), (F, [0, -(BAR + 6) * sign]))
        tr = trim(start=keys((10, 50, EXPO_OUT), (30, 0, HOLD), (OUTRO, 0, EXPO_IN), (OUTRO + 12, 50)),
                  end=keys((10, 50, EXPO_OUT), (30, 100, HOLD), (OUTRO, 100, EXPO_IN), (OUTRO + 12, 50)))
        comp.layer(f"{name} line", [group([polyline([(0, y), (W, y)]), tr, stroke(slot="accent", width=6,
                                                                                    cap="butt")], "line")],
                   position=pos)
        comp.layer(f"{name} line glow", [group([polyline([(0, y), (W, y)]), tr, stroke(slot="accent", width=18,
                                                                                         opacity=20, cap="butt")],
                                               "glow")], position=pos)
        comp.layer(name, [box(0, 0 if sign == 1 else H - BAR, W, BAR, slot="background")], position=pos)
    return comp


def film():
    """Film-strip bars: sprocket holes run along the outer edges while the bars slide in and hold."""
    comp = base("cinema-letterbox-bars--film")
    comp.slot("background", "#0D0B09")
    comp.slot("outline", "#F2E6CF")
    pitch, hw, hh = 64, 34, 22
    n = W // pitch + 3
    run = keys((0, [pitch / 2, 0], LINEAR), (F, [pitch / 2 - pitch * 3, 0]))
    for name, sign in (("top", 1), ("bottom", -1)):
        y = 34 if sign == 1 else H - 34
        holes = [group([rect((hw, hh), (0, y), 5), fill(slot="outline", opacity=85), repeater(n, position=(pitch, 0))],
                       "holes", position=run)]
        edge_y = BAR - 3 if sign == 1 else H - BAR + 3
        pos = slide(sign)
        comp.layer(f"{name} holes", holes, position=pos)
        comp.layer(f"{name} edge", [group([polyline([(0, edge_y), (W, edge_y)]), stroke(slot="outline", width=2,
                                                                                         opacity=35, cap="butt")],
                                          "edge")], position=pos)
        comp.layer(name, [box(0, 0 if sign == 1 else H - BAR, W, BAR, slot="background")], position=pos)
    return comp


build_asset(CAT, "cinema-letterbox-bars", "Cinema Letterbox Bars",
            "Full-frame letterbox bars that slide in to a widescreen 2.39:1 picture, hold (stretchable) and slide "
            "out. Optional title and caption text areas sit inside the bars.",
            ["letterbox", "cinematic", "widescreen", "movie", "bars", "film", "2.39", "black bars"], [
    V("classic", "Classic", classic(), "intro-hold-outro", text_area=CAPTION,
      text_areas={"title": TITLE, "caption": CAPTION}, thumb_t=0.5, bg="6b7488",
      description="Plain bars glide in smoothly from top and bottom, hold, then glide out."),
    V("accent", "Accent Line", accent(), "intro-hold-outro", text_area=CAPTION,
      text_areas={"title": TITLE, "caption": CAPTION}, thumb_t=0.5, bg="6b7488",
      description="Bars snap in with a small overshoot; a thin gold line draws out from the centre along each edge."),
    V("film", "Film Strip", film(), "intro-hold-outro", text_area=FILM_AREAS["caption"],
      text_areas=FILM_AREAS, thumb_t=0.5, bg="6b7488",
      description="Film-strip bars with sprocket holes running along the outer edges."),
])
