from .agent_common import call_agent
from .contracts import EvidenceReport, ReviewInput
from .provider import JSONBackend
from .trust import TrustedContext


async def review_evidence(job: ReviewInput, backend: JSONBackend,
                          trusted: TrustedContext, timeout: float = 100):
    return await call_agent("B", EvidenceReport, job, backend, trusted, timeout)
