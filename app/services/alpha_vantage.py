import httpx
from typing import Optional
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import get_settings


class AlphaVantageService:
    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self):
        self.settings = get_settings()
        self.api_key = self.settings.alpha_vantage_api_key

    def _make_request(self, params: dict) -> dict:
        params["apikey"] = self.api_key
        with httpx.Client(timeout=30.0) as client:
            response = client.get(self.BASE_URL, params=params)
            response.raise_for_status()
            return response.json()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def get_stock_quote(self, symbol: str) -> Optional[dict]:
        """Get real-time stock quote for a symbol."""
        try:
            params = {"function": "GLOBAL_QUOTE", "symbol": symbol}
            data = self._make_request(params)

            if "Global Quote" in data and data["Global Quote"]:
                quote = data["Global Quote"]
                return {
                    "symbol": quote.get("01. symbol"),
                    "price": float(quote.get("05. price", 0)),
                    "change": float(quote.get("09. change", 0)),
                    "change_percent": quote.get("10. change percent", "0%"),
                    "volume": int(quote.get("06. volume", 0)),
                    "latest_trading_day": quote.get("07. latest trading day"),
                }
            return None
        except Exception as e:
            print(f"Error fetching quote for {symbol}: {e}")
            return None

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def get_daily_prices(self, symbol: str, outputsize: str = "compact") -> Optional[dict]:
        """Get daily price history. outputsize: 'compact' (100 days) or 'full' (20+ years)."""
        try:
            params = {
                "function": "TIME_SERIES_DAILY",
                "symbol": symbol,
                "outputsize": outputsize,
            }
            data = self._make_request(params)

            if "Time Series (Daily)" in data:
                time_series = data["Time Series (Daily)"]
                prices = []
                for date, values in list(time_series.items())[:30]:
                    prices.append({
                        "date": date,
                        "open": float(values["1. open"]),
                        "high": float(values["2. high"]),
                        "low": float(values["3. low"]),
                        "close": float(values["4. close"]),
                        "volume": int(values["5. volume"]),
                    })
                return {"symbol": symbol, "prices": prices}
            return None
        except Exception as e:
            print(f"Error fetching daily prices for {symbol}: {e}")
            return None

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def get_company_overview(self, symbol: str) -> Optional[dict]:
        """Get fundamental company data."""
        try:
            params = {"function": "OVERVIEW", "symbol": symbol}
            data = self._make_request(params)

            if data and "Symbol" in data:
                return {
                    "symbol": data.get("Symbol"),
                    "name": data.get("Name"),
                    "description": data.get("Description"),
                    "sector": data.get("Sector"),
                    "industry": data.get("Industry"),
                    "market_cap": data.get("MarketCapitalization"),
                    "pe_ratio": data.get("PERatio"),
                    "dividend_yield": data.get("DividendYield"),
                    "52_week_high": data.get("52WeekHigh"),
                    "52_week_low": data.get("52WeekLow"),
                }
            return None
        except Exception as e:
            print(f"Error fetching overview for {symbol}: {e}")
            return None

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def get_news_sentiment(self, tickers: str = None, topics: str = "financial_markets") -> Optional[list]:
        """Get news and sentiment data. tickers: comma-separated symbols, topics: financial_markets, economy, etc."""
        try:
            params = {"function": "NEWS_SENTIMENT", "topics": topics}
            if tickers:
                params["tickers"] = tickers
            params["limit"] = 10

            data = self._make_request(params)

            if "feed" in data:
                news_items = []
                for item in data["feed"][:5]:
                    news_items.append({
                        "title": item.get("title"),
                        "summary": item.get("summary"),
                        "source": item.get("source"),
                        "url": item.get("url"),
                        "sentiment_score": item.get("overall_sentiment_score"),
                        "sentiment_label": item.get("overall_sentiment_label"),
                        "published": item.get("time_published"),
                    })
                return news_items
            return None
        except Exception as e:
            print(f"Error fetching news sentiment: {e}")
            return None

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def get_technical_indicator(
        self, symbol: str, indicator: str = "RSI", interval: str = "daily", time_period: int = 14
    ) -> Optional[dict]:
        """Get technical indicator (RSI, SMA, EMA, MACD, etc.)."""
        try:
            params = {
                "function": indicator,
                "symbol": symbol,
                "interval": interval,
                "time_period": time_period,
                "series_type": "close",
            }
            data = self._make_request(params)

            key = f"Technical Analysis: {indicator}"
            if key in data:
                values = list(data[key].items())[:10]
                return {
                    "symbol": symbol,
                    "indicator": indicator,
                    "values": [{"date": d, "value": float(v[indicator])} for d, v in values],
                }
            return None
        except Exception as e:
            print(f"Error fetching {indicator} for {symbol}: {e}")
            return None

    def format_market_context(self, symbol: str) -> str:
        """Get formatted market context for a symbol to use in prompts."""
        context_parts = []

        quote = self.get_stock_quote(symbol)
        if quote:
            context_parts.append(
                f"Current Price: ${quote['price']:.2f} ({quote['change_percent']} change)"
            )

        overview = self.get_company_overview(symbol)
        if overview:
            context_parts.append(f"Company: {overview['name']} ({overview['sector']})")
            if overview.get('pe_ratio'):
                context_parts.append(f"P/E Ratio: {overview['pe_ratio']}")
            if overview.get('dividend_yield'):
                context_parts.append(f"Dividend Yield: {overview['dividend_yield']}%")

        rsi = self.get_technical_indicator(symbol, "RSI")
        if rsi and rsi["values"]:
            latest_rsi = rsi["values"][0]["value"]
            context_parts.append(f"RSI (14): {latest_rsi:.2f}")

        if context_parts:
            return f"Market data for {symbol}:\n" + "\n".join(context_parts)
        return f"Unable to fetch market data for {symbol}"
