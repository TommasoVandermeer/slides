---
theme: default
title: Safe social robot navigation
author: Tommaso Van Der Meer
info: |
  Monash Robotics Seminar · Melbourne · 26 November 2026
colorSchema: light
routerMode: hash
transition: fade
layout: cover
---

<img src="/logos/unisi_oriz_col.png" alt="Università di Siena" class="absolute top-8 left-14 h-16" />

# Learning safe and social robot navigation, from simulated crowds to a real robot

Tommaso Van Der Meer · University of Siena

Monash Robotics Seminar · Melbourne · 26 November 2026

<!--
Thank the hosts. One sentence on who I am: PhD student at the University of Siena, working on reinforcement learning for robots that move among people.

Transition: let me start with what this work is about, in one short video.
-->

---

# Robots now share corridors with people, and they must move among them naturally

<div class="flex justify-center items-center gap-10 mt-2">
<SlidevVideo autoplay loop muted controls poster="/videos/turtlebot_corridor.jpg" printPoster="/videos/turtlebot_corridor.jpg" class="h-80">
  <source src="/videos/turtlebot_corridor.mp4" type="video/mp4" />
</SlidevVideo>
<div class="text-xl leading-relaxed w-80">A TurtleBot4 with a 2D LiDAR.<br>Five people walking towards it.<br>The policy was trained only in simulation.</div>
</div>

<p class="caption">2×</p>

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

<div class="cards">
  <div class="card"><h3>Efficiency</h3><p>Reach the goal, and do it quickly</p><span class="tag">success rate · time to goal</span></div>
  <div class="card"><h3>Safety</h3><p>No collisions with people or obstacles</p><span class="tag">collision rates</span></div>
  <div class="card"><h3>Social compliance</h3><p>Keep personal space, move smoothly</p><span class="tag">space compliance · jerk</span></div>
</div>

<p class="caption mt-8">Space compliance: share of the time the robot stays more than 0.5 m from every human</p>

<!--
Social navigation asks for three things at the same time. Efficiency: reach the goal, and do it quickly. We measure it with the success rate and the time to goal. Safety: no collisions with walls or people. Social compliance: choose paths that are comfortable for the people around. Our main social metric is space compliance: the percentage of time, in a successful episode, in which the robot stays more than half a meter from every human.

These objectives can be in conflict. A fast robot gets close to people. A very cautious robot may never reach its goal.

Transition: classical planners handle the first two well, but crowds are hard for them.
-->

---

# Classical planners treat people as moving obstacles and can freeze in dense crowds

<img src="/figures/freezing_robot.svg" class="mx-auto h-72" alt="A robot facing a crowd whose predicted motion covers every path to the goal" />

<p class="caption">When the predicted motion of the crowd covers every path, the planner finds none and the robot stops</p>

<div class="cite">Trautman and Krause, IROS 2010</div>

<!--
Model-based planners, like the dynamic window approach or velocity obstacles, work well in many applications. But a crowd is interactive: people react to the robot, and the robot reacts to them. Some planners overestimate the risk of collision, and in a dense crowd every path looks unsafe, so the robot stops. This is the freezing robot problem. Other planners are expensive to compute, and most of them need manual tuning of their parameters.

Transition: this is why learning-based methods, and reinforcement learning in particular, have become popular.
-->

---

# Reinforcement learning learns the interaction from experience, but only in simulation

<img src="/figures/robotmodel3.png" class="mx-auto h-80" alt="Closed loop between the robot policy and the simulated humans" />

<p class="caption">During training, the policy only meets the humans of the lower loop: a model of human motion</p>

<!--
With reinforcement learning, the robot learns the interaction from experience. Once trained, the policy can be used in new scenarios without retuning. But it needs millions of interactions, so in practice it is trained in simulation. The simulated humans move according to a human motion model, and the policy learns to deal with these simulated humans, not with real ones.

So the design effort does not disappear: it moves to the simulator and to the reward function.

Transition: the best-known policies of this kind work well, but in a world that is simpler than the real one.
-->

---

# Human-aware RL policies work well, but in an idealized world

<div class="cards" style="--n: 4">
  <div class="card" style="--c: var(--c-jessi)"><h3>Exact human state</h3><p>Position and velocity of every person are known</p><span class="tag">removed by JESSI</span></div>
  <div class="card" style="--c: var(--c-dirsafe)"><h3>No static obstacles</h3><p>Only people in the scene</p><span class="tag">removed by DIR-SAFE</span></div>
  <div class="card" style="--c: var(--c-dirsafe)"><h3>No kinematic constraints</h3><p>The robot can move in any direction</p><span class="tag">removed by DIR-SAFE</span></div>
  <div class="card" style="--c: var(--c-dirsafe)"><h3>Few discrete actions</h3><p>A small set to choose from</p><span class="tag">removed by DIR-SAFE</span></div>
</div>

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

