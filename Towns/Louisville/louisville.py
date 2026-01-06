import requests
import os
import json

# CONFIGURATION
GITHUB_USER = "KFruti88"
REPOS = ["Clay-County-Fuel", "clay-county-news", "Clay-County-All"]
KEYWORDS = ["louisville", "north clay", "cardinals"]
ACCESS_TOKEN = os.getenv("GH_TOKEN") 

# CLEAN PATH (This ensures no leading/trailing spaces exist)
TOWN_PATH = "Towns/Louisville".strip()

def scan_repository(repo_name):
    print(f"--- Searching {repo_name} for Louisville content ---")
    url = f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}/contents/"
    headers = {"Authorization": f"token {ACCESS_TOKEN}"} if ACCESS_TOKEN else {}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return []
        contents = response.json()
    except Exception as e:
        print(f"Connection Error: {e}")
        return []

    found_items = []
    for item in contents:
        # Check if item is a file (dictionary) and has a name
        if isinstance(item, dict) and 'name' in item:
            name_lower = item['name'].lower()
            if any(key in name_lower for key in KEYWORDS):
                category = "General"
                if name_lower.endswith(('.png', '.jpg', '.jpeg')):
                    category = "Image/Sports"
                elif "calendar" in item.get('path', '').lower() or "event" in name_lower:
                    category = "Calendar"
                
                found_items.append({
                    "category": category,
                    "name": item['name'],
                    "url": item['html_url']
                })
    return found_items

if __name__ == "__main__":
    # Create the folder safely
    os.makedirs(TOWN_PATH, exist_ok=True)

    all_results = []
    markdown_lines = ["# Louisville, IL - Automated Intelligence Report\n"]

    for repo in REPOS:
        results = scan_repository(repo)
        if results:
            all_results.extend(results)
            markdown_lines.append(f"## From {repo}")
            for item in results:
                markdown_lines.append(f"- **[{item['category']}]** {item['name']} ([Link]({item['url']}))")
            markdown_lines.append("")

    # Save the JSON data (data.json)
    json_data = {
        "town": "Louisville",
        "last_updated": "2026-01-06",
        "updates": all_results
    }
    
    # Path construction using join to prevent slash/space errors
    json_file_path = os.path.join(TOWN_PATH, "data.json")
    with open(json_file_path, "w") as f:
        json.dump(json_data, f, indent=4)

    # Save the Markdown report
    md_file_path = os.path.join(TOWN_PATH, "LOUISVILLE_REPORT.md")
    with open(md_file_path, "w") as f:
        f.write("\n".join(markdown_lines))

    print(f"Successfully updated files in: {TOWN_PATH}")
