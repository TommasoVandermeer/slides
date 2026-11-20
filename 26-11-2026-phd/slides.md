---
theme: default
title: Safe and social robot navigation
author: Tommaso Van Der Meer
info: |
  Monash Robotics Seminar · Melbourne · 26 November 2026
colorSchema: light
routerMode: hash
transition: fade
layout: cover
---

# Learning safe and social robot navigation, from simulated crowds to a real robot

Tommaso Van Der Meer · University of Siena

Monash Robotics Seminar · Melbourne · 26 November 2026

<!--
Thank the hosts. One sentence on who I am: PhD student at the University of Siena, working on reinforcement learning for robots that move among people.

Transition: let me start with what this work is about, in one short video.
-->

---

# Robots now share corridors with people, and they must move among them naturally

<span class="todo">TODO: video of the TurtleBot4 in the corridor (last part of video_demonstration.mp4)</span>

<p class="caption">TODO: what to watch · speed</p>

<!--
This is a small robot in a university corridor. Five people walk towards it. The robot has only a 2D LiDAR, and the policy that drives it was trained only in simulation.

Hospitals, museums, warehouses: robots are entering spaces built for people. Reaching the goal is not enough. They must do it safely and without making people uncomfortable.

Transition: by the end of the talk we will be back in this corridor. First, let me show you the path that leads here.
-->

---
layout: section
---

# This talk follows one policy from an idealized simulator to a real corridor

<RoadMap :current="0" />

<!--
The talk has four stops. First, the problem of social navigation and why we use reinforcement learning. Second, the simulated humans we train with, and how much they matter. Third, DIR-SAFE, where we add the constraints of a real robot and build safety into the actions. Fourth, JESSI, where the robot loses access to the state of the humans and works from a 2D LiDAR, up to the real robot.

Transition: let me start from the problem.
-->

---

# A social robot must reach its goal, avoid collisions and respect personal space

<span class="todo">TODO: diagram of the three objectives, each with its metric (SR, TtG, SC)</span>

<!--
Social navigation asks for three things at the same time. Efficiency: reach the goal, and do it quickly. We measure it with the success rate and the time to goal. Safety: no collisions with walls or people. Social compliance: choose paths that are comfortable for the people around. Our main social metric is space compliance: the percentage of time, in a successful episode, in which the robot stays more than half a meter from every human.

These objectives can be in conflict. A fast robot gets close to people. A very cautious robot may never reach its goal.

Transition: classical planners handle the first two well, but crowds are hard for them.
-->

---

# Classical planners treat people as moving obstacles and can freeze in dense crowds

<span class="todo">TODO: diagram of the freezing robot problem</span>

<div class="cite">Trautman and Krause, IROS 2010</div>

<!--
Model-based planners, like the dynamic window approach or velocity obstacles, work well in many applications. But a crowd is interactive: people react to the robot, and the robot reacts to them. Some planners overestimate the risk of collision, and in a dense crowd every path looks unsafe, so the robot stops. This is the freezing robot problem. Other planners are expensive to compute, and most of them need manual tuning of their parameters.

Transition: this is why learning-based methods, and reinforcement learning in particular, have become popular.
-->

---

# Reinforcement learning learns the interaction from experience, but only in simulation

<span class="todo">TODO: diagram of the training loop between policy, robot and simulated humans (from ch5/robotmodel3.pdf)</span>

<!--
With reinforcement learning, the robot learns the interaction from experience. Once trained, the policy can be used in new scenarios without retuning. But it needs millions of interactions, so in practice it is trained in simulation. The simulated humans move according to a human motion model, and the policy learns to deal with these simulated humans, not with real ones.

So the design effort does not disappear: it moves to the simulator and to the reward function.

Transition: the best-known policies of this kind work well, but in a world that is simpler than the real one.
-->

---

# Human-aware RL policies work well, but in an idealized world

<span class="todo">TODO: the four simplifications, each linked to the section that removes it</span>

