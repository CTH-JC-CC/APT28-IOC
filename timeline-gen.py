import matplotlib.pyplot as plt
import numpy as np

# Define the categories and their contents
categories = {
    "Initial Access": [
        {"label": "Event 1", "date": "April 2023", "description": "APT28 uses a spear-phishing email with a malicious attachment to gain initial access into the target organization's network."},
    ],
    "Attack Phase": [
        {"label": "Event 2", "date": "April 2023 - May 2023", "description": "APT28 uses stolen credentials to move laterally within the network and gain access to sensitive data."},
        {"label": "Event 3", "date": "May 2023 - June 2023", "description": "APT28 uses a zero-day exploit to gain access to a critical system in the network."},
    ],
    "Discovery": [
        {"label": "Lead 1", "date": "June 2023", "description": "The target organization's security team notices suspicious network traffic and begins investigating."},
        {"label": "Lead 2", "date": "June 2023", "description": "The security team discovers APT28's presence in the network and begins analyzing the attack."},
    ],
    "Threat Hunt Begins": [
        {"label": "Tool Used 1", "date": "June 2023 - July 2023", "description": "The security team uses a combination of network traffic analysis tools and endpoint detection and response (EDR) tools to track APT28's movements in the network."},
        {"label": "Tool Used 2", "date": "July 2023 - August 2023", "description": "The security team also deploys a threat hunting tool that leverages machine learning algorithms to identify anomalous behavior in the network."},
    ],
    "Report": [
        {"label": "Report", "date": "August 2023", "description": "The security team compiles a report detailing APT28's tactics, techniques, and procedures (TTPs), and shares it with relevant stakeholders, including law enforcement and industry peers, to prevent similar attacks in the future."},
    ]
}

# Set up the plot
fig, ax = plt.subplots()

# Define the colors for each category
colors = {
    "Initial Access": "#e41a1c",
    "Attack Phase": "#377eb8",
    "Discovery": "#4daf4a",
    "Threat Hunt Begins": "#984ea3",
    "Report": "#ff7f00"
}

# Plot each category and its contents
y_pos = 0
for category, contents in categories.items():
    # Plot the category label
    ax.annotate(category, xy=(0, y_pos + 0.2), fontsize=12, fontweight="bold", color=colors[category])
    # Plot each content item in the category
    for item in contents:
        start, end = item["date"].split(" - ") if " - " in item["date"] else (item["date"], item["date"])
        ax.plot([start, end], [y_pos, y_pos], color=colors[category], lw=6, solid_capstyle="butt")
        ax.annotate(item["label"], xy=(start, y_pos), fontsize=10, ha="left", va="center")
        ax.annotate(item["description"], xy=(start, y_pos), xytext=(10, 0), textcoords="offset points", fontsize=8, ha="left", va="center")
    # Increase the y-position for the next category
    y_pos += 1

# Set the x-axis limits
ax.set_xlim(left="April 2023", right="September 2023")

# Set the y-axis limits
ax.set_ylim(bottom=-0.5, top=len(categories)-0.5)

# Set the tick marks and labels for the x-axis
date_ticks = ["April 2023", "May 2023", "June 2023", "July 2023", "August 2023", "September 2023"]
ax.set_xticks(date_ticks)
ax.set_xticklabels(date_ticks, fontsize=10)

# Set the tick marks and labels for the y-axis
ax.set_yticks(np.arange(len(categories)))
ax.set_yticklabels(list(categories.keys()), fontsize=12)

# Set the gridlines
ax.grid(axis="x", linestyle="--", color="gray")

# Set the title and save the figure
plt.title("Timeline of APT28 Attack", fontsize=16, fontweight="bold")
plt.tight_layout()
plt.savefig("timeline.png")
