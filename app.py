import streamlit as st
import requests
import pandas as pd


# TaxiFareModel front

st.set_page_config(page_title="Taxi Fare Predictor", page_icon="🚖")

st.title("🚕 Taxi Fare Predictor")

st.image("https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&h=400&q=80",
         caption="", use_container_width =True)

# st.markdown('''
# Remember that there are several ways to output content into your web page...

# Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
# ''')

# Section 1: User Input Controllers
st.header("📍 Ride Parameters")
st.markdown("Please enter the details of your taxi ride:")


# Here we would like to add some controllers in order to ask the user to select the parameters of the ride


date = st.date_input("Date")
time = st.time_input("Time")
pickup_lng = st.number_input(
    "Pickup Longitude",
    value=-73.9731084,
    format="%.8f",
    step=0.000001
)
pickup_lat = st.number_input(
    "Pickup Latitude",
    value=40.7958402,
    format="%.8f",
    step=0.000001
)
dropoff_lng = st.number_input(
    "Dropoff Longitude",
    value=-73.9731084,
    format="%.8f",
    step=0.000001
)
dropoff_lat = st.number_input(
    "Dropoff Latitude",
    value=40.7958402,
    format="%.8f",
    step=0.000001
)
passengers = st.number_input("Passengers", value=1, min_value=1, max_value=6)

if st.button("Predict"):
    # Prepare data
    params = {
        'pickup_datetime': f"{date} {time}",
        'pickup_longitude': pickup_lng,
        'pickup_latitude': pickup_lat,
        'dropoff_longitude': dropoff_lng,
        'dropoff_latitude': dropoff_lat,
        'passenger_count': passengers
    }


# '''
# # ## Once we have these, let's call our API in order to retrieve a prediction

# # See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

# # 🤔 How could we call our API ? Off course... The `requests` package 💡
# '''

    url = 'https://taxifare.lewagon.ai/predict'


# Call API
    response = requests.get(url, params=params)

    if response.status_code == 200:
        fare = response.json()['fare']
        st.write(f"Predicted fare: ${fare:.2f}")
    else:
        st.write("Error calling API")


## Finally, we can display the prediction to the user

df_points = pd.DataFrame([
    {'lat': float(pickup_lat),'long' : float(pickup_lng)},
    {'lat': float(dropoff_lat),'long' : float(dropoff_lng)}
])

#center_lat = (float(pickup_lat)+float(pickup_lng))/2
st.map(df_points, latitude = 'lat', longitude = 'long', zoom = 12)
