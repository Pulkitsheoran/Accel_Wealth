💹 AccelWealth AI
The Next-Gen Quant-Sentiment Terminal for 2026 Markets

AccelWealth AI is a high-performance financial intelligence engine. It doesn't just track prices; it synthesizes Global Macro Context and FinBERT Sentiment Analysis into a single, actionable "Technical Confluence" report.

Built with an asynchronous backbone, it is designed to bypass modern API restrictions while delivering institutional-grade insights to your terminal.
⚡ Key Capabilities

    🌐 Macro-Weighted Intelligence: Scans geopolitical, monetary, and energy pillars. Macro news is weighted 2.5x heavier than ticker news to detect systemic shifts before they hit the price.

    🤖 Neural Sentiment Engine: Leverages ProsusAI/finbert to decode the "vibe" of global headlines with high precision.

    📊 Real-Time Confluence: Fuses fast_info live pricing with RSI, MACD, and Bollinger Band calculations.

    🛡️ Stealth Networking: Utilizes curl_cffi for advanced TLS fingerprinting, ensuring uninterrupted data flow from Yahoo Finance in the 2026 security environment.

🚀 Installation & Deployment

Choose the path that fits your setup. Both methods automatically configure the environment and solve the curl_cffi dependency.
Method 1: The Quick-Start (No Clone)

Ideal for a quick test. This script builds the entire directory structure and environment in one go:
Bash

curl -sSL https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO_NAME/main/setup.sh | bash

Method 2: The Developer Flow (Git)

Use this if you plan to modify the logic or contribute to the engine:
Bash

# Clone the core
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

# Initialize Environment
chmod +x setup.sh && ./setup.sh

# Launch the Terminal
source .venv/bin/activate
python tool.py

🛠️ Technical Architecture
Component	Responsibility	Tech Stack
Ingestion	Multi-pillar Async Scraping	aiohttp, yfinance
Analysis	Weighted NLP Sentiment	FinBERT, PyTorch
Quant	Technical Indicator Math	NumPy, Pandas
UI	Interactive CLI Interface	Rich, Markdown
⚙️ Configuration

Before firing up the engine, update your config.py with your credentials:
Python

class Config:
    OPENROUTER_API_KEY = "your_api_key_here"
    BASE_URL = "https://openrouter.ai/api/v1"
    # Select your preferred AI model
    PRIMARY_MODEL = "google/gemini-2.0-flash-exp:free"

    [!IMPORTANT]
    Financial Disclaimer: AccelWealth AI is an experimental research tool. It is not financial advice. Trading securities involves significant risk. Always verify data through official brokerage channels.
