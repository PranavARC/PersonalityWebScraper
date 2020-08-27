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
        select = input("Please enter the " + is_art + " (1-" + str(high) + "): ")
        try:
            select = int(select)
        except ValueError:
            input("Input not numeric, press enter to try again ")
        else:
            if(1 <= select <= high):
                return select
            else:
                input("Input not between 1 and " + str(high) + ", press enter to try again ")

# Finding the oldest page number
scrape = webscrape("https://smashboards.com/news")
start_index = scrape.find("min=\"1\" max=\"") + len("min=\"1\" max=\"")
end_index = scrape.find("\"", start_index)
try:
    old_page = int(scrape[start_index:end_index].strip())
except ValueError:
    # print("Oldest page is " + str(OLDEST))
    old_page = OLDEST   # in case oldest page scrape doesn't work

# Take a given page number from 1 to old_page and return the first article of that page
page_no = chooser("Smashboards page you want to browse", old_page)

# Check the number of articles on that page (usually 20 for every page but the last)
scrape = webscrape("https://smashboards.com/news/page-"+ str(page_no))
max_art = scrape.count("<span>")
art_no = chooser("article index you want to check out", max_art)

# Way to dynamically choose the (n-1)th index. WARNING: Corrupts the original scrape
start_index = scrape.replace('<span>', '777777', art_no-1).find('<span>') + len("<span>")
end_index = scrape.find("</span>", start_index)
art_title = scrape[start_index:end_index]

# Removes tabs, newlines, spaces, and HTML character codes in the extracted string
str_list = art_title.split()
art_title = " ".join(str_list)
print("The article's title is: " + unescape(art_title))

# Open a webbrowser to the scraped article link if chosen
choice = input("Do you want to read it? (Y/N): ")
if(choice != 'Y' and choice != 'y'):
    exit(0)
start_index = scrape.rfind("<a href=\"", 0, start_index) + len("<a href=\"")
end_index = scrape.find("\">", start_index)
open("https://smashboards.com" + scrape[start_index:end_index], new=0, autoraise=True)

# To print into a file for checking
# a_file = open("output.txt", "w")
# print(first_title, file = a_file)
# a_file.close()