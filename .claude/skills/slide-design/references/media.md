# Figure, video ed equazioni

## Figure
- **Rigenerale dagli script originali** con uno stile da slide, invece di riusare le figure del paper:
  - font di assi e legende grandi (almeno 18-20 pt alla dimensione finale sulla slide);
  - linee spesse, marker grandi;
  - solo le curve e le baseline che servono al messaggio della slide;
  - etichette dirette sulle curve al posto della legenda, quando possibile;
  - ciò che conta in colore, il resto in grigio.
- **Palette coerente in tutto il deck:** ogni metodo ha sempre lo stesso colore. Usa una palette leggibile anche da chi non distingue i colori (per esempio Okabe-Ito).
- **Formato:** SVG per grafici e diagrammi; PNG ad alta risoluzione per immagini. Mai screenshot di figure del paper con testo piccolo.
- **Dove:** `<deck>/public/figures/`, referenziate come `/figures/nome.svg`.
- Se una figura serve ma non c'è, segnaposto `<span class="todo">TODO: figura ...</span>` e una riga nel riepilogo all'autore.

## Video
- **Brevi e tagliati sull'azione:** 5-30 secondi, senza audio, in loop se mostrano un comportamento.
- **Didascalia** che dica cosa guardare e la velocità se accelerati ("Robot yields to the pedestrian on the left · 4×").
- **Poster:** ogni video ha un fotogramma JPG usato come `poster` e `printPoster`, così il PDF di riserva mostra un'immagine al posto del video.
- **Dove:** `<deck>/public/videos/`, referenziati come `/videos/nome.mp4`.
- **Dimensioni:** idealmente sotto 20 MB; GitHub rifiuta file oltre 100 MB.

Ricette ffmpeg:

```bash
# taglia (da 5 s, durata 20 s), ridimensiona a 1280 px, togli audio, comprimi
ffmpeg -ss 5 -i in.mp4 -t 20 -vf "scale=1280:-2,fps=30" -an \
  -c:v libx264 -crf 26 -preset veryfast -pix_fmt yuv420p -movflags +faststart out.mp4

# accelera 4x (aggiungi a -vf, prima di scale)
#   -vf "setpts=0.25*PTS,scale=1280:-2,fps=30"

# poster dal secondo 2
ffmpeg -ss 2 -i out.mp4 -frames:v 1 -q:v 3 out.jpg
```

Markup:

```md
<SlidevVideo autoplay controls poster="/videos/nome.jpg" printPoster="/videos/nome.jpg" class="mx-auto h-72">
  <source src="/videos/nome.mp4" type="video/mp4" />
</SlidevVideo>

<p class="caption">Cosa guardare · 4×</p>
```

## Macro LaTeX
- `setup/katex.ts` contiene le macro KaTeX del deck.
- Per i talk sulla tesi, converti le macro necessarie da `../PhD-thesis/tex/macros.tex` (solo `\newcommand` semplici; KaTeX non supporta tutti i pacchetti LaTeX). Nel file TypeScript le barre rovesciate vanno raddoppiate: `'\\policy': '\\pi'`.
- Dopo ogni modifica controlla nel browser che le formule si vedano: un errore KaTeX appare in rosso sulla slide.
