import { defineKatexSetup } from '@slidev/types'

// Macro KaTeX del deck, convertite da ../PhD-thesis/tex/macros.tex
// (stessa notazione della tesi; barre rovesciate raddoppiate).
export default defineKatexSetup(() => {
  return {
    macros: {
      '\\norm': '\\lVert #1 \\rVert',
      '\\dt': '\\Delta t',
      '\\rpos': '\\mathbf{p}',
      '\\romega': '\\omega',
      '\\goal': '\\mathbf{p}^{\\text{goal}}',
      '\\reward': 'R',
      '\\Rbase': 'R_{\\text{base}}',
      '\\Rprog': 'R_{\\text{prog}}',
      '\\Rtime': 'R_{\\text{time}}',
      '\\Rrot': 'R_{\\text{rot}}',
      '\\wbase': 'w_{\\text{b}}',
      '\\wprog': 'w_{\\text{p}}',
      '\\wtime': 'w_{\\text{t}}',
      '\\wrot': 'w_{\\text{r}}',
      '\\dsoc': 'd_{\\text{s}}',
      '\\omegathr': '\\omega_{\\text{b}}',
    },
  }
})
