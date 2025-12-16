
### Obiettivo del Progetto
L'obiettivo principale è sviluppare un programma automatizzato per monitorare la lista dei follower su piattaforme come GitHub, utilizzando come riferimento un account con molti follower. Il sistema deve essere in grado di tracciare l'evoluzione dei follower giorno per giorno, permettendo di identificare specificamente chi ha smesso di seguirti e chi ha iniziato a farlo.

### Analisi Tecnica e Problemi
La sfida principale risiede nella struttura della pagina web, poiché la lista dei follower non è visibile interamente in una sola schermata.
- **Paginazione**: Per visualizzare tutti gli utenti è necessario navigare tra diverse pagine.
- **Parsing HTML**: Il programma deve analizzare il contenuto HTML completo per identificare i pattern specifici, come il bottone per la pagina successiva o i contenitori dei profili utente.

### Flusso Operativo (Algoritmo)
Il funzionamento logico del software è stato delineato in cinque passaggi sequenziali:
1.  **Avvio**: Inizializzazione del processo di scraping.
2.  **Download**: Scaricamento del contenuto HTML della pagina corrente.
3.  **Verifica Paginazione**: Controllo della presenza del bottone "next".
    - *Se presente*: Si estrae l'URL e si scarica la pagina successiva (ciclo iterativo).
    - *Se assente*: Si procede all'analisi finale verificando la lista completa tramite l'HTML specifico.

### Archiviazione e Statistiche
Una volta estratti i dati, è necessario definire una strategia di salvataggio e analisi:
- **Salvataggio Dati**: I nomi dei follower e il loro numero totale devono essere salvati in un file persistente o in una tabella (si fa riferimento a uno spreadsheet già esistente).
- **Analisi**: I dati archiviati verranno utilizzati per generare statistiche temporali, confrontando i risultati attuali con quelli dei giorni precedenti per evidenziare i trend.