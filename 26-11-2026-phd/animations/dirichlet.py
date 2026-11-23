"""Gaussiana con clipping contro Dirichlet sullo spazio d'azione triangolare (tesi, Cap. 2.3 e 9.1).

Due scene, per la slide 18:
- GaussianClipping: campioni gaussiani, clipping, poi la PDF in 3D prima e dopo il clipping;
- DirichletMapping: simplesso, a = V z, PDF della Dirichlet mappata sul triangolo in 3D, alpha che cambia,
  triangolo ristretto con gli stessi fattori della scena bounding.py (slide 19).

Illustrazione: parametri della gaussiana, concentrazioni alpha e campioni sono sintetici, scelti per mostrare il
meccanismo. Seguono la tesi la matrice dei vertici V, la mappa a = V z, l'azione media V E[z] e la densità della
Dirichlet trasportata sul triangolo (mappa affine: densità divisa per il rapporto delle aree).
Dopo il clipping la massa esterna finisce sul bordo: densità lungo i lati e massa concentrata nei vertici, disegnate
in scala diversa dalla densità (sono masse), come dice la nota nel video.

Render (dalla radice della repo):
    .venv-manim/bin/manim -qh --fps 30 26-11-2026-phd/animations/dirichlet.py GaussianClipping DirichletMapping --media_dir /tmp/manim
"""
import sys
from pathlib import Path

import numpy as np
from scipy.special import gammainc, gammaincinv, gammaln

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "scripts"))
sys.path.insert(0, str(HERE))
from manim_style import *  # noqa: E402,F403
from manim import *  # noqa: E402,F403
from bounding import V_MAX, W_MAX, scaling_factors  # noqa: E402

N = 70
U = np.random.default_rng(7).uniform(0.02, 0.98, size=(N, 3))  # uniformi fisse per i campioni Dirichlet
ALPHAS = [np.array([2.0, 3.0, 8.0]), np.array([9.0, 2.5, 2.5]), np.array([3.0, 7.0, 2.0])]
Z_COLORS = ["#CC79A7", "#56B4E9", "#8C6D31"]  # vertici z1 (avanti), z2 (sinistra), z3 (destra)
C_CLIP = "#D55E00"
MU, SD = np.array([0.62, 0.9]), np.array([0.24, 0.85])  # gaussiana illustrativa
CAM_3D = dict(phi=58 * DEGREES, theta=35 * DEGREES, zoom=1.25)  # dal lato esterno al lato obliquo superiore


# ---------------------------------------------------------------- funzioni comuni

def vertices(kv=1.0, kl=1.0, kr=1.0):
    """Colonne della matrice V (eq. dir_safe_vertex_matrix / dir_safe_safe_vertices)."""
    return np.array([[kv * V_MAX, 0.0, 0.0], [0.0, kl * W_MAX, -kr * W_MAX]])


def inside(a):
    return (a[:, 0] >= 0) & (a[:, 0] <= V_MAX) & (np.abs(a[:, 1]) <= W_MAX * (1 - a[:, 0] / V_MAX) + 1e-9)


def clip(a):
    v = np.clip(a[:, 0], 0, V_MAX)
    lim = W_MAX * (1 - v / V_MAX)
    return np.stack([v, np.clip(a[:, 1], -lim, lim)], axis=1)


def gauss_pdf(v, w):
    return np.exp(-0.5 * (((v - MU[0]) / SD[0]) ** 2 + ((w - MU[1]) / SD[1]) ** 2)) / (2 * np.pi * SD[0] * SD[1])


def dirichlet_samples(alpha):
    g = gammaincinv(alpha[None, :], U)
    return g / g.sum(axis=1, keepdims=True)


def z_of(u, s):
    """Parametrizzazione del simplesso: u = z1, s in [-1, 1] divide il resto tra z2 e z3."""
    return np.array([u, (1 - u) * (1 + s) / 2, (1 - u) * (1 - s) / 2])


def dirichlet_density_on_triangle(z, alpha, V):
    """Densità di a = V z: densità della Dirichlet sul simplesso (area 1/2) divisa per l'area del triangolo."""
    z = np.clip(z, 1e-12, 1)
    log_p = gammaln(alpha.sum()) - gammaln(alpha).sum() + ((alpha - 1) * np.log(z)).sum()
    area = 0.5 * abs(np.linalg.det(np.array([V[:, 0] - V[:, 2], V[:, 1] - V[:, 2]])))
    return np.exp(log_p) * 0.5 / area


