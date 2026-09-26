"""Deterministic decisions. No model call and no state writes in this module."""
from .contracts import (
    AgentEnvelope, EvidenceReport, EvidenceSummary, FinalReport,
    MathReport, MathSummary, ReviewInput,
)
from .trust import HistoryEntry, TrustedContext, submission_digest


def _validate_ids(job, a, b):
    candidate_ids = {c.id for c in job.candidate.claims}
    known = candidate_ids | {c.id for c in job.state.claims}
    if a:
        if not set(a.accepted_mathematical_claims) <= candidate_ids:
            return "A references unregistered accepted claims"
        if not set(a.unproved_claims) <= known:
            return "A references unregistered unproved claims"
        if a.first_fatal_error and not set(a.first_fatal_error.claim_ids) <= known:
            return "A issue references an unknown claim"
        if a.mathematical_verdict == "PASS" and job.cell.target_claim_id not in a.accepted_mathematical_claims:
            return "A PASS does not establish the exact target"
    if b:
        if not {p.claim_id for p in b.claim_provenance} <= candidate_ids:
            return "B references unregistered provenance"
        for issue in b.source_issues + b.computation_issues + b.rule_violations:
            if not set(issue.claim_ids) <= known:
                return "B issue references an unknown claim"
        if b.evidence_verdict == "PASS" and {p.claim_id for p in b.claim_provenance} != candidate_ids:
            return "B PASS does not cover every declared claim"
    return None


def _safe_claims(job, a, b, trusted, digest, refuted):
    if not a or not b:
        return []
    claims = {c.id: c for c in job.candidate.claims}
    approved = set(a.accepted_mathematical_claims)
    supported = {
        p.claim_id for p in b.claim_provenance
        if p.evidence_sufficient and p.permitted_by_rules
        and not {"UNVERIFIED", "EXPERIMENTAL_ONLY"}.intersection(p.categories)
        and (job.rules.allow_literature_as_proof or not p.relies_on_external_result)
        and (job.rules.allow_computation or not p.uses_computation_as_proof)
    }
    kinds = {"LEAN", "EXACT_CERTIFICATE"}
    if not job.rules.require_machine_verification:
        kinds.add("HUMAN_REVIEW")
    if not job.rules.allow_computation:
        kinds.discard("EXACT_CERTIFICATE")
    certified = {r.claim_id for r in trusted.records
                 if r.submission_digest == digest and r.kind in kinds
                 and r.evidence_reference.strip()}
    issues = b.source_issues + b.computation_issues + b.rule_violations
    if a.first_fatal_error:
        issues = issues + [a.first_fatal_error]
    blocking = [i for i in issues if i.severity != "INFO"]
    # Unscoped issues may affect the entire submission. Do not guess independence.
    if any(not i.claim_ids for i in blocking):
        return []
    excluded = refuted | {cid for i in blocking for cid in i.claim_ids}
    pending = (approved & supported & certified) - excluded
    established = {c.id for c in job.state.claims}
    retained = []
    while pending:
        ready = sorted(cid for cid in pending if set(claims[cid].depends_on) <= established)
        if not ready:  # Unverified dependencies or a dependency cycle.
            break
        for cid in ready:
            retained.append(claims[cid])
            established.add(cid)
            pending.remove(cid)
    return retained


