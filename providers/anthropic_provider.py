"""
Anthropic Provider — Claude Sonnet
Uses web_search_20250305 tool with agentic loop for URL intelligence gathering.
"""

import json
import re
import requests
from .base import BaseProvider, ProviderError

MODEL = "claude-sonnet-4-5-20251001"
API_URL = "https://api.anthropic.com/v1/messages"
HEADERS_BASE = {
    "anthropic-version": "2023-06-01",
    "content-type": "application/json",
}


class AnthropicProvider(BaseProvider):

    def _headers(self, api_key: str) -> dict:
        return {**HEADERS_BASE, "x-api-key": api_key}

    def _call(self, api_key: str, messages: list, system: str = "", max_tokens: int = 4000, tools: list = None) -> dict:
        body = {
            "model": MODEL,
            "max_tokens": max_tokens,
            "messages": messages,
        }
        if system:
            body["system"] = system
        if tools:
            body["tools"] = tools

        resp = requests.post(API_URL, headers=self._headers(api_key), json=body, timeout=120, verify=False)
        if not resp.ok:
            try:
                err = resp.json().get("error", {}).get("message", resp.text)
            except Exception:
                err = resp.text
            raise ProviderError(f"Anthropic API error {resp.status_code}: {err}")
        return resp.json()

    def _agentic_call(self, api_key: str, prompt: str, system: str = "", max_tokens: int = 4000) -> str:
        """
        Handles multi-turn tool use loop for web_search.
        Returns the final text response after all tool calls complete.
        """
        messages = [{"role": "user", "content": prompt}]
        tools = [{"type": "web_search_20250305", "name": "web_search"}]
        final_text = ""

        for turn in range(10):  # max 10 turns
            data = self._call(api_key, messages, system=system, max_tokens=max_tokens, tools=tools)

            # Collect text from this response
            text_blocks = [b["text"] for b in data.get("content", []) if b.get("type") == "text"]
            if text_blocks:
                final_text = "\n".join(text_blocks)

            # If done — no more tool calls
            if data.get("stop_reason") == "end_turn":
                break

            # Handle tool_use — push results back and continue
            tool_use_blocks = [b for b in data.get("content", []) if b.get("type") == "tool_use"]
            if not tool_use_blocks:
                break

            # Add assistant message
            messages.append({"role": "assistant", "content": data["content"]})

            # Add tool results — the API handles the actual search internally
            # We return the input back as result to signal completion
            tool_results = [
                {
                    "type": "tool_result",
                    "tool_use_id": tu["id"],
                    "content": json.dumps(tu.get("input", {})),
                }
                for tu in tool_use_blocks
            ]
            messages.append({"role": "user", "content": tool_results})

        return final_text

    def _simple_call(self, api_key: str, prompt: str, system: str = "", max_tokens: int = 4000) -> str:
        """Single-turn call without tools — for generation steps."""
        data = self._call(api_key, [{"role": "user", "content": prompt}], system=system, max_tokens=max_tokens)
        texts = [b["text"] for b in data.get("content", []) if b.get("type") == "text"]
        return "\n".join(texts)

    def scan(self, url: str, api_key: str) -> dict:
        prompt = _build_scan_prompt(url)
        system = _scan_system()
        raw = self._agentic_call(api_key, prompt, system=system, max_tokens=4000)
        return _parse_json_response(raw, url)

    def generate(self, context: dict, api_key: str) -> dict:
        system = _generation_system()
        results = {}

        # Call 1 — Dashboard: vision, risk domains, KPIs, pillars, framework alignment
        r1 = self._simple_call(api_key, _dashboard_prompt(context), system=system, max_tokens=3000)
        results["dashboard"] = _parse_json_response(r1)

        # Call 2 — Roadmap: phases, risk cards, ROI note
        r2 = self._simple_call(api_key, _roadmap_prompt(context, results.get("dashboard")), system=system, max_tokens=3000)
        results["roadmap"] = _parse_json_response(r2)

        # Call 3 — Document: all sections
        r3 = self._simple_call(api_key, _document_prompt(context, results.get("dashboard")), system=system, max_tokens=4000)
        results["document"] = _parse_json_response(r3)

        return results


# ── Shared prompt builders (used by all providers) ────────────────────────────

def _scan_system() -> str:
    return (
        "You are an intelligence analyst for a cybersecurity strategy platform. "
        "Your job is to analyse company websites and extract structured intelligence signals. "
        "Always return valid JSON only — no markdown, no explanation."
    )

