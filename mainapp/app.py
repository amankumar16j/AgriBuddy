import streamlit as st
from streamlit_option_menu import option_menu
import subprocess
from PIL import Image
import streamlit_shadcn_ui as ui
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import pandas as pd
import requests
import altair as alt
from datetime import datetime
import joblib
from streamlit_lottie import st_lottie
from datetime import datetime
import os


st.set_page_config(layout="wide")

# @st.cache_data
# def get_data():
#     source = data.stocks()
#     source = source[source.date.gt("2004-01-01")]
#     return source
# def generate_historical_data(state, crop):
#             np.random.seed(hash(state + crop) % 1234567)
#             dates = pd.date_range(start='2020-01-01', periods=100, freq='M')
            
#             # Adding a trend and more noise
#             trend = np.linspace(50, 150, len(dates))
#             noise = np.random.randn(len(dates)) * 10
#             prices = trend + noise
            
#             return pd.DataFrame({'Date': dates, 'Price': prices})
        
# def predict_future_prices(data, future_periods=12):
#             data['Time'] = np.arange(len(data))
#             X = data[['Time']]
#             y = data['Price']
            
#             # Train a simple linear regression model
#             model = LinearRegression()
#             model.fit(X, y)
            
#             # Predict future prices
#             future_times = np.arange(len(data), len(data) + future_periods)
#             future_prices = model.predict(future_times.reshape(-1, 1))
            
#             # Create a DataFrame for the predictions
#             future_dates = pd.date_range(start=data['Date'].iloc[-1], periods=future_periods + 1, freq='M')[1:]
#             future_data = pd.DataFrame({'Date': future_dates, 'Price': future_prices})
            
#             return future_data

#function to get longitude and latitude of the given state

#weather api key
api_key = "75f5259e5f36234789875b400c78db3b"
annual_rainfall = [29, 21, 37.5, 30.7, 52.6, 150, 299, 251.7, 179.2, 70.5, 39.8, 10.9]
crop=1

def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json() 

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
        'daily': 'temperature_2m_max,temperature_2m_min,windspeed_10m_max,relative_humidity_2m_max,relative_humidity_2m_min,precipitation_probability_max',
        'forecast_days': days,
        'timezone': 'auto'
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None



def preprocess_frame(frame):
    # Resize frame to 256x256 to match your model's input size
    frame=np.array(frame)
    frame_resized = cv2.resize(frame, (256, 256))
    
    # Convert frame to array and preprocess it
    frame_array = img_to_array(frame_resized)
    frame_array = np.expand_dims(frame_array, axis=0)
    frame_array /= 255.0  # Normalize to [0, 1]
    
    return frame_array

def process_video(video_path, model, plant_type_dict):
    cap = cv2.VideoCapture(video_path)
    predictions = []
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        preprocessed_frame = preprocess_frame(frame)
        prediction = model.predict(preprocessed_frame)
        pred_class = np.argmax(prediction, axis=1)[0]
        predictions.append(pred_class)
    
    cap.release()
    final_prediction = max(set(predictions), key=predictions.count)  # Majority voting
    return plant_type_dict[final_prediction]

# Initialize session state for page selection
if 'page' not in st.session_state:
    st.session_state.page = 'Predict Price'  # Default page

# Sidebar title with custom size
# st.sidebar.markdown(
#     "<h1 style='font-size:24px;'>Navigation</h1>", unsafe_allow_html=True
# )
# st.sidebar.markdown(
#     "<p style='font-size:18px;'>Select Functionality:</p>", unsafe_allow_html=True
# )


# Create a black background box with padding around the buttons


# Use the buttons to switch pages and update session state
with st.sidebar:
    menu_select = option_menu(
        menu_title="Menu",   # Required
        options=["Dashboard", "Plant Disease Detection", "Predict Price"],  # Options to display
        menu_icon="cast",  # You can add any icon from Bootstrap Icons or FontAwesome
        default_index=0,  # Default option to be selected
    )

# Main content based on the selected page
if menu_select == 'Predict Price':
    st.title("Crop Price Prediction")
    st.subheader("This functionality is coming soon!")
    st.info("Placeholder card for crop price prediction.")

