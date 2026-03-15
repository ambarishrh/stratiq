<div align="center">

<img src="https://img.shields.io/badge/StratIQ-Intelligence%20Platform-006ECC?style=for-the-badge&logoColor=white" alt="StratIQ" height="36"/>

# StratIQ
### AI-Powered IT & Cybersecurity Strategy Intelligence Platform

**Enter a URL. Walk into the boardroom with a complete strategy.**

*Built for CISOs, CIOs, and those who wear both hats.*

<br/>

[![Docker Pulls](https://img.shields.io/docker/pulls/ambarishrh/stratiq?style=flat-square&logo=docker&logoColor=white&color=2496ED&label=Docker%20Pulls)](https://hub.docker.com/r/ambarishrh/stratiq)
[![Version](https://img.shields.io/badge/Version-2.8.1-006ECC?style=flat-square)](https://github.com/ambarishrh/stratiq/releases)
[![License](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey?style=flat-square)](LICENSE)
[![BYOK](https://img.shields.io/badge/AI-Bring%20Your%20Own%20Key-28a745?style=flat-square)](https://openrouter.ai)
[![Privacy](https://img.shields.io/badge/Data-100%25%20Local-success?style=flat-square)](#privacy--security)

<br/>

---

</div>

## What is StratIQ?

StratIQ is a **free, open-source, privacy-first platform** that empowers IT and cybersecurity leaders to generate board-ready strategy in under 30 minutes — without consultants, without enterprise tooling budgets, and without company data ever leaving their machine.

### Who it's designed for

Most organisations — especially mid-market — don't have a written IT or cybersecurity strategy. Hiring consultants costs $50,000–$200,000+. Internal teams lack time. Board pressure is increasing. Compliance deadlines are real. **StratIQ is built for those organisations — the ones starting from zero.**

StratIQ scrapes your company's public presence — homepage, about page, news, leadership — to understand your organisation's vision, mission, goals, and growth trajectory. It uses this as the foundation to build an IT and cybersecurity strategy grounded in where the business is actually going.

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

## Quick Start

> **Only requirement:** [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### Mac / Linux

```bash
docker run -d -p 3000:3000 -v stratiq_data:/app/data \
  --name stratiq ambarishrh/stratiq:latest

open http://localhost:3000
```

### Windows (PowerShell)

```powershell
docker run -d -p 3000:3000 -v stratiq_data:/app/data `
  --name stratiq ambarishrh/stratiq:latest

start http://localhost:3000
```

No configuration. No environment variables. No setup wizard. **Two commands.**

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
2. StratIQ scrapes homepage, about, news, and leadership pages
3. AI extracts intelligence signals: vision, growth, sector, leadership gaps, risk signals
4. AI recommends applicable frameworks based on geography, sector, and regulatory signals
5. You complete a 14-question Internal Context Interview (budget, headcount, team structure, constraints)
6. You confirm your tools inventory, known gaps, and organisational context
7. AI generates all three outputs in ~60 seconds
8. Export as PDF, copy to Word, or download raw JSON
```

<br/>

## Global Framework Intelligence

StratIQ recommends frameworks based on your company's geography, sector, and regulatory signals — not a hardcoded default list. 25 frameworks across all major regions, with full domain and obligation context:

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

Frameworks are presented in three tiers: 🔴 **Mandatory** (pre-selected) · 🔵 **Recommended** (pre-selected) · ⚪ **Also Consider** (user opts in)

Any framework from the library can be added from a grouped dropdown — no free-text guessing.

**Framework-aware generation:** When you select ISO 27001 + GDPR + ADHICS, the AI generates pillars named *Information Security Governance*, *Data Privacy & Subject Rights*, and *Healthcare Information Security* — not generic NIST boilerplate. Every Mandatory framework gets a dedicated compliance initiative in the roadmap. The regulatory section writes one substantive paragraph per framework linking it to your specific gaps and roadmap.

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
2. **Company URL** — Enter URL, StratIQ scrapes 4 pages (homepage, about, news, leadership)
3. **Review Sources** — Review extracted signals, deselect or remove individual signals
4. **Company Profile** — Confirm AI-inferred company name, industry, region, size, stage
5. **Internal Context** — 14-question interview: budget, headcount, team, incidents, board attitude, constraints
6. **Frameworks** — Review AI-recommended frameworks by tier; add from full library dropdown
7. **IT Landscape** — Tools inventory (68 categories), gaps, wishlist, replacements, org context
8. **Output Config** — Select audience and output formats
9. **Generate** — 3 sequential AI calls; export via PDF/print, copy to clipboard, or JSON download

<br/>

## Privacy & Security

| What | Where it happens |
|------|-----------------|
| Company URL scraping | Your Docker container → public internet |
| AI generation | Your browser → your AI provider (direct, no proxy) |
| Session history | Your machine only — SQLite in a local Docker volume |
| Your API key | Browser localStorage only — never transmitted to StratIQ |
| Generated strategy | Your machine only |

> **StratIQ has no servers. There is nothing to breach.**

<br/>

## Updating

```bash
docker pull ambarishrh/stratiq:latest
docker stop stratiq && docker rm stratiq
docker run -d -p 3000:3000 -v stratiq_data:/app/data \
  --name stratiq ambarishrh/stratiq:latest
```

Session history is preserved in the `stratiq_data` volume across updates.

<br/>

## Building from Source

```bash
git clone https://github.com/ambarishrh/stratiq.git
cd stratiq
docker build -t stratiq .
docker run -d -p 3000:3000 -v stratiq_data:/app/data --name stratiq stratiq
open http://localhost:3000
```

**Stack:** Single-file HTML/JS frontend · Python Flask · SQLite · Docker

<br/>

## FAQ

**Does my company data leave my machine?**
No. Scraping runs inside your Docker container. AI calls go directly from your browser to your chosen provider. Nothing passes through any StratIQ infrastructure.

**Is StratIQ free?**
Yes. StratIQ is free and open source. You pay only for your own AI API usage — typically a few cents per full analysis.

**We already have a corporate strategy document — how does that help?**
If you have a written organisational strategy, use it as your primary input. StratIQ's scan gives a starting point by inferring strategy from public signals — your real internal strategy will always be richer. The best use in that case is alignment validation: does your IT and cybersecurity roadmap actually support where the business says it's going?

**What if a scan returns limited signals?**
StratIQ flags inaccessible pages and generates from whatever signals were collected. You can add context manually in the Internal Context Interview and Organisational Context sections before generating.

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

<br/>

## Strategic Framework & Attribution

StratIQ's strategy generation methodology is inspired by the published work of **[Dr. Muhammad Malik](https://www.linkedin.com/in/dr-muhammad-malik-45940a/)**.

> *"Clarity Over Controls: The One-Page Cybersecurity Strategy Every CISO Needs"*
>
> *"Learning Cybersecurity Strategy From Zero — A Guide for New and Seasoned Leaders"*
>
> *"Securing What Matters: Why Cyber Strategy Must Start with Business Truths"*

**Core principles applied throughout:** Clarity over controls. Direction over decoration. Business language over technical jargon. Risk in dollars, not CVSS scores. Vision as one business outcome sentence. Strategy as a loop, not a one-time plan.

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

**[Docker Hub](https://hub.docker.com/r/ambarishrh/stratiq)** &nbsp;·&nbsp; **[Report an Issue](https://github.com/ambarishrh/stratiq/issues)** &nbsp;·&nbsp; **[Dr. Muhammad Malik](https://www.linkedin.com/in/dr-muhammad-malik-45940a/)**

</div>
