import streamlit as st
import google.generativeai as genai
import google.ai.generativelanguage as glm
import time

def page_config():
    st.set_page_config(page_title="TERRA", page_icon=None, layout="centered", initial_sidebar_state="collapsed", menu_items=None)

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

def text_stream(text, delay=0.003):
    for word in text.split(" "):
        for char in word:
            yield char
            time.sleep(delay)
        yield " "


@st.cache_data(show_spinner=False)
def generate_response(prompt,temperature_model=1,_image=None,max_tokens = 100,input_prompt = None):
    system_prompt = f"""
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

    full_inputs = [prompt]
    if input_prompt != None:
        full_inputs.append(input_prompt)
    else:
        full_inputs.append(system_prompt)
    
    if _image!=None:
        blob = glm.Blob(
            mime_type='image/jpeg',
            data=_image
        )
        full_inputs.append(blob)
        model_used = load_model(model_name="gemini-1.5-flash")
    else:
        model_used = load_model()


    with st.spinner("Waiting Torch Bearer's response"):
        response = model_used.generate_content(
            contents=full_inputs,

            generation_config=genai.types.GenerationConfig(
                # Only one candidate for now.
                candidate_count=1,
                max_output_tokens=max_tokens,
                temperature=temperature_model),
            safety_settings={'HATE_SPEECH':'block_none','HARASSMENT':'block_none'},
            stream=True
        )
        response.resolve()
    return response.text

@st.cache_data(show_spinner=False)
def load_model(model_name = "gemini-1.0-pro"):
    ## Load Gemini
    with st.spinner('Loading Torch Bearer'):
        # Configuration
        genai.configure(api_key = st.secrets["GEMINI"])
        model = genai.GenerativeModel(model_name) # gemini-1.5-pro gemini-1.5-flash gemini-1.0-pro
    success_model = st.success('Loaded Torch Bearer Successfully!')
    time.sleep(0.5)
    success_model.empty()

    return model