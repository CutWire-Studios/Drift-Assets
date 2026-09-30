from _broadcast2 import *

F = 120
N = 4
ARRIVE = [4, 26, 48, 70]
MOVE = 12


def lift(k, step):
    """Offset keys for bubble k: it arrives in the bottom slot and moves up one slot per later arrival."""
    ks = [(ARRIVE[k], [0, 0], HOLD)]
    for j in range(k + 1, N):
        ks[-1] = (ks[-1][0], ks[-1][1], EXPO_OUT)
        ks.append((ARRIVE[j], ks[-1][1], EXPO_OUT))
        ks.append((ARRIVE[j] + MOVE, [0, -(j - k) * step], HOLD))
    # collapse duplicate keys at the same frame
    out = []
    for t, v, e in ks:
        if out and out[-1][0] == t:
            out[-1] = (t, v, e)
        else:
            out.append((t, v, e))
    return Anim(out) if len(out) > 1 else Anim(out + [(F, out[0][1])])


def modern():
    """Livestream chat: dark rounded rows with coloured avatars pop in at the bottom and push up."""
    W, H = 760, 860
    comp = Comp("chat-bubble-stream", W, H, fps=30, frames=F)
    comp.slot("background", "#16171D")
    comp.slot("primary", "#FF4D6D")
    comp.slot("secondary", "#3DB2FF")
    comp.slot("accent", "#FFC53D")
    av_slots = ("primary", "secondary", "accent", "primary")
    bh, gap = 170, 26
    step = bh + gap
    x0, bw = 40, W - 80
    y0 = H - 40 - bh  # bottom slot top
    areas = {}
    for k in range(N):
        t = ARRIVE[k]
        pivot = (x0, y0 + bh)
        av = (x0 + 70, y0 + bh / 2)
        shapes = [
            group([ellipse((84, 84), av), fill(slot=av_slots[k])], "avatar"),
            group([ellipse((96, 96), av), fill("#FFFFFF", 14)], "avatar ring"),
            group([rect_tl(x0, y0, bw, bh, 34), fill(slot="background", opacity=88)], "row"),
            group([rect_tl(x0, y0 + 8, bw, bh, 34), fill("#000000", 22)], "shadow"),
        ]
        lay(comp, f"bubble{k}", shapes, pivot, lift(k, step), ip=t,
            scale=keys((t, [40, 40], SPRING), (t + 14, [100, 100])), opacity=fade(t, t + 5))
        fy = y0 - (N - 1 - k) * step
        areas[f"name{k + 1}"] = (x0 + 136, fy + 26, bw - 176, 40)
        areas[f"message{k + 1}"] = (x0 + 136, fy + 72, bw - 176, 72)
    return comp, areas


def messenger():
    """Messenger-style bubbles with tails, alternating left and right, popping from their tail corner."""
    W, H = 760, 860
    comp = Comp("chat-bubble-stream--messenger", W, H, fps=30, frames=F)
    comp.slot("primary", "#1F8BFF")
    comp.slot("secondary", "#E9E9EE")
    bh, gap = 150, 40
    step = bh + gap
    bw = 520
    y0 = H - 40 - bh
    areas = {}
    for k in range(N):
        t = ARRIVE[k]
        right = k % 2 == 1
        x = W - 40 - bw if right else 40
        tail_x = x + bw if right else x
        s = 1 if right else -1
        tail = path(bezier([(tail_x - s * 30, y0 + bh - 44), (tail_x + s * 12, y0 + bh + 2),
                            (tail_x - s * 46, y0 + bh - 2)],
                           [(0, 0), (-s * 8, -2), (s * 14, 0)], [(s * 4, 26), (-s * 18, 2), (0, 0)]))
        slot = "primary" if right else "secondary"
        shapes = [group([rect_tl(x, y0, bw, bh, 44), fill(slot=slot)], "bubble"), group([tail, fill(slot=slot)], "tail"),
                  group([rect_tl(x, y0 + 6, bw, bh, 44), fill("#000000", 16)], "shadow")]
        pivot = (tail_x, y0 + bh)
        lay(comp, f"bubble{k}", shapes, pivot, lift(k, step), ip=t,
            scale=keys((t, [0, 0], SPRING), (t + 15, [100, 100])))
        fy = y0 - (N - 1 - k) * step
        areas[f"message{k + 1}"] = (x + 40, fy + 30, bw - 80, bh - 60)
    return comp, areas


def gamer():
    """Gaming stream chat: slim dark rows slide in from the left with a neon name stripe."""
    W, H = 760, 700
    comp = Comp("chat-bubble-stream--gamer", W, H, fps=30, frames=F)
    comp.slot("background", "#0D0B14")
    comp.slot("primary", "#9B5CFF")
    comp.slot("accent", "#3DFFB5")
    bh, gap = 124, 22
    step = bh + gap
    x0, bw = 40, W - 80
    y0 = H - 40 - bh
    areas = {}
    for k in range(N):
        t = ARRIVE[k]
        slot = "primary" if k % 2 == 0 else "accent"
        off = lift(k, step)
        off = Anim([(t - 1, [-120, 0], EXPO_OUT), (t + 12, [0, 0], off.keys[0][2])] + off.keys[1:]) \
            if len(off.keys) > 1 and off.keys[1][0] > t + 12 else Anim([(t - 1, [-120, 0], EXPO_OUT), (t + 12, [0, 0])])
        stripe = rect_tl(x0, y0, 12, bh, 0)
        shapes = glow_strokes([polyline([(x0 + 6, y0 + 14), (x0 + 6, y0 + bh - 14)])], slot=slot, width=6,
                              widths=(22, 12), ops=(12, 24)) + [
            group([rect_tl(x0 + 34, y0 + 22, 30, 30, 6), fill(slot=slot)], "badge"),
            group([rect_tl(x0, y0, bw, bh, 10), stroke(slot=slot, width=2, opacity=40)], "edge"),
            group([rect_tl(x0, y0, bw, bh, 10), fill(slot="background", opacity=82)], "row"),
        ]
        lay(comp, f"row{k}", shapes, (x0, y0), off, ip=t - 1, opacity=fade(t - 1, t + 5))
        fy = y0 - (N - 1 - k) * step
        areas[f"name{k + 1}"] = (x0 + 78, fy + 18, bw - 110, 38)
        areas[f"message{k + 1}"] = (x0 + 34, fy + 62, bw - 66, 48)
        del stripe
    return comp, areas


m, ma = modern()
s, sa = messenger()
g, ga = gamer()
build_asset(CAT, "chat-bubble-stream", "Chat Bubble Stream",
            "Live chat messages that pop in at the bottom and push the earlier ones up, then hold. Every "
            "bubble has its own text areas (name1-4 and message1-4, oldest first).",
            ["chat", "live chat", "comments", "messages", "stream", "bubbles", "text", "social"], [
    V("modern", "Live Chat", m, "intro-hold", text_area=ma["message4"], text_areas=ma, thumb_t=0.95,
            bg="6a7087", description="Dark rounded rows with coloured avatar circles pop in and push up."),
    V("messenger", "Messenger", s, "intro-hold", text_area=sa["message4"], text_areas=sa, thumb_t=0.95,
            description="Tailed message bubbles alternating left and right, popping from their tail corner."),
    V("gamer", "Gamer Chat", g, "intro-hold", text_area=ga["message4"], text_areas=ga, thumb_t=0.95,
            bg="6a7087", description="Slim dark rows with a glowing name stripe slide in from the left, gaming-stream style."),
])
