# Brief

> Lo compila l'autore (o l'agente con quello che l'autore ha detto). Ciò che manca si chiede, non si inventa.

- **Evento, luogo, data:** Monash Robotics Seminar, Monash Robotics (Melbourne, Australia), 26/11/2026
- **Pubblico:** membri del laboratorio Monash Robotics: dottorandi, post-doc e professori. POMDP e RL si danno per scontati: PPO non si spiega nel dettaglio. La social navigation va introdotta bene, perché è il problema su cui si basa tutto il lavoro.
- **Durata:** slot di 45 min + domande; obiettivo 35-40 min di talk
- **Lingua:** inglese
- **Tre messaggi da ricordare:**
  1. How we simulate humans shapes the robot we train: the human motion model is part of the method, not a detail of the simulator.
  2. Safety should be built into the actions, not only rewarded: with DIR-SAFE, every action the policy can sample stays within the safety bounds. La safety è promossa, non garantita: non presentarla come garanzia.
  3. Social navigation works from a 2D LiDAR alone: JESSI brings these pieces together and runs on a real robot.
- **Fonti:**
  - note della tesi: `../PhD-thesis/notes/` (in particolare `outline.md`);
  - testo della tesi: `../PhD-thesis/tex/` (capitoli in `tex/chapters/`, figure in `tex/figures/`, macro in `tex/macros.tex`);
  - paper in `../PhD-thesis/sources/`: THRI (`THRI_Comparative/`), RS (`Springer_Reward_Shaping/`), DS (`ICAR25_DIR_SAFE/`), JC (`IROS26_JESSI/`), JJ (la cartella della versione journal di JESSI);
  - video: `~/Videos/Research/` (`icar25_astar_local_planner_2.mp4`, `icar25_dirsafe_parallel_traffic.mp4`, `video_demonstration.mp4`).
- **Vincoli:**
  - JJ (versione journal di JESSI): dati, figure e risultati si possono usare, ma non va detto niente sulla sua pubblicazione (né sede, né stato), né nelle slide, né nelle note del relatore, né nei file di `notes/` (la repo è pubblica). I lavori dell'autore si citano nelle slide che presentano un suo metodo o risultato ("JESSI: Van Der Meer et al., IROS 2026", anche per i risultati presi da JJ), e le sedi compaiono anche sotto le tappe della mappa ricorrente.
  - Safety: "promote safety", mai "guarantee" (messaggio 2).
