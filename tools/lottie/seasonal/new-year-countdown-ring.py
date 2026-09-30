"""New Year countdown ring: a ring fills up and bursts into fireworks on completion (seamless loop).
The number is not drawn: put it in the text area inside the ring."""

from _common import *

T = 90
W = H = 640
C = (W / 2, H / 2)
R = 200
FILL_END = 60
TEXT = (C[0] - 140, C[1] - 105, 280, 210)
GOLD, CHAMPAGNE, NIGHT = "#F5C451", "#FFF1C1", "#1B2340"


def firework(comp, name, center, t0, count, r0, r1, colors, width=5, dur=18, dots=True, slot=None):
    """Streaks shooting out from a centre plus trailing sparkle dots, then fading."""
    items = []
    for i in range(count):
        a = math.radians(360 * i / count + (0 if i % 2 else 360 / count / 2 * 0))
        rr1 = r1 * (1 if i % 2 == 0 else 0.78)
        p0, p1 = (r0 * math.cos(a), r0 * math.sin(a)), (rr1 * math.cos(a), rr1 * math.sin(a))
        col = colors[i % len(colors)]
        items.append(group([polyline([p0, p1]),
                            trim(start=anim([(t0 + 3, 0, EASE_OUT), (t0 + dur, 100)]),
                                 end=anim([(t0, 0, SNAP_OUT), (t0 + dur * 0.6, 100)])),
                            stroke(col, width, slot=slot if i % len(colors) == 0 else None)], f"ray{i}"))
        if dots:
            d = rr1 * 1.1
            items.append(group([ellipse((width * 1.3, width * 1.3)), fill(col)], f"dot{i}",
                               position=anim([(t0 + 4, [p1[0] * 0.8, p1[1] * 0.8], DECEL),
                                              (t0 + dur + 6, [d * math.cos(a), d * math.sin(a) + 18])]),
                               scale=anim([(t0 + 4, [0, 0], EASE_OUT), (t0 + 8, [100, 100], EASE_IN),
                                           (t0 + dur + 6, [0, 0])])))
    comp.layer(name, items, position=center, ip=t0, op=min(T, t0 + dur + 7))


def ring_path(r=R):
    return group([ellipse((2 * r, 2 * r))], "e", rotation=-90)


def progress(t):
    return 100 * ease_in_out(t / FILL_END) if t < FILL_END else 100


def fade_out():
    return anim([(0, 100, HOLD), (FILL_END + 16, 100, EASE_IN), (T - 2, 0, HOLD), (T, 100)])


def gold():
    comp = Comp("new-year-countdown-ring", W, H, frames=T)
    comp.slot("primary", GOLD)
    comp.slot("secondary", CHAMPAGNE)
    comp.slot("background", NIGHT)
    cols = [GOLD, CHAMPAGNE, "#FFFFFF"]
    for j, (a, d, t) in enumerate(((-50, 300, 0), (40, 290, 5), (160, 285, 9), (-140, 295, 3), (100, 300, 12))):
        p = (C[0] + d * math.cos(math.radians(a)) * 0.95, C[1] + d * math.sin(math.radians(a)) * 0.95)
        firework(comp, f"fw{j}", p, FILL_END + t, 12, 8, 70, cols, 4, slot="primary")
    # completion flash ring
    comp.layer("flash", [ring_path(), stroke(CHAMPAGNE, 10, slot="secondary")], position=C, ip=FILL_END,
               op=FILL_END + 13, scale=anim([(FILL_END, [100, 100], DECEL), (FILL_END + 13, [135, 135])]),
               opacity=anim([(FILL_END, 90, EASE_IN), (FILL_END + 13, 0)]))
    # head dot riding the tip
    comp.layer("tip", [group([ellipse((22, 22)), fill(WHITE)], "core"), glow(40, "#FFE8A0", 100)],
               position=looped(lambda t: (C[0] + R * math.sin(TAU * progress(t) / 100),
                                          C[1] - R * math.cos(TAU * progress(t) / 100)), T, 1),
               opacity=anim([(0, 100, HOLD), (FILL_END, 0, HOLD), (T, 100)]))
    comp.layer("progress", [ring_path(), trim(end=looped(progress, T, 1)),
                            stroke(GOLD, 16, slot="primary")], position=C, opacity=fade_out())
    ticks = []
    for i in range(60):
        a = math.radians(i * 6)
        r0, r1 = (R + 24, R + 40) if i % 5 == 0 else (R + 27, R + 34)
        ticks.append(polyline([(r0 * math.sin(a), -r0 * math.cos(a)), (r1 * math.sin(a), -r1 * math.cos(a))]))
    comp.layer("ticks", ticks + [stroke(GOLD, 3, 70, slot="primary")], position=C)
    comp.layer("track", [ring_path(), stroke(GOLD, 16, 18, slot="primary")], position=C)
    comp.layer("inner-rim", [ring_path(R - 22), stroke(GOLD, 2, 50, slot="primary")], position=C)
    comp.layer("disc", [ellipse((2 * R - 44, 2 * R - 44)), fill(NIGHT, 88, slot="background")], position=C)
    return comp


