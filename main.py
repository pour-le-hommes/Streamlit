import streamlit as st
from utils.navbar import Navbar
from pages.home import homepage

def main():
    st.set_page_config(page_title="Main Page", page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)
    # builds the sidebar menu
    Navbar()

    st.title(f'🔥 My Main Page')
    homepage()

    # your content


if __name__ == '__main__':
    main()