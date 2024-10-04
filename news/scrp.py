import requests
from bs4 import BeautifulSoup

URL = "https://www.livemint.com/industry/agriculture"
r = requests.get(URL)

soup = BeautifulSoup(r.content, 'html5lib')

# Find all h2 elements with class 'headline'
cont = soup.find_all("h2", class_="headline")

for news in cont:
    newslink = news.find('a')  # Find the anchor tag inside the h2
    if newslink:
        link = newslink['href']  # Get the href attribute (link)
        text = newslink.text.strip()  # Get the text inside the anchor tag and strip whitespace
        full_link = "https://www.livemint.com" + link  # Construct the full link if it's a relative path
        print(f"Text: {text}")
        print(f"Link: {full_link}\n")
