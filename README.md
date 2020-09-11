# SmashboardsArticleScraper
 Personal project to either:  
 1. view the articles of a particular author, listed from most to least viewed, and their total view count, while being able to select one of them (viewer.py) or  
 2. display the article titles on a given news page of https://smashboards.com and select one of them for reading in a web browser (scraper.py)

 An experiment with web scraping technologies in Python using the urllib package.

 ## Branch Descriptions ##  
timer: Doesn't require a pytz installation to work (allows small timezone errors)

(outdated, only have scraper.py)  
lister: Doesn't list articles  
looper: Allows selection of different page without relaunching

## Installation ##
Only requires an installation of pytz to system to prevent miscalculations due to timezones
```shell
> pip install pytz
```
