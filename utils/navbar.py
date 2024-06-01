import streamlit as st

def Navbar():
    with st.sidebar:
        st.page_link('main.py', label='Home page', icon='🔥')
        st.page_link('pages/skills.py', label='Skills', icon='🛡️')
        st.page_link('pages/chatbot.py', label='Chatbot', icon='💯')
        st.page_link('pages/bps_data.py', label="Indonesia's Data", icon='🇮🇩')
        # st.page_link('pages/password.py', label="Password Entry", icon='🧭')