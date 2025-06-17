import streamlit as st

class SidebarNavigation:
    def __init__(self):
        self.pages = {
            "Page 1": "🏠 Location & Year Input",
            "Page 2": "📊 Rainfall Prediction",
            "Page 3": "📅 Flood Prediction"
        }

    def render(self):
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Choose a page:", list(self.pages.values()))
        
        for page_name, icon_label in self.pages.items():
            if page == icon_label:
                st.sidebar.markdown(f"<span style='color: white; font-size: 18px; background-color: #007bff; padding: 5px; border-radius: 5px;'>{icon_label}</span>", unsafe_allow_html=True)
            else:
                st.sidebar.markdown(f"<span style='font-size: 18px;'>{icon_label}</span>", unsafe_allow_html=True)
        
        return page
