import streamlit as st
from utils.navbar import Navbar
from utils.cloudflare.cloudflare_functions import  check_api_token
from utils.cloudflare.text_generation import text_generation_inputs, text_generation, text_gen_hyperparameter
from utils.Chatbot_config import text_stream
import time

Navbar()

try:
    if st.session_state.model_type_picked != None and st.session_state.model_picked != None:
        model_picked = st.session_state.model_picked
    
    if "submit_text_generation" not in st.session_state:
        st.session_state["submit_text_generation"] = False
except:
    st.title("You're not supposed to be here")
    st.title(":red-background[What the fuck are you doing?]")
    st.stop()

# Text Generation
if st.session_state.model_type_picked=="Text Generation":
    st.header("Text Generation")
    st.subheader(model_picked)
    if f"{st.session_state.model_picked}" not in st.session_state:
        st.session_state[f"{st.session_state.model_picked}"] = []
    st.sidebar.caption("Text Generation Sidebar")
    system_input = text_generation_inputs()
    if system_input!="" and len(st.session_state[f"{st.session_state.model_picked}"])==0:
        st.session_state[f"{st.session_state.model_picked}"].append(
            {"role": "system", "content": system_input}
        )
    hyperparameter = text_gen_hyperparameter()

for message in st.session_state[f"{st.session_state.model_picked}"]:
    if message["role"] == "user":
        with st.chat_message(message["role"],avatar="data/itb.jpg"):
            if type(message["content"]) == str:
                st.markdown(f'<medium>{message["content"]}</medium>',unsafe_allow_html=True)
            else:
                st.plotly_chart(message["content"])
    elif message["role"] == "model":
        with st.chat_message(message["role"],avatar="data/287981.jpg"):
            st.markdown(f'<medium>{message["content"]}</medium>',unsafe_allow_html=True)

if prompt := st.chat_input("Please explain the Indonesian independence on 17 of august 1945",max_chars=100):
    st.session_state[f"{st.session_state.model_picked}"].append({"role": "user", "content": prompt})
    with st.chat_message("user",avatar="data/itb.jpg"):
        st.markdown(prompt)

    with st.chat_message("model",avatar="data/287981.jpg"):
        with st.spinner("What a difficult question... Let me think"):
            stream = text_generation(payload=hyperparameter)

        response = st.write_stream(text_stream(stream,delay=0.03,type="word"))
        st.session_state[f"{st.session_state.model_picked}"].append(
            {"role": "model", "content": response}
        )