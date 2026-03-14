# StratIQ — Project Brief & Continuation Guide
> Last updated: 08 March 2026 | Current version: v2.3.0
> Read this file at the start of every session. Keep it current at the end of every session.

---

## HOW TO RESUME THIS PROJECT
In a new Claude chat, say: "Continue StratIQ" or "Resume StratIQ"

The assistant reads this file from Project Knowledge and picks up exactly where we left off.
Summarise status in 3-5 bullets. State exact next action. Wait for confirmation before starting.

**CRITICAL RULES — NEVER BREAK:**
1. `str_replace` only — never full rebuilds of the HTML
2. Read the file before editing it
3. State what changes, why, and that it won't affect other parts — before every edit
4. Run full regression check before every handover
5. Update this brief + present both files at end of every session
6. Never remove working functionality
7. Warn at ~80% context window — wrap up cleanly, don't start large features above 70%

---

## PROJECT VISION & END GOAL

StratIQ is a **free, open-source, privacy-first AI platform** that enables any CISO or CIO — regardless of budget or team size — to generate a **board-ready, audit-quality IT & Cybersecurity Strategy** in under 30 minutes, using nothing but a company URL and their own AI API key.

### The Problem It Solves
Most organisations — especially mid-market — don't have a written IT or cybersecurity strategy. Hiring consultants costs $50,000–$200,000+. Internal teams lack time. Board pressure is increasing. Compliance deadlines are real. StratIQ democratises what was previously only available to enterprises with large budgets.

### The One-Line Goal
A CISO at a mid-market company installs StratIQ in 5 minutes, enters a URL, and walks into a board meeting the same day with a complete, audit-ready IT & cybersecurity strategy — in business language, not technical jargon.

