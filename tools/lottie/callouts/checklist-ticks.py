"""Three checklist rows whose boxes get ticked one after another."""
from _callouts2 import *

W, H = 540, 380
N = 54
ROWS = [86, 190, 294]
BX = 66  # box centre x
B = 64   # box size
TICK = [(-20, 2), (-6, 18), (24, -20)]
TEXTS = {f"row{i + 1}": (BX + B / 2 + 26, y - 30, W - (BX + B / 2 + 26) - 20, 60) for i, y in enumerate(ROWS)}


def tick_time(i):
    return 14 + i * 12


def make(style):
    comp = Comp(f"checklist-ticks--{style}", W, H, frames=N)
    comp.slot("primary", "#22C55E")
    if style == "clean":
        comp.slot("outline", "#FFFFFF")
        comp.slot("icon", "#FFFFFF")
        for i, y in enumerate(ROWS):
            t = tick_time(i)
            comp.layer(f"tick{i}", [clean_line(TICK, 9, "icon", t0=t + 1, t1=t + 8, ease=SETTLE)], position=(BX, y),
                       ip=t + 1)
            comp.layer(f"fill{i}", [group([rect((B, B), roundness=16), fill(slot="primary")], "f")],
                       position=(BX, y), scale=pop(t, 9, 118), ip=t)
            comp.layer(f"box{i}", [group([rect((B - 6, B - 6), roundness=14), stroke(slot="outline", width=6)], "b")],
                       position=(BX, y), scale=pop(i * 3, 10, 115), ip=i * 3)
            comp.layer(f"line{i}", [group([P([(BX + B / 2 + 26, y), (W - 30, y)]), trim(0, draw(i * 3 + 2, i * 3 + 14)),
                                           stroke(slot="outline", width=3, opacity=25)], "l")],
                       ip=i * 3 + 2, opacity=anim([(t, 100, EASE_OUT), (t + 8, 0)]))
    elif style == "hand":
        comp.slot("outline", "#FFFFFF")
        strokes = []
        for i, y in enumerate(ROWS):
            box = wobble(closed_loop(rrect_pts((BX, y), B - 6, B - 6, 6, start=180), 0.06, 3), 1.8, seed=i, freq=1.5)
            strokes.append(hand_line(box, i * 4, i * 4 + 9, 7, "outline", seed=i + 1, chunks=2, taper=(0.05, 0.1),
                                     mins=(0.6, 0.4), wob=0.08, name=f"box{i}"))
        for i, y in enumerate(ROWS):
            t = tick_time(i)
            tk = dense(fillet([(BX - 26, y - 4), (BX - 4, y + 22), (BX + 44, y - 48)], 5, 4))
            strokes.append(hand_line(tk, t, t + 7, 19, "primary", seed=i + 7, taper=(0.12, 0.3), mins=(0.6, 0.3),
                                     wob=0.06, name=f"tick{i}"))
        emit(comp, strokes[::-1])
    else:
        comp.slot("outline", INK)
        comp.slot("background", "#FFFFFF")
        tick = [(x * 1.3, y * 1.3) for x, y in [(-30, -2), (-10, 18), (26, -26), (36, -16), (-10, 38), (-40, 8)]]
        for i, y in enumerate(ROWS):
            t = tick_time(i)
            comp.layer(f"tick{i}", comic([path(bezier(tick, closed=True)), round_corners(5)], "primary", "outline",
                                         "outline", width=6, shadow=(4, 5)),
                       position=(BX + 6, y - 4), scale=pop(t, 10, 135), rotation=anim([(t, -25, SETTLE), (t + 10, 0)]),
                       ip=t)
            comp.layer(f"box{i}", comic([rect((B, B), roundness=10)], "background", "outline", "outline", width=7,
                                        shadow=(6, 7)),
                       position=(BX, y), scale=pop(i * 3, 12, 118), ip=i * 3)
    return comp


build_asset(CATEGORY, "checklist-ticks", "Checklist Ticks",
            "Three checklist rows whose boxes get ticked one after another; type an item next to each box.",
            ["checklist", "check", "tick", "todo", "list", "done", "steps"], [
    Variant("clean", "Clean", make("clean"), "intro-hold", thumb_t=0.99, region=(10, 30, 310, 316), pad=0.04, text_area=TEXTS["row1"],
            text_areas=TEXTS, description="Rounded outline boxes that fill green as a white tick draws in."),
    Variant("hand", "Hand-Drawn", make("hand"), "intro-hold", thumb_t=0.99, region=(10, 30, 310, 316), pad=0.04, text_area=TEXTS["row1"],
            text_areas=TEXTS, description="Marker boxes with big green ticks swooshing out past their corners."),
    Variant("bold", "Comic", make("bold"), "intro-hold", thumb_t=0.99, region=(10, 30, 310, 316), pad=0.04, text_area=TEXTS["row1"], text_areas=TEXTS,
            bg="e8e8ee", description="Chunky outlined boxes with fat green ticks that stamp in."),
])
