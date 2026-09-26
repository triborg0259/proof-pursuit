"""Replaceable JSON backend. Independent requests; no conversation memory."""
from typing import Any, Protocol


class JSONBackend(Protocol):
    async def generate(self, *, role: str, system: str, payload: dict,
                       schema: dict) -> dict[str, Any]: ...


class ClaudeBackend:
    def __init__(self, model_a: str, model_b: str | None = None,
                 max_tokens: int = 5000, timeout: float = 90):
        from anthropic import AsyncAnthropic
        # No automatic retries: a call budget should not be silently multiplied.
        self.client = AsyncAnthropic(timeout=timeout, max_retries=0)
        self.models = {"A": model_a, "B": model_b or model_a}
        self.max_tokens = max_tokens
        self.usage: list[dict] = []

    async def generate(self, *, role, system, payload, schema):
        import json
        response = await self.client.messages.create(
            model=self.models[role], max_tokens=self.max_tokens,
            system=system,
            messages=[{"role": "user", "content": json.dumps(payload, ensure_ascii=False)}],
            tools=[{"name": "submit_report", "description": "Submit the review JSON",
                    "input_schema": schema}],
            tool_choice={"type": "tool", "name": "submit_report"},
        )
        self.usage.append({"role": role, "request_id": response.id,
                           "usage": response.usage.model_dump(mode="json")})
        if response.stop_reason != "tool_use":
            raise ValueError("No complete report: refusal, truncation or unexpected stop")
        calls = [b for b in response.content if b.type == "tool_use"]
        if len(calls) != 1 or calls[0].name != "submit_report":
            raise ValueError("Expected exactly one submit_report call")
        return calls[0].input

    async def close(self):
        await self.client.close()
