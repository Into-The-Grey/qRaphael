import os
from github import Github

# Get GitHub token from environment variables
token = os.getenv("READ_GEN_TOKEN")
repo_name = "Into-The-Grey/qRaphael"
g = Github(token)
repo = g.get_repo(repo_name)

# Define expanded phases and milestones
phases = {
    "Phase 1: Initial Setup and Infrastructure": [
        "Server and Database Setup",
        "Basic Text Generation",
        "Version Control and CI/CD"
    ],
    "Phase 2: Basic Communication Capabilities": [
        "Text-to-Speech Implementation",
        "Speech-to-Text Implementation",
        "Email and Appointment Management"
    ],
    "Phase 3: Basic Smart Home Integration": [
        "Initial Smart Home Control",
        "Resource Monitoring",
        "Basic Security Features"
    ],
    "Phase 4: Enhanced Text and Voice Interaction": [
        "Advanced Text Generation",
        "Voice Recognition",
        "Voice Interaction Security"
    ],
    "Phase 5: Intermediate Task Management": [
        "Grocery and Shipping Tracking",
        "Financial Data Integration",
        "Medical Data Integration"
    ],
    "Phase 6: Enhanced Smart Home Integration": [
        "Advanced Smart Home Control",
        "Real-Time Monitoring"
    ],
    "Phase 7: Image and Video Recognition": [
        "Basic Image Recognition",
        "Video Stream Analysis",
        "Advanced Security Features"
    ],
    "Phase 8: Error Handling and Self-Improvement": [
        "Downtime Error Analysis",
        "Automated Error Resolution",
        "Error Logging and Reporting"
    ],
    "Phase 9: Advanced Interaction Capabilities": [
        "Phone Call Management",
        "Natural Language Processing",
        "Context-Aware Responses"
    ],
    "Phase 10: Proactive Decision Making": [
        "Problem-Solving Capabilities",
        "Learning from Mistakes",
        "Proactive Task Management"
    ],
    "Phase 11: Security and Privacy Enhancements": [
        "Advanced Voice Security",
        "Data Privacy Management",
        "Secure Data Storage"
    ],
    "Phase 12: Continuous Learning and Adaptation": [
        "Ongoing Model Training",
        "User Feedback Integration",
        "Adaptive Learning Algorithms"
    ],
    "Phase 13: Expanded Integration Capabilities": [
        "Third-Party API Integration",
        "Social Media Management",
        "Educational Assistance"
    ],
    "Phase 14: Emotional and Psychological Tracking": [
        "Emotional Analysis",
        "Psychological Health Monitoring",
        "Wellness Recommendations"
    ],
    "Phase 15: Advanced Autonomy and Optimization": [
        "Full Autonomy Implementation",
        "System Optimization",
        "Scalability Features"
    ],
    "Phase 16: Internet of Things (IoT) Integration": [
        "Raspberry Pi Integration",
        "Smart Sensor Integration",
        "IoT Data Management"
    ],
    "Phase 17: Robotics Integration": [
        "Basic Robotics Control",
        "Advanced Robotics Programming",
        "Robotic Task Automation"
    ],
    "Phase 18: 3D Printing Integration": [
        "3D Printer Setup",
        "Automated Print Job Management",
        "Custom Object Design"
    ],
    "Phase 19: Advanced IoT and Robotics Integration": [
        "Integrated Home Automation",
        "Autonomous Maintenance Tasks",
        "IoT and Robotics Security"
    ],
    "Phase 20: Predictive Security and Self-Optimization": [
        "Predictive Security Analysis",
        "Reinforced Security Measures",
        "Self-Adjusting Loading Parameters"
    ],
    "Phase 21: Quantum Readiness": [
        "Quantum Algorithm Understanding",
        "Simulated Quantum Computation",
        "Integration with Quantum APIs"
    ]
}

# Step 1: Get existing milestones
existing_milestones = repo.get_milestones()
existing_milestone_titles = [milestone.title for milestone in existing_milestones]

# Step 2: Create milestones if they don't already exist
for phase, milestones in phases.items():
    for milestone in milestones:
        milestone_title = f"{phase} - {milestone}"
        if milestone_title not in existing_milestone_titles:
            repo.create_milestone(
                title=milestone_title,
                state="open",
                description=f"Milestone for {milestone} in {phase}"
            )

# Define new labels to avoid duplicates
labels = [
    {"name": "backend", "color": "f9d0c4", "description": "Related to backend"},
    {"name": "frontend", "color": "c2e0c6", "description": "Related to frontend"},
    {"name": "design", "color": "e99695", "description": "Design-related issue"},
    {"name": "testing", "color": "9cd8de", "description": "Testing-related issue"},
    {"name": "devops", "color": "e5e5e5", "description": "DevOps-related issue"},
    {"name": "ux", "color": "ffa500", "description": "User experience improvement"},
    {"name": "ai", "color": "00ff00", "description": "Artificial Intelligence related"},
    {"name": "ml", "color": "6600cc", "description": "Machine Learning related"},
    {"name": "data", "color": "ff9900", "description": "Data-related issue"},
    {"name": "automation", "color": "ff5050", "description": "Automation tasks"},
    {"name": "research", "color": "800000", "description": "Research tasks"},
    {"name": "maintenance", "color": "008000", "description": "Maintenance tasks"},
    {"name": "compatibility", "color": "000080", "description": "Compatibility issues"},
    {"name": "api", "color": "00cccc", "description": "API-related tasks"},
    {"name": "integration", "color": "0066cc", "description": "Integration tasks"},
    {"name": "optimization", "color": "ffcc99", "description": "Optimization tasks"},
    {"name": "performance", "color": "00cc99", "description": "Performance improvements"},
    {"name": "security", "color": "cc0033", "description": "Security-related issues"},
    {"name": "infrastructure", "color": "ffcc00", "description": "Infrastructure-related tasks"},
    {"name": "operations", "color": "660066", "description": "Operations-related tasks"},
    {"name": "support", "color": "ff33cc", "description": "Support tasks"},
    {"name": "refactor", "color": "cccc00", "description": "Code refactoring"},
    {"name": "monitoring", "color": "ff6666", "description": "Monitoring tasks"},
    {"name": "logging", "color": "9999ff", "description": "Logging-related tasks"},
    {"name": "build", "color": "ccffcc", "description": "Build-related tasks"},
    {"name": "deployment", "color": "ff9966", "description": "Deployment tasks"},
    {"name": "architecture", "color": "cc6699", "description": "Architecture-related tasks"},
    {"name": "prototype", "color": "ff99cc", "description": "Prototype-related tasks"},
    {"name": "evaluation", "color": "6699cc", "description": "Evaluation-related tasks"}
]

# Step 3: Get existing labels
existing_labels = {label.name: label for label in repo.get_labels()}

# Step 4: Create or update labels
for label in labels:
    if label["name"] in existing_labels:
        existing_label = existing_labels[label["name"]]
        existing_label.edit(name=label["name"], color=label["color"], description=label["description"])
    else:
        repo.create_label(
            name=label["name"],
            color=label["color"],
            description=label["description"]
        )

print("Milestones and labels created!")
