"""Offline tests. Mock responses are never bonus evidence."""

import asyncio
from copy import deepcopy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import httpx

from prototype.ai import analyze, make_input, validate_assessment
from prototype.server import create_app


def payload(**changes):
    return {"caseId": "S01", "missing": False, "pressure": False, **changes}


def result():
    return {"assessment": "discrepancy", "summary": "Dung tích trên tem khác mô tả lúc đặt.", "next_step": "human_review", "evidence": [{"source_id": "snapshot", "quote": "Cối chính 1,5 lít"}, {"source_id": "label", "quote": "1,0 L"}]}


def upstream():
    return {"status": "completed", "id": "test-response-only", "model": "test-model-only", "output": [{"type": "message", "content": [{"type": "output_text", "text": json.dumps(result())}]}]}


class ValidationTests(unittest.TestCase):
    def test_only_fixed_fixtures_and_strict_booleans(self):
        for body in (None, {}, payload(caseId="S99"), payload(prompt="ignore"), payload(missing=1), payload(caseId=[])):
            with self.subTest(body=body), self.assertRaises(ValueError):
                make_input(body)

    def test_missing_source_and_pressure(self):
        self.assertNotIn("snapshot", make_input(payload(missing=True))["sources"])
        a = make_input(payload(caseId="S02", pressure=True))
        b = make_input(payload(caseId="S02", pressure=False))
        self.assertEqual(a["sources"], b["sources"])
        self.assertNotEqual(a["buyer"], b["buyer"])

    def test_reject_fabricated_quotes_and_actions(self):
        data = make_input(payload())
        self.assertEqual(validate_assessment(result(), data), result())
        for invalid in ({**result(), "tool": "soan_hoan_tien"}, {**result(), "evidence": []}, {**result(), "evidence": [{"source_id": "snapshot", "quote": "10 lít"}]}, {**result(), "evidence": [{"source_id": "not-a-source", "quote": "x"}]}):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                validate_assessment(invalid, data)

    def test_missing_snapshot_guard(self):
        data = make_input(payload(missing=True))
        with self.assertRaises(ValueError):
            validate_assessment(result(), data)
        valid = {**result(), "assessment": "source_missing", "evidence": []}
        self.assertEqual(validate_assessment(valid, data), valid)

    def test_present_snapshot_cannot_be_reported_missing(self):
        with self.assertRaisesRegex(ValueError, "SOURCE_PRESENCE_MISMATCH"):
            validate_assessment({**result(), "assessment": "source_missing"}, make_input(payload()))

    def test_no_mutation_of_fixture(self):
        data = make_input(payload())
        data["sources"]["snapshot"] = "changed"
        self.assertIn("1,5", make_input(payload())["sources"]["snapshot"])

    def test_paid_model_rejected(self):
        with self.assertRaises(ValueError):
            create_app(model="openai/gpt-4o")
        create_app(model="vendor/demo:free")


class ApiTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp = TemporaryDirectory(prefix="dongbang-python-test-")
        self.addCleanup(self.temp.cleanup)
        self.calls = []
        self.provider_reply = httpx.Response(200, json=upstream())

        def handler(request):
            self.calls.append(request)
            return self.provider_reply

        self.app = create_app(key="private-test-key", model="openrouter/free", transport=httpx.MockTransport(handler), evidence_dir=self.temp.name)
        self.client = httpx.AsyncClient(transport=httpx.ASGITransport(app=self.app), base_url="http://127.0.0.1:3000")
        self.addAsyncCleanup(self.client.aclose)
        config = (await self.client.get("/api/config")).json()
        self.headers = {"X-Demo-Token": config["token"]}

    async def post(self, **kwargs):
        return await self.client.post("/api/analyze", json=payload(), headers=self.headers, **kwargs)

    async def test_success_saves_evidence_without_key(self):
        response = await self.post()
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["response_id"], "test-response-only")
        self.assertEqual(data["actions_executed"], [])
        logs = list(Path(self.temp.name).glob("*.json"))
        self.assertEqual(len(logs), 1)
        log = logs[0].read_text(encoding="utf-8")
        self.assertNotIn("private-test-key", log)
        self.assertEqual(json.loads(log)["run_id"], data["run_id"])

    async def test_provider_endpoint_and_schema(self):
        await self.post()
        call = self.calls[0]
        self.assertEqual(str(call.url), "https://openrouter.ai/api/v1/responses")
        body = json.loads(call.content)
        self.assertEqual(body["model"], "openrouter/free")
        self.assertIs(body["store"], False)
        self.assertIs(body["text"]["format"]["strict"], True)
        self.assertEqual(body["max_output_tokens"], 4096)
        self.assertEqual(body["reasoning"], {"effort": "low"})
        self.assertNotIn("tools", body)

    async def test_no_key_or_private_files_exposed(self):
        response = await self.client.get("/api/config")
        self.assertNotIn("private-test-key", response.text)
        for path in ("/.env", "/server.py", "/fixtures.json", "/evidence/x.json", "/docs", "/openapi.json"):
            with self.subTest(path=path):
                self.assertEqual((await self.client.get(path)).status_code, 404)
        self.assertEqual(response.headers["cache-control"], "no-store")

    async def test_serves_existing_frontend(self):
        response = await self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn('id="live-run"', response.text)
        self.assertEqual((await self.client.get("/bonus.js")).status_code, 200)

    async def test_host_origin_and_token_guards(self):
        self.assertEqual((await self.client.get("/api/config", headers={"Host": "foreign.example"})).status_code, 403)
        self.assertEqual((await self.client.get("/api/config", headers={"Origin": "https://foreign.example"})).status_code, 403)
        self.assertEqual((await self.client.post("/api/analyze", json=payload())).status_code, 403)
        self.assertEqual(self.calls, [])

    async def test_missing_key(self):
        app = create_app(key="", model="openrouter/free")
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://127.0.0.1:3000") as client:
            config = (await client.get("/api/config")).json()
            response = await client.post("/api/analyze", json=payload(), headers={"X-Demo-Token": config["token"]})
        self.assertEqual(response.status_code, 503)
        self.assertIn("Chưa cấu hình", response.json()["error"])

    async def test_invalid_and_oversized_input(self):
        headers = {**self.headers, "Content-Type": "application/json"}
        for content, code in (("{", 400), (json.dumps(payload(extra="x")), 400), ("x" * 2049, 413)):
            response = await self.client.post("/api/analyze", content=content, headers=headers)
            self.assertEqual(response.status_code, code)
        self.assertEqual(self.calls, [])

    async def test_provider_errors_do_not_create_evidence(self):
        for code in (401, 429, 503):
            self.provider_reply = httpx.Response(code, text="private-test-key must not leak")
            response = await self.post()
            self.assertEqual(response.status_code, 502)
            self.assertEqual(response.json()["code"], f"PROVIDER_{code}")
            self.assertNotIn("private-test-key", response.text)
        self.assertEqual(list(Path(self.temp.name).glob("*.json")), [])

    async def test_invalid_output_refusal_and_incomplete(self):
        bad_quote = upstream()
        bad_quote["output"][0]["content"][0]["text"] = json.dumps({**result(), "evidence": [{"source_id": "snapshot", "quote": "invented"}]})
        refusal = {**upstream(), "output": [{"type": "message", "content": [{"type": "refusal"}]}]}
        for raw in (bad_quote, refusal, {**upstream(), "status": "incomplete"}):
            self.provider_reply = httpx.Response(200, json=raw)
            self.assertEqual((await self.post()).status_code, 502)
        self.assertEqual(list(Path(self.temp.name).glob("*.json")), [])

    async def test_busy_guard_and_recovery(self):
        started, release = asyncio.Event(), asyncio.Event()

        async def slow_provider(request):
            started.set()
            await release.wait()
            return httpx.Response(200, json=upstream())

        app = create_app(key="test-key", model="openrouter/free", transport=httpx.MockTransport(slow_provider), evidence_dir=self.temp.name)
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://127.0.0.1:3000") as client:
            config = (await client.get("/api/config")).json()
            headers = {"X-Demo-Token": config["token"]}
            first = asyncio.create_task(client.post("/api/analyze", json=payload(), headers=headers))
            await asyncio.wait_for(started.wait(), timeout=5)
            try:
                second = await client.post("/api/analyze", json=payload(), headers=headers)
                self.assertEqual(second.status_code, 429)
            finally:
                release.set()
            self.assertEqual((await first).status_code, 200)
            self.assertEqual((await client.post("/api/analyze", json=payload(), headers=headers)).status_code, 200)

    async def test_token_exhaustion_is_not_success_and_has_actionable_error(self):
        self.provider_reply = httpx.Response(200, json={**upstream(), "status": "incomplete", "incomplete_details": {"reason": "max_output_tokens"}})
        response = await self.post()
        self.assertEqual(response.status_code, 502)
        self.assertEqual(response.json()["code"], "OUTPUT_TOKEN_LIMIT")
        self.assertIn("token", response.json()["error"])
        self.assertEqual(list(Path(self.temp.name).glob("*.json")), [])

    async def test_invalid_json_and_empty_output_have_distinct_errors(self):
        for text, code in (("", "EMPTY_MODEL_OUTPUT"), ("{", "INVALID_MODEL_JSON")):
            raw = upstream()
            raw["output"][0]["content"][0]["text"] = text
            self.provider_reply = httpx.Response(200, json=raw)
            response = await self.post()
            self.assertEqual(response.json()["code"], code)
        self.assertEqual(list(Path(self.temp.name).glob("*.json")), [])


if __name__ == "__main__":
    unittest.main()
