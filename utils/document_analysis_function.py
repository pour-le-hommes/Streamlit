import streamlit as st
from utils.Chatbot_config import text_stream
import asyncio
import streamlit_shadcn_ui as ui

async def document_formulas(empty_func,func:str):
    if func not in st.session_state:
        st.session_state[f"{func}"] = None

    if func=="TF-IDF":
        full_text = '''\\text{TF-IDF}(t,d) = TF(t,d) \\times IDF(t)'''

    elif func=="TF":
        full_text = '''TF(t,d) = \\frac{\\text{Number of times term }t\\text{ appears in document }d}{\\text{Total number of terms in document }d}'''
        
    elif func=="IDF":
        full_text = '''IDF(t) = \log\left(\\frac{\\text{Total number of documents}}{1 + \\text{Number of documents containing term } t}\\right)'''
        
    elif func=="PWZ":
        full_text = '''P(w|z) = \\frac{\\beta_w + n_w^{(z)}}{\sum_w'(\\beta_w' + n_w'^{(z)})}'''
        
    elif func=="PZD":
        full_text = '''P(z|d) = \\frac{\\alpha_w + n_w^{(d)}}{\sum_w'(\\alpha_z' + n_z'^{(d)})}'''
        
    elif func=="COSIM":
        full_text = '''Cosine\\text{ }Similarity(A,B) = \\frac{A.B}{\|A\|.\|B\|}'''
    
    if st.session_state[f"{func}"]==None:
        empty_func.write_stream(text_stream(full_text,delay=0.01))
        empty_func.latex(fr'''{full_text}''')
    else:
        empty_func.latex(fr'''{full_text}''')

    st.session_state[f"{func}"] = full_text

def formula_section():
    formula_name,check = st.columns(2,gap="large")
    with formula_name:
        st.subheader("TF-IDF")
    temp = st.empty()
    with check:
        if ui.button(text="Show formula",key="tf_idf",variant="outline"):
            asyncio.run(document_formulas(temp,"TF-IDF"))

    formula_name,check = st.columns(2,gap="large")
    with formula_name:
        st.subheader("TF (Term Frequency)")
    temp = st.empty()
    with check:
        if ui.button("Show formula",key="tf",variant="outline"):
            asyncio.run(document_formulas(temp,"TF"))

    formula_name,check = st.columns(2,gap="large")
    with formula_name:
        st.subheader("IDF (Inverse Document Frequency)")
    temp = st.empty()
    with check:
        if ui.button("Show formula",key="idf",variant="outline"):
            asyncio.run(document_formulas(temp,"IDF"))

    formula_name,check = st.columns(2,gap="large")
    with formula_name:
        st.markdown("<h4>Probability of a word given a topic</h4>",unsafe_allow_html=True)
    temp = st.empty()
    with check:
        if ui.button("Show formula",key="pwz",variant="outline"):
            asyncio.run(document_formulas(temp,"PWZ"))

    formula_name,check = st.columns(2,gap="large")
    with formula_name:
        st.markdown("<h4>Probability of a topic given a document</h4>",unsafe_allow_html=True)
    temp = st.empty()
    with check:
        if ui.button("Show formula",key="pzd",variant="outline"):
            asyncio.run(document_formulas(temp,"PZD"))

    formula_name,check = st.columns(2,gap="large")
    with formula_name:
        st.subheader("Cosine Similarity")
    temp = st.empty()
    with check:
        if ui.button("Show formula",key="cosim",variant="outline"):
            asyncio.run(document_formulas(temp,"COSIM"))