def merge_reports(job: ReviewInput, math: AgentEnvelope[MathReport],
                  evidence: AgentEnvelope[EvidenceReport],
                  trusted: TrustedContext | None = None) -> FinalReport:
    trusted = trusted or TrustedContext()
    a, b = math.report, evidence.report
    digest = submission_digest(job)
    candidate_ids = {c.id for c in job.candidate.claims}
    counterexamples = [c for c in trusted.counterexamples
                       if c.submission_digest == digest and c.claim_id in candidate_ids
                       and c.evidence_reference.strip()]
    refuted = {c.claim_id for c in counterexamples}
    binding_error = _validate_ids(job, a, b)
    kept = [] if binding_error else _safe_claims(job, a, b, trusted, digest, refuted)
    kept_ids = {c.id for c in kept}
    target = job.cell.target_claim_id
    opens = trusted.open_status
    open_matches = bool(opens and opens.submission_digest == digest
                        and opens.target_claim_id == target
                        and opens.source_reference.strip() and opens.checked_on.strip())
    conflicting_certificates = refuted & {
        r.claim_id for r in trusted.records
        if r.submission_digest == digest and r.evidence_reference.strip()
    }
    verdict = "UNKNOWN_STATUS"
    blocker = "No independently verified progress or complete target proof"
    next_step = "Provide the missing review or independently checked evidence"
    key = "UNVERIFIED"

    if conflicting_certificates or (open_matches and target in kept_ids):
        kept = []
        blocker = "Conflicting trusted evidence: investigate before any state update"
        next_step = "Audit the external verification records"
        key = "TRUST_CONFLICT"
    elif counterexamples:
        verdict = "COUNTEREXAMPLE_FOUND"
        blocker = "Verified counterexample to declared claim(s): " + ", ".join(sorted(refuted))
        next_step = "Withdraw the refuted claim(s) and invalidate dependent arguments"
        key = "COUNTEREXAMPLE:" + ",".join(sorted(refuted))
    elif binding_error:
        blocker, next_step, key = binding_error, "Regenerate a contract-valid report", "CONTRACT_ERROR"
    elif (a and a.mathematical_verdict == "FAIL") or (b and b.evidence_verdict == "FAIL"):
        verdict = "REJECT"
        causes = []
        if a and a.mathematical_verdict == "FAIL":
            causes.append(("A", a.first_fatal_error))
        if b and b.evidence_verdict == "FAIL":
            issues = b.source_issues + b.computation_issues + b.rule_violations
            causes.append(("B", next(i for i in issues if i.severity == "FATAL")))
        blocker = "; ".join(f"Referee {role}: {issue.detail}" for role, issue in causes)
        role, issue = causes[0]
        key = f"{role}:{issue.code}:" + ",".join(sorted(issue.claim_ids))
        next_step = "Address the stated blocking obligation without silently changing the target"
    elif a and b and a.mathematical_verdict == "PASS" and b.evidence_verdict == "PASS" and target in kept_ids:
        verdict, blocker, next_step, key = "ACCEPT", "", "Orchestrator may record the solved cell", ""
    elif kept:
        verdict = "PARTIAL_PROGRESS"
        blocker = "Only the listed claims have passed both reviews and external checks"
        next_step = "Complete the unresolved target obligations or evidence checks"
        key = "PARTIAL:" + target
    elif open_matches and not (a and a.mathematical_verdict == "PASS"):
        verdict = "KNOWN_OPEN"
        blocker = f"Exact target documented open as of {opens.checked_on}: {opens.source_reference}"
        next_step = "Orchestrator assesses dependent cells; do not infer every later cell is blocked"
        key = "KNOWN_OPEN:" + target
    elif not a or not b:
        blocker = "; ".join(x for x in (math.limitation, evidence.limitation) if x)
        key = "REVIEW_UNAVAILABLE"
    elif a.mathematical_verdict == "PASS" and b.evidence_verdict == "PASS":
        blocker = "Both reviewers passed; independent verification or dependency closure is missing"
        next_step = "Run an independent checker on the exact target and its declared dependencies"
        key = "CERTIFICATE_MISSING:" + target

    current = HistoryEntry(job.problem_id, job.cell.id, job.candidate.attempt_id,
                           job.candidate.method_tag, key, tuple(c.id for c in kept))
    # Only authenticated history from this problem and cell, distinct attempts.
    previous = {}
    for h in trusted.history:
        if h.problem_id == job.problem_id and h.cell_id == job.cell.id and h.attempt_id != current.attempt_id:
            previous[h.attempt_id] = h
    recent = list(previous.values())[-2:] + [current]
    stagnant = verdict != "ACCEPT" and len(recent) == 3 and (
        all(not h.new_verified_claim_ids for h in recent)
        or bool(key and all(h.blocking_key == key for h in recent))
    )
    return FinalReport(
        final_verdict=verdict,
        highest_verified_cell=job.state.highest_verified_cell,
        math_review=MathSummary(
            verdict=a.mathematical_verdict if a else "UNAVAILABLE",
            first_fatal_error=a.first_fatal_error if a else None,
            accepted_claims=a.accepted_mathematical_claims if a else [],
            unproved_claims=a.unproved_claims if a else [],
            missing_cases=a.missing_cases if a else []),
        evidence_review=EvidenceSummary(
            verdict=b.evidence_verdict if b else "UNAVAILABLE",
            source_issues=b.source_issues if b else [],
            computation_issues=b.computation_issues if b else [],
            rule_violations=b.rule_violations if b else [],
            claim_provenance=b.claim_provenance if b else []),
        accepted_progress=kept, blocking_issue=blocker,
        next_required_step=next_step, stagnation_signal=stagnant,
    )
