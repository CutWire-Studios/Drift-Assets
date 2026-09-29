from _lt2 import *

W, H = 1100, 240
X, Y, NW, NH = 50, 36, 840, 96    # name bar
TW, TH = 400, 50                  # role tag
TY = Y + NH + 10


def classic():
    comp = base("lower-third-interview-name-role", W, H, 34)
    comp.slot("primary", "#FFFFFF")
    comp.slot("secondary", "#1E2A44")
    comp.slot("accent", "#E63946")
    lay(comp, "tag-accent", [rrect(X, TY, 10, TH), fill(slot="accent")], (X, TY),
        scale=grow_y(12, 24, 118, 128))
    wipe(comp, "tag", [rrect(X, TY, TW, TH), fill(slot="secondary")], (X, TY - 2, TW, TH + 2), 14, 32, 116, 130,
         "top", ein=EXPO_OUT)
    lay(comp, "name-accent", [rrect(X, Y, 10, NH), fill(slot="accent")], (X, Y + NH),
        scale=grow_y(0, 12, 128, 140))
    wipe(comp, "name", [rrect(X, Y, NW, NH), fill(slot="primary")], (X, Y, NW, NH), 4, 26, 122, 140, "left")
    lay(comp, "shadow", [rrect(X + 6, Y + 8, NW, NH), rrect(X + 6, TY + 8, TW, TH), fill("#000000", 20)],
        opacity=fade(22, 32, 116, 124))
    return comp, (X + 40, Y + 16, NW - 70, NH - 32), (X + 34, TY + 10, TW - 56, TH - 20)


def offset():
    comp = base("lower-third-interview-name-role--offset", W, H, 36)
    comp.slot("primary", "#111318")
    comp.slot("secondary", "#FFC53D")
    comp.slot("accent", "#FFFFFF")
    tx = X + NW - TW + 20
    lay(comp, "tag", [para(tx, TY, TW, TH, 0.4), fill(slot="secondary")],
        off=slide(160, 0, 14, 34, 116, 132), opacity=fade(14, 18, 126, 132))
    lay(comp, "edge", [rrect(X, Y + NH - 5, NW, 5), fill(slot="accent")], (X + NW / 2, 0),
        scale=grow_x(10, 30, 120, 134, INOUT, INOUT))
    comp.layer("name", [rect_grow(X, Y, NW, NH, 6, 0, 24, 122, 142, "centre", start=20), fill(slot="primary")],
               opacity=fade(0, 4, 136, 142))
    return comp, (X + 36, Y + 16, NW - 72, NH - 36), (tx + 40, TY + 10, TW - 70, TH - 20)


def minimal():
    comp = base("lower-third-interview-name-role--minimal", W, H, 40)
    comp.slot("outline", "#FFFFFF")
    comp.slot("secondary", "#00B4D8")
    comp.slot("icon", "#FFFFFF")
    ly = Y + NH + 4
    lay(comp, "dot", [ellipse((16, 16), (X + 8, ly + 2)), fill(slot="secondary")], (X + 8, ly + 2),
        scale=pop(0, 12, 130, 142))
    comp.layer("line", [poly([(X + 28, ly + 2), (X + NW, ly + 2)], False), stroke(slot="outline", width=4),
                        draw_rev(4, 30, 120, 140)])
    tag_y = ly + 18
    comp.layer("tag", [rect_grow(X + 28, tag_y, TW - 40, TH - 6, (TH - 6) / 2, 18, 38, 116, 132, "left", start=TH - 6),
                       fill(slot="secondary")], opacity=fade(18, 22, 128, 132))
    return comp, (X + 28, Y + 20, NW - 28, NH - 28), (X + 50, tag_y + 8, TW - 84, TH - 22)


c, ch, cs = classic()
o, oh, os_ = offset()
m, mh, ms = minimal()
build("lower-third-interview-name-role", "Interview Name and Role",
      "Interview lower third: a name bar with a smaller role tag underneath. Type the person's name in the "
      "bar and their job title or role in the tag.",
      ["lower third", "interview", "name", "role", "title", "documentary", "speaker"], [
          V("classic", "Classic", c, ch, cs,
            description="White name bar wipes in from the left; the role tag drops down beneath it."),
          V("offset", "Offset Tag", o, oh, os_, bg="e8e8ee",
            description="Dark bar opens from the centre; a slanted role tag slides in under its right end."),
          V("minimal", "Minimal Underline", m, mh, ms,
            description="No bar: an underline draws beneath the name and a rounded role pill slides out."),
      ])
