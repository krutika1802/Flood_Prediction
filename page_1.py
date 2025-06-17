import streamlit as st
from base_page import BasePage, datetime
from rainfall_archive import get_area_name
class Page1(BasePage):
    def __init__(self):
        super().__init__()

    def render(self):
        st.title("Location and Year Input")
        current_year = datetime.now().year
        self.latitude = st.number_input(
            "Enter Latitude (in decimal degrees):", 
            min_value=-90.0, 
            max_value=90.0, 
            step=0.000001, 
            value=self.latitude  
        )
        self.longitude = st.number_input(
            "Enter Longitude (in decimal degrees):", 
            min_value=-180.0, 
            max_value=180.0, 
            step=0.000001, 
            value=self.longitude  
        )
        
        year_options = list(range(current_year - 10, current_year + 2))
        self.year = st.selectbox(
            "Select Year", 
            options=year_options, 
            index=year_options.index(self.year) if self.year in year_options else 0
        )

        st.write(f"Latitude: {self.latitude}°")
        st.write(f"Longitude: {self.longitude}°")
        st.write(f"Selected Year: {self.year}")
        st.write(f"Location: {get_area_name(self.latitude, self.longitude)}")
        self.update_session_state()
