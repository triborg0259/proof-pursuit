"""Orchestrator-owned evidence. NOT an LLM tool or a public request schema.

No checker is implemented here. Records must come from actual independent
verification (or explicit human review), not from model-generated reports.
Hash binding prevents accidental reuse; it is not authentication or a sandbox.
"""
from dataclasses import dataclass
import hashlib
import json
from typing import Literal
from .contracts import ReviewInput


def submission_digest(job: ReviewInput) -> str:
    data = json.dumps(job.model_dump(mode="json"), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(data.encode()).hexdigest()


@dataclass(frozen=True)
class VerifiedRecord:
    submission_digest: str
    claim_id: str
    kind: Literal["LEAN", "EXACT_CERTIFICATE", "HUMAN_REVIEW"]
    evidence_reference: str


@dataclass(frozen=True)
class CounterexampleRecord:
    submission_digest: str
    # May refute an intermediate claim, not necessarily the target.
    claim_id: str
    evidence_reference: str


@dataclass(frozen=True)
class OpenStatusRecord:
    submission_digest: str
    target_claim_id: str
    source_reference: str
    checked_on: str


@dataclass(frozen=True)
class HistoryEntry:
    problem_id: str
    cell_id: str
    attempt_id: str
    method_tag: str
    blocking_key: str
    new_verified_claim_ids: tuple[str, ...]


@dataclass(frozen=True)
class TrustedContext:
    records: tuple[VerifiedRecord, ...] = ()
    counterexamples: tuple[CounterexampleRecord, ...] = ()
    open_status: OpenStatusRecord | None = None
    # Authenticated orchestrator history; never supplied by the researcher.
    history: tuple[HistoryEntry, ...] = ()
    # Source retrieval / execution logs produced outside the LLM.
    evidence_observations: tuple[str, ...] = ()
