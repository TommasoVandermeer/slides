<script setup lang="ts">
// Mappa ricorrente del talk: il percorso dal mondo idealizzato al robot reale.
// `current`: 0 = nessuna tappa evidenziata, 1-4 = tappa corrente.
// `venue`: unico punto del deck dove compaiono le sedi dei lavori dell'autore (scelta dell'autore).
const props = withDefaults(defineProps<{ current?: number }>(), { current: 0 })

const stops = [
  { n: 1, title: 'Social navigation', sub: 'the problem', venue: '', color: 'var(--c-problem)' },
  { n: 2, title: 'Simulating humans', sub: 'idealized world', venue: 'ACM THRI 2025 · Springer 2025', color: 'var(--c-hm)' },
  { n: 3, title: 'DIR-SAFE', sub: '+ kinematics, obstacles', venue: 'ICAR 2025', color: 'var(--c-dirsafe)' },
  { n: 4, title: 'JESSI', sub: '+ 2D LiDAR only, real robot', venue: 'IROS 2026', color: 'var(--c-jessi)' },
]
</script>

<template>
  <div class="roadmap">
    <template v-for="(s, i) in stops" :key="s.n">
      <div
        class="stop"
        :class="{ active: props.current === s.n, dim: props.current !== 0 && props.current !== s.n }"
        :style="{ '--stop': s.color }"
      >
        <div class="title">{{ s.title }}</div>
        <div class="sub">{{ s.sub }}</div>
        <div v-if="s.venue" class="venue">{{ s.venue }}</div>
      </div>
      <div v-if="i < stops.length - 1" class="arrow" aria-hidden="true">&rarr;</div>
    </template>
  </div>
</template>

<style scoped>
.roadmap {
  display: flex;
  align-items: stretch;
  justify-content: center;
  gap: 0.6rem;
  margin-top: 2.5rem;
}
.stop {
  flex: 1;
  padding: 0.9rem 0.8rem;
  border: 3px solid var(--stop);
  border-radius: 0.6rem;
  text-align: center;
  transition: opacity 0.3s;
}
.stop.active {
  background: var(--stop);
  color: #fff;
}
.stop.dim {
  opacity: 0.35;
}
.title {
  font-size: 1.15rem;
  font-weight: 700;
  line-height: 1.25;
}
.sub {
  margin-top: 0.3rem;
  font-size: 0.85rem;
  opacity: 0.85;
}
.venue {
  margin-top: 0.45rem;
  font-size: 0.75rem;
  font-style: italic;
  opacity: 0.7;
}
.arrow {
  align-self: center;
  font-size: 1.6rem;
  opacity: 0.5;
}
</style>
