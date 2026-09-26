import asyncio
from .contracts import ReviewInput
from .merge import merge_reports
from .referee_a import review_math
from .referee_b import review_evidence
from .trust import TrustedContext


async def review(job: ReviewInput, backend, trusted: TrustedContext | None = None,
                 timeout: float = 100):
    trusted = trusted or TrustedContext()
    a, b = await asyncio.gather(
        review_math(job.model_copy(deep=True), backend, trusted, timeout),
        review_evidence(job.model_copy(deep=True), backend, trusted, timeout),
    )
    return merge_reports(job, a, b, trusted)
