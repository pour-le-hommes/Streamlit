import streamlit as st

def Navbar():
    st.markdown("""
        <style>
            section[data-testid="stSidebarNav"][aria-expanded="true"]{
                display: none;
            }
        </style>
        """, unsafe_allow_html=True)
    with st.sidebar:
        st.page_link('pages/home.py', label='Individual Checker', icon='🔥')
        st.page_link('pages/skillspage.py', label='Skills', icon='🛡️')
        st.page_link('pages/chatbot.py', label='Chatbot', icon='💯')