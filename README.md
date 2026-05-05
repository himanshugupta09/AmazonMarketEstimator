# Amazon Market Estimator (AI-Native)

## System Architecture
A full-stack web application designed to estimate market revenue for Amazon Best Seller categories.
* **Frontend:** ReactJS, TailwindCSS. Component-driven architecture.
* **Backend:** FastAPI (Python). Chosen for asynchronous request handling.
* **AI Categorization:** Hugging Face `facebook/bart-large-mnli` (Zero-Shot Classification) dynamically categorizes market niches based on aggregated product titles.

## Engineering Trade-offs & Infrastructure
1. **Data Ingestion: LLM Agents vs. Traditional Parsing:** Amazon aggressively rate-limits unauthenticated scrapers and frequently mutates their DOM. Rather than using traditional DOM parsing (like BeautifulSoup) which breaks when CSS classes change, this backend utilizes the **TinyFish Agent SDK**. By passing a natural language extraction goal to an autonomous LLM agent, the scraping pipeline is strictly resilient to frontend mutations.
2. **Latency Considerations:** While the Agent approach drastically reduces maintenance engineering, LLM orchestration introduces higher latency (~15-20s per request). In a true enterprise environment, I would decouple this by placing the extraction task into a background queue (e.g., Celery) and having the frontend poll for the result via WebSockets. For this MVP, the synchronous timeout threshold has simply been increased.
3. **Resilience & Graceful Degradation:** If the TinyFish free-tier quota is exceeded or the agent times out, the backend gracefully degrades. It catches the error and serves a realistic mock dataset, flagging it in the UI so the application never crashes for the end user.
4. **Heuristic Financial Model:** Because Amazon does not expose live sales data, the revenue estimations use a heuristic formula based on rank and price `(Est. Sales = max(5000 - (Rank * 400), 100))`. For a production release, this would be replaced by a regression model trained on Keepa/BSR datasets.

## Local Setup
**Backend:**
1. `cd backend`
2. `python -m venv venv`
3. `source venv/bin/activate`
4. `pip install -r requirements.txt`
5. Create a `.env` file with `HF_API_TOKEN` and `TINYFISH_API_KEY`.
6. `pytest` (Run tests)
7. `uvicorn main:app --reload`

**Frontend:**
1. `cd frontend`
2. `npm install`
3. `npm start`