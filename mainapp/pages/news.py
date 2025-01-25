import http.client
import urllib.parse
import json
import streamlit as st
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from streamlit_lottie import st_lottie


st.set_page_config(layout="wide")

# Function to fetch news related to farmers and agriculture
def load_image_from_url(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json() 
  
col3=st.columns([1,4])
with col3[0]:
      link="https://lottie.host/e38e30a2-e829-4928-b271-e4b3f3569fb3/BK67yUyrvM.json"
      l=load_lottieurl(link)
      st.lottie(l,height=130,width=300)
with col3[1]:
    st.markdown("""
                <h1 style='font-size: 60px;'>
                    NEWS
                </h1>
                <hr style='border: 2px solid white;'>
                
                """, unsafe_allow_html=True)


URL = "https://www.livemint.com/industry/agriculture"
r = requests.get(URL)
# soup = BeautifulSoup(r.content, 'html5lib')
soup = BeautifulSoup(r.content,  "html.parser")
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

