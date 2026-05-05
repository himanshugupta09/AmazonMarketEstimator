from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import URLInput, MarketAnalysisResponse
from services import scrape_with_agent, get_market_category

app = FastAPI(title="Amazon Market Estimator API")

origins = [
    "http://localhost:3000",
    "https://amazon-market-estimator.vercel.app" # <-- Add your live Vercel URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/analyze", response_model=MarketAnalysisResponse)
async def analyze_market(data: URLInput):
    if "amazon." not in data.url:
        raise HTTPException(status_code=400, detail="Invalid URL. Must be an Amazon domain.")
    
    # Delegate to the TinyFish Agent
    is_mock, top_products = scrape_with_agent(data.url)
    
    total_revenue = sum(p['estimated_revenue'] for p in top_products)
    titles = [p['title'] for p in top_products]
    market_niche = get_market_category(titles)

    # CHECK THIS LINE: Make sure the word 'return' is here!
    return MarketAnalysisResponse(
        is_mock_data=is_mock,
        market_niche=market_niche,
        total_estimated_revenue=total_revenue,
        top_10_products=top_products
    )