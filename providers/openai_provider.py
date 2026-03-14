"""
OpenAI Provider — GPT-4o
Uses the Responses API with web_search_preview tool for URL intelligence.
Falls back to chat completions for generation (no search needed).
"""

import json
import requests
from .base import BaseProvider, ProviderError
from .anthropic_provider import (
    _build_scan_prompt, _dashboard_prompt, _roadmap_prompt,
    _document_prompt, _parse_json_response,
    _scan_system, _generation_system
)

CHAT_MODEL = "gpt-4o"
RESPONSES_MODEL = "gpt-4o"
CHAT_URL = "https://api.openai.com/v1/chat/completions"
RESPONSES_URL = "https://api.openai.com/v1/responses"


class OpenAIProvider(BaseProvider):

    def _headers(self, api_key: str) -> dict:
        return {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def scan(self, url: str, api_key: str) -> dict:
        """
        Use OpenAI Responses API with web_search_preview tool.
        Falls back to chat completions if responses API unavailable.
        """
        prompt = _build_scan_prompt(url)
        system = _scan_system()

        # Try Responses API first (has web search)
        try:
            body = {
                "model": RESPONSES_MODEL,
                "tools": [{"type": "web_search_preview"}],
                "input": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
            }
            resp = requests.post(RESPONSES_URL, headers=self._headers(api_key), json=body, timeout=120, verify=False)
            if resp.ok:
                data = resp.json()
                # Extract text from output blocks
                raw = ""
                for block in data.get("output", []):
                    if block.get("type") == "message":
                        for part in block.get("content", []):
                            if part.get("type") == "output_text":
                                raw += part.get("text", "")
                if raw:
                    return _parse_json_response(raw, url)
        except Exception:
            pass

        # Fallback — Chat Completions (no live search, but still useful)
        return self._chat_scan(url, api_key, system, prompt)

    def _chat_scan(self, url: str, api_key: str, system: str, prompt: str) -> dict:
        """Chat completions fallback — Claude will reason about the URL without live browsing."""
        body = {
            "model": CHAT_MODEL,
            "max_tokens": 4000,
            "messages": [
                {"role": "system", "content": system + "\nNote: You do not have live web access for this request. Reason from your training knowledge about this organisation if possible, or return a best-effort structure."},
                {"role": "user", "content": prompt},
            ],
        }
        resp = requests.post(CHAT_URL, headers=self._headers(api_key), json=body, timeout=120, verify=False)
        if not resp.ok:
            try:
                err = resp.json().get("error", {}).get("message", resp.text)
            except Exception:
                err = resp.text
            raise ProviderError(f"OpenAI API error {resp.status_code}: {err}")
        data = resp.json()
        raw = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        return _parse_json_response(raw, url)

    def _chat_call(self, api_key: str, system: str, prompt: str, max_tokens: int = 4000) -> str:
        body = {
            "model": CHAT_MODEL,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
        }
        resp = requests.post(CHAT_URL, headers=self._headers(api_key), json=body, timeout=120, verify=False)
        if not resp.ok:
            try:
                err = resp.json().get("error", {}).get("message", resp.text)
            except Exception:
                err = resp.text
            raise ProviderError(f"OpenAI API error {resp.status_code}: {err}")
        return resp.json().get("choices", [{}])[0].get("message", {}).get("content", "")

    def generate(self, context: dict, api_key: str) -> dict:
        system = _generation_system()
        results = {}

        r1 = self._chat_call(api_key, system, _dashboard_prompt(context), max_tokens=3000)
        results["dashboard"] = _parse_json_response(r1)

        r2 = self._chat_call(api_key, system, _roadmap_prompt(context, results.get("dashboard")), max_tokens=3000)
        results["roadmap"] = _parse_json_response(r2)

        r3 = self._chat_call(api_key, system, _document_prompt(context, results.get("dashboard")), max_tokens=4000)
        results["document"] = _parse_json_response(r3)

        return results
