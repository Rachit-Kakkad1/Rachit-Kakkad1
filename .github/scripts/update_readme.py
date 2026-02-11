import requests
import re
from datetime import datetime

USERNAME = "Rachit-Kakkad1"
README_PATH = "README.md"


def get_repos():
    url = f"https://api.github.com/users/{USERNAME}/repos?sort=pushed"
    return requests.get(url).json()


def pick_active_repo(repos):
    for repo in repos:
        # skip profile repo
        if repo["name"].lower() != USERNAME.lower():
            return repo
    return repos[0]


def get_latest_commit(repo_name):
    url = f"https://api.github.com/repos/{USERNAME}/{repo_name}/commits"
    commits = requests.get(url).json()
    return commits[0]["commit"]["message"]


def get_live_link(repo):
    # try homepage first
    if repo.get("homepage"):
        return repo["homepage"]

    # common deployment guess
    name = repo["name"]
    return f"https://{name}.vercel.app"


def build_section(repo, commit_msg):
    stars = repo["stargazers_count"]
    lang = repo["language"] or "Unknown"
    live = get_live_link(repo)
    updated = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    return f"""
<!-- AUTO-DASHBOARD-START -->
## ⚡ Currently Building

### 🚀 {repo['name']}

- ⭐ **Stars:** {stars}  
- 🧠 **Primary Language:** {lang}  
- 📝 **Latest Commit:** {commit_msg}  
- 🌐 **Live Demo:** {live}  
- ⏱ **Updated:** {updated}

<!-- AUTO-DASHBOARD-END -->
"""


def update_readme(section):
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r"<!-- AUTO-DASHBOARD-START -->.*?<!-- AUTO-DASHBOARD-END -->"
    updated = re.sub(pattern, section, content, flags=re.S)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(updated)


def main():
    repos = get_repos()
    repo = pick_active_repo(repos)
    commit = get_latest_commit(repo["name"])
    section = build_section(repo, commit)
    update_readme(section)


if __name__ == "__main__":
    main()
