<div align="center">

<img src="https://img.shields.io/badge/StratIQ-Intelligence%20Platform-006ECC?style=for-the-badge&logoColor=white" alt="StratIQ" height="36"/>

# StratIQ
### AI-Powered IT & Cybersecurity Strategy Intelligence Platform

**Enter a URL. Walk into the boardroom with a complete strategy.**

*Built for CISOs, CIOs, and those who wear both hats.*

<br/>

[![Docker Pulls](https://img.shields.io/docker/pulls/ambarishrh/stratiq?style=flat-square&logo=docker&logoColor=white&color=2496ED&label=Docker%20Pulls)](https://hub.docker.com/r/ambarishrh/stratiq)
[![Version](https://img.shields.io/badge/Version-2.9.4-006ECC?style=flat-square)](https://github.com/ambarishrh/stratiq/releases)
[![License](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey?style=flat-square)](LICENSE)
[![BYOK](https://img.shields.io/badge/AI-Bring%20Your%20Own%20Key-28a745?style=flat-square)](https://openrouter.ai)
[![Privacy](https://img.shields.io/badge/Data-100%25%20Local-success?style=flat-square)](#privacy--security)
[![Web](https://img.shields.io/badge/Web-GitHub%20Pages-222?style=flat-square&logo=github)](https://ambarishrh.github.io/stratiq)

<br/>

---

</div>

## What is StratIQ?

StratIQ is a **free, open-source, privacy-first platform** that empowers IT and cybersecurity leaders to generate board-ready strategy in under 30 minutes — without consultants, without enterprise tooling budgets, and without company data ever leaving their machine.

### Who it's designed for

Most organisations — especially mid-market — don't have a written IT or cybersecurity strategy. Hiring consultants costs $50,000–$200,000+. Internal teams lack time. Board pressure is increasing. Compliance deadlines are real. **StratIQ is built for those organisations — the ones starting from zero.**

StratIQ researches your company's public presence — homepage, about page, news, leadership — using AI-powered web search to understand your organisation's vision, mission, goals, and growth trajectory. It uses this as the foundation to build an IT and cybersecurity strategy grounded in where the business is actually going.

> **If your organisation already has a written corporate strategy, that should be your starting point.** StratIQ produces the first 80% — something credible, structured, and board-ready to build from, not a replacement for deep internal strategy work.

**StratIQ democratises what was previously only available to enterprises with large budgets.**

<br/>

## What It Produces

| Output | Description |
|--------|-------------|
| 🎯 **Executive Dashboard** | Maturity scores by domain, framework alignment, strategic pillars, KPIs including quantified financial risk exposure |
| 🗺️ **Strategic Roadmap** | 3-year phased initiative plan with budgets, owners, success criteria, and business cases |
| 📄 **Formal Strategy Document** | 12-section audit-ready document: threat landscape, governance model, risk quantification, resource plan, quick wins |

All outputs are **framework-aware** — pillars, risk domains, and initiatives are derived from your actual selected compliance stack, not generic boilerplate.

All outputs are **audience-aware** — language, depth, and framing adapt for CISO, CIO, combined leadership, or Board.

<br/>

## Deployment Options

StratIQ supports two deployment modes from the same file. Choose based on your needs.

---

### Option A — GitHub Pages / Static Hosting *(Zero Install)*

No Docker. No server. Open in a browser and go.

**Live instance:** **[https://ambarishrh.github.io/stratiq](https://ambarishrh.github.io/stratiq)**

Or deploy your own in 60 seconds:
1. Fork this repo on GitHub
2. Go to **Settings → Pages → Deploy from branch → `gh-pages` → root**
3. Access at `https://<your-username>.github.io/stratiq`

**How it works in this mode:**
- All data stored in your browser's IndexedDB — nothing leaves your machine, ever
- Company research powered by AI web search — no scraping, no CORS issues, works on every site
- Sessions persist across browser restarts on the same device
- No cross-device sync (by design — privacy first)

**Supported AI providers:** Anthropic Claude, OpenAI GPT-4o, Google Gemini, OpenRouter

---

### Option B — Docker *(Self-Hosted, Enterprise)*

Full persistence via SQLite. Air-gap capable. Multi-session support.

#### Mac / Linux

```bash
docker run -d -p 3000:3000 -v stratiq_data:/app/data \
  --name stratiq ambarishrh/stratiq:latest

open http://localhost:3000
```

#### Windows (PowerShell)

```powershell
docker run -d -p 3000:3000 -v stratiq_data:/app/data `
  --name stratiq ambarishrh/stratiq:latest

start http://localhost:3000
```

No configuration. No environment variables. No setup wizard. **Two commands.**

**Supported AI providers:** Anthropic Claude, OpenAI GPT-4o, Google Gemini, OpenRouter

---

### Comparison

| Feature | GitHub Pages | Docker |
|---|---|---|
| Installation | None | Docker required |
| Data storage | Browser IndexedDB | SQLite (server) |
| Cross-device sync | No | Yes (shared volume) |
| Company research | AI web search (primary) | AI web search (primary) |
| Scraping fallback | No | Yes — if AI web search fails |
| Air-gap support | No | Yes |
| Cost | Free | Free |

<br/>

## Bring Your Own Key (BYOK)

StratIQ never hosts or proxies your API key. All AI calls go directly from your browser to your chosen provider.

| Provider | Recommended For | Est. Cost Per Analysis | Get Key |
|----------|----------------|----------------------|---------|
| **OpenRouter** ⭐ | Most users — works through corporate firewalls/EDR | ~$0.01–0.05 | [openrouter.ai/keys](https://openrouter.ai/keys) |
| **Anthropic Claude** | Highest quality output | ~$0.05–0.15 | [console.anthropic.com](https://console.anthropic.com/settings/keys) |
| **OpenAI GPT-4o** | OpenAI ecosystem | ~$0.05–0.10 | [platform.openai.com](https://platform.openai.com/api-keys) |
| **Google Gemini** | Google ecosystem | ~$0.01–0.05 | [aistudio.google.com](https://aistudio.google.com/app/apikey) |

Your API key is stored only in your browser's localStorage — never transmitted to StratIQ.

> **Corporate firewall blocking Anthropic?** Switch to OpenRouter. It routes through a different endpoint that works in most corporate environments. Cost is identical.

<br/>

## How It Works

```
1. Enter company URL
2. AI researches the company using web search — homepage, about, news, leadership signals
3. AI extracts intelligence signals: vision, growth, sector, leadership gaps, risk signals
4. AI recommends applicable frameworks based on geography, sector, and regulatory signals
5. You complete a 14-question Internal Context Interview (budget, headcount, team structure, constraints)
6. You confirm your tools inventory, known gaps, and organisational context
7. AI generates all three outputs in ~60 seconds
8. Export as PDF, copy to Word, or download raw JSON
```

> **Docker users:** If AI web search fails (e.g. provider outage), StratIQ automatically falls back to live HTML scraping via BeautifulSoup. You get results either way.

<br/>

## Global Framework Intelligence

StratIQ recommends frameworks based on your company's geography, sector, and regulatory signals — not a hardcoded default list. 25 frameworks across all major regions, with full domain and obligation context.

All frameworks are **pre-selected by AI based on your scan** but remain fully editable — you can uncheck any framework, including ones tagged Mandatory, if it genuinely does not apply to your organisation. Mandatory means "regulatory requirement if you operate in this geography/sector" — not "you cannot remove it."

| Region | Frameworks |
|--------|-----------|
| 🇸🇦 Saudi Arabia | NCA ECC, SAMA CSF, NCA CSCC |
| 🇦🇪 UAE | ADHICS, UAE PDPL |
| 🇪🇺 European Union | GDPR, NIS2, DORA |
| 🇬🇧 United Kingdom | UK GDPR, NCSC CAF |
| 🇺🇸 United States | NIST CSF 2.0, NIST 800-53, HIPAA, PCI-DSS, CCPA, CMMC |
| 🇦🇺 Australia | ASD Essential 8, APRA CPS 234 |
| 🇸🇬 Singapore | MAS TRM, PDPA |
| 🇮🇳 India | DPDP Act, RBI Cybersecurity |
| 🌐 Global | ISO 27001, ISO 22301, ITIL 4 |

Frameworks are presented in three tiers: 🔴 **Mandatory** (pre-selected, editable) · 🔵 **Recommended** (pre-selected, editable) · ⚪ **Also Consider** (user opts in)

Any framework from the library can be added from a grouped dropdown — no free-text guessing.

**Framework-aware generation:** When you select ISO 27001 + GDPR + ADHICS, the AI generates pillars named *Information Security Governance*, *Data Privacy & Subject Rights*, and *Healthcare Information Security* — not generic NIST boilerplate. Every Mandatory framework gets a dedicated compliance initiative in the roadmap.

<br/>

## The Strategy Document — What's Inside

The full 12-section document is built for execution, not decoration:

| # | Section | What it contains |
|---|---------|-----------------|
| 1 | Executive Summary | Named risk + financial exposure + investment + board ask |
| 2 | Business Context & Why Now | Organisation signals, growth trajectory, why now |
| 3 | Threat Landscape | 3–4 named, sector-specific threats with financial impact |
| 4 | Strategic Vision & Pillars | Vision + 5–6 pillars derived from selected frameworks |
| 5 | Governance & Operating Model | Owner, reporting cadence, risk appetite statement |
| 6 | Current State Assessment | Maturity per NIST CSF 2.0 domain with gap + business consequence |
| 7 | Regulatory Obligations | One substantive paragraph per selected framework |
| 8 | 3-Year Roadmap Summary | Named initiatives, phase budgets, owners, year-3 outcome |
| 9 | Resource Plan | Year-by-year budget, MSSP vs in-house split, benchmarks |
| 10 | Risk Quantification | FAIR methodology: ransomware + breach + regulatory ranges |
| 11 | KPIs & Review Cadence | 5 board-level KPIs with baselines, targets, and review cadence |
| 12 | Quick Wins — Start Here | 5 actions this week, zero budget required |

<br/>

## Audience-Aware Generation

| Audience | Language Style | Auto-selects |
|----------|---------------|--------------|
| **CISO** | Security maturity, controls, framework compliance | Dashboard + Document |
| **CIO** | IT governance, digital transformation, service management | Roadmap + Document |
| **CISO + CIO** | Both lenses, unified strategy | All three outputs |
| **Board** | Zero jargon, risk in dollars, 5-section concise brief | Dashboard only |

<br/>

## Wizard Steps

1. **API Key** — Choose provider, enter key (saved to localStorage), check balance
2. **Company URL** — Enter URL, AI researches the company using web search
3. **Review Sources** — Review extracted signals, deselect or remove individual signals
4. **Company Profile** — Confirm AI-inferred company name, industry, region, size, stage
5. **Internal Context** — 14-question interview: budget, headcount, team, incidents, board attitude, constraints
6. **Frameworks** — Review AI-recommended frameworks by tier; add from full library dropdown; uncheck any that don't apply
7. **IT Landscape** — Tools inventory (68 categories), gaps, wishlist, replacements, org context
8. **Output Config** — Select audience and output formats
9. **Generate** — 3 sequential AI calls; export via PDF/print, copy to clipboard, or JSON download

<br/>

## Privacy & Security

| What | Where it happens |
|------|-----------------|
| Company research | Your browser → your AI provider (direct, no proxy) |
| AI generation | Your browser → your AI provider (direct, no proxy) |
| Session history (Docker) | Your machine only — SQLite in a local Docker volume |
| Session history (GitHub Pages) | Your browser only — IndexedDB, never leaves the device |
| Your API key | Browser localStorage only — never transmitted to StratIQ |
| Generated strategy | Your machine only |

> **StratIQ has no servers. There is nothing to breach.**

> **GitHub Pages mode:** Data never transits a network at all. AI calls go browser-direct to your provider. Session data lives in your browser's IndexedDB. StratIQ as a hosting provider has zero visibility into any data you enter.

<br/>

## Updating

```bash
docker pull ambarishrh/stratiq:latest
docker stop stratiq && docker rm stratiq
docker rmi ambarishrh/stratiq:latest
docker pull ambarishrh/stratiq:latest
docker run -d -p 3000:3000 -v stratiq_data:/app/data \
  --name stratiq ambarishrh/stratiq:latest
```

The `docker rmi` step removes any cached local image, ensuring you get the actual latest version from Docker Hub rather than a cached copy.

Session history is preserved in the `stratiq_data` volume across updates.

**GitHub Pages:** Simply refresh your browser. No install step required — the live instance at [https://ambarishrh.github.io/stratiq](https://ambarishrh.github.io/stratiq) always serves the latest version.

<br/>

## Building from Source

```bash
git clone https://github.com/ambarishrh/stratiq.git
cd stratiq
docker build -t stratiq .
docker run -d -p 3000:3000 -v stratiq_data:/app/data --name stratiq stratiq
open http://localhost:3000
```

**Stack:** Single-file HTML/JS frontend · Python Flask · SQLite · Docker · GitHub Pages

<br/>

## FAQ

**Does my company data leave my machine?**
No. In Docker mode, AI calls go browser-direct to your provider and session data stays in a local SQLite volume. In GitHub Pages mode, AI calls go browser-direct and session data lives in your browser's IndexedDB. Nothing passes through any StratIQ infrastructure in either mode.

**Is StratIQ free?**
Yes. StratIQ is free and open source. You pay only for your own AI API usage — typically a few cents per full analysis.

**Do I need Docker to use StratIQ?**
No. Open [https://ambarishrh.github.io/stratiq](https://ambarishrh.github.io/stratiq) in any browser and start immediately. Docker gives you SQLite persistence and scraping fallback, but is not required.

**We already have a corporate strategy document — how does that help?**
If you have a written organisational strategy, use it as your primary input. StratIQ's AI research gives a starting point by inferring strategy from public signals — your real internal strategy will always be richer. The best use in that case is alignment validation: does your IT and cybersecurity roadmap actually support where the business says it's going?

**Can I remove a Mandatory framework?**
Yes. Mandatory means the AI assessed it as a regulatory requirement given your geography or sector — it does not mean you are forced to include it. A CISO who understands their regulatory scope can uncheck any framework. Pre-selected does not mean locked.

**What if the scan returns limited signals?**
StratIQ flags inaccessible information and generates from whatever signals were collected. You can add context manually in the Internal Context Interview and Organisational Context sections before generating.

**How do I update my API key?**
Click the "Forget" link next to your saved key on the API screen, then enter the new one.

**Can I use this for client work?**
StratIQ is licensed CC BY-NC-SA 4.0 — free for non-commercial use with attribution. Contact us for commercial licensing.

**How do I completely remove StratIQ?**
```bash
docker stop stratiq && docker rm stratiq
docker volume rm stratiq_data
docker rmi ambarishrh/stratiq:latest
```
For GitHub Pages mode: clear your browser's IndexedDB for `ambarishrh.github.io` in browser settings.

<br/>

## Strategic Framework & Attribution

StratIQ's strategy generation engine draws on a broad body of established frameworks, methodologies, and published research — synthesised into a single coherent output that a CISO or CIO can walk into a boardroom with.

### Communication Philosophy
The language principles and communication framework are inspired by the published work of **[Dr. Muhammad Malik](https://www.linkedin.com/in/dr-muhammad-malik-45940a/)**.

> *"Clarity Over Controls: The One-Page Cybersecurity Strategy Every CISO Needs"*
>
> *"Learning Cybersecurity Strategy From Zero — A Guide for New and Seasoned Leaders"*
>
> *"Securing What Matters: Why Cyber Strategy Must Start with Business Truths"*

**Principles applied throughout:** Clarity over controls. Direction over decoration. Business language over technical jargon. Risk in dollars, not CVSS scores. Vision as one business outcome sentence. Strategy as a loop, not a one-time plan.

### Business Strategy Lenses
The 9 business intelligence lenses used to analyse organisations and generate context-aware strategy:

| Lens | Applied As |
|------|-----------|
| **OCAI Culture Model** | Infers org culture type from signals; adapts language (clan = storytelling, hierarchy = policies, market = ROI, adhocracy = innovation) |
| **SWOT Analysis** | Business lens mapped to NIST CSF initiative categories |
| **Porter's Five Forces** | Competitive forces translated into security priority areas |
| **Business Model Canvas** | Identifies what breaks under attack — crown jewels and critical dependencies |
| **Strategy Map (Kaplan & Norton)** | Capability → enabler → operational → financial → customer chain |
| **Stakeholder Mapping** | Adapts language and framing to power/interest/skill of the audience |
| **Crown Jewels Analysis** | Asset criticality, RTO, and business function mapping |
| **PESTEL Analysis** | External macro forces mapped to NIST CSF initiative priorities |
| **Business + Threat Timeline** | Growth milestones correlated against emerging threat trajectory |

### Risk Quantification
Risk scoring and financial exposure estimates follow the **FAIR methodology** (Factor Analysis of Information Risk) — frequency × impact framing, expressed in local currency, never CVSS scores.

### Cybersecurity Frameworks
Framework recommendations, control mappings, and compliance obligations draw on the official published documentation of 25 frameworks including NCA ECC, ADHICS, UAE PDPL, ISO 27001, NIST CSF 2.0, GDPR, and others. See the [Global Framework Intelligence](#global-framework-intelligence) section for the full list.

<br/>

## License

[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](LICENSE)

Free to use, share, and adapt for non-commercial purposes with attribution.

<br/>

## Contributing

Issues, feature requests, and pull requests are welcome. Please open an issue before starting significant work.

<br/>

---

<div align="center">

*Built for IT and security leaders who need strategy on the board's timeline — not the consultant's.*

**[Try it now — no install](https://ambarishrh.github.io/stratiq)** &nbsp;·&nbsp; **[Docker Hub](https://hub.docker.com/r/ambarishrh/stratiq)** &nbsp;·&nbsp; **[Report an Issue](https://github.com/ambarishrh/stratiq/issues)** &nbsp;·&nbsp; **[Dr. Muhammad Malik](https://www.linkedin.com/in/dr-muhammad-malik-45940a/)**

</div>
