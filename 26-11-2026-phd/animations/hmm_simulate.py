"""Simula lo stesso circular crossing con ORCA, SFM e HSFM (repo JORCA, JSFM, JHSFM dell'autore).

- Condizioni iniziali identiche per i tre modelli: persone su un cerchio, posizioni perturbate da un'estrazione
  casuale fissa (seed), obiettivo nel punto opposto del cerchio.
- Parametri condivisi identici: raggio, velocità massima, margine di sicurezza, passo di integrazione.
  Gli altri parametri sono quelli standard di ciascuna repo (get_standard_humans_parameters).
- Andata e ritorno: quando una persona raggiunge l'obiettivo, il nuovo obiettivo è il punto di partenza,
  così si vede la svolta di 180 gradi (dove SFM e HSFM differiscono di più).

Uscita: data/hmm_circular_crossing.npz, letto dalla scena Manim hmm.py.

Ambiente: serve JAX con le tre repo installate (non è nel requirements di Manim), per esempio
    python3 -m venv /tmp/venv-jax && /tmp/venv-jax/bin/pip install jax ~/Projects/JSFM ~/Projects/JHSFM ~/Projects/JORCA
    /tmp/venv-jax/bin/python 26-11-2026-phd/animations/hmm_simulate.py
"""
from pathlib import Path

import jax.numpy as jnp
import numpy as np
from jhsfm import utils as hsfm_utils
from jhsfm.hsfm import step as hsfm_step
from jorca import utils as orca_utils
from jorca.orca import step as orca_step
from jsfm import utils as sfm_utils
from jsfm.sfm import step as sfm_step

OUT = Path(__file__).resolve().parent / "data" / "hmm_circular_crossing.npz"

N_HUMANS = 7
CIRCLE_RADIUS = 4.0
POS_NOISE = 0.35       # deviazione standard della perturbazione delle posizioni iniziali (m)
SEED = 3
RADIUS, V_MAX, SAFETY = 0.3, 1.0, 0.05  # parametri condivisi dai tre modelli
DT = 0.01
T_END = 26.0
SAVE_EVERY = 5          # salva uno stato ogni 0.05 s
GOAL_TOL = 0.3          # distanza a cui l'obiettivo si considera raggiunto (= raggio)


def initial_conditions():
    rng = np.random.default_rng(SEED)
    ang = 2 * np.pi * np.arange(N_HUMANS) / N_HUMANS
    start = CIRCLE_RADIUS * np.stack([np.cos(ang), np.sin(ang)], axis=1) + rng.normal(0, POS_NOISE, (N_HUMANS, 2))
    goal = -start  # punto opposto (della posizione perturbata)
    return start, goal


def shared(params, idx_radius, idx_vmax, idx_safety):
    return params.at[:, idx_radius].set(RADIUS).at[:, idx_vmax].set(V_MAX).at[:, idx_safety].set(SAFETY)


def run(model):
    start, goal0 = initial_conditions()
    visibility = jnp.fill_diagonal(jnp.ones((N_HUMANS, N_HUMANS), dtype=bool), jnp.zeros((N_HUMANS,), dtype=bool),
                                   inplace=False)
    if model == "orca":
        # (radius, time_horizon, v_max, neighbor_dist, max_neighbor, safety_space)
        params = shared(orca_utils.get_standard_humans_parameters(N_HUMANS), 0, 2, 5)
        state = jnp.array(np.concatenate([start, np.zeros((N_HUMANS, 2))], axis=1))
        obstacles = jnp.array([[[[1000., 1000.], [1000., 1000.]]]])  # ostacolo fittizio, come nell'esempio di JORCA
        step = lambda s, g: orca_step(s, visibility, g, params, obstacles, DT)  # noqa: E731
    else:
        utils, step_fn = (sfm_utils, sfm_step) if model == "sfm" else (hsfm_utils, hsfm_step)
        # (radius, mass, v_max, tau, Ai, Aw, Bi, Bw, Ci, Cw, Di, Dw, k1, k2, ko, kd, alpha, k_lambda, safety_space)
        params = shared(utils.get_standard_humans_parameters(N_HUMANS), 0, 2, 18)
        if model == "sfm":  # (px, py, vx, vy)
            state = jnp.array(np.concatenate([start, np.zeros((N_HUMANS, 2))], axis=1))
        else:  # (px, py, bvx, bvy, theta, omega): orientati verso l'obiettivo, fermi
            theta = np.arctan2(goal0[:, 1] - start[:, 1], goal0[:, 0] - start[:, 0])
            state = jnp.array(np.concatenate([start, np.zeros((N_HUMANS, 2)), theta[:, None],
                                              np.zeros((N_HUMANS, 1))], axis=1))
        dummy = jnp.array([[[[jnp.nan, jnp.nan], [jnp.nan, jnp.nan]]]])
        obstacles = jnp.stack([dummy for _ in range(N_HUMANS)])
        step = lambda s, g: step_fn(s, visibility, g, params, obstacles, DT)  # noqa: E731

    targets = np.stack([goal0, start])  # andata, ritorno
    leg = np.zeros(N_HUMANS, dtype=int)
    goal = jnp.array(goal0)
    pos, theta = [], []
    for k in range(int(T_END / DT) + 1):
        s = np.asarray(state)
        if k % SAVE_EVERY == 0:
            pos.append(s[:, :2].copy())
            theta.append(s[:, 4].copy() if model == "hsfm" else np.full(N_HUMANS, np.nan))
        reached = np.linalg.norm(s[:, :2] - np.asarray(goal), axis=1) < GOAL_TOL
        if reached.any():
            leg = np.where(reached, 1 - leg, leg)
            goal = jnp.array(targets[leg, np.arange(N_HUMANS)])
        state = step(state, goal)
    return np.array(pos), np.array(theta)


if __name__ == "__main__":
    data = {}
    for m in ("orca", "sfm", "hsfm"):
        p, th = run(m)
        data[f"{m}_pos"], data[f"{m}_theta"] = p, th
        print(m, p.shape)
    start, goal = initial_conditions()
    OUT.parent.mkdir(exist_ok=True)
    np.savez_compressed(OUT, dt=DT * SAVE_EVERY, start=start, goal=goal, radius=RADIUS, **data)
    print("salvato", OUT)
