from fastapi import APIRouter
from app.models.news_models import StockNews
from app.services.news_service import get_stock_news

router = APIRouter()

@router.get("/news/{symbol}", response_model=StockNews)
async def news_endpoint(symbol: str):
    """Get recent news articles for a given stock symbol"""
    articles = get_stock_news(symbol)
    return StockNews(symbol=symbol, articles=articles)
