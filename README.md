<div align="center">

<img src="https://img.shields.io/badge/status-experimental-0a0a0a?style=flat-square&labelColor=0a0a0a&color=ffaa00" alt="status"/>

<br/>
<br/>

# AccelWealth AI

**Quant-Sentiment Intelligence for Modern Markets**

*Three signals. One report. No noise.*

<br/>

[Get Started](#installation) · [Architecture](#architecture) · [Configuration](#configuration) · [Disclaimer](#disclaimer)

---

</div>

## Overview

Markets move on information — but most terminals only show you price. AccelWealth AI is built on the premise that a price without context is just a number.

It runs three analytical layers in parallel: a macro intelligence engine that tracks geopolitical shifts, central bank posture, and energy dynamics; a FinBERT sentiment pipeline that reads and scores live financial headlines the way a trained analyst would; and a quant layer that computes RSI, MACD, and Bollinger Bands against real-time market data. Rather than presenting these as three separate outputs, AccelWealth fuses them into a single **Technical Confluence report** — a structured view of where the signals agree, and what that agreement implies.

The goal is not to predict markets. It is to give you a faster, more complete picture of what is happening in them.

> **Who this is for:** Quantitative researchers, algorithmic traders, and finance students who want a structured, programmable intelligence layer — not a black-box prediction tool.

<br/>

## Features

| Capability | What it does |
|---|---|
| **Macro Intelligence** | Monitors geopolitical developments, central bank posture, and energy market dynamics, then weights each pillar's contribution to the overall signal |
| **Neural Sentiment Engine** | Passes live financial headlines through `ProsusAI/finbert`, a model trained specifically on financial text, to extract institutional-grade sentiment scores |
| **Technical Confluence** | Computes RSI, MACD, and Bollinger Bands against live `yfinance` pricing data and identifies zones where indicators converge |
| **Async Data Ingestion** | Fetches from multiple sources concurrently via `aiohttp`, keeping pipeline latency low even when sources respond unevenly |
| **TLS Fingerprint Spoofing** | Uses `curl_cffi` to mimic browser TLS handshakes, significantly reducing the likelihood of rate-limit blocks from financial data endpoints |
| **Rich Terminal UI** | Outputs structured, colour-coded reports directly in the terminal via the `Rich` library — no browser, no external dashboard required |

<br/>

## Installation

### Option 1 — Quick Start

The fastest way to get running. Downloads, configures, and launches the environment in a single command:

```bash
curl -sSL https://raw.githubusercontent.com/Pulkitsheoran/Accel_Wealth/main/setup.sh | bash
```

> `setup.sh` creates an isolated virtual environment, installs all dependencies from `requirements.txt`, and runs a basic configuration check before exiting.

---

### Option 2 — Developer Setup

Recommended if you intend to modify the source, contribute, or inspect the pipeline before running:

```bash
# Clone the repository
git clone https://github.com/Pulkitsheoran/Accel_Wealth.git
cd Accel_Wealth

# Make the setup script executable and run it
chmod +x setup.sh && ./setup.sh

# Activate the virtual environment and start the terminal
source .venv/bin/activate
python tool.py
```

<br/>

## Architecture

The pipeline runs in three sequential stages. Data is ingested asynchronously, passed through the sentiment and quant layers in parallel, then rendered as a unified report.

```
┌─────────────────────────────────────────────────────────┐
│                    AccelWealth AI                       │
├──────────────┬──────────────┬───────────────────────────┤
│   INGESTION  │   ANALYSIS   │          OUTPUT           │
│              │              │                           │
│  aiohttp     │  FinBERT     │  Rich CLI Terminal        │
│  yfinance    │  PyTorch     │  Confluence Report        │
│  curl_cffi   │  NumPy       │  Macro Signal Summary     │
│              │  Pandas      │                           │
└──────────────┴──────────────┴───────────────────────────┘
```

| Layer | Component | Responsibility | Stack |
|---|---|---|---|
| **Ingestion** | Data Collector | Async multi-source scraping and live price feeds | `aiohttp`, `yfinance`, `curl_cffi` |
| **Sentiment** | NLP Engine | FinBERT inference over financial headlines | `ProsusAI/finbert`, `PyTorch` |
| **Quant** | Indicator Engine | RSI, MACD, and Bollinger Band computation | `NumPy`, `Pandas` |
| **Output** | CLI Renderer | Structured terminal report generation | `Rich` |

<br/>

## Configuration

Before running for the first time, open `config.py` and set your credentials:

```python
class Config:
    # Your OpenRouter API key — required for LLM-powered synthesis
    OPENROUTER_API_KEY = "your_api_key_here"
    BASE_URL           = "https://openrouter.ai/api/v1"

    # The model used for report generation
    # Gemini Flash is the default: fast, free-tier eligible, and sufficient for most use cases
    PRIMARY_MODEL      = "google/gemini-2.0-flash-exp:free"
```

OpenRouter provides a free tier that covers standard usage. Create an account at [openrouter.ai](https://openrouter.ai) to generate your key.

<br/>

## Requirements

- **Python 3.10 or later** — f-string and `match` statement compatibility required
- **PyTorch** — CPU inference works fine; a CUDA-capable GPU will meaningfully speed up FinBERT on large headline batches
- **OpenRouter API key** — used for the LLM synthesis step that produces the final confluence narrative
- **Network access** — required for live price feeds and headline ingestion

All Python dependencies are declared in `requirements.txt` and installed automatically by `setup.sh`. No manual `pip install` steps are needed.

<br/>

## Disclaimer

> **AccelWealth AI is an experimental research tool. It is not financial advice.**
>
> All output generated by this software — including sentiment scores, technical signals, macro summaries, and confluence reports — is the product of automated data processing. It carries no guarantee of accuracy, completeness, or timeliness. Past signal performance does not imply future reliability.
>
> Investing and trading in financial markets involves significant risk of capital loss. You are solely and entirely responsible for your own investment and trading decisions. The authors, contributors, and maintainers of this project bear no liability whatsoever for any financial outcomes, direct or indirect, resulting from use of this software.
>
> If you are making real capital decisions, consult a licensed financial professional.

---

<div align="center">

Built for research. Use it like one.

</div>
