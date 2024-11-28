import json
import matplotlib.pyplot as plt

fig, ax = None, None

def plot_chart(date):
    global fig, ax

    if fig is None or ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))

    ax.clear()

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
    except KeyError as e:
        print(f"Error: {e}")
        apps = ["No Data"]
        times = [0]
    except FileNotFoundError as e:
        print(f"Error: {e}")
        apps = ["No Data"]
        times = [0]

    ax.bar(apps, times, color="blue")
    ax.set_title("Time Spent on Applications")
    ax.set_xlabel("Applications")
    ax.set_ylabel("Time Spent (seconds)")

    ax.set_xticks(range(len(apps)))
    ax.set_xticklabels(apps, rotation=45)

    plt.tight_layout()

    return fig