elif menu_select == 'Plant Disease Detection':
    st.title("Plant Disease Detection")
    
    # Choose detection mode
    detection_mode = st.selectbox(
        "Select Detection Mode",
        ["Detect using Image", "Detect using Live Feed", "Detect using Video"]
    )

    # Choose plant type
    plant_type = st.selectbox(
        "Select Plant Type",
        ["Corn", "Tomato", "Potato"]
    )

    # Handle user input based on detection mode
    if detection_mode == "Detect using Image":
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)
            st.write("Classifying...")
            if plant_type=='Corn':
                image=Image.open(uploaded_file)
                preprocessed_image=preprocess_frame(image)
             
                corn_model = load_model("CornPrediction/cornprediction.h5")
                prediction = corn_model.predict(preprocessed_image) 
                dict={
                0: 'Cercospora_leaf_spot Gray_leaf_spot',
                1: 'Common_rust_', 
                2: 'Northern_Leaf_Blight',
                3: 'Healthy',
                }
                pred_class=np.argmax(prediction,axis=1)[0]
                label=dict[pred_class]
                st.write("predictied image has disease: ",label)
            elif plant_type=='Tomato':
                image=Image.open(uploaded_file)
                preprocessed_image=preprocess_frame(image)
                tomato_model = load_model("tomatopred/tomatopred1.h5")
                prediction = tomato_model.predict(preprocessed_image) 
                dict={0:'Bacterial_spot',
                1:'Early_blight',
                2:'Late_blight',
                3:'Leaf_Mold',
                4:'Septoria_leaf_spot',
                5:'Spider_mites Two-spotted_spider_mite',
                6:'Target_Spot',
                7:'Yellow_Leaf_Curl_Virus',
                8:'mosaic_virus',
                9: 'healthy'}
                pred_class=np.argmax(prediction,axis=1)[0]
                label=dict[pred_class]
                st.write("predictied image has disease: ",label)
            elif plant_type=='Potato':
                image=Image.open(uploaded_file)
                preprocessed_image=preprocess_frame(image)
                potato_model = load_model("mainapp/potatoes.h5")
                prediction = potato_model.predict(preprocessed_image) 
                dict={
                0: 'Early_blight',
                1: 'Late_blight',
                2: 'healthy',
                }
                pred_class=np.argmax(prediction,axis=1)[0]
                label=dict[pred_class]
                st.write("predictied image has disease: ",label)
                
                
            # Add your model prediction code here

    elif detection_mode == "Detect using Live Feed":
        if plant_type=='Potato':
            st.write("Running live prediction for Potato...")
            

        # Run the external Python script
        # Ensure that the script is located in the same directory or provide the full path
            subprocess.Popen(["python", "mainapp/Potatoapp.py"])
            st.write("Live prediction script has been started.")
            st.write("give 30 s to load")
            st.write("type q to end........")
        elif plant_type=='Tomato':
            subprocess.Popen(["python", "tomatopred/tomatoapp.py"])
            st.write("Live prediction script has been started.")
            st.write("give 30 s to load")
            st.write("type q to end........")
        elif plant_type=='Corn':
            subprocess.Popen(["python", "CornPrediction/cornapp.py"])
            st.write("Live prediction script has been started.")
            st.write("give 30 s to load")
            st.write("type q to end........")
            
            
       
    elif detection_mode == "Detect using Video":
        uploaded_video = st.file_uploader("Upload a video...", type=["mp4", "mov", "avi"])
        if uploaded_video is not None:
            st.video(uploaded_video)
            st.write("Processing video...")
            # Add your model prediction code for video here
            temp_video_path = "temp_video.mp4"  # Save uploaded video to a temporary file
            with open(temp_video_path, "wb") as f:
                f.write(uploaded_video.read())
            
            # Process the video
            if plant_type=='Corn':
                model = load_model("CornPrediction/cornprediction.h5")
                dict={
                0: 'Cercospora_leaf_spot Gray_leaf_spot',
                1: 'Common_rust_', 
                2: 'Northern_Leaf_Blight',
                3: 'Healthy',
                }
            elif plant_type=='Tomato':
                model = load_model("tomatopred/tomatopred1.h5")
                dict={0:'Bacterial_spot',
                1:'Early_blight',
                2:'Late_blight',
                3:'Leaf_Mold',
                4:'Septoria_leaf_spot',
                5:'Spider_mites Two-spotted_spider_mite',
                6:'Target_Spot',
                7:'Yellow_Leaf_Curl_Virus',
                8:'mosaic_virus',
                9: 'healthy'}
            elif plant_type=='Potato':
                model = load_model("mainapp\potatoes.h5")
                dict={
                0: 'Early_blight',
                1: 'Late_blight',
                2: 'healthy',
                }
            predicted_label = process_video(temp_video_path,model,dict)
            st.write(f"Predicted disease in video: {predicted_label}")
            
            
    
