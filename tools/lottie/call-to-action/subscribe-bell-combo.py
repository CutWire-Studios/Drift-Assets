from _common import *
from _cta_actions import body
from drift_lottie import Variant, build_asset
from lottie_kit import svg_shapes

W, H = 960, 270
N = 150
Y = 118
THUMB_C = (126, Y)
PILL_C = (484, Y)
BELL_C = (830, Y)
PW, PH = 440, 116
BS = 0.64  # bell scale

C_THUMB, C_PILL, C_BELL = 36, 66, 94
OUTRO = 128


def outro(t0, keys):
    return keys + [(t0, [100, 100], EASE_OUT), (t0 + 5, [108, 108], EASE_IN), (t0 + 15, [0, 0], LINEAR)]


def base(name):
    comp = Comp(name, W, H, fps=30, frames=N)
    comp.slot("primary", "#FF0000")
    comp.slot("secondary", "#606060")
    comp.slot("accent", "#3EA6FF")
    comp.slot("icon", "#FFFFFF")
    comp.marker("intro", 0, 124)
    comp.marker("outro", OUTRO, N - OUTRO)
    return comp


def classic():
    """Line icons and a flat pill: the pointer taps the thumb (fills), the pill (turns grey) and the bell (rings)."""
    comp = base("subscribe-bell-combo")

    # ---------------------------------------------------------------- cursor
    tip_thumb = (THUMB_C[0] + 22, THUMB_C[1] + 18)
    pill_local = (120, 16)
    tip_pill = (PILL_C[0] + pill_local[0], PILL_C[1] + pill_local[1])
    tip_bell = (BELL_C[0] + 10, BELL_C[1] + 22)
    cursor(comp, [(14, [40, H + 90], DECEL), (32, list(tip_thumb), EASE_IN_OUT), (C_THUMB + 8, list(tip_thumb), EASE_IN_OUT),
                  (C_PILL - 6, list(tip_pill), EASE_IN_OUT), (C_PILL + 8, list(tip_pill), EASE_IN_OUT),
                  (C_BELL - 6, list(tip_bell), EASE_IN_OUT), (C_BELL + 16, list(tip_bell), EASE_IN),
                  (C_BELL + 32, [W + 40, H + 90])],
           [C_THUMB, C_PILL, C_BELL], ip=14, op=C_BELL + 33, scale=3.9)

    # ---------------------------------------------------------------- thumb
    TS, TSW = 116, 8.5
    t_pivot = (THUMB_C[0] - 30, THUMB_C[1] + 50)
    t_local = (THUMB_C[0] - t_pivot[0], THUMB_C[1] - t_pivot[1])
    thumb = comp.null("thumb", position=t_pivot, scale=anim(outro(OUTRO, [
        (0, [0, 0], SPRING), (13, [100, 100], EASE_IN_OUT), (C_THUMB - 3, [100, 100], EASE_IN),
        (C_THUMB, [86, 86], SNAP_OUT), (C_THUMB + 6, [124, 124], EASE_IN_OUT), (C_THUMB + 13, [95, 95], EASE_IN_OUT),
        (C_THUMB + 20, [101, 101], EASE_IN_OUT), (C_THUMB + 26, [100, 100], EASE_IN_OUT)])),
        rotation=anim([(0, -25, SNAP_OUT), (13, 0, EASE_IN_OUT), (C_THUMB - 3, 0, EASE_IN), (C_THUMB, 8, SNAP_OUT),
                       (C_THUMB + 6, -16, EASE_IN_OUT), (C_THUMB + 14, 5, EASE_IN_OUT), (C_THUMB + 21, -2, EASE_IN_OUT),
                       (C_THUMB + 28, 0)]))
    comp.layer("thumb-matte", [group([ellipse(anim([(C_THUMB, [0, 0], EASE_OUT), (C_THUMB + 9, [300, 300])])), fill()],
                                     "wipe")], parent=thumb)
    comp.layer("thumb-fill", [group(glyph(THUMB, TS, t_local) + [fill(slot="accent"), stroke(slot="accent", width=TSW)],
                                    "thumb")], parent=thumb, matte="alpha")
    comp.layer("thumb-outline", [group(glyph(THUMB, TS, t_local) + [stroke(slot="icon", width=TSW)], "thumb")],
               parent=thumb, op=C_THUMB + 10)
    burst(comp, THUMB_C, C_THUMB + 3, 82, 104, count=8, slot="accent", width=7, rotation=22.5)

    # ---------------------------------------------------------------- pill
    button = comp.null("button", position=PILL_C, scale=anim(outro(OUTRO + 3, [
        (0, [0, 0], HOLD), (5, [0, 0], SPRING), (19, [100, 100], LINEAR), (C_PILL - 4, [100, 100], EASE_IN),
        (C_PILL, [95, 90], SNAP_OUT), (C_PILL + 3, [95, 90], OVERSHOOT), (C_PILL + 16, [100, 100], LINEAR)])))
    click_wipe(comp, [pill(PW, PH)], pill_local, C_PILL, "secondary", parent=button)
    comp.layer("subscribe", [pill(PW, PH), fill(slot="primary")], parent=button, op=C_PILL + 13)
    comp.layer("shadow", [pill(PW, PH), fill("#000000", 22)], parent=button, position=(0, 7))

    # ---------------------------------------------------------------- bell
    R = C_BELL
    bell_pop = comp.null("bell-pop", position=BELL_C, scale=anim(outro(OUTRO + 6, [
        (0, [0, 0], HOLD), (10, [0, 0], SPRING), (23, [100, 100], LINEAR), (R - 3, [100, 100], EASE_IN),
        (R, [88, 88], SNAP_OUT), (R + 8, [108, 108], EASE_IN_OUT), (R + 18, [100, 100], LINEAR)])))
    bell = comp.null("bell", parent=bell_pop, position=(0, -88 * BS), rotation=anim([
        (R - 1, 0, EASE_OUT), (R + 4, 22), (R + 10, -19), (R + 16, 15), (R + 22, -11), (R + 28, 7), (R + 34, -4),
        (R + 40, 1.5), (R + 46, 0)]))
    bell_path = BELL_BODY
    bell_items = svg_shapes(bell_path, BS, name="body")
    comp.layer("bell-fill", [group(bell_items + [fill(slot="icon")], "fill")], parent=bell, ip=R + 1,
               opacity=anim([(R + 1, 0, EASE_OUT), (R + 4, 100)]))
    comp.layer("bell-outline", [
        group([ellipse((20 * BS, 20 * BS), (0, 3 * BS)), fill(slot="icon")], "knob"),
        group(bell_items + [stroke(slot="icon", width=8.5)], "outline")], parent=bell)
    comp.layer("clapper", [group([path(arc_pts(15 * BS, 0, 180, (0, 156 * BS))),
                                  stroke(slot="icon", width=8.5)], "clapper")], parent=bell,
               rotation=anim([(R - 1, 0), (R + 2, -8), (R + 8, 10), (R + 14, -8), (R + 20, 6), (R + 26, -4), (R + 32, 3),
                              (R + 38, -1), (R + 44, 0)]))
    rays = []
    for side, (a0, a1) in (("r", (-40, -8)), ("l", (188, 220))):
        for i, r in enumerate((82, 100)):
            d = i * 3
            rays.append(group([path(arc_pts(r, a0, a1)),
                               trim(start=anim([(R + d, 50, SNAP_OUT), (R + 10 + d, 0)]),
                                    end=anim([(R + d, 50, SNAP_OUT), (R + 10 + d, 100)])),
                               stroke(slot="icon", width=7, opacity=anim([(R + 20 + d, 100, EASE_IN), (R + 32 + d, 0)]))],
                              f"{side}{i}"))
    comp.layer("rays", rays, ip=R, op=R + 36, position=(BELL_C[0], BELL_C[1] + 6),
               scale=anim([(R, [92, 92], SNAP_OUT), (R + 34, [104, 104])]))
    return comp


