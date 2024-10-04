import streamlit as st
import requests
import pandas as pd
import altair as alt


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
    


# Function to get weather data using Open-Meteo
def get_weather_data(lat, lon, days):
    base_url = "https://api.open-meteo.com/v1/forecast"
    
    # Parameters for current weather and extended forecast (including wind, humidity, precipitation chance)
    params = {
        'latitude': lat,
        'longitude': lon,
        'current_weather': 'true',
        'daily': 'temperature_2m_max,precipitation_probability_mean,temperature_2m_min,windspeed_10m_max,relative_humidity_2m_max,relative_humidity_2m_min,precipitation_probability_max',
        'forecast_days': days,
        'timezone': 'auto'
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Streamlit App
def main():
    st.title("Weather and Forecast App (Open-Meteo)")

    # Get latitude and longitude from user
    # city = st.text_input("Enter city name (e.g., London)")
    api_key = "75f5259e5f36234789875b400c78db3b"
    
    
    # Hardcoded lat/lon values for some cities
   
    
        # Allow user to select the number of forecast days
    days = 7
    city="Ranchi"
    
    lat, lon = get_lat_lon(city, api_key)
    if lat is not None and lon is not None:
        pass
        # st.write(f"Latitude: {lat}")
        # st.write(f"Longitude: {lon}")
    else:
        st.error("City not found, please try again.")
    weather_data = get_weather_data(lat, lon, days)

    if weather_data:
        # Display current weather
        forecast = weather_data['daily']
        current_weather = weather_data['current_weather']
        st.subheader(f"Current Weather in {city}")
        st.write(f"Temperature: {current_weather['temperature']} °C")
        st.write(f"Windspeed: {current_weather['windspeed']} km/h")
      
        minhumi=forecast['relative_humidity_2m_max'][0]
        maxhumi=forecast['relative_humidity_2m_min'][0]
        humi=(minhumi+maxhumi)/2
        st.write("current humidity",humi)
        
        
        # Display forecast
        st.subheader(f"{days}-Day Forecast")
            
        data = {
        'Date': forecast['time'],  # Assuming forecast['date'] has the dates
        'Max_temp(°C)': forecast['temperature_2m_max'],
        'Min_temp(°C)': forecast['temperature_2m_min'],
        'Max Humidity (%)': forecast['relative_humidity_2m_max'],
        'Min Humidity (%)': forecast['relative_humidity_2m_min'],
        'Precpitation(%)': forecast['precipitation_probability_max']
        }

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # Streamlit Title
        st.title("7-Day Weather Forecast")
        
        cols=st.columns([1.5,1])
        
        with cols[0]:

        # 1. Max and Min Temperature Line Chart
            temp_chart = alt.Chart(df).transform_fold(
            ['Max_temp(°C)', 'Min_temp(°C)'],
            as_=['Temperature Type', 'Temperature']
            ).mark_line(strokeWidth=3).encode(
            x=alt.X('Date:T', timeUnit='date'),
            y='Temperature:Q',
            color='Temperature Type:N',
            tooltip=[alt.Tooltip('Date:T', title='Date'),
                    alt.Tooltip('Temperature:Q', title='Temperature (°C)'),
                    alt.Tooltip('Temperature Type:N', title='Type')]
            ).properties(
                title='Max and Min Temperature Over Time',
                width=600,
                height=400
            )

            # Adding points (dots) on each data point
            points = alt.Chart(df).transform_fold(
                ['Max_temp(°C)', 'Min_temp(°C)'],
                as_=['Temperature Type', 'Temperature']
            ).mark_point(size=100).encode(  # Increase size for bigger dots
                x=alt.X('Date:T', timeUnit='date'),
                y='Temperature:Q',
                color='Temperature Type:N',
                tooltip=[alt.Tooltip('Date:T', title='Date'),
                        alt.Tooltip('Temperature:Q', title='Temperature (°C)'),
                        alt.Tooltip('Temperature Type:N', title='Type')]
            )

        # Layering the line chart with the points chart
            final_chart = temp_chart + points

            st.altair_chart(final_chart, use_container_width=True)


        with cols[1]:
        
        # 3. Precipitation Probability Line Chart
            precip_chart = alt.Chart(df).mark_line(strokeWidth=3).encode(
                x=alt.X('Date:T',timeUnit="date"),
                y=alt.Y('Precpitation(%):Q', title='Precipitation Probability (%)'),
                
                tooltip=[alt.Tooltip('Date:T', title='Date'),
                    alt.Tooltip('Precpitation(%):Q',title='Precipatation(%)')]
            ).properties(
                title='Precipitation Probability Over Time',
                width=600,
                height=400
            )

            points1 = alt.Chart(df).mark_point(size=100).encode(  # Increase size for bigger dots
                x=alt.X('Date:T', timeUnit='date'),
                y=alt.Y('Precpitation(%):Q',title='Precipitation Probability (%)'),
                
                tooltip=[alt.Tooltip('Date:T', title='Date'),
                    alt.Tooltip('Precpitation(%):Q',title='Precipatation(%)')]
            )
            finalchart1=precip_chart+points1
            st.altair_chart(finalchart1, use_container_width=True)
            
            
   
if __name__ == '__main__':
    main()
