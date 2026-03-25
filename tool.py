#!/usr/bin/env python
import sys
from typing import List, Optional
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from config import Config

try:
    from scrapper import DataIngestionLayer
    from analyzer import SentimentAnalyzer
except ImportError:
    print("Error: scrapper.py or analyzer.py not found.")
    sys.exit(1)

Config.validate()
client = OpenAI(base_url=Config.BASE_URL, api_key=Config.OPENROUTER_API_KEY)
console = Console()

history: List[ChatCompletionMessageParam] = [
    {
        "role": "system",
        "content": "You are AccelWealth AI. Be professional and conversational. "
        "If stock sentiment data is provided, explain it clearly.",
    }
]


def chat_with_llm(message: str) -> str:
    global history
    history.append({"role": "user", "content": message})

    for model_id in Config.FREE_MODELS:
        try:
            # Inform the user which model is being tried (optional)
            # console.print(f"[dim]Trying {model_id}...[/dim]")

            response = client.chat.completions.create(
                model=model_id,
                messages=history,
                timeout=30,  # Increased for 120B models
            )

            answer = response.choices[0].message.content
            if answer:
                history.append({"role": "assistant", "content": answer})
                return answer

        except Exception as e:
            # Move to next model if 400 (Invalid), 408 (Timeout), or 429 (Rate Limit)
            error_str = str(e)
            if any(code in error_str for code in ["400", "408", "429"]):
                continue
            return f"Critical API Error: {e}"

    return "⚠️ [bold red]All models busy.[/bold red] Please try again in 30 seconds."


def run_app():
    console.print(Panel("[bold cyan]ACCEL_WEALTH AI INTERFACE[/bold cyan]"))

    try:
        with console.status("[yellow]Waking up local AI engines...", spinner="dots"):
            scraper = DataIngestionLayer()
            analyzer = SentimentAnalyzer()
    except Exception as e:
        console.print(f"[bold red]Failed to start engines:[/bold red] {e}")
        return

    while True:
        try:
            user_msg = console.input("\n[bold green]You > [/bold green]").strip()

            if user_msg.lower() in ["exit", "quit"]:
                break
            if not user_msg:
                continue

            # --- SMARTER TICKER EXTRACTION ---
            # Finds 'AAPL' even in "Tell me about AAPL stock"
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
                with console.status(
                    f"[blue]Fetching and Analyzing {ticker}...", spinner="dots"
                ):
                    try:
                        data = scraper.scrape_news(ticker)
                        if data:
                            analyzer.analyze_headlines(
                                [item["headline"] for item in data]
                            )
                            vibe = analyzer.final_vibe
                            context = f"Internal analysis for {ticker}: Sentiment Vibe is {vibe:.2f}."
                            bot_reply = chat_with_llm(
                                f"User asked: '{user_msg}'. {context}"
                            )
                        else:
                            bot_reply = chat_with_llm(user_msg)
                    except Exception as e:
                        console.print(f"[dim red]Local Analysis Failed: {e}[/dim red]")
                        bot_reply = chat_with_llm(user_msg)
            else:
                bot_reply = chat_with_llm(user_msg)

            console.print(Markdown(f"**AccelWealth:** {bot_reply}"))

        except KeyboardInterrupt:
            console.print("\n[yellow]Session ended by user.[/yellow]")
            break
        except Exception as e:
            console.print(f"[bold red]Loop Error:[/bold red] {e}")


if __name__ == "__main__":
    run_app()