def neon():
    comp = Comp("new-year-countdown-ring--neon", W, H, frames=T)
    comp.slot("primary", "#35E0FF")
    comp.slot("secondary", "#FF3FD1")
    cols = ["#35E0FF", "#FF3FD1", "#FFE14A", "#7CFF6B"]
    for j, (a, d, t) in enumerate(((-60, 290, 0), (20, 300, 6), (120, 290, 3), (200, 300, 10), (-130, 280, 14))):
        p = (C[0] + d * math.cos(math.radians(a)) * 0.95, C[1] + d * math.sin(math.radians(a)) * 0.95)
        firework(comp, f"fw{j}", p, FILL_END + t, 14, 6, 80, cols[j % 4:] + cols[:j % 4], 4.5)
    for name, r, col, sid, direction in (("outer", R, "#35E0FF", "primary", 1), ("inner", R - 30, "#FF3FD1",
                                                                                "secondary", -1)):
        shape = group([ellipse((2 * r, 2 * r))], "e", rotation=-90, scale=(direction * 100, 100))
        tr = trim(end=looped(progress, T, 1))
        comp.layer(name + "-core", [shape, tr, stroke(WHITE, 4, 90)], position=C, opacity=fade_out())
        comp.layer(name, [shape, tr, stroke(col, 10, slot=sid)], position=C, opacity=fade_out())
        comp.layer(name + "-glow", [shape, tr, stroke(col, 30, 25, slot=sid)], position=C, opacity=fade_out())
        comp.layer(name + "-track", [shape, stroke(col, 3, 30, slot=sid)], position=C)
    comp.layer("pulse", [ring_path(R + 20), stroke("#35E0FF", 8, slot="primary")], position=C, ip=FILL_END,
               op=FILL_END + 13, scale=anim([(FILL_END, [100, 100], DECEL), (FILL_END + 13, [128, 128])]),
               opacity=anim([(FILL_END, 100, EASE_IN), (FILL_END + 13, 0)]))
    return comp


def segments():
    comp = Comp("new-year-countdown-ring--segments", W, H, frames=T)
    comp.slot("primary", "#FFFFFF")
    comp.slot("secondary", "#FF5A7A")
    comp.slot("accent", "#FFC93C")
    n = 12
    seg = 360 / n
    for i in range(n):
        t_on = FILL_END * i / n + 2
        a0, a1 = -90 + i * seg + 3, -90 + (i + 1) * seg - 3
        arc = S(arc_d(R, a0, a1))
        mid = math.radians((a0 + a1) / 2)
        comp.layer(f"seg{i}", [group(arc + [stroke(WHITE, 26, slot="primary", cap="butt")], "on")], ip=0,
                   position=C,
                   opacity=anim([(0, 0, HOLD), (t_on, 0, EASE_OUT), (t_on + 3, 100, HOLD), (FILL_END + 16, 100, EASE_IN),
                                 (T - 2, 0, HOLD), (T, 0)]),
                   scale=anim([(0, [100, 100], HOLD), (t_on, [112, 112], SNAP_OUT), (t_on + 8, [100, 100])]))
        comp.layer(f"off{i}", [group(arc + [stroke(WHITE, 26, 16, slot="primary", cap="butt")], "off")], position=C)
    # confetti burst on completion
    r = rng(12)
    cols = [("secondary", "#FF5A7A"), ("accent", "#FFC93C"), ("primary", "#FFFFFF")]
    for i in range(34):
        a = r.uniform(0, TAU)
        sp = r.uniform(170, 300)
        sid, col = cols[i % 3]
        t0 = FILL_END + r.uniform(0, 3)
        life = r.uniform(22, 28)
        shape = [rect((12, 7) if i % 2 else (8, 8), roundness=2 if i % 2 else 4), fill(col, slot=sid)]
        spin = r.uniform(-500, 500)

        def fn(u, a=a, sp=sp, life=life, spin=spin):
            k = u / life
            d = sp * ease_out(k, 2.5) + 60
            return {"position": (C[0] + (R * 0.9 + d * 0.6) * math.cos(a) * 1.0,
                                 C[1] + (R * 0.9 + d * 0.6) * math.sin(a) + 90 * k * k),
                    "rotation": spin * k, "opacity": 100 * smooth((1 - k) / 0.3),
                    "scale": [100 * (1 - 0.6 * abs(math.cos(k * 9))), 100]}
        particle(comp, f"confetti{i}", shape, t0, life, T, fn, step=2, wrap=False)
    comp.layer("flash", [ellipse((2 * R + 40, 2 * R + 40)), stroke(WHITE, 6, slot="primary")], position=C,
               ip=FILL_END, op=FILL_END + 12, scale=anim([(FILL_END, [96, 96], DECEL), (FILL_END + 12, [120, 120])]),
               opacity=anim([(FILL_END, 100, EASE_IN), (FILL_END + 12, 0)]))
    return comp


build("new-year-countdown-ring", "New Year Countdown Ring",
      "A countdown ring that fills up and bursts into fireworks when it completes; loop it once per number. "
      "Put the countdown number in the text area inside the ring.",
      ["new year", "countdown", "fireworks", "ring", "timer", "celebration", "nye"], [
          Variant("gold", "Gold Clock", gold(), "loop", thumb_t=0.84, text_area=TEXT,
                  description="Elegant gold ring with clock ticks on a night disc and golden firework bursts."),
          Variant("neon", "Neon", neon(), "loop", thumb_t=0.84, text_area=TEXT,
                  description="Twin neon rings filling in opposite directions, with multicolour fireworks."),
          Variant("segments", "Segments", segments(), "loop", thumb_t=0.71, text_area=TEXT,
                  description="Twelve segments light up one by one, then a confetti burst on completion."),
      ])
