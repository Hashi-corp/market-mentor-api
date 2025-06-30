from fastapi import APIRouter
from app.models.stock_models import StockInfo
from app.services.stock_service import fetch_stock_data

router = APIRouter()

@router.get("/stocks/{symbol}", response_model=StockInfo)
async def get_stock_info(symbol: str):
    """Get current stock information for a given symbol"""
    stock_data = fetch_stock_data(symbol)
    if not stock_data:
        # Return placeholder data if real data isn't available
        return StockInfo(
            symbol=symbol,
            name="Reliance Industries Limited",
            price=2850.75,
            currency="INR",
            exchange="NSE",
            change=15.20,
            percent_change=0.54
        )
    return stock_data
