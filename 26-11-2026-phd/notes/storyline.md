# Storyline

Stato: approvata (20/11/2026)  <!-- diventa "approvata" solo con l'ok dell'autore -->
Durata del talk: 44.25 min (slot di 45 min + domande; obiettivo 35-40)

## Approfondimenti proposti

**Approfondimento A: modelli di moto umano (THRI, Cap. 4-5 della tesi).** Sostiene il messaggio 1 ed è il risultato più solido della Parte I: si osserva in due setup diversi (Cap. 7). È anche il punto meno ovvio per un pubblico di robotica, che di solito considera il simulatore un dettaglio. L'evidenza si legge al volo: due righe di boxplot (modello di test contro modello di training) e due traiettorie a confronto.

**Approfondimento B: JESSI (Cap. 10).** Sostiene il messaggio 3 e chiude il messaggio 2. Riusa Dirichlet e bounding di DIR-SAFE sulla point cloud, e l'ablation senza bounding (CR-O da 3.3% a 40.3%) è la prova più forte che costruire la safety nelle azioni funziona. Porta al robot reale, che per un lab di robotica è il finale più convincente.

**Episodi brevi:**
- reward shaping (RS, Cap. 6): una slide dentro A, perché modula l'effetto del modello di moto;
- DIR-SAFE (DS, Cap. 9): episodio di circa 5 minuti. Introduce l'idea del messaggio 2 (triangolo, Dirichlet, bounding) a livello intuitivo; JESSI la riprende e l'ablation la verifica;
- simulatori (Social-Navigation-PyEnvs, social-jym): solo nelle note, come motivo per cui gli studi della Parte II sono stati possibili;
- sensor agnosticism e Loomo: una slide dentro B.

Alternativa possibile: approfondire DIR-SAFE (bounding con la sua derivazione) al posto di JESSI, e trattare JESSI in breve. La sconsiglio: il messaggio 3 e il robot reale resterebbero accennati, e il bounding si vede meglio nell'ablation di JESSI che nella derivazione.

## Sezioni

| Sezione | Domanda a cui risponde | Messaggio | Minuti |
|---|---|---|---|
| Apertura | Perché ci interessa e dove andiamo? | Un robot deve muoversi tra le persone; il talk segue il percorso da un simulatore idealizzato a un robot reale | 2.5 |
| Il problema | Cos'è la social navigation e perché il RL? | Il RL impara l'interazione, ma in simulazione e in un mondo idealizzato | 5.5 |
| A. Simulare gli umani | Il modo in cui simuliamo gli umani cambia il robot che addestriamo? | Messaggio 1: il modello di moto umano fa parte del metodo | 10 |
| DIR-SAFE (episodio) | Si può costruire la safety dentro le azioni? | Messaggio 2: ogni azione campionabile resta nei limiti di sicurezza (safety promossa, non garantita) | 7 |
| B. JESSI | Funziona tutto partendo solo da un LiDAR 2D? | Messaggio 3: JESSI mette insieme i pezzi e gira su un robot reale | 15.75 |
| Chiusura | Cosa resta aperto e cosa ricordare? | Limiti, linea futura, i tre messaggi | 2.5 |

## Slide

Fonti: capitoli della tesi in `../PhD-thesis/tex/chapters/`, figure in `../PhD-thesis/tex/figures/`. Le figure dei paper sono pensate per la stampa: quelle segnate con (*) vanno ridisegnate o divise per essere leggibili in slide (fase 5).

