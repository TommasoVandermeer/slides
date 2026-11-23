"""Stile comune dei video Manim dei deck: stessi colori e fondo delle slide.

Uso in una scena (dalla radice della repo):
    import sys; sys.path.insert(0, "scripts")
    from manim_style import *

Render (1080p, 30 fps, sfondo bianco), con l'mp4 copiato in public/videos del deck:
    .venv-manim/bin/manim -qh --fps 30 <deck>/animations/<file>.py <Scena> --media_dir /tmp/manim
"""
from manim import config, WHITE

# Palette Okabe-Ito, la stessa di style.css dei deck
C_PROBLEM = "#555555"   # neutro: il problema, il robot generico
C_HM = "#E69F00"        # modelli di moto umano
C_DIRSAFE = "#0072B2"   # DIR-SAFE
C_JESSI = "#009E73"     # JESSI
C_BASELINE = "#D55E00"  # baseline, azioni non vincolate
# Spazio d'azione: rosso per le azioni ammissibili originali, verde per quelle ristrette dal bounding,
# come nelle figure della tesi e nei video di DIR-SAFE e JESSI
C_FEASIBLE = "#D62728"
C_RESTRICTED = "#2CA02C"
INK = "#222222"         # testo e ostacoli
MUTED = "#888888"       # assi e elementi secondari
FONT = "Inter"          # font sans installato; le slide usano Nunito Sans

config.background_color = WHITE
config.frame_rate = 30
