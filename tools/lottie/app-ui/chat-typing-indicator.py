import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from app_kit import *

F = 60


def imessage():
    comp = Comp("chat-typing-indicator", 300, 160, frames=F)
    comp.slot("secondary", "#E9E9EB")
    comp.slot("icon", "#8E8E93")
    x, y, w, h = 40, 30, 150, 86
    tail = "M{0},{1} L{2},{1} Q{2},{3} {4},{5} Q{6},{7} {8},{9} Z".format(x + 38, y + h - 30, x + 8, y + h, x - 12, y + h + 8, x + 22, y + h + 10, x + 44, y + h - 6)
    comp.layer("dots", dots_typing(x + w / 2, y + h / 2, 30, 11, F, lo=55, hi=100))
    comp.layer("bubble", [group(svg_shapes(tail) + [fill(slot="secondary")], "tail"),
                          group([rect_tl(x, y, w, h, 43), fill(slot="secondary")], "bubble")])
    return comp


def messenger():
    comp = Comp("chat-typing-indicator", 340, 160, frames=F)
    comp.slot("secondary", "#E4E6EB")
    comp.slot("primary", "#0084FF")
    comp.slot("icon", "#65676B")
    x, y, w, h = 90, 40, 150, 76
    comp.layer("dots", dots_typing(x + w / 2, y + h / 2, 30, 10, F, lo=55, hi=100))
    comp.layer("bubble", [group([rect_tl(x, y, w, h, 38), fill(slot="secondary")], "bubble")])
    comp.layer("avatar", [avatar(x - 38, y + h - 26, 52, slot="primary", fg="secondary", fg_opacity=100)])
    return comp


def whatsapp_label():
    comp = Comp("chat-typing-indicator", 340, 120, frames=F)
    comp.slot("primary", "#25D366")
    tw = text_width("typing", 46, 500)
    x0 = 30
    comp.layer("dots", [g for g in dots_typing(x0 + tw + 22 + 22, 62, 22, 6, F, slot="primary", lo=35, hi=100, lift=1.2)])
    comp.layer("text", [label("typing", x0, 74, 46, 500, slot="primary")])
    return comp


def whatsapp_bubble():
    comp = Comp("chat-typing-indicator", 300, 160, frames=F)
    comp.slot("secondary", "#FFFFFF")
    comp.slot("icon", "#8696A0")
    x, y, w, h = 40, 30, 150, 80
    comp.layer("dots", dots_typing(x + w / 2, y + h / 2, 28, 9, F, lo=55, hi=100))
    comp.layer("bubble", [group(rrect_path(x, y, w, h, 0, 24, 24, 24) + [fill(slot="secondary")], "bubble"),
                          group([polyline([(x + 1, y), (x - 20, y), (x + 1, y + 22)], closed=True), fill(slot="secondary")], "tail")])
    return comp


build_asset(CAT, "chat-typing-indicator", "Typing Indicator",
            "The 'someone is typing' animation: three bouncing dots in an iMessage or WhatsApp bubble, Messenger's "
            "dots with an avatar, or WhatsApp's green 'typing' label with animated dots. Loops.",
            ["typing", "typing indicator", "dots", "chat", "imessage", "whatsapp", "messenger", "texting", "loading"], [
    Variant("imessage", "iMessage", imessage(), "loop", thumb_t=0.2, bg="6a7087"),
    Variant("messenger", "Messenger", messenger(), "loop", thumb_t=0.2, bg="6a7087"),
    Variant("whatsapp", "WhatsApp Bubble", whatsapp_bubble(), "loop", thumb_t=0.2, bg="6a7087"),
    Variant("whatsapp-label", "WhatsApp Label", whatsapp_label(), "loop", thumb_t=0.2, bg="1c1c22"),
])
