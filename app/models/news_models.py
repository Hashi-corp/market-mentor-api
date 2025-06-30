from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class NewsArticle(BaseModel):
    title: str
    url: str
    published_at: datetime
    source: Optional[str] = None
    summary: Optional[str] = None

class StockNews(BaseModel):
    symbol: str
    articles: List[NewsArticle]
