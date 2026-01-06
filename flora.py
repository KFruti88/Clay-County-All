import requests
import os

# CONFIGURATION
GITHUB_USER = "KFruti88"
REPOS = ["Clay-County-Fuel", "clay-county-news", "Clay-County-All"]
TARGET_KEYWORD = "flora"  # The script will look for this in filenames
ACCESS_TOKEN = os.getenv("GH_TOKEN") # Set this in your environment or GitHub Secrets

def get_flora_data(repo_name):
    print(f"--- Scanning {repo_name} for Flora info ---")
    
    # API URL to get the file tree
    url = f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}/contents/"
    headers = {"Authorization": f"token {ACCESS_TOKEN}"} if ACCESS_TOKEN else {}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error accessing {repo_name}: {response.status_code}")
        return

    contents = response.json()
    
    for item in contents:
        # 1. Search by Filename (News, Events, Calendar)
        if TARGET_KEYWORD in item['name'].lower():
            print(f"Found Match: {item['name']} | URL: {item['download_url']}")
            
        # 2. Identify Images (png, jpg, jpeg)
        if item['name'].lower().endswith(('.png', '.jpg', '.jpeg')):
            # If it's an image, we still check if it's in a 'Flora' folder or has the name
            if TARGET_KEYWORD in item['path'].lower():
                print(f"Found Image: {item['name']} | URL: {item['download_url']}")

        # 3. Handle Folders (Recursively check if needed)
        if item['type'] == 'dir' and TARGET_KEYWORD in item['name'].lower():
            print(f"Found Folder dedicated to Flora: {item['path']}")

if __name__ == "__main__":
    for repo in REPOS:
        get_flora_data(repo)
