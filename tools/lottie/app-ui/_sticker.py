import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from app_kit import *

F = 75


def sticker_comp(name, W, H):
    c = Comp(name, W, H, frames=F)
    c.slot("background", "#FFFFFF")
    c.slot("icon", "#262626")
    c.slot("primary", "#3897F0")
    c.slot("secondary", "#EFEFEF")
    return c


def pop_sticker(comp, shapes, W, H):
    comp.layer("sticker", shapes, anchor=(W / 2, H / 2), position=(W / 2, H / 2),
               scale=Anim([(0, [0, 0], OVERSHOOT), (14, [100, 100], EASE_IN_OUT), (F - 20, [100, 100], EASE_IN_OUT),
                           (F - 10, [103, 103], EASE_IN_OUT), (F, [100, 100])]),
               rotation=Anim([(0, -8, OVERSHOOT), (14, 0)]))
    comp.layer("shadow", soft_shadow(20, 20, W - 40, H - 40, 40, spread=16, dy=8, strength=16), opacity=fade(0, 10))
