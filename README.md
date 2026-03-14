<div align="center">

<img src="https://img.shields.io/badge/StratIQ-Intelligence%20Platform-006ECC?style=for-the-badge&logoColor=white" alt="StratIQ" height="36"/>

# StratIQ
### AI-Powered IT & Cybersecurity Strategy Intelligence Platform

**Enter a URL. Walk into the boardroom with a complete strategy.**

*Built for CISOs, CIOs, and those who wear both hats.*

<br/>

[![Docker Pulls](https://img.shields.io/docker/pulls/ambarishrh/stratiq?style=flat-square&logo=docker&logoColor=white&color=2496ED&label=Docker%20Pulls)](https://hub.docker.com/r/ambarishrh/stratiq)
[![Version](https://img.shields.io/badge/Version-2.5.0-006ECC?style=flat-square)](https://github.com/ambarishrh/stratiq/releases)
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

StratIQ works by scraping your company's public presence — homepage, about page, news, and leadership — to understand your organisation's vision, mission, goals, and growth trajectory. It uses this as the foundation to build an IT and cybersecurity strategy that is grounded in where the business is actually going, not generic boilerplate.

> **If your organisation already has a written corporate strategy, that should be your starting point.** StratIQ is a starting-point generator — it gives you something credible, structured, and board-ready to build from, not a replacement for deep internal strategy work. Think of it as the first 80% that would otherwise take weeks and cost tens of thousands.

**StratIQ democratises what was previously only available to enterprises with large budgets.**

<br/>

## What It Produces

| Output | Description |
|--------|-------------|
| 🎯 **Executive Dashboard** | Maturity scores, risk domains, framework alignment, strategic pillars |
| 🗺️ **Strategic Roadmap** | 3-year phased initiative plan with budgets, priorities, and business cases |
| 📄 **Formal Strategy Document** | ISO-structured, audit-ready document with document control and signature block |

All outputs are **audience-aware** — language, depth, and framing adapt based on who the document is for.

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
| **OpenRouter** ⭐ | Most users — broadest model support | ~$0.01–0.05 | [openrouter.ai/keys](https://openrouter.ai/keys) |
| **Anthropic Claude** | Highest quality output | ~$0.05–0.15 | [console.anthropic.com](https://console.anthropic.com/settings/keys) |
| **OpenAI GPT-4o** | OpenAI ecosystem | ~$0.05–0.10 | [platform.openai.com](https://platform.openai.com/api-keys) |
| **Google Gemini** | Google ecosystem | ~$0.01–0.05 | [aistudio.google.com](https://aistudio.google.com/app/apikey) |

Your API key is stored only in your browser's localStorage — never transmitted to StratIQ.

<br/>

## Global Framework Intelligence

StratIQ recommends applicable frameworks based on your company's geography, sector, and regulatory signals — not a generic default list. 25 frameworks across all major regions:

| Region | Frameworks |
|--------|-----------|
| 🇦🇪 UAE / GCC | NCA ECC, ADHICS, UAE PDPL, SAMA CSF, NCA CSCC |
| 🇪🇺 European Union | GDPR, NIS2, DORA |
| 🇬🇧 United Kingdom | UK GDPR, NCSC CAF |
| 🇺🇸 United States | NIST CSF 2.0, NIST 800-53, HIPAA, PCI-DSS, CCPA, CMMC |
| 🇦🇺 Australia | ASD Essential 8, APRA CPS 234 |
| 🇸🇬 Singapore | MAS TRM, PDPA |
| 🇮🇳 India | DPDP Act, RBI Cybersecurity |
| 🌐 Global | ISO 27001, ISO 22301, ITIL 4 |

Frameworks are presented in three tiers: 🔴 **Mandatory** (pre-selected) · 🔵 **Recommended** (pre-selected) · ⚪ **Also Consider** (user opts in)

<br/>

## Audience-Aware Generation

| Audience | Language Style | Auto-selects |
|----------|---------------|--------------|
| **CISO** | Security maturity, controls, compliance deadlines | Dashboard + Document |
| **CIO** | IT governance, digital transformation, service management | Roadmap + Document |
| **CISO + CIO** | Both lenses, unified strategy | All three outputs |
| **Board** | Zero jargon, risk in dollars, concise executive brief | Dashboard only |

<br/>

## Privacy & Security

| What | Where it happens |
|------|-----------------|
| Company URL scraping | Your Docker container → public internet |
| AI generation | Your browser → your AI provider (direct, no proxy) |
| Session history | Your machine only — SQLite in a local Docker volume |
| Your API key | Browser localStorage only — never transmitted |
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

## FAQ

**Does my company data leave my machine?**
No. Scraping runs inside your Docker container. AI calls go directly from your browser to your chosen provider. Nothing passes through any StratIQ infrastructure.

**Is StratIQ free?**
Yes. StratIQ is free and open source. You pay only for your own AI API usage — typically a few cents per full analysis.

**What if a scan returns limited signals?**
StratIQ flags inaccessible pages and generates from whatever signals were collected. You can add context manually in the Organisational Context section before generating.

**How do I update my API key?**
Click the "Forget" link next to your saved key on the API screen, then enter the new one.

**Can I use this for client work?**
StratIQ is licensed CC BY-NC-SA 4.0 — free for non-commercial use with attribution. Contact us for commercial licensing.

**We already have a corporate strategy document — how does that help?**
If you have a written organisational strategy, use it as your primary input. StratIQ's scan gives you a starting point by inferring strategy from public signals — your real internal strategy will always be richer. The best use of StratIQ in that case is to validate alignment: does your IT and cybersecurity roadmap actually support where the business says it's going?

**How do I completely remove StratIQ?**
```bash
docker stop stratiq && docker rm stratiq
docker volume rm stratiq_data
docker rmi ambarishrh/stratiq:latest
```

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

## Strategic Framework & Attribution

StratIQ's strategy generation methodology is inspired by the published work of **[Dr. Muhammad Malik](https://www.linkedin.com/in/dr-muhammad-malik-45940a/)**.

> *"Clarity Over Controls: The One-Page Cybersecurity Strategy Every CISO Needs"*
>
> *"Learning Cybersecurity Strategy From Zero — A Guide for New and Seasoned Leaders"*
>
> *"Securing What Matters: Why Cyber Strategy Must Start with Business Truths"*

**Core principles:** Clarity over controls. Direction over decoration. Business language over technical jargon. Risk in dollars, not CVSS scores.

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
