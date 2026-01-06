import requests
import os

# CONFIGURATION
GITHUB_USER = "KFruti88"
REPOS = ["Clay-County-Fuel", "clay-county-news", "Clay-County-All"]
# Search for the town and the mascot to catch sports updates
KEYWORDS = ["louisville", "north clay", "cardinals"]
ACCESS_TOKEN = os.getenv("GH_TOKEN") 

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
        # Check if any keyword matches the filename
        if any(key in name_lower for key in KEYWORDS):
            category = "General"
            if item['name'].endswith(('.png', '.jpg', '.jpeg')):
                category = "Image/Sports"
            elif "calendar" in item['path'].lower() or "event" in name_lower:
                category = "Calendar"
            
            found_items.append(f"- **[{category}]** {item['name']} ([Link]({item['html_url']}))")
            
    return found_items

if __name__ == "__main__":
    report = ["# Louisville, IL - Automated Intelligence Report\n"]
    for repo in REPOS:
        results = scan_repository(repo)
        if results:
            report.append(f"## From {repo}")
            report.extend(results)
            report.append("")
    
    # Save the report to a Markdown file
    with open("LOUISVILLE_REPORT.md", "w") as f:
        f.write("\n".join(report))
    print("Report generated: LOUISVILLE_REPORT.md")
