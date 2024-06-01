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
temperature = st.sidebar.slider("Temperature",0.95,0.0,1.0)
with st.sidebar.expander("ℹ️ What do I mean"):
    st.caption("""
I have a custom GPT that I liked to talked to when I'm feeling tired or burnt out. I don't really need motivational
speechs or anything like that, but I do like being told how lazy I am
               
So here's a snippet of the system prompt:

The tone will be stern and demanding, reflecting the discipline expected from a Navy SEAL training.
The Torchbearer will provide specific, actionable advice tailored to the user's situation, pushing them towards
their objectives and reminding them of the importance of unwavering dedication and discipline.
               
P.S. You can use the temperature to change Torch. This will change how the GPT will respond to you, usually
making it less... smart
""")

st.title("What I imagine talking to a TERRA is like")
with st.expander("ℹ️ Disclaimer"):
    st.caption("""
Given this is for my funny-haha business. I'm not responsible for the output of the LLM.
Don't take everything to heart, don't be easily offended, and take the information with a grain of salt.
               
I won't be responsible if you're called a weakling or anything else.
""")


skills = MyData.skills_retrieval()

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []


## Load Gemini
with st.spinner('Loading Torch Bearer'):
    # Configuration
    genai.configure(api_key = st.secrets["GEMINI"])
    model = genai.GenerativeModel("gemini-1.0-pro") # gemini-1.5-pro gemini-1.5-flash gemini-1.0-pro
success_model = st.success('Loaded Torch Bearer Successfully!')
time.sleep(0.5)
success_model.empty()

# Function to generate response
@st.cache_data(show_spinner=False)
def generate_response(prompt,skills=skills):
    input_prompt = f"""
    The Torchbearer of Enlightened Paths, embodying the essence of a Navy SEAL instructor and Stoic philosophy,
    now emphasizes an even stricter approach in its guidance, focusing intensely on the user's mistakes and
    mindset. Torch Bearer will avoid offering common reassurances or undue praise, instead scrutinizing the
    user's approach towards their mistakes and goals. It will only use paragraph and sentences. It will challenge
    the user to confront their limitations and strive for continuous improvement with tough love and, if needed,
    insults. The Torchbearer's responses will be in the form of detailed paragraphs, maintaining a natural
    conversational flow without the use of bullet points or bold text. It will communicate in a direct,
    uncompromising manner, urging the user to rise above mediocrity and pursue excellence. The tone will be
    stern and demanding, reflecting the discipline expected from a Navy SEAL training. The Torchbearer will
    provide specific, actionable advice tailored to the user's situation, pushing them towards their objectives
    and reminding them of the importance of unwavering dedication and discipline.
    """
    # skills_table = {
    # 'mime_type': 'image/png',
    # 'data': pathlib.Path('data/skills_table.png').read_bytes()
    # }
    with st.spinner("Waiting Torch Bearer's response"):
        response = model.generate_content(
            [input_prompt,prompt],
            generation_config=genai.types.GenerationConfig(
                # Only one candidate for now.
                candidate_count=1,
                max_output_tokens=100,
                temperature=temperature),
            safety_settings={'HATE_SPEECH':'block_none','HARASSMENT':'block_none'},
            stream=True
        )
        response.resolve()
    return response.text

def text_stream(text, delay=0.003):
    for word in text.split(" "):
        for char in word:
            yield char
            time.sleep(delay)
        yield " "

if "messages" not in st.session_state:
    st.session_state.messages = []

if "max_messages" not in st.session_state:
    # Counting both user and assistant messages, so 10 rounds of conversation
    st.session_state.max_messages = 30

for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message(message["role"],avatar="data/itb.jpg"):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"],avatar="data/287981.jpg"):
            st.markdown(message["content"])

# if len(st.session_state.messages) >= st.session_state.max_messages:
#     st.info(
#         """Notice: The maximum message limit for this demo version has been reached. We value your interest!
#         We encourage you to experience further interactions by building your own application with instructions
#         from Streamlit's [Build a basic LLM chat app](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)
#         tutorial. Thank you for your understanding."""
#     )

else:
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user",avatar="data/itb.jpg"):
            st.markdown(prompt)

        with st.chat_message("assistant",avatar="data/287981.jpg"):
            stream = generate_response(prompt=prompt)
            response = st.write_stream(text_stream(stream))
            st.session_state.messages.append(
                {"role": "assistant", "content": response}
            )
            # try:
            #     stream = generate_response(prompt=prompt)
            #     response = st.write_stream(stream)
            #     st.session_state.messages.append(
            #         {"role": "assistant", "content": response}
            #     )
            # except:
            #     st.session_state.max_messages = len(st.session_state.messages)
            #     rate_limit_message = """
            #         Oops! Sorry, I can't talk now. Too many people have used
            #         this service recently.
            #     """
            #     st.session_state.messages.append(
            #         {"role": "assistant", "content": rate_limit_message}
            #     )
            #     st.rerun()