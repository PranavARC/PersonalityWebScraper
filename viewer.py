from urllib.request import urlopen
from html import unescape
from operator import attrgetter
import datetime

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
        return self.title + ": " + str(self.views) + " (" + self.date.strftime("%b %d, %Y") + ")"

# Check the number of articles on that page, and list their titles and view counts by looping
scrape = webscrape("https://smashboards.com/news/authors/arcain.421960/")
max_art = scrape.count("<span>")
begin = 0
total_views = 0
articles = []
last_date = 0

for i in range(1, max_art + 1):
    # Find the title first
    start_index = scrape.find('<span>', begin) + len("<span>")
    end_index = scrape.find("</span>", start_index)
    art_title = scrape[start_index:end_index]
    # Remove whitespace, HTML character codes in art_title with split, join, unescape
    str_list = art_title.split()
    art_title = unescape(" ".join(str_list))
    begin = end_index

    # Find the publication date next
    start_index = scrape.find("datetime=\"", start_index) + len("datetime=\"")
    end_index = scrape.find("\"", start_index) - 5
    date_obj = datetime.datetime.strptime((scrape[start_index:end_index]).replace("T", " "), "%Y-%m-%d %H:%M:%S")
    if(i == 1):
        last_date = date_obj    # Date of the latest article

    # Find the view count last
    start_index = scrape.find("<i class=\"fa--xf far fa-eye\" aria-hidden=\"true\"></i>", begin) + len("<i class=\"fa--xf far fa-eye\" aria-hidden=\"true\"></i>")
    end_index = scrape.find("</li>", start_index)
    view_count = scrape[start_index:end_index]
    # Remove whitespace, commas in view_count with split, join, replace
    str_list = view_count.split()
    view_count = int((" ".join(str_list)).replace(",", ""))
    total_views += view_count
    # begin = end_index # Just in case
    articles.append(article(art_title, view_count, date_obj))    

# Sorting the array by descending view counts and printing
articles.sort(key=attrgetter('views'), reverse=True)
num = 1
for i in articles:
    print(str(num) + ". " + str(i))
    num += 1

# Find days since last article
days_since = ((datetime.datetime.now()) - last_date).days
# To prevent negative days from timezone issues
if(days_since < 0):
    days_since = 0

print("\nTotal views: " + str(total_views))
print("Days since last article: " + str(days_since))
input("")