def clipped_mass():
    """Dove finisce la massa gaussiana esterna: densità lungo i tre lati e masse nei vertici."""
    dv, dw = 0.004, 0.012
    v, w = np.meshgrid(np.arange(-1.0, 2.2, dv), np.arange(-4.5, 6.5, dw), indexing="ij")
    a = np.stack([v.ravel(), w.ravel()], axis=1)
    m = gauss_pdf(a[:, 0], a[:, 1]) * dv * dw
    out = ~inside(a)
    c = clip(a[out])
    mo = m[out]
    corner = np.isclose(c[:, 0], V_MAX) | (np.isclose(c[:, 0], 0) & np.isclose(np.abs(c[:, 1]), W_MAX))
    masses = {"v": mo[np.isclose(c[:, 0], V_MAX)].sum(),
              "left": mo[np.isclose(c[:, 0], 0) & np.isclose(c[:, 1], W_MAX)].sum(),
              "right": mo[np.isclose(c[:, 0], 0) & np.isclose(c[:, 1], -W_MAX)].sum()}
    edges = {}
    nb = 24
    up = ~corner & (c[:, 0] > 0) & (c[:, 1] > 0) & np.isclose(c[:, 1], W_MAX * (1 - c[:, 0] / V_MAX))
    lo = ~corner & (c[:, 0] > 0) & (c[:, 1] < 0) & np.isclose(-c[:, 1], W_MAX * (1 - c[:, 0] / V_MAX))
    lf = ~corner & np.isclose(c[:, 0], 0)
    seg_len = np.hypot(V_MAX, W_MAX) / nb  # lunghezza di un tratto sui lati obliqui
    for name, sel, coord, lo_, hi_, length in [("upper", up, 0, 0, V_MAX, seg_len), ("lower", lo, 0, 0, V_MAX, seg_len),
                                               ("left", lf, 1, -W_MAX, W_MAX, 2 * W_MAX / nb)]:
        h, _ = np.histogram(c[sel, coord], bins=nb, range=(lo_, hi_), weights=mo[sel])
        edges[name] = h / length  # massa per unità di lunghezza
    return masses, edges, mo.sum()


def label(text):
    return Text(text, font=FONT, color=INK, font_size=34).to_edge(UP, buff=0.3)


class BaseScene(ThreeDScene):
    """Spazio d'azione su assi 3D: dall'alto è il piano (v, omega), ruotando la camera compare la densità."""

    def setup_axes(self, z_max, center, z_length=3.0):
        self.ax = ThreeDAxes(x_range=[0, 1.25, 0.5], y_range=[-3.2, 3.2, 1], z_range=[0, z_max, z_max],
                             x_length=3.4, y_length=5.6, z_length=z_length, tips=False,
                             axis_config={"color": MUTED, "stroke_width": 2, "include_ticks": False})
        self.ax.z_axis.set_opacity(0)
        self.ax.shift(center - self.ax.c2p(0.5, 0, 0))  # centro del triangolo in `center`
        self.v_lbl = MathTex("v", color=INK, font_size=40).move_to(self.ax.c2p(1.38, 0, 0))
        self.w_lbl = MathTex(r"\omega", color=INK, font_size=40).move_to(self.ax.c2p(-0.1, 3.4, 0))
        self.add_fixed_orientation_mobjects(self.v_lbl, self.w_lbl)

    def A(self, v, w, z=0.0):
        return self.ax.c2p(v, w, z)

    def tri(self, kv, kl, kr, color, opacity, width=3):
        return Polygon(*[self.A(*c) for c in vertices(kv, kl, kr).T], color=color, fill_opacity=opacity,
                       stroke_width=width)

    def set_title(self, text, run_time=0.6, extra=()):
        new = label(text)
        self.add_fixed_in_frame_mobjects(new)
        new.set_opacity(0)
        if getattr(self, "title", None) is not None:  # prima sparisce il vecchio titolo, poi compare il nuovo
            anims = [AnimationGroup(FadeOut(self.title), new.animate.set_opacity(1), lag_ratio=0.9)]
        else:
            anims = [new.animate.set_opacity(1)]
        self.play(*anims, *extra, run_time=run_time)
        self.title = new


