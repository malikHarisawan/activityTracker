import json
"""
Creates and displays a visualization of application usage data for a specific date.
This function generates two charts:
1. A 3D bar chart showing time spent on different applications
2. A nested pie chart where:
    - Outer ring shows percentage of total time
    - Inner ring shows hours spent
    Both using different color schemes and exploded segments
Parameters:
     date (str): The date to plot data for, in format 'YYYY-MM-DD'
Returns:
     tuple: Contains:
          - matplotlib.figure.Figure: The figure object containing both plots
          - tuple: Contains two axes objects (ax1, ax2) for the 3D bar and nested pie charts
Raises:
     KeyError: If the specified date is not found in the activity data
     FileNotFoundError: If the activity_data.json file is not found
Notes:
     - Reads data from 'activity_data.json' file
     - Times are stored in seconds and converted to hours for the inner pie chart
     - Uses global figure and axes objects to maintain state between calls
     - Both charts include proper labeling, legends, and color coding
"""
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

fig, ax = None, None

def plot_chart(date):
    global fig, ax

    if fig is None or ax is None:
        fig = plt.figure(figsize=(16, 6))
        ax1 = fig.add_subplot(121, projection='3d')
        ax2 = fig.add_subplot(122)  # Changed to 2D for nested pie chart
    else:
        ax1, ax2 = ax

    ax1.clear()
    ax2.clear()

    apps = []
    times = []

    try:
        with open("activity_data.json") as f:
            data = json.load(f)
            if date and date in data:
                day_data = data[date]
                apps = list(day_data.keys())
                times = list(day_data.values())
            else:
                raise KeyError(f"The date {date} does not exist in the data.")
    except (KeyError, FileNotFoundError) as e:
        print(f"Error: {e}")
        apps = ["No Data"]
        times = [0]

    # 3D Bar chart
    x_pos = np.arange(len(apps))
    z_pos = np.zeros_like(x_pos)
    dx = np.ones_like(z_pos) * 0.8
    dy = np.array(times)
    dz = np.ones_like(z_pos) * 0.8

    bars = ax1.bar3d(x_pos, z_pos, z_pos, dx, dy, dz, color='blue', alpha=0.8)
    ax1.set_title("Time Spent on Applications (3D Bar Chart)")
    ax1.set_xlabel("Applications")
    ax1.set_ylabel("Time Spent (seconds)")
    ax1.set_xticks(x_pos + dx/2)
    ax1.set_xticklabels(apps, rotation=45)
    ax1.view_init(elev=20, azim=45)

    # Nested 2D Pie chart
    if sum(times) > 0:
        # Create explode tuple for outer pie (slight separation for all slices)
        explode_outer = tuple(0.05 for _ in range(len(times)))
        
        # Create explode tuple for inner pie (more pronounced separation)
        explode_inner = tuple(0.02 for _ in range(len(times)))

        # Outer pie with enhanced features
        outer_sizes = times
        outer_colors = plt.cm.Set3(np.linspace(0, 1, len(times)))
        wedges, texts, autotexts = ax2.pie(outer_sizes, 
                                          explode=explode_outer,
                                          radius=1,
                                          colors=outer_colors,
                                          autopct='%1.1f%%',
                                          pctdistance=0.85,
                                          shadow=True,
                                          startangle=90,
                                          wedgeprops=dict(width=0.3))
        
        # Inner pie (showing hours instead of percentages)
        hours_spent = [t/3600 for t in times]  # Convert seconds to hours
        inner_colors = plt.cm.Set3(np.linspace(0.2, 0.8, len(times)))
        inner_wedges, inner_texts, inner_autotexts = ax2.pie(hours_spent,
                                                            explode=explode_inner,
                                                            radius=0.7,
                                                            colors=inner_colors,
                                                            autopct=lambda p: f'{p*sum(hours_spent)/100:.1f}h',
                                                            pctdistance=0.75,
                                                            shadow=True,
                                                            startangle=90,
                                                            wedgeprops=dict(width=0.3))
        
        # Enhance text properties
        plt.setp(autotexts, size=8, weight="bold")
        plt.setp(inner_autotexts, size=8, weight="bold")
        
        ax2.set_title("Time Spent on Applications\nOuter: % of Total Time, Inner: Hours Spent")
        
        # Add legend with enhanced styling
        legend_elements = [plt.Rectangle((0,0),1,1, color=c) for c in outer_colors]
        ax2.legend(legend_elements, 
                  apps,
                  title="Applications",
                  loc="center left",
                  bbox_to_anchor=(1, 0.5),
                  shadow=True,
                  fancybox=True)


    plt.tight_layout()
    return fig, (ax1, ax2)


plot_chart("2024-11-29")
plt.show()