<div class="cards" style="--n: 4; --c: var(--c-hm)">
  <div class="card"><h3>ORCA</h3><p>Velocity-based: picks a collision-free velocity</p><span class="tag">efficiency</span></div>
  <div class="card"><h3>SFM</h3><p>Force-based: people as particles pushed by forces</p><span class="tag">collision avoidance</span></div>
  <div class="card"><h3>HSFM</h3><p>SFM plus body orientation: no sideways steps</p><span class="tag">more realistic motion</span></div>
  <div class="card"><h3>Enhanced HSFM</h3><p>Turns towards the total force (ours)</p><span class="tag">mutual avoidance</span></div>
</div>

<div class="cite">Van Der Meer et al., ACM THRI 2025</div>

<!--
We use microscopic models, which describe each pedestrian. They are fast, simple and predictable, which is what RL needs. There are two families. Velocity-based models, like ORCA, choose a collision-free velocity close to the preferred one. They are cooperative and favor efficiency. Force-based models, like the social force model, treat each pedestrian as a particle pushed by forces: attraction to the goal, repulsion from other people and from walls. They favor collision avoidance. The headed social force model, HSFM, adds the orientation of the body, so people do not slide sideways or walk backwards.

Our contribution here is an enhanced HSFM, which turns the pedestrian towards the total force and favors mutual avoidance.

Transition: we then trained and tested the policies with each of these models.
-->

---

# We crossed three policies with three training models and three testing models

<div class="flex justify-center items-stretch gap-3 mt-8 text-center">
  <div class="card" style="--c: var(--c-problem)"><h3>3 policies</h3><p>CADRL<br>LSTM-RL<br>SARL</p></div>
  <div class="self-center text-3xl opacity-60">×</div>
  <div class="card" style="--c: var(--c-hm)"><h3>3 training models</h3><p>ORCA<br>SFM<br>HSFM</p></div>
  <div class="self-center text-3xl opacity-60">×</div>
  <div class="card" style="--c: var(--c-problem)"><h3>3 training settings</h3><p>circular crossing<br>parallel traffic<br>hybrid (both and more)</p></div>
  <div class="self-center text-3xl opacity-60">→</div>
  <div class="card" style="--c: var(--c-hm)"><h3>Test</h3><p>3 testing models<br>5 crowd densities<br>100 trials each</p></div>
</div>

<div class="cite">Van Der Meer et al., ACM THRI 2025</div>

<!--
We trained CADRL, LSTM-RL and SARL with ORCA, SFM and HSFM pedestrians, in three training settings: circular crossing, parallel traffic, and a hybrid setting that mixes several scenarios. Then we tested every policy with each of the three models, at five crowd densities, with one hundred trials per setting.

SARL gave the best balance between navigation and social metrics, so from now on I will show SARL trained in the hybrid setting.

Transition: here is the first result, about the model used in testing.
-->

---

# The human model used for testing barely changes the results

<img src="/figures/hm_test_row.png" class="mx-auto w-full mt-6" alt="Boxplots of navigation and social metrics grouped by testing human model" />

<p class="caption">Policies grouped by the human model used in testing: the three boxes look alike in every metric</p>

<div class="cite">Van Der Meer et al., ACM THRI 2025</div>

<!--
Each box groups three thousand test episodes. Here the policies are grouped by the human model used in testing, and averaged over the training models. Path length, time to goal, space compliance, acceleration and jerk: the three boxes are very similar in every metric.

Transition: now let me group the same episodes by the model used in training.
-->

---

# The human model used for training changes them a lot

<img src="/figures/hm_train_row.png" class="mx-auto w-full mt-6" alt="Boxplots of navigation and social metrics grouped by training human model" />

<p class="caption">Same episodes, grouped by training model: HSFM gives shorter paths and times, SFM the best space compliance</p>

<div class="cite">Van Der Meer et al., ACM THRI 2025</div>

<!--
Same episodes, grouped by the training model. Now the differences are large. Policies trained with the HSFM have shorter paths and a lower time to goal. Policies trained with the SFM have the best social metrics: higher space compliance, lower acceleration and jerk. Policies trained with ORCA are the least socially compliant, especially in dense crowds.

So the model we choose for training decides a large part of the behavior we get.

Transition: you can also see the difference directly in the trajectories.
-->

---

# HSFM-trained robots move closer and faster, SFM-trained robots slow down near people

<img src="/figures/sarl_over_hsfm.png" class="mx-auto h-80" alt="Trajectories of two SARL policies from the same initial conditions" />

<p class="caption">Red circles: the robot every 3 s. Left: trained with SFM, it slows down in the center. Right: trained with HSFM</p>

<div class="cite">Van Der Meer et al., ACM THRI 2025</div>

<!--
Same initial conditions, same pedestrians, two policies. The robot trained with the SFM is more conservative: it slows down when it crosses the paths of the humans in the center. The robot trained with the HSFM accepts to get closer to the humans, covers more distance in the same time and reaches the goal earlier, with a smoother path.

Transition: the human model is not the only part of the simulator that shapes the policy. The reward does too.
-->

---

# The reward also shapes behavior, and a richer reward makes the human model matter less

<img src="/figures/r0_r7_ttg_angacc.png" class="mx-auto h-76" alt="Time to goal and angular acceleration for base and complete rewards, trained with SFM and HSFM" />

<p class="caption">R0: base reward, R7: complete reward. With R7 the SFM and HSFM bars almost coincide</p>

