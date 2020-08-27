from urllib.request import urlopen
url = "https://smashboards.com/news/"
page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")
start_index = html.find("<span>") + len("<span>")
print(start_index)
end_index = html.find("</span>",start_index)
print(end_index)
first_title = html[start_index:end_index]
str_list = first_title.split()
first_title = " ".join(str_list)
# a_file = open("output.txt", "w")
print(first_title)# print(html, file=a_file)
# a_file.close()