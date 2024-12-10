import json
from pathlib import Path
from datetime import datetime

import matplotlib.pyplot as plt

APP_CATEGORIES = {
    "Software Development": {"color": "#2E7D32"},   # Green
    "Reference & Learning": {"color": "#1976D2"},   # Blue
    "Communication": {"color": "#C62828"}, # Red
    "Utilities": {"color": "#F9A825"},      # Yellow
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

def handle_empty_data(fig, ax3):
    """Handle the case when there is no data to display"""
    ax3.text(0.5, 0.5, 'No data available', horizontalalignment='center', verticalalignment='center', transform=ax3.transAxes)
    #ax2.text(0.5, 0.5, 'No data available', horizontalalignment='center', verticalalignment='center', transform=ax2.transAxes)
    plt.tight_layout()
    return fig, (ax3)




def plot_chart(date):
    fig, (ax2, ax3, ax1) = plt.subplots(1, 3, figsize=(20, 6))  # Added ax4 for hourly chart

    # Load data
    data = get_data_for_date(date)
    if not data or "categories" not in data:
        return handle_empty_data(fig, ax3)

    categories = list(data["categories"].keys())
    
    times = list(data["categories"].values())
    colors = [
        APP_CATEGORIES.get(cat, APP_CATEGORIES["Miscellaneous"])["color"]
        for cat in categories
    ]
    total_time = sum(times)
    percentages = [(time / total_time) * 100 for time in times]

    # Horizontal bar chart
    ax1.barh(categories, percentages, color=colors)
    ax1.set_title("Time Spent by Category")
    ax1.set_xlabel("Percentage (%)")
    ax1.invert_yaxis()  # Largest on top
    for i, v in enumerate(percentages):
        ax1.text(v + 1, i, f"{v:.1f}%", va='center')

    
    explode = tuple(0.1 if i == 1 else 0 for i in range(len(categories))) 
   
    ax3.pie(times, explode=explode, labels=None, autopct='%1.1f%%',
       shadow=True, startangle=90,colors = colors)
    ax3.set_title("Category Distribution")
   

  
    hourly_data = data.get("hourly", {})
    if hourly_data:
        hours = sorted(hourly_data.keys(), key=lambda h: datetime.strptime(h, '%H:%M'))
        hours_display = hours  

        category_times = {
            cat: [hourly_data.get(hour, {}).get("categories", {}).get(cat, 0) / 60 for hour in hours]
            for cat in APP_CATEGORIES.keys()
        }

        bottom = [0] * len(hours)
        for category, times in category_times.items():
            if any(times):
                ax2.bar(hours_display, times, bottom=bottom, label=category, color=APP_CATEGORIES[category]["color"])
                bottom = [b + t for b, t in zip(bottom, times)]

        ax2.set_title("Hourly Category Usage")
        ax2.set_xlabel("Hour of Day")
        ax2.set_ylabel("Time Spent (Minutes)")
        ax2.legend(title="Categories", bbox_to_anchor=(1.05, 1), loc='upper left')
        ax2.tick_params(axis='x', rotation=45)


    plt.tight_layout()
    return fig, ( ax3, ax1, ax2)
