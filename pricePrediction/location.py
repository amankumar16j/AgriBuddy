import streamlit as st
import requests

# Function to fetch latitude and longitude using Positionstack API
def get_lat_lon(city_name, api_key):
    base_url = "http://api.positionstack.com/v1/forward"
    params = {
        'access_key': api_key,
        'query': city_name,
        'limit': 1
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['data']:
            lat = data['data'][0]['latitude']
            lon = data['data'][0]['longitude']
            return lat, lon
        else:
            return None, None
    else:
        return None, None

# Streamlit app to get the latitude and longitude
def main():
    st.title("Get Latitude and Longitude of a City (Positionstack)")
    
    # Input for city name
    city_name = st.text_input("Enter city name (e.g., London, New York)")
    
    api_key = "75f5259e5f36234789875b400c78db3b"  # Replace with your Positionstack API key

    if st.button("Get Coordinates"):
        lat, lon = get_lat_lon(city_name, api_key)
        if lat is not None and lon is not None:
            st.write(f"Latitude: {lat}")
            st.write(f"Longitude: {lon}")
        else:
            st.error("City not found, please try again.")

if __name__ == '__main__':
    main()
