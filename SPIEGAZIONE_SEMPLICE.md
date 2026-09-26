# Proof Pursuit spiegato semplice

*Come lo racconterebbe un ragazzo di 12 anni a un altro: quattro problemi, cosa chiedono davvero, come li abbiamo
attaccati, e come funziona la "squadra di robot" che ci ha aiutato. Tutto qui dentro è esatto: le metafore
semplificano le parole, non i fatti.*

---

## Prima di tutto: cos'è questa gara

Immagina una gara di 7 ore con 4 problemi di matematica. Ogni problema è una **scala di 6 gradini**: il primo vale
1 punto ed è facile, l'ultimo vale 13 punti ed è una domanda a cui **nessuno al mondo sa ancora rispondere**.
Non basta dire la risposta giusta: devi **dimostrarla**, cioè convincere un giudice severissimo che non può essere
altrimenti. Puoi usare il computer, ma solo se il calcolo è esatto, finisce in meno di 10 minuti, e spieghi perché
quel calcolo dimostra davvero qualcosa. Copiare la risposta da un libro non vale.

---

## Problema 1 — Gli angoli tra le rette (il problema di Fejes Tóth)

**La metafora.** Prendi degli spaghetti e infilzali tutti nello stesso punto, come raggi di una ruota. Tra ogni
coppia di spaghetti c'è un angolo (quello piccolo, mai più di 90°). Somma tutti gli angoli di tutte le coppie.
**Domanda: come li disponi per fare la somma più grande possibile?**

Nel 1959 un matematico ungherese, László Fejes Tóth, disse: "Il modo migliore è metterli lungo le direzioni
perpendicolari, il più equamente possibile". Nel piano ci sono 2 direzioni perpendicolari (come una croce), nello
spazio 3 (come gli spigoli di una stanza in un angolo), e così via. Sembra ovvio, ma nessuno è mai riuscito a
dimostrarlo in generale: è una **congettura** da 67 anni.

**I sei gradini.**
1. Nel piano (la croce): dimostrare che la somma è al massimo (π/2)·⌊N²/4⌋. È l'unico caso già risolto in
   letteratura, ma va ridimostrato.
2. Un lemma su una "catena" di vettori dove ognuno è perpendicolare a tutti tranne i suoi vicini: la somma degli
   angoli consecutivi non supera (m−2)·90°.
3. Una retta in più della dimensione (d+1 rette in d dimensioni).
4. Due casi concreti: 5 rette nello spazio a 3 dimensioni, 6 rette in quello a 4.
5. Due rette in più della dimensione, in ogni dimensione.
6. La congettura intera: aperta.

**Il nostro approccio.**
- Per il gradino 1 abbiamo trovato una via **"con il dado"**: immagina di lanciare un diametro a caso attraverso la
  ruota di spaghetti. Ogni coppia di spaghetti viene separata dal diametro con una probabilità proporzionale
  all'angolo tra loro. Allora la somma degli angoli è (π/2) volte il numero medio di coppie separate; ma un diametro
  divide gli spaghetti in due gruppi, k da una parte e N−k dall'altra, e k·(N−k) non può mai superare ⌊N²/4⌋.
  Fine. Bello perché non usa nessun libro. (Poi abbiamo letto che gli esperti Bilyk e Matzke hanno una prova
  molto simile: bene, vuol dire che è la strada giusta.)
- Per il gradino 2 usiamo un'**induzione con le proiezioni**: togli l'ultimo vettore, "schiaccia" il penultimo sul
  piano perpendicolare, e ti ritrovi con una catena più corta a cui applicare la stessa regola. Un triangolo sferico
  rettangolo chiude il conto.
- Gradini 3–5: il lemma del gradino 2 è il mattone; il difficile è trasformare rette "in disordine" in una catena.
  Ancora in lavorazione. Il gradino 4 si può anche fare con un calcolo rigoroso (aritmetica a intervalli).
