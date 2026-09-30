from _lt2 import *


def blink(t0, t_out, period=16):
    """Cursor visibility: on from t0, blinking every `period` frames until t_out."""
    k = [(0, 0, HOLD), (t0, 100, HOLD)]
    t, on = t0 + period, False
    while t < t_out:
        k.append((t, 100 if on else 0, HOLD))
        on = not on
        t += period // 2 if on else period
    k.append((t_out, 0, HOLD))
    k.append((t_out + 1, 0))
    return keys(*k)


def square_bracket(x, y0, y1, arm, side=1):
    """[ when side=1, ] when side=-1; x is the spine."""
    return poly([(x + arm * side, y0), (x, y0), (x, y1), (x + arm * side, y1)], False)


def chevron(x, cy, s):
    return poly([(x, cy - s), (x + s * 0.9, cy), (x, cy + s)], False)


def curly(x, y0, y1, w, side=1):
    """{ when side=1 (x = left tip), } when side=-1 (x = right tip)."""
    ym, r, k = (y0 + y1) / 2, w * 0.9, 0.55
    s = side
    v = [(x + w * s, y0), (x + w / 2 * s, y0 + r), (x + w / 2 * s, ym - r), (x, ym), (x + w / 2 * s, ym + r),
         (x + w / 2 * s, y1 - r), (x + w * s, y1)]
    it = [(0, 0), (0, -r * k), (0, 0), (w / 2 * k * s, 0), (0, -r * k), (0, 0), (-w / 2 * k * s, 0)]
    ot = [(-w / 2 * k * s, 0), (0, 0), (0, r * k), (w / 2 * k * s, 0), (0, 0), (0, r * k), (0, 0)]
    return path(bezier(v, it, ot, closed=False), "brace")


def brackets():
    W, H = 1100, 230
    x0, x1, y0, y1 = 60, 1040, 36, 190
    cx = (x0 + x1) / 2
    comp = base("lower-third-terminal-bracket", W, H, 36)
    comp.slot("accent", "#3DFF8C")
    comp.slot("primary", "#0D1117")
    comp.slot("secondary", "#3DFF8C")
    lay(comp, "cursor", [rrect(x1 - 70, y0 + 28, 24, 48), fill(slot="accent")], opacity=blink(30, 120))
    comp.layer("prompt", [chevron(x0 + 40, y0 + 52, 14), stroke(slot="accent", width=6, cap="square", join="miter"),
                          draw_rev(22, 30, 118, 124)])
    comp.layer("scan", [rrect(x0 + 40, y1 - 44, 300, 2), fill(slot="secondary", opacity=50)],
               opacity=fade(26, 34, 116, 122))
    for side, x in ((1, x0), (-1, x1)):
        lay(comp, f"bracket{side}", [square_bracket(x, y0, y1, 26, side),
                                     stroke(slot="accent", width=7, cap="square", join="miter")],
            off=keys((0, [cx - x, 0], HOLD), (6, [cx - x, 0], INOUT), (26, [0, 0], HOLD), (120, [0, 0], INOUT),
                     (140, [cx - x, 0])),
            opacity=keys((0, 0, HOLD), (2, 100, HOLD), (140, 100, HOLD), (141, 0)))
    comp.layer("panel", [rect_grow(x0, y0, x1 - x0, y1 - y0, 0, 6, 26, 120, 140, "centre", start=0),
                         fill(slot="primary", opacity=88)])
    # the brackets first draw vertically at the centre
    return comp, (x0 + 80, y0 + 26, x1 - x0 - 170, 54), (x0 + 80, y0 + 94, x1 - x0 - 170, 30)


