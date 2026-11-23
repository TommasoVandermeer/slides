"""ORCA, SFM e HSFM sullo stesso circular crossing, con andata e ritorno (slide 9).

Disegna le traiettorie simulate da hmm_simulate.py (repo JORCA, JSFM, JHSFM): nessuna traiettoria è inventata.
Parte 1: scena intera a 2x. Parte 2: zoom sulla svolta di 180 gradi di una persona, a 1x, ogni pannello
centrato sull'istante della sua svolta.

Render (dalla radice della repo):
    .venv-manim/bin/manim -qh --fps 30 26-11-2026-phd/animations/hmm.py HumanMotionModels --media_dir /tmp/manim
"""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "scripts"))
from manim_style import *  # noqa: E402,F403
from manim import *  # noqa: E402,F403

# formato più largo del 16:9 (circa 16:7): tre pannelli affiancati, meno spazio vuoto sopra e sotto nella slide
config.frame_height = 6.4
config.pixel_height = 864
config.pixel_width = 1920

D = np.load(HERE / "data" / "hmm_circular_crossing.npz")
DT = float(D["dt"])
R = float(D["radius"])
MODELS = [("orca", "ORCA", "velocity-based"), ("sfm", "SFM", "force-based"), ("hsfm", "HSFM", "force-based + body orientation")]
FOCUS = 5            # persona evidenziata
T_FULL = 14.0        # secondi simulati nella parte 1 (andata, svolta, inizio del ritorno)
TRAIL = 2.0          # coda delle persone non evidenziate (s)
ZOOM_HALF = 1.7      # metà lato della finestra di zoom (m)
ZOOM_T = 1.8         # secondi prima e dopo la svolta
GRAY = "#9AA0A6"


def at(arr, t):
    """Interpolazione lineare nel tempo di un array (frame, persone, ...)."""
    x = np.clip(t / DT, 0, len(arr) - 1)
    i = int(np.floor(x)); j = min(i + 1, len(arr) - 1); f = x - i
    return (1 - f) * arr[i] + f * arr[j]


def turn_time(m):
    """Istante della svolta: minima distanza dall'obiettivo della persona evidenziata."""
    p = D[f"{m}_pos"][:, FOCUS]
    return float(np.argmin(np.linalg.norm(p - D["goal"][FOCUS], axis=1)) * DT)


class Panel:
    def __init__(self, scene, model, center, side, window_center, half):
        self.m, self.scene = model, scene
        self.pos, self.theta = D[f"{model}_pos"], D[f"{model}_theta"]
        self.center, self.k = np.array(center), side / (2 * half)  # unità di scena per metro
        self.wc, self.half = np.array(window_center), half

    def inside(self, xy):
        """Dentro la finestra del pannello (con un margine pari al raggio)."""
        return np.all(np.abs(np.asarray(xy) - self.wc) <= self.half - R, axis=-1)

    def P(self, xy):
        d = (np.asarray(xy) - self.wc) * self.k
        return self.center + np.array([d[0], d[1], 0.0])

    def people(self, t, trail_all, t0=0.0):
        g = VGroup()
        k0 = int(max(t0, t - trail_all) / DT) if trail_all else int(t0 / DT)
        k1 = int(np.clip(t / DT, 0, len(self.pos) - 1))
        for h in range(self.pos.shape[1]):
            focus = h == FOCUS
            kk0 = int(t0 / DT) if focus else k0
            if k1 > kk0 + 1:
                xy = np.vstack([self.pos[kk0:k1 + 1, h], at(self.pos, t)[h][None]])
                xy = xy[self.inside(xy)]  # solo la parte dentro la finestra
                if len(xy) > 1:
                    g.add(VMobject(stroke_color=C_HM if focus else GRAY, stroke_width=4 if focus else 2,
                                   stroke_opacity=1 if focus else 0.6).set_points_as_corners([self.P(p) for p in xy]))
            if not self.inside(at(self.pos, t)[h]):
                continue
            c = self.P(at(self.pos, t)[h])
            g.add(Circle(radius=R * self.k, color=C_HM if focus else GRAY, fill_opacity=0.9 if focus else 0.55,
                         stroke_width=0).move_to(c))
            if self.m == "hsfm":  # orientamento del corpo
                th = at(self.theta, t)[h]
                g.add(Line(c, c + R * self.k * 1.6 * np.array([np.cos(th), np.sin(th), 0]), color=INK, stroke_width=3))
        return g


class HumanMotionModels(Scene):
    def construct(self):
        side, gap = 4.15, 0.45
        xs = [-(side + gap), 0, side + gap]
        y0 = -0.1
        frames = VGroup(*[Square(side, stroke_color=MUTED, stroke_width=1.5).move_to([x, y0, 0]) for x in xs])
        names = VGroup(*[Text(n, font=FONT, color=INK, font_size=34, weight=BOLD).next_to(f, UP, buff=0.42)
                         for f, (_, n, _) in zip(frames, MODELS)])
        tags = VGroup(*[Text(s, font=FONT, color=MUTED, font_size=22).next_to(f, UP, buff=0.12)
                        for f, (_, _, s) in zip(frames, MODELS)])
        lim = np.abs(D["start"]).max() + 0.6

        def title(text):
            return Text(text, font=FONT, color=INK, font_size=30).to_edge(DOWN, buff=0.3)

        # --- parte 1: scena intera, 2x
        t = ValueTracker(0.0)
        panels = [Panel(self, m, [x, y0, 0], side, (0, 0), lim) for (m, _, _), x in zip(MODELS, xs)]
        goals = VGroup(*[Star(n=5, outer_radius=0.09, color=C_HM, fill_opacity=1).move_to(p.P(D["goal"][FOCUS]))
                         for p in panels])
        live = always_redraw(lambda: VGroup(*[p.people(t.get_value(), TRAIL) for p in panels]))
        cap = title("Same start and goals · everyone walks across and back · 2×")
        self.add(frames, names, tags, goals, live, cap)
        self.play(t.animate.set_value(T_FULL), run_time=T_FULL / 2, rate_func=linear)
        self.wait(0.5)

        # --- parte 2: zoom sulla svolta della persona evidenziata, 1x
        tt = [turn_time(m) for m, _, _ in MODELS]
        u = ValueTracker(-1.2)  # tempo relativo alla svolta: si parte quando la persona è già nella finestra
        zpanels = [Panel(self, m, [x, y0, 0], side, at(D[f"{m}_pos"], tk)[FOCUS], ZOOM_HALF)
                   for (m, _, _), x, tk in zip(MODELS, xs, tt)]

        def zoomed():
            g = VGroup()
            for zp, tk, fr in zip(zpanels, tt, frames):
                g.add(zp.people(tk + u.get_value(), 0, t0=tk - ZOOM_T))
            return g

        zlive = always_redraw(zoomed)
        cap2 = title("Zoom on the orange person's 180° turn · 1×")
        self.play(FadeOut(live), FadeOut(goals), AnimationGroup(FadeOut(cap), FadeIn(cap2), lag_ratio=0.9), run_time=0.6)
        self.add(zlive)
        self.play(u.animate.set_value(ZOOM_T), run_time=ZOOM_T + 1.2, rate_func=linear)
        self.wait(2.0)
