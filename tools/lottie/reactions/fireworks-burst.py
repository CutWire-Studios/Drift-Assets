"""Fireworks: three shells launch, burst and fade in turn, overlapping so the sky is never empty
(loop). Styles: streak trails, glittering sparks, or cartoon doodle bursts."""

from _reactions2 import *

T = 90
W, H = 500, 500
COLS = [("primary", "#FF4D6D"), ("secondary", "#FFC93C"), ("accent", "#4DD8FF")]
# (launch frame, burst x, burst y, radius, colour index)
SHELLS = [(0, 250, 190, 170, 0), (30, 150, 250, 130, 1), (60, 350, 230, 140, 2)]
RISE = 12


def make(style):
    comp = Comp("fireworks-burst", W, H, frames=T)
    for sid, c in COLS:
        comp.slot(sid, c)
    if style == "doodle":
        comp.slot("outline", "#161616")

    for s_i, (t00, bx, by, rad, ci) in enumerate(SHELLS):
      for t0 in [t00] + ([t00 - T] if t00 + RISE + 40 > T else []):  # wrap the last shell
          sid, col = COLS[ci]
          tb = t0 + RISE
          # rocket trail rising from the bottom
          trail = [path(bezier([(bx - 20, H - 10), (bx, by + 16)], closed=False)),
                   trim(start=anim([(t0 + 4, 0, EASE_IN), (tb + 3, 100)]),
                        end=anim([(t0, 0, EASE_OUT), (tb, 100)])),
                   stroke(col, 5 if style != "doodle" else 7, slot=sid)]
          if style == "doodle":
              trail.append(stroke("#161616", 13, slot="outline"))
          comp.layer(f"trail{s_i}", [group(trail)], ip=t0, op=tb + 4)

          # flash at the burst point
          comp.layer(f"flash{s_i}", [group([ellipse((70, 70)),
                                            gradient_fill([(0, "#FFFFFF", 1), (0.4, col, 0.7), (1, col, 0)],
                                                          (0, 0), (35, 0), radial=True)])]
                     if style != "doodle" else
                     [group(S(star_d(40, 0.4)) + [fill("#FFFFFF"), stroke("#161616", 6, slot="outline")])],
                     position=(bx, by), ip=tb, op=tb + 8,
                     scale=anim([(tb, [30, 30], SNAP_OUT), (tb + 3, [130, 130], EASE_IN), (tb + 8, [0, 0])]))

          n = 14 if style != "glitter" else 30
          life = 40
          for k in range(n):
              a = TAU * k / n + (0.1 * s_i)
              ca, sa = math.cos(a), math.sin(a)
              if style == "trails":
                  # streak drawn outward, tail catching up, drooping slightly
                  p0 = (bx + ca * rad * 0.15, by + sa * rad * 0.15)
                  pm = (bx + ca * rad * 0.7, by + sa * rad * 0.7 + 6)
                  p1 = (bx + ca * rad, by + sa * rad + 22)
                  comp.layer(f"ray{s_i}_{k}", [group([path(smooth_open([p0, pm, p1])),
                                                       trim(start=anim([(tb + 3, 0, EASE_IN), (tb + 26, 100)]),
                                                            end=anim([(tb, 0, SNAP_OUT), (tb + 14, 100)])),
                                                       stroke(col if k % 2 == 0 else "#FFFFFF", 7, slot=sid if k % 2 == 0 else None)])],
                             ip=tb, op=tb + 27)
                  # sparkle at the tip that twinkles out
                  comp.layer(f"tip{s_i}_{k}", [group(S(sparkle_d(10)) + [fill("#FFFFFF")])],
                             position=anim([(tb + 12, list(pm)), (tb + 30, [p1[0], p1[1] + 14])]),
                             ip=tb + 12, op=tb + 32,
                             scale=anim([(tb + 12, [120, 120]), (tb + 20, [60, 60]), (tb + 26, [110, 110]), (tb + 32, [0, 0])]))
              elif style == "glitter":
                  sp = rad / 8.5 * (0.55 + 0.45 * ((k * 7) % 5) / 4) * (0.6 if k % 3 == 0 else 1)

                  def fn(u, ca=ca, sa=sa, sp=sp, k=k):
                      f = (1 - 0.88 ** u) / 0.12
                      x, y = bx + ca * sp * f, by + sa * sp * f + 0.09 * u * u
                      tw = 0.65 + 0.35 * math.cos(u * 1.3 + k)
                      s = 100 * (1 - u / life * 0.6) * tw
                      return {"position": (x, y), "scale": (s, s),
                              "opacity": 100 * (1 - smooth((u / life - 0.55) / 0.45))}
                  particle(comp, f"g{s_i}_{k}", [
                      group([ellipse((10, 10)), fill("#FFFFFF")]),
                      group([ellipse((18, 18)), fill(col, slot=sid)]),
                      group([ellipse((56, 56)), gradient_fill([(0, col, 0.7), (1, col, 0)], (0, 0), (28, 0),
                                                              radial=True)])],
                           tb, life, T, fn, step=2, wrap=False)
              else:  # doodle: chunky capsule rays with ink outline, popping outward
                  if k % 2:
                      continue
                  r0, r1 = rad * 0.35, rad * 0.8
                  ray = capsule((ca * r0, sa * r0), (ca * r1, sa * r1), 9)
                  comp.layer(f"d{s_i}_{k}", [group(ray + [stroke("#161616", 7, slot="outline"), fill(col, slot=sid)])],
                             position=(bx, by), ip=tb, op=tb + 30,
                             scale=anim([(tb, [20, 20], SNAP_OUT), (tb + 8, [100, 100], EASE_IN_OUT), (tb + 30, [140, 140])]),
                             opacity=anim([(tb, 100), (tb + 20, 100), (tb + 30, 0)]))
                  dot = (ca * rad * 1.02, sa * rad * 1.02)
                  comp.layer(f"dd{s_i}_{k}", [group([ellipse((18, 18), dot), stroke("#161616", 6, slot="outline"),
                                                     fill("#FFFFFF")])],
                             position=(bx, by), ip=tb + 4, op=tb + 30,
                             scale=anim([(tb + 4, [40, 40], SNAP_OUT), (tb + 14, [100, 100], EASE_IN_OUT), (tb + 30, [125, 125])]),
                             opacity=anim([(tb + 4, 100), (tb + 22, 100), (tb + 30, 0)]))
          if style == "doodle":
              ring = [group([ellipse((rad * 1.1, rad * 1.1)), stroke(col, 6, slot=sid), stroke("#161616", 14, slot="outline")])]
              comp.layer(f"ring{s_i}", ring, position=(bx, by), ip=tb, op=tb + 22,
                         scale=anim([(tb, [10, 10], SNAP_OUT), (tb + 20, [110, 110])]),
                         opacity=anim([(tb, 100), (tb + 12, 100), (tb + 22, 0)]))
    return comp


build3("fireworks-burst", "Fireworks Burst",
       "Three fireworks launch, burst and fade in turn so the sky is never empty; for celebrations, "
       "launches and new-year moments. Seamless loop.",
       ["fireworks", "celebration", "party", "new year", "burst", "congrats", "reaction"], make, [
           ("trails", "Streak Trails", "loop", 0.3, "Classic streaking trails with twinkling tips."),
           ("glitter", "Glitter", "loop", 0.3, "Glowing spark dots that spray out and fall with gravity."),
           ("doodle", "Doodle", "loop", 0.3, "Cartoon bursts with chunky ink-outlined rays and rings."),
       ])
