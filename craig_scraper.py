#!/usr/bin/env python3

import sys, time, re, queue, threading, requests, json, argparse
from bs4 import BeautifulSoup
from collections import namedtuple
from cs_arg_parse import initArgParse
from JSONReader import JSONReader

# Post Tuple containing a post's Title and Url Extension
Post = namedtuple("Post", ["title", "url_ext"])

class CraigsList:
    def __init__(self, region, search, keywords):
        self.base_url = "https://" + region + ".craigslist.org/"
        self.search = search
        self.keywords = keywords
        self.pageNumber = 0

    def get_urls(self):
        """Gets and returns all the url extension for each post"""
        html = requests.get("%ssearch/%s?s=%s&sort=rel" % (self.base_url, self.search, str(self.pageNumber))).text
        soup = BeautifulSoup(html)

        return [a.attrs.get('href') for a in soup.select('div.content a.hdrlnk')]

    def begin_queries(self, numOfPages=1):
        for i in range(0, numOfPages):
            self.pageNumber = (i * 100)
            print("Loading Page %s" % (str(i + 1)))
            self.query()

    def query(self):
        """Creates a thread for each post to retrieve the data and then prints the overall data"""

        # Start a thread for each post and then join them into the main thread
        threads = [threading.Thread(target=self.collect_data, args=(url, self.keywords)) for url in self.get_urls()]
    
        for t in threads:
            t.start()

        for t in threads:
            t.join()

    def collect_data(self, url, keywords):
        """Determines if any of the search keywords appear in the post, if so it will increment the keyword's freq and enqueue a Post tuple"""
        if "http" in url:
            html = requests.get(url).text
        else:
            html = requests.get(self.base_url + url).text

        print("Scanning %s Words From %s" % (len(html), url))
        soup = BeautifulSoup(html)

        compile_search = []
        for key in keywords:
            compile_search.append(re.escape(key))

        find = soup.body.find_all(text=re.compile("|".join(compile_search), re.IGNORECASE))

        if find:
            for key, value in keywords.items():
                for line in find:
                    if key.lower() in line.lower():
                        value["freq"] += 1
                        value["posts"].put(Post(soup.title.string, url))
                        break

    
    
    def __str__(self):
        """
        Prints all the data
        Base Url, Number of Results, and All the Results with their Title and Url Extension
        """
        output = []

        dashes = "-" * 95
        output.append(dashes)

        output.append("\n\n\033[1mBase Url: %s\033[0m\n" % (self.base_url))

        searches = []
        [searches.append(key) for key, value in self.keywords.items()]
        output.append("Searches: %s" % (", ".join(searches)))

        for key, value in self.keywords.items():
            output.append("\n %s Results (%d)" % (key, value["freq"]))
            output.append(dashes)
            while not value["posts"].empty():
                q = value["posts"].get()
                output.append("%-70s %s" % (q.title, q.url_ext))
            output.append(dashes)

        return "\n".join(output)

if __name__ == "__main__":
    start = time.time()
    p = initArgParse()

    if len(sys.argv) < 2 or p.num_pages:
        j = JSONReader("data.json")
        c = CraigsList(j.get_region(), j.get_category(), j.get_keywords())

        if p.num_pages:
            c.begin_queries(int(p.num_pages))
        else:
            c.begin_queries()

        print(c)

    end = time.time()
    print("Runtime: %f Seconds" % (end - start))
