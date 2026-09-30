"""Snowfall: a full-frame transparent snow overlay (seamless loop)."""

from _common import *

W, H = 1920, 1080
T = 120
SNOW = "#FFFFFF"
REGION = (610, 190, 700, 700)


def arm_d(r):
    """One crystal arm pointing up: spoke plus two pairs of side branches (open strokes)."""
    d = f"M 0 0 L 0 {-r:.2f} "
    for k, bl in ((0.45, 0.34), (0.72, 0.24)):
        for s in (-1, 1):
            d += f"M 0 {-r * k:.2f} L {s * r * bl:.2f} {-(r * k + r * bl * 0.7):.2f} "
    return d


def crystal(r, width):
    """Six arms via a repeater (keeps the file small)."""
    return group(S(arm_d(r)) + [stroke(SNOW, width, slot="primary"), repeater(6, rotation=60)], "crystal")


def soft():
    comp = Comp("snowfall", W, H, frames=T)
    comp.slot("primary", SNOW)

    def shapes(i, d):
        s = lerp(6, 20, d)
        items = [group([ellipse((s, s)), fill(SNOW, slot="primary")], "flake")]
        if d > 0.45:
            for k, o in ((1.5, 16), (2.1, 9), (2.8, 5)):
                items.append(group([ellipse((s * k, s * k)), fill(SNOW, o, slot="primary")], "halo"))
        return items

    fall(comp, "snow", 110, T, W, H, shapes, seed=11, speed=(3.0, 6.0), sway=(8, 30), sway_period=(50, 120),
         size=(1, 1), opacity=(55, 100), depth_pow=1.6, margin=40)
    return comp


def crystals():
    comp = Comp("snowfall--crystals", W, H, frames=T)
    comp.slot("primary", SNOW)

    def shapes(i, d):
        r = lerp(12, 34, d)
        if i % 3 == 0:  # a few soft dots between the crystals
            return [group([ellipse((r * 0.5, r * 0.5)), fill(SNOW, slot="primary")], "dot")]
        return [crystal(r, lerp(2.2, 4.5, d)),
                group([ellipse((r * 0.34, r * 0.34)), fill(SNOW, slot="primary")], "hub")]

    fall(comp, "flake", 50, T, W, H, shapes, seed=5, speed=(2.8, 4.6), sway=(14, 40), sway_period=(60, 120),
         spin=(40, 110), flip=0.35, flip_period=(40, 60), opacity=(60, 100), depth_pow=1.4, margin=50)
    return comp


def blizzard():
    comp = Comp("snowfall--blizzard", W, H, frames=T)
    comp.slot("primary", SNOW)
    wind = 7.0

    def shapes(i, d):
        s = lerp(5, 15, d)
        v = lerp(9, 18, d)
        ang = -math.degrees(math.atan2(wind, v))
        return [group([group([ellipse((s, s * lerp(2.2, 3.4, d))), fill(SNOW, slot="primary")], "streak",
                             rotation=ang)], "flake")]

    fall(comp, "gust", 230, T, W, H, shapes, seed=23, speed=(9, 18), sway=(2, 10), sway_period=(20, 40),
         wind=wind, size=(1, 1), opacity=(40, 95), depth_pow=1.3, margin=30)
    return comp


build("snowfall", "Snowfall",
      "Full-frame transparent snow overlay that falls over your footage in a seamless loop; "
      "for winter, Christmas and holiday edits.",
      ["snow", "snowfall", "winter", "christmas", "holiday", "overlay", "weather"], [
          Variant("soft", "Soft Snow", soft(), "loop", thumb_t=0.5, region=REGION, pad=0, bg="3a4a66",
                  description="Soft round flakes in three depths, drifting and swaying gently."),
          Variant("crystals", "Crystal Flakes", crystals(), "loop", thumb_t=0.5, region=REGION, pad=0,
                  bg="3a4a66", description="Six-armed crystal snowflakes that spin and flutter as they fall."),
          Variant("blizzard", "Blizzard", blizzard(), "loop", thumb_t=0.5, region=REGION, pad=0, bg="3a4a66",
                  description="Fast wind-driven snow streaking diagonally across the frame."),
      ])
