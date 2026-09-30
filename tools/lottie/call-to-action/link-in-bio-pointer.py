from _cta_actions import *

W, H = 560, 344
N = 60
C = (280, 76)  # chip centre
CW, CH = 500, 108
IC = (C[0] - CW / 2 + CH / 2, C[1])  # icon circle
TIP = (C[0] + 20, 156)
POKES = (0, 30)


def chain(slot, width=6):
    link = lambda x: group([rect((50, 24), roundness=12), stroke(slot=slot, width=width)], "link", position=(x, 0))
    return [group([link(-16), link(16)], "chain", rotation=-45)]


def make(style):
    comp = Comp(f"link-in-bio-pointer--{style}", W, H, fps=30, frames=N)
    comp.slot("primary", "#6C5CE7")
    if style == "outline":
        comp.slot("outline", "#FFFFFF")
    else:
        comp.slot("background", "#FFFFFF")
    hand_slots(comp, style)
    ico = "outline" if style == "outline" else "icon"
    # hand pokes up at the chip twice per loop
    down, up = [TIP[0], TIP[1] + 26], list(TIP)
    pos = []
    for t in POKES:
        pos += [(t, down, EASE_IN), (t + 7, up, EASE_OUT), (t + 11, up, EASE_IN_OUT)]
    pos.append((N, down))
    hand(comp, style, position=anim(pos), scale=(72, 72), rotation=8)
    # chip nudges when poked
    nudge = [(0, [0, 0], LINEAR)]
    for t in POKES:
        nudge += [(t + 6, [0, 0], EASE_OUT), (t + 9, [0, -7], EASE_IN_OUT), (t + 18, [0, 0], LINEAR)]
    nudge.append((N, [0, 0]))
    chip = comp.null("chip", position=anim(nudge))
    wig = anim([(0, 0, LINEAR), (6, 0, EASE_OUT), (10, -14, EASE_IN_OUT), (16, 9, EASE_IN_OUT), (22, -4, EASE_IN_OUT),
                (27, 0, LINEAR), (36, 0, EASE_OUT), (40, -14, EASE_IN_OUT), (46, 9, EASE_IN_OUT), (52, -4, EASE_IN_OUT),
                (57, 0, LINEAR), (N, 0)])
    comp.layer("chain", chain(ico), parent=chip, position=IC, rotation=wig)
    if style == "outline":
        body(comp, "icon-disc", [ellipse((CH - 22, CH - 22))], style, parent=chip, position=IC, line=5,
             line_slot="primary")
        body(comp, "chip", [pill(CW, CH)], style, parent=chip, position=C, line=5)
    else:
        body(comp, "icon-disc", [ellipse((CH - 22, CH - 22))], style, parent=chip, position=IC, depth=6,
             shadow=False)
        shine(comp, [pill(CW, CH)], C, 8, 30, CW / 2 + 80, N, parent=chip)
        body(comp, "chip", [pill(CW, CH)], style, slot="background", parent=chip, position=C, depth=10)
    return comp


TEXT = (IC[0] + CH / 2, C[1] - CH * 0.3, CW - CH - CH * 0.4, CH * 0.6)

build_asset(CATEGORY, "link-in-bio-pointer", "Link In Bio Pointer",
            "A link chip with a chain icon and a cartoon finger poking up at it; seamless loop. "
            "Type \"Link in bio\" or your URL inside the chip.",
            ["link", "bio", "link in bio", "url", "pointer", "finger", "loop"], [
    Variant(s, STYLE_NAMES[s], make(s), "loop", thumb_t=0.2, text_area=TEXT, description=STYLE_DESC[s])
    for s in STYLES])