- Gradino 6: solo ricerche di controesempi al computer; non ci aspettiamo di chiuderlo.

**Cosa abbiamo verificato al computer.** Un programma che prova milioni di disposizioni e non trova mai una somma
più grande di quella prevista, per N fino a 10. Non è una prova (il computer usa numeri approssimati), è solo un
"sembra vero".

---

## Problema 2 — I sentieri in salita sul cubo

**La metafora.** Prendi un cubo a d dimensioni: per d=3 è il cubo normale, 8 angoli e 12 spigoli. Scrivi su ogni
angolo un numero diverso da 1 a 8: è la sua "altezza". Un angolo è una **valle** se tutti i suoi vicini sono più
alti. Un **sentiero in salita** parte da una valle e va di vicino in vicino sempre salendo (anche restare fermi
nella valle è un sentiero). **Domanda: come scrivi i numeri per avere il minor numero possibile di sentieri?**

Questo gioco, su una griglia quadrata, è stato il problema 6 delle Olimpiadi di matematica 2022 (il più difficile).
Sul cubo è ancora aperto.

**I sei gradini.** Trovare il minimo per il cubo in 3 e 4 dimensioni (1 punto), in 5 (2 punti), in 6 (3 punti),
in 7 e 8 (5 punti); migliorare i limiti noti per 9 dimensioni, 2368 ≤ U(Q₉) ≤ 2400 (8 punti); trovare esattamente
U(Q₉) (13 punti, aperto).

**Il nostro approccio.**
- **L'idea che conta tutto:** invece di contare i sentieri uno per uno, per ogni angolo v contiamo quanti sentieri
  *finiscono* in v. È la somma di quelli che finiscono nei vicini più bassi (più 1 se v è una valle). Così il computer
  conta in un lampo, con numeri interi esatti.
- **Il limite dal basso "gratis":** ogni angolo è la fine di almeno un sentiero, e ogni spigolo "in salita" ne
  regala uno in più. Quindi i sentieri sono almeno (numero di spigoli) + (numero di valli). Per il cubo 3D: almeno 13.
- **Perché 13 è impossibile e il minimo è 14:** con esattamente 13 sentieri ogni angolo dovrebbe avere "grado in
  entrata" 0, 1 oppure 3, e i conti non tornano (come cercare di pagare 17 euro con sole monete da 3). Stessa idea
  per il cubo 4D: minimo 34, e abbiamo costruito la disposizione che lo raggiunge, scrivendo i numeri per "peso"
  (quanti 1 ha ogni angolo scritto in binario).
- **Cubo 5D: 88.** Qui il trucco delle monete non basta più. Il ragionamento arriva a dire: "se esistesse una
  disposizione con meno di 88 sentieri, allora nel cubo dovrebbe esistere una certa figura strana (12 angoli mai
  vicini tra loro, più uno, che tolti dal cubo lo spezzano in una foresta senza cicli)". Poi il computer controlla
  **tutte** le 3672 figure possibili in mezzo secondo: quella figura non esiste. Quindi 88 è il minimo, e abbiamo la
  disposizione che fa esattamente 88. Tre programmi diversi (due del robot ricercatore, uno nostro con un altro
  metodo) danno lo stesso conteggio.
- Cubi più grandi: la ricerca è in corso con la squadra di robot (vedi sotto).

**Curiosità.** In 3 e 4 dimensioni il minimo è "spigoli + 2"; in 5 dimensioni salta a "spigoli + 8". Il pattern
facile si rompe, ed è proprio per questo che il problema è difficile.

---

## Problema 3 — Il solitario bulgaro

**La metafora.** Hai delle pile di carte. A ogni mossa prendi **una carta da ogni pila** e con quelle carte fai una
pila nuova. Le pile vuote spariscono. Ripeti. Siccome le carte sono sempre le stesse, prima o poi la situazione
**si ripete**: entri in un ciclo. **Domanda: quante mosse possono servire, al massimo, prima di entrare nel ciclo?**