### End Goal (Fully Built Product)
A **Docker-packaged desktop application** that:
1. Runs entirely locally — no cloud, no SaaS, no data leaving the machine
2. Takes a company URL as input
3. Scrapes public intelligence (homepage, about, news, leadership)
4. Accepts practitioner context (existing tools, gaps, wishlist, org realities)
5. Uses AI (user's own API key — Anthropic/OpenAI/Google/OpenRouter) to generate:
   - **Executive Dashboard** — maturity scores, risk domains, framework alignment, strategic pillars
   - **Strategic Roadmap** — 3-year phased plan with initiatives, AED budgets, priorities
   - **Formal Strategy Document** — ISO-compliant, audit-ready, document control
6. Exports everything — PDF dashboard, .docx strategy document, roadmap print view
7. Installable via a single launcher script (no Docker knowledge required)

---

## CURRENT STATE

### Active Files
- `stratiq_8.html` — main frontend, single HTML file (~2090 lines, **v2.3.0**)
- `server.py` — Flask backend (scraping + SQLite). **IMPORTANT: use the fixed version — dead provider imports removed**
- `Dockerfile` — python:3.11-slim, port 3000
- `requirements.txt` — flask, flask-cors, requests, beautifulsoup4, lxml
- `providers/` — legacy modules, NOT used, NOT needed in Docker image

### CRITICAL: server.py state
The `server.py` in Project Knowledge still has broken imports:
```python
from providers import get_provider      # ← CRASHES Flask if providers/ dir missing
from providers.base import ProviderError
```
The **fixed server.py** (with these lines removed) has been presented for download multiple times.
Every Docker rebuild with the old server.py produces a broken container — `/api/scrape` returns 404.
**Always use the fixed server.py from outputs when rebuilding Docker.**

### HTML Structure (single file, no build tools)
```
<head>          — DM Sans font, all CSS variables (light + dark themes), animations
<body>
  #ver-badge    — fixed top-left version pill (hidden on results screen)
  #theme-btn    — fixed top-right dark/light toggle
  #wiz-prog     — fixed top progress bar
  #wiz-dots     — fixed bottom step dots

  Screens (shown/hidden via goTo()):
  #screen-api        — Step 0: API key + provider + recent sessions + Dr. Malik credit
  #screen-url        — Step 1: Company URL input + scan trigger
  #screen-sources    — Step 2: Review extracted signals, toggle sources/signals
  #screen-company    — Step 3: Company profile confirmation
  #screen-frameworks — Step 4: Framework selection
  #screen-landscape  — Step 5: Tools inventory, gaps, wishlist, replace, org context
  #screen-output     — Step 6: Audience + output format selection
  #screen-generating — Generating: progress spinner + 3-call AI status
  #screen-results    — Results: sticky header + tabs (Dashboard / Roadmap / Document)

<script>        — All JS (state vars, all functions, page-load init)
```

### Architecture (LOCKED)
```
Browser → POST /api/scrape → Flask scrapes company pages → returns clean text
Browser → calls AI provider DIRECTLY (browser-direct fetch)
Browser → POST /api/session/:id/save → Flask saves to SQLite
```
AI calls are browser-direct. Flask handles scraping + SQLite only. No AI in Flask.

### Provider Support
| Provider | Endpoint | Notes |
|---|---|---|
| Anthropic | api.anthropic.com/v1/messages | Requires `anthropic-dangerous-direct-browser-access: true` header |
| OpenAI | api.openai.com/v1/chat/completions | gpt-4o |
| Google | generativelanguage.googleapis.com | gemini-1.5-pro |
| OpenRouter | openrouter.ai/api/v1/chat/completions | **RECOMMENDED for corporate EDR** — not blocked by MDE |

### Network/EDR Issue (DOCUMENTED)
- MDE (Microsoft Defender for Endpoint) on developer's Mac blocks Python/Docker → api.anthropic.com
- Browser fetch works fine. OpenRouter bypasses this entirely.
- Most corporate machines without personal MDE config work fine with Anthropic direct.
- OpenRouter requires credits — top up at https://openrouter.ai/settings/credits

### Docker Deploy
```bash
# Always use fixed server.py (no providers import)
docker build -t stratiq .
docker stop stratiq && docker rm stratiq
docker run -d -p 3000:3000 -v stratiq_data:/app/data --name stratiq stratiq
open http://localhost:3000
# Verify version pill shows v2.3.0 top-left
```

### Versioning Convention
- `STRATIQ_VERSION` JS constant — displayed as fixed pill top-left (hidden on results screen)
- Format: `MAJOR.MINOR.PATCH`
- Bug fix → patch bump (2.1.8 → 2.1.9)
- New feature → minor bump (2.1 → 2.2)
- New phase → major bump (2.x → 3.x)
- Always tell user new version number after each change

---

## KEY STATE VARIABLES

```javascript
const STRATIQ_VERSION = '2.5.0'

// Auth & Provider
let curProv = 'anthropic'           // active provider
let apiKey = ''                     // set on Initialize click

// Session
let currentSessionId = null         // SQLite session UUID
let _pendingResumeId = null         // session queued for resume before key entry

// AI outputs (reset to null at start of every startGen())
let aiDashboard = null              // parsed JSON from dashboard AI call
let aiRoadmap = null                // parsed JSON from roadmap AI call
let aiDocument = null               // parsed JSON from document AI call

// Sources
const SOURCES = [...]               // {icon, label, url, signals[]}
let srcSel = [true,true,true,true]  // which sources selected
let removedSignals = new Set()      // individually removed signal IDs

// Frameworks
const FW_LIBRARY = {...}            // 25 global frameworks (UAE/GCC, EU, USA, APAC, UK, India, Global)
let aiFrameworks = []               // AI-populated after scan: [{id,name,priority,reason,color,region,sector}]
let selFw = new Set()               // Mandatory+Recommended auto-selected; Consider unselected

// Landscape
let lsInventory = []                // confirmed tools
const LS_GAPS = [...]               // identified gaps
const LS_WISHLIST = [...]           // pipeline items
let LS_REPLACE = []                 // replacement candidates
let lsOrgChips = new Set([...])     // org context chip IDs
let lsOrgCustom = []                // free-text org context items
let lsOrgText = ''                  // current textarea value

// Output config
let selAud = 'both'                 // ciso | cio | both | board
let selOut = new Set(['dashboard','roadmap','document'])

let isDark = false
```

---

## AI GENERATION PIPELINE

Three sequential AI calls, each feeding the next:

**Call 1 — Dashboard** (`buildDashboardPrompt`):
- Input: company, signals, frameworks, inventory, gaps
- Output JSON: `{companyName, vision, tagline, kpis[4], risks[6], pillars[4]}`
- max_tokens: 4000

**Call 2 — Roadmap** (`buildRoadmapPrompt`):
- Input: company, signals, frameworks, inventory, gaps, pillar names from dashboard
- Output JSON: `{phases[3], totalBudget, roiStatement}`
- Each phase: `{label, theme, color, items[]}` — items have title, domain, priority, budget, businessCase, desc
- Instruction: every gap must map to at least one initiative; don't re-recommend tools already in inventory
- max_tokens: 4000

**Call 3 — Document** (`buildDocumentPrompt`):
- Input: company, signals, frameworks, inventory, gaps, vision+pillars from dashboard, full roadmap phases
- Output JSON: `{title, subtitle, docRef, sections[8]}`
- Sections: Executive Summary, Business Context, Strategic Vision, Pillars, Current State, Regulatory, Roadmap Summary, Measuring Success
- Section 5 references actual gaps; Section 7 references actual roadmap initiatives
- max_tokens: 8000 (8 full prose sections needs extra tokens)

**JSON cleaning** (`cleanJSON`): strips markdown fences, extracts first `{...}` object — handles any preamble/trailing text

**Error handling**: each call wrapped separately — failure falls back to static baseline, never blocks the other calls

---

## PHASE STATUS

### Phase 1: Design & UI ✅ COMPLETE
Full wizard (7 steps + generating + results), all screens, light/dark themes, DM Sans, responsive, animations.

### Phase 2: Functionality & AI ← IN PROGRESS
- [x] URL scan — /api/scrape + browser-direct AI signal extraction
- [x] OpenRouter EDR-safe path confirmed working
- [x] Real AI strategy generation — 3 sequential calls
- [x] buildStrategyContext / buildDashboardPrompt / buildRoadmapPrompt / buildDocumentPrompt
- [x] Roadmap includes inventory context + gap-to-initiative mapping instruction
- [x] Document includes actual roadmap phases, gaps, inventory
- [x] AI vars reset at start of every generation (fixes stale regeneration)
- [x] rDash / rRoad / rDoc — AI-data-aware rendering, static fallback if AI fails
- [x] Full wizard state auto-saved to SQLite on every change (17+ mutation hooks)
- [x] Session resume — fully restores all state
- [x] Session cards — status stripe, Resume CTA, relative time, hover glow
- [x] Pending resume — queue before key entry, auto-resume after Initialize
- [x] Version badge all screens (hidden on results)
- [x] Results header version dynamic (reads STRATIQ_VERSION)
- [x] Edit & Regenerate button in results header
- [x] New Analysis button in results header
- [x] Dr. Malik credit on homepage (screen-api), removed from document footer
- [x] Scan error messages — actionable (402/401/429/404/parse errors)
- [x] Landscape save fixes — lsAddGap, lsAddOrgContext, lsRemoveOrgCustom all autoSave
- [x] Framework recommendation engine (AI-driven, post-scan) — Option C hybrid, 25 global frameworks, tiered UI
- [x] Export dropdown — Print/PDF (window.print + print CSS), Copy Document Text (clipboard markdown), Download JSON
- [x] Audience-aware generation — audTone() injects tone/depth/framing per audience into all 3 prompts
- [x] Audience auto-selects output formats (CISO=dash+doc, CIO=road+doc, both=all3, board=dash only)
- [x] startGen() skips unselected output calls — real token savings
- [x] Results tabs hide unselected outputs, auto-activate first visible
- [x] Board document: 5 sections, 4000 tokens, pure business language
- [x] FWS → aiFrameworks migration complete (buildStrategyContext, rDash fixed)
- [x] localStorage API key + provider persistence (loadSavedKey, forgetSavedKey)
- [x] Balance checker — OpenRouter live balance, honest messages for others
- [x] server.py: _LEADERSHIP_KEYS expanded (our-history, history, founders, people, governance, senior)
- [x] Leadership content slice 1500 → 3000 chars

### Phase 3: Docker Packaging ← NOT STARTED

---

## EXACT NEXT ACTION

**Word document export** — next enhancement for export:
- POST to Flask `/api/export/docx` using python-docx, returns file download
- Cover page, document control table, all sections, roadmap table, signature block
- Requires `server.py` change + `requirements.txt` update (add python-docx)

**Then:** End-to-end test across all 4 audience types with a real company URL

---

## REQUIRED FUNCTIONS (46 — all must be present)

```
Core:       initStratIQ, goTo, updProg, selProv, toggleTheme, genUUID
Sessions:   loadSessions, resumeSession, deleteSession, sessionCard,
            renderSessionsList, relTime
Auto-save:  buildWizardState, autoSave, _doAutoSave, flashSaved,
            saveSessionScan, saveSessionGeneration
Scan:       startScan, buildSignalPrompt, scanStep, scanError
Sources:    rSrc, tSrc, removeSig, restoreAll
Frameworks: rFw, tFw
Landscape:  rLandscape, lsAddToolFromRow, lsRemoveTool, lsSetStatus, lsSetCov,
            lsToggleChip, lsAddOrgContext, lsRemoveOrgCustom, lsRemoveGap,
            lsAddGap, lsAddWishlist, lsRemoveWishlist, lsAddReplace, lsRemoveReplace
Output:     rOut, selAudFn, tOut
AI gen:     buildStrategyContext, buildDashboardPrompt, buildRoadmapPrompt,
            buildDocumentPrompt, cleanJSON, genSetStatus, startGen, callClaude
Results:    rResults, rDash, rRoad, rDoc, switchTab
```

---

## REGRESSION CHECK (mandatory before every handover)

```python
import re, subprocess, tempfile
from collections import Counter

with open('/home/claude/stratiq_8.html','r') as f:
    html = f.read()

s=html.index('<script>'); e=html.index('</script>')
js=html[s+8:e]

with tempfile.NamedTemporaryFile(mode='w',suffix='.js',delete=False) as f:
    f.write(js); fname=f.name
r=subprocess.run(['node','--check',fname],capture_output=True,text=True)
print("SYNTAX:", "PASS" if r.returncode==0 else "FAIL:\n"+r.stdout+r.stderr)

REQUIRED=[
    'function initStratIQ(','function goTo(','async function startScan(',
    'async function startGen(','function cleanJSON(','function callClaude(',
    'function buildStrategyContext(','function buildDashboardPrompt(',
    'function buildRoadmapPrompt(','function buildDocumentPrompt(',
    'function resumeSession(','function rDash(','function rRoad(','function rDoc(',
    'function autoSave(','function buildWizardState(','function lsAddGap(',
    'function lsAddOrgContext(','function lsRemoveOrgCustom(',
    'STRATIQ_VERSION','id="ver-badge"','id="res-ver-num"','_pendingResumeId',
    'aiDashboard=null;aiRoadmap=null;aiDocument=null',
    'anthropic-dangerous-direct-browser-access',
    'max_tokens:maxTok','maxTok=4000',',8000)',
    'road.phases','CURRENT TOOLS INVENTORY','IDENTIFIED GAPS',
    'dr-muhammad-malik','Insufficient credits'
]
missing=[r for r in REQUIRED if r not in html]
print(f"REQUIRED: {len(REQUIRED)-len(missing)}/{len(REQUIRED)}",
      "ALL OK" if not missing else f"\nMISSING: {missing}")

fns=re.findall(r'(?:async\s+)?function (\w+)\(',js)
dups={k:v for k,v in Counter(fns).items() if v>1}
print("DUPLICATES:", "none" if not dups else dups)

sg=js.split('async function startGen')[1].split('\nasync function')[0]
print("startGen resets AI vars:", "aiDashboard=null" in sg)
print("startGen no double-goTo:", "goTo('generating')" not in sg)
print("doc call 8000 tokens:", ',8000)' in sg)
print("Malik credit on homepage only:", html.count('dr-muhammad-malik')==1)
print("version:", re.search(r"STRATIQ_VERSION='([^']+)'",html).group(1))
```

---

## STRATEGIC FRAMEWORK — DR. MUHAMMAD MALIK

LinkedIn: https://www.linkedin.com/in/dr-muhammad-malik-45940a/
**Credit mandatory in StratIQ homepage (screen-api). NOT in the formal document.**

### Three Articles to Credit
1. "Clarity Over Controls: The One-Page Cybersecurity Strategy Every CISO Needs"
2. "Learning Cybersecurity Strategy From Zero — A Guide for New and Seasoned Leaders"
3. "Securing What Matters: Why Cyber Strategy Must Start with Business Truths"

### Core Principles (applied in all AI prompts and output language)
- Clarity over controls. Direction over decoration. Business language over technical jargon.
- **Vision:** one sentence, business outcome. e.g. "We reduce the probability that a cyber event materially impacts the business."
- **Pillars (board language):** Assume Breach / Make Risk Visible / Secure What Matters Most / Embed Resilience Into Culture
- Risk in dollars, not CVSS. Risk ownership to business units, not security team.
- Strategy is a loop: Year 1 = foundation wins, Year 2 = learn & adjust, Year 3 = mature & certify
- 9 Business Intelligence Lenses: Culture (OCAI), SWOT, Porter's Five Forces, Business Model Canvas, Strategy Map, Stakeholder Map, Crown Jewels, PESTEL, Business + Threat Timeline

### Language Rules for AI Prompts
- NEVER: "Privilege escalation vulnerability found"
- ALWAYS: "SSO compromise enables exec impersonation and financial fraud"
- Always above-the-line: revenue, brand, downtime
- Never surprise the CEO. Align before presenting.

---

## LOCKED DECISIONS
- Light theme default; dark theme available but parked for polish
- Font: DM Sans (Google Fonts)
- Single HTML file — no frameworks, no build tools
- BYOK model — no hosted API keys, no data leaves user's machine
- CC BY-NC-SA license
- Dr. Malik credit mandatory on homepage
- AI calls are browser-direct (not proxied through Flask)
- OpenRouter recommended as default for corporate/EDR environments
- Version format: MAJOR.MINOR.PATCH

---

## KNOWN ISSUES / TECH DEBT
- About page scraping thin on some sites (URL construction edge case — fix in Phase 3)
- "Not provided in content" sometimes appears as company description on scan
- providers/ directory referenced in Dockerfile COPY — can be removed in Phase 3 cleanup
- server.py in Project Knowledge has broken imports — always use the fixed version from outputs

---

## CHANGELOG

### 14 March 2026 — v2.3.0 → v2.5.0: Global framework engine + audience-aware generation + export

**v2.3.0 — Global AI-driven framework recommendation engine**
- Replaced static 6-framework list with `FW_LIBRARY` — 25 globally relevant frameworks
  - Covers: UAE/GCC, EU (GDPR/NIS2/DORA), USA (HIPAA/PCI-DSS/CMMC/CCPA), UK, Australia, Singapore, India, Global
- `buildSignalPrompt()` extended — AI returns `frameworks[]` in same scan JSON (zero extra tokens)
- `aiFrameworks` state var — AI populates after scan, drives all framework logic
- Tiered UI: Mandatory (pre-selected) / Recommended (pre-selected) / Also Consider (not selected)
- Company-specific AI reason per framework + library educational description
- Fallback defaults if AI returns no frameworks: ISO 27001 + NIST CSF
- `aiFrameworks` saved to SQLite + restored on session resume
- Removed old `inferFrameworks()` keyword matching
- Fixed: `FWS is not defined` — `buildStrategyContext()` and `rDash()` migrated to `aiFrameworks`

**v2.4.0 — Audience-aware generation + output format logic**
- `audTone()` — new shared function, injects audience tone/depth/framing into all 3 prompts
  - CISO: security-aware, controls + maturity language
  - CIO: IT governance, digital transformation, ITIL framing
  - CISO+CIO: balanced both lenses
  - Board: zero jargon, risk in dollars, pure business language
- `selAudFn()` — audience selection now auto-sets `selOut`:
  - CISO → Dashboard + Document
  - CIO → Roadmap + Document
  - CISO+CIO → All 3
  - Board → Dashboard only
- `startGen()` — skips AI calls for unselected outputs (real token savings)
  - Progress bar recalculates dynamically per selected outputs
  - Board document: 4000 tokens (5 sections), full doc: 8000 tokens (8 sections)
- Results tabs: hide unselected, auto-activate first visible

**v2.5.0 — Export dropdown**
- Dead Export button replaced with working dropdown menu
- Print / Save as PDF: window.print() with full print CSS (A4, nav hidden, all tabs visible)
- Copy Document Text: clipboard markdown of all sections, "Copied!" confirmation
- Download JSON: stratiq_<company>_<date>.json with all AI outputs
- Menu only shows options relevant to what was generated
- Closes on outside click
- Print CSS: hides all UI chrome, renders all generated tabs for print

### 14 March 2026 — v2.2.0 → v2.3.0: Saved API key + global framework engine

**v2.2.0 — Saved API key + balance checker + leadership scan fix**
- localStorage persistence for provider + API key — pre-fills on next visit
- "Saved" badge + "Forget" link on API key field
- Eye icon to show/hide key
- "Check Balance" button — OpenRouter returns real credit balance; others show honest explanation
- server.py: `_LEADERSHIP_KEYS` expanded with `our-history`, `history`, `founders`, `people`, `governance`, `senior`
- server.py: `_ABOUT_KEYS` expanded with `our-journey`, `our-history`
- Leadership content slice bumped 1500 → 3000 chars

**v2.3.0 — Global AI-driven framework recommendation engine**
- Replaced static 6-framework hardcoded list with `FW_LIBRARY` — 25 globally relevant frameworks
  - Covers: UAE/GCC, EU, USA, UK, Australia, Singapore, India, Global/sector-specific
- `buildSignalPrompt()` extended — AI returns `frameworks[]` array in same JSON response (zero extra tokens)
- `aiFrameworks` state var — AI populates after scan, replaces hardcoded `FWS` + `selFw`
- Tiered framework UI in `rFw()`:
  - **Mandatory** — pre-selected, regulatory requirement
  - **Recommended** — pre-selected, strongly applicable
  - **Also Consider** — shown but not pre-selected, with educational note
- AI provides company-specific reason per framework (not generic boilerplate)
- Library `desc` shown as educational tooltip below AI reason
- Fallback if AI doesn't return frameworks — sensible global defaults (ISO 27001, NIST CSF)
- `aiFrameworks` saved to SQLite + restored on session resume
- Removed old `inferFrameworks()` keyword matching (replaced by AI)

### 08 March 2026 — v2.3.0: Scan error messages
- Generic "Failed to fetch" replaced with specific actionable error messages
- 402 (no credits): shows link to openrouter.ai/settings/credits
- 401 (bad key): tells user to check their API key for the selected provider
- 429 (rate limit): tells user to wait 30 seconds
- 404 (Docker down): tells user container may not be running + docker start command
- Parse failure: tells user it's a one-off, try again
- scanError() upgraded from textContent to innerHTML to support links

### 08 March 2026 — v2.1.8: Fix stale regeneration + gaps/inventory missing from outputs
- `startGen()` now resets `aiDashboard=null`, `aiRoadmap=null`, `aiDocument=null` before every run
  - Root cause: Edit & Regenerate re-used stale AI data from previous run, appeared to "skip"
- `buildRoadmapPrompt` now includes full tools inventory + signals
  - Instruction added: "do NOT re-recommend tools already in inventory"
  - Instruction added: "every identified gap must map to at least one initiative"
- `buildDocumentPrompt` now includes inventory and gaps
  - Section 5 (Current State) explicitly instructed to reference actual gaps
  - Section 7 (Roadmap Summary) references actual phases and initiatives

### 08 March 2026 — v2.1.7: Dr. Malik credit location + document includes roadmap
- Malik credit removed from formal document footer
- Malik credit added as attribution block on homepage (screen-api) — shows 3 article titles
- `buildDocumentPrompt` now serialises full roadmap phases into prompt
  - Section 7 now references actual initiative names, timelines and budgets

### 08 March 2026 — v2.1.6: Results header UI audit
- ver-badge (version pill) hidden on results screen — was overlapping StratIQ logo
- Results header version badge now reads STRATIQ_VERSION dynamically (was hardcoded "v2.1")
- Company name in results header no longer shows dummy "Emirates Integrated Group"
  - Priority: AI dashboard company name > typed value (if not the demo placeholder)
- Sticky header right padding increased to 170px — New Analysis button was hidden behind Dark Mode

### 08 March 2026 — v2.1.5: Fix generated document always showing static/generic content
- Root cause: document AI call had `max_tokens:4000` — 8 prose sections exceeds this, response
  truncated mid-JSON, parse threw, aiDocument stayed null, static fallback rendered every time
- `callClaude()` signature changed to `callClaude(prompt, maxTok=4000, system='')`
- Dashboard + roadmap calls: 4000 tokens (sufficient)
- Document call: 8000 tokens (needed for 8 full prose sections)
- `cleanJSON()` helper added — strips markdown fences, extracts first `{...}` object
  - More robust than `.replace(/```json|```/g,'')` which failed on edge cases

### 08 March 2026 — v2.1.4: Landscape save bugs
- `lsAddGap()` — missing `autoSave()` call; gaps added but never persisted
- `lsAddOrgContext()` — `autoSave()` fired before push; saved state without the new item
- `lsRemoveOrgCustom()` — missing `autoSave()` call; removals not persisted

### 08 March 2026 — v2.1.3: Bugfix — Resume not working when API key already typed
- Root cause: `resumeSession()` checked `apiKey` JS variable (empty until Initialize clicked)
- Fix: reads `document.getElementById('api-inp').value.trim()` directly if `apiKey` unset
- If key typed but Initialize not yet clicked → grabs it immediately, resumes
- If no key at all → sets `_pendingResumeId`, shows hint above Initialize button

### 08 March 2026 — v2.1.2: Bugfix — dummy/static report + Edit & Regenerate
- Root cause 1: `startGen()` called `goTo('generating')` which re-triggered `startGen()` via
  goTo dispatch — double execution race condition
- Root cause 2: Missing `anthropic-dangerous-direct-browser-access: true` header — browser CORS
  block caused silent failure, fell through to static fallback every time
- Fix: removed redundant `goTo('generating')` from inside `startGen()`
- Fix: added CORS header to Anthropic callClaude() headers
- Added "Edit & Regenerate" button in results header
- Company name in results header now dynamic

### 08 March 2026 — v2.1.1: Bugfix — Initialize does nothing
- Root cause: `STRATIQ_VERSION`, `_pendingResumeId`, `aiDashboard`, `aiRoadmap`, `aiDocument`
  used but never declared — written to stale intermediate files in earlier patch sessions
- Fix: all 5 missing declarations added at correct position before first use
- Mandatory regression check added as session rule

### 08 March 2026 — v2.1: AI generation + session persistence + resume UX + versioning
- `buildStrategyContext()` — collects company, signals, frameworks, inventory, gaps, audience
- `buildDashboardPrompt()` / `buildRoadmapPrompt()` / `buildDocumentPrompt()` added
- `startGen()` — real async 3-call AI sequence, graceful fallback per call
- `rDash()` / `rRoad()` / `rDoc()` — AI-data-aware, static baseline fallback
- `buildWizardState()` — serialises 14 state fields
- `autoSave()` — debounced 1.2s, 17 mutation hooks
- `flashSaved()` — green "Saved" pill confirmation
- `saveSessionGeneration()` — persists all 3 AI outputs
- `resumeSession()` — restores full wizard state, navigates to correct screen
- Session cards redesigned — status stripe, relative time, Resume CTA
- `STRATIQ_VERSION` constant, pill top-left, inline badge in results header
- Bug fixed: version init code injected inside `deleteSession` try block by bad patch

### March 2026 — Phase 2: Network/EDR debugging + first successful scan
- Diagnosed MDE blocking Python/Docker → api.anthropic.com on developer's machine
- Tried: browser-direct, Flask proxy, curl subprocess, Node.js proxy, SDK — all blocked by MDE
- Solution: OpenRouter as EDR-safe provider
- Confirmed scan end-to-end on yasholding.ae — 15 real signals extracted
- Architecture finalised: browser-direct AI, Flask for scraping + SQLite only
- server.py updated: /api/scrape, /api/scan/save, /api/ai proxy (kept but not used by HTML)
- callClaude() supports all 4 providers with correct browser-direct headers

### February 2026 — Phase 2 Session 1: Real scan pipeline
- Added `curProv` and `apiKey` state vars
- Added `callClaude()` — provider-agnostic, handles all 4 providers
- Added `buildSignalPrompt()` — structured prompt for signal extraction
- Replaced animation-only `startScan()` stub with real async scrape → AI → parse → navigate
- Added `/api/scrape` endpoint to server.py (BeautifulSoup scraping)
- Docker architecture confirmed: hybrid (browser AI + Flask scraping + SQLite)

### Previous Sessions — Phase 1: Design & UI (complete)
- Single HTML file architecture decided — no frameworks, no build tools
- Full wizard: API screen, URL screen, Sources, Company, Frameworks, Landscape, Output, Generating, Results
- Results screen: sticky header, 3 tabs (Dashboard / Roadmap / Document)
- Dashboard: KPI cards, risk domain progress bars, framework alignment, strategic pillars grid
- Roadmap: 3-phase timeline (0-6mo, 6-12mo, 1-3yr), initiative cards with domain/priority badges
- Document: styled formal document with document control table, 8 sections, signature block
- Landscape: 68-category tools inventory with single-row add form, gaps, wishlist, replace, org chips
- Framework selection: 6 frameworks with rationale (NCA ECC, ISO 27001, NIST CSF, ADHICS, GDPR, ITIL 4)
- Light theme (default) + dark theme, DM Sans, CSS variables for both themes
- Fixed progress bar top, step dots bottom, version badge top-left, theme toggle top-right
- Author credit block on homepage: Dr. Muhammad Malik, LinkedIn link, 3 articles cited
- CC BY-NC-SA license footer
- Flask backend: SQLite sessions, session_data, audit_log tables; full CRUD endpoints
