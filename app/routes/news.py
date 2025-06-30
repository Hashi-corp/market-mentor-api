from fastapi import APIRouter
from app.models.news_models import StockNews, NewsArticle
from datetime import datetime

router = APIRouter()

@router.get("/news/{symbol}", response_model=StockNews)
async def get_stock_news(symbol: str):
    """Get recent news articles for a given stock symbol"""
    # Placeholder logic - replace with actual news fetching
    articles = [
        NewsArticle(
            title="Stock hits new high!",
            url="https://example.com/news1",
            published_at=datetime.utcnow(),
            source="Economic Times",
            summary="The stock reached a new high today."
        ),
        NewsArticle(
            title="Analyst upgrades stock",
            url="https://example.com/news2",
            published_at=datetime.utcnow(),
            source="MoneyControl",
            summary="Analyst upgrades the stock to buy."
        )
    ]
    return StockNews(symbol=symbol, articles=articles)
