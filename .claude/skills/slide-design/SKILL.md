---
name: slide-design
description: Processo e regole di design per creare o modificare le presentazioni Slidev di questa repo. Usala SEMPRE quando crei un nuovo deck, scrivi, riscrivi o rivedi slide, prepari brief, storyline, note del relatore, figure, equazioni o video per una presentazione, anche se l'utente non la nomina. Per la sintassi di Slidev usa insieme la skill slidev.
---

# Creare e rivedere presentazioni

Questa skill dice cosa mettere nelle slide e in che ordine lavorare; la sintassi di Slidev è nella skill `slidev`. Le convenzioni della repo (struttura, comandi, regole) sono in `AGENTS.md`.

Una presentazione si giudica da ciò che il pubblico ricorda: pochi messaggi, ciascuno sostenuto da un'evidenza che si capisce in pochi secondi. Ogni regola qui sotto serve a questo.

## Processo per un nuovo deck
Lavora per fasi e fermati dove indicato: l'autore deve poter correggere la direzione prima che il lavoro diventi costoso.

1. **Cartella.** Copia `_template/` in `GG-MM-AAAA-<tema>/`. Non aggiungere il deck a `decks.txt`.
2. **Brief.** Compila `notes/brief.md` con ciò che l'autore ha detto. Se mancano pubblico, durata o i tre messaggi, chiedi: non inventarli. ⏸ Conferma dell'autore.
3. **Storyline.** Compila `notes/storyline.md` usando le fonti indicate nel brief:
   - sezioni con la domanda a cui rispondono e i minuti;
   - per ogni slide: titolo-asserzione, evidenza (figura, video, equazione, diagramma), durata;
   - budget di riferimento: circa una slide al minuto; apertura e chiusura insieme circa il 15% del tempo; meglio due argomenti approfonditi che sei accennati.
   ⏸ Presenta la storyline e aspetta l'approvazione. Non creare slide prima.
4. **Scheletro.** Una slide per riga della storyline: titolo definitivo, segnaposto `<span class="todo">` per le evidenze mancanti, note del relatore abbozzate. Rimuovi dal template le slide di esempio non usate. Il deck deve già compilare ed essere navigabile.
5. **Materiale.** Figure, video ed equazioni secondo `references/media.md`. Macro LaTeX in `setup/katex.ts` (se il talk riguarda la tesi, convertile da `../PhD-thesis/tex/macros.tex` per avere la stessa notazione).
6. **Rifinitura.** Animazioni solo dove scandiscono il ragionamento; note del relatore complete.
7. **Verifica.** Checklist in fondo. Poi riepiloga all'autore: cosa hai fatto, TODO rimasti, slide di cui non sei sicuro, durata stimata.

Per modificare un deck esistente salta le fasi 1-3, ma rispetta comunque brief, storyline e regole di design.

## Regole essenziali
Dettagli ed esempi in `references/design.md`: leggilo prima di scrivere slide.

- **Una slide, un messaggio.** Il titolo è una frase che afferma il messaggio ("JESSI keeps a 97% success rate in dense crowds"), non un'etichetta ("Results").
- **Il corpo è l'evidenza** che sostiene il titolo: figura, video, equazione o diagramma. Testo oltre il titolo: al massimo circa 25 parole; niente paragrafi.
- **Se non entra, si taglia o si divide.** Mai rimpicciolire font, figure o margini per far stare il contenuto.
- **Coerenza visiva:** stesso colore per lo stesso metodo o concetto in tutto il deck, stessa transizione, stessi stili (`style.css`).
- **Note del relatore su ogni slide**, con la frase di transizione verso la slide successiva.
- **Chiusura:** l'ultima slide prima del backup riassume i messaggi da ricordare e resta visibile durante le domande.

## Verifica (prima di consegnare)
Esegui i comandi in `AGENTS.md`.
1. Anteprima Pages: compila senza errori, figure e video si caricano al percorso `/slides/<deck>/`.
2. Esporta le slide in PNG e **guardale una per una** (leggi le immagini). Cerca: testo che esce dai bordi o si sovrappone, font piccoli, slide affollate, figure illeggibili, colori incoerenti.
3. `python3 scripts/timing.py <deck>/slides.md --target <minuti>`: durata totale e per sezione rispetto alla storyline.
4. `grep -n 'class="todo"' <deck>/slides.md`: elenca all'autore i TODO rimasti.
5. Rileggi titoli e note contro la lista "Lingua" di `references/design.md`.
