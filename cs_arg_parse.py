#!/usr/bin/env python3

import argparse, json, os.path

FILE_NAME = "data.json"

class ShowKeywords(argparse.Action):
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
                        dict["Personal"]["Search"] = value
            elif update_key == "rm":
                dict["Keywords"] = {}

            data.update(dict)
            file.write(json.dumps(data, indent=4))

    def create_json_file(self):
        if not os.path.isfile(FILE_NAME):
            with open(FILE_NAME, "w") as file:
                file.write("{\n\t\"Personal\": {\n\t\t\"Region\": \"INSERT REGION HERE\",\n\t\t\"Search\": \"INSERT SEARCH HERE\"\n\t},\n\t\"Keywords\": {\n\t}\n}")

class AddKeyword(UpdateDataJson):
    def __call__(self, parser, namespace, values, option_string=None):
        self.update_json("k", values)

class UpdateRegion(UpdateDataJson):
    def __call__(self, parser, namespace, values, option_string=None):
        self.update_json("r", values)

class UpdateSearch(UpdateDataJson):
    def __call__(self, parser, namespace, values, option_string=None):
        self.update_json("s", values)

class RemoveKeywords(UpdateDataJson):
    def __call__(self, parser, namespace, values, option_string=None):
        self.update_json("rm", values)

def initArgParse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--add-keyword", action=AddKeyword, nargs='+')
    parser.add_argument("--update-region", action=UpdateRegion, nargs=1)
    parser.add_argument("--update-search", action=UpdateSearch, nargs=1)
    parser.add_argument("--remove-keywords", action=RemoveKeywords, nargs=0)
    parser.add_argument("--keywords", action=ShowKeywords, nargs=0)
    return parser.parse_args()