<div class="cite">Van Der Meer et al., Springer 2025</div>

<!--
In a second study we used a differential-drive robot and changed the reward. Each reward term does what it is designed for, but it has side effects on other metrics. For example, a penalty on rotations reduces the angular acceleration but makes the paths longer.

The complete reward, which combines progress to the goal, a time penalty and a rotation penalty, gives faster and smoother policies and reduces the variance of the metrics. And it reduces the effect of the human model: with the base reward the training model matters a lot, with the complete reward much less.

Transition: so what should we take from these two studies?
-->

---

# The human motion model is part of the method, not a detail of the simulator

<div class="cards" style="--n: 2; --c: var(--c-hm)">
  <div class="card"><h3>Train</h3><p>with the enhanced HSFM<br>in many scenarios<br>choosing the reward together with the human model</p></div>
  <div class="card"><h3>Test</h3><p>with other models too (ORCA, SFM)<br>in new scenarios, at several crowd densities<br>on both navigation and social metrics</p></div>
</div>

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

<img src="/figures/action_space.png" class="mx-auto w-4/5 mt-6" alt="Triangular set of feasible linear and angular velocities" />

<p class="caption">Full linear speed means no turning; turning fast means slowing down</p>

<!--
A differential-drive robot has two wheels, each with a maximum speed. If we translate the wheel limits into linear and angular velocity, we get a triangle: at full linear speed the robot cannot turn, and to turn fast it must slow down. Every action the policy outputs should lie in this triangle.

Transition: the usual way to output continuous actions does not fit this shape.
-->

---

# A Gaussian policy needs clipping, so the robot does not execute what it learned

<SlidevVideo autoplay muted controls poster="/videos/gaussian_clipping.jpg" printPoster="/videos/gaussian_clipping.jpg" class="mx-auto h-80">
  <source src="/videos/gaussian_clipping.mp4" type="video/mp4" />
</SlidevVideo>

<p class="caption">Illustration · Gaussian policy: the mass outside the triangle ends up on its border</p>

<div class="cite">Van Der Meer et al., ICAR 2025</div>

<!--
Most continuous RL policies use a Gaussian distribution. A Gaussian has unbounded support, so some of its samples fall outside the triangle, and they have to be clipped onto the border. Look at the density: here almost half of the probability mass is outside. Clipping does not remove it, it piles it onto the edges and into the corner. So the actions the robot executes do not follow the distribution the policy is optimizing, and this mismatch makes learning worse.

Transition: we need a distribution that cannot leave the triangle.
-->

---

# A Dirichlet policy samples only inside the triangle, so no clipping is needed

<SlidevVideo autoplay muted controls poster="/videos/dirichlet_mapping.jpg" printPoster="/videos/dirichlet_mapping.jpg" class="mx-auto h-80">
  <source src="/videos/dirichlet_mapping.mp4" type="video/mp4" />
</SlidevVideo>

<p class="caption">Illustration · Dirichlet policy: a = V z, every sample and all the density inside the triangle</p>

<div class="cite">Van Der Meer et al., ICAR 2025</div>

<!--
A Dirichlet distribution lives on the simplex: three non-negative weights that sum to one. We use them as the weights of a convex combination of the three vertices of the triangle, a equals V z. So every sample is a feasible action by construction, and all the density stays inside the triangle, with nothing on the border. The policy outputs the concentration parameters alpha, which decide where the actions are and how spread out they are. At deployment we use the mean action. And if the triangle gets smaller, the same output still works.

Transition: and once the actions live in a triangle, we can also make that triangle smaller.
-->

---

# Shrinking the triangle near obstacles keeps every sampled action within the safety bounds

<SlidevVideo autoplay muted controls poster="/videos/action_space_bounding.jpg" printPoster="/videos/action_space_bounding.jpg" class="mx-auto h-80">
  <source src="/videos/action_space_bounding.mp4" type="video/mp4" />
</SlidevVideo>

<p class="caption">Red: every action and where it can take the robot · Green: what is left after the two stages</p>

<div class="cite">Van Der Meer et al., ICAR 2025</div>

<!--
Let me show it step by step. On the right is the triangle of actions, on the left the robot and a wall. Each action in the triangle moves the robot somewhere in the next step: together, these positions form the red region, and part of it crosses the wall.

We take the bounding box of this region and split it into four boxes: front, left, right and back. In the first stage we look at the front box and reduce the maximum linear speed until the box stops at the wall. In the second stage we look at the side boxes and reduce the turns towards the wall. On the other side there is no obstacle, so nothing changes there.

What is left is a smaller triangle. It is never empty, so the policy always has an action, and every action it can sample keeps the robot clear of the wall. The computation is light: a few box intersections per control step.

This is a conservative approximation, so some safe actions are excluded. It promotes safety, but it is not a guarantee: for example, collisions remain possible in the back of the robot, or with noisy sensor readings.

Transition: does this work in practice?
-->

---

# Without retuning, DIR-SAFE crosses a large crowded map more often than DWA

<div class="flex justify-center items-center gap-8 mt-2">
<SlidevVideo autoplay loop muted controls poster="/videos/dirsafe_long_nav.jpg" printPoster="/videos/dirsafe_long_nav.jpg" class="h-72">
  <source src="/videos/dirsafe_long_nav.mp4" type="video/mp4" />
