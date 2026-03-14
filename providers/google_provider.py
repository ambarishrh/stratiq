"""
Google Provider — Gemini 1.5 Pro / 2.0 Flash
Uses google_search grounding tool for URL intelligence gathering.
"""

import json
import requests
from .base import BaseProvider, ProviderError
from .anthropic_provider import (
    _build_scan_prompt, _dashboard_prompt, _roadmap_prompt,
    _document_prompt, _parse_json_response,
    _scan_system, _generation_system
)

# Use gemini-2.0-flash for speed/cost, gemini-1.5-pro for quality
SCAN_MODEL = "gemini-2.0-flash"
GEN_MODEL = "gemini-1.5-pro"
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"


class GoogleProvider(BaseProvider):

    def _url(self, model: str, api_key: str, action: str = "generateContent") -> str:
        return f"{BASE_URL}/{model}:{action}?key={api_key}"

    def _call(self, api_key: str, model: str, system: str, prompt: str,
              max_tokens: int = 4000, use_search: bool = False) -> str:
        body = {
            "contents": [
                {"role": "user", "parts": [{"text": prompt}]}
            ],
            "systemInstruction": {
                "parts": [{"text": system}]
            },
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": 0.3,
            },
        }
        if use_search:
            body["tools"] = [{"googleSearch": {}}]

        resp = requests.post(
            self._url(model, api_key),
            headers={"Content-Type": "application/json"},
            json=body,
            timeout=120,
            verify=False,
        )
        if not resp.ok:
            try:
                err = resp.json().get("error", {}).get("message", resp.text)
            except Exception:
                err = resp.text
            raise ProviderError(f"Google API error {resp.status_code}: {err}")

        data = resp.json()
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            return ""

    def scan(self, url: str, api_key: str) -> dict:
        prompt = _build_scan_prompt(url)
        system = _scan_system()
        raw = self._call(api_key, SCAN_MODEL, system, prompt, max_tokens=4000, use_search=True)
        return _parse_json_response(raw, url)

    def generate(self, context: dict, api_key: str) -> dict:
        system = _generation_system()
        results = {}

        r1 = self._call(api_key, GEN_MODEL, system, _dashboard_prompt(context), max_tokens=3000)
        results["dashboard"] = _parse_json_response(r1)

        r2 = self._call(api_key, GEN_MODEL, system, _roadmap_prompt(context, results.get("dashboard")), max_tokens=3000)
        results["roadmap"] = _parse_json_response(r2)

        r3 = self._call(api_key, GEN_MODEL, system, _document_prompt(context, results.get("dashboard")), max_tokens=4000)
        results["document"] = _parse_json_response(r3)

        return results
