#!/usr/bin/env python3

import argparse, json, os.path

FILE_NAME = "data.json"

class ShowSettings(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        with open(FILE_NAME, "r") as file:
            print(file.read())

class UpdateDataJson(argparse.Action):
    def update_json(self, update_key, values):
        if not os.path.isfile(FILE_NAME):
            self.create_json_file()

        with open(FILE_NAME, "r") as file:
            data = json.load(file)

        with open(FILE_NAME, "w+") as file:
            dict = data

            if len(values) > 0:
                for value in values:
                    if update_key == "k":
                        dict["Keywords"][value] = { "freq": 0 }
                    elif update_key == "r":
                        dict["Personal"]["Region"] = value
                    elif update_key == "s":
                        dict["Personal"]["Category"] = value
            elif update_key == "rm":
                dict["Keywords"] = {}

            data.update(dict)
            file.write(json.dumps(data, indent=4))

    def create_json_file(self):
        if not os.path.isfile(FILE_NAME):
            data = {
                "Personal": {
                    "Region": "INSERT REGION HERE",
                    "Category": "INSERT SEARCH HERE"
                },
                "Keywords": {}
            }

            with open(FILE_NAME, "w") as file:
                json.dump(data, file)

class AddKeywords(UpdateDataJson):
    def __call__(self, parser, namespace, values, option_string=None):
        self.update_json("k", values)
        print("Keyword(s): " + str(values) + " Added")

class UpdateRegion(UpdateDataJson):
    def __call__(self, parser, namespace, values, option_string=None):
        self.update_json("r", values)
        print("Region Updated To: " + values[0])

class UpdateCategory(UpdateDataJson):
    def __call__(self, parser, namespace, values, option_string=None):
        self.update_json("s", values)
        print("Category Updated To: " + values[0])

class RemoveKeywords(UpdateDataJson):
    def __call__(self, parser, namespace, values, option_string=None):
        self.update_json("rm", values)
        print("All Keywords Removed")

def initArgParse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--add-keywords", action=AddKeywords, nargs='+', help="Add Keyword(s) To Search For")
    parser.add_argument("--update-region", action=UpdateRegion, nargs=1, help="Update Region To Search Through")
    parser.add_argument("--update-category", action=UpdateCategory, nargs=1, help="Update Category To Search Through")
    parser.add_argument("--remove-keywords", action=RemoveKeywords, nargs=0, help="Removes All Keywords")
    parser.add_argument("--settings", action=ShowSettings, nargs=0, help="Displays Current Settings")
    parser.add_argument("-n", "--num-pages", type=int, dest="num_pages", help="Number Of Pages To Search Through");
    return parser.parse_args()
