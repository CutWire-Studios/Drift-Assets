import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from app_kit import *

ONE, TWO = 92, 160     # bubble heights for one / two text lines
BW = 600


def whatsapp(side, h, F=60):
    W, H = BW + 120, h + 60
    comp = Comp("whatsapp-bubble", W, H, frames=F)
    comp.slot("primary", "#D9FDD3")      # sent
    comp.slot("secondary", "#FFFFFF")    # received
    comp.slot("icon", "#667781")         # time stamp
    comp.slot("accent", "#53BDEB")       # read ticks
    sent = side == "sent"
    x = 30 if not sent else W - 30 - BW
    y = 30
    r = 22
    if sent:
        body = rrect_path(x, y, BW, h, r, 0, r, r, "bubble")
        tail = [polyline([(x + BW - 1, y), (x + BW + 22, y), (x + BW - 1, y + 24)], closed=True)]
        pivot = (x + BW, y)
    else:
        body = rrect_path(x, y, BW, h, 0, r, r, r, "bubble")
        tail = [polyline([(x + 1, y), (x - 22, y), (x + 1, y + 24)], closed=True)]
        pivot = (x, y)
    col = "primary" if sent else "secondary"
    shapes = []
    t_x = x + BW - 22
    if sent:
        shapes += [group([polyline([(t_x - 20, y + h - 26), (t_x - 12, y + h - 18), (t_x + 4, y + h - 36)]), stroke(slot="accent", width=3.2, join="round")], "tick1"),
                   group([polyline([(t_x - 6, y + h - 26), (t_x + 2, y + h - 18)]), stroke(slot="accent", width=3.2, join="round")], "tick2")]
        shapes += [label("9:41", t_x - 34, y + h - 17, 22, 400, anchor="r")]
    else:
        shapes += [label("9:41", t_x, y + h - 17, 22, 400, anchor="r")]
    shapes += [group(body + tail + [fill(slot=col)], "bubble")]
    shapes = [group(shapes, "wa", opacity=100)]
    pop_from(comp, "bubble", shapes, pivot, 0, 14)
    comp.layer("shadow", [group(body + [fill("#000000", 10)], "sh")], position=(0, 3), opacity=fade(6, 14))
    area = (x + 22, y + 12, BW - 44, h - 50)
    return comp, area


def imessage(side, h, F=60):
    W, H = BW + 120, h + 60
    comp = Comp("imessage-bubble", W, H, frames=F)
    comp.slot("primary", "#0B84FE")
    comp.slot("secondary", "#E9E9EB")
    sent = side == "sent"
    x = 30 if not sent else W - 30 - BW
    y = 30
    r = 34
    d = rrect_d(x, y, BW, h, r, r, r, r)
    # curved tail at the bottom outer corner
    if sent:
        tx = x + BW
        d_tail = f"M{tx - 40},{y + h - 36} L{tx - 8},{y + h - 36} Q{tx - 8},{y + h - 6} {tx + 14},{y + h + 2} Q{tx - 20},{y + h + 4} {tx - 44},{y + h - 8} Z"
        pivot = (tx, y + h)
    else:
        tx = x
        d_tail = f"M{tx + 40},{y + h - 36} L{tx + 8},{y + h - 36} Q{tx + 8},{y + h - 6} {tx - 14},{y + h + 2} Q{tx + 20},{y + h + 4} {tx + 44},{y + h - 8} Z"
        pivot = (tx, y + h)
    col = "primary" if sent else "secondary"
    shapes = [group(svg_shapes(d_tail, name="tail") + [fill(slot=col)], "tail"),
              group(svg_shapes(d, name="body") + [fill(slot=col)], "bubble")]
    pop_from(comp, "bubble", shapes, pivot, 0, 14)
    return comp, (x + 30, y + 14, BW - 60, h - 28)


def messenger(side, h, F=60):
    W, H = BW + 200, h + 60
    comp = Comp("messenger-bubble", W, H, frames=F)
    comp.slot("primary", "#0084FF")
    comp.slot("secondary", "#E4E6EB")
    comp.slot("icon", "#FFFFFF")
    sent = side == "sent"
    x = 30 if not sent else W - 30 - BW
    if not sent:
        x += 66
    y = 30
    R = 36
    body = rrect_path(x, y, BW, h, R, R, 8 if sent else R, R if sent else 8, "bubble")
    col = "primary" if sent else "secondary"
    shapes = [group(body + [fill(slot=col)], "bubble")]
    pivot = (x + BW if sent else x, y + h)
    pop_from(comp, "bubble", shapes, pivot, 0, 14)
    if not sent:
        pop_from(comp, "avatar", [avatar(x - 34, y + h - 26, 52, slot="primary", fg="icon", fg_opacity=100)], (x - 34, y + h - 26), 4, 12)
    return comp, (x + 30, y + 14, BW - 60, h - 28)


def build(fn, asset_id, name, desc, tags):
    vs = []
    for side, h, vid, nm in (("sent", ONE, "sent", "Sent"), ("received", ONE, "received", "Received"),
                             ("sent", TWO, "sent-long", "Sent, Two Lines"), ("received", TWO, "received-long", "Received, Two Lines")):
        c, a = fn(side, h)
        vs.append(Variant(vid, nm, c, "intro-hold", text_area=a, thumb_t=0.95, bg="6a7087" if "messenger" not in asset_id else "6a7087"))
    build_asset(CAT, asset_id, name, desc, tags, vs)
