from _broadcast2 import *

F = 90          # 3 s, holds on the result
VALS = (0.64, 0.24, 0.12)


def grow_rect(x, cy, w_full, h, v, t0, t1, r):
    """Pill anchored at x that grows to v * w_full (keeps its rounded ends)."""
    w0, w1 = h, max(h, w_full * v)
    size = keys((t0, [w0, h], EXPO_OUT), (t1, [w1, h]))
    pos = keys((t0, [x + w0 / 2, cy], EXPO_OUT), (t1, [x + w1 / 2, cy]))
    return rect(size, pos, r)


def modern():
    """Three floating pill bars slide in and fill to their results; the leader gets a highlight colour."""
    W, H = 1000, 500
    comp = Comp("poll-bars", W, H, fps=30, frames=F)
    comp.slot("primary", "#4C7DFF")
    comp.slot("secondary", "#8A8FA3")
    comp.slot("background", "#FFFFFF")
    x0, bw, bh = 40, 920, 104
    areas = {}
    for i, v in enumerate(VALS):
        cy = 100 + i * 150
        t0 = 4 + i * 6
        slide = keys((t0, [-80, 0], EXPO_OUT), (t0 + 18, [0, 0]))
        op = fade(t0, t0 + 8)
        slot = "primary" if i == 0 else "secondary"
        if i == 0:
            lay(comp, "leader glow", [group([grow_rect(x0, cy, bw, bh, v, t0 + 12, t0 + 42, bh / 2),
                                             stroke(slot="primary", width=26, opacity=22)], "g")],
                off=slide, opacity=keys((t0 + 30, 0, EASE_OUT), (t0 + 44, 100)))
        lay(comp, f"fill{i}", [group([grow_rect(x0, cy, bw, bh, v, t0 + 12, t0 + 42, bh / 2),
                                      fill(slot=slot)], "fill")], off=slide, opacity=op)
        lay(comp, f"track{i}", [group([rect((bw, bh), (x0 + bw / 2, cy), bh / 2), fill(slot="background",
                                                                                         opacity=18)], "t"),
                                group([rect((bw, bh), (x0 + bw / 2, cy), bh / 2), stroke(slot="background", width=3,
                                                                                         opacity=30)], "e")],
            off=slide, opacity=op)
        areas[f"option{i + 1}"] = (x0 + 44, cy - 30, 600, 60)
        areas[f"value{i + 1}"] = (x0 + bw - 190, cy - 30, 160, 60)
    return comp, areas


def card():
    """White poll card with a question header, radio dots and thin bars; the winner's dot gets a check."""
    W, H = 920, 660
    comp = Comp("poll-bars--card", W, H, fps=30, frames=F)
    comp.slot("background", "#FFFFFF")
    comp.slot("primary", "#7B4DFF")
    comp.slot("secondary", "#D9D4E8")
    comp.slot("icon", "#FFFFFF")
    C = (W / 2, H / 2)
    cw, ch = 840, 580
    pl = rig(comp, "card", C, scale=keys((0, [86, 86], SPRING), (16, [100, 100])),
             opacity=keys((0, 0, EASE_OUT), (5, 100)))
    top = C[1] - ch / 2
    areas = {"question": (C[0] - cw / 2 + 50, top + 40, cw - 100, 90)}
    bx0, bw, bh = C[0] - cw / 2 + 50, cw - 100, 22
    for i, v in enumerate(VALS):
        ry = top + 180 + i * 130
        t0 = 12 + i * 6
        rc = (bx0 + 24, ry + 16)
        if i == 0:
            comp.layer("tick", [group([polyline([(rc[0] - 9, rc[1]), (rc[0] - 2, rc[1] + 7), (rc[0] + 10, rc[1] - 7)]),
                                       trim(end=keys((t0 + 34, 0, EASE_OUT), (t0 + 42, 100))),
                                       stroke(slot="icon", width=5)], "tick")], parent=pl)
            comp.layer("dot", [group([ellipse((36, 36), rc), fill(slot="primary")], "dot")], parent=pl,
                       anchor=rc, position=rc, scale=keys((t0 + 28, [0, 0], SPRING), (t0 + 40, [100, 100])))
        comp.layer(f"radio{i}", [group([ellipse((36, 36), rc), stroke(slot="secondary", width=4)], "r")],
                   parent=pl, opacity=fade(t0, t0 + 6))
        by = ry + 76
        comp.layer(f"fill{i}", [group([grow_rect(bx0, by, bw, bh, v, t0 + 4, t0 + 36, bh / 2),
                                       fill(slot="primary" if i == 0 else "secondary")], "f")], parent=pl,
                   opacity=fade(t0, t0 + 4))
        comp.layer(f"track{i}", [group([rect((bw, bh), (bx0 + bw / 2, by), bh / 2), fill("#EEEDF3")], "t")],
                   parent=pl, opacity=fade(t0, t0 + 6))
        areas[f"option{i + 1}"] = (bx0 + 64, ry - 10, bw - 250, 52)
        areas[f"value{i + 1}"] = (bx0 + bw - 160, ry - 10, 160, 52)
    comp.layer("divider", [box(C[0] - cw / 2 + 50, top + 146, cw - 100, 3, "#000000", opacity=8)], parent=pl)
    comp.layer("card", [group([rect((cw, ch), C, 36), fill(slot="background")], "card")], parent=pl)
    comp.layer("shadow", [group([rect((cw, ch), (C[0], C[1] + 14), 36), fill("#000000", 22)], "s"),
                          group([rect((cw + 20, ch + 20), (C[0], C[1] + 18), 46), fill("#000000", 10)], "s2")],
               parent=pl)
    return comp, areas


