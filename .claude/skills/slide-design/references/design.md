# Regole di design

## Struttura del talk
- **Apertura (primo minuto):** il problema in concreto, meglio con un video o un'immagine, e una frase che dica perché conta. Niente slide "Outline" con un elenco di sezioni.
- **Mappa ricorrente:** se il talk ha più contributi, una slide-mappa visiva (diagramma del percorso, non un elenco) che ricompare a ogni cambio di sezione con la parte corrente evidenziata.
- **Ogni sezione** si apre con la domanda a cui risponde e si chiude con il messaggio che ha stabilito.
- **Approfondire poco, bene:** meglio due contributi spiegati fino in fondo che tutti accennati. Gli altri diventano episodi brevi.
- **Chiusura:** slide con i messaggi da ricordare (massimo tre), che resta proiettata durante le domande. Non una slide vuota "Thank you / Questions?".
- **Backup:** dopo la chiusura, slide per le domande prevedibili (dettagli sperimentali, ablation, limiti). Non contano nel tempo.

## Titoli
- Frase completa, al massimo due righe, che afferma il messaggio della slide.
- Leggendo solo i titoli in sequenza si deve capire il talk: è il test della storyline.
- Sentence case ("Robots yield earlier with JESSI"), non Title Case.

## Corpo della slide
- Un'evidenza principale, grande. Se servono due figure per due idee, sono due slide.
- Testo: al massimo circa 25 parole oltre al titolo. Elenchi: al massimo tre punti brevi, e solo se l'evidenza è davvero una lista.
- Didascalia breve (classe `caption`) che dica **cosa guardare**, non cosa c'è.
- Contrasto alto e tema chiaro: i proiettori sbiadiscono i colori.
- Mai ridurre font, figure o margini per far entrare il contenuto: taglia o dividi.

## Equazioni
- Solo quelle necessarie al ragionamento. Prima l'intuizione a parole, poi la formula.
- Costruzione per gradi: evidenziazione per righe (`$$ {1|2|all}`) o `v-click`.
- Colori coerenti per i termini ricorrenti (`\textcolor{#d62728}{A_t}`), spiegati in didascalia.
- Solo macro definite in `setup/katex.ts`, con la notazione della tesi se il talk ne fa parte.
- Ogni simbolo nuovo si spiega sulla slide o nelle note.

## Animazioni
- `v-click` per sincronizzare la slide con il parlato: passi di un algoritmo, curve una alla volta, termini di un'equazione.
- Nessun effetto decorativo. Una sola transizione in tutto il deck (quella dell'headmatter).

## Citazioni
- Forma breve in basso a sinistra: `<div class="cite">Everett et al., IROS 2018</div>`.
- I lavori dell'autore con il nome della venue, così il pubblico li riconosce come contributi.
- Bibliografia completa solo in backup, se serve.

## Note del relatore
- Ogni slide ha note (ultimo commento HTML della slide): cosa dire in 2-5 frasi o punti, più la frase di transizione verso la slide successiva.
- La lunghezza delle note determina la stima di `scripts/timing.py` (circa 130 parole al minuto): scrivile alla lunghezza del parlato previsto.
- La repo è pubblica: nelle note niente che l'autore non direbbe in pubblico.

## Lingua (slide in inglese)
- Registro formale ma non ricercato, frasi brevi, parole comuni. L'autore non è madrelingua e deve poter dire le note con naturalezza.
- Acronimi spiegati alla prima occorrenza, sulla slide o a voce.
- Da evitare: "delve", "crucial", "pivotal", "paramount", "seamlessly", "leverage" (usa "use"), "utilize", "showcase", "underscore", "groundbreaking", "cutting-edge", "game-changer", "it is worth noting", "in the realm of"; trattini lunghi a raffica; terne di aggettivi; domande retoriche come titolo.
