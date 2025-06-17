import streamlit as st
from base_page import BasePage, datetime
import joblib
import pandas as pd

class Page3(BasePage):
    def __init__(self):
        super().__init__()

    def render(self):
        st.title("Flood Prediction - Monthly Rainfall Data")

        model = joblib.load('models/flood_prediction.pkl')

        if 'rainfall' not in st.session_state:
            st.error("Monthly rainfall data is not available in session state.")
            return

        input_df = pd.DataFrame([self.rainfall], columns=self.months)

        prediction = model.predict(input_df)

        st.write("### Monthly Rainfall Data:")
        st.dataframe(input_df)

        st.write("### Prediction Result:")
        if prediction[0] == 1:
            st.markdown("<h3 style='color: red;'>Flood Risk: HIGH</h3>", unsafe_allow_html=True)
        else:
            st.markdown("<h3 style='color: green;'>Flood Risk: LOW</h3>", unsafe_allow_html=True)
