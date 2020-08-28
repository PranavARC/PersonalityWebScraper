from urllib.request import urlopen
from html import unescape
from webbrowser import open
from sys import exit
OLDEST = 83 # oldest page number as of August 27th, 2020

# Webpage scraping code
def webscrape(url):
    page = urlopen(url)
    html_bytes = page.read()
    return html_bytes.decode("utf-8")

# Function to choose between a range of pages/articles
# is_art = "article index you want to check out" or "Smashboards page you want to browse"
def chooser(is_art, high):
    while(True):
        loop = ""
        if(is_art == "article index you want to check out"):
            loop = ", 0 to choose new page" # extra loop text for articles
        select = input("Please enter the " + is_art + " (1-" + str(high) + loop + "): ")
        try:
            select = int(select)
        except ValueError:
            print("Input not numeric, try again\n")
        else:
            if(1 <= select <= high):
                return select
            else:
                if(select == 0 and is_art == "article index you want to check out"):
                    return 0    # article looping
                print("Input not between 1 and " + str(high) + ", try again\n")

# Finding the oldest page number
scrape = webscrape("https://smashboards.com/news")
start_index = scrape.find("min=\"1\" max=\"") + len("min=\"1\" max=\"")
end_index = scrape.find("\"", start_index)
try:
    old_page = int(scrape[start_index:end_index].strip())
except ValueError:
    old_page = OLDEST   # in case oldest page scrape doesn't work

# Loop until user chooses an article to read
while(True):
    # Take a given page number from 1 to old_page and return the first article of that page
    page_no = chooser("Smashboards page you want to browse", old_page)

    # Check the number of articles on that page (usually 20), and list all their titles by looping
    scrape = webscrape("https://smashboards.com/news/page-"+ str(page_no))
    max_art = scrape.count("<span>")
    begin = 0
    i = 1
    while(i <= max_art):
        start_index = scrape.find('<span>', begin) + len("<span>")
        end_index = scrape.find("</span>", start_index)
        art_title = scrape[start_index:end_index]
        # Remove tabs, newlines, spaces, HTML character codes in art_title with split, join, unescape
        str_list = art_title.split()
        art_title = " ".join(str_list)
        begin = end_index
        if("<span class=\"" in art_title):
            continue
        print(str(i) + ": " + unescape(art_title))
        i += 1

    # Take a given article number, move to its title, take its corresponding link, and open it
    art_no = chooser("article index you want to check out", max_art)
    if(art_no == 0):
        print("")
        continue    # Loop if 0 was given
    start_index = scrape.replace('<span>', '777777', art_no-1).find('<span>') + len("<span>")
    start_index = scrape.rfind("<a href=\"", 0, start_index) + len("<a href=\"")
    end_index = scrape.find("\">", start_index)
    open("https://smashboards.com" + scrape[start_index:end_index], new = 0, autoraise = True)
    break