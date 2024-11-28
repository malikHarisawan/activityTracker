import json
import matplotlib.pyplot as plt

fig, ax = None, None
def plot_chart():
    global fig, ax

    if fig is None or ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))

    ax.clear()

    with open('activity_data.json') as f:
        data = json.load(f)
    
    app_names = [app for app, total_time in data.items()]
    time_spent = [total_time for app, total_time in data.items()]

    # Create the bar plot
    bars = ax.bar(app_names, time_spent, color='blue')
    ax.set_title("Time Spent on Applications")
    ax.set_xlabel("Applications")
    ax.set_ylabel("Time Spent (seconds)")

    # Set the tick labels
    ax.set_xticks(range(len(app_names)))  # Set the ticks to be at the correct positions
    ax.set_xticklabels(app_names, rotation=45)  # Set the tick labels

    plt.tight_layout()

    return fig
