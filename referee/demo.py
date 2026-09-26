"""Offline demonstration of merge safety. Reviews are SIMULATED, not AI calls."""
import asyncio
from pathlib import Path
from referees.contracts import ReviewInput
from referees.runner import review


class DemoBackend:
    async def generate(self, *, role, **kwargs):
        if role == "A":
            return {"report": {
                "mathematical_verdict": "PASS", "first_fatal_error": None,
                "accepted_mathematical_claims": ["main"], "unproved_claims": [],
                "missing_cases": [], "math_notes": "SIMULATED DEMO REPORT"}, "limitation": None}
        return {"report": {
            "evidence_verdict": "PASS", "source_issues": [], "computation_issues": [],
            "rule_violations": [], "claim_provenance": [{
                "claim_id": "main", "categories": ["PROVED_BY_US"],
                "evidence_sufficient": True, "permitted_by_rules": True,
                "relies_on_external_result": False, "uses_computation_as_proof": False,
                "references": [], "notes": "SIMULATED DEMO REPORT"}],
            "reproducibility_notes": "SIMULATED DEMO REPORT"}, "limitation": None}


async def main():
    job = ReviewInput.model_validate_json((Path(__file__).parent / "examples/input.json").read_text())
    print((await review(job, DemoBackend())).model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
