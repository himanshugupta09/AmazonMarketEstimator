import os
import json
import requests
from dotenv import load_dotenv
from tinyfish import TinyFish

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY", "")
TINYFISH_API_KEY = os.getenv("TINYFISH_API_KEY", "")
HF_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
# Initialize TinyFish Client
tf_client = TinyFish(api_key=TINYFISH_API_KEY) if TINYFISH_API_KEY else None

# Fallback Data for Graceful Degradation
MOCK_PRODUCTS = [
    {"rank": 1, "title": "Wireless Earbuds with Active Noise Cancellation", "price": 49.99, "estimated_sales": 4600, "estimated_revenue": 229954.0},
    {"rank": 2, "title": "Bluetooth Portable Speaker Waterproof", "price": 29.99, "estimated_sales": 4200, "estimated_revenue": 125958.0},
    {"rank": 3, "title": "Smart Watch Fitness Tracker 2024 Edition", "price": 35.00, "estimated_sales": 3800, "estimated_revenue": 133000.0},
    {"rank": 4, "title": "USB-C Fast Charging Cable 6ft (2-Pack)", "price": 12.99, "estimated_sales": 3400, "estimated_revenue": 44166.0},
    {"rank": 5, "title": "Ergonomic Wireless Mouse with USB Receiver", "price": 15.50, "estimated_sales": 3000, "estimated_revenue": 46500.0}
]



def get_market_category(titles: list) -> str:
    if not titles or not HF_API_KEY: 
        print("-> HF Error: No titles provided or Missing HF_API_KEY")
        return "Unknown Niche"
        
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    text_to_analyze = " ".join(titles)[:1000]
    payload = {
        "inputs": text_to_analyze,
        "parameters": {"candidate_labels": ["electronics", "home goods", "software", "books", "health", "apparel"]}
    }
    try:
        # Increased timeout to 10s to help with Hugging Face cold starts
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            return response.json().get('labels', ['Unknown Niche'])[0]
            
        # X-RAY VISION: Print the exact error Hugging Face returns
        print(f"-> HF API Error ({response.status_code}): {response.text}")
        return "Uncategorized (AI Error)"
        
    except Exception as e:
        print(f"-> HF Network Error: {e}")
        return "Uncategorized (Network Error)"

def scrape_with_agent(url: str):
    """Uses a TinyFish LLM Agent to extract data, immune to DOM changes."""
    if not tf_client:
        print("No TinyFish API key found. Triggering fallback.")
        return True, MOCK_PRODUCTS

    goal = """
    Extract the top 10 products from this Amazon Best Sellers page.
    For each product, get the rank (integer), the full title (string), and the price (float).
    If a price is hidden or missing, use 15.00.
    Return ONLY a raw JSON array of objects with keys: rank, title, price.
    Do not include any markdown formatting, backticks, or extra text. Just the JSON array.
    """
    try:
        print("Spawning TinyFish Agent...")
        final_data_list = []
        
        with tf_client.agent.stream(url=url, goal=goal) as stream:
            for event in stream:
                # 1. Convert ANY event object into a safe, standard Python dictionary
                e_dict = {}
                if isinstance(event, dict):
                    e_dict = event
                elif hasattr(event, "model_dump"): # For newer Pydantic models
                    e_dict = event.model_dump()
                elif hasattr(event, "dict"): # For older Pydantic models
                    e_dict = event.dict()
                elif hasattr(event, "__dict__"): # For standard Python classes
                    e_dict = event.__dict__
                else:
                    # Ultimate fallback
                    for k in ["result_json", "data", "result", "type"]:
                        if hasattr(event, k):
                            e_dict[k] = getattr(event, k)
                
                # Keep the terminal clean (ignoring the spammy heartbeats)
                e_type = str(e_dict.get("type", type(event).__name__))
                if "HEARTBEAT" not in e_type:
                    print(f"-> Agent Status: {e_type}")

                # 2. Safely extract the array directly (No string parsing needed!)
                if "result_json" in e_dict and e_dict["result_json"]:
                    res = e_dict["result_json"]
                    # TinyFish puts the array inside a dict key called 'result'
                    if isinstance(res, dict) and "result" in res:
                        final_data_list = res["result"]
                    elif isinstance(res, list):
                        final_data_list = res
        
        # 3. Process the native data
        if final_data_list and isinstance(final_data_list, list):
            products = []
            for item in final_data_list[:10]:
                rank = int(item.get("rank", 0))
                price = float(item.get("price", 15.00))
                title = str(item.get("title", "Unknown Title"))
                
                est_sales = max(5000 - (rank * 400), 100)
                products.append({
                    "rank": rank, "title": title, "price": price,
                    "estimated_sales": est_sales, "estimated_revenue": est_sales * price
                })
            return False, products
        else:
            raise ValueError("Agent finished but did not find a valid result array.")

    except Exception as e:
        print(f"\nAgent Extraction Failed: {e}. Triggering fallback.")
        return True, MOCK_PRODUCTS
    
    except Exception as e:
        print(f"\nAgent Extraction Failed: {e}. Triggering fallback.")
        return True, MOCK_PRODUCTS
    
    except Exception as e:
        print(f"\nAgent Extraction Failed: {e}. Triggering fallback.")
        return True, MOCK_PRODUCTS
    except Exception as e:
            print(f"\nAgent Extraction Failed: {e}. Triggering fallback.")
            return True, MOCK_PRODUCTS
        
    
    except Exception as e:
        print(f"Agent Extraction Failed: {e}. Triggering fallback.")
        return True, MOCK_PRODUCTS