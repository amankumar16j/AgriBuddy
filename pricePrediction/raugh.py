import streamlit as st
import requests
import pandas as pd
import altair as alt

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

# Function to get 7-day weather forecast using Open-Meteo
def get_weather_forecast(lat, lon):
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': lat,
        'longitude': lon,
        'daily': 'temperature_2m_max,temperature_2m_min',
        'forecast_days': 7,
        'timezone': 'auto'
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Streamlit app to show weather forecast
def main():
    st.title("7-Day Weather Forecast with Line Chart")

    # Input for city name
    city_name = st.text_input("Enter city name (e.g., London, New York)")
    api_key = "your_positionstack_api_key"  # Replace with your Positionstack API key

    if st.button("Get 7-Day Forecast"):
        lat, lon = get_lat_lon(city_name, api_key)
        if lat is not None and lon is not None:
            weather_data = get_weather_forecast(lat, lon)

            if weather_data:
                # Parse the data
                forecast = weather_data['daily']
                dates = forecast['time']
                temp_max = forecast['temperature_2m_max']
                temp_min = forecast['temperature_2m_min']

                # Create a DataFrame
                df = pd.DataFrame({
                    'Date': dates,
                    'Max Temperature (°C)': temp_max,
                    'Min Temperature (°C)': temp_min
                })

                # Display the data
                st.subheader(f"7-Day Weather Forecast for {city_name}")
                st.dataframe(df)

                # Altair Line Chart
                line_chart = alt.Chart(df).transform_fold(
                    ['Max Temperature (°C)', 'Min Temperature (°C)'],
                    as_=['Temperature Type', 'Temperature']
                ).mark_line().encode(
                    x='Date:T',
                    y='Temperature:Q',
                    color='Temperature Type:N'
                ).properties(
                    title=f"7-Day Temperature Forecast for {city_name}",
                    width=600,
                    height=400
                )

                st.altair_chart(line_chart)
            else:
                st.error("Could not retrieve weather data.")
        else:
            st.error("City not found. Please try again.")

if __name__ == '__main__':
    main()
