"""Sticky note that flaps onto the screen, with room for a short note."""
from _callouts2 import *

W, H = 400, 420
N = 36
C = (W / 2, 216)
S = 300
FOLD = 46
TEXT = (C[0] - S / 2 + 34, C[1] - S / 2 + 58, S - 68, S - 110)


def note_pts(s=S, fold=FOLD):
    h = s / 2
    return [(-h, -h), (h, -h), (h, h - fold), (h - fold, h), (-h, h)]


def fold_pts(s=S, fold=FOLD):
    h = s / 2
    return [(h, h - fold), (h - fold - 4, h - fold - 6), (h - fold, h)]


def note_items(style, seed=1):
    body = [path(bezier(note_pts(), closed=True))]
    fold = [path(bezier(fold_pts(), closed=True))]
    band = [rect((S, 40), (0, -S / 2 + 20))]
    items = [group(fold + [fill("#000000", 22)], "fold-shade"),
             group(fold + [fill(slot="primary")], "fold"),
             group(band + [fill("#000000", 6)], "glue-band")]
    if style == "hand":
        line = wobble(closed_loop(dense(note_pts() + [note_pts()[0]]), 0.04, 3), 2.2, seed=seed, freq=2)
        fl = dense([fold_pts()[0], fold_pts()[1], fold_pts()[2]])
        items = [hand_static(fl, 6, "outline", seed=seed + 1, color=INK, taper=(0.1, 0.1), mins=(0.7, 0.7)),
                 hand_static(line, 7, "outline", seed=seed, color=INK, taper=(0.03, 0.05), mins=(0.6, 0.6),
                             wob=0.1)] + items
    items.append(group(body + [fill(slot="primary")], "paper"))
    return items


def shadow_items():
    return [group([path(bezier(note_pts(), closed=True)), fill("#000000", 30)], "s", position=(6, 12))]


def make(style):
    comp = Comp(f"sticky-note--{style}", W, H, frames=N + 6 if style == "pinned" else N)
    comp.slot("primary", {"classic": "#FFE066", "pinned": "#7FD6FF", "hand": "#FF9EC4"}[style])
    top = (C[0], C[1] - S / 2)
    if style == "classic":
        # hinged at the glue strip: the note swings down flat from above the screen
        flap = dict(anchor=(0, -S / 2), position=top,
                    scale=anim([(0, [100, 0], (0.5, 0.0, 0.9, 0.6)), (9, [100, 104], SETTLE), (14, [100, 97], SETTLE),
                                (19, [100, 100])]),
                    rotation=anim([(0, -10, SETTLE), (12, -1, SETTLE), (20, -3)]),
                    skew=anim([(0, 12, SETTLE), (10, -3, SETTLE), (18, 0)]), skew_axis=90)
        comp.layer("note", note_items(style), **flap)
        comp.layer("shadow", shadow_items(), **flap, opacity=anim([(4, 0, EASE_OUT), (14, 100)]))
    elif style == "pinned":
        comp.slot("accent", "#FF2D2D")
        pin = (C[0], top[1] + 26)
        comp.layer("pin", [group([ellipse((12, 8), (-6, -6)), fill("#FFFFFF", 70)], "shine"),
                           group([ellipse((34, 34)), fill(slot="accent")], "head"),
                           group([ellipse((34, 34)), fill("#000000", 35)], "shadow", position=(4, 8))],
                   position=pin, scale=anim([(0, [220, 220], (0.55, 0.0, 0.9, 0.6)), (6, [90, 90], SETTLE),
                                             (11, [100, 100])]),
                   opacity=anim([(0, 0, EASE_OUT), (3, 100)]))
        swing = dict(anchor=(0, -S / 2 + 26), position=pin,
                     rotation=anim([(5, -34, SETTLE), (13, 12, EASE_IN_OUT), (21, -7, EASE_IN_OUT),
                                    (28, 3, EASE_IN_OUT), (34, -1, EASE_IN_OUT), (40, 0)]),
                     scale=anim([(5, [70, 70], SETTLE), (14, [100, 100])]))
        comp.layer("note", note_items(style), **swing, opacity=anim([(5, 0, EASE_OUT), (9, 100)]), ip=5)
        comp.layer("shadow", shadow_items(), **swing, opacity=anim([(5, 0, EASE_OUT), (13, 100)]), ip=5)
    else:
        comp.slot("outline", INK)
        pop_ = dict(anchor=(0, 0), position=C, scale=squash_pop(0, 16),
                    rotation=anim([(0, 14, SETTLE), (10, -6, SETTLE), (16, 3, SETTLE), (22, 2)]))
        # a strip of tape doodled across the top
        tp = [(-60, -14), (60, -14), (60, 14), (-60, 14)]
        comp.layer("tape", [hand_static(wobble(closed_loop(dense(tp + [tp[0]]), 0.04, 2), 1.2, seed=9), 5, "outline",
                                        seed=5, color=INK, taper=(0.05, 0.05), mins=(0.7, 0.7)),
                            group([P(tp, True), fill("#FFFFFF", 70)], "t")],
                   position=(C[0] + 4, C[1] - S / 2 + 2), rotation=-6, ip=12,
                   scale=anim([(12, [150, 150], (0.55, 0.0, 0.9, 0.6)), (16, [95, 95], SETTLE), (20, [100, 100])]))
        comp.layer("note", note_items(style, 3), **pop_)
        comp.layer("shadow", shadow_items(), **pop_)
    return comp


build_asset(CATEGORY, "sticky-note", "Sticky Note",
            "A square sticky note that flaps onto the screen with a curled corner; write a short note "
            "on it.",
            ["sticky note", "note", "post-it", "memo", "reminder", "paper", "callout"], [
    Variant("classic", "Classic", make("classic"), "intro-hold", thumb_t=0.99, text_area=TEXT, bg="3b3b48",
            description="Yellow note hinged at its glue strip, swinging down flat onto the screen."),
    Variant("pinned", "Pinned", make("pinned"), "intro-hold", thumb_t=0.99, text_area=TEXT, bg="3b3b48",
            description="Blue note pinned up by a red push pin, swinging on it before it settles."),
    Variant("hand", "Doodle", make("hand"), "intro-hold", thumb_t=0.99, text_area=TEXT, bg="3b3b48",
            description="Pink note with a marker outline that bounces in, with a doodled tape strip."),
])