</SlidevVideo>
<div class="flex flex-col gap-6">
  <div class="stat" style="--c: var(--c-dirsafe)"><div class="num">88%</div><div class="lbl">DIR-SAFE success rate</div></div>
  <div class="stat" style="--c: var(--c-baseline)"><div class="num">82%</div><div class="lbl">DWA, tuned by hand</div></div>
</div>
</div>

<p class="caption">Waypoints from A* · 30 people · a map never seen in training · 2×</p>

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

<SlidevVideo autoplay loop muted controls poster="/videos/jessi_sim.jpg" printPoster="/videos/jessi_sim.jpg" class="mx-auto h-80">
  <source src="/videos/jessi_sim.mp4" type="video/mp4" />
</SlidevVideo>

<p class="caption">Left: scans and estimated humans · Right: action space after bounding · 2×</p>

<div class="cite">Van Der Meer et al., IROS 2026</div>

<!--
JESSI takes a short stack of LiDAR scans. A perception module estimates where the humans are and how they move. An actor-critic uses these estimates to choose the action. Everything is one network, and it is differentiable end to end.

In the video, on the left you see the scene and the scans, in the middle the point cloud and the humans estimated by the network, on the right the action space, shrunk by the bounding.

Transition: let me open the two modules.
-->

---

# Perception estimates each human with its uncertainty, and the policy also sees the raw scan

<img src="/figures/journal_jessi_architecture.png" class="mx-auto w-4/5 mt-10" alt="Perception module feeding an actor-critic, with the latest scan in parallel" />

<p class="caption mt-6">X(k): stack of LiDAR scans · H(k): estimated humans, with covariances · O(k): latest raw scan</p>

<div class="cite">Van Der Meer et al., IROS 2026</div>

<!--
The perception module looks at the stack of scans and outputs, for each human, a position and a velocity with their covariances, and a confidence score. This layer is readable: you can look at what the robot believes about the people around it. This makes the policy partly interpretable.

The actor-critic uses attention over these estimates, like SARL. But it also receives the latest raw scan, in parallel. This gives the policy a geometric view of the scene that does not depend on recognizing people, which helps when the perception makes mistakes.

Because everything is differentiable, perception and policy can be trained together.

Transition: the safety part comes from DIR-SAFE.
-->

---

# The same bounding now runs directly on the LiDAR point cloud

<img src="/figures/action_space_bounding_summary.png" class="mx-auto h-80" alt="Action space bounding computed on the LiDAR points" />

<p class="caption">Blue crosses: LiDAR points. Red: unbounded; green: bounded displacements and action space</p>

<div class="cite">Van Der Meer et al., IROS 2026</div>

<!--
In DIR-SAFE the bounding used a map of the obstacles. In JESSI it uses the LiDAR points directly. Same idea: we look at the positions the robot could reach in the next step, and we shrink the triangle when LiDAR points fall inside them. The Dirichlet output stays the same, so every action is feasible and stays within the bounds.

Transition: we then compared JESSI with many baselines, in a fair setting.
-->

---

# Every method gets the same LiDAR, and human-aware baselines get JESSI's estimates

<img src="/figures/scenarios.png" class="mx-auto h-64" alt="The navigation scenarios used in the benchmark" />

<p class="caption">Model-based: DWA, MPPI, DRA-MPPI · Human-aware: CADRL, SARL, SARL*, DIR-SAFE · End-to-end: V-E2E, BV-E2E</p>

<div class="cite">Van Der Meer et al., IROS 2026</div>

<!--
Three setups, twelve hundred episodes each, with one to ten humans and one to five obstacles. Setup 1 uses the training scenarios with new initial conditions. Setup 2 uses scenarios never seen in training. Setup 3 uses circular obstacles that look like people standing still.

Baselines: model-based planners, DWA, MPPI and DRA-MPPI; human-aware policies, CADRL, SARL, SARL-star and DIR-SAFE; and end-to-end policies. No real robot knows the exact state of the humans, so the human-aware baselines receive the estimates of JESSI's perception. Every trained policy is trained with ten random seeds.

Transition: here is the success rate.
-->

---

# JESSI has the highest success rate in unseen layouts, and is among the best in known ones

<img src="/figures/benchmark_sr.svg" class="mx-auto h-84" alt="Success rate of JESSI and the baselines in known and unseen layouts" />

<p class="caption">JESSI: multi-task training. Mean and 95% confidence interval over 10 seeds; model-based planners have no interval</p>

<div class="cite">Van Der Meer et al., IROS 2026</div>

<!--
In the scenarios seen in training, the three JESSI variants and the bounded end-to-end baseline have the highest success rate. In the unseen scenarios of Setup 2, JESSI trained with the multi-task paradigm reaches 89.6 percent. DIR-SAFE, with JESSI's perception, is in the same range. SARL-star reaches 82.7, the bounded end-to-end policy 78.6, and the model-based planners at most 77.7. The space compliance of JESSI is comparable to that of the human-aware policies.

