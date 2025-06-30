import yfinance as yf
from app.models.stock_models import StockInfo
from typing import Optional
from functools import lru_cache

# Simple in-memory cache for demonstration (can be replaced with Redis, etc.)
@lru_cache(maxsize=32)
def fetch_stock_data(symbol: str) -> Optional[StockInfo]:
    """Fetch stock data from yfinance with caching"""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        if not info or 'regularMarketPrice' not in info:
            return None
        return StockInfo(
            symbol=symbol,
            name=info.get('shortName', symbol),
            price=info['regularMarketPrice'],
            currency=info.get('currency', 'INR'),
            exchange=info.get('exchange', 'NSE'),
            change=info.get('regularMarketChange', 0.0),
            percent_change=info.get('regularMarketChangePercent', 0.0)
        )
    except Exception as e:
        # Log error in production
        print(f"Error fetching stock data: {e}")
        return None

# Example test function
def test_fetch_indian_stocks():
    """Test function for Indian stocks"""
    for symbol in ["RELIANCE.NS", "TCS.NS", "INFY.NS"]:
        stock = fetch_stock_data(symbol)
        if stock:
            print(stock)
        else:
            print(f"Failed to fetch data for {symbol}")

if __name__ == "__main__":
    test_fetch_indian_stocks()
