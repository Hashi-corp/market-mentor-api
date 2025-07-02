from fastapi import APIRouter, HTTPException
from app.models.stock_models import StockInfo
from app.models.response_models import APIResponse
from app.services.stock_service import (
    fetch_stock_data, 
    get_real_time_price, 
    get_market_status,
    clear_stock_cache
)
from typing import List

router = APIRouter()

@router.get("/stocks/{symbol}", response_model=StockInfo)
async def get_stock_info(symbol: str):
    """Get comprehensive real-time stock information for a given symbol"""
    stock_data = fetch_stock_data(symbol)
    if not stock_data:
        raise HTTPException(status_code=404, detail=f"Stock data not found for symbol: {symbol}")
    return stock_data

@router.get("/stocks/{symbol}/price")
async def get_stock_price(symbol: str):
    """Get real-time price for a stock symbol"""
    price = get_real_time_price(symbol)
    if price is None:
        raise HTTPException(status_code=404, detail=f"Price data not found for symbol: {symbol}")
    
    return {
        "symbol": symbol,
        "price": price,
        "timestamp": "real-time"
    }

@router.get("/stocks/{symbol}/status")
async def get_stock_market_status(symbol: str):
    """Get market status for a stock"""
    status = get_market_status(symbol)
    return {
        "symbol": symbol,
        "market_status": status
    }

@router.post("/stocks/refresh")
async def refresh_stock_cache():
    """Clear stock cache to get fresh data"""
    clear_stock_cache()
    return {"message": "Stock cache cleared successfully"}

@router.get("/stocks/popular/indian")
async def get_popular_indian_stocks():
    """Get information for popular Indian stocks"""
    popular_symbols = [
        "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS",
        "HINDUNILVR.NS", "ITC.NS", "KOTAKBANK.NS", "LT.NS", "BAJFINANCE.NS"
    ]
    
    stocks = []
    for symbol in popular_symbols:
        stock_data = fetch_stock_data(symbol)
        if stock_data:
            stocks.append(stock_data)
    
    return {
        "stocks": stocks,
        "count": len(stocks)
    }
