import http.client
import urllib.parse
import json
import streamlit as st

# Custom CSS for scrollable container
scrollable_style = """
    <style>
    .scrollable-container {
        height: 400px;  /* Set the height of the scrollable section */
        overflow-y: auto;
        border: 1px solid #ccc;
        padding: 10px;
    }
    </style>
"""

# Function to fetch news related to farmers and agriculture
def fetch_news(language):
    conn = http.client.HTTPSConnection('api.thenewsapi.com')

    # Updated search terms to include India-related keywords
    params = urllib.parse.urlencode({
        'api_token': 'xhfC0dlBlxEl5P2r8Oi24ogQNFxgPY3EXGJMnM3n',  # Replace with your API token
        'search': 'farming OR agriculture OR farmer OR crop OR irrigation OR rural OR India OR "Indian farmers" OR "Indian agriculture" OR "government schemes"',
        'language': language,  # Specify language ('en' for English, 'hi' for Hindi)
        'limit': 50,  # Limit the number of articles
    })

    conn.request('GET', '/v1/news/all?{}'.format(params))
    res = conn.getresponse()
    data = res.read()
    conn.close()

    # Decode and parse the response
    news_data = json.loads(data.decode('utf-8'))
    return news_data

# Display the news articles in Streamlit with a scrollable container
def display_news(news_data, language):
    if language == 'en':
        st.title("Latest Indian Farmer and Agriculture News (English)")
    else:
        st.title("Latest Indian Farmer and Agriculture News (Hindi)")

    # Inject custom CSS for scrollable container
    st.markdown(scrollable_style, unsafe_allow_html=True)

    # Create a scrollable container for the news section
    with st.container():
        st.markdown('<div class="scrollable-container">', unsafe_allow_html=True)
        
        # Check if news data contains articles
        if 'data' in news_data:
            articles = news_data['data']

            # Loop through articles and display in Streamlit
            for article in articles:
                st.subheader(article['title'])
                st.write(article['description'])
                st.markdown(f"[Read more]({article['url']})")
                st.markdown("---")  # Separator between articles
        else:
            st.write("No news articles available in this language.")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Main Streamlit app function
def main():
    st.sidebar.header("News Categories")
    st.sidebar.text("Farmer & Agriculture News (India)")  # Sidebar header

    # Option to select language
    language_choice = st.sidebar.selectbox("Select Language", ['English', 'Hindi'])

    # Fetch and display news based on language selection
    if language_choice == 'English':
        news_data = fetch_news('en')  # Fetch English news
        display_news(news_data, 'en')
    else:
        news_data = fetch_news('hi')  # Fetch Hindi news
        display_news(news_data, 'hi')

if __name__ == "__main__":
    main()
