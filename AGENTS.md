# Slides

Presentazioni di Tommaso Van Der Meer (PhD, University of Siena), scritte con [Slidev](https://sli.dev) e pubblicate su GitHub Pages:
https://tommasovandermeer.github.io/slides/

## La repo è pubblica
- Tutto ciò che viene committato è visibile a chiunque: sorgenti, note del relatore dentro `slides.md`, file in `notes/`. L'opzione `--without-notes` toglie le note solo dal sito, non dai sorgenti.
- Non inserire risultati non ancora pubblicati, dati riservati o commenti su persone senza conferma esplicita dell'autore.
- Il materiale riservato va in `private/`, che git ignora (quindi non ha backup).

## Struttura
- `_template/`: deck di partenza, da copiare per ogni nuovo talk. Non modificarlo per un talk specifico.
- `GG-MM-AAAA-<tema>/`: un deck per cartella (es. `26-11-2026-phd/`), con:
  - `slides.md`: il deck;
  - `notes/brief.md`: pubblico, durata, messaggi (lo decide l'autore);
  - `notes/storyline.md`: scaletta approvata dall'autore;
  - `public/figures/`, `public/videos/`: asset, referenziati con percorso assoluto (`/figures/x.svg`);
  - `setup/katex.ts`: macro LaTeX; `style.css`: stili globali; `components/`: componenti Vue;
  - `slide-bottom.vue`: cartiglio in fondo a ogni slide (logo, autore e `info` dall'headmatter, numero di slide); loghi in `public/logos/`.
- `<deck>/animations/`: scene Manim del deck; stile comune (colori, sfondo, font) in `scripts/manim_style.py`. I video si generano in locale e si committano come mp4 in `public/videos/`: il deploy non usa Manim.
- `requirements-manim.txt`: Manim Community con versione fissata; il virtualenv `.venv-manim/` è ignorato da git.
- `decks.txt`: elenco dei deck pubblicati. Pubblicare è una decisione dell'autore: non modificare questo file senza richiesta esplicita.
- `scripts/timing.py`: stima della durata dalle note del relatore.
- `.github/workflows/deploy.yml`: build e deploy su GitHub Pages a ogni push su `main`.

## Comandi
Tutti dalla radice della repo; `<deck>` è il nome della cartella.

```bash
# sviluppo, con hot reload: http://localhost:3030 (modalità relatore: /presenter)
npx slidev <deck>/slides.md

# anteprima identica a GitHub Pages (stesso percorso base)
(cd <deck> && npx slidev build slides.md --base /slides/<deck>/ --out ../dist/preview/slides/<deck>)
python3 -m http.server -d dist/preview 8080     # http://localhost:8080/slides/<deck>/

# PNG di ogni slide, per il controllo visivo (cartella <deck>/slides-export/)
(cd <deck> && npx slidev export slides.md --format png)

# PDF di riserva (<deck>/slides-export.pdf)
(cd <deck> && npx slidev export slides.md)

# durata stimata dalle note del relatore
python3 scripts/timing.py <deck>/slides.md --target <minuti>

# video Manim (una tantum: python3 -m venv .venv-manim && .venv-manim/bin/pip install -r requirements-manim.txt)
.venv-manim/bin/manim -qh --fps 30 <deck>/animations/<file>.py <Scena> --media_dir /tmp/manim
```

Se l'export dice che manca il browser: `npx playwright install chromium`.

## Regole
1. **Push = pubblicazione.** Ogni push su `main` rilancia il deploy. Non fare commit né push senza richiesta esplicita.
2. **Prima di scrivere o modificare slide**, segui `.claude/skills/slide-design/` (in Claude Code: skill `slide-design`; per la sintassi di Slidev, skill `slidev`).
3. **Nessun deck senza brief, nessuno scheletro senza storyline approvata.** Se il brief manca o è incompleto, chiedi.
4. **Niente contenuti inventati.** Numeri, risultati, figure e citazioni vengono solo da fonti fornite dall'autore (paper, tesi in `../PhD-thesis/` in sola lettura). Se manca qualcosa, metti un segnaposto visibile `<span class="todo">TODO: ...</span>` e prosegui.
5. **Prima di dichiarare finito un deck:** l'anteprima Pages compila senza errori, figure e video si caricano, nessun `class="todo"` rimasto (`grep -n 'class="todo"' <deck>/slides.md`), durata entro il target.
6. **Asset:** video mp4 H.264 compressi (idealmente sotto 20 MB, mai oltre 100 MB: GitHub li rifiuta). Ogni video ha un'immagine `poster` per il PDF.
7. **Lingua delle slide:** inglese, salvo diversa indicazione nel brief.
