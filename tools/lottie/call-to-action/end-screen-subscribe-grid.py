from _cta_actions import *

W, H = 1680, 580
N = 150
OUT = 124
AV = (250, 236)
AD = 300
PY, PW, PH = 480, 360, 92
CW, CH = 560, 315
CARDS = ((480 + CW / 2, 236), (1080 + CW / 2, 236))
TITLE_Y = CARDS[0][1] + CH / 2 + 26


def person(k=1.0):
    return [ellipse((110 * k, 110 * k), (0, -38 * k)),
            shape([(-96 * k, 116 * k), (-80 * k, 44 * k), (80 * k, 44 * k), (96 * k, 116 * k)],
                  [0, 50 * k, 50 * k, 0], name="shoulders")]


def play(k=1.0):
    return [shape([(-24 * k, -30 * k), (34 * k, 0), (-24 * k, 30 * k)], 8 * k, name="play")]


def out_scale(t_in, t_out, spring=SPRING):
    return anim([(t_in, [0, 0], spring), (t_in + 16, [100, 100], HOLD), (t_out, [100, 100], EASE_OUT),
                 (t_out + 4, [105, 105], EASE_IN), (t_out + 14, [0, 0])])


def card(comp, style, i, pos, t0):
    t_out = OUT + 4 + i * 4
    n = comp.null(f"card{i}", position=pos, scale=anim([(t_out, [100, 100], EASE_OUT), (t_out + 4, [104, 104], EASE_IN),
                                                         (t_out + 14, [0, 0])]))
    frame = rect((CW, CH), roundness=28)
    ul = [(-CW / 2, CH / 2 + 88), (-CW / 2 + 150, CH / 2 + 88)]  # accent underline below the title area
    comp.layer(f"underline{i}", [polyline(ul), trim(end=anim([(t0 + 18, 0, SNAP_OUT), (t0 + 34, 100)])),
                                 stroke(slot="primary", width=8)], parent=n, ip=t0 + 18)
    pb = pop(t0 + 12, 16)
    if style == "3d-pop":
        body(comp, f"play{i}-icon", play(), "classic", slot="icon", parent=n, shadow=False, scale=pb)
        body(comp, f"play{i}", [ellipse((110, 110))], style, slot="primary", parent=n, depth=8, scale=pb)
        body(comp, f"card{i}-body", [frame], style, slot="background", parent=n, depth=16,
             scale=anim([(t0, [0, 0], SPRING), (t0 + 16, [100, 100])]))
        return
    draw = trim(end=anim([(t0, 0, EASE_IN_OUT), (t0 + 22, 100)]), offset=anim([(t0, -30, EASE_IN_OUT), (t0 + 22, 0)]))
    if style == "outline":
        body(comp, f"play{i}", play(), style, parent=n, line=5, scale=pb, position=(4, 0))
        comp.layer(f"play{i}-ring", [ellipse((110, 110)), stroke(slot="primary", width=6)], parent=n, scale=pb)
        comp.layer(f"card{i}-frame", [frame, draw, stroke(slot="outline", width=6)], parent=n)
        # corner ticks give the line-art card a viewfinder feel
        comp.layer(f"card{i}-inner", [rect((CW - 40, CH - 40), roundness=16),
                                      stroke(slot="outline", width=2, opacity=40, dashes=[10, 12])], parent=n,
                   opacity=fade(t0 + 16, dur=10))
    else:
        body(comp, f"play{i}-icon", play(), "classic", slot="icon", parent=n, shadow=False, scale=pb, position=(4, 0))
        comp.layer(f"play{i}", [ellipse((110, 110)), fill(slot="primary")], parent=n, scale=pb)
        comp.layer(f"card{i}-frame", [frame, draw, stroke(slot="outline", width=6)], parent=n)
        comp.layer(f"card{i}-fill", [frame, fill(slot="background", opacity=anim([(t0 + 10, 0, EASE_OUT),
                                                                                  (t0 + 24, 70)]))], parent=n)
        comp.layer(f"card{i}-shadow", [frame, fill("#000000", anim([(t0 + 10, 0, EASE_OUT), (t0 + 24, 22)]))],
                   parent=n, position=(0, 10))


