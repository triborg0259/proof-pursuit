#!/bin/bash
# Ricerca arXiv deterministica per i 4 problemi (nessun modello). Salva problema-N/fonti/arxiv.json.
# Perché: il Researcher deve posizionare il metodo rispetto allo stato dell'arte con id arXiv reali,
# e il rapporto LaTeX cita solo voci trovate così. Uso: tools/cerca_letteratura.sh
cd "$(dirname "$0")/.."
L=".venv/bin/python researcher/literature.py --max 6"
$L --workdir problema-1/fonti --query "angles between lines" --query "sum of angles between lines" --query "Fejes Toth lines conjecture" --query "ti:\"lines\" AND abs:\"sum of angles\""
mv problema-1/fonti/literature.json problema-1/fonti/arxiv.json
$L --workdir problema-2/fonti --query "uphill paths" --query "hypercube labelling paths" --query "increasing paths labelled graph" --query "monotone paths hypercube ordering"
mv problema-2/fonti/literature.json problema-2/fonti/arxiv.json
$L --workdir problema-3/fonti --query "Bulgarian solitaire" --query "Bulgarian solitaire cycles" --query "Bulgarian solitaire triangular" --query "Garden of Eden Bulgarian solitaire"
mv problema-3/fonti/literature.json problema-3/fonti/arxiv.json
$L --workdir problema-4/fonti --query "disjoint covering systems" --query "disjoint residue classes" --query "exact covering systems moduli" --query "Erdos covering congruences distinct moduli"
mv problema-4/fonti/literature.json problema-4/fonti/arxiv.json
