#!/usr/bin/env python3

import sys, time, re, queue, threading, requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import namedtuple

# Post Tuple containing a post's Title and Url Extension
Post = namedtuple("Post", ["title", "url_ext"])

class CraigsList:
    def __init__(self, city="sandiego"):
        self.city = city
        self.base_url = "https://" + self.city + ".craigslist.org/"

    def get_urls(self, search="sof"):
        """Gets and returns all the url extension for each post"""
        html = requests.get("http://sandiego.craigslist.org/search/%s?sort=rel" % search).text
        soup = BeautifulSoup(html)
        return [a.attrs.get('href') for a in soup.select('div.content a[href*html]')]

    def query(self):
        """Creates a thread for each post to retrieve the data and then prints the overall data"""
        self.keywords = {
            "Java": {
                "freq": 0,
                "posts": queue.PriorityQueue()
            },
        }

        # Start a thread for each post and then join them into the main thread
        threads = [threading.Thread(target=self.collect_data, args=(url, self.keywords)) for url in self.get_urls()]

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        print(self)

    def collect_data(self, url, keywords):
        """Determines if any of the search keywords appear in the post, if so it will increment the keyword's freq and enqueue a Post tuple"""
        html = requests.get(self.base_url + url).text
        #html = urlopen(self.base_url + url).read()
        print("Scraping %s words from %s" % (len(html), url))
        soup = BeautifulSoup(html)

        if soup.body.find(text=re.compile("Java")):
            keywords["Java"]["freq"] += 1
            keywords["Java"]["posts"].put(Post(soup.title.string, url))

    def __str__(self):
        """
        Prints all the data
        Base Url, Number of Results, and All the Results with their Title and Url Extension
        """
        output = []

        dash = []
        [dash.append("-") for x in range(1, 50)]
        output.append("".join(dash))

        output.append("\n\n\033[1mBase Url: %s\033[0m\n" % (self.base_url))

        searches = []
        [searches.append(key) for key, value in self.keywords.items()]
        output.append("Searches: %s" % (", ".join(searches)))

        output.append("\nNumber of Results: %s" % (self.keywords["Java"]["freq"]))

        while not self.keywords["Java"]["posts"].empty():
            q = self.keywords["Java"]["posts"].get()
            output.append("{:<70} {:<40}".format(q.title, q.url_ext))

        return "\n".join(output)

if __name__ == "__main__":
    start = time.time()
    c = CraigsList()
    c.query()
    end = time.time()
    print("Runtime: %f Seconds" % (end - start))
