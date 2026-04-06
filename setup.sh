#!/bin/bash

# AccelWealth AI - Universal Setup (Git & No-Git Support)
REPO_RAW_URL="https://raw.githubusercontent.com/Pulkitsheoran/Accel_Wealth/main"
PROJECT_DIR="accelwealth_ai"

echo -e "\033[1;34m[*] AccelWealth AI: Initializing System...\033[0m"

# --- STEP 1: DETECT MODE ---
if [ -d ".git" ]; then
    echo -e "\033[0;32m[✓] Git Repository detected. Skipping file downloads.\033[0m"
else
    echo -e "\033[1;33m[!] No repository detected. Entering Zero-Clone Mode...\033[0m"
    mkdir -p $PROJECT_DIR
    cd $PROJECT_DIR
    
    FILES=("tool.py" "scrapper.py" "analyzer.py" "indicator.py" "config.py")
    for file in "${FILES[@]}"; do
        curl -sSL "$REPO_RAW_URL/$file" -o "$file"
        echo -e "\033[0;32m    [+] Fetched $file\033[0m"
    done
fi

# --- STEP 2: ENVIRONMENT ---
if [ ! -d ".venv" ]; then
    echo -e "\033[1;34m[*] Creating isolated Arch Linux environment (.venv)...\033[0m"
    python -m venv .venv
fi

source .venv/bin/activate

# --- STEP 3: DEPENDENCIES (The 2026 Yahoo Fix) ---
echo -e "\033[1;34m[*] Installing 2026-compliant drivers...\033[0m"
./.venv/bin/pip install --upgrade pip
# curl_cffi is MANDATORY for the yfinance Engine Error fix
./.venv/bin/pip install yfinance transformers torch aiohttp rich openai curl_cffi

echo -e "\n\033[1;32m[SUCCESS] AccelWealth AI is compiled and ready.\033[0m"
echo -e "--------------------------------------------------"
echo -e "1. Ensure \033[1;33mconfig.py\033[0m has your API Key."
echo -e "2. Run: \033[1;36msource .venv/bin/activate && python tool.py\033[0m"
echo -e "--------------------------------------------------"