def pointer(comp, tips):
    tip_thumb, tip_pill, tip_bell = tips
    cursor(comp, [(14, [40, H + 90], DECEL), (32, list(tip_thumb), EASE_IN_OUT),
                  (C_THUMB + 8, list(tip_thumb), EASE_IN_OUT), (C_PILL - 6, list(tip_pill), EASE_IN_OUT),
                  (C_PILL + 8, list(tip_pill), EASE_IN_OUT), (C_BELL - 6, list(tip_bell), EASE_IN_OUT),
                  (C_BELL + 16, list(tip_bell), EASE_IN), (C_BELL + 32, [W + 40, H + 90])],
           [C_THUMB, C_PILL, C_BELL], ip=14, op=C_BELL + 33, scale=3.9)


def bell_rays(comp, R, slot="icon", width=7):
    rays = []
    for side, (a0, a1) in (("r", (-40, -8)), ("l", (188, 220))):
        for i, r in enumerate((82, 100)):
            d = i * 3
            rays.append(group([path(arc_pts(r, a0, a1)),
                               trim(start=anim([(R + d, 50, SNAP_OUT), (R + 10 + d, 0)]),
                                    end=anim([(R + d, 50, SNAP_OUT), (R + 10 + d, 100)])),
                               stroke(slot=slot, width=width,
                                      opacity=anim([(R + 20 + d, 100, EASE_IN), (R + 32 + d, 0)]))], f"{side}{i}"))
    comp.layer("rays", rays, ip=R, op=R + 36, position=(BELL_C[0], BELL_C[1] + 6),
               scale=anim([(R, [92, 92], SNAP_OUT), (R + 34, [104, 104])]))


