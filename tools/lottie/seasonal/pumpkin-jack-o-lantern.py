"""Jack-o'-lantern: a carved pumpkin whose candle-lit face flickers (seamless loop)."""

from _common import *

T = 60
W, H = 520, 500
C = (W / 2, 255)
ORANGE, STEM, LIGHT = "#F47A1F", "#5A7A2E", "#FFD24A"

EYE_L = "M -96 -24 L -38 -24 L -64 -80 Z"
EYE_R = "M 96 -24 L 38 -24 L 64 -80 Z"
NOSE = "M -16 14 L 16 14 L 0 -14 Z"
MOUTH = ("M -116 36 C -64 62 64 62 116 36 C 100 96 44 122 0 122 C -44 122 -100 96 -116 36 Z")
TEETH = ("M -46 50 L -20 54 L -22 76 L -44 72 Z M 20 54 L 46 50 L 44 72 L 22 76 Z "
         "M -12 122 L 14 122 L 12 100 L -10 100 Z")
FACE = [EYE_L, EYE_R, NOSE, MOUTH]
RIBS = [(-112, 150, 236), (112, 150, 236), (-62, 176, 262), (62, 176, 262), (0, 184, 272)]
STEM_D = "M -14 -112 C -14 -140 -8 -162 10 -176 L 26 -166 C 14 -152 12 -134 14 -110 Z"
VINE_D = "M 6 -122 C 30 -140 58 -136 66 -116 C 72 -100 60 -92 52 -100"


def fl(t, seed=1):
    return clamp(0.5 + 0.5 * flicker(t, T, seed) + 0.25 * flicker(t, T, seed + 11))


def classic():
    comp = Comp("pumpkin-jack-o-lantern", W, H, frames=T)
    comp.slot("primary", ORANGE)
    comp.slot("secondary", STEM)
    comp.slot("accent", LIGHT)
    p = comp.null("pumpkin", position=C, anchor=(0, 130),
                  scale=looped(lambda t: [100 + 0.8 * wave(t, T, 1), 100 - 0.8 * wave(t, T, 1)], T, 3))
    p = comp.null("pumpkin-pos", parent=p, position=(0, 130))
    # face glow spilling over the pumpkin skin
    comp.layer("face-glow", [glow(170, "#FFE08A", 100, falloff=((0, 0.55), (0.5, 0.22), (1, 0)), position=(0, 30),
                                  sy=0.8)], parent=p,
               opacity=looped(lambda t: 18 + 30 * fl(t), T, 1),
               scale=looped(lambda t: [96 + 8 * fl(t, 4)] * 2, T, 2))
    comp.layer("teeth", [group(S(TEETH) + [fill(ORANGE, slot="primary")], "teeth"),
                         group(S(TEETH) + [fill("#7A2A04", 60)], "teeth-rim", position=(0, -4))], parent=p)
    comp.layer("flame-dim", [group(sum((S(d) for d in FACE), []) + [fill("#A8320A")], "dim")], parent=p,
               opacity=looped(lambda t: 55 * (1 - fl(t)), T, 1))
    comp.layer("holes", [group(sum((S(d) for d in FACE), []) + [
        gradient_fill([(0, "#FFF6C8"), (0.45, "#FFC93C"), (1, "#F07A12")], (0, 40), (150, 40), radial=True)],
        "light", position=(0, 6), scale=(97, 94)),
        group(sum((S(d) for d in FACE), []) + [fill("#6B2203")], "rim"),
        group(sum((S(d) for d in FACE), []) + [stroke("#C4520C", 6)], "cut-edge")], parent=p)
    # body
    items = []
    for x, w, h in reversed(RIBS):
        pass
    for j, (x, w, h) in enumerate(reversed(RIBS)):
        box = (x - w / 2, 20 - h / 2, x + w / 2, 20 + h / 2)
        items.append(group([ellipse((w, h), (x, 20)),
                            stroke("#A5400A", 5, 70),
                            gradient_fill([(0, WHITE, 0.28), (0.45, WHITE, 0), (0.8, "#5A1800", 0.12),
                                           (1, "#5A1800", 0.4)],
                                          (x - w * 0.18, 20 - h * 0.25), (x - w * 0.18 + w * 0.75, 20 - h * 0.25),
                                          radial=True),
                            fill(ORANGE, slot="primary")], f"rib{j}"))
    comp.layer("body", items, parent=p)
    comp.layer("stem", [group(S(VINE_D) + [stroke(STEM, 6, slot="secondary")], "vine"),
                        group(S(STEM_D) + [gradient_fill([(0, WHITE, 0.25), (1, "#000000", 0.25)], (-14, -150),
                                                         (26, -150))], "shade"),
                        group(S(STEM_D) + [fill(STEM, slot="secondary")], "stem")], parent=p)
    comp.layer("halo", [glow(215, "#FF9A2E", 100, falloff=((0, 0.35), (0.6, 0.14), (1, 0)), position=(0, 20))],
               parent=p, opacity=looped(lambda t: 50 + 35 * fl(t, 2), T, 2))
    comp.layer("shadow", [ellipse((330, 40)), fill("#000000", 28)], position=(C[0], C[1] + 150))
    return comp


