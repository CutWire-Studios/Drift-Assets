import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from app_kit import *

W, H = 1080, 1920
F = 45


def status(slot="icon", dark=False):
    base = 74
    out = [time_text("9:41", 96, base, 40, 600, slot=slot)]
    b, bw = battery(W - 88 - 62, base - 28, 62, 28, 0.8, slot=slot)
    wf, _ = wifi(W - 88 - 62 - 50, base, 42, slot=slot)
    cb, _ = cell_bars(W - 88 - 62 - 50 - 22 - 42 - 20, base, 28, slot=slot)
    return out + b + wf + cb


def layers(comp, header, body, footer, bar=230, foot=170):
    comp.layer("footer", footer, position=Anim([(4, [0, 160], EXPO_OUT), (22, [0, 0])]), opacity=fade(4, 14))
    comp.layer("header", header, position=Anim([(0, [0, -bar], EXPO_OUT), (18, [0, 0])]), opacity=fade(0, 10))
    comp.layer("body", body, opacity=fade(0, 16))


def doodles(seed=4, n=46, color="#000000", op=5):
    rng = random.Random(seed)
    out = []
    for i in range(n):
        x, y = rng.uniform(40, W - 40), rng.uniform(260, H - 260)
        k = i % 4
        s = rng.uniform(16, 30)
        if k == 0:
            out.append(group([ellipse((s, s), (x, y)), stroke(color, 3, op)], f"d{i}"))
        elif k == 1:
            out.append(group([polyline([(x - s / 2, y), (x + s / 2, y)]), polyline([(x, y - s / 2), (x, y + s / 2)]), stroke(color, 3, op)], f"d{i}"))
        elif k == 2:
            out.append(group([star(5, s * 0.7, s * 0.3, (x, y), rng.uniform(0, 70)), stroke(color, 3, op, join="round")], f"d{i}"))
        else:
            out.append(group([rect((s, s), (x, y), 5), stroke(color, 3, op)], f"d{i}", rotation=rng.uniform(-30, 30)))
    return out


def whatsapp():
    comp = Comp("whatsapp-chat-window", W, H, frames=F)
    comp.slot("primary", "#008069")
    comp.slot("background", "#EFE7DE")
    comp.slot("secondary", "#FFFFFF")
    comp.slot("icon", "#FFFFFF")
    comp.slot("outline", "#667781")
    comp.slot("accent", "#00A884")
    header = status() + [
        glyph("back", 54, 62, 176), avatar(172, 176, 100, slot="outline", fg="secondary", fg_opacity=100),
        label("online", 244, 212, 28, 400, opacity=80),
        glyph("video", 52, 770, 176), glyph("call", 46, 868, 176), glyph("more", 50, 984, 176),
        group([rect_tl(0, 0, W, 230), fill(slot="primary")], "bar")]
    body = doodles() + [group([rect_tl(0, 0, W, H), fill(slot="background")], "wallpaper")]
    cy = 1822
    footer = [
        glyph("mic", 46, 986, cy, slot="icon"), group([ellipse((104, 104), (986, cy)), fill(slot="accent")], "mic-bg"),
        glyph("camera", 44, 870, cy, slot="outline"), glyph("clip", 40, 790, cy, slot="outline", rotation=45),
        label("Message", 150, cy + 12, 38, 400, slot="outline"), glyph("emoji", 48, 90, cy, slot="outline"),
        group([rect_tl(24, cy - 52, 872, 104, 52), fill(slot="secondary")], "pill")]
    layers(comp, header, body, footer)
    return comp, {"name": (250, 132, 420, 44), "chat": (24, 250, 1032, 1480)}


