# Immagine in cui gira SOLO il Researcher. Dentro non esistono referee/, researcher/, gli schemi né gli altri run:
# il modello vede la sandbox della cella (/work), tools/ e la cartella del problema in sola lettura.
# Perché: con i permessi bypassati un agente legge tutto ciò che il processo può leggere; l'unico confine che
# regge è quello del sistema (rapporto, sezione "Implicazioni", P3/P8).
FROM python:3.12-slim

# Node serve alla CLI `claude`; le librerie Python sono le stesse del .venv del repo.
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates git \
    && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && npm install -g @anthropic-ai/claude-code \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir numpy mpmath scipy pydantic sympy networkx matplotlib pandas

# Utente non privilegiato: le credenziali montate in /home/researcher/.claude restano leggibili solo a lui.
RUN useradd -m researcher
USER researcher
WORKDIR /work
