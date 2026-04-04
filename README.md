🚀 AccelWealth AI

AccelWealth AI is a sophisticated financial analysis terminal that bridges the gap between Quantitative Technical Analysis and NLP-driven Sentiment. Built for the 2026 market environment, it uses asynchronous data ingestion and browser-mimicry to provide a holistic "Verdict" on any stock ticker.

    [!WARNING]

    Status: UNDER ACTIVE DEVELOPMENT > This project is currently in a pre-alpha state. Features are being added rapidly. Real-time data fetching is optimized to bypass modern API restrictions using curl_cffi.

🧠 Core Features

    Global Macro Awareness: Asynchronously scans for Geopolitical Risk, Monetary Policy, and Energy shocks to provide context beyond simple price action.

    Weighted Sentiment (FinBERT): Uses a local ProsusAI/finbert model. Macro-economic news is weighted 2.5x heavier than ticker-specific news to capture systemic market risks.

    Real-Time Confluence: Integrates yfinance fast_info for absolute live pricing with classic indicators like RSI, MACD, and Bollinger Bands.

    Stealth Initialization: Optimized for CLI use with suppressed library logs and a clean, "Rich" terminal interface.

🛠️ Tech Stack

    Language: Python 3.10+ (Arch Linux Optimized)

    ML Engine: transformers (FinBERT), torch

    Data Ingestion: yfinance, aiohttp, curl_cffi (for TLS fingerprinting)

    Interface: Rich (Terminal formatting, tables, and spinners)

    LLM Integration: OpenAI / OpenRouter API

📥 Quick Start

You can get AccelWealth AI running in under 60 seconds using either method below.
Option A: The "Zero-Clone" (No Git Required)

Best for testing. This one-liner downloads the core files and builds the environment for you:
Bash

curl -sSL https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO_NAME/main/setup.sh | bash

Option B: The "Developer" (Git Clone)

Best if you want to explore or modify the code:
Bash

# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

# 2. Run the Universal Setup
chmod +x setup.sh && ./setup.sh

# 3. Activate the Environment and Launch
source .venv/bin/activate
python tool.py

⚙️ Configuration

Before launching, ensure your config.py is updated with your API keys:
Python

class Config:
    OPENROUTER_API_KEY = "your_key_here"
    BASE_URL = "https://openrouter.ai/api/v1"
    FREE_MODELS = ["google/gemini-2.0-flash-exp:free"]

📂 Project Structure

    tool.py: The main CLI entry point and UI controller.

    scrapper.py: Async engine for fetching ticker and macro news.

    analyzer.py: Stealth NLP engine for weighted sentiment analysis.

    indicator.py: Mathematical logic for technical indicators (RSI, MACD, etc.).

    setup.sh: The universal bootstrapper for environment and dependency management.

⚠️ Disclaimer

Not Financial Advice. AccelWealth AI is an experimental tool for research and educational purposes. Trading securities involves a high degree of risk. Always perform your own due diligence (DD) before making any investment.
