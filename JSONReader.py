#!/usr/bin/env python3

import json, queue

class JSONReader:
    def __init__(self, json_file):
        self.load_json(json_file)
        self.region = self.data["Personal"]["Region"]
        self.search = self.data["Personal"]["Search"]
        self.keywords = self.data["Keywords"]

        for key, value in self.keywords.items():
            value["posts"] = queue.PriorityQueue()
        
    def load_json(self, json_file):
        with open(json_file) as file:
            self.data = json.load(file)

    def get_region(self):
        return self.region

    def get_search(self):
        return self.search

    def get_keywords(self):
        return self.keywords
            
