import { defineKatexSetup } from '@slidev/types'

// Macro KaTeX del deck. Per i talk sulla tesi, convertire quelle necessarie
// da ../PhD-thesis/tex/macros.tex (barre rovesciate raddoppiate).
export default defineKatexSetup(() => {
  return {
    macros: {
      '\\E': '\\mathbb{E}',
      '\\R': '\\mathbb{R}',
      '\\policy': '\\pi',
    },
  }
})
