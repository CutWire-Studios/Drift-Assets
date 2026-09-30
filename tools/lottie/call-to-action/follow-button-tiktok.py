from _common import *
from drift_lottie import build_asset, Variant
from _platforms import Platform
from _retro_a import chroma, follow_extras

W, H = 700, 300
N = 120
PW, PH = 560, 136
CENTER = (W / 2, 130)
LOGO_X = -PW / 2 + 78
BTN_X = PW / 2 - 76
CLICK = 42
OUTRO = 96
LS = 72


def out(keys, t0):
    return keys + [(t0, [100, 100], EASE_OUT), (t0 + 5, [106, 106], EASE_IN), (t0 + 15, [0, 0], LINEAR)]


def jitter(sign):
    base = [3.2 * sign, 2.6 * sign]
    pts = [(5, [22, -6]), (8, [-14, 8]), (10, [10, 4]), (12, [-6, -3]), (14, [4, 2]), (16, [0, 0])]
    keys = [(t, [base[0] + v[0] * sign, base[1] + v[1] * sign], HOLD) for t, v in pts]
    keys += [(CLICK, base, HOLD), (CLICK + 2, [base[0] + 9 * sign, base[1] - 2 * sign], HOLD),
             (CLICK + 4, [base[0] - 4 * sign, base[1] + 1 * sign], HOLD), (CLICK + 6, base)]
    return anim(keys)


def classic():
    """Black pill with a glitching logo; the red plus spins into a check."""
    comp = Comp("follow-button-tiktok", W, H, fps=30, frames=N)
    comp.slot("primary", "#000000")
    comp.slot("accent", "#FE2C55")
    comp.slot("icon", "#FFFFFF")
    comp.marker("intro", 0, 80)
    comp.marker("outro", OUTRO, N - OUTRO)

    tip = (CENTER[0] + BTN_X + 8, CENTER[1] + 12)
    cursor(comp, [(16, [W + 60, H + 80], DECEL), (36, list(tip), EASE_IN_OUT), (CLICK + 20, list(tip), EASE_IN),
                  (CLICK + 36, [W + 60, H + 80])], [CLICK], ip=16, op=CLICK + 38, scale=4.0)

    button = comp.null("button", position=CENTER, scale=anim(out([
        (0, [0, 0], SPRING), (14, [100, 100], LINEAR), (CLICK - 3, [100, 100], EASE_IN), (CLICK, [96, 92], SNAP_OUT),
        (CLICK + 3, [96, 92], OVERSHOOT), (CLICK + 15, [100, 100], LINEAR)], OUTRO + 6)))

    # ------------------------------------------------------------ follow circle: + morphs into a check
    plus = [((-15, 0), (15, 0)), ((0, -15), (0, 15))]
    check = [((-15, 1), (-5, 11)), ((-5, 11), (15, -10))]

    def seg(i):
        return path(anim([(CLICK + 1, bezier(plus[i], closed=False), SNAP_OUT),
                          (CLICK + 11, bezier(check[i], closed=False))]), f"seg{i}")

    comp.layer("follow", [
        group([seg(0), seg(1), stroke(slot="icon", width=8.5)], "mark",
              rotation=anim([(CLICK + 1, -90, SNAP_OUT), (CLICK + 13, 0)])),
        group([ellipse((78, 78)), fill(slot="accent")], "circle"),
    ], parent=button, position=(BTN_X, 0), scale=anim(out([
        (0, [0, 0], HOLD), (10, [0, 0], SPRING), (24, [100, 100], LINEAR), (CLICK - 2, [100, 100], EASE_IN),
        (CLICK + 1, [80, 80], SNAP_OUT), (CLICK + 8, [118, 118], EASE_IN_OUT), (CLICK + 18, [100, 100], LINEAR)],
        OUTRO)))
    burst(comp, (BTN_X, 0), CLICK + 4, 52, 70, count=8, slot="accent", width=6, dots=False, parent=button)

    # ------------------------------------------------------------ TikTok logo with chromatic offset
    logo = comp.null("logo", parent=button, position=(LOGO_X, 0), scale=anim(out([
        (0, [0, 0], HOLD), (5, [0, 0], SPRING), (19, [100, 100], LINEAR)], OUTRO + 3)))
    comp.layer("logo-white", [group(glyph(TIKTOK, LS) + [fill("#FFFFFF")], "note")], parent=logo)
    comp.layer("logo-red", [group(glyph(TIKTOK, LS) + [fill("#FE2C55")], "note")], parent=logo, position=jitter(1))
    comp.layer("logo-cyan", [group(glyph(TIKTOK, LS) + [fill("#25F4EE")], "note")], parent=logo, position=jitter(-1))

    comp.layer("pill", [pill(PW, PH), fill(slot="primary")], parent=button)
    comp.layer("shadow", [pill(PW, PH), fill("#000000", 18)], parent=button, position=(0, 8))
    return comp


chroma()
TT = Platform("follow-button-tiktok", "TikTok", TIKTOK, tile="#000000", rim=True, glyph_size=0.52,
              glyph_offset=(0, 0), primary="#FE2C55", secondary="#363636", second="outline")

build_asset("call-to-action", "follow-button-tiktok", "Follow Button TikTok",
            "TikTok follow button with the logo; a pointer clicks it. Put your own \"Follow\" text inside the "
            "button.",
            ["follow", "tiktok", "button", "click", "cursor", "social"], [
    Variant("classic", "Classic Pill", classic(), "intro-hold-outro", thumb_t=0.5, bg="e8e8ee",
            text_area=(CENTER[0] + LOGO_X + 56, CENTER[1] - PH / 2 + 24, BTN_X - LOGO_X - 112, PH - 48),
            description="Black follow pill with a glitching TikTok logo; a pointer clicks the red plus, which "
                        "spins into a check."),
] + follow_extras(TT))
