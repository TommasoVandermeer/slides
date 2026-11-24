"""Due politiche SARL sullo stesso episodio (slide 13): addestrata con SFM a sinistra, con HSFM a destra.

Dati: episodi registrati con social-jym (examples/test_sarl.py, random_seed = 70), convertiti da sarl_extract.py in
data/sarl_episodes.npz. Stesse condizioni iniziali, persone mosse dall'HSFM, robot olonomo (raggi 0.3 m).
Accanto a ogni simulazione: il valore che SARL calcola per ognuna delle 81 velocità discrete (ferma + 5 moduli
x 16 direzioni, come in socialjym/policies/cadrl.py), con il colore normalizzato a ogni passo e l'azione scelta
(la migliore) bordata. Nessuna traiettoria è inventata.

Render (dalla radice della repo):
    .venv-manim/bin/manim -qh --fps 30 26-11-2026-phd/animations/sarl_episodes.py SarlEpisodes --media_dir /tmp/manim
"""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "scripts"))
from manim_style import *  # noqa: E402,F403
from manim import *  # noqa: E402,F403

# formato largo (12:5): due simulazioni con il loro spazio d'azione, affiancate
config.frame_height = 6.0
config.pixel_height = 800
config.pixel_width = 1920

D = np.load(HERE / "data" / "sarl_episodes.npz")
DT = float(D["robot_dt"])
SUB = DT / int(D["substeps"])           # passo dei sotto-campioni (s)
R = float(D["radius"])
MODELS = [("sfm", "Trained with SFM"), ("hsfm", "Trained with HSFM")]
HALF = 7.8                               # metà lato della finestra (m), centrata nell'origine
TRAIL = 1.5                              # coda delle persone (s)
GRAY = "#9AA0A6"
ROBOT = C_HM

# spazio d'azione olonomo di SARL: indice 0 = ferma, poi i = 1 + 5*direzione + modulo
SPEEDS = (np.exp(np.arange(1, 6) / 5) - 1) / (np.e - 1)
ANGLES = np.linspace(0, 2 * np.pi, 16, endpoint=False)
EDGES = np.concatenate([[SPEEDS[0] / 2], (SPEEDS[:-1] + SPEEDS[1:]) / 2, [1.0]])  # bordi degli anelli (m/s)

VIRIDIS = ["#440154", "#482878", "#3E4A89", "#31688E", "#26828E", "#1F9E89", "#35B779", "#6DCD59", "#B4DE2C", "#FDE725"]


def viridis(x):
    x = float(np.clip(x, 0, 1)) * (len(VIRIDIS) - 1)
    i = min(int(x), len(VIRIDIS) - 2)
    return interpolate_color(ManimColor(VIRIDIS[i]), ManimColor(VIRIDIS[i + 1]), x - i)


def normalized(v):
    """Colore relativo al passo: dal 10° percentile al massimo (poche azioni pessime non schiacciano la scala)."""
    lo = np.percentile(v, 10)
    return np.clip((v - lo) / max(v.max() - lo, 1e-9), 0, 1)


