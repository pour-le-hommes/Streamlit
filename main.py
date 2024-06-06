import streamlit as st
from utils.navbar import Navbar
from utils.Chatbot_config import text_stream
from utils.homepage_function import project_list, download_button, first_show_me, show_more_more, email_button
import asyncio
import streamlit_shadcn_ui as ui
from markdownlit import mdlit

st.set_page_config(
    page_title='Home',
    page_icon='🔥',
    layout='wide',
    initial_sidebar_state='collapsed'
)

with open("style.css") as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

SOCIAL_MEDIA = {
    "Kaggle": "https://www.kaggle.com/ogatakashi",
    "LinkedIn": "https://www.linkedin.com/in/bima-ilyasa/",
    "GitHub": "https://github.com/pour-le-hommes"
}

if "model_picked" not in st.session_state:
    st.session_state.model_picked = "@cf/meta/llama-3-8b-instruct"

if "first_home" not in st.session_state:
    st.session_state.first_home = False

if "second_home" not in st.session_state:
    st.session_state.second_home = False

if "first_proj" not in st.session_state:
    st.session_state.first_proj = ""

if "second_proj" not in st.session_state:
    st.session_state.second_proj = ""

if "third_proj" not in st.session_state:
    st.session_state.third_proj = ""

Navbar()
maincol1,maincol2,_,_ = st.columns(4,gap="medium")
with maincol1:
    st.markdown("<medium>**Bima Ilyasa Rachmanditya**</medium>", unsafe_allow_html=True)
    st.markdown("<medium>AI Engineer, Data enthusiast</medium>", unsafe_allow_html=True)
with maincol2:
    smallcol1,smallcol2,_ = st.columns(3)
    with smallcol1:
        st.markdown("")
        st.markdown("[![LinkedIn](https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg)](https://www.linkedin.com/in/bima-ilyasa/)",unsafe_allow_html=True)
    with smallcol2:
        st.markdown("[![GitHub](https://img.icons8.com/?size=100&id=62856&format=png&color=FFFFFF)](https://github.com/pour-le-hommes)",unsafe_allow_html=True)
# st.button("📫 Email me",key="email",type="secondary")
# email_button()

st.markdown("<h1>Welcome to my machine learning journey! 🚀 I'm thrilled to share my passion for harnessing the power of Large Language Models (LLMs) with you. As a machine learning engineer, I'm constantly exploring innovative ways to analyze and visualize data, with a focus on Government Data Analysis, Cloudflare's AI Integration, and making Accessible AI Tools.</h1>",unsafe_allow_html=True)

# res = st.empty()
# asyncio.run(welcoming_prompt(res))
# st.divider()
if st.session_state.first_home==False:
    clicked = ui.button("Show more (My projects here)", key="clk_btn",variant="outline")
    if clicked:
        st.session_state.first_home = True

if st.session_state.first_home==True:
    st.divider()
    project1,project2,project3 = first_show_me()

    if st.session_state.first_proj=="":
        asyncio.run(project_list(project1,project2,project3))

    if st.session_state.second_home==False:
        clicked = ui.button("Show even more (My contact)", key="clk_btn_2",variant="ghost")
        if clicked:
            st.session_state.second_home = True

    if st.session_state.second_home==True:
        st.divider()
        large_cols1,large_cols2,_ = st.columns(3,gap="medium")
        with large_cols1:
            st.markdown("<h2>My Socials</h2>",unsafe_allow_html=True)
        with large_cols2:
            smaller_cols1,smaller_cols2 = st.columns(2)
            with smaller_cols1:
                st.markdown("")
                st.markdown("")
                ui.link_button(text="📫 Email me",url="mailto:bimoilyasa@gmail.com", key="clck_btn",variant="outline")
            with smaller_cols2:
                st.markdown("")
                st.markdown("")
                download_button()
        cols = st.columns(len(SOCIAL_MEDIA))
        for index, (platform, link) in enumerate(SOCIAL_MEDIA.items()):
            cols[index].link_button(platform,link,use_container_width=True)
            
# if __name__ == '__main__':
#     main()