def imessage():
    comp = Comp("imessage-chat-window", W, H, frames=F)
    comp.slot("background", "#FFFFFF")
    comp.slot("secondary", "#F6F6F6")
    comp.slot("primary", "#0B84FE")
    comp.slot("icon", "#000000")
    comp.slot("outline", "#8E8E93")
    header = status("icon") + [
        glyph("back", 0, 0, 0) if False else group([polyline([(84, 150), (56, 188), (84, 226)]), stroke(slot="primary", width=7)], "back"),
        glyph("video", 54, 990, 190, slot="primary"),
        avatar(540, 168, 118, slot="outline", fg="secondary", fg_opacity=100),
        group([polyline([(580, 252), (596, 266), (580, 280)]), stroke(slot="outline", width=3.5)], "chev"),
        group([polyline([(0, 297), (W, 297)]), stroke(slot="outline", width=1.5, opacity=45)], "hair"),
        group([rect_tl(0, 0, W, 300), fill(slot="secondary")], "bar")]
    body = [group([rect_tl(0, 0, W, H), fill(slot="background")], "bg")]
    cy = 1790
    footer = [
        glyph("mic", 44, 970, cy, slot="outline"),
        label("iMessage", 170, cy + 13, 40, 400, slot="outline", opacity=75),
        group([rect_tl(128, cy - 46, 884, 92, 46), stroke(slot="outline", width=2, opacity=55)], "pill-edge"),
        plus(72, cy, 20, slot="outline", w=5),
        group([ellipse((86, 86), (72, cy)), fill(slot="secondary")], "plus-bg"),
        group([rect_tl(W / 2 - 150, 1880, 300, 10, 5), fill(slot="icon")], "home-indicator")]
    layers(comp, header, body, footer, bar=300)
    return comp, {"name": (400, 234, 280, 48), "chat": (0, 320, W, 1380)}


def messenger():
    comp = Comp("messenger-chat-window", W, H, frames=F)
    comp.slot("background", "#FFFFFF")
    comp.slot("secondary", "#F0F2F5")
    comp.slot("primary", "#0084FF")
    comp.slot("icon", "#000000")
    comp.slot("outline", "#65676B")
    header = status("icon") + [
        glyph("back", 56, 60, 186, slot="primary"), avatar(168, 186, 104, slot="outline", fg="secondary", fg_opacity=100),
        group([ellipse((30, 30), (212, 232)), fill("#31A24C")], "active"),
        group([ellipse((38, 38), (212, 232)), fill(slot="background")], "active-ring"),
        label("Active now", 236, 222, 28, 400, slot="outline"),
        glyph("call", 52, 760, 186, slot="primary"), glyph("video", 56, 866, 186, slot="primary"), glyph("info", 56, 976, 186, slot="primary"),
        group([polyline([(0, 262), (W, 262)]), stroke(slot="outline", width=1.5, opacity=30)], "hair"),
        group([rect_tl(0, 0, W, 262), fill(slot="background")], "bar")]
    body = [group([rect_tl(0, 0, W, H), fill(slot="background")], "bg")]
    cy = 1810
    footer = [
        glyph("thumb", 56, 996, cy, slot="primary"), glyph("emoji", 48, 880, cy, slot="outline"),
        label("Aa", 480, cy + 13, 40, 400, slot="outline"),
        group([rect_tl(440, cy - 48, 480, 96, 48), fill(slot="secondary")], "pill"),
        glyph("mic", 50, 380, cy, slot="primary"), glyph("image", 50, 280, cy, slot="primary"), glyph("camera", 52, 180, cy, slot="primary"),
        glyph("plus-circle", 58, 74, cy, slot="primary"),
        group([rect_tl(W / 2 - 150, 1888, 300, 10, 5), fill(slot="icon")], "home-indicator")]
    layers(comp, header, body, footer, bar=262)
    return comp, {"name": (240, 136, 420, 44), "chat": (0, 280, W, 1440)}


def build(fn, asset_id, name, desc, tags):
    c, a = fn()
    build_asset(CAT, asset_id, name, desc, tags, [
        Variant("phone", "Phone Screen", c, "intro-hold", text_area=a["name"], text_areas=a, thumb_t=0.95, bg="6a7087")])
