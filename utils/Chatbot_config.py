import streamlit as st

def page_config():
    st.set_page_config(page_title="My Skills Chatbot", page_icon=None, layout="centered", initial_sidebar_state="collapsed", menu_items=None)

def text_format():
    st.markdown(
    """
    <style>
    .message-container {
        background-color: black;
        color: white;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
        word-wrap: break-word;
    }
    .user-message {
        background-color: white;
        color: black;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
        word-wrap: break-word;
    }
    </style>
    """,
    unsafe_allow_html=True
    )

