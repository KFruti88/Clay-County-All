import requests
import os
import json
import csv
import io

# --- CONFIGURATION ---
GITHUB_USER = "KFruti88"
REPOS = ["Clay-County-Fuel", "clay-county-news", "Clay-County-All"]

# Broad terms for filenames (News/Sports)
KEYWORDS = ["louisville", "north clay", "cardinals", "indians"]

# Specific ID for inside CSV files (Fuel data only)
GAS_STATION_ID = "48026" 

ACCESS_TOKEN = os.getenv("GH_TOKEN") 
TOWN_PATH = "Towns/Louisville".strip()

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
            # Logic: Only pull the row if it contains our specific Station ID
            if GAS_STATION_ID in row_str:
                return f"Casey's ({GAS_STATION_ID}) Update: {', '.join(row)}"
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
        # Skip folders, only scan files
        if item['type'] == 'dir':
            continue
            
        name_lower = item['name'].lower()
        
        # 1. Broad Filename Search (News/General)
        if any(key in name_lower for key in KEYWORDS):
            category = "General"
            if "fuel" in repo_name.lower() or "gas" in name_lower:
                category = "Fuel/Gas"
            found_items.append({
                "category": category, 
                "name": item['name'], 
                "url": item['html_url']
            })
        
        # 2. Deep CSV Search (Specific ID search)
        elif name_lower.endswith('.csv'):
            gas_info = search_csv_content(item['download_url'])
            if gas_info:
                found_items.append({
                    "category": "Fuel/Gas", 
                    "name": gas_info, 
                    "url": item['html_url']
                })
            
    return found_items

if __name__ == "__main__":
    # Ensure the Towns/Louisville directory exists
    os.makedirs(TOWN_PATH, exist_ok=True)

    all_results = []
    # Prepare Markdown Report Content
    markdown_lines = [f"# Louisville, IL - Automated Intelligence Report\n"]

    for repo in REPOS:
        results = scan_repository(repo)
        if results:
            all_results.extend(results)
            markdown_lines.append(f"## Data from {repo}")
            for item in results:
                markdown_lines.append(f"- **[{item['category']}]** {item['name']} ([Link]({item['url']}))")
            markdown_lines.append("")

    # --- SAVE OUTPUT 1: data.json (For the Website) ---
    json_data = {
        "town": "Louisville",
        "last_updated": "2026-01-06",
        "updates": all_results
    }
    json_path = os.path.join(TOWN_PATH, "data.json")
    with open(json_path, "w") as f:
        json.dump(json_data, f, indent=4)

    # --- SAVE OUTPUT 2: LOUISVILLE_REPORT.md (For GitHub) ---
    md_path = os.path.join(TOWN_PATH, "LOUISVILLE_REPORT.md")
    with open(md_path, "w") as f:
        f.write("\n".join(markdown_lines))

    print(f"Successfully processed all repositories. Files saved to {TOWN_PATH}")
