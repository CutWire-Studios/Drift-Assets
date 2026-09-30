"""Party popper: the cone winds up, recoils with a pop and fires confetti and curly streamers
(loop)."""

from _reactions2 import *

T = 60
W, H = 500, 500
PX, PY = 150, 400             # cone tip pivot
ANG = 40                      # cone tilt (degrees clockwise from pointing up)
CONE, BAND, INSIDE = "#FFC23D", "#FF4D6D", "#5B2A86"
COLORS = [("secondary", "#FF4D6D"), ("accent", "#2EC4B6"), ("primary", "#FFC23D"),
          (None, "#7B61FF")]
POP = 8

# cone in local space: tip at (0, 0), mouth centred at (0, -200)
CL, MW = 200, 84


def cone_d():
    return f"M 0 18 C -8 18 -12 10 -10 0 L {-MW} {-CL} L {MW} {-CL} L 10 0 C 12 10 8 18 0 18 Z"


def band_d(y0, y1):
    """Stripe across the cone between heights y0 > y1 (both negative)."""
    w0, w1 = MW * -y0 / CL, MW * -y1 / CL
    return f"M {-w0:.1f} {y0} L {-w1:.1f} {y1} L {w1:.1f} {y1} L {w0:.1f} {y0} Z"


def mouth_world():
    a = math.radians(ANG)
    return (PX + CL * math.sin(a), PY - CL * math.cos(a))


def recoil(t):
    return -bump(t, 0, POP) * 0.5 + bump(t, POP, POP + 12)


def make(kind):
    st = Style(kind)
    comp = Comp("emoji-party-popper", W, H, frames=T)
    for sid, c in COLORS:
        if sid:
            comp.slot(sid, c)
    comp.slot("background", INSIDE)
    if not st.glossy:
        comp.slot("outline", WHITE if st.flat else st.ink)

    mx, my = mouth_world()
    a0 = math.radians(ANG)
    r = rng(21)
    # confetti pieces
    for i in range(26):
        spread = math.radians(r.gauss(0, 30))
        ang = a0 + spread
        sp = r.uniform(13, 22)
        vx, vy = sp * math.sin(ang), -sp * math.cos(ang)
        life = r.randint(34, 46)
        spin = r.uniform(12, 26) * r.choice((-1, 1))
        sid, col = COLORS[i % 4]
        kind_ = i % 3
        if kind_ == 0:
            sh = [rect((14, 24), roundness=2)]
        elif kind_ == 1:
            sh = [ellipse((16, 16))]
        else:
            sh = S(star_d(12, 0.5))
        paint = [fill(col, slot=sid)]
        if st.outline:
            paint = [stroke(st.ink, 4, slot="outline")] + paint
        elif st.flat:
            paint = paint + [stroke(WHITE, 7, slot="outline")]

        def fn(u, vx=vx, vy=vy, spin=spin, life=life):
            drag = 0.9
            f = (1 - drag ** u) / (1 - drag)
            x = mx + vx * f
            y = my + vy * f + 0.12 * u * u
            flip = math.cos(u * 0.35 + vx)
            s = 100 * min(1, 0.3 + u / 4)
            return {"position": (x, y), "rotation": spin * u,
                    "scale": (s * (0.35 + 0.65 * abs(flip)), s),
                    "opacity": 100 if u < life - 10 else 100 * (life - u) / 10}

        particle(comp, f"confetti{i}", [group(sh + paint)], POP + r.uniform(0, 3), life, T, fn,
                 step=2)

    # curly streamers shooting out
    for j, (off, curl, (sid, col)) in enumerate([(-22, 1, COLORS[0]), (6, -1, COLORS[1]),
                                                 (30, 1, COLORS[3])]):
        ang = math.radians(ANG + off)
        pts = []
        for k in range(9):
            d = 28 * k
            wig = curl * 16 * math.sin(k * 1.5)
            pts.append((mx + d * math.sin(ang) + wig * math.cos(ang), my - d * math.cos(ang) + wig * math.sin(ang)))
        items = [smooth_open(pts)]
        lst = [path(items[0]),
               trim(start=anim([(POP + 6, 0, EASE_IN), (POP + 26, 100)]),
                    end=anim([(POP, 0, SNAP_OUT), (POP + 12, 100)])),
               stroke(col, 9, slot=sid)]
        if st.outline:
            lst.append(stroke(st.ink, 17, slot="outline"))
        elif st.flat:
            lst.append(stroke(WHITE, 19, slot="outline"))
        comp.layer(f"streamer{j}", [group(lst)], ip=POP, op=POP + 27)

    # pop flash at the mouth
    comp.layer("flash", [group(S(star_d(60, 0.42)) + [fill("#FFF4B8")])], position=(mx, my),
               ip=POP, op=POP + 7, rotation=ANG,
               scale=anim([(POP, [20, 20], SNAP_OUT), (POP + 4, [110, 110], EASE_IN), (POP + 7, [60, 60])]),
               opacity=anim([(POP, 100), (POP + 4, 100), (POP + 7, 0)]))

    cone = comp.null("cone", position=(PX, PY),
                     rotation=sampled(lambda t: ANG + 8 * recoil(t), 0, T),
                     scale=sampled(lambda t: [100 + 6 * bump(t, 0, POP) - 4 * bump(t, POP, POP + 8),
                                              100 - 8 * bump(t, 0, POP) + 8 * bump(t, POP, POP + 8)], 0, T))
    mouth = S(f"M {-MW} {-CL} A {MW} 22 0 1 1 {MW} {-CL} A {MW} 22 0 1 1 {-MW} {-CL} Z")
    bands = [S(band_d(-40, -64)), S(band_d(-100, -126)), S(band_d(-160, -184))]
    top = [group(mouth + st.paint(INSIDE, "background", lw=FLINE), name="mouth")]
    top += [group(b + [fill(BAND, slot="secondary")], name=f"band{i}") for i, b in enumerate(bands)]
    if st.glossy:
        top.insert(1, group(S(f"M -54 -170 L -14 -24 L -4 -28 L -34 -170 Z") + [fill(WHITE, 40)], name="spec"))
    body = S(cone_d())
    comp.layer("cone-art", top + [group(body + mouth + st.paint(CONE, "primary", (-MW, -CL, MW, 18),
                                                                 sil=True, under=True), name="cone")] +
               st.shadow(body + mouth), parent=cone)
    return comp


build3("emoji-party-popper", "Emoji Party Popper",
       "Party popper that winds up, recoils with a pop and fires confetti and curly streamers; for "
       "celebrations and announcements. Seamless loop.",
       ["emoji", "party", "popper", "celebrate", "confetti", "congrats", "tada", "reaction"], make, [
           ("glossy", "Glossy", "loop", 0.4, "Shaded cone with soft highlights."),
           ("flat", "Flat Sticker", "loop", 0.4, "Flat colours with white die-cut borders on every piece."),
           ("outline", "Bold Outline", "loop", 0.4, "Cartoon line art with bold black outlines."),
       ])
