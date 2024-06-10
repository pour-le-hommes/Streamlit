import streamlit as st
from utils.cloudflare.text_generation import text_generation
from utils.Chatbot_config import text_stream
import asyncio
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.row import row
import streamlit_shadcn_ui as ui

def run_async_task(task):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(task)
    loop.close()
    return result

async def welcoming_prompt(result:st.empty):
    if st.session_state.first_home==False:
        res = default_prompt()
        st.write_stream(text_stream(res,delay=0.03,type="word"))
    else:
        with st.status("Preparing welcoming prompt...", expanded=True) as status:
            status.write("Creating system and user prompt...")
            if f"{st.session_state.model_picked}" not in st.session_state:
                st.session_state[f"{st.session_state.model_picked}"] = []
            system_prompt = """You are an advanced AI model specialized in creating unique and engaging welcome messages for a website.
        Your task is to generate a warm, inviting, and informative welcome text with emoticons appropriate for the situation for a machine learning engineer's home page.
        You will explain briefly regarding my current work, which are (Project 1: Government Data Analysis, Project 2: Cloudflare's AI Integration, Project 3: Accessible AI Tools).
        You begin the answer with [START] and ends with [END]. Follow these guidelines:

        [START]
        - Welcome Greeting: Start with a friendly and welcoming greeting.
        - Introduction: Briefly introduce the machine learning engineer and their interests.
        - Current Work: Mention the engineer's work with LLMs and their three projects.
        - Website Purpose: Explain the purpose of the website and its ease of use with Python's data libraries.
        - Call to Action: Encourage visitors to return frequently for updates.
        [END]

        Example:

        [START] 
        - Welcome to my home page!
        - I'm a machine learning engineer who thrives in the world of Hugging Face and Kaggle.
        - Here, you'll see my latest projects involving large language models (LLMs), akin to ChatGPT for those unfamiliar with the jargon.
            1. Charts of government data (Mainly education and unemployment) through their official API and at the bottom I made a connection with Gemini's LLM which I upload the photo of the chart and a system prompt to discuss further if someone wants to
            2. Cloudflare's AI, right now I have connected and made the page for their LLMs, a total of 35 models with their own history and fully customizable hyperparameters from system prompt to top k and top p, all of them.
            3. I'm planning to make all of the cloudflare's free tier AI accessable, meaning their image generation etc, a total of 10 types with just one of them being their text generation LLMs
        - This website leverages the power of Python's data libraries, making it easy to showcase my work.
        - Be sure to visit often, as I'll be updating it regularly. 🤘
        [END]
            """

            user_prompt = "Generate a unique welcome message for my home page using the system's guidelines."

            st.session_state[f"{st.session_state.model_picked}"].append({"role": "system", "content": system_prompt})
            st.session_state[f"{st.session_state.model_picked}"].append({"role": "user", "content": user_prompt})

            status.write("Prompting to cloud flare...")

            
            res = text_generation(payload={})
            if "home page:" in res:
                res = res.split("home page:")[-1]
            if "[START]" in res:
                res = res.split("[START]")[-1]
            if "[END]" in res:
                res = res.split("[END]")[0]
            del st.session_state[f"{st.session_state.model_picked}"]
            res = res.strip()

            status.update(label="Processing Finished", state="complete", expanded=False)

            result.write_stream(text_stream(res,delay=0.03,type="word"))

    # return result.write_stream(text_stream(result,delay=0.03))
    # return result


async def load_welcome():
    res = st.empty()
    res = await welcoming_prompt(res)
    return res

def default_prompt():
    default = """🌟 Welcome to my machine learning journey! 🚀 I'm thrilled to share my passion for harnessing the power of Large Language Models (LLMs) with you. As a machine learning engineer, I'm constantly exploring innovative ways to analyze and visualize data, with a focus on Government Data Analysis, Cloudflare's AI Integration, and making Accessible AI Tools.

Currently, I'm working on three exciting projects. First, I'm diving into Government Data Analysis, utilizing official APIs to create insightful charts and visualizations, such as Gemini's LLM-based photo uploads for further discussion. Next, I'm harnessing Cloudflare's AI might, connecting 35 models with customizable hyperparameters, and making their free tier AI accessible for image generation, text-to-image, and more!

On this website, you'll find a showcase of my projects, facilitated by Python's impressive data libraries. I've designed it to be easy to navigate, so you can quickly explore my work and stay up-to-date on my latest developments. 🙏 Be sure to bookmark this page and return often, as I'll be updating it regularly with new insights, code snippets, and exciting projects! 🚀"""

    return default

async def first_project(proj1):
    full_text = """<h2>🏆 Badan Pusat Statistik Graph with LLM Analysis</h2>

<medium>Dive Deep into Education and Unemployment Data</medium>

<regular>Content:</regular>

<regular>► Charts and graphs with real-time data</regular>

<regular>► Explanation of how the data is collected and processed</regular>

<regular>► Integration with Gemini's LLM for further discussion</regular>
"""
    st.session_state.first_proj = full_text
    proj1.write_stream(text_stream(full_text,delay=0.01,type="word"))
    proj1.markdown(f"{full_text}",unsafe_allow_html=True)

