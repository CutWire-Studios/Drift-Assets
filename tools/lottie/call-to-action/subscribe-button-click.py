from _common import *
from _cta_actions import body
from drift_lottie import Variant, build_asset
import _platforms as P

W, H = 640, 300
N = 120
PW, PH = 480, 124
CENTER = (W / 2, 128)
CLICK = 38
LOCAL_TIP = (130, 14)
TIP = (CENTER[0] + LOCAL_TIP[0], CENTER[1] + LOCAL_TIP[1])
OUTRO = 96


def classic():
    """Red pill pops in, is clicked and turns grey."""
    comp = Comp("subscribe-button-click", W, H, fps=30, frames=N)
    comp.slot("primary", "#FF0000")
    comp.slot("secondary", "#606060")
    comp.marker("intro", 0, 80)
    comp.marker("outro", OUTRO, N - OUTRO)

    cursor(comp, [(12, [W + 60, H + 70], DECEL), (32, list(TIP), EASE_IN_OUT), (CLICK + 22, list(TIP), EASE_IN),
                  (CLICK + 38, [W + 60, H + 70])], [CLICK], ip=12, op=CLICK + 40, scale=4.2)

    button = comp.null("button", position=CENTER, scale=anim([
        (0, [0, 0], SPRING), (14, [100, 100], LINEAR), (CLICK - 4, [100, 100], EASE_IN), (CLICK, [94, 90], SNAP_OUT),
        (CLICK + 3, [94, 90], OVERSHOOT), (CLICK + 16, [100, 100], LINEAR), (OUTRO, [100, 100], EASE_OUT),
        (OUTRO + 6, [106, 106], EASE_IN), (OUTRO + 18, [0, 0], LINEAR)]))

    click_wipe(comp, [pill(PW, PH)], LOCAL_TIP, CLICK, "secondary", parent=button)
    comp.layer("subscribe", [pill(PW, PH), fill(slot="primary")], parent=button, op=CLICK + 13)
    comp.layer("shadow", [pill(PW, PH), fill("#000000", 22)], parent=button, position=(0, 8))
    return comp


def pop3d():
    """Chunky 3D key: the pointer presses it down into its base and it turns grey."""
    comp = Comp("subscribe-button-click--3d-pop", W, H, fps=30, frames=N)
    comp.slot("primary", "#FF0000")
    comp.slot("secondary", "#606060")
    comp.marker("intro", 0, 80)
    comp.marker("outro", OUTRO, N - OUTRO)
    pw, ph, d = 460, 118, 16
    c = (W / 2, 118)
    tip = (c[0] + 124, c[1] + 18)
    cursor(comp, [(12, [W + 60, H + 70], DECEL), (32, list(tip), EASE_IN_OUT), (CLICK - 3, list(tip), EASE_IN),
                  (CLICK, [tip[0], tip[1] + d * 0.6], EASE_OUT), (CLICK + 8, list(tip), EASE_IN_OUT),
                  (CLICK + 22, list(tip), EASE_IN), (CLICK + 38, [W + 60, H + 70])],
           [CLICK], ip=12, op=CLICK + 40, scale=4.2)
    out = [(OUTRO, [100, 100], EASE_OUT), (OUTRO + 6, [106, 106], EASE_IN), (OUTRO + 18, [0, 0], LINEAR)]
    button = comp.null("button", position=c, scale=anim([
        (0, [0, 0], SPRING), (16, [100, 100], HOLD), (CLICK - 3, [100, 100], EASE_IN), (CLICK, [103, 95], SNAP_OUT),
        (CLICK + 4, [98, 102], EASE_IN_OUT), (CLICK + 14, [100, 100], LINEAR)] + out))
    # the key face sinks into its side on the press
    key = comp.null("key", parent=button, position=anim([
        (CLICK - 3, [0, 0], EASE_IN), (CLICK, [0, d * 0.6], SNAP_OUT), (CLICK + 3, [0, d * 0.6], OVERSHOOT),
        (CLICK + 14, [0, 0])]))
    click_wipe(comp, [pill(pw, ph)], (124, 18), CLICK + 1, "secondary", parent=key)
    body(comp, "red", [pill(pw, ph)], "3d-pop", slot="primary", parent=key, depth=d, shadow=False, op=CLICK + 13)
    body(comp, "grey", [pill(pw, ph)], "3d-pop", slot="secondary", parent=key, depth=d, shadow=False)
    comp.layer("base", [pill(pw + 10, ph + 6), fill("#000000", 30)], parent=button, position=(0, d + 4))
    comp.layer("drop", [pill(pw + 10, ph + 6), fill("#000000", 16)], parent=button, position=(0, d + 12))
    return comp, (c[0] - pw / 2 + 46, c[1] - ph / 2 + 22, pw - 92, ph - 44)


def logo_tab():
    """YouTube-style play icon springs in and a subscribe pill slides out from behind it."""
    p = P.Platform("subscribe-button-click", "YouTube", YOUTUBE + "M9.545 15.568V8.432L15.818 12z", tile="#FFFFFF", glyph_color="#FF0000",
                   glyph_size=0.66, primary="#FF0000", secondary="#606060", rim=False)
    comp = P.classic(p)
    comp.name = "subscribe-button-click--logo-tab"
    return comp


pc, pa = pop3d()
build_asset("call-to-action", "subscribe-button-click", "Subscribe Button Click",
            "Red subscribe button that pops in, gets clicked by a mouse pointer and turns grey. Put your own "
            "\"Subscribe\" text inside the button.",
            ["subscribe", "youtube", "button", "click", "cursor"], [
    Variant("classic", "Classic Pill", classic(), "intro-hold-outro", thumb_t=0.26,
            text_area=(CENTER[0] - PW / 2 + 44, CENTER[1] - PH / 2 + 22, PW - 88, PH - 44),
            description="Flat red subscribe pill that pops in, gets clicked by a mouse pointer and turns grey."),
    Variant("3d-pop", "3D Key", pc, "intro-hold-outro", thumb_t=0.26, text_area=pa,
            description="Chunky 3D key with a highlight rim and depth; the pointer presses it down into its base "
                        "and it turns grey."),
    Variant("logo-tab", "Logo Tab", logo_tab(), "intro-hold-outro", thumb_t=0.34, text_area=P.PILL_TEXT,
            description="A white play-button tile springs in and the red pill slides out from behind it; the click "
                        "turns it grey."),
])
