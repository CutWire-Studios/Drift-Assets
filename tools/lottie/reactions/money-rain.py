"""Money rain: banknotes flutter and flip down while gold coins spin past (loop)."""

from _reactions2 import *

T = 90
W, H = 460, 560
NOTE, NOTE_DARK, COIN, COIN_DARK = "#4CC38A", "#1F7A4E", "#FFC93C", "#D08A12"

# a stylised currency emblem drawn from shapes (an S-curve with a bar), not a font glyph
EMBLEM_D = "M 9 -10 C 6 -15 -8 -16 -9 -8 C -10 0 9 0 9 8 C 9 16 -6 16 -10 10"


def note(st):
    top = []
    if st.glossy:
        top.append(group([rect((96, 12), (0, -18), roundness=6), fill(WHITE, 30)], name="shine"))
    top += [
        group(S(EMBLEM_D) + [path(bezier([(0, -20), (0, 20)], closed=False)),
                             stroke(NOTE_DARK, 4.5)], name="emblem"),
        group([ellipse((42, 42)), stroke(NOTE_DARK, 3.5), fill("#BDF0D2")], name="seal"),
        group([ellipse((14, 14), (-44, 0)), ellipse((14, 14), (44, 0)), fill(NOTE_DARK, 60)], name="dots"),
        group([rect((112, 50), roundness=6), stroke(NOTE_DARK, 3, 80)], name="inner"),
    ]
    return top + st.body([rect((128, 66), roundness=8)], NOTE, "primary", (-64, -33, 64, 33),
                         spec=False, gloss=0.6)


def coin(st):
    top = []
    if st.glossy:
        top.append(group([ellipse((16, 26)), fill(WHITE, 60)], position=(-14, -12), rotation=30))
    top += [group(S(star_d(13, 0.5)) + [fill(COIN_DARK)], name="star"),
            group([ellipse((42, 42)), stroke(COIN_DARK, 4)], name="rim")]
    return top + st.body([ellipse((56, 56))], COIN, "secondary", (-28, -28, 28, 28), spec=False)


def make(kind):
    st = Style(kind)
    comp = Comp("money-rain", W, H, frames=T)
    comp.slot("primary", NOTE)
    comp.slot("secondary", COIN)
    if not st.glossy:
        comp.slot("outline", WHITE if st.flat else st.ink)

    rain(comp, "note", 9, T, W, H, lambda i: note(st), seed=31, life=(0.8, 1.0), size=(0.75, 1.0),
         sway=34, spin=140, flip=0.0, tumble=0.75, margin=70, fade=0.12)
    rain(comp, "coin", 7, T, W, H, lambda i: coin(st), seed=17, life=(0.6, 0.75), size=(0.8, 1.1),
         sway=10, spin=0, flip=0.9, margin=50, fade=0.1)
    return comp


build3("money-rain", "Money Rain",
       "Banknotes fluttering and flipping down with spinning gold coins; for wins, sales, payday "
       "and 'make it rain' moments. Seamless loop.",
       ["money", "cash", "rain", "rich", "payday", "coins", "reaction"], make, [
           ("glossy", "Glossy", "loop", 0.5, "Shaded notes and shiny coins with highlights."),
           ("flat", "Flat Sticker", "loop", 0.5, "Flat colours with white die-cut borders."),
           ("outline", "Bold Outline", "loop", 0.5, "Cartoon line art with bold black outlines."),
       ])
