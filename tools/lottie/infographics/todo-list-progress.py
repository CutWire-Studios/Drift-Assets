from _common import *

W, H, F = 700, 640, 105
PX, PW = 70, 560           # progress bar x, width
PY, PH = 138, 20
ROWS = [236, 332, 428, 524]
BX = 104                   # checkbox centre x
DONE = 3                   # rows ticked off (of 4)


def tick_t(i):
    return 26 + i * 18


def step_keys(x, cy, w, h, e=SNAP_OUT):
    """Size/position keys for a left-anchored pill stepping 0 -> 1/4 -> ... as rows tick off."""
    fr = [0.0] + [(i + 1) / len(ROWS) for i in range(DONE)]
    sk, pk = [], []
    t_prev = 0
    for i in range(DONE + 1):
        wv = max(h, w * fr[i])
        if i == 0:
            sk.append((0, [h, h], HOLD))
            pk.append((0, [x + h / 2, cy], HOLD))
            continue
        t = tick_t(i - 1) + 4
        sk += [(t, [max(h, w * fr[i - 1]), h], e), (t + 14, [wv, h], HOLD)]
        pk += [(t, [x + max(h, w * fr[i - 1]) / 2, cy], e), (t + 14, [x + wv / 2, cy], HOLD)]
    sk.append((F, sk[-1][1]))
    pk.append((F, pk[-1][1]))
    return rect(anim(sk), anim(pk), h / 2)


def areas(dx=0):
    d = {"title": (PX + dx, 44, 380, 60), "value": (PX + PW - 150 + dx, 44, 150, 60)}
    for i, y in enumerate(ROWS):
        d[f"item{i + 1}"] = (BX + 44 + dx, y - 28, PX + PW - BX - 44, 56)
    return d


def row_in(i):
    t = 6 + i * 4
    return t, keys((t, [-40, 0], EXPO_OUT), (t + 16, [0, 0])), fade(t, t + 8)


def flat():
    """White card: rows slide in, checkboxes fill and tick in turn while the bar steps to 75%."""
    comp = Comp("todo-list-progress", W, H, fps=30, frames=F)
    slots(comp, FLAT | {"outline": "#C9CEDC"}, "primary", "background", "outline", "icon")
    card = rig(comp, "card", (W / 2, H / 2), scale=keys((0, [92, 92], SOFT_SPRING), (16, [100, 100])))
    for i, y in enumerate(ROWS):
        t0, off, op = row_in(i)
        c = (BX, y)
        if i < DONE:
            t = tick_t(i)
            comp.layer(f"tick{i}", [group([tick_shape(c, 1.25), trim(end=keys((t + 3, 0, EASE_OUT), (t + 11, 100))),
                                           stroke(slot="background", width=6)], "tick")], parent=card, ip=t)
            comp.layer(f"box{i}", [group([rect((44, 44), c, 12), fill(slot="icon")], "b")], parent=card,
                       anchor=c, position=c, scale=keys((t, [30, 30], SPRING), (t + 12, [100, 100])), ip=t)
            ring_pulse(comp, c, t + 2, 26, 50, slot="icon", width=3, dur=14, name=f"pulse{i}", parent=card)
        lay(comp, f"row{i}", [group([rect((44, 44), c, 12), stroke(slot="outline", width=3.5)], "empty"),
                              box(PX, y + 44, PW, 2, slot="outline", opacity=45, name="rule")],
            off=off, opacity=op, parent=card)
    comp.layer("bar", [group([step_keys(PX, PY, PW, PH), fill(slot="primary")], "fill")], parent=card,
               opacity=fade(8, 14))
    comp.layer("track", [group([rect((PW, PH), (PX + PW / 2, PY), PH / 2), fill(slot="outline", opacity=40)], "t")],
               parent=card, anchor=(PX, PY), position=(PX, PY), scale=keys((4, [0, 100], EXPO_OUT), (22, [100, 100])))
    comp.layer("card", [group([rect((W - 40, H - 40), (W / 2, H / 2), 30), fill(slot="background")], "c"),
                        group([rect((W - 40, H - 40), (W / 2, H / 2 + 10), 30), fill("#000000", 22)], "s")],
               parent=card, opacity=fade(0, 5))
    return comp


