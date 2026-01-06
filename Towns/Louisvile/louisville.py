import requests
import os
import json  # 1. Added json import

# CONFIGURATION
GITHUB_USER = "KFruti88"
REPOS = ["Clay-County-Fuel", "clay-county-news", "Clay-County-All"]
KEYWORDS = ["louisville", "north clay", "cardinals"]
ACCESS_TOKEN = os.getenv("GH_TOKEN") 
# 2. Define your output path
TOWN_PATH = "Towns/Louisville/"

def scan_repository(repo_name):
    print(f"--- Searching {repo_name} for Louisville/North Clay content ---")
    url = f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}/contents/"
    headers = {"Authorization": f"token {ACCESS_TOKEN}"} if ACCESS_TOKEN else {}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []

    found_items = []
    contents = response.json()
    
    for item in contents:
        name_lower = item['name'].lower()
        if any(key in name_lower for key in KEYWORDS):
            category = "General"
            if item['name'].endswith(('.png', '.jpg', '.jpeg')):
                category = "Image/Sports"
            elif "calendar" in item['path'].lower() or "event" in name_lower:
                category = "Calendar"
            
            # Store as a dictionary for the JSON file
            found_items.append({
                "category": category,
                "name": item['name'],
                "url": item['html_url']
            })
            
    return found_items

if __name__ == "__main__":
    # 3. Create the folder if it doesn't exist
    os.makedirs(TOWN_PATH, exist_ok=True)

    all_results = []
    markdown_lines = ["# Louisville, IL - Automated Intelligence Report\n"]

    for repo in REPOS:
        results = scan_repository(repo)
        if results:
            all_results.extend(results) # Keep data for JSON
            markdown_lines.append(f"## From {repo}")
            for item in results:
                markdown_lines.append(f"- **[{item['category']}]** {item['name']} ([Link]({item['url']}))")
            markdown_lines.append("")

    # 4. Save the JSON data for your website
    json_data = {
        "town": "Louisville",
        "last_updated": "2026-01-06",
        "updates": all_results
    }
    with open(f"{TOWN_PATH}data.json", "w") as f:
        json.dump(json_data, f, indent=4)

    # 5. Save the Markdown file inside the town folder too
    with open(f"{TOWN_PATH}LOUISVILLE_REPORT.md", "w") as f:
        f.write("\n".join(markdown_lines))

    print(f"Files generated in {TOWN_PATH}")