<div class="cite">Chen et al., ICRA 2017 · Everett et al., IROS 2018 · Chen et al., ICRA 2019</div>

<!--
CADRL, LSTM-RL and SARL are among the first human-aware RL policies. SARL uses attention to weigh the humans in the crowd. They work well, but they make four simplifications. The robot knows the exact position and velocity of every human. There are no static obstacles. The robot can move in any direction, without kinematic constraints. And it chooses from a small, discrete set of actions.

The rest of the talk removes these simplifications. But first, we keep the idealized world and look at the simulator itself.

Transition: so the first question is about the simulated humans.
-->

---
layout: section
---

# Does the way we simulate humans change the robot we train?

<RoadMap :current="2" />

<!--
Every RL policy for social navigation is trained against simulated pedestrians. The question is how much the choice of the pedestrian model matters.

Transition: let me first show you the models we compared.
-->

---

# Pedestrian models trade efficiency against collision avoidance

<span class="todo">TODO: ORCA, SFM and HSFM side by side (from ch4/hsfm.pdf)</span>

<div class="cite">Van Der Meer et al., ACM THRI 2025</div>

<!--
We use microscopic models, which describe each pedestrian. They are fast, simple and predictable, which is what RL needs. There are two families. Velocity-based models, like ORCA, choose a collision-free velocity close to the preferred one. They are cooperative and favor efficiency. Force-based models, like the social force model, treat each pedestrian as a particle pushed by forces: attraction to the goal, repulsion from other people and from walls. They favor collision avoidance. The headed social force model, HSFM, adds the orientation of the body, so people do not slide sideways or walk backwards.

Our contribution here is an enhanced HSFM, which turns the pedestrian towards the total force and favors mutual avoidance.

Transition: we then trained and tested the policies with each of these models.
-->

---

# We crossed three policies with three training models and three testing models

<span class="todo">TODO: diagram of the experimental design</span>

<div class="cite">Van Der Meer et al., ACM THRI 2025</div>

<!--
We trained CADRL, LSTM-RL and SARL with ORCA, SFM and HSFM pedestrians, in three training settings: circular crossing, parallel traffic, and a hybrid setting that mixes several scenarios. Then we tested every policy with each of the three models, at five crowd densities, with one hundred trials per setting.

SARL gave the best balance between navigation and social metrics, so from now on I will show SARL trained in the hybrid setting.

Transition: here is the first result, about the model used in testing.
-->

---

# The human model used for testing barely changes the results

<span class="todo">TODO: top row of ch5/cross_train_and_test_env.pdf, redrawn for slides</span>

<div class="cite">Van Der Meer et al., ACM THRI 2025</div>

<!--
Each box groups three thousand test episodes. Here the policies are grouped by the human model used in testing, and averaged over the training models. Path length, time to goal, space compliance, acceleration and jerk: the three boxes are very similar in every metric.

Transition: now let me group the same episodes by the model used in training.
-->

---

# The human model used for training changes them a lot

<span class="todo">TODO: bottom row of ch5/cross_train_and_test_env.pdf, redrawn for slides</span>

<div class="cite">Van Der Meer et al., ACM THRI 2025</div>

<!--
Same episodes, grouped by the training model. Now the differences are large. Policies trained with the HSFM have shorter paths and a lower time to goal. Policies trained with the SFM have the best social metrics: higher space compliance, lower acceleration and jerk. Policies trained with ORCA are the least socially compliant, especially in dense crowds.

So the model we choose for training decides a large part of the behavior we get.

Transition: you can also see the difference directly in the trajectories.
-->

---

# HSFM-trained robots move closer and faster, SFM-trained robots slow down near people

<span class="todo">TODO: trajectories of SARL-HS-SFM and SARL-HS-HSFM from the same initial conditions (ch5/sarl_over_hsfm.pdf)</span>

<div class="cite">Van Der Meer et al., ACM THRI 2025</div>

