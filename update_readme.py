import os
from datetime import datetime, timedelta
from github import Github

# Get GitHub token from environment variables
token = os.getenv("READ_GEN_TOKEN")
repo_name = "Into-The-Grey/qRaphael"
g = Github(token)
repo = g.get_repo(repo_name)

# Calculate the time range for commits in the last hour
now = datetime.utcnow()
one_hour_ago = now - timedelta(hours=1)

# Fetch commits from the last hour
commits = repo.get_commits(since=one_hour_ago)

# Prepare the content to append
content_to_append = "\n## Updates in the Last Hour\n"
for commit in commits:
    message = commit.commit.message
    timestamp = commit.commit.author.date
    content_to_append += f"- {message} (at {timestamp})\n"

# Read the current README.md content
with open("README.md", "r") as file:
    readme_content = file.read()

# Append the new content
new_readme_content = readme_content + content_to_append

# Write the updated content back to README.md
with open("README.md", "w") as file:
    file.write(new_readme_content)

print("README.md updated with the latest commit messages!")
