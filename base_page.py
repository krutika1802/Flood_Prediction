import streamlit as st
from datetime import datetime
import calendar
class BasePage:
    def __init__(self):
        # Initialize session state variables if they don't exist
        if 'latitude' not in st.session_state:
            st.session_state.latitude = 0.0
        if 'longitude' not in st.session_state:
            st.session_state.longitude = 0.0
        if 'year' not in st.session_state:
            st.session_state.year = 2020
        if 'rainfall' not in st.session_state:
            st.session_state.rainfall = []

        self.latitude = st.session_state.latitude
        self.longitude = st.session_state.longitude
        self.year = st.session_state.year
        self.current_year = datetime.now().year
        self.rainfall = st.session_state.rainfall
        self.months =[calendar.month_abbr[i].upper() for i in range(1, 13)]

    def update_session_state(self):
        st.session_state.latitude = self.latitude
        st.session_state.longitude = self.longitude
        st.session_state.year = self.year
        st.session_state.rainfall = self.rainfall 
