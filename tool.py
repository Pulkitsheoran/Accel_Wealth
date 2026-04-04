#!/usr/bin/env python
import sys
import os
import asyncio
import readline
import atexit
import yfinance as yf
from typing import List, Dict
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table

from config import Config
from indicator import TechnicalIndicators
import requests

try:
    from scrapper import DataIngestionLayer
    from analyzer import SentimentAnalyzer
except ImportError:
    print("Error: scrapper.py or analyzer.py not found.")
    sys.exit(1)

# --- SETUP & HISTORY ---
Config.validate()
client = OpenAI(base_url=Config.BASE_URL, api_key=Config.OPENROUTER_API_KEY)
console = Console()

histfile = os.path.join(os.path.expanduser("~"), ".accelwealth_history")
try:
    readline.read_history_file(histfile)
    readline.set_history_length(1000)
except FileNotFoundError:
    pass
atexit.register(readline.write_history_file, histfile)

history: List[ChatCompletionMessageParam] = [
    {
        "role": "system",
        "content": (
            "You are AccelWealth AI, a sophisticated financial analyst. "
            "You combine NLP sentiment with quantitative technical indicators. "
            "Provide a synthesized 'Verdict' based on both data types. "
            " Provide the verdit in a simple straight forward way and in points for easier understanding but do not remove the neccessary data an information."
            "When using technical terms, provide the full name followed by its abbreviation in parenthesis. "
            "Always include a disclaimer about financial risk at the end. "
            "Ask the user at the end if they would like to know what any specific terms mean."
            " also when you provide the nlp synthesis there is not need to mention that just mention sentimental analysis"
        ),
    }
]

# --- CORE FUNCTIONS ---


def chat_with_llm(message: str) -> str:
    global history
    history.append({"role": "user", "content": message})
    for model_id in Config.FREE_MODELS:
        try:
            response = client.chat.completions.create(
                model=model_id,
                messages=history,
                timeout=30,
            )
            answer = response.choices[0].message.content
            if answer:
                history.append({"role": "assistant", "content": answer})
                return answer
        except Exception as e:
            if any(code in str(e) for code in ["400", "408", "429"]):
                continue
            return f"Critical API Error: {e}"
    return "⚠️ [bold red]All models busy.[/bold red] Please try again."


def display_summary_table(
    ticker: str, price: float, rsi: float, vibe: float, news_count: int
):
    """Displays a clean summary of the fetched data."""
    table = Table(title=f"Market Intelligence: {ticker}", title_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", justify="right")
    table.add_column("Status", justify="center")

    rsi_status = (
        "[red]Overbought[/red]"
        if rsi > 65
        else "[green]Oversold[/green]"
        if rsi < 35
        else "Neutral"
    )
    vibe_status = (
        "[green]Bullish[/green]"
        if vibe > 0.3
        else "[red]Bearish[/red]"
        if vibe < -0.3
        else "Neutral"
    )

    table.add_row("Price", f"${price:.2f}", "LIVE")
    table.add_row("Relative Strength Index (RSI)", f"{rsi:.2f}", rsi_status)
    table.add_row("Sentiment Vibe", f"{vibe:.2f}", vibe_status)
    table.add_row("News Contexts", str(news_count), "Aggregated")

    console.print(table)


session = requests.Session()
session.headers.update(
    {
        "User-Agent": "Mozilla/5.0 (X11; Arch Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
)


def run_app():
    console.print(
        Panel("[bold cyan]ACCEL_WEALTH AI: QUANT-SENTIMENT ENGINE[/bold cyan]")
    )

    with console.status("[yellow]Waking up local AI engines...", spinner="dots"):
        scraper = DataIngestionLayer()
        analyzer = SentimentAnalyzer()

    while True:
        try:
            user_msg = console.input("\n[bold green]You > [/bold green]").strip()
            if user_msg.lower() in ["exit", "quit"]:
                break
            if not user_msg:
                continue

            # Ticker Extraction
            words = user_msg.replace(",", "").replace(".", "").replace("?", "").split()
            ticker = next(
                (
                    w.strip("$").upper()
                    for w in words
                    if (w.isupper() and 1 <= len(w) <= 5) or w.startswith("$")
                ),
                None,
            )

            if ticker:
                # 1. ADDED 'as status' HERE (This was your missing link)
                with console.status(
                    f"[blue]Global Intelligence Scan: {ticker}...", spinner="dots"
                ) as status:
                    curr_price = 0.0  # Pre-initialize to prevent crash on error
                    try:
                        # PHASE 1: NEWS
                        all_news = asyncio.run(scraper.scrape_comprehensive(ticker))

                        # 2. Update now works because 'status' is defined
                        status.update(
                            f"[magenta]Fetching LIVE + Historical data for {ticker}..."
                        )

                        # PHASE 2: REAL-TIME DATA
                        stock = yf.Ticker(ticker)
                        live_price = stock.fast_info["last_price"]
                        hist = stock.history(period="3mo")
                        intraday = stock.history(period="1d", interval="1m")

                        # Fallback for empty data
                        if hist.empty:
                            status.update(
                                "[yellow]Primary data empty, trying fallback..."
                            )
                            hist = stock.history(period="1mo")

                        if hist.empty or intraday.empty:
                            bot_reply = f"I'm sorry, I couldn't retrieve market data for {ticker}."
                        else:
                            # PHASE 3: ANALYSIS
                            status.update(
                                f"[cyan]Executing AI Sentiment & Technical Analysis..."
                            )

                            closes = hist["Close"]
                            rsi = TechnicalIndicators.calculate_rsi(closes)
                            macd, macd_sig = TechnicalIndicators.calculate_macd(closes)
                            upper, mid, lower = (
                                TechnicalIndicators.calculate_bollinger_bands(closes)
                            )

                            curr_price = live_price
                            vibe = analyzer.analyze_comprehensive(all_news)

                            # UI: Show the data table
                            display_summary_table(
                                ticker, curr_price, rsi, vibe, len(all_news)
                            )

                            # 5. Build AI Context
                            tech_report = (
                                f"REAL-TIME CONFLUENCE FOR {ticker}:\n"
                                f"- Price: ${curr_price:.2f}\n"
                                f"- Relative Strength Index (RSI): {rsi:.2f}\n"
                                f"- INTRADAY TREND: {'UP' if live_price > intraday['Close'].iloc[0] else 'DOWN'} since market open\n"
                                f"- Moving Average Convergence Divergence (MACD): {macd:.4f} (Signal: {macd_sig:.4f})\n"
                                f"- Bollinger Bands: Upper ${upper:.2f}, Lower ${lower:.2f}\n"
                                f"- Global Sentiment Vibe: {vibe:.2f} (Weighted Macro + Ticker)\n"
                                f"- Latest Macro Context: {[n['headline'] for n in all_news if n['type'] != 'TICKER'][:3]}"
                            )

                            bot_reply = chat_with_llm(
                                f"Analyze this confluence for {ticker}: {tech_report}\nUser: {user_msg}"
                            )

                    except Exception as e:
                        console.print(f"[dim red]Engine Error: {e}[/dim red]")
                        bot_reply = chat_with_llm(user_msg)
            else:
                bot_reply = chat_with_llm(user_msg)

            console.print(Markdown(f"**AccelWealth:** {bot_reply}"))
        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[bold red]Loop Error:[/bold red] {e}")


if __name__ == "__main__":
    run_app()
