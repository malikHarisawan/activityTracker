# import matplotlib.pyplot as plt
# from categorization import categorize_apps  # Ensure this import is correct

# # def show_categorized_graph(time_spent, current_date):
# #     """Show a graph of time spent by category."""
# #     if current_date not in time_spent:
# #         raise ValueError("No data available for this date.")

# #     # Categorize time spent data using the imported function
# #     category_data = categorize_apps(time_spent[current_date])

# #     # Create the graph
# #     fig, ax = plt.subplots()

# #     # Assign colors to specific categories
# #     category_colors = {
# #         "Work": "green", 
# #         "Entertainment": "red", 
# #         "Communication": "lightblue", 
# #         "Uncategorized": "gray"
# #     }

# #     categories = list(category_data.keys())
# #     times = list(category_data.values())

# #     # Map each category to its corresponding color
# #     bar_colors = [category_colors.get(category, "gray") for category in categories]

# #     # Create the bar chart with the specific colors
# #     ax.bar(categories, times, color=bar_colors)

# #     ax.set_title("Time Spent by Category")
# #     ax.set_ylabel("Time (seconds)")
# #     ax.set_xlabel("Categories")
# #     ax.grid(axis="y", linestyle="--", alpha=0.7)

# #     return fig
# def show_categorized_graph(time_spent, date, config_file="categories.json"):
#     """
#     Displays a categorized graph of application usage for the given date.
    
#     :param time_spent: Dictionary containing app usage data.
#     :param date: Date string in "yyyy-MM-dd" format.
#     :param config_file: Path to the categorization config file.
#     :return: Matplotlib figure for the categorized graph.
#     """
#     from matplotlib.figure import Figure
    
#     if date not in time_spent:
#         raise ValueError(f"No data available for date {date}")
    
#     category_data = categorize_apps(time_spent[date], config_file=config_file)
    
#     # Create the graph
#     fig = Figure()
#     ax = fig.add_subplot(111)
#     categories = list(category_data.keys())
#     time_spent_values = list(category_data.values())
#     ax.bar(categories, time_spent_values, color="skyblue")
#     ax.set_title(f"Application Usage Categories - {date}")
#     ax.set_xlabel("Categories")
#     ax.set_ylabel("Time Spent (seconds)")
#     ax.tick_params(axis='x', rotation=45)  # Rotate x-axis labels for clarity
    
#     return fig

import matplotlib.pyplot as plt
from categorization import categorize_apps  # Ensure this import is correct

def show_categorized_graph(time_spent, date, config_file="categories.json"):
    """
    Displays a categorized graph of application usage for the given date.
    
    :param time_spent: Dictionary containing app usage data.
    :param date: Date string in "yyyy-MM-dd" format.
    :param config_file: Path to the categorization config file.
    :return: Matplotlib figure for the categorized graph.
    """
    from matplotlib.figure import Figure
    
    if date not in time_spent:
        raise ValueError(f"No data available for date {date}")
    
    # Categorize the data
    category_data = categorize_apps(time_spent[date], config_file=config_file)
    
    # Define category colors
    category_colors = {
        "Development": "lightgreen",
        "Entertainment": "red",
        "Communication": "lightblue",
        "Uncategorized": "gray"
    }
    
    # Assign colors based on categories
    categories = list(category_data.keys())
    time_spent_values = list(category_data.values())
    colors = [category_colors.get(cat, "gray") for cat in categories]  # Default to gray if category not in mapping
    
    # Create the graph
    fig = Figure()
    ax = fig.add_subplot(111)
    bars = ax.bar(categories, time_spent_values, color=colors)
    
    # Graph aesthetics
    ax.set_title(f"Application Usage Categories - {date}")
    ax.set_xlabel("Categories")
    ax.set_ylabel("Time Spent (seconds)")
    ax.tick_params(axis='x', rotation=45)  # Rotate x-axis labels for clarity
    
    return fig
