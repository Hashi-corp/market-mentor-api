from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StockInfo(BaseModel):
    symbol: str
    name: str
    price: float
    currency: str
    exchange: Optional[str] = None
    change: Optional[float] = None
    percent_change: Optional[float] = None
    
    # Market data
    market_cap: Optional[float] = None
    volume: Optional[int] = None
    avg_volume: Optional[int] = None
    
    # Price ranges
    day_high: Optional[float] = None
    day_low: Optional[float] = None
    week_52_high: Optional[float] = None
    week_52_low: Optional[float] = None
    
    # Financial metrics
    pe_ratio: Optional[float] = None
    eps: Optional[float] = None
    dividend_yield: Optional[float] = None
    book_value: Optional[float] = None
    
    # Market status
    market_state: Optional[str] = None
    last_updated: Optional[datetime] = None
    
    # Additional info
    sector: Optional[str] = None
    industry: Optional[str] = None
