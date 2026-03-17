# Changelog

All notable changes to StratIQ are documented here.

---

## [2.9.4] — 2026-03-17

### Fixed — Framework Selection UX

- **Mandatory frameworks are no longer permanently locked.** Previously, frameworks tagged Mandatory (ADHICS, UAE PDPL, NCA ECC, etc.) were pre-selected and impossible to deselect — the checkbox showed a padlock icon and clicking had no effect. A CISO who genuinely understands their regulatory scope should be able to consciously remove a framework if it does not apply to their organisation
- **Root cause 1:** `tFw()` had an early-return guard (`if priority === 'Mandatory') return`) that silently blocked all deselect attempts
- **Root cause 2:** `rFw()` unconditionally called `selFw.add()` for every Mandatory framework on every render — so even after successfully removing a framework from the set, the next render immediately re-added it
- **Root cause 3:** The card rendered `cursor: default` and a padlock SVG for Mandatory frameworks instead of the standard checkbox
- **Fix:** Removed the early-return guard, removed the force-add loop in `rFw()`, changed cursor to `pointer`, replaced the lock icon with the standard checkmark/empty checkbox pattern used by all other tiers. Mandatory frameworks still arrive pre-selected from the AI scan; the user now has the freedom to consciously uncheck them

### Improved — Homepage Attribution Footer

- Footer credit block expanded from a single attribution line to a fuller acknowledgement
- Dr. Muhammad Malik's three articles remain the primary credit ("Core strategy methodology inspired by...")
- Added a second sentence crediting the broader intellectual foundation: Porter's Five Forces, Kaplan & Norton Strategy Maps, Osterwalder's Business Model Canvas, and the FAIR risk quantification methodology
- Framing: "applied through a practitioner's eye to make security strategy legible to boards, not just auditors"

---

## [2.9.0] — 2026-03-16

