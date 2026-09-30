from _common import *

W, H, F = 520, 580, 75
CX = W / 2
PW = 400
TOP, HB, BOT = 96, 206, 520      # calendar top, header bottom (= page top), bottom
FLIPS = [12, 24, 34]
LAND = 44


def areas():
    return {"month": (CX - 150, TOP + 26, 300, HB - TOP - 40), "day": (CX - 150, HB + 40, 300, 230)}


def page_rect(inset=0):
    return rect((PW - 2 * inset, BOT - HB - inset), (CX, (HB + BOT - inset) / 2), 22)


def page_shape_bottom_round():
    """Page with square top corners and rounded bottom corners."""
    return path(top_round_bar(CX, PW, HB, BOT, 0), "page")


def week_strip(highlight=4, slot="primary"):
    items = []
    for i in range(7):
        c = (CX - 150 + i * 50, BOT - 34)
        items.append(group([rect((30, 12), c, 6), fill(slot=slot) if i == highlight else fill("#000000", 10)],
                           f"d{i}"))
    return items


def rings(comp, style, parent):
    items = []
    for sx in (-1, 1):
        x = CX + sx * 110
        if style == "neon":
            items += glow_strokes([polyline([(x, TOP - 30), (x, TOP + 22)])], slot="outline", width=8, core=True,
                                  widths=(20,), ops=(14,), name=f"ring{sx}")
        else:
            items += [group([rect((18, 64), (x, TOP - 4), 9), fill("#D9DDE6")], f"ring{sx}"),
                      group([rect((18, 64), (x + 3, TOP - 1), 9), fill("#000000", 30)], f"rs{sx}")]
    comp.layer("rings", items, parent=parent)


def flat():
    """Desk calendar: pages flip up over the binding one after another and the last one lands with a bounce."""
    comp = Comp("calendar-flip", W, H, fps=30, frames=F)
    slots(comp, FLAT | {"primary": "#FF4D5E", "background": "#FFFFFF", "outline": "#E3E6EE"},
          "primary", "background", "outline")
    rg = rig(comp, "calendar", (CX, BOT), scale=keys((0, [70, 70], SOFT_SPRING), (14, [100, 100], HOLD),
                                                   (LAND, [100, 100], EASE_OUT), (LAND + 4, [104, 96], EASE_IN_OUT),
                                                   (LAND + 12, [100, 100])))
    for k, t in enumerate(FLIPS):
        d = 7 if k < 2 else 10
        comp.layer(f"flipback{k}", [group([page_rect(), fill("#000000", 10)], "sh", position=(0, -6)),
                                    group([page_rect(), fill(slot="outline")], "b")], parent=rg,
                   anchor=(CX, HB), position=(CX, HB), ip=t + d, op=t + d + 9,
                   scale=keys((t + d, [100, 0], EASE_OUT), (t + d + 6, [100, -70])),
                   opacity=keys((t + d + 3, 100, EASE_IN), (t + d + 9, 0)))
    rings(comp, "flat", rg)
    comp.layer("header", [group([path(top_round_bar(CX, PW, TOP, HB, 22)),
                                 fill(slot="primary")], "h"),
                          group([ellipse((16, 16), (CX + sx * 110, TOP + 22)) for sx in (-1, 1)] + [fill("#000000", 35)],
                                "holes")], parent=rg)
    for k, t in enumerate(FLIPS):
        d = 7 if k < 2 else 10
        comp.layer(f"flip{k}", [group([page_rect(), fill("#000000")], "shade",
                                      opacity=keys((t, 0, EASE_IN), (t + d, 30))),
                                *week_strip(k + 1), group([page_rect(), fill(slot="background")], "p")],
                   parent=rg, anchor=(CX, HB), position=(CX, HB), op=t + d,
                   scale=keys((t, [100, 100], EASE_IN), (t + d, [100, 0])))
    comp.layer("page", week_strip(4) + [group([page_rect(), fill(slot="background")], "p")], parent=rg)
    comp.layer("stack", [group([rect((PW - 8, 30), (CX, BOT - 8), 16), fill(slot="outline")], "s1"),
                         group([rect((PW - 16, 30), (CX, BOT - 2), 16), fill(slot="outline")], "s2"),
                         group([rect((PW, BOT - TOP), (CX, (TOP + BOT) / 2 + 14), 24), fill("#000000", 22)], "sh")],
               parent=rg)
    return comp


