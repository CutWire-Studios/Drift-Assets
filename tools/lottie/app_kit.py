"""Helpers for app-ui assets: avatar placeholders, pop-in wrappers, text-area bookkeeping."""

from ui_kit import *
from os_icons import *
from devices_kit import rrect_path, soft_shadow

CAT = "app-ui"


def avatar(cx, cy, d, slot="secondary", fg="icon", fg_opacity=55, ring=None, name="avatar"):
    """Round placeholder avatar: a disc with a head and shoulders silhouette."""
    items = [group([ellipse((d * 0.30, d * 0.30), (cx, cy - d * 0.10)), fill(slot=fg, opacity=fg_opacity)], "head"),
             group([path(arc(d * 0.30, 180, 360, (cx, cy + d * 0.34)), "shoulders"), fill(slot=fg, opacity=fg_opacity)], "body"),
             group([ellipse((d, d), (cx, cy)), fill(slot=slot)], "disc")]
    if ring:
        items.append(group([ellipse((d + 8, d + 8), (cx, cy)), stroke(slot=ring, width=4)], "ring"))
    return group(items, name)


def pop_from(comp, name, shapes, pivot, delay=0, dur=14, spring=OVERSHOOT, off=(0, 0), **kw):
    """Layer that scales in from `pivot` (with an optional slide from `off`) and fades in."""
    px, py = pivot
    pos = Anim([(delay, [px + off[0], py + off[1]], EXPO_OUT), (delay + dur, [px, py])]) if off != (0, 0) else (px, py)
    return comp.layer(name, shapes, anchor=pivot, position=pos,
                      scale=Anim([(delay, [0, 0], spring), (delay + dur, [100, 100])]),
                      opacity=Anim([(0, 0, HOLD), (delay, 0, EASE_OUT), (delay + 4, 100)]), ip=0, **kw)


def slide_up(comp, name, shapes, y_from=80, delay=0, dur=16, **kw):
    return comp.layer(name, shapes, position=Anim([(delay, [0, y_from], EXPO_OUT), (delay + dur, [0, 0])]),
                      opacity=fade(delay, delay + 8), **kw)


def dots_typing(cx, cy, gap, r, F, slot="icon", lo=45, hi=100, lift=0.9, name="typing"):
    """Three dots that rise and brighten in sequence; one seamless cycle over F frames."""
    out = []
    for i in range(3):
        pk, ok = [], []
        for t in range(0, F + 1, 2):
            ph = ((t / F) - i * 0.14) % 1.0
            w = max(0.0, math.sin(math.pi * ph * 1.6)) if ph < 0.625 else 0.0
            pk.append((t, [0, -r * lift * w], LINEAR))
            ok.append((t, lo + (hi - lo) * w, LINEAR))
        out.append(group([ellipse((r * 2, r * 2), (cx + (i - 1) * gap, cy)), fill(slot=slot)], f"dot{i}",
                         position=Anim(pk), opacity=Anim(ok)))
    return out