def rise(t0, dy=70):
    """Null position offset keys: rises from below at t0 (tray entrance)."""
    return [(0, [0, dy], HOLD), (t0, [0, dy], (0.2, 0.9, 0.3, 1.0)), (t0 + 16, [0, 0], HOLD), (OUTRO, [0, 0], EASE_IN),
            (OUTRO + 14, [0, dy], LINEAR)]


def combo(style):
    """3d-pop: chunky layered icons and a 3D key. tray: line icons on a frosted tray, rising in one by one."""
    comp = base(f"subscribe-bell-combo--{style}")
    tray = style == "tray"
    tips = ((THUMB_C[0] + 22, THUMB_C[1] + 18), (PILL_C[0] + 120, PILL_C[1] + 16), (BELL_C[0] + 10, BELL_C[1] + 22))
    pointer(comp, tips)

    def pop(t0, click, amt=(86, 124, 95, 101)):
        k = [(0, [0, 0], HOLD), (t0, [0, 0], SPRING), (t0 + 13, [100, 100], EASE_IN_OUT)] if not tray else \
            [(0, [100, 100], HOLD)]
        k += [(click - 3, [100, 100], EASE_IN), (click, [amt[0], amt[0]], SNAP_OUT),
              (click + 6, [amt[1], amt[1]], EASE_IN_OUT), (click + 13, [amt[2], amt[2]], EASE_IN_OUT),
              (click + 20, [amt[3], amt[3]], EASE_IN_OUT), (click + 26, [100, 100], EASE_IN_OUT)]
        return anim(outro(OUTRO, k)) if not tray else anim(k)

    def holder(name, pos, t0):
        """Entrance carrier: rises in for the tray, static otherwise."""
        if tray:
            return comp.null(name + "-in", position=anim([(t, [pos[0] + v[0], pos[1] + v[1]], e)
                                                          for t, v, e in rise(t0)]),
                             scale=anim([(0, [0, 0], HOLD), (t0, [40, 40], (0.2, 0.9, 0.3, 1.0)), (t0 + 14, [100, 100], HOLD),
                                         (OUTRO, [100, 100], EASE_IN), (OUTRO + 14, [0, 0])]))
        return comp.null(name + "-in", position=pos)

    # ------------------------------------------------------------ thumb
    TS = 116 if tray else 124
    t_in = holder("thumb", (THUMB_C[0] - 30, THUMB_C[1] + 50), 8)
    t_local = (30, -50)
    thumb = comp.null("thumb", parent=t_in, scale=pop(0, C_THUMB),
                      rotation=anim([(0, -25 if not tray else 0, SNAP_OUT), (13, 0, EASE_IN_OUT), (C_THUMB - 3, 0, EASE_IN),
                                     (C_THUMB, 8, SNAP_OUT), (C_THUMB + 6, -16, EASE_IN_OUT), (C_THUMB + 14, 5, EASE_IN_OUT),
                                     (C_THUMB + 21, -2, EASE_IN_OUT), (C_THUMB + 28, 0)]))
    geo = glyph(THUMB, TS, t_local, name="thumb")
    if tray:
        comp.layer("thumb-matte", [group([ellipse(anim([(C_THUMB, [0, 0], EASE_OUT), (C_THUMB + 9, [300, 300])])),
                                          fill()], "wipe")], parent=thumb)
        comp.layer("thumb-fill", [group(glyph(THUMB, TS, t_local) + [fill(slot="accent")], "thumb")], parent=thumb,
                   matte="alpha")
        body(comp, "thumb-line", geo, "outline", parent=thumb, line=4.5, line_slot="icon", op=C_THUMB + 10)
    else:
        body(comp, "thumb-3d", geo, "3d-pop", slot="accent", parent=thumb, depth=12)
    burst(comp, THUMB_C, C_THUMB + 3, 82, 104, count=8, slot="accent", width=7, rotation=22.5)

    # ------------------------------------------------------------ pill
    p_in = holder("pill", PILL_C, 14)
    press = [(C_PILL - 4, [100, 100], EASE_IN), (C_PILL, [95, 90], SNAP_OUT), (C_PILL + 3, [95, 90], OVERSHOOT),
             (C_PILL + 16, [100, 100], LINEAR)]
    if tray:
        button = comp.null("button", parent=p_in, scale=anim(press))
        click_wipe(comp, [pill(PW, PH)], (120, 16), C_PILL, "secondary", parent=button)
        comp.layer("subscribe", [pill(PW, PH), fill(slot="primary")], parent=button, op=C_PILL + 13)
    else:
        d = 14
        button = comp.null("button", parent=p_in, scale=anim(outro(OUTRO + 3, [
            (0, [0, 0], HOLD), (5, [0, 0], SPRING), (19, [100, 100], LINEAR)] + press)))
        key = comp.null("key", parent=button, position=anim([
            (C_PILL - 3, [0, 0], EASE_IN), (C_PILL, [0, d * 0.6], SNAP_OUT), (C_PILL + 3, [0, d * 0.6], OVERSHOOT),
            (C_PILL + 14, [0, 0])]))
        click_wipe(comp, [pill(PW, PH)], (120, 16), C_PILL + 1, "secondary", parent=key)
        body(comp, "red", [pill(PW, PH)], "3d-pop", slot="primary", parent=key, depth=d, shadow=False, op=C_PILL + 13)
        body(comp, "grey", [pill(PW, PH)], "3d-pop", slot="secondary", parent=key, depth=d, shadow=False)
        comp.layer("base", [pill(PW + 8, PH + 6), fill("#000000", 30)], parent=button, position=(0, d + 4))

    # ------------------------------------------------------------ bell
    R = C_BELL
    b_in = holder("bell", BELL_C, 20)
    ring = [(R - 3, [100, 100], EASE_IN), (R, [88, 88], SNAP_OUT), (R + 8, [108, 108], EASE_IN_OUT),
            (R + 18, [100, 100], LINEAR)]
    bell_pop = comp.null("bell-pop", parent=b_in, scale=anim(
        ring if tray else outro(OUTRO + 6, [(0, [0, 0], HOLD), (10, [0, 0], SPRING), (23, [100, 100], LINEAR)] + ring)))
    bell = comp.null("bell", parent=bell_pop, position=(0, -88 * BS), rotation=anim([
        (R - 1, 0, EASE_OUT), (R + 4, 22), (R + 10, -19), (R + 16, 15), (R + 22, -11), (R + 28, 7), (R + 34, -4),
        (R + 40, 1.5), (R + 46, 0)]))
    clap_rot = anim([(R - 1, 0), (R + 2, -8), (R + 8, 10), (R + 14, -8), (R + 20, 6), (R + 26, -4), (R + 32, 3),
                     (R + 38, -1), (R + 44, 0)])
    bs = BS if tray else BS * 1.08
    bell_geo = svg_shapes(BELL_BODY, bs, name="body") + [ellipse((26 * bs, 26 * bs), (0, 10 * bs), name="knob")]
    clap_geo = svg_shapes(BELL_CLAPPER, bs, name="clapper")
    if tray:
        comp.layer("bell-fill", [group(bell_geo + [fill(slot="icon")], "fill")], parent=bell, ip=R + 1,
                   opacity=anim([(R + 1, 0, EASE_OUT), (R + 4, 100)]))
        body(comp, "bell-line", bell_geo, "outline", parent=bell, line=4.5, line_slot="icon")
        body(comp, "clapper-line", clap_geo, "outline", parent=bell, line=4.5, line_slot="icon", rotation=clap_rot)
    else:
        body(comp, "bell-3d", bell_geo, "3d-pop", slot="icon", parent=bell, depth=12)
        body(comp, "clapper-3d", clap_geo, "3d-pop", slot="icon", parent=bell, depth=6, shadow=False, rotation=clap_rot)
    bell_rays(comp, R)

    if tray:
        tw, th = W - 40, 196
        size = anim([(0, [th, th], (0.2, 0.9, 0.3, 1.0)), (14, [tw, th], HOLD), (OUTRO + 6, [tw, th], EASE_IN),
                     (OUTRO + 20, [th, th])])
        op = anim([(0, 0, EASE_OUT), (4, 100, HOLD), (OUTRO + 14, 100, EASE_IN), (OUTRO + 20, 0)])
        comp.layer("tray-rim", [rect(size, roundness=th / 2), stroke(slot="background", width=2.5, opacity=45)],
                   position=(W / 2, Y), opacity=op)
        comp.layer("tray", [rect(size, roundness=th / 2), fill(slot="background", opacity=14)], position=(W / 2, Y),
                   opacity=op)
        comp.layer("tray-shadow", [rect(size, roundness=th / 2), fill("#000000", 22)], position=(W / 2, Y + 8),
                   opacity=op)
        comp.slot("background", "#FFFFFF")
    return comp