async def second_project(proj2):
    full_text = """<h2>🏆 Harnessing the Power of Cloudflare's AI</h2>

<medium>Explore 35 Customizable LLMs</medium>

<regular>Content:</regular>

<regular>► Overview of the integration</regular>

<regular>► Detailed description of the features (e.g., history, hyperparameters)</regular>

<regular>► How companies can utilize these models</regular>
"""
    st.session_state.second_proj = full_text

    proj2.write_stream(text_stream(full_text,delay=0.01,type="word"))
    proj2.markdown(f"{full_text}",unsafe_allow_html=True)

async def third_project(proj3):
    full_text = """<h2>🏆 Personal Chatbot</h2>

<medium>How is it like to talk to TERRA?</medium>

<regular>Content:</regular>

<regular>► Overview of the integration</regular>

<regular>► Detailed description of the features (e.g., history, hyperparameters)</regular>

<regular>► How companies can utilize these models</regular>
"""
    st.session_state.third_proj = full_text
    proj3.write_stream(text_stream(full_text,delay=0.01,type="word"))
    proj3.markdown(f"{full_text}",unsafe_allow_html=True)


async def project_list(prod1,prod2,prod3):
    await asyncio.gather(
        first_project(prod1),
        second_project(prod2),
        third_project(prod3)
    )


def change_state_2():
    st.session_state.second_home = True

def show_more_more():
    with stylable_container(
        key="show_more",
        css_styles="""
            button {
                font-family: 'inherit';
                background-color: 1e1e1e1e;
                color: #ffffff;
                border-radius: 20px;
                transition-duration: 0.4s;
            }
            button:hover {
            background-color: green;
            color: white;
            }
            """,
    ):
        st.button("Still curious?",on_click=change_state_2,type="secondary")

def show_tips():
    st.write_stream(text_stream("if you have colleague from ITB, ask them lmao.",delay=0.03))
    st.write_stream(text_stream("Or... just google 'Bagi kami, untukmu. _, Bangsa, dan _'",delay=0.03))

def for_the_password():
    clicked = ui.button("For the password", key="clk_btn_3",variant="secondary")
    if clicked:
        st.write("if you have colleague from ITB, ask them lmao.")
        st.write("Or... just google 'Bagi kami, untukmu. _, Bangsa, dan _'")
            

def email_button():
    with st.button("📫 Email me",key="email",type="secondary"):
        st.button("📫 Email me",key="email",type="secondary")

    
def download_button():
    with stylable_container(
        key="cv_download",
        css_styles="""
            button {
                font-family: 'inherit';
                background-color: 1e1e1e1e;
                color: #ffffff;
                border-radius: 50px;
                transition-duration: 0.4s;
            }
            """,
    ):
        with open("data/CV-BimaIRv3.3.pdf", "rb") as pdf_file_handle:
            btn = st.download_button(
            label="📄 Download CV",
            data=pdf_file_handle.read(),
            file_name="data/seevee.pdf",
            mime="application/pdf",
            type="secondary"
          )
            
def first_show_me():

    cols1, cols2 = st.columns(2)

    with cols1:
        if st.session_state.first_proj=="":
            project1 = st.empty()
            st.page_link('pages/indonesia_data.py', label="Indonesia's Data 🇮🇩", icon='➡️')
            project2 = st.empty()
            st.page_link("pages/cloudflare_main_page.py", label="Testing Cloudflare LLMs ☁️", icon='➡️')
            project3 = st.empty()
            st.page_link('pages/terra.py', label='TERRA Impersonator 💯', icon='➡️')

        else:
            project1 = st.markdown(st.session_state.first_proj,unsafe_allow_html=True)
            st.page_link('pages/indonesia_data.py', label="Indonesia's Data 🇮🇩", icon='➡️')
            project2 = st.markdown(st.session_state.second_proj,unsafe_allow_html=True)
            st.page_link("pages/cloudflare_main_page.py", label="Testing Cloudflare LLMs ☁️", icon='➡️')
            project3 = st.markdown(st.session_state.third_proj,unsafe_allow_html=True)
            st.page_link('pages/terra.py', label='TERRA Impersonator 💯', icon='➡️')
        
    with cols2:
        if st.session_state.first_proj=="":
            st.image("data/pengangguran.png",caption="Hover to find the button to full screen")
            st.markdown("<medium></medium>",unsafe_allow_html=True)
            st.markdown("<medium></medium>",unsafe_allow_html=True)
            st.image("data/cloudflare.png",caption="Hover to find the button to full screen")
            st.markdown("<medium></medium>",unsafe_allow_html=True)
            st.markdown("<medium></medium>",unsafe_allow_html=True)
            st.image("data/terra_chatbot.png",caption="Hover to find the button to full screen")
        else:
            st.image("data/pengangguran.png",caption="Hover to find the button to full screen")
            st.markdown("<h2></h2>",unsafe_allow_html=True)
            st.image("data/cloudflare.png",caption="Hover to find the button to full screen")
            st.markdown("<h2></h2>",unsafe_allow_html=True)
            st.image("data/terra_chatbot.png",caption="Hover to find the button to full screen")
        for_the_password()
    return project1, project2, project3