def tearoff():
    """Tear-off pad: pages rip off one after another and tumble away, revealing a fresh page."""
    comp = Comp("calendar-flip--tear-off", W, H, fps=30, frames=F)
    slots(comp, FLAT | {"primary": "#2F6BFF", "background": "#FFFFFF", "outline": "#E3E6EE"},
          "primary", "background", "outline")
    rg = rig(comp, "calendar", (CX, BOT), scale=keys((0, [70, 70], SOFT_SPRING), (14, [100, 100])))
    comp.layer("header", [group([path(top_round_bar(CX, PW, TOP, HB, 22)), fill(slot="primary")], "h"),
                          group([rect((PW, 10), (CX, HB - 5)), fill("#000000", 20)], "lip")], parent=rg)
    # perforation along the tear line
    comp.layer("perf", [group([polyline([(CX - PW / 2 + 10, HB + 8), (CX + PW / 2 - 10, HB + 8)]),
                               stroke(slot="outline", width=4, dashes=[6, 8])], "d")], parent=rg)
    for k, t in enumerate(FLIPS):
        sgn = 1 if k % 2 == 0 else -1
        piv = (CX - sgn * PW / 2, HB)
        fall = keys((t, [0, 0], ANTICIPATE), (t + 16, [sgn * 140, 420]))
        rot = keys((t - 4, 0, EASE_IN_OUT), (t, sgn * 4, EASE_IN), (t + 16, sgn * 38))
        comp.layer(f"tear{k}", [*week_strip(k + 1), group([page_rect(), fill(slot="background")], "p"),
                                group([page_rect(), fill("#000000", 12)], "sh", position=(0, 6))],
                   parent=rg, anchor=piv, position=at(piv, fall), rotation=rot, op=t + 16,
                   opacity=keys((t + 8, 100, EASE_IN), (t + 16, 0)))
    comp.layer("page", week_strip(4) + [group([page_rect(), fill(slot="background")], "p")], parent=rg)
    comp.layer("stack", [group([rect((PW - 6, 30), (CX, BOT - 8), 16), fill(slot="outline")], "s1"),
                         group([rect((PW, BOT - TOP), (CX, (TOP + BOT) / 2 + 14), 24), fill("#000000", 22)], "sh")],
               parent=rg)
    return comp


def neon():
    """Dark panel; a neon calendar whose outlined pages flip up over glowing rings."""
    comp = Comp("calendar-flip--neon", W, H, fps=30, frames=F)
    slots(comp, NEON | {"primary": "#FF3DCB", "outline": "#23E5FF"}, "primary", "background", "outline")
    rings(comp, "neon", None)
    comp.layer("header", glow_strokes([polyline([(CX - PW / 2 + 16, HB), (CX + PW / 2 - 16, HB)])], slot="primary",
                                      width=4, widths=(20,), ops=(16,)))
    for k, t in enumerate(FLIPS):
        d = 7 if k < 2 else 10
        comp.layer(f"flip{k}", glow_strokes([page_rect(10)], slot="outline", width=3, core=False, widths=(16,),
                                            ops=(12,)) + [group([page_rect(10), fill(slot="background")], "bg")],
                   anchor=(CX, HB), position=(CX, HB), op=t + d,
                   scale=keys((t, [100, 100], EASE_IN), (t + d, [100, 0])),
                   opacity=keys((t, 100, EASE_IN), (t + d, 40)))
    comp.layer("page", glow_strokes([page_rect(10)], slot="outline", width=3, core=False, widths=(16,), ops=(12,)),
               opacity=keys((0, 0, HOLD), (FLIPS[-1] + 8, 0, HOLD), (FLIPS[-1] + 10, 100, HOLD), (FLIPS[-1] + 12, 40,
                                                                                                  HOLD),
                            (FLIPS[-1] + 14, 100)))
    comp.layer("frame", glow_strokes([rect((PW, BOT - TOP), (CX, (TOP + BOT) / 2), 24)], slot="primary", width=4,
                                     widths=(26, 14), ops=(8, 16),
                                     extra=[trim(end=keys((0, 0, EASE_IN_OUT), (18, 100)))]))
    neon_panel(comp, 16, 16, W - 32, H - 32, r=34)
    return comp


A = areas()
build_asset(CAT, "calendar-flip", "Calendar Flip",
            "A desk calendar whose pages flip over to land on a new date. Put the month in the 'month' area on the "
            "header and the day or date in the big 'day' area on the page.",
            ["calendar", "date", "day", "schedule", "deadline", "event", "time", "infographic"], [
    V("flat", "Flip Over", flat(), "intro-hold", text_area=A["day"], text_areas=A, thumb_t=0.95,
      description="Desk calendar with binder rings; pages flip up over the binding and the last one lands."),
    V("tear-off", "Tear-off Pad", tearoff(), "intro-hold", text_area=A["day"], text_areas=A, thumb_t=0.95,
      description="Tear-off pad: pages rip off and tumble away, revealing a fresh page."),
    V("neon", "Neon", neon(), "intro-hold", text_area=A["day"], text_areas=A, thumb_t=0.95,
      description="Dark panel; outlined neon pages flip up over glowing rings."),
])
