#!/usr/bin/env python3

import sys, time, re, queue, threading, requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import namedtuple

Post = namedtuple("Post", ["title", "url_ext"])

class CraigsList:
    def __init__(self, city="sandiego"):
        self.city = city
        self.base_url = "https://" + self.city + ".craigslist.org/"

    def query(self, search="sof"):
        html = requests.get("http://sandiego.craigslist.org/search/sof?sort=rel").text
 #       html = urlopen("http://sandiego.craigslist.org/search/sof?sort=rel").read()
        soup = BeautifulSoup(html)
        return [a.attrs.get('href') for a in soup.select('div.content a[href*html]')]

    def get_page_data(self):
        self.keywords = {
            "Java": {
                "freq": 0,
                "posts": queue.Queue()
            },
        }
        
        threads = [threading.Thread(target=self.fetch_data, args=(url, self.keywords)) for url in self.query()]

        for t in threads:
            t.start()

        for t in threads:
            t.join()
        
        print(self)

    def fetch_data(self, url, keywords):
        html = requests.get(self.base_url + url).text
        #html = urlopen(self.base_url + url).read()
        print("Scraping %s words from %s" % (len(html), url))
        soup = BeautifulSoup(html)

        if soup.body.find(text=re.compile("Python")):
            keywords["Java"]["freq"] += 1
            keywords["Java"]["posts"].put(Post(soup.title.string, url))

    def __str__(self):
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
    a = c.query()
    c.get_page_data()
    end = time.time()
    print("Runtime: %d Seconds" % (end - start))
