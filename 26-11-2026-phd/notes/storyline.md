# Storyline

Stato: approvata (20/11/2026)  <!-- diventa "approvata" solo con l'ok dell'autore -->
Durata del talk: 38.5 min (slot di 45 min + domande; obiettivo 35-40)

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
| Il problema | Cos'è la social navigation e perché il RL? | Il RL impara l'interazione, ma in simulazione e in un mondo idealizzato | 6 |
| A. Simulare gli umani | Il modo in cui simuliamo gli umani cambia il robot che addestriamo? | Messaggio 1: il modello di moto umano fa parte del metodo | 10 |
| DIR-SAFE (episodio) | Si può costruire la safety dentro le azioni? | Messaggio 2: ogni azione campionabile resta nei limiti di sicurezza (safety promossa, non garantita) | 5 |
| B. JESSI | Funziona tutto partendo solo da un LiDAR 2D? | Messaggio 3: JESSI mette insieme i pezzi e gira su un robot reale | 12.5 |
| Chiusura | Cosa resta aperto e cosa ricordare? | Limiti, linea futura, i tre messaggi | 2.5 |

## Slide

Fonti: capitoli della tesi in `../PhD-thesis/tex/chapters/`, figure in `../PhD-thesis/tex/figures/`. Le figure dei paper sono pensate per la stampa: quelle segnate con (*) vanno ridisegnate o divise per essere leggibili in slide (fase 5).

| # | Sezione | Titolo-asserzione | Evidenza | Min |
|---|---|---|---|---|
| 1 | Apertura | Learning safe and social robot navigation, from simulated crowds to a real robot | Slide del titolo: nome, University of Siena, Monash Robotics Seminar, 26/11/2026 | 0.5 |
| 2 | Apertura | Robots now share corridors with people, and they must move among them naturally | Video: robot reale nel corridoio, dalla parte finale di `video_demonstration.mp4`. L'autore la giudica poco spettacolare: si prova così e si valuta se cambiare apertura | 1 |
| 3 | Apertura | This talk follows one policy from an idealized simulator to a real corridor | Mappa (diagramma): Problem → A. Simulating humans → DIR-SAFE → B. JESSI → real robot | 1 |
| 4 | Problema | A social robot must reach its goal, avoid collisions and respect personal space | Diagramma dei tre obiettivi, ciascuno con la sua metrica: SR, TtG, SC (Cap. 3.5) | 1.5 |
| 5 | Problema | Classical planners treat people as moving obstacles and can freeze in dense crowds | Diagramma del freezing robot (Cap. 1.1, Cap. 8.1) (*) | 1 |
| 6 | Problema | Reinforcement learning learns the interaction from experience, but only in simulation | Diagramma robot-simulatore-policy (`ch5/robotmodel3.pdf`, `fig:simulation_flow`) (*) | 1.5 |
| 7 | Problema | Human-aware RL policies work well, but in an idealized world | Le quattro semplificazioni: stato esatto degli umani, niente ostacoli statici, niente vincoli cinematici, azioni discrete (Cap. 1, Cap. 8.2). Ognuna verrà ripresa da una sezione | 1.5 |
| 8 | A | Does the way we simulate humans change the robot we train? | Mappa con la sezione A evidenziata | 0.5 |
| 9 | A | Pedestrian models trade efficiency against collision avoidance | ORCA (velocity-based), SFM e HSFM (force-based), con l'HSFM enhanced come nostro contributo (`ch4/hsfm.pdf`, Cap. 4) | 1.5 |
| 10 | A | We crossed three policies with three training models and three testing models | Diagramma del disegno sperimentale: CADRL, LSTM-RL, SARL; ORCA, SFM, HSFM in training e in test; scenari CC, PT, HS; 5 densità, 100 trial (Cap. 5.2) | 1.5 |
| 11 | A | The human model used for testing barely changes the results | Riga superiore di `ch5/cross_train_and_test_env.pdf` (*) | 1 |
| 12 | A | The human model used for training changes them a lot | Riga inferiore della stessa figura: HSFM path length e TtG più bassi, SFM metriche sociali migliori (*) | 1.5 |
| 13 | A | HSFM-trained robots move closer and faster, SFM-trained robots slow down near people | Traiettorie SARL-HS-SFM contro SARL-HS-HSFM dalle stesse condizioni iniziali (`ch5/sarl_over_hsfm.pdf`) | 1.5 |
| 14 | A | The reward also shapes behavior, and a richer reward makes the human model matter less | Figura dal Cap. 6 (`ch6/all_rewards_metrics_hsfm.pdf` o `ch6/r0_train_test_hm.pdf`, da scegliere) | 1.5 |
| 15 | A | The human motion model is part of the method, not a detail of the simulator | Indicazioni pratiche del Cap. 7.2: training con HSFM su più scenari, test con ORCA e SFM, più densità, metriche di navigazione e sociali | 1 |
| 16 | DIR-SAFE | Can safety be built into the actions themselves? | Mappa con DIR-SAFE evidenziato | 0.5 |
| 17 | DIR-SAFE | A differential-drive robot can only choose velocities inside a triangle | Triangolo delle velocità ammissibili (`ch3/action_space.pdf`) | 1 |
| 18 | DIR-SAFE | A Dirichlet policy samples only inside the triangle, so no clipping is needed | Diagramma: gaussiana con clipping contro Dirichlet sul triangolo (Cap. 2.3, Cap. 9.1) | 1 |
| 19 | DIR-SAFE | Shrinking the triangle near obstacles keeps every sampled action within the safety bounds | Bounding in due passi (`ch9/action_space_bounding_1/2.pdf`) (*); in nota: approssimazione conservativa, safety promossa e non garantita | 1.5 |
| 20 | DIR-SAFE | Without retuning, DIR-SAFE crosses a large crowded map more often than DWA | Video `icar25_astar_local_planner_2.mp4`; SR 88% contro 82% con 30 umani; DWA tarato a mano (Cap. 9.4) | 1 |
| 21 | B | Can the robot do all this from a 2D LiDAR alone? | Mappa con la sezione B evidenziata | 0.5 |
| 22 | B | JESSI maps raw LiDAR scans to safe, social actions in one differentiable network | Video: spiegazione di JESSI in simulazione dall'inizio di `video_demonstration.mp4` (traiettoria, point cloud, umani stimati, spazio d'azione); teaser (`ch10/teaser.pdf`) come poster | 1.5 |
| 23 | B | Perception estimates each human with its uncertainty, and the policy also sees the raw scan | Architettura e modulo di percezione (`ch10/journal_jessi_architecture.pdf`, `journal_jessi_perception.pdf`) (*) | 2 |
| 24 | B | The same bounding now runs directly on the LiDAR point cloud | `ch10/action_space_bounding_summary.pdf` (*) | 1 |
| 25 | B | Every method gets the same LiDAR, and human-aware baselines get JESSI's estimates | Scenari e setup del benchmark (`ch3/scenarios.pdf`); baseline model-based, human-aware, E2E (Cap. 10.4) | 1 |
| 26 | B | JESSI has the highest success rate, with the largest margin in unseen layouts | Grafico a barre dell'SR per Setup 1 e 2 con IC al 95% su 10 seed, dalla tabella `tab:jessi_benchmark` (da costruire) | 2 |
| 27 | B | Removing the bounding raises obstacle collisions from 3% to 40% | Barre CR-O: JESSI-MT 3.3% contro JESSI-A1 40.3% (Setup 2); V-E2E 42.5% contro BV-E2E 5.7%; in nota il costo: più timeout | 1.5 |
| 28 | B | Zero-shot on a TurtleBot4, JESSI completes every run and moves more smoothly than DWA | Video del robot reale + `ch10/campaign_metrics.pdf` (SC più alta, jerk più bassi, TtG più alto di DWA); 12.79 ms sul Raspberry Pi | 2 |
| 29 | B | The same network works with other sensors, down to a depth camera on a Loomo | Sintesi della tabella del sensor agnosticism (da 50 a 500 raggi senza riaddestramento; degrada con 20 raggi e FoV di 90°) + foto Loomo (`ch10/loomo_real_world_test.jpg`) | 1 |
| 30 | Chiusura | Safety is promoted, not guaranteed, and decisions still look only one step ahead | Limiti (Cap. 11, 12) e linea futura: predizione delle traiettorie umane e RL model-based | 1.25 |
| 31 | Chiusura | Three things to remember | I tre messaggi del brief, con le icone delle tre sezioni. Resta proiettata durante le domande | 1.25 |

