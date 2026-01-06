import requests
import os
import json
import csv
import io
from datetime import datetime

# --- CONFIGURATION ---
GITHUB_USER = "KFruti88"
REPOS = ["Clay-County-Fuel", "clay-county-news", "Clay-County-All"]

# Strict Town Filtering for local data.json
INCLUDE_KEYS = ["louisville", "north clay", "clay county"]
EXCLUDE_KEYS = ["flora", "clay city", "xenia", "sailor springs"]

# Specific ID for inside CSV files (Fuel data only)
GAS_STATION_ID = "48026" 

ACCESS_TOKEN = os.getenv("GH_TOKEN") 
TOWN_PATH = "Towns/Louisville"

def search_csv_content(file_url):
    """Downloads a CSV and looks specifically for the Casey's Station ID."""
    headers = {"Authorization": f"token {ACCESS_TOKEN}"} if ACCESS_TOKEN else {}
    try:
        response = requests.get(file_url, headers=headers)
        if response.status_code != 200:
            return None

        csv_raw = response.text
        reader = csv.reader(io.StringIO(csv_raw))
        
        for row in reader:
            row_str = ",".join(row)
            # Logic: We need the raw comma-separated string for the JS split(',') to work
            if GAS_STATION_ID in row_str:
                return row_str # Returns "48026,Casey's,3.29,3.89"
    except Exception as e:
        print(f"Error reading CSV content: {e}")
    return None

def scan_repository(repo_name):
    print(f"--- Deep Scanning {repo_name} ---")
    url = f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}/contents/"
    headers = {"Authorization": f"token {ACCESS_TOKEN}"} if ACCESS_TOKEN else {}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []

    found_items = []
    contents = response.json()
    
    for item in contents:
        if item['type'] == 'dir':
            continue
            
        name_lower = item['name'].lower()
        
        # 1. Broad Filename Search with Strict Exclusion
        if any(key in name_lower for key in INCLUDE_KEYS):
            # Check if it should be excluded
            if any(ex in name_lower for ex in EXCLUDE_KEYS):
                continue # Skip Flora/Xenia news even if it says "Clay County"
                
            category = "General"
            if "fuel" in repo_name.lower() or "gas" in name_lower:
                category = "Fuel"
            
            found_items.append({
                "category": category, 
                "name": item['name'], 
                "url": item['html_url']
            })
        
        # 2. Deep CSV Search (Specifically for the Gas Widget)
        elif name_lower.endswith('.csv'):
            gas_info = search_csv_content(item['download_url'])
            if gas_info:
                found_items.append({
                    "category": "Fuel", 
                    "name": gas_info, 
                    "url": item['html_url']
                })
            
    return found_items

if __name__ == "__main__":
    # Ensure the Towns/Louisville directory exists
    os.makedirs(TOWN_PATH, exist_ok=True)

    all_results = []
    
    for repo in REPOS:
        results = scan_repository(repo)
        if results:
            all_results.extend(results)

    # --- SAVE OUTPUT: data.json (Optimized for the Glossy Website) ---
    # We wrap results in an "updates" key so JS can find it
    json_data = {
        "town": "Louisville",
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "updates": all_results
    }
    
    json_path = os.path.join(TOWN_PATH, "data.json")
    with open(json_path, "w") as f:
        json.dump(json_data, f, indent=4)

    # --- SAVE OUTPUT: LOUISVILLE_REPORT.md (For GitHub Logs) ---
    markdown_lines = [f"# Louisville Intelligence Log - {json_data['last_updated']}\n"]
    for item in all_results:
        markdown_lines.append(f"- **[{item['category']}]** {item['name']} [View]({item['url']})")
    
    md_path = os.path.join(TOWN_PATH, "LOUISVILLE_REPORT.md")
    with open(md_path, "w") as f:
        f.write("\n".join(markdown_lines))

    print(f"Successfully processed. Files saved to {TOWN_PATH}")