<!--
Same initial conditions, same pedestrians, two policies. The robot trained with the SFM is more conservative: it slows down when it crosses the paths of the humans in the center. The robot trained with the HSFM accepts to get closer to the humans, covers more distance in the same time and reaches the goal earlier, with a smoother path.

Transition: the human model is not the only part of the simulator that shapes the policy. The reward does too.
-->

---

# The reward also shapes behavior, and a richer reward makes the human model matter less

<span class="todo">TODO: figure from Chapter 6 (to choose between ch6/all_rewards_metrics_hsfm.pdf and ch6/r0_train_test_hm.pdf)</span>

<div class="cite">Van Der Meer et al., Springer 2025</div>

<!--
In a second study we used a differential-drive robot and changed the reward. Each reward term does what it is designed for, but it has side effects on other metrics. For example, a penalty on rotations reduces the angular acceleration but makes the paths longer.

The complete reward, which combines progress to the goal, a time penalty and a rotation penalty, gives faster and smoother policies and reduces the variance of the metrics. And it reduces the effect of the human model: with the base reward the training model matters a lot, with the complete reward much less.

Transition: so what should we take from these two studies?
-->

---

# The human motion model is part of the method, not a detail of the simulator

<span class="todo">TODO: practical recipe (train with HSFM in many scenarios; test with ORCA and SFM; several densities; navigation and social metrics)</span>

<!--
This is the first message of the talk. The model used to simulate humans in training shapes the policy much more than the model used in testing. We found this in two different setups, so it is our most consistent result. The reward modulates the effect, so the two have to be chosen together.

In practice: train with the enhanced HSFM in many scenarios, test with other models such as ORCA and the SFM, also in new scenarios, at several crowd densities, and always look at both navigation and social metrics.

One more practical note: we moved from a Python simulator to social-jym, our JAX simulator. A training run went from about a day to a few hours, although the two setups are not identical. This made the next studies possible.

Transition: so far the world was idealized. Now we start to remove the simplifications.
-->

---
layout: section
---

# Can safety be built into the actions themselves?

<RoadMap :current="3" />

<!--
Here we keep the exact state of the humans, but we add two things that every real robot has: kinematic constraints and static obstacles. The question is how to keep the robot safe without relying only on the reward.

Transition: let me start from the actions a differential-drive robot can actually take.
-->

---

# A differential-drive robot can only choose velocities inside a triangle

<span class="todo">TODO: triangle of feasible velocities (ch3/action_space.pdf)</span>

<!--
A differential-drive robot has two wheels, each with a maximum speed. If we translate the wheel limits into linear and angular velocity, we get a triangle: at full linear speed the robot cannot turn, and to turn fast it must slow down. Every action the policy outputs should lie in this triangle.

Transition: the usual way to output continuous actions does not fit this shape.
-->

---

# A Dirichlet policy samples only inside the triangle, so no clipping is needed

<span class="todo">TODO: diagram, Gaussian with clipping against Dirichlet on the triangle</span>

<div class="cite">Van Der Meer et al., ICAR 2025</div>

<!--
Most continuous RL policies use a Gaussian distribution. A Gaussian has unbounded support, so it samples actions outside the triangle, and they have to be clipped. Clipping can make both learning and execution unstable.

A Dirichlet distribution lives on a simplex. We use its sample as the weights of a convex combination of the three vertices of the triangle. So every sample is a feasible action, by construction.

Transition: and once the actions live in a triangle, we can also make that triangle smaller.
-->

---

# Shrinking the triangle near obstacles keeps every sampled action within the safety bounds

<span class="todo">TODO: action space bounding in two steps (ch9/action_space_bounding_1.pdf and _2.pdf), redrawn for slides</span>

<div class="cite">Van Der Meer et al., ICAR 2025</div>