def flat():
    """Geometric flat sticker that hops; the face flashes between two warm tones."""
    comp = Comp("pumpkin-jack-o-lantern--flat", W, H, frames=T)
    comp.slot("primary", "#FF8A2A")
    comp.slot("secondary", "#3E8E4E")
    comp.slot("accent", "#FFE066")
    comp.slot("outline", WHITE)

    def hop(t):
        u = t / T
        if u < 0.5:
            k = u / 0.5
            return -70 * (1 - (2 * k - 1) ** 2)
        return 0

    def squash(t):
        u = t / T
        if u < 0.08:
            k = u / 0.08
            return [100 + 10 * (1 - k), 100 - 10 * (1 - k)]
        if u < 0.5:
            return [96, 104]
        if u < 0.62:
            k = (u - 0.5) / 0.12
            return [lerp(96, 112, smooth(k)), lerp(104, 88, smooth(k))]
        k = (u - 0.62) / 0.38
        return [lerp(112, 100, smooth(k)) + 4 * math.sin(k * 7) * (1 - k),
                lerp(88, 100, smooth(k)) - 4 * math.sin(k * 7) * (1 - k)]

    base = comp.null("base", position=(C[0], C[1] + 140), scale=looped(squash, T, 1))
    p = comp.null("pumpkin", parent=base, position=looped(lambda t: (0, hop(t) - 140), T, 1))
    face = [S(d.replace("-96 -24 L -38 -24 L -64 -80", "-92 -26 L -40 -26 L -66 -70")) for d in FACE]
    comp.layer("face", [group(sum(face, []) + [fill("#FFE066", slot="accent")], "face")], parent=p,
               opacity=looped(lambda t: 100 if (t // 4) % 5 else 70, T, 1))
    comp.layer("face-under", [group(sum(face, []) + [fill("#C8401A")], "under")], parent=p)
    ribs = [(-86, 170, 230), (86, 170, 230), (0, 210, 250)]
    comp.layer("stem", [group([rect((30, 56), (0, -118), 10), fill("#3E8E4E", slot="secondary")], "stem"),
                        group(S("M 14 -126 C 40 -150 70 -140 74 -118 C 50 -112 30 -116 14 -126 Z") +
                              [fill("#3E8E4E", slot="secondary")], "leaf")], parent=p)
    comp.layer("ribs", [group([ellipse((210, 250), (0, 20)), fill("#FF8A2A", slot="primary")], "mid")] +
               [group([ellipse((w, h), (x, 20)), fill("#E0671A")], f"r{j}") for j, (x, w, h) in
                enumerate(ribs[:2])], parent=p)
    comp.layer("ribs-base", [group([ellipse((w, h), (x, 20)) for x, w, h in ribs[:2]] +
                                   [fill("#FF8A2A", slot="primary")], "base")], parent=p)
    comp.layer("diecut", [group([ellipse((w, h), (x, 20)) for x, w, h in ribs] +
                                [rect((30, 56), (0, -118), 10)] +
                                S("M 14 -126 C 40 -150 70 -140 74 -118 C 50 -112 30 -116 14 -126 Z") +
                                [stroke(WHITE, 26, slot="outline"), fill(WHITE, slot="outline")], "cut")], parent=p)
    comp.layer("shadow", [ellipse((300, 34)), fill("#000000", 26)], position=(C[0], C[1] + 150),
               scale=looped(lambda t: [100 + hop(t) * 0.5] * 2, T, 1))
    return comp


def neon():
    """Neon-sign outline pumpkin that buzzes and flickers like a tube light."""
    comp = Comp("pumpkin-jack-o-lantern--neon", W, H, frames=T)
    comp.slot("primary", "#FF7A1A")
    comp.slot("secondary", "#6CFF5A")
    comp.slot("accent", "#FFE14A")
    body = [ellipse((w, h), (x, 20)) for x, w, h in RIBS[:4]] + [ellipse((184, 272), (0, 20))]
    outline = S("M -150 20 C -150 -90 -80 -112 0 -112 C 80 -112 150 -90 150 20 C 150 120 80 156 0 156 "
                "C -80 156 -150 120 -150 20 Z")
    ribs = S("M -60 -104 C -110 -60 -110 100 -60 150 M 60 -104 C 110 -60 110 100 60 150")
    face = sum((S(d) for d in FACE), [])

    def buzz(t, seed):
        u = t % T
        off = 1 if (20 <= u < 22) or (26 <= u < 27) else 0
        return (100 - 70 * off) * (0.92 + 0.08 * fl(t, seed))

    for name, shapes, col, sid, seed, w in (("face", face, "#FFE14A", "accent", 3, 7),
                                            ("stem", S(STEM_D), "#6CFF5A", "secondary", 5, 7),
                                            ("body", outline + ribs, "#FF7A1A", "primary", 7, 9)):
        comp.layer(name, [group(shapes + [stroke(WHITE, w * 0.35, 85)], "core"),
                          group(shapes + [stroke(col, w, slot=sid)], "tube"),
                          group(shapes + [stroke(col, w * 3.2, 22, slot=sid)], "glow1"),
                          group(shapes + [stroke(col, w * 6, 8, slot=sid)], "glow2")],
                   position=C, opacity=looped(lambda t, seed=seed, name=name: buzz(t, seed) if name != "stem"
                                              else 90 + 10 * fl(t, seed), T, 1))
    comp.layer("fill", [group(outline + [fill("#FF7A1A", 8, slot="primary")], "wash")], position=C)
    return comp


build("pumpkin-jack-o-lantern", "Pumpkin Jack-o'-Lantern",
      "A carved Halloween pumpkin whose face glows and flickers like a candle inside; a seamless loop.",
      ["pumpkin", "jack-o-lantern", "halloween", "candle", "spooky", "autumn"], [
          Variant("classic", "Candle Lit", classic(), "loop", thumb_t=0.3,
                  description="Shaded ribbed pumpkin with a candle-lit carved face and a flickering warm glow."),
          Variant("flat", "Flat Sticker", flat(), "loop", thumb_t=0.95,
                  description="Geometric flat pumpkin sticker with a white die-cut border that hops and squashes."),
          Variant("neon", "Neon Sign", neon(), "loop", thumb_t=0.1,
                  description="Neon-tube outline pumpkin that hums and buzzes off and on like a sign."),
      ])
