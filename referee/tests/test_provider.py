import unittest
from types import SimpleNamespace
from referees.provider import ClaudeBackend


class ProviderTests(unittest.IsolatedAsyncioTestCase):
    def backend(self, response):
        calls = []
        class Messages:
            async def create(self, **kwargs):
                calls.append(kwargs)
                return response
        backend = ClaudeBackend.__new__(ClaudeBackend)
        backend.client = SimpleNamespace(messages=Messages())
        backend.models = {"A": "model-a", "B": "model-b"}
        backend.max_tokens = 100
        backend.usage = []
        return backend, calls

    def response(self, stop="tool_use"):
        return SimpleNamespace(
            id="synthetic", stop_reason=stop,
            usage=SimpleNamespace(model_dump=lambda **kwargs: {"input_tokens": 10, "output_tokens": 20}),
            content=[SimpleNamespace(type="tool_use", name="submit_report", input={"report": None, "limitation": "test"})])

    async def test_single_forced_tool_and_usage_capture(self):
        backend, calls = self.backend(self.response())
        out = await backend.generate(role="B", system="role-b", payload={"proof": "test"}, schema={"type": "object"})
        self.assertEqual(calls[0]["model"], "model-b")
        self.assertEqual(calls[0]["tool_choice"], {"type": "tool", "name": "submit_report"})
        self.assertEqual(len(calls[0]["messages"]), 1)
        self.assertEqual(backend.usage[0]["usage"]["input_tokens"], 10)
        self.assertEqual(out["limitation"], "test")

    async def test_truncation_is_not_a_report(self):
        backend, _ = self.backend(self.response(stop="max_tokens"))
        with self.assertRaises(ValueError):
            await backend.generate(role="A", system="a", payload={}, schema={})
