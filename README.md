# SmashboardsArticleScraper
 Personal project to either:  
 1. display the article titles on a given news page of https://smashboards.com and select one of them for reading in a web browser (scraper.py) or  
 2. view the articles of a particular author, listed from most to least viewed, and their total view count (viewer.py)

 An experiment with web scraping technologies in Python using the urllib package.

 ## Branch Descriptions ##  
timer: Corrects for timezones in viewer.py (requires user to install pytz on their machine)

(outdated, only have scraper.py)  
lister: Doesn't list articles  
looper: Allows selection of different page without relaunching

## Installation ##
Only requires installation of pytz to system for timer branch and best performance  
```shell
$ pip install pytz
```