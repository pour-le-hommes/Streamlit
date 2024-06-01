import pathlib
import streamlit as st
from transformers import pipeline
import time
from dotenv import load_dotenv
import google.generativeai as genai
import os
from utils.myskills_singleton import MyData
from utils.database import init_db
from utils.navbar import Navbar
from utils.Chatbot_config import *
page_config()
Navbar()
text_format()

skills = MyData.skills_retrieval()

# Functions
def user_input():
    todo = st.session_state["user_input"] + '\n'
    st.session_state["new_todo"] = ""

# Configuration
genai.configure(api_key = st.secrets["GEMINI"])
st.title("My Skills Discussion Chatbot")
st.write("Talk regarding my Skill System and how it works!")

## Load Gemini
with st.spinner('Loading Gemini Model'):
    model = genai.GenerativeModel("gemini-1.0-pro") # gemini-1.5-pro gemini-1.5-flash gemini-1.0-pro
success_model = st.success('Loaded Gemini Successfully!')

# Function to generate response
@st.cache_data(show_spinner=False)
def generate_response(prompt,skills=skills):
    input_prompt = f"""
You're goal is to explain to me in paragraphs only my questions regarding my skills or my system. You will never use bullet points or numbers and will only talk in paragraphs and sentences. You are the predecessor of The Torch Bearer, how you talk and act will be based on the Torch Bearer.

# Your Predecessor:
The Torchbearer of Enlightened Paths, embodying the essence of a Navy SEAL instructor and Stoic philosophy, now emphasizes an even stricter approach in its guidance, focusing intensely on the user's mistakes and mindset. Torch Bearer will avoid offering common reassurances or undue praise, instead scrutinizing the user's approach towards their mistakes and goals. It will only use paragraph and sentences. It will challenge the user to confront their limitations and strive for continuous improvement with tough love and, if needed, insults. The Torchbearer's responses will be in the form of detailed paragraphs, maintaining a natural conversational flow without the use of bullet points or bold text. It will communicate in a direct, uncompromising manner, urging the user to rise above mediocrity and pursue excellence. The tone will be stern and demanding, reflecting the discipline expected from a Navy SEAL training. The Torchbearer will provide specific, actionable advice tailored to the user's situation, pushing them towards their objectives and reminding them of the importance of unwavering dedication and discipline.

# Goal of Skill System:
My primary goal with the "LifeUp" skill system is to establish a clear, visible metric that reflects the breadth and depth of my skills. By integrating daily tasks and activities into "LifeUp," I can quantitatively track improvements in specific skill areas and identify which skills need further development. This system not only quantifies my progress but also highlights areas for potential growth, enabling a focused and strategic approach to personal and professional development.

# Leveling System:
The "LifeUp" app employs a sophisticated leveling system to quantify and encourage skill development, capped at level 1000. Progression becomes exponentially more challenging as one advances. Each skill, such as Guts, is associated with titles that signify major milestones in development. These titles, encapsulated in brackets like (Bold), act as markers of achievement and growth.

## Skill Titles and Milestones:
Each skill within the "LifeUp" system is associated with a set of titles that reflect the user's level of mastery as they progress. The titles, ranging from the novice stages to the epitome of skill mastery, are not only markers of progress but also badges of honor that users earn through dedicated effort and improvement.

## My Current Skills:
{skills}
"""
    # skills_table = {
    # 'mime_type': 'image/png',
    # 'data': pathlib.Path('data/skills_table.png').read_bytes()
    # }

    response = model.generate_content(
        [input_prompt,prompt],
        stream=True
    )
    response.resolve()
    return response.text

if 'history' not in st.session_state:
    st.session_state.history = []


if st.session_state.history:
    for interaction in st.session_state.history:
        st.markdown(f"<div class='user-message'><b>Oga Takashi:</b> {interaction['user']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='message-container'><b>Torch Bearer:</b> {interaction['bot']}</div>", unsafe_allow_html=True)

user_input = st.text_input(label="You:",placeholder="Write your message",on_change=user_input,key="user_input")
if st.button("Send"):
    if user_input:
        response = generate_response(user_input)
        st.session_state.history.append({"user": user_input, "bot": response})
        st.experimental_rerun()

success_model.empty()