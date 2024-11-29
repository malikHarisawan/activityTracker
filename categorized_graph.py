import matplotlib.pyplot as plt
from categorization import categorize_apps  # Ensure this import is correct

def show_categorized_graph(time_spent, current_date):
    """Show a graph of time spent by category."""
    if current_date not in time_spent:
        raise ValueError("No data available for this date.")

    # Categorize time spent data using the imported function
    category_data = categorize_apps(time_spent[current_date])

    # Create the graph
    fig, ax = plt.subplots()

    # Assign colors to specific categories
    category_colors = {
        "Work": "green", 
        "Entertainment": "red", 
        "Communication": "lightblue", 
        "Uncategorized": "gray"
    }

    categories = list(category_data.keys())
    times = list(category_data.values())

    # Map each category to its corresponding color
    bar_colors = [category_colors.get(category, "gray") for category in categories]

    # Create the bar chart with the specific colors
    ax.bar(categories, times, color=bar_colors)

    ax.set_title("Time Spent by Category")
    ax.set_ylabel("Time (seconds)")
    ax.set_xlabel("Categories")
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    return fig
