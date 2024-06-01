import streamlit as st
from utils.navbar import Navbar
from pages.skills import skillspage

def main():
    st.set_page_config(page_title="Main Page", page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)
    # builds the sidebar menu
    Navbar()

    st.title(f'🔥 My Main Page')
    st.logo("data/itb.jpg")
    st.sidebar.markdown("Welcome! My personal information page!")
    st.sidebar.title("Navigation")
    pages = ["Home", "My Skills", "First Portfolio"]
    page = st.sidebar.radio("Go to", pages)


    def home():
        st.title("Home")
        st.write("Welcome to the home page!")

    if page == "Home":
        home()
    elif page == "My Skills":
        skillspage()
    elif page == "First Portfolio":
        st.write("Lmao, fucking none")

    # your content


if __name__ == '__main__':
    main()