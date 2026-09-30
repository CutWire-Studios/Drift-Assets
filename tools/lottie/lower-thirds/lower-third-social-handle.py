from _lt2 import *

STORY = [(0, "#FEDA75"), (0.3, "#FA7E1E"), (0.55, "#D62976"), (0.8, "#962FBF"), (1, "#4F5BD5")]


def avatar(comp, cx, cy, R, parent):
    """Generic person placeholder clipped to a circle."""
    comp.layer("avatar-matte", [ellipse((R * 2, R * 2), (cx, cy)), fill("#FFFFFF")], parent=parent)
    comp.layer("person", [group([ellipse((R * 0.78, R * 0.78), (cx, cy - R * 0.2)), fill(slot="icon")], "head"),
                          group([ellipse((R * 1.5, R * 1.1), (cx, cy + R * 0.82)), fill(slot="icon")], "body")],
               parent=parent, matte="alpha")
    comp.layer("avatar-bg", [ellipse((R * 2, R * 2), (cx, cy)), fill(slot="secondary")], parent=parent)


def verified(comp, cx, cy, r, t0, t_out):
    b = rig(comp, "verified", (cx, cy), scale=pop(t0, t0 + 12, t_out, t_out + 10),
            rotation=keys((t0, -90, EXPO_OUT), (t0 + 14, 0)))
    comp.layer("tick", [poly([(cx - r * 0.42, cy + r * 0.02), (cx - r * 0.1, cy + r * 0.34), (cx + r * 0.45, cy - r * 0.3)],
                             False), stroke("#FFFFFF", width=r * 0.26),
                        trim(end=keys((t0 + 6, 0, EASE_OUT), (t0 + 14, 100)))], parent=b)
    comp.layer("seal", [star(8, r, r * 0.84, (cx, cy), outer_roundness=40, inner_roundness=40), fill(slot="accent"),
                        stroke(slot="primary", width=4)], parent=b)


def pill():
    W, H = 1050, 200
    comp = base("lower-third-social-handle", W, H, 34)
    comp.slot("primary", "#FFFFFF")
    comp.slot("secondary", "#CBD5E1")
    comp.slot("icon", "#F8FAFC")
    comp.slot("accent", "#1D9BF0")
    cx, cy, R = 100, 100, 62
    verified(comp, cx + R * 0.72, cy + R * 0.72, 20, 20, 120)
    a = rig(comp, "avatar", (cx, cy), scale=pop(0, 16, 126, 140))
    avatar(comp, cx, cy, R, a)
    comp.layer("ring", [ellipse((R * 2 + 14, R * 2 + 14), (cx, cy)), fill(slot="primary")], parent=a)
    x, y, w, h = cx, cy - 42, 860, 84
    comp.layer("bar", [rect_grow(x, y, w, h, h / 2, 8, 30, 120, 138, "left", start=0), fill(slot="primary")])
    comp.layer("bar-shadow", [rect_grow(x, y + 8, w, h, h / 2, 8, 30, 120, 138, "left", start=0),
                              fill("#000000", 20)])
    return comp, (cx + R + 30, y + 16, w - R - 80, h - 32)


def story_card():
    W, H = 1100, 240
    comp = base("lower-third-social-handle--story", W, H, 36)
    comp.slot("primary", "#121212")
    comp.slot("secondary", "#3A3A3A")
    comp.slot("icon", "#8E8E8E")
    comp.slot("accent", "#FFFFFF")
    x, y, w, h = 50, 40, 920, 160
    cx, cy, R = x + 90, y + h / 2, 54
    a = rig(comp, "avatar", (cx, cy), scale=pop(6, 22, 124, 136))
    avatar(comp, cx, cy, R, a)
    comp.layer("gap", [ellipse((R * 2 + 12, R * 2 + 12), (cx, cy)), fill(slot="primary")], parent=a)
    lay(comp, "story-ring", [ellipse((R * 2 + 24, R * 2 + 24), (cx, cy)),
                             gradient_fill(STORY, (cx - R, cy + R), (cx + R, cy - R))], (cx, cy), parent=a,
        rotation=keys((6, -180, EXPO_OUT), (40, 0, LINEAR), (150, 200)))
    lay(comp, "follow", [rrect(x + w - 190, cy - 24, 150, 48, 12), fill(slot="accent")], (x + w - 115, cy),
        scale=pop(24, 36, 118, 128))
    c = rig(comp, "card", (x, cy), scale=keys((0, [0, 100], EXPO_OUT), (22, [100, 100], HOLD),
                                              (122, [100, 100], EXPO_IN), (140, [0, 100])),
            opacity=fade(0, 4, 136, 140))
    comp.layer("card", [rrect(x, y, w, h, 24), fill(slot="primary")], parent=c)
    comp.layer("card-edge", [rrect(x, y, w, h, 24), stroke(slot="secondary", width=2)], parent=c)
    return comp, (cx + R + 34, y + 36, w - 420, 50), (cx + R + 34, y + 94, w - 420, 30), \
        (x + w - 180, cy - 16, 130, 32)


def minimal():
    W, H = 1050, 200
    comp = base("lower-third-social-handle--minimal", W, H, 36)
    comp.slot("primary", "#FFFFFF")
    comp.slot("secondary", "#FF3B5C")
    comp.slot("icon", "#FFFFFF")
    comp.slot("accent", "#FF3B5C")
    cx, cy, R = 86, 100, 54
    a = rig(comp, "avatar", (cx, cy), scale=pop(0, 16, 126, 140), off=slide(-30, 0, 0, 16, 126, 140))
    comp.layer("ring", [ellipse((R * 2 + 12, R * 2 + 12), (cx, cy)), stroke(slot="primary", width=4)], parent=a)
    avatar(comp, cx, cy, R, a)
    comp.layer("line", [poly([(cx + R + 26, cy + 34), (960, cy + 34)], False), draw_rev(10, 34, 118, 138),
                        stroke(slot="primary", width=4)])
    lay(comp, "dot", [ellipse((14, 14), (960, cy + 34)), fill(slot="accent")], (960, cy + 34),
        scale=pop(30, 40, 116, 124))
    return comp, (cx + R + 26, cy - 40, 960 - cx - R - 26, 64)


a, ah = pill()
b, bh, bs, bf = story_card()
c, chd = minimal()
build("lower-third-social-handle", "Social Handle Lower Third",
      "Social media handle lower third with a round avatar placeholder. Type your @handle in the bar; the "
      "avatar is a generic person silhouette.",
      ["lower third", "social", "handle", "username", "avatar", "profile", "creator"], [
          V("pill", "Handle Pill", a, ah,
            description="Avatar pops in with a verified seal and a white capsule extends for the handle."),
          V("story", "Profile Card", b, bh, bs, {"button": bf},
            description="Dark two-line profile card with a spinning story-style gradient ring and a follow button."),
          V("minimal", "Minimal", c, chd,
            description="Just the avatar with an outline ring and an underline drawing out beneath the handle."),
      ])
