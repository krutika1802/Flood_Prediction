import streamlit as st
from base_page import BasePage, datetime
from rainfall_archive import get_monthly_rainfall
import joblib
import numpy as np
import pandas as pd
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM
from keras.models import Sequential

class Page2(BasePage):
    def __init__(self):
        super().__init__()
        self.monthly_rainfall = []
        self.rainfall_df = pd.DataFrame()

    def render(self):
        st.title("🌧️ Rainfall Prediction 📊")
        
        st.markdown("""
        Predict or fetch the monthly rainfall for a selected year based on historical data. 
        """)

        st.subheader("📅 Selected Year")
        st.write(f"**Selected Year:** {self.year}")
        st.write(f"**Current Year:** {self.current_year}")

        # Loading model and scaler        
        model = joblib.load('models/rainfall_prediction.pkl')
        scaler = joblib.load('models/rainfall_scaler.pkl')

        consolidated_rainfall = []

        if self.year <= self.current_year:
            # Fetching for previous month
            self.monthly_rainfall = get_monthly_rainfall(self.latitude, self.longitude, self.year)
            if self.year != self.current_year:
                # If we're in same year, we will have to predict at least one
                st.subheader("📊 Monthly Rainfall Data (Historical)")
                st.write("The historical data is shown below for the selected year:")
        else:
            # Fetching last year's december value to predict next 12 months
            self.monthly_rainfall = get_monthly_rainfall(self.latitude, self.longitude, self.year-1)
            self.monthly_rainfall = [self.monthly_rainfall[-1]]
        
        # Not enough months data from historical data
        if len(self.monthly_rainfall) < 12:
            last_available_month_data = np.array([[self.monthly_rainfall[-1]]])

            new_data_scaled = scaler.transform(last_available_month_data)
            new_data_scaled = np.reshape(new_data_scaled, (new_data_scaled.shape[0], 1, new_data_scaled.shape[1]))

            predictions = model.predict(new_data_scaled)
            predicted_rainfall = scaler.inverse_transform(predictions)

            months_needed = 12 - len(self.monthly_rainfall) 

            # We're predicting all 12 months, so we'll directly use this
            if len(self.monthly_rainfall) == 1:
                st.subheader("🔮 Rainfall Prediction (Upcoming Year)")
                consolidated_rainfall = predicted_rainfall.flatten()
            else:
                st.subheader(f"🔮 Rainfall Prediction (Upcoming {months_needed} {'month' if months_needed == 1 else 'months'})")
                consolidated_rainfall = np.append(self.monthly_rainfall,predicted_rainfall.flatten()[:months_needed])

            self.monthly_rainfall = consolidated_rainfall

            st.write("**Predicted Monthly Rainfall (in mm):**")


        # Updating session
        self.rainfall = self.monthly_rainfall
        self.update_session_state()
        self.rainfall_df = pd.DataFrame([self.monthly_rainfall], columns=self.months)

        st.write(self.rainfall_df)

        st.sidebar.header("Location Details 📍")
        st.sidebar.write(f"**Latitude:** {self.latitude}°")
        st.sidebar.write(f"**Longitude:** {self.longitude}°")
