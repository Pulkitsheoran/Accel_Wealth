import asyncio
import yfinance as yf
import requests
from datetime import datetime
from typing import List, Dict


class DataIngestionLayer:
    def __init__(self):
        # 1. BRAINS: The Macro Pillars for global context
        self.macro_pillars = {
            "GEOPOLITICS": "global conflict war geopolitical risk stability",
            "MONETARY": "federal reserve interest rates inflation CPI central bank",
            "ENERGY": "oil prices gas energy supply disruption commodities",
            "MACRO": "global economy recession gdp growth market outlook",
        }

        # 2. SESSION: Pretend to be a real browser to avoid being blocked
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (X11; Arch Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            }
        )

    async def _fetch_pillar(self, query: str, p_type: str) -> List[Dict]:
        """Asynchronous worker using yfinance's internal optimized session."""
        try:
            # Keep the jitter sleep; it's good practice for Arch/high-speed tasks
            await asyncio.sleep(0.1)

            loop = asyncio.get_event_loop()

            # REMOVED: session=self.session
            # yfinance will now use its own internal curl_cffi session automatically
            search = await loop.run_in_executor(
                None, lambda: yf.Search(query, max_results=6)
            )

            if not search or not search.news:
                return []

            return [
                {
                    "headline": n.get("title", "No Title"),
                    "type": p_type,
                    "source": n.get("publisher", "Unknown"),
                    "time": datetime.fromtimestamp(
                        n.get("providerPublishTime", 0)
                    ).strftime("%H:%M"),
                }
                for n in search.news
            ]
        except Exception:
            # Silently fail for the individual pillar so the whole scan doesn't crash
            return []

    async def scrape_comprehensive(self, ticker: str) -> List[Dict]:
        """Parallel fetch of Ticker + Global context."""
        # Start with the specific ticker
        tasks = [self._fetch_pillar(ticker, "TICKER")]

        # Fire off all macro pillars simultaneously
        for name, query in self.macro_pillars.items():
            tasks.append(self._fetch_pillar(query, name))

        results = await asyncio.gather(*tasks)

        # Flatten the list of lists
        return [item for sublist in results for item in sublist]


# Helper for tool.py
def get_global_news(ticker: str) -> List[Dict]:
    # We create a new instance each time or reuse a global one
    # Reusing a global instance is better for session persistence
    scraper = DataIngestionLayer()
    return asyncio.run(scraper.scrape_comprehensive(ticker))