def make(style):
    comp = Comp(f"end-screen-subscribe-grid--{style}", W, H, fps=30, frames=N)
    comp.marker("intro", 0, 60)
    comp.marker("outro", OUT, N - OUT)
    comp.slot("primary", "#FF2E4D")
    comp.slot("outline", "#FFFFFF")
    if style != "outline":
        comp.slot("secondary", "#3D3D4A")
        comp.slot("background", "#1F1F27")
    if style != "outline":
        comp.slot("icon", "#FFFFFF")
    # subscribe pill under the avatar
    tr = label(comp, style, AV[0] - PW / 2, PY, PW, PH, 14, slot="primary", out_at=OUT, depth=10)
    # avatar placeholder
    av = comp.null("avatar", position=AV, scale=out_scale(0, OUT))
    ring = [ellipse((AD, AD))]
    ringdraw = trim(end=anim([(2, 0, EASE_IN_OUT), (24, 100)]))
    if style == "outline":
        body(comp, "person", person(0.84), style, parent=av, line=5, scale=pop(10, 16), position=(0, -6))
        comp.layer("avatar-ring", [group([ellipse((AD, AD)), ringdraw, stroke(slot="primary", width=8)], "r",
                                         rotation=-90)], parent=av)
        comp.layer("avatar-inner", [ellipse((AD - 34, AD - 34)), stroke(slot="outline", width=4)], parent=av,
                   opacity=fade(12, dur=10))
    elif style == "classic":
        comp.layer("person-clip", [ellipse((AD - 30, AD - 30)), fill()], parent=av)
        comp.layer("person", [group(person() + [fill(slot="outline", opacity=70)], "p")], parent=av, matte="alpha",
                   position=anim([(8, [0, 120], DECEL), (24, [0, 10])]))
        comp.layer("avatar-ring", [group([ellipse((AD, AD)), ringdraw, stroke(slot="primary", width=10)], "r",
                                         rotation=-90)], parent=av)
        comp.layer("avatar-disc", [ellipse((AD - 30, AD - 30)), fill(slot="secondary")], parent=av,
                   scale=pop(0, 16))
    else:
        comp.layer("person-clip", [ellipse((AD - 40, AD - 40)), fill()], parent=av)
        comp.layer("person", [group(person() + [fill(slot="outline", opacity=70)], "p")], parent=av, matte="alpha",
                   position=(0, 10))
        body(comp, "avatar-disc", [ellipse((AD - 40, AD - 40))], "classic", slot="secondary", parent=av, shadow=False)
        body(comp, "avatar-rim", ring, style, slot="primary", parent=av, depth=16)
    for i, pos in enumerate(CARDS):
        card(comp, style, i, pos, 10 + i * 8)
    return comp, tr


def variant(s):
    comp, tr = make(s)
    areas = {"subscribe": tr}
    for i, (x, y) in enumerate(CARDS):
        areas[f"video{i + 1}"] = (x - CW / 2, TITLE_Y, CW, 56)
    return Variant(s, STYLE_NAMES[s], comp, "intro-hold-outro", thumb_t=0.6, text_area=tr, text_areas=areas,
                   description=STYLE_DESC[s])


build_asset(CATEGORY, "end-screen-subscribe-grid", "End Screen Subscribe Grid",
            "End-screen layout: a round channel-avatar placeholder with a subscribe pill and two 16:9 "
            "video-card placeholders that draw in. Drop your videos over the cards and type into the "
            "named text areas (subscribe, video1, video2 titles).",
            ["end screen", "outro", "subscribe", "video", "youtube", "layout", "channel"], [variant(s) for s in STYLES])
