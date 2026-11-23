#!/usr/bin/env python3
"""Grafici del deck: SR e ablation dai numeri della tesi (Cap. 10, tab:jessi_benchmark e
tab:jessi_ablation); gaussiana contro Dirichlet è un'illustrazione con campioni sintetici.

Uso, dalla cartella del deck: python3 scripts/charts.py -> public/figures/*.svg
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent.parent / "public" / "figures"
JESSI, DIRSAFE, GRAY, INK, MUTED = "#009e73", "#0072b2", "#8a8a8a", "#222222", "#666666"
# spazio d'azione: rosso = azioni originali, verde = ristrette dal bounding (come i video e le figure della tesi)
FEASIBLE, RESTRICTED = "#d62728", "#2ca02c"

plt.rcParams.update({
    "font.family": "sans-serif", "font.size": 20, "svg.fonttype": "none",
    "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": INK,
    "axes.spines.top": False, "axes.spines.right": False,
})

# SR (%) medio e IC al 95% su 10 seed (None = planner senza training)
SR = {  # policy: (setup1, ci1, setup2, ci2)
    "JESSI": (97.5, 1.9, 89.6, 8.5),
    "DIR-SAFE": (85.4, 7.2, 87.1, 7.8),
    "SARL*": (70.2, 10.6, 82.7, 8.9),
    "BV-E2E": (98.8, 1.2, 78.6, 13.8),
    "DRA-MPPI": (78.1, None, 77.7, None),
    "DWA": (74.3, None, 75.0, None),
    "MPPI": (61.0, None, 74.4, None),
    "V-E2E": (91.5, 6.3, 54.7, 24.2),
}
COLOR = {"JESSI": JESSI, "DIR-SAFE": DIRSAFE}


def sr_chart():
    order = sorted(SR, key=lambda p: SR[p][2])  # dal più basso al più alto in Setup 2
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.6), sharey=True)
    for ax, (col, ci, title) in zip(axes, [(0, 1, "Known layouts (Setup 1)"), (2, 3, "Unseen layouts (Setup 2)")]):
        for y, p in enumerate(order):
            v, e = SR[p][col], SR[p][ci]
            c = COLOR.get(p, GRAY)
            ax.barh(y, v, height=0.62, color=c)
            if e:
                ax.errorbar(v, y, xerr=e, fmt="none", ecolor=INK, elinewidth=1.6, capsize=4)
            ax.text((v + (e or 0)) + 1.5, y, f"{v:.1f}", va="center", fontsize=17,
                    color=INK, fontweight="bold" if p in COLOR else "normal")
        ax.set_xlim(0, 118)
        ax.set_xticks([0, 25, 50, 75, 100])
        ax.set_title(title, fontsize=21, color=INK, loc="left", pad=12)
        ax.set_xlabel("Success rate (%)")
        ax.grid(axis="x", color="#e5e5e5", linewidth=1)
        ax.set_axisbelow(True)
        ax.tick_params(axis="y", length=0)
    axes[0].set_yticks(range(len(order)))
    axes[0].set_yticklabels(order)
    for lbl in axes[0].get_yticklabels():
        if lbl.get_text() in COLOR:
            lbl.set_fontweight("bold")
    fig.tight_layout()
    fig.savefig(OUT / "benchmark_sr.svg", transparent=True)


def bounding_chart():
    rows = [  # (etichetta, CR-O %, con bounding?)
        ("JESSI\nwith bounding", 3.3, True),
        ("JESSI\nwithout bounding", 40.3, False),
        ("End-to-end\nwith bounding", 5.7, True),
        ("End-to-end\nwithout bounding", 42.5, False),
    ]
    fig, ax = plt.subplots(figsize=(12, 5.4))
    xs = [0, 1, 2.6, 3.6]
    for x, (name, v, b) in zip(xs, rows):
        ax.bar(x, v, width=0.72, color=RESTRICTED if b else FEASIBLE)
        ax.text(x, v + 1.2, f"{v:.1f}%", ha="center", fontsize=21, color=INK, fontweight="bold")
    ax.set_xticks(xs)
    ax.set_xticklabels([r[0] for r in rows], fontsize=18)
    ax.set_ylabel("Collisions with obstacles (%)")
    ax.set_ylim(0, 50)
    ax.set_yticks([0, 10, 20, 30, 40, 50])
    ax.grid(axis="y", color="#e5e5e5", linewidth=1)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", length=0)
    fig.tight_layout()
    fig.savefig(OUT / "bounding_ablation.svg", transparent=True)



def dirichlet_vs_gaussian(seed=3):
    """Illustrazione (campioni sintetici, non dati): gaussiana con clipping contro Dirichlet sul triangolo."""
    import numpy as np
    rng = np.random.default_rng(seed)
    V = np.array([[0.0, 1.0], [0.0, -1.0], [1.0, 0.0]])  # vertici (v, omega) normalizzati
    tri = plt.Polygon(V, closed=True, fill=False, edgecolor=INK, linewidth=2.5)

    def inside(p):
        v, w = p[:, 0], p[:, 1]
        return (v >= 0) & (np.abs(w) <= 1 - v)

    def clip(p):
        q = p.copy()
        q[:, 0] = np.clip(q[:, 0], 0, 1)
        lim = 1 - q[:, 0]
        q[:, 1] = np.clip(q[:, 1], -lim, lim)
        return q

    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2))
    g = rng.normal([0.7, 0.25], [0.22, 0.3], size=(160, 2))
    ok = inside(g)
    ax = axes[0]
    ax.add_patch(plt.Polygon(V, closed=True, fill=False, edgecolor=INK, linewidth=2.5))
    ax.scatter(g[ok, 0], g[ok, 1], s=28, color=GRAY, alpha=0.8)
    ax.scatter(g[~ok, 0], g[~ok, 1], s=34, facecolors="none", edgecolors="#d55e00", linewidths=1.6)
    c = clip(g[~ok])
    for a, b in zip(g[~ok], c):
        ax.plot([a[0], b[0]], [a[1], b[1]], color="#d55e00", alpha=0.35, linewidth=1)
    ax.scatter(c[:, 0], c[:, 1], s=28, color="#d55e00", marker="x")
    ax.set_title("Gaussian: samples outside, then clipped", fontsize=21, color=INK, loc="left")
    d = rng.dirichlet([2.0, 3.0, 9.0], size=160) @ V
    ax = axes[1]
    ax.add_patch(plt.Polygon(V, closed=True, fill=False, edgecolor=INK, linewidth=2.5))
    ax.scatter(d[:, 0], d[:, 1], s=28, color=DIRSAFE, alpha=0.85)
    ax.set_title("Dirichlet: every sample is feasible", fontsize=21, color=INK, loc="left")
    for ax in axes:
        ax.set_xlim(-0.15, 1.35)
        ax.set_ylim(-1.15, 1.3)
        ax.set_xlabel("linear velocity $v$")
        ax.set_ylabel(r"angular velocity $\omega$")
        ax.set_xticks([])
        ax.set_yticks([])
    fig.tight_layout()
    fig.savefig(OUT / "dirichlet_vs_gaussian.svg", transparent=True)


if __name__ == "__main__":
    sr_chart()
    bounding_chart()
    dirichlet_vs_gaussian()