<!--
At each control step we look at all the positions the robot could reach in the next step, and at the obstacles that intersect them. Then we shrink the triangle: first we reduce the maximum linear speed, then the turns to the left and to the right. The result is still a non-empty triangle, so the policy always has an action, and every action it can sample stays within the safety bounds.

This is a conservative approximation, so some safe actions are excluded. It promotes safety, but it is not a guarantee: for example, collisions remain possible in the back of the robot, or with noisy sensor readings.

Transition: does this work in practice?
-->

---

# Without retuning, DIR-SAFE crosses a large crowded map more often than DWA

<span class="todo">TODO: video icar25_astar_local_planner_2.mp4, with SR 88% against 82%</span>

<div class="cite">Van Der Meer et al., ICAR 2025</div>

<!--
DIR-SAFE is trained in simulation with SARL as its starting point, now as an actor-critic. In a first test against the dynamic window approach, over nine hundred episodes per crowd density, we observed no collisions, a slightly higher success rate and a much better space compliance.

Here DIR-SAFE follows waypoints from an A-star planner in a large map, with more than thirty obstacles and thirty people. The policy has never seen this map. It succeeds in eighty-eight percent of the episodes, against eighty-two for DWA, which we had to tune by hand. DIR-SAFE runs in about seven milliseconds.

This is the second message: safety is built into the actions, not only rewarded.

Transition: but DIR-SAFE still knows exactly where every person is. A real robot does not.
-->

---
layout: section
---

# Can the robot do all this from a 2D LiDAR alone?

<RoadMap :current="4" />

<!--
Now we remove the last simplification. The robot has no access to the state of the humans: it only has the scans of a 2D LiDAR, and it must still be feasible, safe and social.

Transition: this is JESSI.
-->

---

# JESSI maps raw LiDAR scans to safe, social actions in one differentiable network

<span class="todo">TODO: video, JESSI explained in simulation (first part of video_demonstration.mp4), with ch10/teaser.pdf as poster</span>

<div class="cite">Van Der Meer et al., IROS 2026</div>

<!--
JESSI takes a short stack of LiDAR scans. A perception module estimates where the humans are and how they move. An actor-critic uses these estimates to choose the action. Everything is one network, and it is differentiable end to end.

In the video, on the left you see the scene and the scans, in the middle the point cloud and the humans estimated by the network, on the right the action space, shrunk by the bounding.

Transition: let me open the two modules.
-->

---

# Perception estimates each human with its uncertainty, and the policy also sees the raw scan

<span class="todo">TODO: architecture and perception module (ch10/journal_jessi_architecture.pdf, journal_jessi_perception.pdf), redrawn for slides</span>

<div class="cite">Van Der Meer et al., IROS 2026</div>

<!--
The perception module looks at the stack of scans and outputs, for each human, a position and a velocity with their covariances, and a confidence score. This layer is readable: you can look at what the robot believes about the people around it. This makes the policy partly interpretable.

The actor-critic uses attention over these estimates, like SARL. But it also receives the latest raw scan, in parallel. This gives the policy a geometric view of the scene that does not depend on recognizing people, which helps when the perception makes mistakes.

Because everything is differentiable, perception and policy can be trained together.

Transition: the safety part comes from DIR-SAFE.
-->

---

# The same bounding now runs directly on the LiDAR point cloud

<span class="todo">TODO: action space bounding on the point cloud (ch10/action_space_bounding_summary.pdf), redrawn for slides</span>

<div class="cite">Van Der Meer et al., IROS 2026</div>

<!--
In DIR-SAFE the bounding used a map of the obstacles. In JESSI it uses the LiDAR points directly. Same idea: we look at the positions the robot could reach in the next step, and we shrink the triangle when LiDAR points fall inside them. The Dirichlet output stays the same, so every action is feasible and stays within the bounds.

Transition: we then compared JESSI with many baselines, in a fair setting.
-->

---

# Every method gets the same LiDAR, and human-aware baselines get JESSI's estimates

<span class="todo">TODO: benchmark scenarios and setups (ch3/scenarios.pdf), with the list of baselines</span>