# Dashboard  Dashboard Dashboard Dashboard Dashboard Dashboard Dashboard Dashboard Dashboard Dashboard         
            
elif menu_select== 'Dashboard':
    col3=st.columns([1,4])
    with col3[0]:
        link="https://lottie.host/19e17113-27e0-4939-8b89-dc3eee2aa043/Ad83vzKx1U.json"
        l=load_lottieurl(link)
        st.lottie(l,height=130,width=300)
    with col3[1]:
        st.markdown("""
                    <h1 style='font-size: 60px;'>
                        Dashboard
                    </h1>
                    <hr style='border: 2px solid white;'>
                    
                    """, unsafe_allow_html=True)
    with st.container(border=True):
        
        cols = st.columns([5,5,5,5])
        
        # Display current weather
        # Load data according to city info----------------------------
        days = 7
        city = "Jalandhar"
        lat, lon = get_lat_lon(city, api_key)
        if lat is not None and lon is not None:
            pass
        else:
            st.error("City not found, please try again.")
        
        weather_data=get_weather_data(lat, lon, days)
        current_weather = weather_data['current_weather']
        forecast = weather_data['daily']
        minhumi=forecast['relative_humidity_2m_max'][0]
        maxhumi=forecast['relative_humidity_2m_min'][0]
        humi=(minhumi+maxhumi)/2
        precipitation=forecast['precipitation_probability_max'][0]
        with cols[0]:
        
            with st.container(border=True):
                
                now = datetime.now().time()
                # Define the time range for night
                night_start = datetime.strptime("19:00", "%H:%M").time()  # 7 PM
                night_end = datetime.strptime("04:00", "%H:%M").time()  # 4 AM

                # Check if current time is between 7 PM and 4 AM
                                
                sunny="https://lottie.host/7e2f4c85-e3d3-43b6-8a83-aba769f3c0f4/TAjpsqh5ea.json"
                sunny1="https://lottie.host/826c55af-51f7-4f92-9de0-320ee3f39f54/NtAdsdf1Ml.json"
                moon="https://lottie.host/a9a04a62-56f5-4a70-a87f-217f601a270f/d6YUp2fpYO.json"
                
                if now >= night_start or now < night_end:
                    sunny_lottie=load_lottieurl(moon)    
                elif current_weather["temperature"]>35:
                    sunny_lottie=load_lottieurl(sunny)
                else:
                    sunny_lottie=load_lottieurl(sunny1)
                    
                
                # sunny_lottie=load_lottieurl(sunny1)
                    
                st.lottie(sunny_lottie,height=100,width=100)
                ui.metric_card(title="Temperature", content=str(current_weather["temperature"])+" in (c)", key="card1")
       
        with cols[1]:
                with st.container(border=True):
                    windy="https://lottie.host/9462ba5b-410e-4fc4-be63-f8ebd13d3985/HnDwx1zv2P.json"
                    windy_lottie=load_lottieurl(windy)
                    st.lottie(windy_lottie,height=100,width=100)
                    ui.metric_card(title="Wind Speed", content=str(current_weather["windspeed"])+" in (KMPH)", key="card2")
    
        with cols[2]:
            with st.container(border=True):
                humid="https://lottie.host/338a286f-a5b6-4f15-bf33-919241525814/LZLBGuC375.json"
                humid_lottie=load_lottieurl(humid)
                st.lottie(humid_lottie,height=100,width=100)
                ui.metric_card(title="Humidity", content=str(humi)+" in (%)", key="card3")
    
        with cols[3]:
            with st.container(border=True):
                rainy="https://lottie.host/17db9346-022a-4102-8867-b3e511fa8379/rmgkKnkL97.json"
                rainy_lottie=load_lottieurl(rainy)
                st.lottie(rainy_lottie,height=100,width=100)
                ui.metric_card(title="Precipitation", content=str(precipitation)+" in (%)", key="card4")
    
    
    with st.container(border=True):
        

        # Load data according to city info----------------------------
        days = 7
        city = "Jalandhar"
        lat, lon = get_lat_lon(city, api_key)
        if lat is not None and lon is not None:
            pass
        else:
            st.error("City not found, please try again.")
        weather_data = get_weather_data(lat, lon, days)

        if weather_data:
            # Display forecast
            st.header(f"{days}-Day Forecast")
            forecast = weather_data['daily']
                
            data = {
            'Date': forecast['time'],  
            'Max_temp(°C)': forecast['temperature_2m_max'],
            'Min_temp(°C)': forecast['temperature_2m_min'],
            'Max Humidity (%)': forecast['relative_humidity_2m_max'],
            'Min Humidity (%)': forecast['relative_humidity_2m_min'],
            'Precpitation(%)': forecast['precipitation_probability_max']
            }

            # Convert to DataFrame
            df = pd.DataFrame(data)

            # Streamlit Title
            # st.title("7-Day Weather Forecast")
            
            cols=st.columns([1.2,1])
            
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
    
        
    
    with st.container(border=True):
        st.title("Price Forecast For Various Commodities")
        
        with st.container(border=True): 
            st.header("List Of Commodities") 
            
            col1, col2, col3, col4= st.columns([1,1,1,1])
            
            with col1:
                if st.button("Arhar",type="primary", help="Rice",use_container_width=True):
                    crop=0
                                    
            with col2:
                if st.button("Cotton",type="primary", help="Wheat",use_container_width=True):
                    crop=1
                        
            with col3:
                if st.button("Gram",type="primary", help="Tomato",use_container_width=True):
                    crop=2
                    
            with col4:
                if st.button("Masoor",type="primary", help="Potato",use_container_width=True):
                    crop=3
                    
            col1, col2, col3, col4= st.columns([1,1,1,1])
            with col1:
                if st.button("Moong",type="primary", help="Corn",use_container_width=True):
                    crop=4
                                    
            with col2:
                if st.button("Sunflower",type="primary", help="Apple",use_container_width=True):
                    crop=6
                        
            with col3:
                if st.button("Sugarcane",type="primary", help="Mango",use_container_width=True):
                    crop=5
                    
            with col4:
                if st.button("Wheat",type="primary", help="Banana",use_container_width=True):
                    crop=7
                    
        cols=st.columns([1,1])
        with cols[0]:
            with st.container(border=True):
                selected1=option_menu(
                    menu_title="States",
                    options=["andhra","punjab","bihar","tn"],
                    )
                
        with cols[1]:
            with st.container(border=True):
                state=selected1
                current_month = datetime.now().month
                current_year = datetime.now().year
                current_rainfall=annual_rainfall[current_month-1]
                
                months_before_after = []
                for i in range(-12, 13):
                    month = (current_month + i - 1) % 12 + 1
                    months_before_after.append(month)
                    
                rainfall_before_after=[]
                for i in range(-12,13):
                    months=(current_month+i-1) % 12
                    rainfall_before_after.append(months)
                    
                pricemodel=joblib.load("pricePrediction/pricePredmodel.pkl")
                    
                prediction1=[]
                for months,rainfall in zip(months_before_after,rainfall_before_after):
                    x=pd.DataFrame([month,current_year,rainfall,crop]).T
                    pred=pricemodel.predict(x)
                    prediction1.append(pred[0])
    
                st.line_chart(prediction1)
            
      
      ## Need to make it dynamic      
                                  
    with st.container(border=True):
        st.title("Current Price Of Trending Crops")
        cols = st.columns([5,5,5,5])
        with cols[0]:
            ui.metric_card(title="Wheat", content="₹2504/Quintal", description="", key="card5")
        with cols[1]:
            ui.metric_card(title="Potato", content="₹2000/Quintal", description="", key="card6")
        with cols[2]:
            ui.metric_card(title="Millets", content="₹2000/Quintal", description="", key="card7")
        with cols[3]:
            ui.metric_card(title="Arhar", content="₹15500/Quintal", description="", key="card8")
            
    
    