def _generation_system() -> str:
    return """You are StratIQ — an AI-powered IT and Cybersecurity Strategy Intelligence Platform for CISOs and CIOs.
Your strategy generation is inspired by the work of Dr. Muhammad Malik (https://www.linkedin.com/in/dr-muhammad-malik-45940a/).

Core principles:
- Clarity over controls. Direction over decoration. Business language over technical jargon.
- Vision: One sentence, business outcome focused. Never maturity scores.
- Risk in dollars and business impact, not CVSS scores.
- Every control justified by business outcome, not compliance checkbox.
- Language: NEVER "privilege escalation found". ALWAYS "SSO compromise enables exec impersonation and financial fraud".
- Strategy is a loop: Year 1 = foundation wins, Year 2 = learn and adjust, Year 3 = mature and advance.
- Always above-the-line framing: revenue, brand, downtime. Never surprise the board.

UAE/GCC context: Apply NCA ECC, ADHICS, UAE PDPL knowledge. Understand GCC regulatory landscape.
Always return valid JSON only — no markdown fences, no explanation."""

def _build_scan_prompt(url: str) -> str:
    return f"""Analyse this company's public web presence and extract structured intelligence signals for an IT and cybersecurity strategy.

Use web search to visit and analyse: {url}
Also search for: site:{url} about, site:{url} leadership, site:{url} news

Return ONLY valid JSON — no markdown, no explanation, just the raw JSON:
{{
  "company": {{
    "name": "Company name",
    "industry": "Primary industry / sector",
    "region": "HQ location / primary geography",
    "size": "Employee count range or description",
    "growth_stage": "Growth stage description",
    "growth_signal": "One sentence on growth trajectory from signals found"
  }},
  "sources": [
    {{
      "icon": "globe",
      "label": "Homepage",
      "url": "{url}",
      "signals": [
        {{"id": "h1", "cat": "Vision", "text": "Factual signal from homepage"}},
        {{"id": "h2", "cat": "Sector", "text": "Factual signal"}}
      ]
    }},
    {{
      "icon": "building",
      "label": "About Us",
      "url": "{url}/about",
      "signals": [
        {{"id": "a1", "cat": "Values", "text": "Factual signal"}},
        {{"id": "a2", "cat": "Structure", "text": "Factual signal"}}
      ]
    }},
    {{
      "icon": "news",
      "label": "News & Press",
      "url": "{url}/news",
      "signals": [
        {{"id": "n1", "cat": "Expansion", "text": "Factual signal"}},
        {{"id": "n2", "cat": "Technology", "text": "Factual signal"}}
      ]
    }},
    {{
      "icon": "star",
      "label": "Leadership Team",
      "url": "{url}/leadership",
      "signals": [
        {{"id": "l1", "cat": "CISO", "text": "Note if CISO role is absent or present"}},
        {{"id": "l2", "cat": "CTO", "text": "Factual signal"}}
      ]
    }}
  ]
}}

Signal categories: Vision, Mission, Tagline, Sector, Geography, Scale, Tech Signal, Growth, Brand, Values, History, Structure, Leadership, Workforce, Governance, Compliance, Expansion, M&A, Technology, Awards, Sustainability, Risk, Partnership, Investment, Innovation, CISO, CTO, CIO, CEO

Rules: 8-15 signals per source. Factual observations only. Note missing CISO explicitly. Return ONLY the JSON."""

def _dashboard_prompt(ctx: dict) -> str:
    return f"""Generate Executive Dashboard data for this organisation's IT & Cybersecurity Strategy.

COMPANY: {ctx.get('company_name')} | {ctx.get('industry')} | {ctx.get('region')} | {ctx.get('size')} | {ctx.get('growth')}
URL: {ctx.get('url', '')}
AUDIENCE: {ctx.get('audience', 'CISO')}
FRAMEWORKS: {', '.join(ctx.get('frameworks', []))}

INTELLIGENCE SIGNALS:
{ctx.get('signals_text', '')}

TOOL INVENTORY: {ctx.get('inventory', 'Not assessed')}
KNOWN GAPS: {ctx.get('gaps', '')}
ORG CONTEXT: {', '.join(ctx.get('org_context', []))}

Return ONLY valid JSON:
{{
  "vision": "One sentence vision — business outcome focused, not technical",
  "risk_domains": [
    {{"name": "Identity & Access", "score": 62, "color": "#C05000", "finding": "Business-language finding"}},
    {{"name": "Cloud Security", "score": 45, "color": "#FF4D6D", "finding": "..."}},
    {{"name": "Endpoint Protection", "score": 71, "color": "#007A4A", "finding": "..."}},
    {{"name": "Data Privacy", "score": 38, "color": "#FF4D6D", "finding": "..."}},
    {{"name": "Supply Chain Risk", "score": 55, "color": "#C05000", "finding": "..."}},
    {{"name": "Incident Response", "score": 67, "color": "#007A4A", "finding": "..."}}
  ],
  "pillars": [
    {{"title": "Pillar name (board language)", "desc": "One sentence, business impact"}},
    {{"title": "...", "desc": "..."}},
    {{"title": "...", "desc": "..."}},
    {{"title": "...", "desc": "..."}}
  ],
  "kpis": [
    {{"label": "KPI name", "value": "Value", "trend": "up|down|stable", "context": "Brief context"}},
    {{"label": "...", "value": "...", "trend": "...", "context": "..."}},
    {{"label": "...", "value": "...", "trend": "...", "context": "..."}},
    {{"label": "...", "value": "...", "trend": "...", "context": "..."}}
  ],
  "framework_alignment": [
    {{"name": "Framework name", "pct": 45, "status": "Gap|In Progress|Compliant", "priority": "Immediate|Near-term|Ongoing"}}
  ]
}}"""