Note the confidence intervals: across seeds, the variability is much larger in unseen scenarios. So it is important to train several seeds and report them together.

Transition: which part of JESSI makes the difference on obstacles?
-->

---

# Removing the bounding raises obstacle collisions from 3% to 40%

<img src="/figures/bounding_ablation.svg" class="mx-auto h-80" alt="Collisions with obstacles with and without the action space bounding" />

<p class="caption">Unseen layouts (Setup 2). Green: with Dirichlet actions and bounding · Red: without</p>

<div class="cite">Van Der Meer et al., IROS 2026</div>

<!--
This is the clearest evidence for the second message. If we retrain JESSI without the bounding, collisions with obstacles in the unseen scenarios go from 3.3 to 40.3 percent. And if we add the Dirichlet output and the bounding to a plain end-to-end policy, its collisions go from 42.5 to 5.7 percent.

There is a cost: the bounding is conservative, so the robot times out more often and its space compliance drops a little. But the trade is clearly worth it.

Transition: now, the real robot.
-->

---

# Zero-shot on a TurtleBot4, JESSI completes every run and moves more smoothly than DWA

<div class="flex justify-center items-center gap-8 mt-2">
<SlidevVideo autoplay loop muted controls poster="/videos/turtlebot_corridor.jpg" printPoster="/videos/turtlebot_corridor.jpg" class="h-84">
  <source src="/videos/turtlebot_corridor.mp4" type="video/mp4" />
</SlidevVideo>
<img src="/figures/campaign_metrics.png" class="h-84" alt="Time to goal, jerk and space compliance of DWA and JESSI on the real robot" />
</div>

<p class="caption">10 runs each, 5 people walking towards the robot · 12.8 ms per action on the Raspberry Pi · video 2×</p>

<div class="cite">Van Der Meer et al., IROS 2026</div>

<!--
We deployed JESSI on a TurtleBot4 without any retraining. The robot crosses a corridor to a goal ten meters ahead, while five people walk in the opposite direction. Ten runs for JESSI and ten for DWA.

Both complete every run without collisions. DWA is faster to the goal, but JESSI keeps more space from people and moves more smoothly, with lower linear and angular jerk. DWA reacts to people; JESSI anticipates them. It runs in 12.8 milliseconds on the Raspberry Pi of the robot.

Transition: the same network also works with other sensors.
-->

---

# The same network works with other sensors, down to a depth camera on a Loomo

<div class="flex justify-center items-center gap-10 mt-2">
<SlidevVideo autoplay loop muted controls poster="/videos/loomo.jpg" printPoster="/videos/loomo.jpg" class="h-72">
  <source src="/videos/loomo.mp4" type="video/mp4" />
</SlidevVideo>
<div class="cards" style="--n: 1; --c: var(--c-jessi); width: 24rem; margin-top: 0; gap: 0.6rem">
  <div class="card"><h3>Trained with</h3><p>100 beams · 360° · 5 scans</p></div>
  <div class="card"><h3>Works, no retraining</h3><p>50 to 500 beams · 3 to 8 scans</p></div>
  <div class="card" style="--c: var(--c-baseline)"><h3>Degrades</h3><p>20 beams · 90° field of view</p></div>
</div>
</div>

<p class="caption">Loomo: depth image converted into a 2D scan · qualitative test · 2×</p>

<div class="cite">Van Der Meer et al., IROS 2026</div>

<!--
JESSI was trained with one hundred beams. Without retraining, it keeps its performance from fifty to five hundred beams, and with a shorter or longer history of scans. It degrades with only twenty beams, where thin obstacles fall between beams, and with a ninety-degree field of view.

On the real TurtleBot we used two hundred beams. We also ran it on a Loomo, which has only a depth camera: we convert the depth image into a 2D scan. That test was only qualitative.

This is the third message: social navigation works from a 2D LiDAR alone.

Transition: before closing, what is still missing.
-->

---

# Safety is promoted, not guaranteed, and decisions still look only one step ahead

<div class="cards">
  <div class="card"><h3>Safety is promoted</h3><p>Collisions remain possible behind the robot, with noisy or sparse scans</p></div>
  <div class="card"><h3>Simulated humans</h3><p>Disks driven by one model, not validated on real data</p></div>
  <div class="card"><h3>One-step decisions</h3><p>No prediction of where people will be</p></div>
</div>

<div class="cards" style="--n: 1; --c: var(--c-jessi)">
  <div class="card"><h3>Next</h3><p>Long-term prediction of human trajectories inside the differentiable pipeline, towards model-based RL</p></div>
</div>

<!--
Three limits. First, the bounding promotes safety but does not guarantee it: collisions remain possible behind the robot, with noisy readings, or with scans that are too sparse. Second, the simulated humans are still disks driven by one model, which we have not validated on real data, and our real-world tests are limited to one scenario. Third, and most important, the policy decides one step at a time. It does not predict where people will be in a few seconds.

The next step is to add long-term prediction of human trajectories inside the differentiable pipeline, which opens the way to model-based RL and to planning over a longer horizon.

Transition: let me close with three things to remember.
-->

---

# Three things to remember

