import streamlit as st
from utils.navbar import Navbar
from utils.fn_cloudflare import text_generation_inputs, text_generation, check_api_token
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

st.title(model_picked)

# Text Generation
if st.session_state.model_type_picked=="Text Generation":
    system_input,user_input = text_generation_inputs()
    if st.checkbox("Hyperparameter"):
        col1, col2,col3 = st.columns(3)
        with col1:
            column1 =  {
                "frequency_penalty": st.number_input("Frequency penalty",0,2,2,key="frequency_penalty",help="Controls how much to penalize new tokens based on their existing frequency in the text so far. Higher values make the model less likely to repeat the same line of text."),
                "presence_penalty": st.number_input("Presence penalty",0,2,0,key="presence_penalty",help="Controls how much to penalize new tokens based on whether they appear in the text so far. Higher values make the model more likely to talk about new topics.")
            }
        with col2:
            column2 = {
            "repetition_penalty": st.number_input("Repetition penalty",0,2,1,key="repetition_penalty",help="A parameter to penalize the model for repeating the same tokens in the generated text. Higher values reduce repetition."),
            "temperature": st.number_input("Temperature",0,5,4,key="temperature",help="Controls the randomness of the model's outputs. Lower values make the output more focused and deterministic, while higher values make it more random.")
            }
        with col3:
            column3 = {
            "top_k": st.number_input("Top K",0,50,4,key="top_k",help="Limits the sampling pool to the top k tokens. A higher value of k increases the diversity of the generated text."),
            "top_p": st.number_input("Top P",0,2,1,key="top_p",help="Also known as nucleus sampling. It limits the sampling pool to a subset of the most probable tokens with a cumulative probability of top_p. This helps to ensure the generated text is coherent.")
            }
        default = {
            "max_tokens": st.number_input("Max token",0,9999,256,key="max_tokens",disabled=True),
            "seed": st.number_input("Seed value",0,9999999999,12317066,key="seed",disabled=True)
            # "lora": "string",
            # "prompt": "string",
            # "raw": False,
            # "stream": False,
        }
        hyperparameter = default | column1 | column2 | column3
    else:
        hyperparameter = None
    if user_input != None and len(user_input)!=0:
        if st.button("Submit",key="submit_text_generation",type="primary"):
            with st.spinner("Query to Cloud Flare"):
                output = text_generation(user_prompt=user_input,system_prompt=system_input, payload=hyperparameter)

    if st.session_state["submit_text_generation"] == True:
        try:
            st.write_stream(text_stream(output,delay=0.03))
            # st.session_state["submit_text_generation"] = False
        except Exception as e:
            st.error(e)

# for message in st.session_state.chart_message:
#     if message["role"] == "user":
#         with st.chat_message(message["role"],avatar="data/itb.jpg"):
#             if type(message["parts"]) == str:
#                 st.markdown(message["parts"])
#             else:
#                 st.plotly_chart(message["parts"])
#     else:
#         with st.chat_message(message["role"],avatar="data/287981.jpg"):
#             st.markdown(message["parts"])

# if prompt := st.chat_input("What is up?"):
#     st.session_state.chart_message.append({"role": "user", "parts": prompt})
#     with st.chat_message("user",avatar="data/itb.jpg"):
#         st.markdown(prompt)

#     with st.chat_message("model",avatar="data/287981.jpg"):
#         stream = generate_response(prompt=prompt,context_chat=st.session_state.chart_message,input_prompt=system_prompt(),max_tokens=100)
#         response = st.write_stream(text_stream(stream,delay=0.03))
#         st.session_state.chart_message.append(
#             {"role": "model", "parts": response}
#         )