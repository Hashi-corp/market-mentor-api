import yfinance as yf
from app.models.stock_models import StockInfo
from typing import Optional
from functools import lru_cache
from datetime import datetime, timedelta
import time

# Cache with shorter TTL for real-time data
@lru_cache(maxsize=100)
def fetch_stock_data(symbol: str) -> Optional[StockInfo]:
    """Fetch comprehensive real-time stock data from yfinance"""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        # Get recent data for real-time price
        hist = ticker.history(period="1d", interval="1m")
        current_price = float(hist['Close'].iloc[-1]) if not hist.empty else info.get('regularMarketPrice', 0.0)
        
        if not info:
            return None
            
        return StockInfo(
            symbol=symbol,
            name=info.get('shortName') or info.get('longName', symbol),
            price=current_price,
            currency=info.get('currency', 'INR'),
            exchange=info.get('exchange', 'NSE'),
            change=info.get('regularMarketChange', 0.0),
            percent_change=info.get('regularMarketChangePercent', 0.0),
            
            # Market data
            market_cap=info.get('marketCap'),
            volume=info.get('volume'),
            avg_volume=info.get('averageVolume'),
            
            # Price ranges
            day_high=info.get('dayHigh'),
            day_low=info.get('dayLow'),
            week_52_high=info.get('fiftyTwoWeekHigh'),
            week_52_low=info.get('fiftyTwoWeekLow'),
            
            # Financial metrics
            pe_ratio=info.get('trailingPE'),
            eps=info.get('trailingEps'),
            dividend_yield=info.get('dividendYield'),
            book_value=info.get('bookValue'),
            
            # Market status
            market_state=info.get('marketState', 'REGULAR'),
            last_updated=datetime.now(),
            
            # Additional info
            sector=info.get('sector'),
            industry=info.get('industry')
        )
    except Exception as e:
        print(f"Error fetching stock data for {symbol}: {e}")
        return None

def get_real_time_price(symbol: str) -> Optional[float]:
    """Get real-time price with minimal latency"""
    try:
        ticker = yf.Ticker(symbol)
        # Get the most recent price
        hist = ticker.history(period="1d", interval="1m")
        if not hist.empty:
            return float(hist['Close'].iloc[-1])
        
        # Fallback to regular market price
        info = ticker.info
        return info.get('regularMarketPrice')
    except Exception as e:
        print(f"Error fetching real-time price for {symbol}: {e}")
        return None

def get_market_status(symbol: str) -> str:
    """Get current market status"""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return info.get('marketState', 'UNKNOWN')
    except:
        return 'UNKNOWN'

def clear_stock_cache():
    """Clear the stock data cache to ensure fresh data"""
    fetch_stock_data.cache_clear()

# Enhanced test function
def test_fetch_indian_stocks():
    """Test function for comprehensive Indian stock data"""
    test_symbols = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ITC.NS"]
    
    for symbol in test_symbols:
        print(f"\n--- Testing {symbol} ---")
        stock = fetch_stock_data(symbol)
        
        if stock:
            print(f"Name: {stock.name}")
            print(f"Price: {stock.currency} {stock.price}")
            print(f"Change: {stock.change} ({stock.percent_change}%)")
            print(f"Market Cap: {stock.market_cap}")
            print(f"Volume: {stock.volume}")
            print(f"Day Range: {stock.day_low} - {stock.day_high}")
            print(f"52W Range: {stock.week_52_low} - {stock.week_52_high}")
            print(f"P/E: {stock.pe_ratio}")
            print(f"Sector: {stock.sector}")
            print(f"Market State: {stock.market_state}")
            print(f"Last Updated: {stock.last_updated}")
        else:
            print(f"Failed to fetch data for {symbol}")
        
        time.sleep(1)  # Rate limiting

if __name__ == "__main__":
    test_fetch_indian_stocks()
