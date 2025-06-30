from pydantic import BaseModel
from typing import Optional

class StockInfo(BaseModel):
    symbol: str
    name: str
    price: float
    currency: str
    exchange: Optional[str] = None
    change: Optional[float] = None
    percent_change: Optional[float] = None
