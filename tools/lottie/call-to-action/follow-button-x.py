from _common import *
from drift_lottie import build_asset, Variant
from _platforms import Platform
from _retro_a import follow_extras

W, H = 640, 300
N = 120
PW, PH = 500, 128
CENTER = (W / 2, 130)
LOGO_X = -PW / 2 + 74
SW = 5
CLICK = 40
OUTRO = 96


def out(keys, t0):
    return keys + [(t0, [100, 100], EASE_OUT), (t0 + 5, [106, 106], EASE_IN), (t0 + 15, [0, 0], LINEAR)]


def classic():
    """Black pill whose white outline draws on and pulses outward on the click."""
    comp = Comp("follow-button-x", W, H, fps=30, frames=N)
    comp.slot("primary", "#000000")
    comp.slot("outline", "#FFFFFF")
    comp.marker("intro", 0, 80)
    comp.marker("outro", OUTRO, N - OUTRO)

    tip = (CENTER[0] + 150, CENTER[1] + 16)
    cursor(comp, [(14, [W + 60, H + 80], DECEL), (34, list(tip), EASE_IN_OUT), (CLICK + 20, list(tip), EASE_IN),
                  (CLICK + 36, [W + 60, H + 80])], [CLICK], ip=14, op=CLICK + 38, scale=4.0)

    button = comp.null("button", position=CENTER, scale=anim(out([
        (0, [0, 0], SPRING), (14, [100, 100], LINEAR), (CLICK - 3, [100, 100], EASE_IN), (CLICK, [96, 91], SNAP_OUT),
        (CLICK + 3, [96, 91], OVERSHOOT), (CLICK + 15, [100, 100], LINEAR)], OUTRO + 4)))

    comp.layer("logo", [group(glyph(X_LOGO, 60) + [fill("#FFFFFF")], "x")], parent=button, position=(LOGO_X, 0),
               scale=anim(out([(0, [0, 0], HOLD), (6, [0, 0], SPRING), (20, [100, 100], LINEAR),
                               (CLICK + 1, [100, 100], EASE_IN), (CLICK + 4, [80, 80], SNAP_OUT),
                               (CLICK + 10, [118, 118], EASE_IN_OUT), (CLICK + 20, [100, 100], LINEAR)], OUTRO)),
               rotation=anim([(6, -90, SNAP_OUT), (22, 0, HOLD), (CLICK + 3, 0, EASE_IN_OUT), (CLICK + 20, 180)]))

    # outline draws on around the pill, then pulses outward on click
    comp.layer("outline", [pill(PW, PH), trim(end=anim([(8, 0, EASE_IN_OUT), (30, 100)]),
                                              offset=anim([(8, -40, EASE_IN_OUT), (30, 0)])),
                           stroke(slot="outline", width=SW)], parent=button)
    comp.layer("pulse", [rect(anim([(CLICK, [PW, PH], DECEL), (CLICK + 18, [PW + 60, PH + 60])]),
                              roundness=anim([(CLICK, PH / 2, DECEL), (CLICK + 18, PH / 2 + 30)])),
                         stroke(slot="outline", width=anim([(CLICK, SW, EASE_OUT), (CLICK + 18, 1)]),
                                opacity=anim([(CLICK, 90, EASE_IN), (CLICK + 18, 0)]))],
               parent=button, ip=CLICK, op=CLICK + 19)
    comp.layer("pill", [pill(PW, PH), fill(slot="primary")], parent=button)
    return comp


XP = Platform("follow-button-x", "X", X_LOGO, tile="#000000", rim=True, glyph_size=0.5, primary="#FFFFFF",
              secondary="#3A3A3A", badge_icon="#000000", glass_bg="30303a", second="glass")

build_asset("call-to-action", "follow-button-x", "Follow Button X",
            "X (Twitter) follow button with the X logo; a pointer clicks it. Put your own \"Follow\" text inside "
            "the button.",
            ["follow", "x", "twitter", "button", "click", "cursor", "social"], [
    Variant("classic", "Classic Pill", classic(), "intro-hold-outro", thumb_t=0.3, bg="e8e8ee",
            text_area=(CENTER[0] + LOGO_X + 52, CENTER[1] - PH / 2 + 22, PW / 2 - LOGO_X - 52 - 40, PH - 44),
            description="Black follow pill with a white outline and the X logo; a pointer clicks it and the outline "
                        "pulses."),
] + follow_extras(XP))
