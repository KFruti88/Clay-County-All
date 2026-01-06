import requests
import os
import json
import csv
import io
from datetime import datetime

# --- CONFIGURATION ---
GITHUB_USER = "KFruti88"
# Targeted sync for gas prices
FUEL_REPO = "Clay-County-Fuel"
FUEL_FILE = "gas_prices.csv"

# Global news repository to scan
NEWS_REPOS = ["clay-county-news", "Clay-County-All"]

# Strict Filtering Logic
INCLUDE_KEYS = ["louisville", "north clay", "clay county"]
EXCLUDE_KEYS = ["flora", "clay city", "xenia", "sailor springs"]

# Unique ID for the Louisville Casey's station
GAS_STATION_ID = "48026" 
ACCESS_TOKEN = os.getenv("GH_TOKEN") 
TOWN_PATH = "Towns/Louisville"

def get_locked_gas_prices():
    """Syncs directly with the raw CSV file in the Fuel repository."""
    url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{FUEL_REPO}/main/{FUEL_FILE}"
    # Use headers for private repos or rate-limit protection
    headers = {"Authorization": f"token {ACCESS_TOKEN}"} if ACCESS_TOKEN else {}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Parse CSV content from the web response
            reader = csv.reader(io.StringIO(response.text))
            for row in reader:
                # Lock onto the row matching your specific station ID
                if row and row[0].strip() == GAS_STATION_ID:
                    # Return the raw row for the JS .split(',') logic
                    return ",".join(row) 
    except Exception as e:
        print(f"Error syncing gas_prices.csv: {e}")
    return None

def scan_filtered_news():
    """Scans news repos using strict inclusion/exclusion rules."""
    found_news = []
    headers = {"Authorization": f"token {ACCESS_TOKEN}"} if ACCESS_TOKEN else {}
    
    for repo in NEWS_REPOS:
        api_url = f"https://api.github.com/repos/{GITHUB_USER}/{repo}/contents/"
        res = requests.get(api_url, headers=headers)
        if res.status_code == 200:
            for item in res.json():
                name_lower = item['name'].lower()
                
                # Logic: Must have Louisville/North Clay but MUST NOT have Flora/Xenia
                is_included = any(k in name_lower for k in INCLUDE_KEYS)
                is_excluded = any(ex in name_lower for ex in EXCLUDE_KEYS)
                
                if is_included and not is_excluded:
                    found_news.append({
                        "category": "General",
                        "name": item['name'],
                        "url": item['html_url']
                    })
    return found_news

if __name__ == "__main__":
    # Ensure local town directory exists
    os.makedirs(TOWN_PATH, exist_ok=True)

    # Execute Locked Sync
    gas_row = get_locked_gas_prices()
    news_items = scan_filtered_news()

    # Consolidate Updates
    all_updates = []
    if gas_row:
        # High priority entry for the digital sign widget
        all_updates.append({
            "category": "Fuel", 
            "name": gas_row, 
            "url": f"https://github.com/KFruti88/{FUEL_REPO}/blob/main/{FUEL_FILE}"
        })
    all_updates.extend(news_items)

    # Save finalized data.json
    output_data = {
        "town": "Louisville",
        "last_sync": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "updates": all_updates
    }
    
    with open(os.path.join(TOWN_PATH, "data.json"), "w") as f:
        json.dump(output_data, f, indent=4)

    print(f"Sync Complete: {TOWN_PATH}/data.json is locked and updated.")
