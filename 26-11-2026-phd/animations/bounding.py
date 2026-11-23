"""Action space bounding di DIR-SAFE (tesi, Cap. 9.2, Algoritmo 1), in due fasi.

Illustrazione con la geometria della figura della tesi (fig:dir_safe_action_space_bound):
muro a L, parametri del robot del Cap. 9.4, ma dt = 0.75 s per rendere visibile lo spostamento.
Spostamenti, riquadri e fattori di scala sono calcolati con le formule della tesi.

Render (dalla radice della repo):
    .venv-manim/bin/manim -qh --fps 30 26-11-2026-phd/animations/bounding.py Bounding --media_dir /tmp/manim
"""
import sys
from pathlib import Path

import numpy as np
from shapely.geometry import LineString, MultiPoint, box

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from manim_style import *  # noqa: E402,F403
from manim import *  # noqa: E402,F403

# Parametri del robot (Cap. 9.4) e passo illustrativo della figura della tesi
V_MAX, W_MAX, R, DT = 1.0, 2 / 0.7, 0.3, 0.75
# Muro a L, coordinate robot-centriche (x avanti, y a sinistra)
WALLS = [((-0.2, 0.37), (0.72, 0.37)), ((0.72, 0.37), (0.72, -0.45))]
WALL_OUT = [(0.0, 1.0), (1.0, 0.0)]  # normale di ogni faccia, verso l'interno dell'ostacolo
WALL_T = 0.025  # spessore disegnato, tutto oltre la faccia: la geometria resta la faccia
EPS = 1e-6  # bordo dei riquadri laterali aperto: il contatto sullo spigolo non conta


def displacement(v, w):
    """Spostamento in un passo (eq. dir_safe_x_model_rc, dir_safe_y_model_rc)."""
    if abs(w) < 1e-9:
        return v * DT, 0.0
    return v / w * np.sin(w * DT), v / w * (1 - np.cos(w * DT))


def triangle(kv=1.0, kl=1.0, kr=1.0):
    return np.array([[kv * V_MAX, 0.0], [0.0, kl * W_MAX], [0.0, -kr * W_MAX]])


def envelope(kv=1.0, kl=1.0, kr=1.0, n=36):
    """Inviluppo delle configurazioni successive: unione dei dischi del robot su tutte le azioni ammissibili."""
    V = triangle(kv, kl, kr)
    pts = []
    for i in range(n + 1):
        for j in range(n + 1 - i):
            a, b = i / n, j / n
            v, w = a * V[0] + b * V[1] + (1 - a - b) * V[2]
            pts.append(displacement(v, w))
    return MultiPoint(pts).buffer(R, quad_segs=24)


def bounding(kv=1.0, kl=1.0, kr=1.0):
    dx = kv * V_MAX * DT                           # eq. dir_safe_delta_x_max
    dy_max = kv * V_MAX * kl * W_MAX * DT**2 / 8   # eq. dir_safe_delta_y_max
    dy_min = -kv * V_MAX * kr * W_MAX * DT**2 / 8  # eq. dir_safe_delta_y_min
    return dx, dy_max, dy_min


def hits(region):
    """Punti dei muri dentro una regione (Liang-Barsky nella tesi, qui shapely)."""
    out = []
    for a, b in WALLS:
        g = LineString([a, b]).intersection(region)
        if not g.is_empty:
            out.extend(np.array(g.coords).tolist() if g.geom_type == "LineString" else [])
    return np.array(out)


