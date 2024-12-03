
# import json
# from collections import defaultdict

# def load_category_mappings(config_file="categories.json"):
#     """Loads category mappings from a JSON config file."""
#     with open(config_file, "r") as f:
#         config = json.load(f)
#     return config["exe_to_category"], config["title_to_category"]

# def categorize_apps(time_spent_data, config_file="categories.json"):
#     """Categorizes the applications based on the given time_spent data."""
    
#     # Load category mappings from config
#     exe_to_category, title_to_category = load_category_mappings(config_file)
    
#     # Normalize application names and titles
#     normalized_data = defaultdict(float)
#     for exe_name, titles in time_spent_data.items():
#         if isinstance(titles, dict):
#             # Process the case where titles is a dictionary (window title -> time_spent)
#             for title, time_spent in titles.items():
#                 # First try to categorize by title
#                 category = title_to_category.get(title, None)
#                 if not category:
#                     # If no category is found by title, fall back to exe-based categorization
#                     category = exe_to_category.get(exe_name.strip(), "Uncategorized")
#                 normalized_data[category] += time_spent
#         elif isinstance(titles, (int, float)):
#             # Process the case where titles is a float (time spent)
#             category = exe_to_category.get(exe_name.strip(), "Uncategorized")
#             normalized_data[category] += titles

#     return normalized_data
import json
from collections import defaultdict

def load_category_mappings(config_file="categories.json"):
    """Loads category mappings from a JSON config file."""
    with open(config_file, "r") as f:
        config = json.load(f)
    return config.get("exe_to_category", {}), config.get("title_to_category", {})

def categorize_apps(time_spent_data, config_file="categories.json"):
    """Categorizes the applications based on the given time_spent data."""
    exe_to_category, title_to_category = load_category_mappings(config_file)
    
    # Categorize data
    categorized_data = defaultdict(float)
    for app_title, time_spent in time_spent_data.items():
        # Match by title
        matched_title = next(
            (key for key in title_to_category if key in app_title), None
        )
        category = title_to_category.get(matched_title, None)
        
        # Fallback to exe categorization (if no match by title)
        if not category:
            exe_name = app_title.split()[0]  # Assume the first word is the exe
            category = exe_to_category.get(exe_name, "Uncategorized")
        
        categorized_data[category] += time_spent

    return categorized_data
