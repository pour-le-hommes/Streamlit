import streamlit as st
from utils.navbar import Navbar
from utils.Chatbot_config import text_stream
from utils.homepage_function import project_list, show_more, download_button, first_show_me, show_more_more, email_button
import asyncio
from streamlit_extras.stylable_container import stylable_container

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
    "GitHub": "https://github.com/pour-le-hommes",
    "Instagram": "https://www.instagram.com/bimoilyasa/",
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
# st.markdown('🔥 **TERRA17066**')
colhead1, colhead2 = st.columns(2,gap="small")
with colhead1:
    st.image("data/34.jpg", width=300)

with colhead2:
    st.markdown("<medium>**Bima Ilyasa Rachmanditya**</medium>", unsafe_allow_html=True)
    st.markdown("<medium>AI Engineer, Data enthusiast</medium>", unsafe_allow_html=True)
    # st.button("📫 Email me",key="email",type="secondary")
    email_button()
    download_button()

st.markdown("<h1>Welcome to my machine learning journey! 🚀 I'm thrilled to share my passion for harnessing the power of Large Language Models (LLMs) with you. As a machine learning engineer, I'm constantly exploring innovative ways to analyze and visualize data, with a focus on Government Data Analysis, Cloudflare's AI Integration, and making Accessible AI Tools.</h1>",unsafe_allow_html=True)
st.write('\n')

# res = st.empty()
# asyncio.run(welcoming_prompt(res))
# st.divider()
if st.session_state.first_home==False:
    show_more()

if st.session_state.first_home==True:
    st.divider()
    project1,project2,project3 = first_show_me()

    if st.session_state.first_proj=="":
        asyncio.run(project_list(project1,project2,project3))

    if st.session_state.second_home==False:
        show_more_more()

    if st.session_state.second_home==True:
        st.divider()
        st.markdown("<h2>My Socials</h2>",unsafe_allow_html=True)
        cols = st.columns(len(SOCIAL_MEDIA))
        for index, (platform, link) in enumerate(SOCIAL_MEDIA.items()):
            with stylable_container(
                key=f"link_button{index}",
                css_styles="""
                    link_button {
                        background-color: 1e1e1e1e;
                        color: #ffffff;
                        border-radius: 50px;
                        transition-duration: 0.4s;
                    }
                    link_button:hover {
                    background-color: blue;
                    color: white;
                    border-style: dotted;
                    border-color: blue;
                    }
                    """,
            ):
                cols[index].link_button(platform,link,use_container_width=True)
# if __name__ == '__main__':
#     main()