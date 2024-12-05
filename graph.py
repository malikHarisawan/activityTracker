import json
from pathlib import Path

import matplotlib.pyplot as plt

APP_CATEGORIES = {
    "Software Development": {"color": "#2E7D32"},   # Green
    "Reference & Learning": {"color": "#1976D2"},   # Blue
    "Communication": {"color": "#C62828"}, # Red
    "Utility": {"color": "#F9A825"},      # Yellow
    "Miscellaneous": {"color": "#757575"}  # Grey
}

def get_data_for_date(date):
    """Load data for specific date from activity_data.json"""
    try:
        json_path = Path('activity_data.json')
        if not json_path.exists():
            raise FileNotFoundError
            
        with open(json_path, 'r') as f:
            data = json.load(f)
            
        if date not in data:
            return {}
            
        return data[date]
            
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def handle_empty_data(fig, ax1):
    """Handle the case when there is no data to display"""
    ax1.text(0.5, 0.5, 'No data available', horizontalalignment='center', verticalalignment='center', transform=ax1.transAxes)
    #ax2.text(0.5, 0.5, 'No data available', horizontalalignment='center', verticalalignment='center', transform=ax2.transAxes)
    plt.tight_layout()
    return fig, (ax1)
def plot_chart(date):
    """Create horizontal bar, vertical bar, and pie charts for category usage on a given date"""
    fig, (ax2, ax3, ax1) = plt.subplots(1, 3, figsize=(20, 6))
    
    # Load data
    data = get_data_for_date(date)
    if not data or "categories" not in data:
        return handle_empty_data(fig, ax1)

    # Extract categories and times
    categories = list(data["categories"].keys())
    times = list(data["categories"].values())
    colors = [
        APP_CATEGORIES.get(cat, APP_CATEGORIES["Miscellaneous"])["color"]
        for cat in categories
    ]

    total_time = sum(times)
    percentages = [(time / total_time) * 100 for time in times]

    ax2.bar(categories, percentages, color=colors)
    ax2.set_title("Category")
    ax2.set_xlabel("Categories")
    ax2.set_ylabel("Percentage (%)")
    ax2.tick_params(axis='x', rotation=45)
  
    for i, v in enumerate(percentages):
        ax2.text(i, v + 1, f"{v:.1f}%", ha='center')


    ax3.pie(times, labels=categories, colors=colors, autopct='%1.1f%%')
    ax3.set_title("Category Distribution")

    ax1.barh(categories, percentages, color=colors)
    ax1.set_title("Time Spent by Category")
    ax1.set_xlabel("Categories")
    ax1.set_ylabel("Percentage (%)")
    ax1.invert_yaxis()  # Largest on top
    for i, v in enumerate(percentages):
        ax1.text(v + 1, i, f"{v:.1f}%", va='center')
    
    plt.tight_layout()
    return fig, (ax2, ax3, ax1)
