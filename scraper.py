from urllib.request import urlopen
from html import unescape
OLDEST = 83 # oldest page number as of August 27th, 2020

# Webpage scraping code
def webscrape(url):
    page = urlopen(url)
    html_bytes = page.read()
    return html_bytes.decode("utf-8")

    

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
while(True):
    page_no = input("Please enter the Smashboards page you want to extract from (1-" + str(old_page) + "): ")
    try:
        page_no = int(page_no)
    except ValueError:
        input("Input not numeric, press enter to try again ")
    else:
        if(1 <= page_no <= old_page):
            break
        else:
            input("Input not between 1 and " + str(old_page) + ", press enter to try again ")

# The first article on Smashboards starts with a <span>
# so extract words between the first <span> and its corresponding </span>
scrape = webscrape("https://smashboards.com/news/page-"+ str(page_no))
max_art = scrape.count("<span>")
print(max_art)
start_index = scrape.find("<span>") + len("<span>")
end_index = scrape.find("</span>", start_index)
first_title = scrape[start_index:end_index]

# Removes tabs, newlines, spaces, and HTML character codes in the extracted string
str_list = first_title.split()
first_title = " ".join(str_list)
print(unescape(first_title))

# To print into a file for checking
# a_file = open("output.txt", "w")
# print(first_title, file = a_file)
# a_file.close()