# Changelog

All notable changes to StratIQ are documented here.

---

## [2.9.4] — 2026-03-17

### Fixed
- Mandatory frameworks (ADHICS, UAE PDPL, NCA ECC, etc.) can now be deselected. Previously they were permanently locked — pre-selected and impossible to remove. A CISO who understands their regulatory scope can now consciously uncheck any framework that doesn't apply to their organisation.

### Improved
- Homepage attribution footer expanded to acknowledge the broader intellectual foundation: Porter's Five Forces, Kaplan & Norton Strategy Maps, Osterwalder's Business Model Canvas, and the FAIR risk quantification methodology — alongside the primary credit to Dr. Muhammad Malik's published work.

---

## [2.9.0] — 2026-03-16

### Added
- **GitHub Pages / zero-install mode** — StratIQ now runs as a fully static web app with no Docker, no server, and no installation. Live at [https://ambarishrh.github.io/stratiq](https://ambarishrh.github.io/stratiq).
- **Browser-native session persistence** — in static mode, all session data is stored in the browser's IndexedDB. Nothing leaves the device. Sessions persist across browser restarts.
- **Automatic backend detection** — StratIQ detects whether a Flask backend is available and switches between SQLite (Docker) and IndexedDB (static) automatically. No configuration required.
- **AI-powered company research** — company scanning now uses provider-native web search instead of HTML scraping. Works on all deployment modes including GitHub Pages. No CORS issues, no scraping failures.
  - Anthropic: web search tool via `/v1/messages`
  - OpenAI: Responses API with web search
  - Google Gemini: grounding with Google Search
  - OpenRouter: routes to Perplexity Sonar with built-in web search

### Changed
- AI web search is now the primary scan method for all deployment modes. Flask scraping is retained as a Docker-only fallback if AI web search fails.
- Version bumped: 2.8.4 → 2.9.0

---

## [2.8.4] — 2026-03-15

### Improved
- **Biggest Constraint is now multi-select** — users can select any combination of Budget, People & Skills, and Executive buy-in. Previously a single-select radio forced "All three equally" when two constraints applied.

### Fixed
- Wishlist items were saved but never passed to AI prompts. They are now included in all three generation calls, allowing the AI to factor pipeline capabilities into roadmap phasing.

---

## [2.8.3] — 2026-03-15

### Fixed
- Scan errors were invisible — the error message was inside a container that was being hidden on failure. Errors now surface correctly with a "Try Again" button that resets cleanly to URL input without a page reload. Five distinct error states: provider unavailable, network error, invalid key, rate limit, and generic fallback.

---

## [2.8.2] — 2026-03-15

### Fixed
- Leadership page not found on sites that use query-parameter navigation (e.g. `?section=leadership-team`).
- Company name incorrectly inferred from domain in some cases — the scanned URL is now passed as a hint to the AI.

---

## [2.8.1] — 2026-03-15

### Fixed
- Framework "Add" field replaced dead free-text input with a grouped dropdown populated from the full framework library (25 frameworks, organised by region).
- OpenRouter model updated to `claude-sonnet-4-6`.

### Improved
- Document quality significantly raised: Executive Summary now requires a named risk with financial exposure and a specific board ask; Pillars now require business consequence and measurable year-3 outcome; Regulatory section covers all selected frameworks; Roadmap requires exact initiative titles and per-phase budgets.
- Dr. Muhammad Malik's strategy principles injected as system-level rules into every document generation call.

---

## [2.8.0] — 2026-03-15

### Added
- All 25 frameworks now include domain and obligation context, used to derive pillars and roadmap initiatives directly from the user's selected compliance stack.
- Every Mandatory framework gets at least one dedicated compliance initiative in the roadmap.
- Regulatory section (Section 7) writes one substantive paragraph per selected framework.

### Fixed
- NCA ECC correctly identified as a Saudi framework, not UAE.

---

## [2.7.0] — 2026-03-15

### Improved
- Dashboard: KPI 4 changed to quantified financial risk exposure using FAIR methodology.
- Roadmap: Every initiative now requires owner, success criteria, and effort estimate. Ten hard execution rules embedded, including mandatory AI security threat initiative, Zero Trust, and Security Awareness.
- Document: Rebuilt from 8 to 12 sections. Token limit raised to 12,000. New sections: Threat Landscape, Governance & Operating Model, Resource Plan, Risk Quantification, Quick Wins.

---

## [2.6.1] — 2026-03-15

### Fixed
- 401 errors when a saved API key was pre-filled but not formally initialised on page load.

---

## [2.6.0] — 2026-03-15

### Added
- **Internal Context Interview** — new wizard step between Company Profile and Frameworks. 14 structured questions covering budget, headcount, IT team structure, CISO role, last incident, board attitude, top risks, constraints, compliance deadlines, cloud stage, remote workforce, vendor risk, and board notes. All responses are serialised and passed to all three AI generation prompts.

---

## [2.5.0] — 2026-03-14

### Added
- Export options: Print/Save as PDF, Copy Document Text, Download JSON.
- Print CSS: hides all UI chrome and renders all generated tabs for clean A4 output.

---

## [2.4.0] — 2026-03-14

### Added
- **Audience-aware generation** — language, depth, and framing adapt per audience. CISO → Dashboard + Document; CIO → Roadmap + Document; CISO+CIO → All three; Board → Dashboard only with zero jargon, 5 sections, 4,000 tokens.

---

## [2.3.0] — 2026-03-14

### Added
- **Global framework library** — 25 frameworks across all major regions, replacing the previous static 6-framework list.
- AI recommends applicable frameworks per company based on geography, sector, and regulatory signals.
- Three-tier UI: Mandatory (pre-selected) · Recommended (pre-selected) · Also Consider (opt-in).
- Each framework shows a company-specific AI reason alongside the library description.
- Fallback defaults to ISO 27001 + NIST CSF 2.0 if AI recommendation fails.

---

## [2.2.0] — 2026-03-14

### Added
- API key and provider persist to localStorage — pre-filled on next visit.
- "Saved" badge and "Forget" link on API key field. Eye icon to show/hide key.
- "Check Balance" button for OpenRouter — returns live credit balance.

---

## [2.1.0] — 2026-03-08

### Added
- Full wizard state auto-saved to SQLite on every mutation.
- Session resume — fully restores all wizard state from a previous session.
- `STRATIQ_VERSION` constant and version pill in the UI.
- Edit & Regenerate button in results header.

---

## [2.0.0] — 2026-02-28

### Added
- Real scan pipeline: browser-direct AI calls, Flask handles scraping and SQLite only.
- Provider-agnostic AI call function supporting Anthropic, OpenAI, Google Gemini, and OpenRouter.

---

## [1.0.0] — 2026-02-01

### Added
- Single HTML file architecture — no frameworks, no build tools.
- Full 7-step wizard: API key, URL, Sources, Company Profile, Frameworks, Landscape, Output.
- Results screen with sticky header and three tabs: Dashboard, Roadmap, Document.
- Flask backend: SQLite sessions, full CRUD API.
- Dr. Muhammad Malik attribution on homepage.
- CC BY-NC-SA 4.0 license.
