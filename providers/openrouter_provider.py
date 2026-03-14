"""
OpenRouter Provider — pass-through to any supported model.
OpenRouter uses OpenAI-compatible chat completions API.
No native web search — uses prompt-based URL analysis.
Recommended models: anthropic/claude-sonnet-4-5, openai/gpt-4o, google/gemini-pro-1.5
"""

import requests
from .base import BaseProvider, ProviderError
from .anthropic_provider import (
    _build_scan_prompt, _dashboard_prompt, _roadmap_prompt,
    _document_prompt, _parse_json_response,
    _scan_system, _generation_system
)

API_URL = "https://openrouter.ai/api/v1/chat/completions"
# Default model — user can override by passing model in context
DEFAULT_MODEL = "anthropic/claude-sonnet-4-5"


class OpenRouterProvider(BaseProvider):

    def _headers(self, api_key: str) -> dict:
        return {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://stratiq.local",
            "X-Title": "StratIQ Intelligence Platform",
        }

    def _call(self, api_key: str, model: str, system: str, prompt: str, max_tokens: int = 4000) -> str:
        body = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
        }
        resp = requests.post(API_URL, headers=self._headers(api_key), json=body, timeout=120, verify=False)
        if not resp.ok:
            try:
                err = resp.json().get("error", {}).get("message", resp.text)
            except Exception:
                err = resp.text
            raise ProviderError(f"OpenRouter API error {resp.status_code}: {err}")
        return resp.json().get("choices", [{}])[0].get("message", {}).get("content", "")

    def scan(self, url: str, api_key: str, model: str = DEFAULT_MODEL) -> dict:
        system = _scan_system() + (
            "\nNote: You do not have live web browsing via this route. "
            "Use your training knowledge about this organisation where possible. "
            "If unknown, return a well-structured placeholder that the user can edit."
        )
        prompt = _build_scan_prompt(url)
        raw = self._call(api_key, model, system, prompt, max_tokens=4000)
        return _parse_json_response(raw, url)

    def generate(self, context: dict, api_key: str) -> dict:
        model = context.get("model", DEFAULT_MODEL)
        system = _generation_system()
        results = {}

        r1 = self._call(api_key, model, system, _dashboard_prompt(context), max_tokens=3000)
        results["dashboard"] = _parse_json_response(r1)

        r2 = self._call(api_key, model, system, _roadmap_prompt(context, results.get("dashboard")), max_tokens=3000)
        results["roadmap"] = _parse_json_response(r2)

        r3 = self._call(api_key, model, system, _document_prompt(context, results.get("dashboard")), max_tokens=4000)
        results["document"] = _parse_json_response(r3)

        return results