Esempio con 6 carte: (2,1,1,1,1) → (5,1) → (4,2) → (3,2,1) → (3,2,1) → … Dopo 3 mosse sei nel ciclo, che qui è un
punto fisso: la "scala" 3,2,1.

**I sei gradini.**
1. Se le carte sono un numero triangolare (1, 3, 6, 10, 15, …), tutti finiscono alla scala k, k−1, …, 1 e quella è
   l'unica situazione che si ripete. Per gli altri n: descrivere tutte le situazioni che si ripetono e contare i cicli.
2. Il numero massimo di mosse quando n è triangolare (atteso k²−k).
3. Un limite generale k²−2k−1 per n non triangolare, e il valore esatto per n = T_k − 1.
4. Il valore esatto per n = T_{k−1} + 1.
5. Il valore esatto per n = T_{k−1} + 2, con un unico argomento per tutti i k.
6. Il valore per ogni n: aperto.

**Il nostro approccio.**
- **La scala e le "carte extra".** Ogni situazione si può vedere come la scala k−1, k−2, …, 1 più qualche carta in
  più appoggiata su certi gradini. La mossa del solitario fa **ruotare** le carte extra lungo i gradini, come perline
  su una collana. Quindi le situazioni cicliche sono esattamente le **collane** con k perline di cui r nere, e contare
  i cicli è contare le collane diverse a meno di rotazione (una formula classica con la funzione φ di Eulero).
- **Per il resto:** prima calcoliamo con il computer, in modo esatto, il numero massimo di mosse per ogni n fino a
  circa 60, con le situazioni che lo raggiungono. Poi cerchiamo la formula e la dimostriamo con un "potenziale":
  una quantità che misura quanto sei lontano dalla scala e che scende a ogni mossa.
- Fonti da controllare: Brandt 1982, Igusa 1985, Etienne 1991, Griggs–Ho 1998, e un survey di Drensky trovato su
  arXiv (1503.00885). Possiamo riscrivere per esteso una prova nota dichiarando da dove viene: vale.

---

## Problema 4 — Classi di resto disgiunte

**La metafora.** Una "classe di resto" è un insieme di numeri a passo fisso: per esempio "1 modulo 4" sono
1, 5, 9, 13, … (parti da 1 e salti di 4). Prendi k di queste sequenze in modo che **non abbiano nessun numero in
comune**. **Domanda: due dei passi devono per forza avere un fattore comune grande, almeno k?**

Esempio con k=3: le sequenze "0 mod 2", "1 mod 4", "3 mod 8" non si toccano mai, e i passi 4 e 8 hanno il fattore
comune 4 ≥ 3. L'esempio perfetto è 1, 2, …, k modulo k: tutte disgiunte, tutti i fattori comuni esattamente k.
Si crede che sia sempre vero (congettura di Z.-W. Sun), ma è dimostrato solo per k piccoli.

**I sei gradini.** Dimostrarlo per k=3 (1 punto), k=4 (2 punti), fino a 8 (3 punti), fino a 12 con un rapporto
onesto su cosa resta indeciso da 9 a 16 (5 punti); certificare il massimo k possibile e decidere k=24 e k=30 con
un certificato durissimo, incluse **due implementazioni indipendenti** che devono dare la stessa lista (8 punti);
oltre (13 punti, aperto).

**Il nostro approccio.**
- **k=3 a mano.** Se tutti i fattori comuni fossero solo 2, tutti i passi sarebbero pari e i punti di partenza a
  due a due di parità diversa: ma con 3 numeri due hanno la stessa parità. Contraddizione in tre righe.
- **k=4 a mano.** I fattori comuni possono essere solo 2 o 3. Chi è pari deve avere resto diverso dagli altri pari;
  chi è multiplo di 3 deve avere resto diverso dagli altri multipli di 3. Contando quanti possono stare in ogni
  gruppo, 4 sequenze non ci stanno.
