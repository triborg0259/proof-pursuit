# Verifica versione 0.2

50 test software offline superati. Test di dipendenze, timeout, separazione A/B, certificati, approvazione umana firmata, manomissioni, dati float e controlli esatti nei quattro ambiti.

Eseguiti realmente gli esempi rational_vectors, hypercube_paths, unrestricted_partitions_allowed_parts e residue_classes: tutti MATCH per i soli dati degli esempi. Eseguita anche enumerazione di tutte le 40320 etichettature di Q3 nel test dedicato.

Verificata CLI offline: non inventa revisioni né approvazioni. Nessuna chiamata API reale e nessun consumo di crediti; i test A/B usano backend simulati. Lo script adversarial_eval.py deve essere eseguito sul modello reale prima della gara/demo.

Lean e lake non risultano installati in questo ambiente; non sono dipendenze di questa versione. La firma della ricevuta attesta la decisione umana e non è una prova matematica.