<div class="cite">Van Der Meer et al., IROS 2026</div>

<!--
Three setups, twelve hundred episodes each, with one to ten humans and one to five obstacles. Setup 1 uses the training scenarios with new initial conditions. Setup 2 uses scenarios never seen in training. Setup 3 uses circular obstacles that look like people standing still.

Baselines: model-based planners, DWA, MPPI and DRA-MPPI; human-aware policies, CADRL, SARL, SARL-star and DIR-SAFE; and end-to-end policies. No real robot knows the exact state of the humans, so the human-aware baselines receive the estimates of JESSI's perception. Every trained policy is trained with ten random seeds.

Transition: here is the success rate.
-->

---

# JESSI has the highest success rate, with the largest margin in unseen layouts

<span class="todo">TODO: bar chart of SR in Setups 1 and 2, mean and 95% CI over 10 seeds (from tab:jessi_benchmark)</span>

<div class="cite">Van Der Meer et al., IROS 2026</div>

<!--
In the scenarios seen in training, the three JESSI variants and the bounded end-to-end baseline have the highest success rate. In the unseen scenarios of Setup 2, JESSI trained with the multi-task paradigm reaches 89.6 percent. DIR-SAFE, with JESSI's perception, is in the same range. SARL-star reaches 82.7, the bounded end-to-end policy 78.6, and the model-based planners at most 77.7. The space compliance of JESSI is comparable to that of the human-aware policies.

Note the confidence intervals: across seeds, the variability is much larger in unseen scenarios. So it is important to train several seeds and report them together.

Transition: which part of JESSI makes the difference on obstacles?
-->

---

# Removing the bounding raises obstacle collisions from 3% to 40%

<span class="todo">TODO: bar chart of CR-O, JESSI-MT 3.3% against JESSI without bounding 40.3%; V-E2E 42.5% against BV-E2E 5.7% (Setup 2)</span>

<div class="cite">Van Der Meer et al., IROS 2026</div>

<!--
This is the clearest evidence for the second message. If we retrain JESSI without the bounding, collisions with obstacles in the unseen scenarios go from 3.3 to 40.3 percent. And if we add the Dirichlet output and the bounding to a plain end-to-end policy, its collisions go from 42.5 to 5.7 percent.

There is a cost: the bounding is conservative, so the robot times out more often and its space compliance drops a little. But the trade is clearly worth it.

Transition: now, the real robot.
-->

---

# Zero-shot on a TurtleBot4, JESSI completes every run and moves more smoothly than DWA

<span class="todo">TODO: video of the TurtleBot4 runs with ch10/campaign_metrics.pdf</span>

<div class="cite">Van Der Meer et al., IROS 2026</div>

<!--
We deployed JESSI on a TurtleBot4 without any retraining. The robot crosses a corridor to a goal ten meters ahead, while five people walk in the opposite direction. Ten runs for JESSI and ten for DWA.

Both complete every run without collisions. DWA is faster to the goal, but JESSI keeps more space from people and moves more smoothly, with lower linear and angular jerk. DWA reacts to people; JESSI anticipates them. It runs in 12.8 milliseconds on the Raspberry Pi of the robot.

Transition: the same network also works with other sensors.
-->

---

# The same network works with other sensors, down to a depth camera on a Loomo

<span class="todo">TODO: summary of the sensor tests and photo of the Loomo (ch10/loomo_real_world_test.jpg)</span>

<div class="cite">Van Der Meer et al., IROS 2026</div>

<!--
JESSI was trained with one hundred beams. Without retraining, it keeps its performance from fifty to five hundred beams, and with a shorter or longer history of scans. It degrades with only twenty beams, where thin obstacles fall between beams, and with a ninety-degree field of view.

On the real TurtleBot we used two hundred beams. We also ran it on a Loomo, which has only a depth camera: we convert the depth image into a 2D scan. That test was only qualitative.

