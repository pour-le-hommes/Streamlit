import streamlit as st
import pandas as pd
from pages.skills import skillspage

def homepage():
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