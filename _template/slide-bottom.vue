<script setup lang="ts">
// Cartiglio in fondo a ogni slide (tranne la copertina): logo, autore, evento e data, numero di slide.
// I riferimenti della slide (.cite, in style.css) stanno in una riga sottile subito sopra.
// Autore ed evento vengono dall'headmatter (author, prima riga di info), così restano coerenti.
import { computed } from 'vue'
import { useSlideContext } from '@slidev/client'
import { configs } from '@slidev/client'

const { $page, $frontmatter } = useSlideContext()
const meta = computed(() => {
  // info arriva già convertito in HTML: si tolgono i tag
  const info = String(configs.info ?? '').replace(/<[^>]+>/g, '\n').split('\n').find(l => l.trim()) ?? ''
  return [configs.author, info.trim()].filter(Boolean).join(' · ')
})
</script>

<template>
  <footer v-if="$frontmatter.layout !== 'cover'" class="cartiglio">
    <img src="/logos/unisi_oriz_bn.png" alt="Università di Siena" class="logo" />
    <span class="meta">{{ meta }}</span>
    <span class="page">{{ $page }}</span>
  </footer>
</template>

<style scoped>
.cartiglio {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 2rem;
  padding: 0 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  border-top: 1px solid #e2e2e2;
  background: #fafafa;
  color: #666;
  font-size: 0.65rem;
}
.logo {
  height: 1.25rem;
}
.meta {
  flex: 1;
}
.page {
  min-width: 1.5rem;
  text-align: right;
  font-weight: 600;
}
</style>
