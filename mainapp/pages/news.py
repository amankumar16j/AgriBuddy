import http.client
import urllib.parse
import json
import streamlit as st
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO


st.set_page_config(layout="wide")

# Function to fetch news related to farmers and agriculture
def load_image_from_url(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img


URL = "https://www.livemint.com/industry/agriculture"
r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html5lib')
# Find all h2 elements with class 'headline'
cont = soup.find_all("h2", class_="headline")
img_tags = soup.find_all("div",class_="thumbnail")
for news,img in zip(cont,img_tags):
    newslink = news.find('a') 
    link=img.find("img")# Find the anchor tag inside the h2
    img_url=link.get("src")
    
    link = newslink['href']  # Get the href attribute (link)
    text = newslink.text.strip()  # Get the text inside the anchor tag and strip whitespace
    full_link = "https://www.livemint.com" + link 
    
    with st.container(border=True):
    
      cols=st.columns([1,5])
      with cols[0]:
        image = load_image_from_url(img_url)
        st.image(image, width=150)
      
      with cols[1]:
        st.markdown(f'<a href="{full_link}" style="font-size:40px; text-decoration:none;">{text}</a>', unsafe_allow_html=True)
        # st.header(f"{text}")
        # st.write(f"{full_link}\n")


# def fetch_news():
#     conn = http.client.HTTPSConnection('api.thenewsapi.com')

#     # Update the search term to focus on farming and agriculture
#     params = urllib.parse.urlencode({
#         'api_token': 'xhfC0dlBlxEl5P2r8Oi24ogQNFxgPY3EXGJMnM3n',  # Replace with your API token
#         'search': 'farming OR agriculture OR farmer OR crop OR irrigation OR rural OR India OR "Indian farmers" OR "Indian agriculture" OR "government schemes"',  # Search terms for farming and agriculture
#         'language': 'en',  # Filter to get English news
#         'limit': 50,  # Limit the number of articles
#     })

#     conn.request('GET', '/v1/news/all?{}'.format(params))
#     res = conn.getresponse()
#     data = res.read()
#     conn.close()

#     # Decode and parse the response
#     news_data = json.loads(data.decode('utf-8'))
#     return news_data

# # Display the news articles in Streamlit
# def display_news(news_data):
#     st.title("Latest Farmer and Agriculture News")
    
#     # Check if news data contains articles
#     if 'data' in news_data:
#         articles = news_data['data']
        
#         # Loop through articles and display in Streamlit
#         for article in articles:
#             st.subheader(article['title'])
#             st.write(article['description'])
#             st.markdown(f"[Read more]({article['url']})")
#             st.markdown("---")  # Separator between articles
#     else:
#         st.write("No news articles available.")

# # Main Streamlit app function
# def main():
#     # Fetch news data
#     news_data = fetch_news()
    
#     # Display news in Streamlit
#     stx.scrollableTextbox(
#     display_news(news_data))

# if __name__ == "__main__":
#     main()
