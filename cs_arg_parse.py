#!/usr/bin/env python3

import argparse, json, os.path

FILE_NAME = "keywords.json"

class AddKeyword(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not os.path.isfile(FILE_NAME):
            self.create_json_file()

        with open(FILE_NAME, "r") as file:
            data = json.load(file)

        with open(FILE_NAME, "w+") as file:
            dict = {}
            for value in values:
                dict[value] = { "freq": 0 }

            data.update(dict)
            file.write(json.dumps(data, indent=4, sort_keys=True))
    
    def create_json_file(self):
        if not os.path.isfile(FILE_NAME):
            with open(FILE_NAME, "w") as file:
                file.write("{\n}")

class ShowKeywords(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        with open("keywords.json", "r") as file:
            print(file.read())

def initArgParse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--add-keyword", action=AddKeyword, nargs='+')
    parser.add_argument("--keywords", action=ShowKeywords, nargs=0)
    return parser.parse_args()
