# Modules
- BeautifulSoup
- Queue
- Requests

# How To Set Up
1. Set up [python virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)
2. Pull this repository by running the command ```git clone https://github.com/Aadeshp/craig_scraper.git```
3. Change directories in the folder
4. Run the command ```pip install -r requirements.txt```
5. Run the command ```python craig_scraper --update-region [REGION ABBREV. HERE] --update-search [SEARCH ABBREV. HERE]```
6. To add the keywords you want the script to search for, run the command ```python craig_scraper --add-keyword [LIST OF KEYWORDS HERE (Separated By Spaces)]```
7. Run the script using the command ```python craig_scraper```
8. The results output will be separated by keyword

# Optional Arguments
- --update-search [SEARCH ABBREV. HERE]
- --update-region [REGION ABBREV. HERE]
- --add-keyword [LIST OF KEYWORDS HERE (Separated By Spaces)]
- --remove-keywords (This requires no arguments, but it will remove all keywords in the .json file)

# Example
```
$ python craig_scraper --update-region cnj --update-search jjj
$ python craig_scraper --add-keyword Java Python Ruby Bash C++
$ python craig_scraper
```
-----OUTPUT-----
=======
# craig_scraper
>>>>>>> 89df99233be757036c6119c6874f6ab73190874e
