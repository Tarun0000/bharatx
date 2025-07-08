import os
import serpapi
from dotenv import load_dotenv
load_dotenv()

def get_search_results(user_query):
    client = serpapi.Client(api_key=os.getenv("serp_api_key"))
    params = {
        "engine": "google_shopping",
        "q": user_query["query"],
        "gl": user_query["location"],
        "num": 60,
    }   
    results = client.search(params)
    shopping_results = results["shopping_results"]
    if len(shopping_results) == 0:
        return []
    data=[{'ProductName': item['title'],'Price': item['price'], 'Link': item['product_link'],'Seller':item['source']}for item in results["shopping_results"]]
    return data
