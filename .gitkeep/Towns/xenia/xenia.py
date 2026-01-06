import requests
import os

# CONFIGURATION
GITHUB_USER = "KFruti88"
REPOS = ["Clay-County-Fuel", "clay-county-news", "Clay-County-All"]
# Keywords include the town name and the mascot (Tigers)
KEYWORDS = ["xenia", "tigers", "lady tigers"]
ACCESS_TOKEN = os.getenv("GH_TOKEN") 

def scan_repository(repo_name):
    print(f"--- Searching {repo_name} for Xenia/Tigers content ---")
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
            if item['name'].lower().endswith(('.png', '.jpg', '.jpeg')):
                category = "Image/Sports"
            elif "calendar" in item['path'].lower() or "event" in name_lower:
                category = "Calendar"
            elif "news" in repo_name.lower():
                category = "News"
            
            found_items.append(f"- **[{category}]** {item['name']} ([View on GitHub]({item['html_url']}))")
            
    return found_items

if __name__ == "__main__":
    report = ["# Xenia, IL - Automated Intelligence Report\n"]
    report.append(f"Last updated: 2026-01-06\n")
    
    for repo in REPOS:
        results = scan_repository(repo)
        if results:
            report.append(f"## From {repo}")
            report.extend(results)
            report.append("")
    
    with open("XENIA_REPORT.md", "w") as f:
        f.write("\n".join(report))
    print("Report generated: XENIA_REPORT.md")
