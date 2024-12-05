# category_manager.py
from typing import Dict, Optional

class CategoryManager:
    def __init__(self, categories: Dict):
        self.categories = categories
        self._app_category_map = self._build_app_category_map()


    def _build_app_category_map(self) -> Dict[str, str]:
        app_map = {}
        for category, data in self.categories.items():
            for app in data["apps"]:
                #app_map["Visual Studio Code"] = "WORK"
                app_map[app] = category
        return app_map

    def get_app_category(self, app_name: str) -> str:
        return self._app_category_map.get(app_name, "Miscellaneous")

    def get_category_desc(self, category: str) -> str:
        return self.categories[category]["description"]

    def categorize_data(self, daily_data: Dict) -> Dict:
        categorized = {}
        for app, time in daily_data.items():
            category = self.get_app_category(app)
            if category not in categorized:
                categorized[category] = 0
            categorized[category] += time
        return categorized