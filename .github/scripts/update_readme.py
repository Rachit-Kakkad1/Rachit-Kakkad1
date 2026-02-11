import os
import requests
from datetime import datetime

USERNAME = "Rachit-Kakkad1"
README_PATH = "README.md"

def get_latest_repo():
    url = f"https://api.github.com/users/{USERNAME}/repos?sort=pushed"
    repos = requests.get(url).json()

    for repo in repos:
        # skip profile repo (same as username)
        if repo["name"].lower() != USERNAME.lower():
            return repo["name"]

    return USERNAME


def get_latest_commit(repo):
    url = f"https://api.github.com/repos/{USERNAME}/{repo}/commits"
    commits = requests.get(url).json()
    return commits[0]["commit"]["message"]

def update_readme(repo, commit_msg):
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    start = "<!-- AUTO-CURRENT-START -->"
    end = "<!-- AUTO-CURRENT-END -->"

    new_section = f"""
<!-- AUTO-CURRENT-START -->
## ⚡ Currently Building

- 🚀 **Active Repo:** {repo}  
- 📝 **Latest Commit:** {commit_msg}  
- ⏱ **Updated:** {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}
<!-- AUTO-CURRENT-END -->
"""

    import re
    updated = re.sub(f"{start}.*?{end}", new_section, content, flags=re.S)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(updated)


if __name__ == "__main__":
    repo = get_latest_repo()
    commit = get_latest_commit(repo)
    update_readme(repo, commit)