def window():
    W, H = 1000, 260
    x, y, w, tb, bh = 50, 30, 860, 34, 150
    comp = base("lower-third-terminal-bracket--window", W, H, 38)
    comp.slot("primary", "#161B22")
    comp.slot("secondary", "#2D333B")
    comp.slot("accent", "#58A6FF")
    body_y = y + tb
    lay(comp, "cursor", [rrect(x + w - 60, body_y + 30, 22, 44), fill(slot="accent")], opacity=blink(34, 120))
    comp.layer("prompt", [chevron(x + 34, body_y + 52, 13), stroke(slot="accent", width=6, cap="square",
                                                                     join="miter"), draw_rev(24, 32, 118, 124)])
    comp.layer("prompt2", [chevron(x + 34, body_y + 110, 9), stroke(slot="accent", width=4, cap="square",
                                                                      join="miter", opacity=60),
                           draw_rev(28, 36, 116, 122)])
    for i, col in enumerate(("#FF5F57", "#FEBC2E", "#28C840")):
        cx = x + 26 + i * 24
        lay(comp, f"light{i}", [ellipse((13, 13), (cx, y + tb / 2)), fill(col)], (cx, y + tb / 2),
            scale=pop(10 + 2 * i, 22 + 2 * i, 124, 132))
    comp.layer("titlebar", [rect_grow(x, y, w, tb, 0, 0, 18, 126, 142, "left", start=0), fill(slot="secondary")])
    comp.layer("body", [rect_grow(x, body_y, w, bh, 0, 12, 30, 120, 132, "top", start=0), fill(slot="primary")])
    comp.layer("shadow", shadow(x, y, w, tb + bh, 0, dy=12, n=4, spread=5, op=6), opacity=fade(24, 34, 118, 126))
    return comp, (x + 70, body_y + 22, w - 150, 60), (x + 60, body_y + 94, w - 140, 32)


def curly_glitch():
    W, H = 1100, 230
    x0, x1, y0, y1 = 70, 1030, 34, 196
    comp = base("lower-third-terminal-bracket--glitch", W, H, 30)
    comp.slot("accent", "#C792EA")
    comp.slot("secondary", "#82AAFF")

    def braces(col=None):
        st = stroke(col, width=7) if col else stroke(slot="accent", width=7)
        return [group([curly(x0, y0, y1, 34, 1), st], "left"), group([curly(x1, y0, y1, 34, -1), st], "right")]

    lay(comp, "cursor", [rrect(x1 - 90, y0 + 36, 22, 46), fill(slot="secondary")], opacity=blink(30, 120))
    lay(comp, "rule", [rrect(x0 + 60, y0 + 104, 400, 3), fill(slot="secondary", opacity=70)], (x0 + 60, 0),
        scale=grow_x(18, 34, 116, 124))
    lay(comp, "braces", braces(), off=glitch_off(0, 120, 40), opacity=glitch_vis(0, 120))
    glitch_ghosts(comp, braces, 0, 120, amp=18)
    lay(comp, "scanlines", [group([rrect(x0, y0 + i * 18, x1 - x0, 5), fill("#FFFFFF", 10)], f"s{i}")
                            for i in range(9)], opacity=ghost_vis(0, 120))
    return comp, (x0 + 60, y0 + 30, x1 - x0 - 170, 60), (x0 + 60, y0 + 114, x1 - x0 - 170, 30)


a, ah, asub = brackets()
b, bh, bs = window()
c, chd, cs = curly_glitch()
build("lower-third-terminal-bracket", "Terminal Bracket Lower Third",
      "Code-style lower third with brackets, a prompt chevron and a blinking cursor block. Type your name "
      "on the first row and a handle or topic on the second.",
      ["lower third", "code", "terminal", "tech", "developer", "cursor", "hacker"], [
          V("brackets", "Square Brackets", a, ah, asub, thumb_t=0.56,
            description="Square brackets spring apart from the centre, opening a dark panel with a blinking cursor."),
          V("window", "Terminal Window", b, bh, bs, thumb_t=0.56,
            description="A terminal window with traffic-light buttons unfolds: title bar first, then the body."),
          V("glitch", "Curly Glitch", c, chd, cs, thumb_t=0.56,
            description="Curly braces glitch in with RGB-split ghosts and scanlines; no panel."),
      ])
