# time_tracker.py
import json
import time

class TimeTracker:
    def __init__(self):
        self.time_spent = {}
        self.last_switch_time = time.time()
        self.last_app = None
        self.last_date = None
        self.load_data()

    def update_time_spent(self, time_diff, app, category, date, hour=None):
        if date not in self.time_spent:
            self.time_spent[date] = {"apps": {}, "categories": {}, "hourly": {}}
        
        if app not in self.time_spent[date]["apps"]:
            self.time_spent[date]["apps"][app] = 0
        self.time_spent[date]["apps"][app] += time_diff
        
        if category not in self.time_spent[date]["categories"]:
            self.time_spent[date]["categories"][category] = 0
        self.time_spent[date]["categories"][category] += time_diff
        
        if hour is not None:
            if hour not in self.time_spent[date]["hourly"]:
                self.time_spent[date]["hourly"][hour] = {"apps": {}, "categories": {}}
            
            if app not in self.time_spent[date]["hourly"][hour]["apps"]:
                self.time_spent[date]["hourly"][hour]["apps"][app] = 0
            self.time_spent[date]["hourly"][hour]["apps"][app] += time_diff
            
            if category not in self.time_spent[date]["hourly"][hour]["categories"]:
                self.time_spent[date]["hourly"][hour]["categories"][category] = 0
            self.time_spent[date]["hourly"][hour]["categories"][category] += time_diff

    def load_data(self):
        try:
            with open("activity_data.json", "r") as file:
                self.time_spent = json.load(file)
        except FileNotFoundError:
            self.time_spent = {}

    def save_data(self):
        with open("activity_data.json", "w") as file:
            json.dump(self.time_spent, file, indent=4)