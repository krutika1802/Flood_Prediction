import streamlit as st
from sidebar_navigation import SidebarNavigation
from page_1 import Page1
from page_2 import Page2
from page_3 import Page3

def main():
    # Initialize sidebar navigation
    sidebar = SidebarNavigation()
    page = sidebar.render()

    # Render appropriate page
    if page == "🏠 Location & Year Input":
        page1 = Page1()
        page1.render()
    elif page == "📊 Rainfall Prediction":
        page2 = Page2()
        page2.render()
    elif page == "📅 Flood Prediction":
        page3 = Page3()
        page3.render()

if __name__ == "__main__":
    main()
