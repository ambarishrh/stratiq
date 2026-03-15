# Changelog

All notable changes to StratIQ are documented here.

---

## [2.8.2] — 2026-03-15

### Fixed — URL Scraping
- **Leadership page not found on query-param navigation sites**: `best_match()` in `server.py` now checks the full URL including query string, not just the path segment. Previously URLs like `/who-we-are?section=leadership-team` were reduced to `/who-we-are` before keyword matching, causing leadership content to be missed entirely on sites that use query parameters for section navigation
- **Wrong company name inferred from domain**: `buildSignalPrompt()` now receives the scanned URL and passes a domain hint to the AI with an explicit instruction to derive the proper trading name from page content (logo alt text, page title, about section) first, falling back to a clean derivation from the domain — e.g. `holding.com → Company Holding`. Prevents the AI from returning the raw domain URL as the company name
- `_ABOUT_KEYS` and `_LEADERSHIP_KEYS` in `server.py` expanded to include `our-journey`, `our-history`, `history`, `founders`, `people`, `governance`, `senior`

---

## [2.8.1] — 2026-03-15

### Fixed
- Framework "Add" field: replaced dead free-text input with a grouped `<select>` dropdown populated from the full `FW_LIBRARY` (25 frameworks, grouped by region). The `+ ADD` button now correctly wires the selection into `aiFrameworks` as "Consider" priority and re-renders the list
- OpenRouter model updated from `claude-sonnet-4-5` to `claude-sonnet-4-6`

### Improved — Document Quality
- **Section 1 (Executive Summary):** Now requires named risk + specific financial exposure range + investment figure + single board ask. Eliminates generic "maintain business continuity" language
- **Section 4 (Pillars):** Each pillar now requires 2–3 sentences covering: what it builds, the specific business consequence if neglected, and what measurable success looks like at year 3
- **Section 7 (Regulatory):** Now explicitly covers ALL selected frameworks including Recommended — previously only wrote about Mandatory frameworks
- **Section 8 (Roadmap Summary):** Now requires exact initiative titles from the generated roadmap, per-phase budgets, and a year-3 outcome paragraph
- Dr. Muhammad Malik's principles injected as system-level rules into every document generation: risk in dollars, clarity over controls, vision as one business outcome sentence, never surprise the CEO

---

## [2.8.0] — 2026-03-15

### Added — Framework-Aware Prompt Engine
- `FW_LIBRARY` expanded: all 25 frameworks now include `domains[]` (key control areas) and `obligations` (what compliance actually requires in plain terms)
- `buildFrameworkContext()` — new helper that serialises selected frameworks with their domains and obligations into a rich context block, injected into all three AI prompts
- Dashboard: strategic pillars now derived from the **combined domains of ALL selected frameworks** — NIST CSF 2.0 used as a completeness check only, not structural organiser
- Dashboard: 6th risk domain is framework-specific (e.g. "Patient Data Security" for ADHICS, "Payment Data Integrity" for PCI-DSS)
- Roadmap: **MANDATORY FRAMEWORK RULE** — every Mandatory framework gets at least one dedicated compliance initiative named in the roadmap
- Roadmap: initiative domains derived from selected framework vocabulary, not hardcoded Cyber/IT/Compliance
- Document: Regulatory section (Section 7) now writes one substantive paragraph per selected framework linking it to org-specific gaps, roadmap response, and non-compliance consequence in financial terms

### Fixed
- NCA ECC corrected in `FW_LIBRARY`: this is a **Saudi** framework (National Cybersecurity Authority of Saudi Arabia), not UAE. Region tag corrected from "UAE" to "Saudi Arabia"

---

## [2.7.0] — 2026-03-15

### Improved — Prompt Quality Rebuild (Global Best Practices)

**Dashboard prompt**
- KPI 4 changed from vague "maturity" to quantified financial risk exposure (FAIR methodology framing)
- Pillar count increased to 5–6 with instruction to cover all NIST CSF 2.0 functions
- Risk domain rationale now requires business consequence, not technical description

