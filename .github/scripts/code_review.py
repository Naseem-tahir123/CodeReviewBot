import os
import requests
from github import Github

# Initialize GitHub API
github_token = os.getenv("GITHUB_TOKEN")
g = Github(github_token)

# Get PR details
repo_name = os.getenv("GITHUB_REPOSITORY")
pr_number = int(os.getenv("GITHUB_EVENT_PULL_REQUEST_NUMBER"))
repo = g.get_repo(repo_name)
pr = repo.get_pull(pr_number)

# Gemini API setup
gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

# Review each file in the PR
for file in pr.get_files():
    patch = file.patch
    if not patch:
        continue

    # Prepare prompt for Gemini
    prompt = f'''
    Review this code diff and suggest improvements. Focus on bugs, code quality, and best practices:
    ```diff
    {patch}
    ```
    '''