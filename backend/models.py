from pydantic import BaseModel
from typing import List

class URLInput(BaseModel):
    url: str

class Product(BaseModel):
    rank: int
    title: str
    price: float
    estimated_sales: int
    estimated_revenue: float

class MarketAnalysisResponse(BaseModel):
    is_mock_data: bool
    market_niche: str
    total_estimated_revenue: float
    top_10_products: List[Product]