Totale: 38.5 min.

## Backup (non contano nel tempo)

- Definizione delle metriche (SR, TtG, SC, CR-H, CR-O, TR, jerk).
- Struttura a retroazione comune dei modelli di moto (`ch5/humanmodel.pdf`).
- Generalizzazione tra modelli: le politiche addestrate con ORCA generalizzano peggio (`ch5/sarl_hs_cross_env_cc_rates.pdf`).
- Termini della reward (Cap. 6.2).
- Pipeline di training: IL, poi PPO; paradigmi PO, MD, MT (`ch10/journal_jessi_training_paradigms.pdf`).
- Tabella completa del benchmark (Setup 1-3, media ± IC al 95%).
- Setup 3: SARL e CADRL con le sole stime degli umani urtano gli ostacoli (CR-O 40.8% e 55.3%).
- Tabella completa del sensor agnosticism.
- DIR-SAFE contro DWA su 900 episodi per densità (`ch9/dir_safe_vs_dwa.pdf`).

## Citazioni in slide

- Studio sui modelli di moto: Van Der Meer et al., ACM THRI 2025.
- Reward: Van Der Meer et al., Springer 2025.
- DIR-SAFE: Van Der Meer et al., ICAR 2025.
- JESSI, anche per tutti i risultati del Cap. 10: Van Der Meer et al., IROS 2026.

## Da verificare in fase 5

- Video `video_demonstration.mp4`: all'inizio la spiegazione di JESSI in simulazione (slide 22), in fondo il robot reale (slide 2 e 28). Controllare che non riporti scritte sulla sede di pubblicazione. Pesa 28 MB e ha l'audio: va tagliato e compresso.
- Figure segnate con (*): decidere con l'autore se rifarle.
- Le fonti precise del freezing robot (slide 5) e delle quattro semplificazioni (slide 7) nel Cap. 1 e nel Cap. 8.