def scaling_factors():
    """Algoritmo 1 della tesi: prima kappa_v, poi kappa_left e kappa_right."""
    dx, _, _ = bounding()
    I_v = hits(box(0, -R, R + dx, R))
    dx_safe = max(I_v[:, 0].min() - R, 0) if len(I_v) else dx
    kv = dx_safe / (V_MAX * DT)
    if kv == 0:
        return kv, 1.0, 1.0, dx_safe
    _, dy_max, dy_min = bounding(kv)
    I_l = hits(box(-R, R, R + dx_safe - EPS, R + dy_max))
    I_r = hits(box(-R, -R - abs(dy_min), R + dx_safe - EPS, -R))
    kl = 8 * (I_l[:, 1].min() - R) / (kv * V_MAX * W_MAX * DT**2) if len(I_l) else 1.0
    kr = -8 * (I_r[:, 1].max() + R) / (kv * V_MAX * W_MAX * DT**2) if len(I_r) else 1.0
    return kv, kl, kr, dx_safe


class Bounding(Scene):
    def construct(self):
        kv_s, kl_s, kr_s, dx_safe = scaling_factors()

        # --- spazio di lavoro (sinistra) e spazio delle azioni (destra), stessa scala in x e y a sinistra
        ws = Axes(x_range=[-0.45, 1.15], y_range=[-0.62, 0.62], x_length=7.0, y_length=7.0 * 1.24 / 1.6)
        ws.to_edge(LEFT, buff=1.2).shift(DOWN * 0.2)
        act = Axes(x_range=[0, 1.15, 0.5], y_range=[-3.2, 3.2, 1], x_length=2.8, y_length=5.4,
                   tips=False, axis_config={"color": MUTED, "stroke_width": 2, "include_ticks": False})
        act.to_edge(RIGHT, buff=1.1).shift(DOWN * 0.35)
        u = ws.x_length / 1.6  # unità di scena per metro

        # assi del riferimento del robot, a bordo pannello come nella figura della tesi
        x0, y0 = -0.45, -0.62
        frame_axes = VGroup(Line(ws.c2p(x0, y0), ws.c2p(1.15, y0)), Line(ws.c2p(x0, y0), ws.c2p(x0, 0.62)))
        frame_axes.set_stroke(MUTED, 2)
        ticks = VGroup()
        for x in [-0.25, 0, 0.25, 0.5, 0.75, 1.0]:
            ticks.add(Line(ws.c2p(x, y0), ws.c2p(x, y0) + UP * 0.1, stroke_width=2, color=MUTED))
            ticks.add(Text(f"{x:g}", font=FONT, color=MUTED, font_size=20).next_to(ws.c2p(x, y0), DOWN, buff=0.12))
        for y in [-0.5, -0.25, 0, 0.25, 0.5]:
            ticks.add(Line(ws.c2p(x0, y), ws.c2p(x0, y) + RIGHT * 0.1, stroke_width=2, color=MUTED))
            ticks.add(Text(f"{y:g}", font=FONT, color=MUTED, font_size=20).next_to(ws.c2p(x0, y), LEFT, buff=0.12))
        dx_lbl = MathTex(r"\Delta x\ (\mathrm{m})", color=INK, font_size=34).next_to(ws.c2p(1.15, y0), RIGHT, buff=0.15)
        dy_lbl = MathTex(r"\Delta y\ (\mathrm{m})", color=INK, font_size=34).next_to(ws.c2p(x0, 0.62), UP, buff=0.15)
        ws_title = Text("robot frame", font=FONT, color=MUTED, font_size=26).next_to(ws.c2p(0.35, 0.62), UP, buff=0.25)
        ws_axes = VGroup(frame_axes, ticks, dx_lbl, dy_lbl, ws_title)

        def P(x, y):
            return ws.c2p(x, y)

        def poly(geom, color, opacity):
            return Polygon(*[P(x, y) for x, y in list(geom.exterior.coords)[:-1]],
                           color=color, fill_opacity=opacity, stroke_width=1.5)

        def rect(x0, y0, x1, y1, color, opacity=0.12, width=3):
            return Polygon(P(x0, y0), P(x1, y0), P(x1, y1), P(x0, y1),
                           color=color, fill_opacity=opacity, stroke_width=width)

        def strip(a, b, n, color, extend=0.0):
            """Tratto di muro come rettangolo pieno oltre la faccia a-b (normale n)."""
            a, b, n = np.array(a), np.array(b), np.array(n)
            d = (b - a) / np.linalg.norm(b - a) * extend
            a, b = a - d, b + d
            return Polygon(P(*a), P(*b), P(*(b + WALL_T * n)), P(*(a + WALL_T * n)),
                           color=color, fill_opacity=1, stroke_width=0)

        def tri(kv, kl, kr, color, opacity):
            return Polygon(*[act.c2p(v, w) for v, w in triangle(kv, kl, kr)],
                           color=color, fill_opacity=opacity, stroke_width=3)

        def label(text):
            return Text(text, font=FONT, color=INK, font_size=34).to_edge(UP, buff=0.3)

        robot = DashedVMobject(Circle(radius=R * u, color=INK, stroke_width=3), num_dashes=40).move_to(P(0, 0))
        heading = Arrow(P(0, 0), P(0.22, 0), buff=0, color=INK, stroke_width=4, max_tip_length_to_length_ratio=0.3)
        walls = VGroup(*[strip(a, b, n, INK, extend=WALL_T) for (a, b), n in zip(WALLS, WALL_OUT)])
        v_lbl = MathTex("v", color=INK, font_size=40).next_to(act.x_axis.get_end(), RIGHT, buff=0.15)
        w_lbl = MathTex(r"\omega", color=INK, font_size=40).next_to(act.y_axis.get_end(), LEFT, buff=0.15)
        act_title = Text("action space", font=FONT, color=MUTED, font_size=26)
        act_title.move_to([act.get_center()[0], ws_title.get_center()[1], 0])

        full_tri = tri(1, 1, 1, C_FEASIBLE, 0.35)
        title = label("All actions the robot can take in one step")
        self.add(ws_axes, walls, robot, heading)
        self.play(FadeIn(act), FadeIn(v_lbl), FadeIn(w_lbl), FadeIn(act_title), FadeIn(full_tri), Write(title), run_time=1.2)

        # --- un'azione percorre il bordo del triangolo, il robot fantasma mostra dove finisce
        s = ValueTracker(0.0)
        edge = [triangle()[1], triangle()[0], triangle()[2]]

        def action_at(t):
            t = np.clip(t, 0, 1)
            a, b = (edge[0], edge[1]) if t < 0.5 else (edge[1], edge[2])
            k = t * 2 if t < 0.5 else (t - 0.5) * 2
            return (1 - k) * a + k * b

        dot = always_redraw(lambda: Dot(act.c2p(*action_at(s.get_value())), color=INK, radius=0.09))
        ghost = always_redraw(lambda: Circle(radius=R * u, color=C_FEASIBLE, stroke_width=3).move_to(
            P(*displacement(*action_at(s.get_value())))))
        self.add(dot, ghost)
        self.play(s.animate.set_value(1.0), run_time=3.5, rate_func=linear)

        env = poly(envelope(), C_FEASIBLE, 0.35)
        self.play(FadeOut(ghost), FadeOut(dot), FadeIn(env), run_time=0.8)
        # tratti di muro dentro l'inviluppo, calcolati
        segs = []
        for (a, b), n in zip(WALLS, WALL_OUT):
            g = LineString([a, b]).intersection(envelope())
            for part in getattr(g, "geoms", [g]):
                if part.geom_type == "LineString" and part.length > 0:
                    segs.append(strip(part.coords[0], part.coords[-1], n, C_FEASIBLE))
        collide = VGroup(*segs)
        self.play(Transform(title, label("Some next positions hit the wall")), FadeIn(collide), run_time=1.0)
        self.wait(0.6)

        # --- bounding box dell'inviluppo, aumentata del raggio del robot
        dx, dy_max, dy_min = bounding()
        bb = rect(-R, -R - abs(dy_min), R + dx, R + dy_max, C_FEASIBLE, 0, 3)
        self.play(Transform(title, label("Its bounding box, split into four boxes")), Create(bb), run_time=0.8)

        # suddivisione della tesi: B_v (davanti), B_left, B_right, B_back
        parts = [
            (rect(0, -R, R + dx, R, C_FEASIBLE, 0.12, 2), r"\mathcal{B}_v"),
            (rect(-R, R, R + dx, R + dy_max, C_FEASIBLE, 0.12, 2), r"\mathcal{B}_{\text{left}}"),
            (rect(-R, -R - abs(dy_min), R + dx, -R, C_FEASIBLE, 0.12, 2), r"\mathcal{B}_{\text{right}}"),
            (rect(-R, -R, 0, R, C_FEASIBLE, 0.12, 2), r"\mathcal{B}_{\text{back}}"),
        ]
        boxes = VGroup(*[b for b, _ in parts])
        names = VGroup(*[MathTex(t, color=INK, font_size=34).move_to(b.get_center()) for b, t in parts])
        self.play(FadeIn(boxes), FadeIn(names), run_time=0.6)
        self.wait(1.4)

        # --- Fase 1: riquadro frontale, si riduce kappa_v
        kv, kl, kr = ValueTracker(1.0), ValueTracker(1.0), ValueTracker(1.0)
        safe_tri = always_redraw(lambda: tri(kv.get_value(), kl.get_value(), kr.get_value(), C_RESTRICTED, 0.45))
        B_v = always_redraw(lambda: rect(0, -R, R + kv.get_value() * V_MAX * DT, R, C_RESTRICTED))
        self.play(Transform(title, label("Stage 1: limit the forward speed")), FadeOut(env), FadeOut(bb), FadeOut(collide),
                  FadeOut(boxes), FadeOut(names),
                  FadeIn(B_v), FadeIn(safe_tri), full_tri.animate.set_fill(opacity=0.12), run_time=1.0)
        self.play(kv.animate.set_value(kv_s), run_time=2.0)
        self.wait(0.4)

        # --- Fase 2: riquadri laterali, si riducono kappa_left e kappa_right
        def lateral(side):
            def make():
                _, dym, dyn = bounding(kv_s, kl.get_value(), kr.get_value())
                if side == "left":
                    return rect(-R, R, R + dx_safe, R + dym, C_RESTRICTED)
                return rect(-R, -R - abs(dyn), R + dx_safe, -R, C_RESTRICTED)
            return always_redraw(make)

        B_l, B_r = lateral("left"), lateral("right")
        self.play(Transform(title, label("Stage 2: limit turning towards the wall")), FadeIn(B_l), FadeIn(B_r), run_time=1.0)
        self.play(kl.animate.set_value(kl_s), kr.animate.set_value(kr_s), run_time=2.0)
        self.wait(0.4)

        # --- risultato: inviluppo con le sole azioni del triangolo ridotto
        env_safe = poly(envelope(kv_s, kl_s, kr_s), C_RESTRICTED, 0.35)
        self.play(FadeOut(B_v), FadeOut(B_l), FadeOut(B_r), FadeIn(env_safe),
                  Transform(title, label("Every action left keeps the robot off the wall")), run_time=1.2)

        # --- il bounding box si restringe: originale tratteggiato, nuovo in blu
        _, dym_s, dyn_s = bounding(kv_s, kl_s, kr_s)
        bb_old = DashedVMobject(rect(-R, -R - abs(dy_min), R + dx, R + dy_max, C_FEASIBLE, 0, 3), num_dashes=60)
        bb_new = rect(-R, -R - abs(dyn_s), R + dx_safe, R + dym_s, C_RESTRICTED, 0, 3)
        bb_anim = rect(-R, -R - abs(dy_min), R + dx, R + dy_max, C_RESTRICTED, 0, 3)
        self.play(FadeIn(bb_old), FadeIn(bb_anim), run_time=0.5)
        self.play(Transform(bb_anim, bb_new), run_time=1.2)
        self.wait(3.0)
