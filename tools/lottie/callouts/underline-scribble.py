from _common import Brush, Comp, cubic_pts, emit, finish, pressure

W, H = 800, 160
comp = Comp("underline-scribble", W, H, fps=30, frames=30)
comp.slot("primary", "#FF2D2D")

base = 19
# long confident stroke left to right, then a quicker, shorter return stroke underneath
first = [(40, 46), (52, 62), (72, 70)] + cubic_pts((72, 70), (280, 86), (540, 70), (764, 46), 60)[1:]
second = cubic_pts((724, 72), (560, 98), (330, 112), (104, 112), 50)

strokes = [
    Brush(first, 1, 13, pressure(base, taper_in=0.04, taper_out=0.14, min_in=0.5, min_out=0.2,
                                 wobble=0.14, seed=31),
          max_width=base * 1.2, easing=(0.5, 0.0, 0.35, 1.0), slot="primary", name="line-a"),
    Brush(second, 13, 22, pressure(base * 0.9, taper_in=0.06, taper_out=0.3, min_in=0.55,
                                   min_out=0.1, wobble=0.14, seed=32),
          max_width=base * 1.1, easing=(0.4, 0.0, 0.3, 1.0), smooth=False, slot="primary",
          name="line-b"),
]
emit(comp, strokes)

finish(comp, "underline-scribble", "Underline Scribble",
       "Quick hand-drawn double underline: a long marker stroke and a shorter return stroke.",
       ["underline", "scribble", "marker", "emphasis", "hand-drawn", "text"], "intro-hold")
