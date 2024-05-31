import streamlit as st

def Navbar():
    with st.sidebar:
        st.page_link('main.py', label='Home page', icon='🔥')
        st.page_link('pages/skills.py', label='Skills', icon='🛡️')
        st.page_link('pages/chatbot.py', label='Chatbot', icon='💯')