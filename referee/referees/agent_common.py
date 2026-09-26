import asyncio
import json
from importlib.resources import files
from .contracts import AgentEnvelope, ReviewInput
from .provider import JSONBackend
from .trust import TrustedContext


async def call_agent(role, report_class, job: ReviewInput, backend: JSONBackend,
                     trusted: TrustedContext, timeout: float):
    envelope = AgentEnvelope[report_class]
    prompt = files("referees").joinpath(f"prompts/{role.lower()}.md").read_text()
    # Fresh deep JSON copy for each call; no other referee's output or history.
    payload = json.loads(job.model_dump_json())
    if role == "A":
        payload.pop("rules")
    payload = {"submission": payload,
               "trusted_observations": list(trusted.evidence_observations)}
    try:
        raw = await asyncio.wait_for(backend.generate(
            role=role, system=prompt, payload=payload,
            schema=envelope.model_json_schema()), timeout=timeout)
        return envelope.model_validate(raw)
    except Exception as exc:
        # Operational/parse errors never become mathematical FAIL.
        return envelope(report=None, limitation=f"{role}: {type(exc).__name__}")
