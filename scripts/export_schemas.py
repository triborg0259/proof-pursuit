"""Run from the project root after installing the package or with PYTHONPATH=."""
import json
from pathlib import Path
from referees.contracts import AgentEnvelope, EvidenceReport, FinalReport, MathReport, ReviewInput
from referees.hackathon import ReviewPacket, HumanApproval
from referees.exact import CHECKS

root = Path(__file__).resolve().parents[1] / "schemas"
root.mkdir(exist_ok=True)
for name, model in {
    "input": ReviewInput,
    "math_report": AgentEnvelope[MathReport],
    "evidence_report": AgentEnvelope[EvidenceReport],
    "final_report": FinalReport,
    "review_packet": ReviewPacket,
    "human_approval": HumanApproval,
}.items():
    (root / f"{name}.schema.json").write_text(
        json.dumps(model.model_json_schema(), indent=2, ensure_ascii=False) + "\n")
(root / "exact_checks.schema.json").write_text(json.dumps(CHECKS.json_schema(), indent=2) + "\n")