# ---------------------------------------------------------------- scena 1: gaussiana e clipping

class GaussianClipping(BaseScene):
    def construct(self):
        self.title = None
        z_max = gauss_pdf(*MU) * 1.05
        self.setup_axes(z_max, DOWN * 0.3)
        feasible = self.tri(1, 1, 1, C_FEASIBLE, 0.18)
        act_title = Text("action space", font=FONT, color=MUTED, font_size=26).next_to(self.ax, UP, buff=0.2)
        self.add_fixed_in_frame_mobjects(act_title)
        self.add(self.ax, feasible)
        self.set_title("A Gaussian policy over the action space", run_time=0.8)

        # campioni, clipping
        # seme scelto perché la quota di campioni fuori (32 su 70) coincida con la massa esterna (46%)
        g = np.random.default_rng(0).normal(MU, SD, size=(N, 2))
        ok = inside(g)
        dots = VGroup(*[Dot(self.A(*p), radius=0.055, color=INK if k else C_CLIP) for p, k in zip(g, ok)])
        for d, k in zip(dots, ok):
            if not k:
                d.set_fill(opacity=0).set_stroke(C_CLIP, 2.5)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.035), run_time=2.0)
        counter = Text(f"{int((~ok).sum())} of {N} samples outside", font=FONT, color=C_CLIP, font_size=28)
        counter.move_to(RIGHT * 4.6 + UP * 1.5)
        self.add_fixed_in_frame_mobjects(counter)
        counter.set_opacity(0)
        self.set_title("Samples outside the triangle are clipped", extra=[counter.animate.set_opacity(1)])
        c = clip(g[~ok])
        out_dots = [d for d, k in zip(dots, ok) if not k]
        paths = VGroup(*[DashedLine(d.get_center(), self.A(*q), color=C_CLIP, stroke_width=2, dash_length=0.06)
                         for d, q in zip(out_dots, c)])
        self.play(Create(paths), run_time=0.5)
        self.play(*[d.animate.move_to(self.A(*q)).set_fill(C_CLIP, 1) for d, q in zip(out_dots, c)], FadeOut(paths),
                  run_time=1.0)
        self.wait(0.6)

        # PDF in 3D: prima intera, poi clippata
        surf = Surface(lambda u, s: self.A(u, s, gauss_pdf(u, s)), u_range=[-0.2, 1.45], v_range=[-2.0, 3.7],
                       resolution=(34, 34), fill_opacity=0.75, stroke_width=0.4, stroke_color=WHITE)
        out_faces = VGroup()
        for f in surf:
            v, w, _ = self.ax.p2c(f.get_center())
            if inside(np.array([[v, w]]))[0]:
                f.set_fill("#5A6270", 0.8)
            else:
                f.set_fill("#B9BEC6", 0.55)
                out_faces.add(f)
        base = self.A(0, 0, 0)
        surf.save_state()
        surf.stretch(0.01, 2, about_point=base)
        note = Text("height: probability density", font=FONT, color=MUTED, font_size=22).to_corner(DL, buff=0.4)
        self.add_fixed_in_frame_mobjects(note)
        note.set_opacity(0)
        self.set_title("Its density spills outside the triangle", run_time=0.6,
                       extra=[FadeOut(dots), FadeOut(counter), act_title.animate.set_opacity(0),
                              feasible.animate.set_fill(opacity=0)])
        self.move_camera(**CAM_3D, run_time=1.6)
        self.add(surf)
        self.play(Restore(surf), note.animate.set_opacity(1), run_time=1.4)
        self.wait(0.6)

        # massa esterna sul bordo: tende lungo i lati, picchi nei vertici (scala delle masse a parte)
        masses, edges, total_out = clipped_mass()
        k_line = 0.55 * z_max / max(h.max() for h in edges.values())
        k_point = 0.95 * z_max / max(masses.values())
        curtains = VGroup()
        nb = len(edges["upper"])
        for name, h in edges.items():
            for i, hi in enumerate(h):
                t0, t1 = i / nb, (i + 1) / nb
                if name == "left":
                    p0, p1 = (0, -W_MAX + 2 * W_MAX * t0), (0, -W_MAX + 2 * W_MAX * t1)
                else:
                    sgn = 1 if name == "upper" else -1
                    p0 = (t0 * V_MAX, sgn * W_MAX * (1 - t0))
                    p1 = (t1 * V_MAX, sgn * W_MAX * (1 - t1))
                curtains.add(Polygon(self.A(*p0), self.A(*p1), self.A(*p1, hi * k_line), self.A(*p0, hi * k_line),
                                     color=C_CLIP, fill_opacity=0.85, stroke_width=0.5))
        spikes = VGroup()
        for key, (pv, pw) in {"v": (V_MAX, 0), "left": (0, W_MAX), "right": (0, -W_MAX)}.items():
            if masses[key] > 1e-4:
                spikes.add(Line(self.A(pv, pw, 0), self.A(pv, pw, masses[key] * k_point), color=C_CLIP, stroke_width=9))
        curtains.save_state()
        curtains.stretch(0.01, 2, about_point=base)
        note2 = Text(f"orange: the {100 * total_out:.0f}% of the mass that was outside, now on the border (own scale)",
                     font=FONT, color=C_CLIP, font_size=22).next_to(note, UP, buff=0.12, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(note2)
        note2.set_opacity(0)
        self.set_title("Clipping piles that mass onto the border", run_time=0.6)
        self.add(curtains)
        self.play(*[f.animate.set_fill(opacity=0).set_stroke(opacity=0) for f in out_faces], Restore(curtains),
                  LaggedStart(*[Create(s) for s in spikes], lag_ratio=0.2), note2.animate.set_opacity(1), run_time=1.8)
        self.set_title("Executed actions differ from what the policy learns", run_time=0.6)
        self.wait(3.0)


# ---------------------------------------------------------------- scena 2: Dirichlet

class DirichletMapping(BaseScene):
    def construct(self):
        self.title = None
        kv_s, kl_s, kr_s, _ = scaling_factors()
        # altezza massima della densità sugli alpha e sui triangoli mostrati, per una scala fissa
        uu, ss = np.meshgrid(np.linspace(0.01, 0.99, 60), np.linspace(-0.99, 0.99, 60))
        z_max = 1.05 * max(dirichlet_density_on_triangle(z_of(u, s), al, vertices(*k))
                           for al in ALPHAS[:2] for k in [(1, 1, 1), (kv_s, kl_s, kr_s)]
                           for u, s in zip(uu.ravel(), ss.ravel()))
        self.setup_axes(z_max, DOWN * 0.3 + RIGHT * 4.2, z_length=2.3)  # picco più alto sul triangolo ristretto
        feasible = self.tri(1, 1, 1, C_FEASIBLE, 0.18)
        act_title = Text("action space", font=FONT, color=MUTED, font_size=26).next_to(self.ax, UP, buff=0.2)
        self.add_fixed_in_frame_mobjects(act_title)
        self.add(self.ax, feasible)

        # simplesso con i campioni
        side = 4.6
        S = [LEFT * 3.9 + DOWN * 0.3 + side / np.sqrt(3) * np.array([np.cos(t), np.sin(t), 0])
             for t in (0, 2 * np.pi / 3, 4 * np.pi / 3)]  # z1 a destra, z2 in alto, z3 in basso: come il triangolo
        simplex = Polygon(*S, color=INK, stroke_width=3, fill_opacity=0.04)
        s_title = Text("simplex", font=FONT, color=MUTED, font_size=26).move_to([-3.2, act_title.get_y(), 0])
        self.add_fixed_in_frame_mobjects(s_title)
        z_dots = VGroup(*[Dot(p, radius=0.11, color=c) for p, c in zip(S, Z_COLORS)])
        z_lbls = VGroup(MathTex("z_1", color=INK, font_size=36).next_to(S[0], RIGHT, buff=0.15),
                        MathTex("z_2", color=INK, font_size=36).next_to(S[1], UP, buff=0.15),
                        MathTex("z_3", color=INK, font_size=36).next_to(S[2], DOWN, buff=0.15))
        z0 = dirichlet_samples(ALPHAS[0])
        s_dots = VGroup(*[Dot(p, radius=0.055, color=C_DIRSAFE) for p in z0 @ np.array(S)])
        self.set_title("A Dirichlet distribution lives on the simplex", run_time=0.8,
                       extra=[Create(simplex), FadeIn(z_dots), FadeIn(z_lbls)])
        self.play(FadeIn(s_dots), run_time=0.8)
        self.wait(0.5)

        # a = V z
        Vt = vertices()
        eq = MathTex(r"a = V z", color=INK, font_size=44).move_to(RIGHT * 0.6 + UP * 0.4)
        arrow = Arrow(LEFT * 0.6 + DOWN * 0.2, RIGHT * 1.9 + DOWN * 0.2, buff=0, color=INK, stroke_width=4)
        a_dots = VGroup(*[Dot(self.A(*Vt[:, i]), radius=0.11, color=c) for i, c in enumerate(Z_COLORS)])
        target = VGroup(*[Dot(self.A(*a), radius=0.055, color=C_DIRSAFE) for a in z0 @ Vt.T])
        self.set_title("Every sample becomes a feasible action", extra=[Write(eq), GrowArrow(arrow)])
        self.play(TransformFromCopy(z_dots, a_dots), TransformFromCopy(s_dots, target), run_time=1.6)
        self.wait(0.6)

        # densità della Dirichlet sul triangolo, in 3D
        alpha = [ValueTracker(x) for x in ALPHAS[0]]
        kv, kl, kr = ValueTracker(1.0), ValueTracker(1.0), ValueTracker(1.0)

        def surface():
            al = np.array([a.get_value() for a in alpha])
            V = vertices(kv.get_value(), kl.get_value(), kr.get_value())

            def f(u, s):
                z = z_of(u, s)
                return self.A(*(V @ z), dirichlet_density_on_triangle(z, al, V))

            srf = Surface(f, u_range=[0, 1], v_range=[-1, 1], resolution=(26, 26), fill_opacity=0.85,
                          stroke_width=0.4, stroke_color=WHITE)
            srf.set_fill(C_DIRSAFE, 0.85)
            return srf

        def mean_star():
            al = np.array([a.get_value() for a in alpha])
            V = vertices(kv.get_value(), kl.get_value(), kr.get_value())
            return Star(n=5, outer_radius=0.16, color=INK, fill_opacity=1).move_to(self.A(*(V @ (al / al.sum()))))

        note = Text("height: probability density · zero outside, no mass on the border", font=FONT, color=MUTED,
                    font_size=22).to_corner(DL, buff=0.4)
        self.add_fixed_in_frame_mobjects(note)
        note.set_opacity(0)
        self.set_title("Its density, mapped onto the triangle", run_time=0.6,
                       extra=[FadeOut(simplex), FadeOut(z_dots), FadeOut(z_lbls), FadeOut(s_dots), FadeOut(eq),
                              FadeOut(arrow), FadeOut(target), s_title.animate.set_opacity(0),
                              act_title.animate.set_opacity(0), feasible.animate.set_fill(opacity=0)])
        self.play(VGroup(self.ax, feasible, a_dots, self.v_lbl, self.w_lbl).animate.shift(LEFT * 4.2), run_time=0.8)
        surf = surface()  # dopo lo spostamento degli assi
        base = self.A(0, 0, 0)
        surf.save_state()
        surf.stretch(0.01, 2, about_point=base)
        self.move_camera(**CAM_3D, run_time=1.6)
        self.add(surf)
        self.play(Restore(surf), note.animate.set_opacity(1), run_time=1.4)
        self.wait(0.5)

        # la policy sceglie alpha: la densità si sposta e si stringe; stella = azione media V E[z]
        live = always_redraw(surface)
        star = always_redraw(mean_star)
        self.remove(surf)
        self.add(live)
        self.set_title("The policy outputs the concentrations α", extra=[FadeIn(star)])
        self.play(*[a.animate.set_value(x) for a, x in zip(alpha, ALPHAS[1])], run_time=2.0)
        self.wait(0.4)

        # stesso output, triangolo ristretto dal bounding (slide successiva)
        restricted = always_redraw(lambda: self.tri(kv.get_value(), kl.get_value(), kr.get_value(), C_RESTRICTED, 0, 4))
        vdots = always_redraw(lambda: VGroup(*[Dot(self.A(*vertices(kv.get_value(), kl.get_value(), kr.get_value())[:, i]),
                                                   radius=0.11, color=c) for i, c in enumerate(Z_COLORS)]))
        self.remove(a_dots)
        self.add(vdots)
        self.set_title("The same output works on the restricted triangle", extra=[FadeIn(restricted)])
        self.play(kv.animate.set_value(kv_s), kl.animate.set_value(kl_s), kr.animate.set_value(kr_s), run_time=2.0)
        self.wait(2.5)