- **L'idea chiave per i gradini 3–5: ridurre a un insieme finito.** Se un controesempio esiste, si può sempre
  "sfoltire" ogni passo fino a renderlo il minimo comune multiplo dei suoi fattori comuni con gli altri, senza
  rompere la disgiunzione. Allora tutti i passi dividono mcm(2, …, k−1): un numero finito di candidati. Il computer
  può controllarli **tutti**, e siccome la regola di gara vuole ogni regola di potatura dimostrata, la lista dei
  sopravvissuti e una seconda implementazione con un metodo diverso, il lavoro grosso è scrivere il certificato,
  non la ricerca.

---

## La squadra di robot: come funziona il "loop"

Abbiamo costruito un sistema in cui più agenti (programmi basati su un modello di linguaggio) si passano il lavoro.
Immagina una classe:

- **Il Ricercatore (Researcher, il nostro).** È lo studente che prova a risolvere il problema. Legge il problema
  formalizzato, ciò che è già stato dimostrato, i tentativi già falliti e perché, e gli articoli trovati su arXiv.
  Sceglie **un** sotto-obiettivo e **una** strategia, spiega perché l'ha scelta e come si posiziona rispetto a ciò che
  gli esperti hanno già fatto, lavora in una vera shell (può far girare programmi, scaricare articoli), e consegna
  un tentativo con la prova, il codice usato e **una lista onesta delle cose che non è riuscito a giustificare**.
  Regola d'oro: non può mai dire "risolto".
- **Il ponte.** Prima di passare il compito ai giudici, rilancia da capo tutti i programmi del Ricercatore in una
  cartella pulita: i giudici si fidano solo dei risultati che ha visto il ponte, non di quelli raccontati dallo studente.
- **I due Giudici (Referee, di gabundos).** Due professori che correggono lo stesso compito senza parlarsi.
  Il Giudice A guarda solo la matematica: qual è il **primo** passaggio non giustificato? Il Giudice B guarda solo le
  prove: le fonti citate esistono? I calcoli sono stati rifatti? La ricerca era completa o a campione? Poi un
  programma (non un modello) combina i due giudizi con regole fisse. Il massimo che possono dire è "pronto per un
  umano": l'approvazione finale è sempre di una persona.
- **Il Creativo (Creative, di Marco).** L'amico che, quando ti vede sbattere la testa sullo stesso muro, ti dice
  "e se provassi dall'altra parte?". Entra solo quando il ciclo **stagna**: lo stesso errore che si ripete, o il
  Ricercatore che chiede aiuto, o un contatore che vede tentativi tutti uguali. Legge tutta la storia, scrive perché
  ci si blocca, cosa non rifare, e 2–4 direzioni davvero diverse con il loro rischio. Il Ricercatore del giro dopo
  deve dire quale idea segue.
- **Il loop (loop.py).** L'allenatore che tiene il diario: a ogni giro scrive chi ha scelto cosa e perché, cosa ha
  bloccato il giudice, se e perché è entrato il Creativo. Quel diario finisce nel rapporto finale.

**Cosa abbiamo imparato facendolo girare davvero.** Il primo giro reale sul cubo 5D è andato così: il Ricercatore ha
trovato 88 con una prova e sette programmi; il Giudice A ha detto "corretto in entrambe le direzioni" ma ha aggiunto
una riserva ("non ho potuto eseguire il codice") in un campo che il contratto non ammette insieme al verdetto, e il
rapporto è stato scartato; il Giudice B ha chiesto che i calcoli fossero rifatti da qualcuno di fidato. Da lì due
correzioni: il ponte ora rilancia il codice e passa gli esiti ai giudici, e una riserva del giudice va nelle note
invece di far perdere il giudizio.

---

## In una frase

Quattro domande semplici da fare e difficilissime da chiudere; per ognuna separiamo sempre **la costruzione che
raggiunge un valore** dalla **prova che non si può fare meglio**, e distinguiamo sempre ciò che è dimostrato, citato,
verificato al computer su un insieme finito, o solo congetturato.
