---
theme: default
title: Talk title
author: Tommaso Van Der Meer
info: |
  Event · Place · Date
colorSchema: light
routerMode: hash
transition: fade
layout: cover
---

# Talk title in sentence case

Tommaso Van Der Meer · University of Siena

Event · Date

<!--
Opening: the problem in one sentence, and why it matters to this audience.
-->

---
layout: section
---

# Section title: the question this section answers

<!--
Transition: what the previous section left open and how this one addresses it.
-->

---

# Assertion title: the message of this slide in one sentence

<img src="/figures/example.svg" class="mx-auto h-72" alt="Describe the figure" />

<p class="caption">What to look at in the figure</p>

<div class="cite">Author et al., Venue Year</div>

<!--
What the figure shows, why it supports the title, and the transition to the next slide.
-->

---

# A short video shows the behaviour at a glance

<SlidevVideo autoplay controls poster="/videos/example.jpg" printPoster="/videos/example.jpg" class="mx-auto h-72">
  <source src="/videos/example.mp4" type="video/mp4" />
</SlidevVideo>

<p class="caption">What to watch · 1×</p>

<!--
Tell the audience what to watch before the video starts.
-->

---

# The objective is built one term at a time

$$ {1|2|all}
\begin{aligned}
J(\theta) &= \E_{\tau \sim \policy_\theta}\Big[\textstyle\sum_t \gamma^t r_t\Big] \\
\nabla_\theta J(\theta) &= \E\Big[\textstyle\sum_t \nabla_\theta \log \policy_\theta(a_t \mid s_t)\, \textcolor{#d62728}{A_t}\Big]
\end{aligned}
$$

<p v-click class="caption"><span style="color:#d62728">Advantage</span>: how much better the action was than expected</p>

<!--
Intuition first, then each line of the equation, then what it implies.
-->

---
layout: two-cols-header
---

# Two approaches compared side by side

::left::

**Approach A**

<span class="todo">TODO: figure for A</span>

::right::

**Approach B**

<span class="todo">TODO: figure for B</span>

<!--
The one difference that matters, and which approach wins and why.
-->

---

# Take-home messages

1. First message
2. Second message
3. Third message

<!--
Stays on screen during questions.
-->

---
layout: section
---

# Backup

<!--
Backup slides for expected questions. Not counted in the talk time.
-->