### Added — GitHub Pages Support (Zero-Install Deployment)
- **StratIQ now runs as a fully static web app** — no Docker, no server, no installation required
- **Live instance:** [https://ambarishrh.github.io/stratiq](https://ambarishrh.github.io/stratiq)
- **IndexedDB persistence** — full session CRUD in browser: save, resume, delete, auto-save, landscape data, generated outputs. Data stays entirely on the user's machine — never transits a network
- **Storage adapter pattern** — `detectBackend()` pings `/api/ping` on load with a 1.5s timeout. Flask/Docker present → `FlaskAdapter` (SQLite). No backend → `IndexedDBAdapter` (browser-native). Zero configuration — fully automatic
- **`FlaskAdapter`** — wraps all Flask API calls behind a consistent interface
- **`IndexedDBAdapter`** — identical interface, browser-native IndexedDB backend. Full session history, status tracking, auto-save support. Works on `gh-pages`, any static CDN, or local `file://`

### Added — AI-Powered Company Research (Primary Scan Mode)
- **`callClaudeWithWebSearch()`** — new AI call function enabling provider-native web search for company research. No scraping, no CORS proxies, works everywhere including GitHub Pages
  - Anthropic: `web_search_20250305` tool via `/v1/messages`
  - OpenAI: Responses API with `web_search_preview` tool
  - Google Gemini: grounding with `googleSearch`
  - OpenRouter: routes to `perplexity/sonar` model with built-in web search
- **`buildResearchPrompt()`** — structured prompt instructing AI to research a company from its URL using training knowledge + live web search. Returns same JSON schema as scrape-based scan
- AI research is now primary for ALL deployment modes — replaces HTML scraping as the default
- Flask scraping retained as Docker-only fallback if `callClaudeWithWebSearch` throws
- Scan step labels updated: "Researching company online..." / "Analysing public information..."

### Changed
- Single file serves both modes — `stratiq_8.html` auto-detects Docker vs static hosting at runtime
- All session functions now call `storage.*` adapter — never Flask directly
- Version bumped: 2.8.4 → 2.9.0

---

## [2.8.4] — 2026-03-15

### Improved — Internal Context Interview
- **Biggest Constraint changed to multi-select** — users can now select any combination of Budget, People/Skills, and Executive buy-in. Previously a single-select radio forced "All three equally" when two constraints applied
- Constraints stored as array (`internalContext.constraints[]`); legacy single-value sessions still load correctly

### Fixed — Wishlist not reaching AI
- `LS_WISHLIST` items were saved to SQLite but never passed to the AI prompts
- Now serialised in `buildCtxBlock()` as "Capabilities under evaluation / pipeline" with budget status
- AI instructed to factor pipeline capabilities into roadmap phasing

---

## [2.8.3] — 2026-03-15

### Fixed — Scan Error Visibility
- Errors were invisible to users — the scan error div lived inside `#scan-prog` which was being hidden on error
- "Try Again" button added to every error state — resets cleanly back to URL input without a page reload
- Five distinct error states now surface correctly: 500/provider unavailable, network errors, 401 invalid key, 429 rate limit, generic fallback
- Generic fallback no longer dumps raw technical error strings

---

## [2.8.2] — 2026-03-15

### Fixed — URL Scraping
- Leadership page not found on query-param navigation sites: `best_match()` in `server.py` now checks full URL including query string
- Wrong company name inferred from domain: `buildSignalPrompt()` now receives the scanned URL and passes a domain hint to the AI
- `_ABOUT_KEYS` and `_LEADERSHIP_KEYS` in `server.py` expanded

---

## [2.8.1] — 2026-03-15

### Fixed
- Framework "Add" field: replaced dead free-text input with a grouped `<select>` dropdown populated from the full `FW_LIBRARY` (25 frameworks, grouped by region)
- OpenRouter model updated from `claude-sonnet-4-5` to `claude-sonnet-4-6`

### Improved — Document Quality
- Section 1 (Executive Summary): Now requires named risk + specific financial exposure range + investment figure + single board ask
- Section 4 (Pillars): Each pillar now requires 2–3 sentences covering what it builds, the business consequence if neglected, and measurable success at year 3
- Section 7 (Regulatory): Now explicitly covers ALL selected frameworks including Recommended
- Section 8 (Roadmap Summary): Now requires exact initiative titles, per-phase budgets, and a year-3 outcome paragraph
- Dr. Muhammad Malik's principles injected as system-level rules into every document generation

---

## [2.8.0] — 2026-03-15

### Added — Framework-Aware Prompt Engine
- `FW_LIBRARY` expanded: all 25 frameworks now include `domains[]` and `obligations`
- `buildFrameworkContext()` — new helper serialising selected frameworks into a rich context block
- Dashboard pillars now derived from the combined domains of ALL selected frameworks
- Roadmap: MANDATORY FRAMEWORK RULE — every Mandatory framework gets at least one dedicated compliance initiative
- Document: Regulatory section (Section 7) writes one substantive paragraph per selected framework

### Fixed
- NCA ECC corrected: Saudi framework, not UAE

---

## [2.7.0] — 2026-03-15

### Improved — Prompt Quality Rebuild

- Dashboard: KPI 4 changed to quantified financial risk exposure (FAIR methodology); 5–6 pillars covering all NIST CSF 2.0 functions
- Roadmap: Every initiative now requires `owner`, `successCriteria`, `effort`; 10 hard execution rules embedded including mandatory AI security threat initiative, Zero Trust, Security Awareness
- Document: Rebuilt from 8 to 12 sections; token limit raised to 12,000; new sections: Threat Landscape, Governance & Operating Model, Resource Plan, Risk Quantification, Quick Wins

---

## [2.6.1] — 2026-03-15

### Fixed
- `startScan()` now grabs API key directly from input field if `apiKey` variable is unset — fixes 401 errors when saved key is pre-filled but not formally initialised

---

## [2.6.0] — 2026-03-15

### Added — Internal Context Interview (Phase 3A)
- New wizard step between Company Profile and Frameworks
- 14 structured questions covering budget, headcount, IT team, CISO role, last incident, board attitude, top risks, constraints, compliance deadline, cloud stage, remote workforce, vendor risk, board notes
- `internalContext` state var fully serialised and restored on session resume
- `buildCtxBlock()` serialises context into prompt block injected into all 3 AI prompts

---

## [2.5.0] — 2026-03-14

### Added
- Export dropdown: Print/Save as PDF, Copy Document Text, Download JSON
- Print CSS: hides all UI chrome, renders all generated tabs for print (A4)

---

## [2.4.0] — 2026-03-14

### Added — Audience-Aware Generation
- `audTone()` — shared function injecting tone/depth/framing into all 3 prompts per audience
- CISO → Dashboard + Document; CIO → Roadmap + Document; CISO+CIO → All 3; Board → Dashboard only
- Board document: 5 sections, 4,000 tokens, zero jargon

---

## [2.3.0] — 2026-03-14

### Added — Global AI-Driven Framework Recommendation Engine
- Replaced static 6-framework list with `FW_LIBRARY` — 25 globally relevant frameworks
- Tiered UI: Mandatory (pre-selected) / Recommended (pre-selected) / Also Consider (not selected)
- Company-specific AI reason per framework + library educational description
- Fallback defaults: ISO 27001 + NIST CSF 2.0

---

## [2.2.0] — 2026-03-14

### Added
- localStorage API key + provider persistence — pre-fills on next visit
- "Saved" badge + "Forget" link on API key field; eye icon to show/hide key
- "Check Balance" button — OpenRouter returns live credit balance

---

## [2.1.0] — 2026-03-08

### Added — Real AI Generation + Session Persistence
- Full wizard state auto-saved to SQLite on every mutation
- Session resume — fully restores all wizard state
- `STRATIQ_VERSION` constant and version pill
- Edit & Regenerate button in results header

---

## [2.0.0] — 2026-02-28

### Added — Real Scan Pipeline
- `callClaude()` — provider-agnostic, handles Anthropic, OpenAI, Google Gemini, OpenRouter
- `startScan()` replaced stub with real async scrape → AI → parse → navigate flow
- Architecture confirmed: browser-direct AI calls, Flask handles scraping + SQLite only

---

## [1.0.0] — 2026-02-01

### Added
- Single HTML file architecture (no frameworks, no build tools)
- Full 7-step wizard: API key, URL, Sources, Company Profile, Frameworks, Landscape, Output
- Results screen: sticky header, 3 tabs (Dashboard / Roadmap / Document)
- Flask backend: SQLite sessions, full CRUD API
- Dr. Muhammad Malik attribution on homepage
- CC BY-NC-SA 4.0 license