def _roadmap_prompt(ctx: dict, dashboard: dict = None) -> str:
    vision = dashboard.get("vision", "") if dashboard else ""
    return f"""Generate a 3-year IT & Cybersecurity Strategic Roadmap.

COMPANY: {ctx.get('company_name')} | {ctx.get('industry')} | {ctx.get('region')} | {ctx.get('size')}
FRAMEWORKS: {', '.join(ctx.get('frameworks', []))}
KNOWN GAPS: {ctx.get('gaps', '')}
ORG CONTEXT: {', '.join(ctx.get('org_context', []))}
VISION: {vision}

SIGNALS: {ctx.get('signals_text', '')[:1500]}

Strategy loop: Year 1 = foundation wins. Year 2 = learn and adjust. Year 3 = mature and advance.
Prioritise: business risk first, then regulatory (NCA ECC), then operational maturity.

Return ONLY valid JSON:
{{
  "phases": {{
    "0-6 Months": {{
      "color": "var(--danger)",
      "items": [
        {{
          "t": "Initiative title",
          "d": "IT|Cyber|Compliance",
          "p": "Critical|High|Medium",
          "e": "Low|Medium|High|Very High",
          "desc": "Business-language description — risk addressed and outcome delivered",
          "budget_aed": "150,000-250,000"
        }}
      ]
    }},
    "6-12 Months": {{"color": "var(--warning)", "items": [...]}},
    "1-3 Years": {{"color": "var(--success)", "items": [...]}}
  }},
  "risk_without_roadmap": [
    {{"title": "Risk in business language", "impact": "Financial or operational impact", "likelihood": "High|Medium|Low"}},
    {{"title": "...", "impact": "...", "likelihood": "..."}},
    {{"title": "...", "impact": "...", "likelihood": "..."}}
  ],
  "roi_note": "One sentence: roadmap investment vs cost of breach for this organisation"
}}

Rules: 4+ initiatives per phase. Budget in AED. Business language. No CVSS."""

def _document_prompt(ctx: dict, dashboard: dict = None) -> str:
    vision = dashboard.get("vision", "") if dashboard else ""
    year = 2025
    return f"""Write a complete board-ready IT and Cybersecurity Strategy document.

COMPANY: {ctx.get('company_name')} | {ctx.get('industry')} | {ctx.get('region')} | {ctx.get('size')}
FRAMEWORKS: {', '.join(ctx.get('frameworks', []))}
AUDIENCE: {ctx.get('audience', 'CISO')}
VISION: {vision}

SIGNALS: {ctx.get('signals_text', '')[:2000]}
GAPS: {ctx.get('gaps', '')}
ORG CONTEXT: {', '.join(ctx.get('org_context', []))}

Return ONLY valid JSON:
{{
  "doc_ref": "SIQ-STRAT-{year}-001",
  "period": "{year}-{year+3}",
  "executive_summary": "3-4 paragraphs. Business outcome language. Why now.",
  "strategic_context": {{
    "business_environment": "2-3 paragraphs. Growth, expansion, digital transformation risk.",
    "regulatory_landscape": "2-3 paragraphs. Applicable regulations and non-compliance consequences in business terms.",
    "threat_landscape": "2 paragraphs. Relevant threats for this industry/region in business impact terms."
  }},
  "vision_statement": "The single-sentence vision",
  "pillars": [
    {{"number": "4.1", "title": "Pillar Name", "description": "2-3 sentences. Board language."}},
    {{"number": "4.2", "title": "...", "description": "..."}},
    {{"number": "4.3", "title": "...", "description": "..."}},
    {{"number": "4.4", "title": "...", "description": "..."}}
  ],
  "governance": "2 paragraphs. Ownership, reporting cadence, board visibility.",
  "success_metrics": "2 paragraphs. Business metrics, not technical. How the board will know it's working.",
  "attribution": "Strategic frameworks in StratIQ are inspired by the published work of Dr. Muhammad Malik. linkedin.com/in/dr-muhammad-malik-45940a/"
}}"""

def _parse_json_response(raw: str, url: str = None) -> dict:
    """Extract and parse JSON from a raw text response. Returns empty dict on failure."""
    if not raw:
        return {}
    try:
        clean = re.sub(r'```json\s*', '', raw)
        clean = re.sub(r'```\s*', '', clean).strip()
        match = re.search(r'\{[\s\S]*\}', clean)
        if match:
            return json.loads(match.group(0))
    except (json.JSONDecodeError, Exception):
        pass
    return {}
