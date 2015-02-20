#!/usr/bin/env python3

import json, queue

class JSONReader:
    def __init__(self, json_file):
        self.load_json(json_file)
        self.region = self.data["Personal"]["Region"]
        self.category = self.data["Personal"]["Category"]
        self.keywords = self.data["Keywords"]

    @property
    def keywords(self):
        return self._keywords

    @keywords.setter
    def keywords(self, dict):
        for key, value in dict.items():
            value["posts"] = queue.PriorityQueue()

        self._keywords = dict
        
    def load_json(self, json_file):
        with open(json_file) as file:
            self.data = json.load(file)

    def get_region(self):
        return self.region

    def get_category(self):
        return self.category

    def get_keywords(self):
        return self.keywords
            
