from urllib.request import urlopen

# Take a given page number (1-83) and return the first article of that page
while(True):
    page_no = input("Please enter the page you want to extract from (1-83): ")
    try:
        page_no = int(page_no)
    except ValueError:
        print("Input not numeric, please try again")
    else:
        if(1 <= page_no <= 83):
            break
        else:
            print("Input not between 1 and 83, please try again")

# Starter code
url = "https://smashboards.com/news/page-" + str(page_no)
page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")

# The first article on Smashboards starts with a <span>
# so extract words between first <span> and its </span> (not first </span>)
start_index = html.find("<span>") + len("<span>")
end_index = html.find("</span>", start_index)
first_title = html[start_index:end_index]

# Removes tabs, newlines, and spaces in the extracted string
str_list = first_title.split()
first_title = " ".join(str_list)
print(first_title) 

# To print into a file for checking
# a_file = open("output.txt", "w")
# print(first_title, file = a_file)
# a_file.close()