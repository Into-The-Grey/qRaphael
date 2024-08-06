import os
from github import Github # type: ignore

# Get GitHub token from environment variables
token = os.getenv("READ_GEN_TOKEN")
repo_name = "Into-The-Grey/qRaphael"
g = Github(token)
repo = g.get_repo(repo_name)

# Define labels to be added
labels_to_add = {
    "ai": "Artificial Intelligence related",
    "Announcement": "Important News",
    "api": "API-related tasks",
    "architecture": "Architecture-related tasks",
    "automation": "Automation tasks",
    "backend": "Related to backend",
    "Breakthrough": "Succeeded after much struggle",
    "bug": "Something isn't working",
    "build": "Build-related tasks",
    "compatibility": "Compatibility issues",
    "data": "Data-related issue",
    "deployment": "Deployment tasks",
    "design": "Design-related issue",
    "devops": "DevOps-related issue",
    "documentation": "Improvements or additions to documentation",
    "duplicate": "This issue or pull request already exists",
    "enhancement": "New feature or request",
    "evaluation": "Evaluation-related tasks",
    "frontend": "Related to frontend",
    "good first issue": "Good for newcomers",
    "help wanted": "Extra attention is needed",
    "infrastructure": "Infrastructure-related tasks",
    "integration": "Integration tasks",
    "invalid": "This doesn't seem right",
    "logging": "Logging-related tasks",
    "maintenance": "Maintenance tasks",
    "ml": "Machine Learning related",
    "monitoring": "Monitoring tasks",
    "operations": "Operations-related tasks",
    "optimization": "Optimization tasks",
    "performance": "Performance improvements",
    "prototype": "Prototype-related tasks",
    "question": "Further information is requested",
    "refactor": "Code refactoring",
    "research": "Research tasks",
    "security": "Security-related issues",
    "support": "Support tasks",
    "testing": "Testing-related issue",
    "ux": "User experience improvement",
    "wontfix": "This will not be worked on"
}

# Get open issues
open_issues = repo.get_issues(state="open")

for issue in open_issues:
    issue_labels = {label.name for label in issue.labels}
    for label_name, label_description in labels_to_add.items():
        if label_name not in issue_labels:
            issue.add_to_labels(label_name)
            print(f"Added label '{label_name}' to issue #{issue.number}")

print("Issue labeling completed!")
