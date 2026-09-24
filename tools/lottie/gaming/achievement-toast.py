from _common import *

W, H, F = 760, 160, 120
comp = Comp("achievement-toast", W, H, fps=30, frames=F)
comp.slot("background", "#17171E")
comp.slot("secondary", "#26262F")
comp.slot("accent", "#F2C230")
comp.slot("icon", "#F2C230")

CX, CY, CR = 80, H / 2, 58
PH, PW = 100, W - 30 - CX
OUT = 98
comp.marker("intro", 0, 44)
comp.marker("outro", OUT, F - OUT)


def pill(keys):
    size = anim([(t, [w, PH], e) for t, w, e in keys])
    pos = anim([(t, [CX + w / 2, CY], e) for t, w, e in keys])
    return rect(size, pos, PH / 2)


pill_keys = [(10, 0, SNAP_OUT), (26, PW, HOLD), (OUT, PW, ANTICIPATE), (OUT + 11, 0, HOLD), (F, 0, HOLD)]
pop = anim([(0, [0, 0], OVERSHOOT), (10, [100, 100], HOLD), (OUT + 8, [100, 100], ANTICIPATE),
            (OUT + 18, [0, 0])])

# sparkles around the medallion
for i, (dx, dy, s, t) in enumerate(((-44, -50, 18, 12), (52, -40, 13, 15), (-52, 38, 11, 18))):
    comp.layer(f"sparkle {i}", [group([star(4, s, s * 0.28), fill("#FFFFFF")], "sparkle")],
               position=(CX + dx, CY + dy),
               scale=anim([(t, [0, 0], SNAP_OUT), (t + 6, [100, 100], EASE_IN), (t + 16, [0, 0])]),
               rotation=anim([(t, -30, EASE_OUT), (t + 16, 60)]))

trophy = [
    group([star(5, 8, 3.6, position=(0, -12)), fill(slot="secondary")], "star"),
    group([*svg_shapes("M -20 -28 H 20 V -10 A 20 20 0 0 1 -20 -10 Z"),
           rect((9, 12), (0, 16)), rect((32, 8), (0, 27), 2), rect((22, 5), (0, 21), 1),
           fill(slot="icon")], "cup"),
    group([*svg_shapes("M -20 -21 H -29 V -14 C -29 -4 -22 0 -15 1"),
           *svg_shapes("M 20 -21 H 29 V -14 C 29 -4 22 0 15 1"),
           stroke(slot="icon", width=5, cap="round", join="round")], "handles"),
]
comp.layer("trophy", trophy, position=(CX, CY + 1),
           scale=anim([(5, [0, 0], OVERSHOOT), (15, [100, 100], HOLD), (OUT + 6, [100, 100], ANTICIPATE),
                       (OUT + 14, [0, 0])]),
           rotation=anim([(5, -25, OVERSHOOT), (17, 0)]))
comp.layer("ring", [group([ellipse((CR * 2 - 8, CR * 2 - 8)), stroke(slot="accent", width=4, cap="round"),
                           trim(end=anim([(3, 0, SNAP_OUT), (20, 100)]))], "ring", rotation=-90)],
           position=(CX, CY), scale=pop)
comp.layer("medallion", [
    group([ellipse((CR * 2, CR * 2)),
           gradient_fill([(0, "#FFFFFF", 0.16), (0.5, "#FFFFFF", 0.0), (1, "#000000", 0.2)],
                         (0, -CR), (0, CR))], "gloss"),
    group([ellipse((CR * 2, CR * 2)), fill(slot="secondary")], "disc"),
], position=(CX, CY), scale=pop)
comp.layer("shockwave", [group([ellipse(anim([(8, [CR * 2, CR * 2], SNAP_OUT), (26, [CR * 2.6, CR * 2.6])])),
                                stroke(slot="accent", width=anim([(8, 8, EASE_OUT), (26, 1)]))], "wave")],
           position=(CX, CY), opacity=anim([(7, 0, HOLD), (8, 90, EASE_IN), (26, 0)]))

comp.layer("glint matte", [group([pill(pill_keys), fill("#FFFFFF")], "m")], ip=24, op=50)
comp.layer("glint", [group([rect((70, 240)),
                            gradient_fill([(0, "#FFFFFF", 0.0), (0.5, "#FFFFFF", 0.3), (1, "#FFFFFF", 0.0)],
                                          (-35, 0), (35, 0))], "glint", rotation=22)],
           matte="alpha", ip=24, op=50, position=anim([(26, [CX + 40, CY], EASE_IN_OUT), (46, [W + 60, CY])]))
comp.layer("pill gloss", [group([pill(pill_keys),
                                 gradient_fill([(0, "#FFFFFF", 0.1), (0.5, "#FFFFFF", 0.0), (1, "#000000", 0.0)],
                                               (0, CY - PH / 2), (0, CY + PH / 2))], "gloss")], ip=11, op=OUT + 11)
comp.layer("pill", [group([pill(pill_keys), stroke("#FFFFFF", width=2, opacity=12), fill(slot="background")], "pill")], ip=11, op=OUT + 11)

finish(comp, "achievement-toast", "Achievement Toast",
       "Console-style achievement-unlocked toast: a trophy medallion pops in, a dark pill slides out "
       "from behind it and a glint sweeps across. Room for a title and a description in the pill.",
       ["achievement", "trophy", "unlocked", "toast", "notification", "gaming", "console"],
       "intro-hold-outro", text_area=[156, 40, 548, 80],
       text_areas={"title": [156, 40, 548, 38], "description": [156, 84, 548, 30]}, thumb_t=0.4, bg="e8e8ee", region=(12, 12, 440, 136))
