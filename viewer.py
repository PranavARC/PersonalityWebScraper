from urllib.request import urlopen
from html import unescape
from operator import attrgetter

# Webpage scraping code
def webscrape(url):
    page = urlopen(url)
    html_bytes = page.read()
    return html_bytes.decode("utf-8")

# An article class to put objects in an array
class article:
    def __init__(self, title, views, date):
        self.title = title
        self.views = views
        self.date = date
    def __str__(self):
        return self.title + ": " + str(self.views) + " - " + self.date

# Check the number of articles on that page, and list their titles and view counts by looping
scrape = webscrape("https://smashboards.com/news/authors/arcain.421960/")
max_art = scrape.count("<span>")
begin = 0
total_views = 0
articles = []

for i in range(1, max_art + 1):
    # Find the title first
    start_index = scrape.find('<span>', begin) + len("<span>")
    end_index = scrape.find("</span>", start_index)
    art_title = scrape[start_index:end_index]
    # Remove whitespace, HTML character codes in art_title with split, join, unescape
    str_list = art_title.split()
    art_title = unescape(" ".join(str_list))
    begin = end_index

    # Find the publication date last
    start_index = scrape.find("data-date-string=\"", start_index) + len("data-date-string=\"")
    end_index = scrape.find("\"", start_index)
    pub_date = scrape[start_index:end_index]

    # Find the view count next
    start_index = scrape.find("<i class=\"fa--xf far fa-eye\" aria-hidden=\"true\"></i>", begin) + len("<i class=\"fa--xf far fa-eye\" aria-hidden=\"true\"></i>")
    end_index = scrape.find("</li>", start_index)
    view_count = scrape[start_index:end_index]
    # Remove whitespace, commas in view_count with split, join, replace
    str_list = view_count.split()
    view_count = int((" ".join(str_list)).replace(",", ""))
    total_views += view_count
    # begin = end_index # in case
    articles.append(article(art_title, view_count, pub_date))    

# Sorting the array by descending view counts and printing
articles.sort(key=attrgetter('views'), reverse=True)
num = 1
for i in articles:
    print(str(num) + ". " + str(i))
    num += 1

input("Total views: " + str(total_views))