**Roadmap prompt**
- Every initiative now requires: `owner`, `successCriteria`, `effort` alongside existing fields
- Budget is currency-agnostic (local currency from region signals, defaults to USD)
- 10 hard execution rules embedded:
  - AI security threat initiative mandatory (AI-enhanced phishing, deepfakes — #1 emerging risk 2025–2026)
  - Zero Trust architecture initiative mandatory
  - Security Awareness and Human Risk initiative mandatory
  - Governance/board reporting initiative mandatory
  - Constraint and budget signals from Internal Context feed sequencing
  - Every gap must be addressed; inventory not re-recommended

**Document prompt**
- Rebuilt from 8 to **12 sections**:
  1. Executive Summary
  2. Business Context & Why Now
  3. **Threat Landscape** *(new)*
  4. Strategic Vision & Pillars
  5. **Governance & Operating Model** *(new)*
  6. Current State Assessment
  7. Regulatory & Compliance Obligations
  8. 3-Year Roadmap Summary
  9. **Resource Plan** *(new)*
  10. **Risk Quantification** *(new — FAIR methodology)*
  11. Measuring Success — KPIs & Review Cadence
  12. **Quick Wins — Start Here** *(new)*
- Token limit raised from 8,000 to 12,000 for full document; Board version stays at 4,000
- Roadmap initiative owner/successCriteria fields now shown in roadmap card renderer

---

## [2.6.1] — 2026-03-15

### Fixed
- `startScan()` now grabs API key directly from the input field if `apiKey` variable is unset — fixes 401 errors when saved key (pre-filled by `loadSavedKey()`) is not formally initialised via the Initialize button

---

## [2.6.0] — 2026-03-15

### Added — Internal Context Interview (Phase 3A)
- New wizard step between Company Profile and Frameworks: **Internal Context Interview**
- 14 structured questions covering:
  - Annual IT/Security budget (currency-agnostic bands: <$100K → $10M+)
  - Organisation headcount and IT team size
  - Dedicated security team Y/N
  - CISO/security lead role Y/N with title field
  - Last significant security incident (5 options)
  - Board attitude to cyber risk (4 options)
  - Top business risks (AI pre-filled chips from scan + custom add)
  - Biggest constraint (Budget / People / Executive buy-in / All three)
  - Compliance deadline pressure with timeframe
  - Cloud adoption stage
  - Remote/hybrid workforce %
  - Third-party/vendor risk exposure
  - Free-text board notes
- `internalContext` state var — fully serialised in `buildWizardState()`, restored on session resume
- `buildCtxBlock()` — serialises context into prompt block injected into all 3 AI prompts
- Business risks pre-populated from `aiDashboard.risks` if scan complete; falls back to 8 example risks
- Note displayed: "Already approved a tool? Add it to Tools Inventory" — prevents duplicate input
- Progress bar updated to 8 steps

---

## [2.5.0] — 2026-03-14

### Added
- Export dropdown: Print/Save as PDF (window.print + print CSS), Copy Document Text (clipboard markdown), Download JSON
- Menu shows only options relevant to what was generated
- Print CSS: hides all UI chrome, renders all generated tabs for print (A4)

---

## [2.4.0] — 2026-03-14

### Added — Audience-Aware Generation
- `audTone()` — shared function injecting tone/depth/framing into all 3 prompts per audience
- `selAudFn()` — audience selection auto-sets output formats:
  - CISO → Dashboard + Document
  - CIO → Roadmap + Document
  - CISO+CIO → All 3
  - Board → Dashboard only
- `startGen()` — skips AI calls for unselected outputs (real token savings)
- Board document: 5 sections, 4,000 tokens, zero jargon
- Results tabs hide unselected outputs, auto-activate first visible

---

## [2.3.0] — 2026-03-14

### Added — Global AI-Driven Framework Recommendation Engine
- Replaced static 6-framework list with `FW_LIBRARY` — 25 globally relevant frameworks
- `buildSignalPrompt()` extended — AI returns `frameworks[]` in same scan JSON (zero extra tokens)
- `aiFrameworks` state var — AI populates after scan, drives all framework logic
- Tiered UI: Mandatory (pre-selected) / Recommended (pre-selected) / Also Consider (not selected)
- Company-specific AI reason per framework + library educational description
- Fallback defaults if AI returns no frameworks: ISO 27001 + NIST CSF 2.0
- `aiFrameworks` saved to SQLite + restored on session resume

### Fixed
- Scan error messages now actionable: 402 (no credits) → link to OpenRouter top-up; 401 → check key; 429 → wait 30s; 404 → Docker not running; parse failure → retry
- `lsAddGap()`, `lsAddOrgContext()`, `lsRemoveOrgCustom()` — all now call `autoSave()` correctly

---

## [2.2.0] — 2026-03-14

### Added
- localStorage API key + provider persistence — pre-fills on next visit
- "Saved" badge + "Forget" link on API key field
- Eye icon to show/hide key
- "Check Balance" button — OpenRouter returns live credit balance; others show honest explanation
- server.py: `_LEADERSHIP_KEYS` expanded with `our-history`, `history`, `founders`, `people`, `governance`, `senior`
- Leadership content slice bumped 1,500 → 3,000 chars

---

## [2.1.0] — 2026-03-08

### Added — Real AI Generation + Session Persistence
- `buildStrategyContext()` — collects company, signals, frameworks, inventory, gaps, audience
- `buildDashboardPrompt()` / `buildRoadmapPrompt()` / `buildDocumentPrompt()`
- `startGen()` — real async 3-call AI sequence with graceful per-call fallback
- `rDash()` / `rRoad()` / `rDoc()` — AI-data-aware rendering, static baseline fallback if AI fails
- Full wizard state auto-saved to SQLite on every mutation (17+ hooks)
- Session resume — fully restores all wizard state
- Session cards — status stripe, relative time, Resume CTA
- `STRATIQ_VERSION` constant and version pill
- Edit & Regenerate button in results header
- Fixes: stale AI vars on regeneration, CORS header for Anthropic browser-direct calls, double-`goTo` race condition

---

## [2.0.0] — 2026-02-28 (Phase 2 begins)

### Added — Real Scan Pipeline
- `callClaude()` — provider-agnostic, handles Anthropic, OpenAI, Google Gemini, OpenRouter
- `buildSignalPrompt()` — structured prompt for signal + company + framework extraction
- `startScan()` replaced stub with real async scrape → AI → parse → navigate flow
- `/api/scrape` endpoint added to server.py (BeautifulSoup scraping)
- Architecture confirmed: browser-direct AI calls, Flask handles scraping + SQLite only
- OpenRouter confirmed as EDR-safe provider for corporate firewall environments

---

## [1.0.0] — 2026-02-01 (Phase 1 — Design & UI)

### Added
- Single HTML file architecture (no frameworks, no build tools)
- Full 7-step wizard: API key, URL, Sources, Company Profile, Frameworks, Landscape, Output
- Results screen: sticky header, 3 tabs (Dashboard / Roadmap / Document)
- Dashboard: KPI cards, risk domain progress bars, framework alignment, strategic pillars
- Roadmap: 3-phase timeline (0–6mo, 6–12mo, 1–3yr), initiative cards
- Document: formal document with document control table, 8 sections, signature block
- Landscape: 68-category tools inventory, gaps, wishlist, replace, org context chips
- Framework selection: 6 frameworks with rationale
- Light theme (default) + dark theme, DM Sans font
- Flask backend: SQLite sessions, full CRUD API
- Dr. Muhammad Malik attribution on homepage
- CC BY-NC-SA 4.0 license