def neon():
    """Dark panel with round glowing checkboxes; each tick flares and the neon bar steps up."""
    comp = Comp("todo-list-progress--neon", W, H, fps=30, frames=F)
    slots(comp, NEON, "primary", "secondary", "background", "outline")
    for i, y in enumerate(ROWS):
        t0, off, op = row_in(i)
        c = (BX, y)
        if i < DONE:
            t = tick_t(i)
            comp.layer(f"tick{i}", [group([tick_shape(c, 1.1), trim(end=keys((t + 3, 0, EASE_OUT), (t + 11, 100))),
                                           stroke(slot="background", width=6)], "tick")], ip=t)
            comp.layer(f"dot{i}", soft_glow([ellipse((44, 44), c)], slot="secondary", spread=(14, 30), ops=(26, 10)),
                       anchor=c, position=c, scale=keys((t, [20, 20], SPRING), (t + 12, [100, 100])), ip=t)
            ring_pulse(comp, c, t + 2, 26, 56, slot="secondary", width=3, dur=16, name=f"pulse{i}")
            comp.layer(f"rule-lit{i}", [box(BX + 40, y + 42, PX + PW - BX - 40, 2, slot="secondary", opacity=60)],
                       anchor=(BX + 40, y), position=(BX + 40, y),
                       scale=keys((t + 2, [0, 100], EXPO_OUT), (t + 22, [100, 100])), ip=t + 2)
        lay(comp, f"row{i}", glow_strokes([ellipse((44, 44), c)], slot="outline", width=3, core=False, widths=(14,),
                                          ops=(14,))
            + [box(PX, y + 42, PW, 2, slot="outline", opacity=18, name="rule")], off=off, opacity=op)
    bar = step_keys(PX, PY, PW, PH - 4)
    comp.layer("bar", soft_glow([bar], slot="primary", spread=(12, 26), ops=(26, 10)), opacity=fade(8, 14))
    comp.layer("track", glow_strokes([rect((PW + 12, PH + 8), (PX + PW / 2, PY), (PH + 8) / 2)], slot="primary",
                                     width=2, core=False, widths=(12,), ops=(10,),
                                     extra=[trim(end=keys((2, 0, EASE_IN_OUT), (22, 100)))]))
    neon_panel(comp, 20, 20, W - 40, H - 40, r=34)
    return comp


def sketch():
    """Notepad page: hand-drawn boxes get big ink ticks and a marker bar scribbles along in steps."""
    comp = Comp("todo-list-progress--sketch", W, H, fps=30, frames=F)
    slots(comp, SKETCH, "primary", "background", "outline", "icon")
    paper = Paper(comp, 24, 20, W - 48, H - 40, tilt=-1.0, r=10, lines=None)
    card = paper.rig
    for i, y in enumerate(ROWS):
        c = (BX, y)
        t0 = 6 + i * 4
        if i < DONE:
            t = tick_t(i)
            ck = wobble([(c[0] - 16, c[1] - 2), (c[0] - 3, c[1] + 16), (c[0] + 28, c[1] - 30)], 1.0, i, step=20)
            comp.layer(f"tick{i}", [ink([ck], width=7, slot="icon", color="#35C27A", draw=(t, t + 8, EASE_OUT))],
                       parent=card, ip=t)
        comp.layer(f"box{i}", [ink([sketch_rect_pts(c[0] - 20, c[1] - 20, 40, 40, seed=i, amp=1.4, over=5, step=20)],
                                   width=4, draw=(t0, t0 + 12))], parent=card)
        comp.layer(f"rule{i}", [ink([wobble([(PX, y + 44), (PX + PW, y + 44)], 1.0, 20 + i)], width=2, opacity=22,
                                    draw=(t0 + 2, t0 + 16))], parent=card)
    # progress: hand-drawn outline + scribble revealed in steps
    comp.layer("bar-outline", [ink([sketch_rect_pts(PX, PY - 14, PW, 28, seed=8, amp=1.6)], width=4, draw=(2, 20))],
               parent=card)
    sp = scribble_pts(PX + 8, PY - 5, PW - 16, 10, spacing=10, slant=14, seed=3)
    ek = [(0, 0, HOLD)]
    for i in range(DONE):
        t = tick_t(i) + 6
        ek += [(t, 100 * i / 4, EASE_IN_OUT), (t + 12, 100 * (i + 1) / 4, HOLD)]
    ek.append((F, ek[-1][1]))
    comp.layer("bar", [group([polyline(sp), trim(end=anim(ek)), stroke(slot="primary", width=12, opacity=88)], "m")],
               parent=card)
    comp.layer("margin", [ink([wobble([(PX - 20, 110), (PX - 22, H - 40)], 1.0, 40)], width=2, color="#FF5A4E",
                              slot=None, opacity=35, draw=(0, 16))], parent=card)
    paper.sheet()
    return comp


A = areas()
build_asset(CAT, "todo-list-progress", "To-do List Progress",
            "A four-item checklist whose rows tick off one by one while a progress bar at the top steps up to 75%. "
            "Put the list name in 'title', the percentage in 'value' and each task in 'item1'-'item4'.",
            ["todo", "checklist", "tasks", "progress", "list", "checkbox", "infographic", "goals"], [
    V("flat", "Flat Card", flat(), "intro-hold", text_area=A["title"], text_areas=A, thumb_t=0.95,
      description="White card; checkboxes fill and tick in turn while the bar steps up."),
    V("neon", "Neon", neon(), "intro-hold", text_area=A["title"], text_areas=A, thumb_t=0.95,
      description="Dark panel with round glowing checkboxes that flare as they tick; the neon bar steps up."),
    V("sketch", "Notepad", sketch(), "intro-hold", text_area=A["title"], text_areas=A, thumb_t=0.95,
      description="Notepad page with hand-drawn boxes, big ink ticks and a marker bar scribbled in steps."),
])
