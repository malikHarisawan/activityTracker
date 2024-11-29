import json
import matplotlib.pyplot as plt

fig, ax = None, None

def plot_chart(date):
    global fig, ax

    if fig is None or ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))

    ax.clear()

    titles = []
    times = []

    try:
        with open("activity_data.json") as f:
            data = json.load(f)
            if date in data:
                day_data = data[date]

                for app, title_data in day_data.items():
                    if isinstance(title_data, dict):  # If title_data is a dictionary
                        for title, duration in title_data.items():
                            titles.append(title)  # Use window titles
                            times.append(duration)
                    else:
                        # If it's not a dictionary, just use the app name and duration
                        titles.append(app.strip())  # Strip extra spaces
                        times.append(title_data)
            else:
                raise KeyError(f"The date {date} does not exist in the data.")
    except KeyError as e:
        print(f"Error: {e}")
        titles = ["No Data"]
        times = [0]
    except FileNotFoundError as e:
        print(f"Error: {e}")
        titles = ["No Data"]
        times = [0]

    # Plot the data
    ax.bar(titles, times, color="blue")
    ax.set_title("Time Spent on Applications")
    ax.set_xlabel("Window Titles")
    ax.set_ylabel("Time Spent (seconds)")

    ax.set_xticks(range(len(titles)))
    ax.set_xticklabels(titles, rotation=45, ha='right')

    plt.tight_layout()

    return fig
