"""Real exact computations across four domains, without API or proof acceptance."""
import json
from pathlib import Path
from referees.exact import run_checks

raw=json.loads((Path(__file__).parent/'examples/checks-multidomain.json').read_text())
results=run_checks(raw,allowed_claim_ids={c['claim_id'] for c in raw})
print(json.dumps([r.model_dump(mode='json') for r in results],indent=2))
