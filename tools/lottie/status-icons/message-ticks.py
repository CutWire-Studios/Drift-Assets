import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from ui_kit import *
from os_icons import *

CAT = "status-icons"

W, H = 260, 160


def tick(x, y, s, t0, slot):
    pts = [(x, y + 0.5 * s), (x + 0.38 * s, y + 0.88 * s), (x + 1.2 * s, y)]
    return group([polyline(pts), stroke(slot=slot, width=s * 0.2, join="round"),
                  trim(0, Anim([(t0, 0, EASE_OUT), (t0 + 10, 100)]))], "tick")


def ticks(n, read, F=75):
    comp = Comp("message-ticks", W, H, frames=F)
    comp.slot("icon", "#8696A0")
    comp.slot("primary", "#53BDEB")
    s = 80
    x0 = 130 - (s * 1.2 + (s * 0.5 if n == 2 else 0)) / 2 + 0
    y0 = 40
    parts = []
    for i in range(n):
        parts.append(tick(x0 + i * s * 0.5, y0, s, 4 + i * 6, "primary" if read else "icon"))
    if read:
        grey = [tick(x0 + i * s * 0.5, y0, s, 4 + i * 6, "icon") for i in range(n)]
        comp.layer("read", parts, opacity=Anim([(0, 0, HOLD), (36, 0, EASE_OUT), (46, 100)]))
        comp.layer("grey", grey)
    else:
        comp.layer("ticks", parts)
    return comp


build_asset(CAT, "message-ticks", "Message Ticks",
            "Chat delivery ticks as in WhatsApp: one tick for sent, two for delivered, and two that turn blue when "
            "read. Each draws on in sequence.",
            ["ticks", "read receipt", "delivered", "sent", "seen", "whatsapp", "chat", "message status"], [
    Variant("sent", "Sent", ticks(1, False), "intro-hold", thumb_t=0.95, bg="e8e8ee"),
    Variant("delivered", "Delivered", ticks(2, False), "intro-hold", thumb_t=0.95, bg="e8e8ee"),
    Variant("read", "Read", ticks(2, True), "intro-hold", thumb_t=0.95, bg="e8e8ee"),
])