def para(x, y, w, h, k=22):
    """Parallelogram with its top edge shifted right by k."""
    return [(x + k, y), (x + w + k, y), (x + w - k, y + h), (x - k, y + h)]


def slanted():
    """TV-election style slanted bars: coloured label chips snap in and white result bars wipe across."""
    W, H = 1120, 500
    comp = Comp("poll-bars--slanted", W, H, fps=30, frames=F)
    comp.slot("primary", "#E8263B")
    comp.slot("secondary", "#1E6BFF")
    comp.slot("accent", "#FFC21A")
    comp.slot("background", "#14161F")
    comp.slot("icon", "#FFFFFF")
    areas = {}
    cx0, cw, bx0, bw, bh = 60, 300, 390, 680, 100
    slots = ("primary", "secondary", "accent")
    for i, v in enumerate(VALS):
        y = 50 + i * 140
        t0 = 3 + i * 5
        chip = polyline(para(cx0, y, cw, bh), closed=True)
        comp.layer(f"chip{i}", [group([chip, fill(slot=slots[i])], "chip"),
                                group([polyline(para(cx0 + 19.8, y, cw, 10, 2.2), closed=True), fill("#FFFFFF", 30)],
                                      "hi")],
                   anchor=(cx0, y + bh / 2), position=keys((t0, [cx0 - 120, y + bh / 2], EXPO_OUT),
                                                          (t0 + 14, [cx0, y + bh / 2])),
                   opacity=fade(t0, t0 + 4))
        wf = max(60, bw * v)
        k = 22
        pts0 = para(bx0, y, 40, bh, k)
        pts1 = para(bx0, y, wf, bh, k)
        shape = path(keys((t0 + 10, bezier(pts0), EXPO_OUT), (t0 + 40, bezier(pts1))))
        comp.layer(f"edge{i}", [group([polyline([(bx0 + wf + k - 3, y), (bx0 + wf - k - 3, y + bh)]),
                                       stroke(slot=slots[i], width=8, cap="butt")], "edge")],
                   position=keys((t0 + 10, [40 - wf, 0], EXPO_OUT), (t0 + 40, [0, 0])),
                   opacity=fade(t0 + 10, t0 + 14))
        comp.layer(f"bar{i}", [group([shape, fill(slot="icon")], "bar")], opacity=fade(t0 + 10, t0 + 13))
        comp.layer(f"track{i}", [group([polyline(para(bx0, y, bw, bh), closed=True), fill(slot="background",
                                                                                         opacity=85)], "t")],
                   anchor=(bx0, y), position=(bx0, y), scale=keys((t0 + 4, [0, 100], EXPO_OUT), (t0 + 18, [100, 100])))
        areas[f"option{i + 1}"] = (cx0 + 30, y + 20, cw - 60, bh - 40)
        areas[f"value{i + 1}"] = (bx0 + bw - 190, y + 20, 160, bh - 40)
    return comp, areas


m, ma = modern()
c, ca = card()
s, sa = slanted()
build_asset(CAT, "poll-bars", "Poll Bars",
            "Three-option poll whose bars fill to their results, the leader highlighted. Each option has its "
            "own text areas for the answer (option1-3) and its percentage (value1-3).",
            ["poll", "vote", "survey", "results", "bars", "percent", "chart", "question"], [
    V("modern", "Floating Pills", m, "intro-hold", text_area=ma["option1"], text_areas=ma, thumb_t=0.95,
            description="Three floating pill bars slide in and fill; the leader glows in the highlight colour."),
    V("card", "Poll Card", c, "intro-hold", text_area=ca["question"], text_areas=ca, thumb_t=0.95,
            bg="3a3f52",
            description="White card with a question header, radio dots and thin bars; the winner gets a check."),
    V("slanted", "Election Slant", s, "intro-hold", text_area=sa["option1"], text_areas=sa, thumb_t=0.95,
            description="TV-election style: slanted colour chips snap in and white result bars wipe across."),
])
