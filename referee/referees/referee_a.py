from .agent_common import call_agent
from .contracts import MathReport, ReviewInput
from .provider import JSONBackend
from .trust import TrustedContext


async def review_math(job: ReviewInput, backend: JSONBackend,
                      trusted: TrustedContext, timeout: float = 100):
    return await call_agent("A", MathReport, job, backend, trusted, timeout)