This is the third message: social navigation works from a 2D LiDAR alone.

Transition: before closing, what is still missing.
-->

---

# Safety is promoted, not guaranteed, and decisions still look only one step ahead

<span class="todo">TODO: limits and the next step (trajectory prediction and model-based RL)</span>

<!--
Three limits. First, the bounding promotes safety but does not guarantee it: collisions remain possible behind the robot, with noisy readings, or with scans that are too sparse. Second, the simulated humans are still disks driven by one model, which we have not validated on real data, and our real-world tests are limited to one scenario. Third, and most important, the policy decides one step at a time. It does not predict where people will be in a few seconds.

The next step is to add long-term prediction of human trajectories inside the differentiable pipeline, which opens the way to model-based RL and to planning over a longer horizon.

Transition: let me close with three things to remember.
-->

---

# Three things to remember

<span class="todo">TODO: the three messages, with the colors of the three sections</span>

<!--
One: how we simulate humans shapes the robot we train. The human motion model is part of the method.
Two: safety should be built into the actions, not only rewarded. With Dirichlet actions and bounding, every action the policy can sample stays within the safety bounds.
Three: social navigation works from a 2D LiDAR alone. JESSI brings these pieces together and runs on a real robot.

Thank you. I am happy to take questions.
-->

---
layout: section
---

# Backup

<!--
Backup slides for expected questions. Not counted in the talk time.
-->

---

# Evaluation metrics

<span class="todo">TODO: definitions of SR, TtG, SC, CR-H, CR-O, TR, linear and angular jerk</span>

<!--
Definitions from Chapter 3.5 of the thesis.
-->

---

# Velocity-based and force-based models share one feedback structure

<span class="todo">TODO: ch5/humanmodel.pdf</span>

<div class="cite">Van Der Meer et al., ACM THRI 2025</div>

<!--
The two families differ only in the state variables.
-->

---

# Policies trained with ORCA generalize worst to other human models

<span class="todo">TODO: ch5/sarl_hs_cross_env_cc_rates.pdf</span>

<div class="cite">Van Der Meer et al., ACM THRI 2025</div>

<!--
Space compliance and acceleration, normalized by the performance with the training model.
-->

---

# The reward is a weighted sum of four terms

<span class="todo">TODO: reward terms from Chapter 6.2</span>

<div class="cite">Van Der Meer et al., Springer 2025</div>

<!--
Base reward, progress to goal, time penalty, rotation penalty.
-->

---

# JESSI is trained with imitation learning, then PPO, with three paradigms

<span class="todo">TODO: training pipeline and paradigms PO, MD, MT (ch10/journal_jessi_training_paradigms.pdf)</span>

<div class="cite">Van Der Meer et al., IROS 2026</div>

<!--
Training pipeline and the three paradigms.
-->

---

# Full benchmark results

<span class="todo">TODO: full table, Setups 1-3, mean and 95% CI (from tab:jessi_benchmark)</span>

<div class="cite">Van Der Meer et al., IROS 2026</div>

<!--
All policies and metrics.
-->

---

# With only the estimated humans, SARL and CADRL hit obstacles that look like people

<span class="todo">TODO: Setup 3, CR-O of SARL 40.8% and CADRL 55.3%</span>

<div class="cite">Van Der Meer et al., IROS 2026</div>

<!--
Why a geometric channel independent of the perception matters.
-->

---

# JESSI keeps its performance across LiDAR configurations

<span class="todo">TODO: full sensor agnosticism table</span>

<div class="cite">Van Der Meer et al., IROS 2026</div>

<!--
Number of beams, number of scans and field of view.
-->

---

# DIR-SAFE is more socially compliant than DWA at every crowd density

<span class="todo">TODO: ch9/dir_safe_vs_dwa.pdf</span>

<div class="cite">Van Der Meer et al., ICAR 2025</div>

<!--
Nine hundred episodes per density, no collisions.
-->
