import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from app_kit import *

F = 150


def desktop():
    W, H = 1600, 900
    comp = Comp("youtube-player-controls", W, H, frames=F)
    comp.slot("icon", "#FFFFFF")
    comp.slot("primary", "#FF0000")
    comp.slot("outline", "#8A8A8A")
    by = H - 78
    sh = []
    sh += [glyph("fullscreen", 44, W - 60, by, slot="icon"), glyph("settings", 42, W - 130, by, slot="icon"),
           group([rect_tl(W - 248, by - 17, 52, 34, 7), stroke(slot="icon", width=3.5)], "cc"),
           label("1:12 / 3:45", 238, by + 10, 28, 500), glyph("volume", 42, 168, by, slot="icon"),
           glyph("skip-next", 46, 100, by, slot="icon"), glyph("pause", 46, 44, by, slot="icon")]
    sh += [group([ellipse((26, 26), (0, by - 52)), fill(slot="primary")], "scrub", position=Anim([(14, [40, 0], LINEAR), (F, [40 + (W - 80) * 0.32, 0])])),
           group([grow_rect(40, by - 55, (W - 80) * 0.32, 6, 14, F, 3), fill(slot="primary")], "played"),
           group([rect_tl(40, by - 55, (W - 80) * 0.5, 6, 3), fill(slot="icon", opacity=45)], "buffer"),
           group([rect_tl(40, by - 55, W - 80, 6, 3), fill(slot="outline", opacity=70)], "track")]
    comp.layer("bar", sh, position=Anim([(0, [0, 30], EXPO_OUT), (14, [0, 0])]), opacity=fade(0, 10))
    comp.layer("scrim", [group([rect_tl(0, H - 240, W, 240), gradient_fill([(0, "#000000", 0), (1, "#000000", 0.7)], (0, H - 240), (0, H))], "g")],
               opacity=fade(0, 12))
    return comp


def mobile():
    W, H = 1280, 720
    comp = Comp("youtube-player-controls", W, H, frames=F)
    comp.slot("icon", "#FFFFFF")
    comp.slot("primary", "#FF0000")
    comp.slot("outline", "#8A8A8A")
    cx, cy = W / 2, H / 2
    sh = []
    for dx, g, sz in ((-250, "skip-prev", 64), (250, "skip-next", 64), (0, "pause", 90)):
        sh.append(glyph(g, sz, cx + dx, cy, slot="icon"))
    sh += [group([ellipse((150 if dx == 0 else 118,) * 2, (cx + dx, cy)), fill("#000000", 45)], "disc") for dx in (-250, 250, 0)]
    by = H - 60
    sh2 = [glyph("fullscreen", 40, W - 50, by, slot="icon"), label("1:12 / 3:45", 40, by - 22, 26, 500),
           group([ellipse((24, 24), (0, by + 20)), fill(slot="primary")], "scrub", position=Anim([(14, [40, 0], LINEAR), (F, [40 + (W - 80) * 0.32, 0])])),
           group([grow_rect(40, by + 17, (W - 80) * 0.32, 6, 14, F, 3), fill(slot="primary")], "played"),
           group([rect_tl(40, by + 17, W - 80, 6, 3), fill(slot="outline", opacity=70)], "track")]
    comp.layer("bar", sh2, position=Anim([(0, [0, 30], EXPO_OUT), (14, [0, 0])]), opacity=fade(0, 10))
    comp.layer("center", sh, anchor=(cx, cy), position=(cx, cy), scale=Anim([(0, [80, 80], EXPO_OUT), (14, [100, 100])]), opacity=fade(0, 10))
    comp.layer("scrim", [group([rect_tl(0, 0, W, H), fill("#000000", 38)], "dim")], opacity=fade(0, 10))
    return comp


build_asset(CAT, "youtube-player-controls", "Video Player Controls",
            "YouTube-style video player controls drawn over your footage: a desktop control bar with a red progress "
            "bar, time, volume, captions, settings and fullscreen, or the mobile layout with big centred transport buttons.",
            ["youtube", "video player", "controls", "progress bar", "seek", "play", "ui", "scrubber", "overlay"], [
    Variant("desktop", "Desktop Bar", desktop(), "intro-hold", thumb_t=0.7, bg="6a7087"),
    Variant("mobile", "Mobile Controls", mobile(), "intro-hold", thumb_t=0.7, bg="6a7087"),
])
