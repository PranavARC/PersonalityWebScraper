from urllib.request import urlopen
from html import unescape
from operator import attrgetter
from difflib import SequenceMatcher
from time import sleep
from webbrowser import open
import datetime
try:
    import pytz
except ModuleNotFoundError:
    pass

# Webpage scraping code
def webscrape(url):
    page = urlopen(url)
    html_bytes = page.read()
    return html_bytes.decode("utf-8")

# Article and author classes to create arrays of them
class article:
    def __init__(self, title, views, date, age):
        self.title = title
        self.views = views
        self.date = date
        self.age = age
    def __str__(self):
        return self.title + ": " + str(self.views) + " (" + self.date.strftime("%b %d, %Y") + ")"

class author:
    def __init__(self, num, name, tag, link):
        self.num = num
        self.name = name
        self.tag = tag
        self.link = link
    def __str__(self):
        return str(self.num) + ": " + self.name

# Searching the author's page for every Smashboards writer
magic_str = """<div class=\"porta-author-name\">
								<a href=\"/news/authors/"""
num_str = ""
scrape = webscrape("https://smashboards.com/news/authors")
max_auth = scrape.count(magic_str)
authors = []
begin = 0

# Putting every author(their number, name, gamertag if given, and link) in an array
# start_index to mid_index is their link, mid_index to end_index is their name
for i in range(1, max_auth + 1):
    start_index = scrape.find(magic_str , begin) + len(magic_str)
    mid_index = scrape.find("/\">", start_index)
    link = scrape[start_index:mid_index]
    mid_index += 3  # \"> is 3 characters
    end_index = scrape.find("</a>", mid_index)
    name = scrape[mid_index:end_index]

    # Remove whitespace, HTML character codes in art_title with split, join, unescape
    str_list = name.split()
    name = unescape(" ".join(str_list))
    
    # If the name has 2 quotes, the author has a gamertag, else leave it blank
    tag = ""
    if(name.count("\"") == 2):
        t_start = name.find("\"") + 1
        t_end = name.find("\"", t_start)
        tag = name[t_start:t_end]
    authors.append(author(i, name, tag, link))
    begin = end_index

# An infinite loop until the user can provide the author they want to check out
while(True):
    choice = input("Enter the " + num_str + "name/tag of the author you wish to check out, or enter \"list\" to see a list of them: ")
    if(choice.isnumeric()):
        if(num_str == ""):  # This should only work once the authors have been listed
            print("Invalid entry, try again")
            sleep(0.5)
        
        else:   # If the number is between 1 and 73, author has been found
            if(1 <= int(choice) <= max_auth):
                num_str = authors[int(choice) - 1].link
                break
            else:
                print("Invalid number, try again")                
                sleep(0.5)

    elif(choice.lower() == "list"): # List out every author
        for i in authors:
            print(i)
        num_str = "number or "  # Change this to show that authors have been listed
    
    else:   # A name was provided
        if(choice == ""):   # An empty name might match with an empty gamertag, so reject it
            print("Invalid entry, try again")
            sleep(0.5)
            continue

        for i in authors:   # Check the entire authors array for a match
            s1 = choice.lower()
            s2 = i.name.lower()
            s3 = i.tag.lower()
            match = ""
            if(s1 == s2 or s1 == s3):   # If an exact match occurs with name or gamertag, author has been found 
                num_str = i.link
                break

            # SequenceMatcher lets you check if the names typed in were close to correct
            elif(SequenceMatcher(a=s1,b=s2).ratio() >= 0.7):    # name
                match = i.name
            elif(SequenceMatcher(a=s1,b=s3).ratio() >= 0.7):    # tag
                match = i.tag
            else:   # Neither the tag or name were close matches, so move on to the rest of the array
                continue

            choice = input("Did you mean " + match + " (Y/N)? ")
            if(choice.isalpha() and (str(choice)).upper() == 'Y'):  # If Y, author has been found
                num_str = i.link
                break

        # if num_str is still "", no author has been found, so redo the loop
        if(num_str == ""):
            print("Invalid entry, try again")
            sleep(0.5)
        else:
            break

print("")

# Check the number of articles on that page, and list their titles and view counts by looping
scrape = webscrape("https://smashboards.com/news/authors/" + num_str)
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
    articles.append(article(art_title, view_count, date_obj, i))    

# Sorting the array by descending view counts and printing
articles.sort(key=attrgetter('views'), reverse=True)
num = 1
for i in articles:
    print(str(num) + ". " + str(i))
    if(i.age == 1):
        newest = str(num)
    num += 1

# astimezone causes an error if last_date is still 0
if(last_date == 0):
    print("They haven't written any articles yet")
    sleep(2)
    exit(0)

# Use of pytz library to sync timezones (SmashBoards runs on PST)
try:
    pst = pytz.timezone('Europe/Berlin')
    last_date = last_date.astimezone(pst)
except NameError:
    current = datetime.datetime.now()
else:
    current = datetime.datetime.now(pst)

# Find days since last article
days_since = ((current) - last_date).days
# To prevent negative days from timezone issues
if(days_since < 0):
    days_since = 0

print("\nTotal views: " + str(total_views))
print("Days since last article: " + str(days_since) + " (" + newest + ")")

try:
    art_no = int(input("Enter an article number if you wish to read it, or anything else to exit: "))
except ValueError:
    exit(0)
if(1 <= art_no <= len(articles)):
    true_no = articles[art_no - 1].age
    start_index = scrape.replace('<span>', '777777', true_no-1).find('<span>') + len("<span>")
    start_index = scrape.rfind("<a href=\"", 0, start_index) + len("<a href=\"")
    end_index = scrape.find("\">", start_index)
    open("https://smashboards.com" + scrape[start_index:end_index], new = 0, autoraise = True)