| # | Sezione | Titolo-asserzione | Evidenza | Min |
|---|---|---|---|---|
| 1 | Apertura | Learning safe and social robot navigation, from simulated crowds to a real robot | Slide del titolo: nome, University of Siena, Monash Robotics Seminar, 26/11/2026 | 0.5 |
| 2 | Apertura | Robots now share corridors with people, and they must move among them naturally | Video: robot reale nel corridoio, dalla parte finale di `video_demonstration.mp4`. L'autore la giudica poco spettacolare: si prova così e si valuta se cambiare apertura | 1 |
| 3 | Apertura | This talk follows one policy from an idealized simulator to a real corridor | Mappa (diagramma): Problem → A. Simulating humans → DIR-SAFE → B. JESSI → real robot | 1 |
| 4 | Problema | A social robot must reach its goal, avoid collisions and respect personal space | Diagramma dei tre obiettivi, ciascuno con la sua metrica: SR, TtG, SC (Cap. 3.5) | 1.5 |
| 5 | Problema | Classical planners can freeze in dense crowds | Diagramma del freezing robot (Cap. 1.1, Cap. 8.1) (*) | 1 |
| 6 | Problema | Reinforcement learning learns the interaction from experience, but only in simulation | Diagramma robot-simulatore-policy (`ch5/robotmodel3.pdf`, `fig:simulation_flow`) (*) | 1.5 |
| 7 | Problema | Five challenges stand between a policy trained in simulation and a real robot | Cinque sfide (umani simulati, vincoli cinematici, azioni continue, ostacoli statici, percezione delle persone), ciascuna "addressed by" uno studio dell'autore (Cap. 1) | 1.5 |
| 8 | A | Does the way we simulate humans change the robot we train? | Mappa con la sezione A evidenziata | 0.5 |
| 9 | A | Pedestrian models trade efficiency against collision avoidance | Video Manim `human_motion_models.mp4`: ORCA, SFM e HSFM sullo stesso circular crossing con andata e ritorno, simulati con JORCA, JSFM, JHSFM (`animations/hmm_simulate.py`); zoom sulla svolta di 180° | 1.5 |
| 10 | A | We crossed three policies with three training models and three testing models | Diagramma del disegno sperimentale: CADRL, LSTM-RL, SARL; ORCA, SFM, HSFM in training e in test; scenari CC, PT, HS; 5 densità, 100 trial (Cap. 5.2) | 1.5 |
| 11 | A | The human model used for testing barely changes the results | Riga superiore di `ch5/cross_train_and_test_env.pdf` (*) | 1 |
| 12 | A | The human model used for training changes them a lot | Riga inferiore della stessa figura: HSFM path length e TtG più bassi, SFM metriche sociali migliori (*) | 1.5 |
| 13 | A | HSFM-trained robots pass closer and arrive sooner, SFM-trained robots keep their distance | Video Manim (`animations/sarl_episodes.py`): un episodio SARL-HS-SFM contro SARL-HS-HSFM dalle stesse condizioni iniziali (social-jym, seed 70), con il valore delle 81 azioni a ogni passo; a fine episodio time to goal, path length e space compliance | 1.5 |
| 14 | A | Rewarding progress to the goal helps learning, while a time penalty alone slows the robot down | Confronto delle otto reward (`ch6/all_rewards_metrics_hsfm.pdf`) con la tabella dei termini (Cap. 6.3) | 1.5 |
| 15 | A | The human motion model is part of the method, not a detail of the simulator | Indicazioni pratiche del Cap. 7.2: training con HSFM su più scenari, test con ORCA e SFM, più densità, metriche di navigazione e sociali | 1 |
| 16 | DIR-SAFE | Can safety be built into the actions themselves? | Mappa con DIR-SAFE evidenziato | 0.5 |
| 17 | DIR-SAFE | A differential-drive robot can only choose velocities inside a triangle | Triangolo delle velocità ammissibili (`ch3/action_space.pdf`) | 1 |
| 18 | DIR-SAFE | A Gaussian policy needs clipping, so the robot does not execute what it learned | Video Manim `gaussian_clipping.mp4`: campioni e clipping, poi PDF in 3D prima e dopo il clipping (massa esterna sul bordo); illustrazione | 1 |
| 19 | DIR-SAFE | A Dirichlet policy samples only inside the triangle, so no clipping is needed | Video Manim `dirichlet_mapping.mp4`: simplesso, a = V z, PDF della Dirichlet sul triangolo in 3D, alpha, triangolo ristretto; illustrazione (Cap. 2.3, Cap. 9.1) | 1 |
| 20 | DIR-SAFE | Shrinking the triangle near obstacles keeps every sampled action within the safety bounds | Video Manim `action_space_bounding.mp4` (inviluppo, box, fasi 1 e 2, box ristretto); figure statiche in backup; in nota: approssimazione conservativa, safety promossa e non garantita | 1.5 |
| 21 | DIR-SAFE | Without retuning, DIR-SAFE crosses a large crowded map more often than DWA | Video `icar25_astar_local_planner_2.mp4`; SR 88% contro 82% con 30 umani; DWA tarato a mano (Cap. 9.4) | 1 |
| 22 | DIR-SAFE | DIR-SAFE lessons: put the constraints in the action space, and keep them light | Tre lezioni dalle conclusioni del Cap. 9 (Dirichlet, bounding leggero e conservativo, niente ottimizzazione online) | 1 |
| 23 | B | Can the robot do all this from a 2D LiDAR alone? | Mappa con la sezione B evidenziata | 0.5 |
| 24 | B | DIR-SAFE still needs the exact state of every person and a map of the obstacles | Motivazione: cosa assume DIR-SAFE contro cosa ha un robot reale (Cap. 9.5) | 1 |
| 25 | B | JESSI maps raw LiDAR scans to safe, social actions in one differentiable network | Teaser (`ch10/teaser.pdf`), con i contenuti dell'architettura in didascalia e a voce: per ogni umano posizione e velocità con covarianze e score di confidenza; attention nell'actor-critic più lo scan grezzo in parallelo; gradienti attraverso entrambi i moduli. La figura dell'architettura passa nel backup | 2 |
| 26 | B | In simulation, JESSI estimates the people from the scans and keeps only the actions within the bounds | Video: JESSI in simulazione da `video_demonstration.mp4` (5 s - 2:29), con altri scenari e risoluzioni del LiDAR | 1.5 |
| 27 | B | The same bounding now runs directly on the LiDAR point cloud | `ch10/action_space_bounding_summary.pdf` (*) | 1 |
| 28 | B | Three training paradigms decide how much the reward shapes the perception | `ch10/journal_jessi_training_paradigms.pdf` e tre card PO, MD, MT (Cap. 10.3); a voce: si riportano i risultati di MT | 1 |
| 29 | B | Every method gets the same LiDAR, and human-aware baselines get JESSI's estimates | Scenari e setup del benchmark (`ch3/scenarios.pdf`); baseline model-based, human-aware, E2E (Cap. 10.4) | 1 |
| 30 | B | JESSI has the highest success rate in unseen layouts, and is among the best in known ones | Grafico a barre dell'SR per Setup 1 e 2 con IC al 95% su 10 seed, dalla tabella `tab:jessi_benchmark` (da costruire) | 2 |
| 31 | B | Removing the bounding raises obstacle collisions from 3% to 40% | Ablation di JESSI: CR-O con e senza bounding, Setup 1 (1.4% contro 13.6%) e Setup 2 (3.3% contro 40.3%) | 1.5 |
| 32 | B | Zero-shot on a TurtleBot4, JESSI completes every run and moves more smoothly than DWA | Video del robot reale + `ch10/campaign_metrics.pdf` (SC più alta, jerk più bassi, TtG più alto di DWA); 12.79 ms sul Raspberry Pi | 2 |
| 33 | B | The same network works with other sensors, down to a depth camera on a Loomo | Sintesi della tabella del sensor agnosticism (da 50 a 500 raggi senza riaddestramento; degrada con 20 raggi e FoV di 90°) + foto Loomo (`ch10/loomo_real_world_test.jpg`) | 1 |
| 34 | B | JESSI lessons: bound the actions, model the humans, keep the raw geometry | Quattro lezioni dai Cap. 10-11 (bounding, umani espliciti contro E2E, scan grezzo, sensore) | 1.25 |
| 35 | Chiusura | Safety is promoted, not guaranteed, and decisions still look only one step ahead | Limiti (Cap. 11, 12) e linea futura: predizione delle traiettorie umane e RL model-based | 1.25 |
| 36 | Chiusura | Three things to remember | I tre messaggi del brief, con i colori delle tre sezioni, e QR code a GitHub ed email. Resta proiettata durante le domande | 1.25 |

