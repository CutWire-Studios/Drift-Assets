import random

from _broadcast2 import *

W, H = 1920, 1080
F = 60


def noise(comp, color, opacity, seeds=(1, 2), row=5):
    """Faint flickering static: two oversized noise layers jumping to random offsets every other frame."""
    rng = random.Random(sum(seeds))
    for k, s in enumerate(seeds):
        pos, op = [], []
        for f in range(0, F, 2):
            pos.append((f, [rng.randrange(-150, 150), rng.randrange(-3, 3) * row], HOLD))
            op.append((f, 100 if (f // 2 + k) % 2 == 0 else 0, HOLD))
        pos.append((F, pos[0][1]))
        op.append((F, op[0][1]))
        items = noise_rows(W, H + 40, s, row=row, color=color, density=0.35, min_len=3, max_len=40, n_dash=7)
        comp.layer(f"noise{k}", [group(items, "rows", opacity=opacity, position=(0, -20))], position=Anim(pos),
                   opacity=Anim(op))


def rolling_band(comp, color="#FFFFFF", op=10):
    comp.layer("roll band", [group([rect((W, 180)), gradient_fill(
        [(0, color, 0), (0.5, color, op / 100), (1, color, 0)], (0, -90), (0, 90))], "band")],
        position=keys((0, [W / 2, -100], LINEAR), (F, [W / 2, H + 100])))


def classic():
    """Grey CCTV look: heavy corner brackets, blinking dot, scanlines, faint static and a rolling band."""
    comp = Comp("security-cam-frame", W, H, fps=30, frames=F)
    comp.slot("icon", "#FFFFFF")
    comp.slot("primary", "#FF2B2B")
    M, ARM = 70, 130
    comp.layer("dot", [group([ellipse((30, 30), (M + 40, M + 44)), fill(slot="primary")], "dot")],
               opacity=blink(F, 30, 1))
    comp.layer("brackets", [group(corners(M, M, W - M, H - M, ARM) + [stroke(slot="icon", width=8, cap="butt",
                                                                             join="miter")], "b")])
    comp.layer("brackets shadow", [group(corners(M, M, W - M, H - M, ARM) + [stroke("#000000", width=8, cap="butt",
                                                                                     join="miter", opacity=40)],
                                         "b")], position=(3, 3))
    rolling_band(comp)
    scanlines(comp, W, H, 4, 2, 22)
    noise(comp, "#FFFFFF", 7)
    comp.layer("vignette", [vignette(W, H, 0.45, 0.6)])
    areas = {"camera": (M + 80, M + 14, 520, 60), "timestamp": (W - M - 640, H - M - 84, 600, 60)}
    return comp, areas


def night():
    """Night-vision CCTV: green HUD, IR lamp icon, heavy green vignette and grainy static."""
    comp = Comp("security-cam-frame--night", W, H, fps=30, frames=F)
    comp.slot("icon", "#7CFF9A")
    comp.slot("primary", "#FF3B3B")
    comp.slot("background", "#0B2410")
    M, ARM = 80, 110
    ir = (W - M - 60, M + 44)
    rays = [polyline([(ir[0] + 26 * dx, ir[1] + 26 * dy), (ir[0] + 38 * dx, ir[1] + 38 * dy)])
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (0.7, 0.7), (-0.7, 0.7), (0.7, -0.7), (-0.7, -0.7))]
    comp.layer("ir", [group(rays + [stroke(slot="icon", width=4)], "rays"),
                      group([ellipse((30, 30), ir), fill(slot="icon")], "lamp")],
               opacity=wave_keys(F, [100, 55]))
    comp.layer("dot", [group([ellipse((26, 26), (M + 36, M + 44)), fill(slot="primary")], "dot")],
               opacity=blink(F, 30, 1))
    comp.layer("hud", [group(corners(M, M, W - M, H - M, ARM) + [stroke(slot="icon", width=5, cap="butt",
                                                                        join="miter")], "b"),
                       group([polyline([(W / 2 - 40, H / 2), (W / 2 - 12, H / 2)]),
                              polyline([(W / 2 + 12, H / 2), (W / 2 + 40, H / 2)]),
                              polyline([(W / 2, H / 2 - 40), (W / 2, H / 2 - 12)]),
                              polyline([(W / 2, H / 2 + 12), (W / 2, H / 2 + 40)]),
                              stroke(slot="icon", width=3, cap="butt")], "cross")])
    comp.layer("hud glow", [group(corners(M, M, W - M, H - M, ARM) + [stroke(slot="icon", width=16, opacity=15,
                                                                             cap="butt", join="miter")], "b")])
    rolling_band(comp, "#7CFF9A", 8)
    scanlines(comp, W, H, 4, 2, 26)
    noise(comp, "#9BFFB0", 12, seeds=(4, 5), row=4)
    comp.layer("tint", [group([rect((W, H), (W / 2, H / 2)), gradient_fill(
        [(0, "#0B2410", 0), (0.45, "#0B2410", 0.05), (0.8, "#0B2410", 0.7), (1, "#000000", 0.95)],
        (W / 2, H / 2), (W / 2 + W * 0.58, H / 2), radial=True)], "vig")])
    areas = {"camera": (M + 70, M + 14, 520, 60), "timestamp": (W - M - 640, H - M - 84, 600, 60)}
    return comp, areas


def quad():
    """Four-camera CCTV wall: black dividers split the frame into panes, each with its own blinking dot."""
    comp = Comp("security-cam-frame--quad", W, H, fps=30, frames=F)
    comp.slot("icon", "#FFFFFF")
    comp.slot("primary", "#FF2B2B")
    comp.slot("background", "#0A0A0C")
    g = 14
    pw, ph = (W - g) / 2, (H - g) / 2
    areas = {}
    for i in range(4):
        cx, cy = (i % 2) * (pw + g), (i // 2) * (ph + g)
        d = (cx + 46, cy + 46)
        comp.layer(f"dot{i}", [group([ellipse((20, 20), d), fill(slot="primary")], "dot")],
                   opacity=blink(F, 10 + i * 10, 1))
        comp.layer(f"pane{i}", [group(corners(cx + 24, cy + 24, cx + pw - 24, cy + ph - 24, 60) +
                                      [stroke(slot="icon", width=4, cap="butt", join="miter", opacity=85)], "b")])
        areas[f"camera{i + 1}"] = (round(cx + 72), round(cy + 26), 400, 40)
    rolling_band(comp, op=8)
    scanlines(comp, W, H, 4, 2, 20)
    noise(comp, "#FFFFFF", 6)
    comp.layer("dividers", [box(pw, 0, g, H, slot="background"), box(0, ph, W, g, slot="background")])
    comp.layer("pane vignettes", [group([vignette(pw, ph, 0.5, 0.55)], "v", position=((i % 2) * (pw + g),
                                                                                   (i // 2) * (ph + g)))
                                  for i in range(4)])
    areas["timestamp"] = (round(pw + g + 40), round(H - 80), 560, 50)
    return comp, areas


c1, a1 = classic()
c2, a2 = night()
c3, a3 = quad()
build_asset(CAT, "security-cam-frame", "Security Cam Frame",
            "CCTV surveillance overlay with a transparent centre: corner brackets, blinking record dot, scanlines "
            "and flickering static. Add a camera name and timestamp in the text areas.",
            ["cctv", "security camera", "surveillance", "footage", "scanlines", "overlay", "found footage"], [
    V("classic", "Classic CCTV", c1, "loop", text_area=a1["camera"], text_areas=a1, thumb_t=0.2, bg="59616e",
      description="Grey CCTV look: heavy corner brackets, blinking dot, scanlines, faint static and a rolling band."),
    V("night", "Night Vision", c2, "loop", text_area=a2["camera"], text_areas=a2, thumb_t=0.2, bg="4a5a4c",
      description="Green night-vision HUD with an IR lamp icon, heavy green vignette and grainy static."),
    V("quad", "Quad Split", c3, "loop", text_area=a3["camera1"], text_areas=a3, thumb_t=0.2, bg="59616e",
      description="Four-camera wall: dividers split the frame into panes, each with its own dot and camera label."),
])
