"""Converte i due episodi registrati da social-jym (examples/test_sarl.py, random_seed = 70) in un npz leggibile senza JAX.

Episodi: stesse condizioni iniziali (circular crossing, 5 persone mosse dall'HSFM), robot olonomo guidato da
SARL-HS-SFM e da SARL-HS-HSFM. I pickle contengono array JAX: serve un ambiente con jax installato.

    <python con jax> 26-11-2026-phd/animations/sarl_extract.py
"""
import pickle
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
out = {}
for m in ("sfm", "hsfm"):
    with open(HERE / "data" / f"episode_sarl_hs_{m}.pkl", "rb") as f:
        d = {k: np.asarray(v) for k, v in pickle.load(f).items()}
    it = d["intermediate_states"]               # (passi, 24, 6 agenti, 6): l'ultimo agente è il robot
    K, J = it.shape[:2]
    dense = it.reshape(K * J, *it.shape[2:])    # sotto-passi uniformi in ogni passo del robot (0.25 s)
    out[f"{m}_pos"] = dense[:, :, :2].astype(np.float32)
    out[f"{m}_theta"] = dense[:, :, 4].astype(np.float32)
    out[f"{m}_actions"] = d["actions"].astype(np.float32)          # (passi, 2): vx, vy nel frame del mondo
    out[f"{m}_values"] = d["action_values"].astype(np.float32)     # (passi, 81)
    out[f"{m}_goal"] = d["robot_goals"][0].astype(np.float32)
out["robot_dt"] = np.float32(0.25)
out["substeps"] = np.int32(J)
out["radius"] = np.float32(0.3)
np.savez_compressed(HERE / "data" / "sarl_episodes.npz", **out)
print({k: v.shape for k, v in out.items()})
