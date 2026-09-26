from __future__ import annotations

from typing import Generic, Literal, TypeVar
from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class Claim(StrictModel):
    id: str = Field(min_length=1)
    statement: str = Field(min_length=1)
    depends_on: list[str] = Field(default_factory=list)


class Cell(StrictModel):
    id: str
    number: int = Field(ge=1)
    target_claim_id: str
    statement: str = Field(min_length=1)


class VerifiedState(StrictModel):
    highest_verified_cell: int = Field(ge=0)
    claims: list[Claim] = Field(default_factory=list)


class Source(StrictModel):
    id: str
    reference: str
    claim_ids: list[str]
    submitted_excerpt: str = ""


class Artifact(StrictModel):
    id: str
    kind: Literal["CODE", "CERTIFICATE", "LOG"]
    content: str
    claim_ids: list[str]


class Candidate(StrictModel):
    attempt_id: str
    proof: str = Field(min_length=1)
    method_tag: str
    claims: list[Claim]
    sources: list[Source] = Field(default_factory=list)
    artifacts: list[Artifact] = Field(default_factory=list)


class Rules(StrictModel):
    # Explicit choices: do not silently assume contest rules.
    allow_literature_as_proof: bool
    allow_computation: bool
    require_machine_verification: bool
    additional_rules: str


class ReviewInput(StrictModel):
    # Built by the trusted orchestrator, not directly from a researcher payload.
    problem_id: str
    original_problem: str = Field(min_length=1)
    cell: Cell
    state: VerifiedState
    candidate: Candidate
    rules: Rules

    @model_validator(mode="after")
    def check_claim_registry(self):
        old = [c.id for c in self.state.claims]
        new = [c.id for c in self.candidate.claims]
        if len(set(old + new)) != len(old + new):
            raise ValueError("Claim IDs must be unique across state and candidate")
        claims = {c.id: c for c in self.candidate.claims}
        target = claims.get(self.cell.target_claim_id)
        if target is None or target.statement != self.cell.statement:
            raise ValueError("Candidate must declare the exact protected target")
        known = set(old + new)
        if any(dep not in known for c in claims.values() for dep in c.depends_on):
            raise ValueError("Unknown dependency")
        for item in self.candidate.sources + self.candidate.artifacts:
            if not set(item.claim_ids) <= known:
                raise ValueError("Evidence references an unknown claim")
        return self


class Issue(StrictModel):
    code: str = Field(min_length=1)
    detail: str = Field(min_length=1)
    severity: Literal["FATAL", "MISSING", "INFO"]
    claim_ids: list[str] = Field(default_factory=list)


class MathReport(StrictModel):
    mathematical_verdict: Literal["PASS", "PARTIAL", "FAIL"]
    first_fatal_error: Issue | None
    accepted_mathematical_claims: list[str]
    unproved_claims: list[str]
    missing_cases: list[str]
    math_notes: str

    @model_validator(mode="after")
    def coherent(self):
        if self.mathematical_verdict == "PASS" and (
            self.first_fatal_error or self.unproved_claims or self.missing_cases
        ):
            raise ValueError("PASS cannot coexist with unresolved proof obligations")
        if self.mathematical_verdict == "FAIL" and (
            not self.first_fatal_error or self.first_fatal_error.severity != "FATAL"
        ):
            raise ValueError("FAIL must identify a fatal issue")
        if self.mathematical_verdict != "FAIL" and self.first_fatal_error:
            raise ValueError("A fatal issue requires FAIL")
        if self.mathematical_verdict == "PARTIAL" and not self.accepted_mathematical_claims:
            raise ValueError("PARTIAL requires a reusable mathematical claim")
        if set(self.accepted_mathematical_claims) & set(self.unproved_claims):
            raise ValueError("A claim cannot be both established and unproved")
        return self


ProvenanceKind = Literal[
    "PROVED_BY_US", "KNOWN_IN_LITERATURE", "REPRODUCED_BY_US",
    "COMPUTATIONALLY_VERIFIED", "EXPERIMENTAL_ONLY", "UNVERIFIED",
]


class Provenance(StrictModel):
    claim_id: str
    categories: list[ProvenanceKind] = Field(min_length=1)
    evidence_sufficient: bool
    permitted_by_rules: bool
    relies_on_external_result: bool
    uses_computation_as_proof: bool
    references: list[str]
    notes: str


class EvidenceReport(StrictModel):
    evidence_verdict: Literal["PASS", "PARTIAL", "FAIL"]
    source_issues: list[Issue]
    computation_issues: list[Issue]
    rule_violations: list[Issue]
    claim_provenance: list[Provenance]
    reproducibility_notes: str

    @model_validator(mode="after")
    def coherent(self):
        issues = self.source_issues + self.computation_issues + self.rule_violations
        fatal = any(i.severity == "FATAL" for i in issues)
        if (self.evidence_verdict == "FAIL") != fatal:
            raise ValueError("FAIL must correspond to an explicit fatal evidence issue")
        if self.evidence_verdict == "PASS" and any(i.severity != "INFO" for i in issues):
            raise ValueError("PASS cannot have missing or fatal evidence")
        ids = [c.claim_id for c in self.claim_provenance]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate provenance entries")
        if self.evidence_verdict == "PASS" and any(
            not p.evidence_sufficient or not p.permitted_by_rules
            or "UNVERIFIED" in p.categories or "EXPERIMENTAL_ONLY" in p.categories
            for p in self.claim_provenance
        ):
            raise ValueError("PASS requires sufficient, permitted provenance")
        return self


R = TypeVar("R", bound=StrictModel)


class AgentEnvelope(StrictModel, Generic[R]):
    # Keeps PASS/PARTIAL/FAIL intact. Inability to assess is NOT mathematical FAIL.
    report: R | None
    limitation: str | None

    @model_validator(mode="after")
    def coherent(self):
        if self.report is None and not self.limitation:
            raise ValueError("An unavailable report needs a limitation")
        if self.report is not None and self.limitation is not None:
            raise ValueError("Return a report OR a limitation")
        return self


class MathSummary(StrictModel):
    verdict: str
    first_fatal_error: Issue | None
    accepted_claims: list[str]
    unproved_claims: list[str]
    missing_cases: list[str]


class EvidenceSummary(StrictModel):
    verdict: str
    source_issues: list[Issue]
    computation_issues: list[Issue]
    rule_violations: list[Issue]
    claim_provenance: list[Provenance]


class FinalReport(StrictModel):
    final_verdict: Literal["ACCEPT", "PARTIAL_PROGRESS", "REJECT",
                           "COUNTEREXAMPLE_FOUND", "KNOWN_OPEN", "UNKNOWN_STATUS"]
    # Snapshot only. This package NEVER advances the frontier itself.
    highest_verified_cell: int
    math_review: MathSummary
    evidence_review: EvidenceSummary
    accepted_progress: list[Claim]
    blocking_issue: str
    next_required_step: str
    stagnation_signal: bool
