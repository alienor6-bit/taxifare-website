import streamlit as st
import requests
import pandas as pd
from geopy.geocoders import Nominatim

# TaxiFareModel front
st.set_page_config(page_title="Taxi Fare Predictor", page_icon="🚖")
st.title("🚕 Taxi Fare Predictor")
st.image("https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&h=400&q=80",
caption="", use_container_width=True)

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

# Address inputs
pickup_address = st.text_input("Pickup Address", placeholder="e.g., Times Square, New York or İzmir, Turkey")
dropoff_address = st.text_input("Dropoff Address", placeholder="e.g., Central Park, New York or Ankara, Turkey")

# Initialize coordinates
pickup_lng, pickup_lat = None, None
dropoff_lng, dropoff_lat = None, None

# Geocode pickup address
if pickup_address:
    try:
        loc = Nominatim(user_agent="Geopy Library")
        pickup_location = loc.geocode(pickup_address)
        if pickup_location:
            pickup_lng = pickup_location.longitude
            pickup_lat = pickup_location.latitude
            st.success(f"✅ Pickup found: {pickup_location.address}")
        else:
            st.error("❌ Pickup address not found")
    except:
        st.error("❌ Error geocoding pickup address")

# Geocode dropoff address
if dropoff_address:
    try:
        loc = Nominatim(user_agent="Geopy Library")
        dropoff_location = loc.geocode(dropoff_address)
        if dropoff_location:
            dropoff_lng = dropoff_location.longitude
            dropoff_lat = dropoff_location.latitude
            st.success(f"✅ Dropoff found: {dropoff_location.address}")
        else:
            st.error("❌ Dropoff address not found")
    except:
        st.error("❌ Error geocoding dropoff address")
passengers = st.number_input("Passengers", value=1, min_value=1, max_value=6)

if st.button("Predict"):
    # Check if we have valid coordinates
    if pickup_lng and pickup_lat and dropoff_lng and dropoff_lat:
        # Prepare data
        params = {
        'pickup_datetime': f"{date} {time}",
        'pickup_longitude': pickup_lng,
        'pickup_latitude': pickup_lat,
        'dropoff_longitude': dropoff_lng,
        'dropoff_latitude': dropoff_lat,
        'passenger_count': passengers
         }

        url = 'https://taxifare.lewagon.ai/predict'

        # Call API
        response = requests.get(url, params=params)
        if response.status_code == 200:
            fare = response.json()['fare']
            st.write(f"Predicted fare: ${fare:.2f}")
        else:
            st.write("Error calling API")
    else:
        st.error("⚠️ Please enter valid pickup and dropoff addresses before predicting")

## Finally, we can display the prediction to the user

df_points = pd.DataFrame([
 {'lat': float(pickup_lat),'lon' : float(pickup_lng)},
 {'lat': float(dropoff_lat),'lon' : float(dropoff_lng)}
])

#center_lat = (float(pickup_lat)+float(dropoff_lat))/2

st.map(df_points, latitude = 'lat', longitude = 'lon', zoom = 12)