Totale: 43.25 min.

## Backup (non contano nel tempo)

- Definizione delle metriche (SR, TtG, SC, CR-H, CR-O, TR, jerk).
- Struttura a retroazione comune dei modelli di moto (`ch5/humanmodel.pdf`).
- Generalizzazione tra modelli: le politiche addestrate con ORCA generalizzano peggio (`ch5/sarl_hs_cross_env_cc_rates.pdf`).
- Termini della reward (Cap. 6.2).
- Pipeline di training: IL, poi PPO; paradigmi PO, MD, MT (`ch10/journal_jessi_training_paradigms.pdf`).
- Tabella completa del benchmark (Setup 1-3, media ± IC al 95%).
- Setup 3: SARL e CADRL con le sole stime degli umani urtano gli ostacoli (CR-O 40.8% e 55.3%).
- Tabella completa del sensor agnosticism.
- Architettura di JESSI in dettaglio (`ch10/journal_jessi_architecture.pdf`), fusa nel teaser nella scaletta principale.
- DIR-SAFE contro DWA su 900 episodi per densità (`ch9/dir_safe_vs_dwa.pdf`).

## Citazioni in slide

- Studio sui modelli di moto: Van Der Meer et al., ACM THRI 2025.
- Reward: Van Der Meer et al., Springer 2025.
- DIR-SAFE: Van Der Meer et al., ICAR 2025.
- JESSI, anche per tutti i risultati del Cap. 10: Van Der Meer et al., IROS 2026.

## Da verificare in fase 5

- Video `video_demonstration.mp4`: all'inizio la spiegazione di JESSI in simulazione (slide 23), in fondo il robot reale (slide 2 e 29). Controllare che non riporti scritte sulla sede di pubblicazione. Pesa 28 MB e ha l'audio: va tagliato e compresso.
- Figure segnate con (*): decidere con l'autore se rifarle.
- Le fonti precise del freezing robot (slide 5) e delle quattro semplificazioni (slide 7) nel Cap. 1 e nel Cap. 8.