class Side:
    def __init__(self, model, sim_center, side, disk_center, disk_r):
        self.pos, self.theta = D[f"{model}_pos"], D[f"{model}_theta"]
        self.values, self.actions = D[f"{model}_values"], D[f"{model}_actions"]
        self.goal = D[f"{model}_goal"]
        self.n = len(self.pos)
        self.T = len(self.values) * DT                # tempo all'obiettivo: passi x 0.25 s
        self.c, self.k = np.array(sim_center), side / (2 * HALF)
        self.dc, self.dr = np.array(disk_center), disk_r
        rob = self.pos[:, -1]
        self.length = float(np.linalg.norm(np.diff(rob, axis=0), axis=1).sum())
        # space compliance come in social-jym (aux_functions.py) e nella tesi (cap. 3): frazione dei passi del robot
        # in cui la distanza tra i bordi del robot e della persona più vicina supera 0.5 m
        steps = self.pos[::int(D["substeps"])]
        clear = np.linalg.norm(steps[:, :-1] - steps[:, -1:], axis=2).min(axis=1) - 2 * R
        self.sc = float((clear > 0.5).mean())

    def P(self, xy):
        return self.c + np.array([xy[0] * self.k, xy[1] * self.k, 0.0])

    def idx(self, t):
        return float(np.clip(t / SUB, 0, self.n - 1))

    def at(self, arr, t):
        x = self.idx(t)
        i = int(np.floor(x)); j = min(i + 1, self.n - 1); f = x - i
        return (1 - f) * arr[i] + f * arr[j]

    def step(self, t):
        return int(np.clip(t // DT, 0, len(self.values) - 1))

    # --- simulazione
    def world(self, t):
        g = VGroup()
        i1 = int(self.idx(t))
        i0 = max(0, int((t - TRAIL) / SUB))
        now = self.at(self.pos, t)
        for h in range(self.pos.shape[1] - 1):
            if i1 > i0 + 1:
                xy = np.vstack([self.pos[i0:i1 + 1:2, h], now[h][None]])
                g.add(VMobject(stroke_color=GRAY, stroke_width=2, stroke_opacity=0.6)
                      .set_points_as_corners([self.P(p) for p in xy]))
            c = self.P(now[h])
            g.add(Circle(radius=R * self.k, color=GRAY, fill_opacity=0.55, stroke_width=0).move_to(c))
            th = self.at(self.theta, t)[h]  # le persone (HSFM) hanno un orientamento; il robot olonomo no
            g.add(Line(c, c + R * self.k * 1.6 * np.array([np.cos(th), np.sin(th), 0]), color=INK, stroke_width=2.5))
        # robot: traccia completa del percorso, poi il disco
        if i1 > 1:
            xy = np.vstack([self.pos[:i1 + 1:2, -1], now[-1][None]])
            g.add(VMobject(stroke_color=ROBOT, stroke_width=3.5).set_points_as_corners([self.P(p) for p in xy]))
        g.add(Circle(radius=R * self.k, color=ROBOT, fill_opacity=1, stroke_color=INK, stroke_width=1.5)
              .move_to(self.P(now[-1])))
        return g

    # --- spazio d'azione
    def cells(self):
        cells = [Circle(radius=EDGES[0] * self.dr)]
        for i in range(1, 81):
            s, d = (i - 1) % 5, (i - 1) // 5
            cells.append(AnnularSector(inner_radius=EDGES[s] * self.dr, outer_radius=EDGES[s + 1] * self.dr,
                                       angle=ANGLES[1] * 0.999, start_angle=ANGLES[d] - ANGLES[1] / 2))
        g = VGroup(*cells).move_to(self.dc)
        for c in g:
            c.set_stroke(WHITE, width=0.8).set_fill(opacity=1)
        g.shift(self.dc - g[0].get_center())  # centro del disco = velocità nulla
        return g

    def paint(self, cells, t):
        x = normalized(self.values[self.step(t)])
        for c, xi in zip(cells, x):
            c.set_fill(viridis(xi), opacity=1)

    def chosen(self, cells, t):
        best = int(np.argmax(self.values[self.step(t)]))
        return cells[best].copy().set_fill(opacity=0).set_stroke(INK, width=4.5)


class SarlEpisodes(Scene):
    def construct(self):
        side, disk_r, y0 = 4.3, 0.9, 0.1
        sides = [Side(m, [sx, y0, 0], side, [dx, y0 + 0.3, 0], disk_r)
                 for (m, _), sx, dx in zip(MODELS, (-4.9, 2.35), (-1.6, 5.85))]

        t = ValueTracker(0.0)
        T_END = max(s.T for s in sides)
        static, front = VGroup(), VGroup()
        for s, (_, name) in zip(sides, MODELS):
            frame = Square(side, stroke_color=MUTED, stroke_width=1.5).move_to(s.c)
            title = Text(name, font=FONT, color=INK, font_size=30, weight=BOLD).next_to(frame, UP, buff=0.18)
            goal = Star(n=5, outer_radius=0.1, color=ROBOT, fill_opacity=1).move_to(s.P(s.goal))
            # assi dello spazio d'azione (frame del mondo, come la simulazione)
            ax_len = disk_r * 1.12
            axes = VGroup(
                Line(s.dc + LEFT * ax_len, s.dc + RIGHT * ax_len, color=MUTED, stroke_width=1.5),
                Line(s.dc + DOWN * ax_len, s.dc + UP * ax_len, color=MUTED, stroke_width=1.5),
            )
            vx = MathTex("v_x", color=INK, font_size=26).next_to(axes[0].get_end(), UP, buff=0.06)
            vy = MathTex("v_y", color=INK, font_size=26).next_to(axes[1].get_end(), RIGHT, buff=0.08)
            head = Text("Action values", font=FONT, color=INK, font_size=20).next_to(s.dc + UP * disk_r, UP, buff=0.42)
            bar = VGroup(*[Rectangle(width=1.5 / 40, height=0.14, stroke_width=0, fill_color=viridis(i / 39), fill_opacity=1)
                           for i in range(40)]).arrange(RIGHT, buff=0).next_to(s.dc + DOWN * disk_r, DOWN, buff=0.4)
            lo = Text("low", font=FONT, color=MUTED, font_size=16).next_to(bar, DOWN, buff=0.06).align_to(bar, LEFT)
            hi = Text("high", font=FONT, color=MUTED, font_size=16).next_to(bar, DOWN, buff=0.06).align_to(bar, RIGHT)
            key_box = Square(0.16, stroke_color=INK, stroke_width=3, fill_opacity=0)
            key = VGroup(key_box, Text("chosen action", font=FONT, color=MUTED, font_size=16)).arrange(RIGHT, buff=0.1) \
                .next_to(VGroup(bar, lo), DOWN, buff=0.14)
            static.add(frame, title, goal, head, bar, lo, hi, key)
            front.add(axes, vx, vy)  # sopra le celle

        cells = [s.cells() for s in sides]
        for s, c in zip(sides, cells):
            s.paint(c, 0.0)
            c.add_updater(lambda m, s=s: s.paint(m, t.get_value()))

        live = always_redraw(lambda: VGroup(*[s.world(t.get_value()) for s in sides]))
        marks = always_redraw(lambda: VGroup(*[s.chosen(c, t.get_value()) for s, c in zip(sides, cells)]))

        def clock(s):
            def f():
                tt = min(t.get_value(), s.T)
                done = t.get_value() >= s.T
                txt = (f"{s.T:.1f} s to goal · {s.length:.1f} m path · {100 * s.sc:.0f}% space compliance"
                       if done else f"t = {tt:.1f} s")
                box = Square(side).move_to(s.c)
                return Text(txt, font=FONT, color=INK if done else MUTED, font_size=20,
                            weight=BOLD if done else NORMAL).next_to(box, DOWN, buff=0.1).align_to(box, LEFT)
            return always_redraw(f)

        clocks = VGroup(*[clock(s) for s in sides])
        cap = Text("Same start · people move with the HSFM · line: robot path · 1×", font=FONT, color=MUTED,
                   font_size=20).to_edge(DOWN, buff=0.12)

        self.add(static, *cells, front, live, marks, clocks, cap)
        self.wait(1.0)
        self.play(t.animate.set_value(T_END), run_time=T_END, rate_func=linear)
        self.wait(3.0)
