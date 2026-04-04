<div align="center">

<img src="https://img.shields.io/badge/version-1.0.0-0a0a0a?style=flat-square&labelColor=0a0a0a&color=00ff88" alt="version"/>
<img src="https://img.shields.io/badge/python-3.10%2B-0a0a0a?style=flat-square&labelColor=0a0a0a&color=00ff88" alt="python"/>
<img src="https://img.shields.io/badge/license-MIT-0a0a0a?style=flat-square&labelColor=0a0a0a&color=00ff88" alt="license"/>
<img src="https://img.shields.io/badge/status-experimental-0a0a0a?style=flat-square&labelColor=0a0a0a&color=ffaa00" alt="status"/>

<br/>
<br/>

```
  ___               _  _    _   _                 _   _     _     _
 / _ \   __ _  ___ | || |  | | | |   ___  __ _  | | | |_  | |_  | |
| |_| | / _ˋ ||  _||  _  | | | | |  / _ \/ _ˋ | | | |  _| |  _| | . \
|_| |_||___|_||___||_| |_| |_|_|_| |___/\__/_| |_|  \__|  \__| |_||_|
                    A I   T E R M I N A L   2 0 2 6
```

# AccelWealth AI

**Quant-Sentiment Intelligence for Modern Markets**

*Fusing global macro context, FinBERT NLP, and real-time technicals into a single actionable signal.*

<br/>

[Get Started](#-installation) · [Architecture](#-architecture) · [Configuration](#-configuration) · [Disclaimer](#-disclaimer)

---

</div>

## Overview

AccelWealth AI is a research-grade financial intelligence terminal that goes beyond raw price data. It synthesizes **three analytical pillars** — geopolitical macro context, neural sentiment analysis, and quantitative technical indicators — into a unified "Technical Confluence" report designed for informed decision-making.

This is not a trading bot. It is a structured research assistant built for analysts who want signal, not noise.

<br/>

## Features

| Capability | Description |
|---|---|
| **Macro Intelligence** | Scans geopolitical, monetary policy, and energy market pillars for weighted context signals |
| **Neural Sentiment** | Runs `ProsusAI/finbert` over global financial headlines to decode institutional tone |
| **Technical Confluence** | Merges live pricing data with RSI, MACD, and Bollinger Bands into one coherent view |
| **Async Ingestion** | Non-blocking multi-source scraping via `aiohttp` for low-latency data pipelines |
| **Stealth Networking** | Advanced TLS fingerprinting via `curl_cffi` to minimize rate-limit friction |
| **Rich CLI** | Interactive terminal UI powered by `Rich` for clean, readable output |

<br/>

## Installation

### Option 1 — Quick Start

For users who want to run immediately without cloning:

```bash
curl -sSL https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/setup.sh | bash
```

> This script creates a virtual environment, installs all dependencies, and validates your configuration.

---

### Option 2 — Developer Setup

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO

# 2. Run the setup script
chmod +x setup.sh && ./setup.sh

# 3. Activate the environment and launch
source .venv/bin/activate
python tool.py
```

<br/>

## Architecture

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
| **Ingestion** | Data Collector | Multi-source async scraping & live pricing | `aiohttp`, `yfinance`, `curl_cffi` |
| **Analysis** | Sentiment Engine | FinBERT NLP over financial headlines | `ProsusAI/finbert`, `PyTorch` |
| **Quant** | Indicator Engine | RSI, MACD, Bollinger Band computation | `NumPy`, `Pandas` |
| **Output** | CLI Interface | Interactive terminal rendering | `Rich` |

<br/>

## Configuration

Edit `config.py` before first run:

```python
class Config:
    # OpenRouter API credentials
    OPENROUTER_API_KEY = "your_api_key_here"
    BASE_URL           = "https://openrouter.ai/api/v1"

    # Model selection (defaults to Gemini Flash for speed)
    PRIMARY_MODEL      = "google/gemini-2.0-flash-exp:free"
```

To obtain an API key, visit [openrouter.ai](https://openrouter.ai) and create a free account.

<br/>

## Requirements

- Python `3.10+`
- PyTorch (CPU is sufficient; GPU accelerates FinBERT inference)
- An OpenRouter API key
- Internet access for live data ingestion

Full dependency list is managed in `requirements.txt` and installed automatically by `setup.sh`.

<br/>

## Disclaimer

> **AccelWealth AI is an experimental research tool intended for educational and analytical purposes only.**
>
> Nothing produced by this software constitutes financial advice, investment recommendations, or trading signals. All outputs are the result of automated data processing and carry no guarantee of accuracy, timeliness, or fitness for any particular purpose.
>
> Trading and investing in securities involves substantial risk of loss. You are solely responsible for your own investment decisions. The authors and contributors of this project accept no liability for financial outcomes resulting from use of this software.

<br/>

## License

Distributed under the MIT License. See `LICENSE` for details.

---

<div align="center">

Built for research. Not for reckless trading.

</div>
