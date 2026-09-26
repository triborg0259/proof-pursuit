"""Fast two-referee review, optional exact checks, explicit human approval.

The approval key belongs ONLY to the human-control process, never a model worker.
No submitted Python code is executed and no approval is fabricated by a model.
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import hmac
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal
from pydantic import Field
from .contracts import AgentEnvelope, EvidenceReport, FinalReport, MathReport, ReviewInput, StrictModel
from .exact import CheckResult, run_checks
from .merge import merge_reports, _validate_ids
from .referee_a import review_math
from .referee_b import review_evidence
from .trust import TrustedContext, VerifiedRecord, submission_digest


class ReviewPacket(StrictModel):
    job: ReviewInput
    submission_digest: str
    math: AgentEnvelope[MathReport]
    evidence: AgentEnvelope[EvidenceReport]
    checks: list[CheckResult]
    check_errors: list[str]
    report: FinalReport
    review_status: Literal["READY_FOR_HUMAN", "NEEDS_WORK", "INCOMPLETE"]
    proposed_claim_ids: list[str]


class HumanApproval(StrictModel):
    packet_digest: str
    reviewer: str = Field(min_length=1)
    approved_claim_ids: list[str] = Field(min_length=1)
    reason: str = Field(min_length=1)
    approved_at: str
    signature: str


def packet_digest(packet: ReviewPacket) -> str:
    data = json.dumps(packet.model_dump(mode="json"), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(data.encode()).hexdigest()


def _observations(checks):
    return tuple(c.model_dump_json() for c in checks)


def proposed_claims(job, a, b, checks):
    if not a.report or not b.report:
        return []
    known = {c.id for c in job.candidate.claims}
    good = {p.claim_id for p in b.report.claim_provenance
            if p.evidence_sufficient and p.permitted_by_rules
            and not {"EXPERIMENTAL_ONLY", "UNVERIFIED"}.intersection(p.categories)
            and (job.rules.allow_literature_as_proof or not p.relies_on_external_result)
            and (job.rules.allow_computation or not p.uses_computation_as_proof)}
    issues = b.report.source_issues + b.report.computation_issues + b.report.rule_violations
    if a.report.first_fatal_error:
        issues.append(a.report.first_fatal_error)
    blocking = [i for i in issues if i.severity != "INFO"]
    if any(not i.claim_ids for i in blocking):
        return []
    bad = {cid for i in blocking for cid in i.claim_ids}
    bad |= {c.claim_id for c in checks if c.status != "MATCH"}
    eligible = (set(a.report.accepted_mathematical_claims) & good & known) - bad
    # These are suggestions for a human, NOT verified progress.
    return sorted(eligible)


async def prepare_review(job: ReviewInput, backend=None, checks: list[dict] | None = None,
                         timeout: float = 60, check_timeout: float = 5,
                         trusted: TrustedContext | None = None) -> ReviewPacket:
    trusted = trusted or TrustedContext()
    results, errors = [], []
    try:
        results = run_checks(checks or [], allowed_claim_ids={c.id for c in job.candidate.claims},
                             timeout_seconds=check_timeout)
    except (ValueError, TypeError) as exc:
        errors = [str(exc)]
    context = TrustedContext(history=trusted.history,
        evidence_observations=trusted.evidence_observations + _observations(results))
    if backend is None:
        a = AgentEnvelope[MathReport](report=None, limitation="Offline: no mathematical model review was run")
        b = AgentEnvelope[EvidenceReport](report=None, limitation="Offline: no evidence model review was run")
    else:
        a, b = await asyncio.gather(
            review_math(job.model_copy(deep=True), backend, context, timeout),
            review_evidence(job.model_copy(deep=True), backend, context, timeout))
    report = merge_reports(job, a, b, context)
    failed_checks = [r for r in results if r.status in {"MISMATCH", "INVALID"}]
    incomplete = [r for r in results if r.status == "INCONCLUSIVE"]
    if failed_checks:
        report.final_verdict = "REJECT"
        report.blocking_issue = "Computational submission issue: " + "; ".join(
            f"{c.claim_id}: {c.status}: {c.checked_assertion}" for c in failed_checks)
        report.next_required_step = "Correct the checked expectation or clarify its scope; this alone does not refute the whole theorem"
    if (errors or incomplete) and report.final_verdict != "REJECT":
        report.final_verdict = "UNKNOWN_STATUS"
        report.blocking_issue = "Exact checks invalid or unfinished: " + "; ".join(errors + [c.checked_assertion for c in incomplete])
        report.next_required_step = "Provide valid bounded checker inputs; do not infer mathematical falsity from a tool failure"
    suggestions = proposed_claims(job, a, b, results) if not errors else []
    status = "NEEDS_WORK" if report.final_verdict == "REJECT" else "INCOMPLETE"
    if a.report and b.report and a.report.mathematical_verdict == "PASS" and b.report.evidence_verdict == "PASS" and not _validate_ids(job, a.report, b.report) and not errors and not incomplete and not failed_checks:
        status = "READY_FOR_HUMAN"
        report.blocking_issue = "Both model reviews passed. A human must read and approve the argument; this is not formal verification."
        report.next_required_step = "Human reviews the exact target, proof and evidence, then approves explicit claims"
    # No automatic ACCEPT/PARTIAL_PROGRESS in the preapproval path.
    report.accepted_progress = []
    return ReviewPacket(job=job, submission_digest=submission_digest(job), math=a,
                        evidence=b, checks=results, check_errors=errors,
                        report=report, review_status=status, proposed_claim_ids=suggestions)


def _signature(data: dict, secret: str) -> str:
    if len(secret) < 32:
        raise ValueError("Human approval secret must contain at least 32 characters")
    payload = json.dumps(data, sort_keys=True, separators=(",", ":")).encode()
    return hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()


def sign_human_approval(packet: ReviewPacket, *, reviewer: str, claim_ids: list[str],
                        reason: str, secret: str) -> HumanApproval:
    # Call ONLY after actual human review in the isolated human-control process.
    if packet.job.rules.require_machine_verification:
        raise ValueError("Protected policy requires machine verification: human review cannot override it")
    if not reviewer.strip() or not reason.strip():
        raise ValueError("Human identity and review reason are required")
    if packet.submission_digest != submission_digest(packet.job):
        raise ValueError("Stale submission digest")
    if packet.check_errors:
        raise ValueError("Unresolved check input errors")
    eligible = set(proposed_claims(packet.job, packet.math, packet.evidence, packet.checks))
    if not claim_ids or len(claim_ids) != len(set(claim_ids)) or not set(claim_ids) <= eligible:
        raise ValueError("Approval includes an unreviewed or blocked claim")
    if packet.job.cell.target_claim_id in claim_ids and packet.review_status != "READY_FOR_HUMAN":
        raise ValueError("The complete target is not ready for human approval")
    data = dict(packet_digest=packet_digest(packet), reviewer=reviewer,
                approved_claim_ids=claim_ids, reason=reason,
                approved_at=datetime.now(timezone.utc).isoformat())
    return HumanApproval(**data, signature=_signature(data, secret))


def finalize_review(packet: ReviewPacket, approval: HumanApproval, *, secret: str,
                    current_job: ReviewInput) -> FinalReport:
    # current_job must be reread from protected orchestrator state.
    unsigned = approval.model_dump(exclude={"signature"})
    if not hmac.compare_digest(approval.signature, _signature(unsigned, secret)):
        raise ValueError("Invalid human approval signature")
    if approval.packet_digest != packet_digest(packet):
        raise ValueError("Approval does not match this review packet")
    if packet.submission_digest != submission_digest(current_job) or packet.submission_digest != submission_digest(packet.job):
        raise ValueError("Submission changed after human review")
    if current_job.rules.require_machine_verification:
        raise ValueError("Human approval cannot satisfy a machine-verification policy")
    eligible = set(proposed_claims(current_job, packet.math, packet.evidence, packet.checks))
    if packet.check_errors or not set(approval.approved_claim_ids) <= eligible:
        raise ValueError("Approved claims are blocked")
    if current_job.cell.target_claim_id in approval.approved_claim_ids and packet.review_status != "READY_FOR_HUMAN":
        raise ValueError("The target was not ready for human approval")
    context = TrustedContext(records=tuple(VerifiedRecord(
        submission_digest(current_job), cid, "HUMAN_REVIEW",
        f"Human {approval.reviewer} at {approval.approved_at}; packet {approval.packet_digest}; {approval.reason}")
        for cid in approval.approved_claim_ids))
    return merge_reports(current_job, packet.math, packet.evidence, context)


async def main():
    parser = argparse.ArgumentParser(description="Fast review; ACCEPT always requires signed human approval")
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run")
    run.add_argument("input", type=Path)
    run.add_argument("--checks", type=Path)
    run.add_argument("--offline", action="store_true")
    run.add_argument("--model", default=os.getenv("ANTHROPIC_MODEL"))
    run.add_argument("--model-b", default=os.getenv("ANTHROPIC_MODEL_B"))
    run.add_argument("--timeout", type=float, default=60)
    run.add_argument("--max-tokens", type=int, default=2500)
    approve = sub.add_parser("approve")
    approve.add_argument("packet", type=Path)
    approve.add_argument("--reviewer", required=True)
    approve.add_argument("--claims", required=True, help="Comma-separated claim IDs")
    approve.add_argument("--reason", required=True)
    final = sub.add_parser("finalize")
    final.add_argument("packet", type=Path)
    final.add_argument("approval", type=Path)
    final.add_argument("--current-input", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "run":
        job = ReviewInput.model_validate_json(args.input.read_text())
        raw = json.loads(args.checks.read_text()) if args.checks else []
        if args.offline:
            packet = await prepare_review(job, checks=raw)
        else:
            if not args.model:
                parser.error("Set ANTHROPIC_MODEL or --model; use --offline for checker-only mode")
            from .provider import ClaudeBackend
            backend = ClaudeBackend(args.model, args.model_b, args.max_tokens, args.timeout)
            try:
                packet = await prepare_review(job, backend, raw, timeout=args.timeout)
                print(json.dumps({"usage": backend.usage}), file=sys.stderr)
            finally:
                await backend.close()
        print(packet.model_dump_json(indent=2))
    else:
        secret = os.getenv("REFEREE_APPROVAL_SECRET", "")
        if len(secret) < 32:
            parser.error("Set REFEREE_APPROVAL_SECRET in the HUMAN CONTROL process only (32+ chars)")
        packet = ReviewPacket.model_validate_json(args.packet.read_text())
        if args.command == "approve":
            if not sys.stdin.isatty():
                parser.error("Approval requires an interactive human terminal; no --yes bypass")
            print(f"Read the packet. Target: {packet.job.cell.statement}\nStatus: {packet.review_status}\nClaims: {args.claims}", file=sys.stderr)
            phrase = "APPROVE " + packet_digest(packet)[:12]
            print(f"Type exactly {phrase} to attest you reviewed these claims:", file=sys.stderr)
            if input().strip() != phrase:
                parser.error("Approval cancelled")
            receipt = sign_human_approval(packet, reviewer=args.reviewer,
                claim_ids=[s.strip() for s in args.claims.split(",")], reason=args.reason, secret=secret)
            print(receipt.model_dump_json(indent=2))
        else:
            receipt = HumanApproval.model_validate_json(args.approval.read_text())
            current = ReviewInput.model_validate_json(args.current_input.read_text())
            result = finalize_review(packet, receipt, secret=secret, current_job=current)
            print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
