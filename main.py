import streamlit as st
from utils.navbar import Navbar
from utils.Chatbot_config import text_stream
from utils.homepage_function import project_list, show_more, for_the_password, download_button
import asyncio
st.set_page_config(
    page_title='Home',
    page_icon='🔥',
    layout='wide',
    initial_sidebar_state='collapsed'
)

with open("style.css") as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

if "model_picked" not in st.session_state:
    st.session_state.model_picked = "@cf/meta/llama-3-8b-instruct"

if "first_home" not in st.session_state:
    st.session_state.first_home = False

Navbar()
# st.markdown('🔥 **TERRA17066**')
colhead1,_,_, colhead2 = st.columns(4)
with colhead1:
    st.markdown("<medium>I'm Bima, Data Enthusiast, AI Engineer</medium>", unsafe_allow_html=True)
with colhead2:
    download_button()
st.markdown("<h1>Welcome to my machine learning journey! 🚀 I'm thrilled to share my passion for harnessing the power of Large Language Models (LLMs) with you. As a machine learning engineer, I'm constantly exploring innovative ways to analyze and visualize data, with a focus on Government Data Analysis, Cloudflare's AI Integration, and making Accessible AI Tools.</h1>",unsafe_allow_html=True)
# st.image("data/itb.jpg",caption="ITB 1978 with AI enhancement",width=500)
st.sidebar.write("Welcome! My personal information page!",unsafe_allow_html=True)

# res = st.empty()
# asyncio.run(welcoming_prompt(res))
# st.divider()
if st.session_state.first_home==False:
    show_more()

if st.session_state.first_home==True:
    st.divider()
    
    cols1,cols2 = st.columns(2)

    with cols1:
        project1 = st.empty()
        st.page_link('pages/indonesia_data.py', label="Indonesia's Data 🇮🇩", icon='➡️')
        project2 = st.empty()
        st.page_link("pages/cloudflare_main_page.py", label="Testing Cloudflare LLMs ☁️", icon='➡️')
        project3 = st.empty()
        st.page_link('pages/terra.py', label='TERRA Impersonator 💯', icon='➡️')

    with cols2:
        st.image("data/pengangguran.png",caption="Hover to find the button to full screen")
        st.markdown("<h2></h2>",unsafe_allow_html=True)
        st.markdown("<medium></medium>",unsafe_allow_html=True)
        st.markdown('#')
        st.image("data/cloudflare.png",caption="Hover to find the button to full screen")
        st.markdown("<h1></h1>",unsafe_allow_html=True)
        st.markdown("<medium></medium>",unsafe_allow_html=True)
        st.markdown("<medium></medium>",unsafe_allow_html=True)
        st.image("data/terra_chatbot.png",caption="Hover to find the button to full screen")
        for_the_password()

    asyncio.run(project_list(project1,project2,project3))
# if __name__ == '__main__':
#     main()