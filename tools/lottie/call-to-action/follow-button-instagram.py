from _common import *

W, H = 680, 290
N = 120
comp = Comp("follow-button-instagram", W, H, fps=30, frames=N)
comp.slot("primary", "#0095F6")
comp.slot("secondary", "#363636")

Y = 124
IS = 128  # icon size
ICON = (24 + IS / 2, Y)
PL, PW, PH = ICON[0] + IS / 2 + 22, 470, 112
PILL = (PL + PW / 2, Y)
CLICK = 46
OUTRO = 96
comp.marker("intro", 0, 84)
comp.marker("outro", OUTRO, N - OUTRO)

tip = (PILL[0] + 150, Y + 16)
cursor(comp, [(20, [W + 60, H + 80], DECEL), (40, list(tip), EASE_IN_OUT), (CLICK + 20, list(tip), EASE_IN),
              (CLICK + 36, [W + 60, H + 80])], [CLICK], ip=20, op=CLICK + 38, scale=4.0)


def out(keys, t0):
    return keys + [(t0, [100, 100], EASE_OUT), (t0 + 5, [106, 106], EASE_IN), (t0 + 15, [0, 0], LINEAR)]


# ---------------------------------------------------------------- Instagram app icon
ig = comp.layer("instagram", [
    group([rect((78, 78), roundness=24), stroke("#FFFFFF", width=9.5),
           trim(end=anim([(6, 0, SNAP_OUT), (22, 100)]), offset=anim([(6, 90, SNAP_OUT), (22, 0)]))], "frame"),
    group([ellipse((38, 38)), stroke("#FFFFFF", width=9.5), trim(end=anim([(10, 0, SNAP_OUT), (24, 100)]))], "lens",
          rotation=-90),
    group([ellipse((12, 12)), fill("#FFFFFF")], "flash", position=(21, -21),
          scale=anim([(14, [0, 0], SPRING), (24, [100, 100])])),
    group([rect((IS, IS), roundness=34),
           gradient_fill([(0, "#FEDA75"), (0.22, "#FA7E1E"), (0.48, "#D62976"), (0.74, "#962FBF"), (1, "#4F5BD5")],
                         (-IS * 0.42, IS * 0.62), (IS * 0.55, -IS * 0.75), radial=True)], "tile"),
], position=ICON, rotation=anim([(0, -18, SNAP_OUT), (16, 0, HOLD), (CLICK + 4, 0, EASE_IN_OUT), (CLICK + 10, -8, EASE_IN_OUT),
                                 (CLICK + 18, 4, EASE_IN_OUT), (CLICK + 26, 0)]),
    scale=anim(out([(0, [0, 0], SPRING), (15, [100, 100], LINEAR), (CLICK + 3, [100, 100], EASE_IN_OUT),
                    (CLICK + 10, [110, 110], EASE_IN_OUT), (CLICK + 22, [100, 100], LINEAR)], OUTRO + 3)))
comp.layer("icon-shadow", [rect((IS, IS), roundness=34), fill("#000000", 22)], parent=ig, position=(0, 7))

# ---------------------------------------------------------------- pill slides out from behind the icon
button = comp.null("button", position=PILL, scale=anim(out([
    (CLICK - 3, [100, 100], EASE_IN), (CLICK, [96, 90], SNAP_OUT), (CLICK + 3, [96, 90], OVERSHOOT),
    (CLICK + 15, [100, 100], LINEAR)], OUTRO)))
grow = [(6, 0, DECEL), (26, 1, LINEAR)]


def pill_grow():
    return rect(anim([(t, [PH + (PW - PH) * v, PH], e) for t, v, e in grow]), roundness=PH / 2,
                position=anim([(t, [-(PW - PH) * (1 - v) / 2, 0], e) for t, v, e in grow]))


LOCAL_TIP = (tip[0] - PILL[0], tip[1] - PILL[1])
click_wipe(comp, [pill(PW, PH)], LOCAL_TIP, CLICK, "secondary", parent=button)
comp.layer("pill", [group([pill_grow(), fill(slot="primary")], "pill")], parent=button, op=CLICK + 13,
           opacity=anim([(6, 0, EASE_OUT), (9, 100)]))
comp.layer("shadow", [group([pill_grow(), fill("#000000", 20)], "pill")], parent=button, position=(0, 7),
           opacity=anim([(6, 0, EASE_OUT), (9, 100)]))

build(comp, "follow-button-instagram", "Follow Button Instagram",
      "Instagram app icon with a blue follow pill that slides out; a pointer clicks it and it turns grey. "
      "Put your own \"Follow\" text inside the pill.",
      ["follow", "instagram", "button", "click", "cursor", "social"], "intro-hold-outro",
      text_area=(PL + 36, Y - PH / 2 + 20, PW - 72, PH - 40), thumb_t=0.34)
