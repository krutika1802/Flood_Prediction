import streamlit as st
from datetime import datetime
import streamlit.components.v1 as components
from rainfall_archive import get_monthly_rainfall
import joblib
import numpy as np
import pandas as pd
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM
from keras.models import Sequential
import calendar


current_year = datetime.now().year

year_options = list(range(current_year - 10, current_year + 2))
# Initialize session state variables if they don't exist
# Initialize session state variables if they don't exist
if 'latitude' not in st.session_state:
    st.session_state.latitude = 0.0  # Set initial value as a float
if 'longitude' not in st.session_state:
    st.session_state.longitude = 0.0  # Set initial value as a float
if 'year' not in st.session_state:
    st.session_state.year = 2020  # Default year

def page_1():
    st.title("Location and Year Input")

    # Get input values and store them in session state (ensure float values for latitude and longitude)
    st.session_state.latitude = st.number_input(
        "Enter Latitude (in decimal degrees):", 
        min_value=-90.0, 
        max_value=90.0, 
        step=0.1, 
        value=st.session_state.latitude  # Ensure value is float
    )
    st.session_state.longitude = st.number_input(
        "Enter Longitude (in decimal degrees):", 
        min_value=-180.0, 
        max_value=180.0, 
        step=0.1, 
        value=st.session_state.longitude  # Ensure value is float
    )
    
    st.session_state.year = st.selectbox(
        "Select Year", 
        options=year_options, 
        index=year_options.index(st.session_state.year) if st.session_state.year in year_options else 0
    )

    st.write(f"Latitude: {st.session_state.latitude}°")
    st.write(f"Longitude: {st.session_state.longitude}°")
    st.write(f"Selected Year: {st.session_state.year}")

def page_2(latitude, longitude, year, current_year):
    st.title("🌧️ Rainfall Prediction 📊")
    
    st.markdown("""
    Predict the monthly rainfall for a selected year based on historical data. 
    Enter the geographical location (latitude and longitude) and select the year to get predictions.
    """)

    st.subheader("📅 Selected Year")
    st.write(f"**Selected Year:** {year}")
    st.write(f"**Current Year:** {current_year}")

    monthly_rainfall = []
    consolidated_rainfall = []

    if year <= current_year:
        st.subheader("📊 Monthly Rainfall Data (Historical)")
        st.write("The historical data is shown below for the selected year:")

        monthly_rainfall = get_monthly_rainfall(latitude, longitude, year)

        months_short = [calendar.month_abbr[i].upper() for i in range(1, 13)]

        rainfall_df = pd.DataFrame([monthly_rainfall], columns=months_short)
        consolidated_rainfall = monthly_rainfall
        st.session_state.monthly = consolidated_rainfall
        st.write(rainfall_df)
    else:
        # Fetching last december value to predict next 12 months
        monthly_rainfall = get_monthly_rainfall(latitude, longitude, year-1)
        monthly_rainfall = [monthly_rainfall[-1]]

    if len(monthly_rainfall) < 12:
        st.subheader("🔮 Rainfall Prediction (Upcoming Months)")

        model = joblib.load('rainfall_prediction.pkl')
        scaler = joblib.load('scaler.pkl')

        last_available_month_data = np.array([[monthly_rainfall[-1]]])

        new_data_scaled = scaler.transform(last_available_month_data)
        new_data_scaled = np.reshape(new_data_scaled, (new_data_scaled.shape[0], 1, new_data_scaled.shape[1]))

        predictions = model.predict(new_data_scaled)
        predicted_rainfall = scaler.inverse_transform(predictions)

        months_short = [calendar.month_abbr[i].upper() for i in range(1, 13)]

        months_needed = len(monthly_rainfall) - 12

        if len(monthly_rainfall) == 1:
            consolidated_rainfall = predicted_rainfall
        else:
            consolidated_rainfall = monthly_rainfall + predicted_rainfall[:(months_needed+1)]

        final_list = []
        for i in consolidated_rainfall:
            for j in i:
               final_list.append(j)

        st.session_state.monthly = final_list
        rainfall_df = pd.DataFrame(consolidated_rainfall, columns=months_short)
        st.write("**Predicted Monthly Rainfall (in mm):**")
        st.write(rainfall_df)

    st.sidebar.header("Location Details 📍")
    st.sidebar.write(f"**Latitude:** {latitude}°")
    st.sidebar.write(f"**Longitude:** {longitude}°")
    
    st.markdown("<br>", unsafe_allow_html=True)

def page_3():
    # Set the title of the page
    st.title("Flood Prediction - Monthly Rainfall Data")

    # Load the pre-trained model
    model = joblib.load('random_forest_model.pkl')

    # Check if monthly data exists in session state
    if 'monthly' not in st.session_state:
        st.error("Monthly rainfall data is not available in session state.")
        return

    input_values = st.session_state.monthly




    # Ensure there are 12 values (one for each month)
    if len(input_values) != 12:
        st.error("Invalid monthly data. There must be exactly 12 values.")
        return

    # Create a DataFrame to structure the input values
    columns = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']  
    input_df = pd.DataFrame([input_values], columns=columns)

    # Make prediction based on the input data
    prediction = model.predict(input_df)

    # Display the input values in a nice table format
    st.write("### Monthly Rainfall Data:")
    st.dataframe(input_df)

    # Display the prediction result in a more user-friendly format
    st.write("### Prediction Result:")
    if prediction[0] == 1:
        st.markdown("<h3 style='color: red;'>Flood Risk: HIGH</h3>", unsafe_allow_html=True)
    else:
        st.markdown("<h3 style='color: green;'>Flood Risk: LOW</h3>", unsafe_allow_html=True)

    # Add some helpful tips or further information
    st.write("""
    **Note:** The model uses historical rainfall patterns and predicted values to assess the flood risk. 
    The flood risk is determined based on the pattern of monthly rainfall.
    """)



# Streamlit sidebar with styled navigation and icons
def sidebar_navigation():
    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            background-color: #f0f0f0;
            color: #333;
        }
        .sidebar .sidebar-content a {
            font-size: 18px;
            font-weight: bold;
            color: #007bff;
        }
        .sidebar .sidebar-content a:hover {
            color: #0056b3;
            background-color: #e7e7e7;
        }
        .sidebar .sidebar-content a.active {
            color: #ffffff;
            background-color: #007bff;
            border-radius: 5px;
        }
        </style>
        """, unsafe_allow_html=True)

    pages = {
        "Page 1": "🏠 Location & Year Input",
        "Page 2": "📊 Rainfall Prediction",
        "Page 3": "📅 Flood Prediction"
    }

    st.sidebar.title("Navigation")

    page = st.sidebar.radio("Choose a page:", list(pages.values()))

    for page_name, icon_label in pages.items():
        if page == icon_label:
            st.sidebar.markdown(f"<span style='color: white; font-size: 18px; background-color: #007bff; padding: 5px; border-radius: 5px;'>{icon_label}</span>", unsafe_allow_html=True)
        else:
            st.sidebar.markdown(f"<span style='font-size: 18px;'>{icon_label}</span>", unsafe_allow_html=True)

    return page

def main():
    page = sidebar_navigation()

    if page == "🏠 Location & Year Input":
        page_1()
    elif page == "📊 Rainfall Prediction":
        page_2(st.session_state.latitude, st.session_state.longitude, st.session_state.year, current_year)
    elif page == "📅 Flood Prediction":
        page_3()

if __name__ == "__main__":
    main()