build_asset("call-to-action", "subscribe-bell-combo", "Subscribe Bell Combo",
            "Like, subscribe and bell in a row: a pointer taps the thumb (fills blue), the subscribe pill (turns grey) "
            "and the bell (rings). Put your own \"Subscribe\" text inside the pill.",
            ["subscribe", "like", "bell", "youtube", "cursor", "click"], [
    Variant("classic", "Classic", classic(), "intro-hold-outro", thumb_t=0.2,
            text_area=(PILL_C[0] - PW / 2 + 40, PILL_C[1] - PH / 2 + 20, PW - 80, PH - 40),
            description="Line-art thumb and bell either side of a flat red pill, each popping in on a spring."),
    Variant("3d-pop", "3D Pop", combo("3d-pop"), "intro-hold-outro", thumb_t=0.2,
            text_area=(PILL_C[0] - PW / 2 + 40, PILL_C[1] - PH / 2 + 20, PW - 80, PH - 40),
            description="Chunky layered 3D thumb, key and bell; the pill presses down into its base when clicked."),
    Variant("tray", "Glass Tray", combo("tray"), "intro-hold-outro", thumb_t=0.2, bg="3a1c24",
            text_area=(PILL_C[0] - PW / 2 + 40, PILL_C[1] - PH / 2 + 20, PW - 80, PH - 40),
            description="A frosted glass tray stretches open and the line-art thumb, pill and bell rise into it one "
                        "by one."),
])