<div class="cards">
  <div class="card" style="--c: var(--c-hm)"><h3>1 · Simulated humans</h3><p>How we simulate humans shapes the robot we train: the human motion model is part of the method</p></div>
  <div class="card" style="--c: var(--c-dirsafe)"><h3>2 · Safe actions</h3><p>Build safety into the actions, not only into the reward: every sampled action stays within the safety bounds</p></div>
  <div class="card" style="--c: var(--c-jessi)"><h3>3 · LiDAR only</h3><p>Social navigation works from a 2D LiDAR alone: JESSI runs on a real robot</p></div>
</div>

<div class="flex justify-center items-center gap-16 mt-8">
  <div class="flex items-center gap-4">
    <img src="/figures/qr_github.svg" class="h-28" alt="QR code to github.com/TommasoVandermeer" />
    <div><div class="text-lg font-semibold">Code</div><div class="text-sm">github.com/TommasoVandermeer</div><div class="text-xs opacity-70">social-jym: dir-safe and jessi branches</div></div>
  </div>
  <div class="flex items-center gap-4">
    <img src="/figures/qr_email.svg" class="h-28" alt="QR code to email tommaso.vandermeer@student.unisi.it" />
    <div><div class="text-lg font-semibold">Let's connect</div><div class="text-sm">tommaso.vandermeer@student.unisi.it</div></div>
  </div>
</div>

<!--
One: how we simulate humans shapes the robot we train. The human motion model is part of the method.
Two: safety should be built into the actions, not only rewarded. With Dirichlet actions and bounding, every action the policy can sample stays within the safety bounds.
Three: social navigation works from a 2D LiDAR alone. JESSI brings these pieces together and runs on a real robot.

The code is on my GitHub, and I am happy to connect by email. Thank you for your attention. I am happy to take questions.
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

| Metric | Definition |
|---|---|
| SR | Success rate: episodes in which the robot reaches the goal |
| CR-H, CR-O | Collision rate with humans, with obstacles |
| TR | Timeout rate: episodes that end without reaching the goal |
| TtG | Time to goal, in successful episodes |
| SC | Space compliance: share of time with clearance from every human above 0.5 m |
| LJ, AJ | Average linear and angular jerk: smoothness of the motion |

<!--
Definitions from Chapter 3.5 of the thesis.
-->

---

# Velocity-based and force-based models share one feedback structure

<img src="/figures/humanmodel.png" class="mx-auto w-3/4 mt-10" alt="Feedback structure of a human motion model" />

<p class="caption mt-6">The human driving block computes the input u; the dynamics update the state x</p>

<div class="cite">Van Der Meer et al., ACM THRI 2025</div>

<!--
The two families differ only in the state variables.
-->

---

# Policies trained with ORCA generalize worst to other human models

<img src="/figures/sarl_hs_cross_env_cc_rates.png" class="mx-auto w-full mt-4" alt="Space compliance and acceleration of policies tested with a different human model, normalized" />

<p class="caption">Ratios to the performance with the training model, circular crossing</p>

<div class="cite">Van Der Meer et al., ACM THRI 2025</div>

<!--
Space compliance and acceleration, normalized by the performance with the training model.
-->

---

# The reward is a weighted sum of four terms

$$
\reward = \wbase \Rbase + \wprog \Rprog + \wtime \Rtime + \wrot \Rrot
$$

| Term | Meaning |
|---|---|
| $\Rbase$ | $+1$ at the goal, $-0.25$ on collision, a penalty inside the discomfort distance $\dsoc$ |
| $\Rprog = \norm{\rpos - \goal} - \norm{\rpos^{+} - \goal}$ | progress towards the goal |
| $\Rtime = -1$ | penalty at every step |
| $\Rrot = -\lvert\romega\rvert$ if $\lvert\romega\rvert > \omegathr$ | penalty on fast rotations |

<div class="cite">Van Der Meer et al., Springer 2025</div>

<!--
Base reward, progress to goal, time penalty, rotation penalty.
-->

---

# JESSI is trained with imitation learning, then PPO, with three paradigms

<img src="/figures/journal_jessi_training_paradigms.png" class="mx-auto w-full mt-10" alt="The three training paradigms of JESSI" />

<p class="caption mt-6">Imitation learning first, then PPO. Paradigms: PO, MD, MT (multi-task)</p>

<div class="cite">Van Der Meer et al., IROS 2026</div>

<!--
Training pipeline and the three paradigms.
-->

---

# Benchmark in known layouts (Setup 1)

<div class="compact-table">

