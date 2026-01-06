import requests
import os

# CONFIGURATION
GITHUB_USER = "KFruti88"
REPOS = ["Clay-County-Fuel", "clay-county-news", "Clay-County-All"]
# Search for the town and the mascot (Wolves)
KEYWORDS = ["clay city", "wolves", "lady wolves"]
ACCESS_TOKEN = os.getenv("GH_TOKEN") 

def scan_repository(repo_name):
    print(f"--- Searching {repo_name} for Clay City/Wolves content ---")
    # API URL to get the file tree
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
            if item['name'].lower().endswith(('.png', '.jpg', '.jpeg')):
                category = "Image/Sports"
            elif "calendar" in item['path'].lower() or "event" in name_lower:
                category = "Calendar"
            elif "news" in repo_name.lower():
                category = "News"
            
            found_items.append(f"- **[{category}]** {item['name']} ([View on GitHub]({item['html_url']}))")
            
    return found_items

if __name__ == "__main__":
    report = ["# Clay City, IL - Automated Intelligence Report\n"]
    report.append(f"Last updated: 2026-01-06\n")
    
    total_found = 0
    for repo in REPOS:
        results = scan_repository(repo)
        if results:
            report.append(f"## From {repo}")
            report.extend(results)
            report.append("")
            total_found += len(results)
    
    if total_found == 0:
        report.append("*No new files matching Clay City or Wolves were found in the monitored repositories.*")
    
    # Save the report to a Markdown file
    with open("CLAY_CITY_REPORT.md", "w") as f:
        f.write("\n".join(report))
    print("Report generated: CLAY_CITY_REPORT.md")
