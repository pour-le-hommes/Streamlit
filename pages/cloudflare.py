import streamlit as st
from utils.navbar import Navbar
from utils.fn_cloudflare import get_list_models

Navbar()

st.title("**Cloudflare's LLM Models**")

if "cloudflare_models" not in st.session_state:
    with st.spinner("Getting models"):
        st.session_state['cloudflare_models'] = get_list_models()

if "model_type_picked" not in st.session_state:
    st.session_state.model_type_picked = None

if "model_picked" not in st.session_state:
    st.session_state.model_picked = None

model_list = st.session_state['cloudflare_models']

col1, col2 = st.columns(2)

with col1:
    tasks_available = {i["task"]["name"] for i in model_list}
    model_type_selected = st.selectbox("Step 1: Types of models to use:",tasks_available,index=5,help="What do you want to do with the model?")
    st.session_state.model_type_picked = model_type_selected


    model_type_desc = [i["task"]["description"] for i in model_list if i["task"]["name"]==st.session_state.model_type_picked]
    st.subheader("What does it do?")
    st.write(model_type_desc[0])


with col2:
    model_names = [i["name"] for i in model_list if i["task"]["name"]==model_type_selected]
    model_selected = st.selectbox("Step 2: Model to use:",model_names,help="Which one do you want to use?")
    st.session_state.model_picked = model_selected

    model_desc = [i["description"] for i in model_list if i["name"]==st.session_state.model_picked]
    st.subheader("What does it do?")
    st.write(model_desc[0])

if st.session_state.model_type_picked=="Text Generation":
    st.header(f"Step 3: Play with {model_selected}")
    st.page_link("pages/cloudflare_chat.py",label=f":blue-background[Play with {model_selected}]")
else:
    st.subheader("I haven't made it yet hehe")