| Policy | SR (%) | CR-H (%) | CR-O (%) | TR (%) | TtG (s) | SC (%) |
|---|---|---|---|---|---|---|
| JESSI-PO | 98.2 ± 1.4 | 0.1 ± 0.3 | 1.1 ± 1.0 | 0.6 ± 0.7 | 19.07 ± 3.74 | 94.4 ± 6.2 |
| JESSI-MD | 97.4 ± 1.8 | 0.1 ± 0.3 | 1.6 ± 1.1 | 0.9 ± 0.9 | 19.45 ± 3.79 | 93.5 ± 6.6 |
| JESSI-MT | 97.5 ± 1.9 | 0.1 ± 0.2 | 1.4 ± 1.1 | 1.0 ± 1.1 | 19.28 ± 3.65 | 92.5 ± 7.3 |
| V-E2E | 91.5 ± 6.3 | 0.1 ± 0.3 | 8.4 ± 6.1 | 0.0 ± 0.1 | 18.77 ± 2.06 | 93.8 ± 7.0 |
| BV-E2E | 98.8 ± 1.2 | 0.0 ± 0.1 | 0.8 ± 0.7 | 0.4 ± 0.9 | 19.05 ± 2.63 | 92.4 ± 7.8 |
| DIR-SAFE | 85.4 ± 7.2 | 0.1 ± 0.2 | 6.2 ± 3.4 | 8.3 ± 4.6 | 20.92 ± 4.41 | 89.8 ± 9.6 |
| SARL* | 70.2 ± 10.6 | 0.2 ± 0.3 | 0.8 ± 0.7 | 28.8 ± 10.2 | 23.91 ± 6.03 | 92.2 ± 7.6 |
| DWA | 74.3 | 0.0 | 0.0 | 25.7 | 17.19 | 78.6 |
| MPPI | 61.0 | 0.0 | 0.3 | 38.7 | 28.67 | 88.3 |
| DRA-MPPI | 78.1 | 0.2 | 1.2 | 20.5 | 25.67 | 94.3 |

</div>

<p class="caption">Known layouts. Mean ± 95% CI over 10 seeds</p>

<div class="cite">Van Der Meer et al., IROS 2026</div>

<!--
All policies and metrics.
-->

---

# Benchmark in unseen layouts (Setup 2)

<div class="compact-table">

| Policy | SR (%) | CR-H (%) | CR-O (%) | TR (%) | TtG (s) | SC (%) |
|---|---|---|---|---|---|---|
| JESSI-PO | 87.2 ± 10.8 | 0.2 ± 0.2 | 2.8 ± 1.9 | 9.8 ± 10.0 | 18.77 ± 5.95 | 87.3 ± 11.7 |
| JESSI-MD | 86.2 ± 10.3 | 0.2 ± 0.7 | 3.1 ± 1.9 | 10.5 ± 9.2 | 18.11 ± 6.03 | 85.4 ± 12.3 |
| JESSI-MT | 89.6 ± 8.5 | 0.1 ± 0.3 | 3.3 ± 2.3 | 7.0 ± 7.6 | 17.76 ± 5.76 | 84.2 ± 12.9 |
| V-E2E | 54.7 ± 24.2 | 0.8 ± 0.9 | 42.5 ± 23.4 | 2.0 ± 2.0 | 18.15 ± 4.20 | 87.6 ± 12.3 |
| BV-E2E | 78.6 ± 13.8 | 0.3 ± 0.5 | 5.7 ± 4.0 | 15.4 ± 10.6 | 20.39 ± 6.00 | 83.1 ± 14.6 |
| DIR-SAFE | 87.1 ± 7.8 | 0.4 ± 0.7 | 6.4 ± 3.5 | 6.1 ± 5.0 | 19.18 ± 5.65 | 79.7 ± 15.3 |
| SARL* | 82.7 ± 8.9 | 0.4 ± 0.6 | 0.3 ± 0.4 | 16.6 ± 8.4 | 21.53 ± 6.60 | 86.6 ± 12.9 |
| DWA | 75.0 | 0.1 | 0.1 | 24.8 | 14.78 | 75.8 |
| MPPI | 74.4 | 0.1 | 0.2 | 25.3 | 28.53 | 88.7 |
| DRA-MPPI | 77.7 | 0.5 | 5.0 | 16.8 | 22.38 | 92.2 |

</div>

<p class="caption">Unseen layouts. Mean ± 95% CI over 10 seeds</p>

<div class="cite">Van Der Meer et al., IROS 2026</div>

<!--
All policies and metrics in the unseen scenarios.
-->

---

# With only the estimated humans, SARL and CADRL hit obstacles that look like people

<div class="compact-table">

