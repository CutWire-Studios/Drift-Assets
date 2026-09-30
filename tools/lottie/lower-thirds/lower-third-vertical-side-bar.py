from _lt2 import *

W, H = 1100, 250
BX, BY, BW, BH = 60, 30, 14, 190


def side_bar(comp, t0=0, t2=132, slot="accent", x=BX, w=BW, y=BY, h=BH):
    lay(comp, "side-bar", [rrect(x, y, w, h), fill(slot=slot)], (x, y + h),
        scale=keys((t0, [100, 0], (0.3, 1.3, 0.5, 1)), (t0 + 16, [100, 100], HOLD), (t2, [100, 100], EXPO_IN),
                   (t2 + 14, [100, 0])))


def slide_panel(comp, name, box, slot, t0, t1, t2, t3, opacity=100):
    """Panel that slides out to the right from behind x = box.x (clipped there)."""
    x, y, w, h = box
    comp.layer(f"{name}-matte", [rrect(x, y - 20, w + 40, h + 40), fill("#FFFFFF")])
    comp.layer(name, [rrect(*box), fill(slot=slot, opacity=opacity)], matte="alpha",
               position=slide(-w - 10, 0, t0, t1, t2, t3, EXPO_OUT, EXPO_IN))


def panel():
    comp = base("lower-third-vertical-side-bar", W, H, 40)
    comp.slot("accent", "#FF3D00")
    comp.slot("primary", "#FFFFFF")
    comp.slot("secondary", "#1C1C1C")
    side_bar(comp)
    px = BX + BW
    slide_panel(comp, "sub", (px, BY + 118, 540, 56), "secondary", 20, 42, 112, 128)
    slide_panel(comp, "head", (px, BY + 16, 860, 96), "primary", 12, 36, 118, 134)
    return comp, (px + 34, BY + 30, 800, 68), (px + 30, BY + 130, 490, 32)


def outline():
    comp = base("lower-third-vertical-side-bar--outline", W, H, 44)
    comp.slot("accent", "#00E5A0")
    comp.slot("outline", "#FFFFFF")
    comp.slot("secondary", "#00E5A0")
    side_bar(comp)
    px = BX + BW
    x0, y0, x1, y1 = px, BY + 16, px + 860, BY + 116
    frame = poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], False)
    comp.layer("frame", [frame, trim(end=keys((12, 0, INOUT), (40, 100, HOLD), (118, 100, INOUT), (136, 0))),
                         stroke(slot="outline", width=4, join="miter", cap="butt")])
    comp.layer("tag", [rect_grow(px, y1 + 12, 420, 50, 0, 26, 44, 112, 126, "left", start=0), fill(slot="secondary")])
    return comp, (px + 34, y0 + 18, 800, 64), (px + 26, y1 + 22, 380, 30)


def split():
    comp = base("lower-third-vertical-side-bar--split", W, H, 40)
    comp.slot("accent", "#FFC300")
    comp.slot("primary", "#0A2342")
    comp.slot("secondary", "#2CA58D")
    side_bar(comp, 0, 134)
    side_bar(comp, 4, 130, "secondary", x=BX + BW + 8, w=5, y=BY + 30, h=BH - 60)
    px = BX + BW + 13
    slide_panel(comp, "sub", (px, BY + 124, 480, 50), "secondary", 18, 40, 112, 128)
    slide_panel(comp, "head", (px, BY + 14, 850, 102), "primary", 10, 34, 118, 134)
    return comp, (px + 34, BY + 30, 790, 70), (px + 28, BY + 134, 430, 30)


a, ah, asub = panel()
b, bh, bs = outline()
c, chd, cs = split()
build("lower-third-vertical-side-bar", "Vertical Side Bar Lower Third",
      "A vertical accent bar springs up, then text panels slide out to the right from behind it. Put the name "
      "in the top panel and a subtitle in the lower one.",
      ["lower third", "vertical bar", "side bar", "slide", "clean", "name", "corporate"], [
          V("panel", "Slide Panels", a, ah, asub, bg="e8e8ee",
            description="Accent bar grows up, then white name and dark subtitle panels slide out from behind it."),
          V("outline", "Outline Frame", b, bh, bs,
            description="Instead of a filled panel, an outline frame draws out from the bar with a coloured tag below."),
          V("split", "Double Bar", c, chd, cs,
            description="Thick and thin accent bars side by side with separate headline and subtitle panels."),
      ])
