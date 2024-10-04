import requests
from bs4 import BeautifulSoup
import os

# URL of the website to scrape
url = "https://www.livemint.com/industry/agriculture"

# Send a request to fetch the HTML content
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Create a directory to save the images


# Find all image tags
img_tags = soup.find_all("div",class_="thumbnail")

# Loop through the image tags and download them
for img in img_tags:
    # Get the image URL
    link=img.find("img")
    img_url = link.get("src")

    # Sometimes the src attribute contains relative URLs, so we need to handle them
    print(img_url)

    # Extract the image name

  