| Policy | SR (%) | CR-H (%) | CR-O (%) | TR (%) | TtG (s) | SC (%) |
|---|---|---|---|---|---|---|
| JESSI-PO | 99.9 ± 0.3 | 0.0 ± 0.0 | 0.0 ± 0.1 | 0.1 ± 0.3 | 20.38 ± 2.84 | 93.1 ± 6.3 |
| JESSI-MD | 99.9 ± 0.2 | 0.0 ± 0.0 | 0.0 ± 0.1 | 0.1 ± 0.1 | 20.70 ± 3.19 | 90.8 ± 8.2 |
| JESSI-MT | 99.9 ± 0.3 | 0.0 ± 0.0 | 0.0 ± 0.1 | 0.1 ± 0.2 | 20.48 ± 3.17 | 89.6 ± 8.7 |
| V-E2E | 96.3 ± 3.3 | 0.0 ± 0.0 | 3.7 ± 3.3 | 0.0 ± 0.0 | 19.35 ± 2.00 | 89.6 ± 7.9 |
| BV-E2E | 99.9 ± 0.1 | 0.0 ± 0.0 | 0.0 ± 0.1 | 0.1 ± 0.1 | 19.00 ± 2.16 | 88.4 ± 8.6 |
| DIR-SAFE | 97.2 ± 2.0 | 0.0 ± 0.0 | 2.2 ± 1.8 | 0.6 ± 0.9 | 20.25 ± 3.30 | 88.6 ± 9.3 |
| SARL* | 92.8 ± 4.7 | 0.0 ± 0.0 | 0.0 ± 0.1 | 7.2 ± 4.6 | 20.32 ± 4.80 | 88.1 ± 8.7 |
| SARL | 59.2 ± 18.1 | 0.0 ± 0.0 | **40.8 ± 18.1** | 0.0 ± 0.0 | 17.08 ± 1.73 | 89.5 ± 8.4 |
| CADRL | 44.5 ± 23.9 | 0.0 ± 0.0 | **55.3 ± 23.9** | 0.2 ± 0.6 | 18.92 ± 1.70 | 86.9 ± 11.5 |
| DWA | 98.3 | 0.0 | 0.0 | 1.7 | 16.69 | 71.0 |
| MPPI | 98.1 | 0.0 | 0.6 | 1.3 | 28.49 | 87.2 |
| DRA-MPPI | 94.7 | 0.0 | 0.3 | 5.0 | 27.10 | 95.2 |

</div>

<p class="caption">Setup 3: obstacles that look like people standing still</p>

<div class="cite">Van Der Meer et al., IROS 2026</div>

<!--
Why a geometric channel independent of the perception matters.
-->

---

# JESSI keeps its performance across LiDAR configurations

<div class="compact-table">

| Beams | FoV (°) | Scans | SR 1 (%) | CR-O 1 (%) | SR 2 (%) | CR-O 2 (%) | TR 2 (%) |
|---|---|---|---|---|---|---|---|
| **100** | **360** | **5** | 97.5 | 1.4 | 89.6 | 3.3 | 7.0 |
| 20 | 360 | 5 | 79.1 | 20.8 | 81.2 | 17.6 | 0.1 |
| 50 | 360 | 5 | 95.5 | 3.8 | 87.3 | 8.1 | 4.3 |
| 200 | 360 | 5 | 98.0 | 0.4 | 91.4 | 1.0 | 7.4 |
| 500 | 360 | 5 | 98.0 | 0.0 | 93.4 | 0.0 | 6.3 |
| 100 | 360 | 3 | 97.4 | 1.8 | 88.2 | 4.3 | 7.3 |
| 100 | 360 | 8 | 98.7 | 1.0 | 94.5 | 2.3 | 2.7 |
| 100 | 180 | 5 | 95.9 | 0.5 | 85.8 | 1.0 | 13.1 |
| 100 | 90 | 5 | 79.9 | 14.8 | 75.9 | 7.4 | 16.5 |

</div>

<p class="caption">JESSI-MT without retraining. First row: training configuration. 1, 2: Setup 1, Setup 2</p>

<div class="cite">Van Der Meer et al., IROS 2026</div>

<!--
Number of beams, number of scans and field of view.
-->

---

# DIR-SAFE is more socially compliant than DWA at every crowd density

<img src="/figures/dir_safe_vs_dwa.png" class="mx-auto w-full mt-8" alt="Success rate, time to goal and space compliance of DIR-SAFE and DWA against the number of humans" />

<p class="caption mt-4">Blue: DIR-SAFE · Red: DWA · 900 episodes per crowd density, map of obstacles and humans known</p>

<div class="cite">Van Der Meer et al., ICAR 2025</div>

<!--
Nine hundred episodes per density, no collisions.
-->

---

# Action space bounding with a map of the obstacles

<v-switch>
  <template #0>
    <div class="flex justify-center items-center gap-6 mt-2">
      <img src="/figures/action_space_bounding_1.png" class="h-72" alt="Reachable positions of the robot intersecting a wall" />
      <img src="/figures/action_space_bounding_2.png" class="h-72" alt="Full triangle of feasible actions" />
    </div>
    <p class="caption">Before: some reachable positions (red) cross the wall</p>
  </template>
  <template #1>
    <div class="flex justify-center items-center gap-6 mt-2">
      <img src="/figures/action_space_bounding_3.png" class="h-72" alt="Reachable positions after bounding, clear of the wall" />
      <img src="/figures/action_space_bounding_4.png" class="h-72" alt="Smaller triangle after bounding" />
    </div>
    <p class="caption">After: the smaller triangle (green) keeps every reachable position clear of the wall</p>
  </template>
</v-switch>

<div class="cite">Van Der Meer et al., ICAR 2025</div>

<!--
The static figures of the action space bounding, with the same geometry as the video. Click to see the result.
-->

---

# Gaussian samples are clipped, Dirichlet samples are always feasible

<img src="/figures/dirichlet_vs_gaussian.svg" class="mx-auto h-80" alt="Gaussian samples falling outside the triangle and being clipped, against Dirichlet samples always inside" />

<p class="caption">Illustration. Orange: samples outside the triangle, moved to its border by clipping</p>

<div class="cite">Van Der Meer et al., ICAR 2025</div>

<!--
Static version of the two videos on the Gaussian and the Dirichlet policy.
-->
