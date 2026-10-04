import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from app_kit import *

F = 120
W, H = 700, 150
random.seed(7)
LV = [random.uniform(0.25, 1.0) for _ in range(36)]


def voice(sent):
    comp = Comp("whatsapp-voice-message", W, H, frames=F)
    comp.slot("primary", "#D9FDD3" if sent else "#FFFFFF")
    comp.slot("icon", "#667781")
    comp.slot("accent", "#25D366")
    x, y, w, h = 30, 22, 640, 106
    # play head position over time
    bars_x0 = x + 130
    bw, gap = 8, 7
    n = len(LV)
    prog = []
    for i, lv in enumerate(LV):
        bx = bars_x0 + i * (bw + gap)
        bh = 14 + lv * 50
        prog.append((bx, bh))
    shapes = []
    shapes += [group([ellipse((16, 16), (bars_x0 + 0 * 0 + 0, y + h - 18)), fill(slot="accent", opacity=0)], "x")]
    played = []
    base = []
    for i, (bx, bh) in enumerate(prog):
        t = 16 + (F - 30) * i / n
        base.append(group([rect_tl(bx, y + h / 2 - bh / 2 - 8, bw, bh, 4), fill(slot="icon", opacity=45)], f"b{i}"))
        played.append(group([rect_tl(bx, y + h / 2 - bh / 2 - 8, bw, bh, 4), fill(slot="accent")], f"p{i}",
                            opacity=Anim([(0, 0, HOLD), (t, 100, HOLD), (F, 100)])))
    knob_x0, knob_x1 = bars_x0 - 2, bars_x0 + n * (bw + gap)
    shapes += [group([ellipse((20, 20), (0, y + h / 2 - 8)), fill(slot="accent")], "knob",
                     position=Anim([(0, [knob_x0, 0], LINEAR), (16, [knob_x0, 0], LINEAR), (F - 14, [knob_x1, 0])]))]
    shapes += played + base
    shapes += [label("0:12", bars_x0 - 4, y + h - 16, 22, 400)]
    play = [group([polyline([(x + 52, y + h / 2 - 22), (x + 52, y + h / 2 + 8), (x + 80, y + h / 2 - 7)], closed=True), fill(slot="icon")], "play")]
    shapes += play
    shapes += [avatar(x + w - 52, y + h / 2, 70, slot="icon", fg="primary", fg_opacity=100)]
    body = group(rrect_path(x, y, w, h, 24 if True else 0, 24, 24, 24) + [fill(slot="primary")], "bubble")
    shapes += [body]
    pop_from(comp, "voice", shapes, (x + w, y), 0, 14)
    return comp


build_asset(CAT, "whatsapp-voice-message", "WhatsApp Voice Message",
            "WhatsApp voice-note bubble with a play button, a waveform that fills as it plays, a sliding scrubber and "
            "the speaker's avatar. Plays once and holds.",
            ["whatsapp", "voice message", "audio", "voice note", "chat", "waveform", "message", "podcast"], [
    Variant("sent", "Sent", voice(True), "intro-hold", thumb_t=0.6, bg="6a7087"),
    Variant("received", "Received", voice(False), "intro-hold", thumb_t=0.6, bg="6a7087"),
])
