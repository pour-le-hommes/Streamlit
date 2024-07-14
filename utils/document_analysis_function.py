import streamlit as st
from utils.Chatbot_config import text_stream
import asyncio
import streamlit_shadcn_ui as ui
from pypdf import PdfReader
from docx import Document
from nltk import FreqDist, download
import re
import numpy as np

from spacy.pipeline.ner import DEFAULT_NER_MODEL

# config = {
#    "moves": None,
#    "update_with_oracle_cut_size": 100,
#    "model": DEFAULT_NER_MODEL,
#    "incorrect_spans_key": "incorrect_spans",
# }
# nlp.add_pipe("ner", config=config)

def state_creation() -> None:
    if "first_load" not in st.session_state:
        st.session_state.first_load = True

    if "nltk_files" not in st.session_state:
        download('punkt')
        download('averaged_perceptron_tagger')
        download('wordnet')
        download('omw-1.4')
        download('wordnet')
        download('stopwords')
        st.session_state.nltk_files = True

    if "document_added" not in st.session_state:
        st.session_state.document_added = None

    if "docs_data" not in st.session_state:
        st.session_state.docs_data = None

    if "document_input" not in st.session_state:
        st.session_state.document_input = None

    if "confusion_split" not in st.session_state:
        st.session_state.confusion_split = 'visible'

    if "common_splits" not in st.session_state:
        st.session_state.common_splits = None

    if "spacy_ner" not in st.session_state:
        st.session_state.spacy_ner = None

    if "vector_embedding" not in st.session_state:
        st.session_state.vector_embedding = None

    if "t_f" not in st.session_state:
        st.session_state.t_f = None

async def document_formulas(empty_func,func:str) -> None:
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
        full_text = '''\\text{Cosine Similarity}(A,B) = \\frac{A.B}{\|A\|.\|B\|}'''
    
    if st.session_state[f"{func}"]==None:
        empty_func.write_stream(text_stream(full_text,delay=0.01))
        empty_func.latex(fr'''{full_text}''')
    else:
        empty_func.latex(fr'''{full_text}''')

    st.session_state[f"{func}"] = full_text

def formula_section() -> None:
    formula_name,check = st.columns(2,gap="large")
    with formula_name:
        st.subheader("TF-IDF")
    temp = st.empty()
    with check:
        if ui.button(text="Show formula",key="tf_idf",variant="outline"):
            asyncio.run(document_formulas(temp,"TF-IDF"))

    formula_name,check = st.columns(2,gap="large")
    with formula_name:
        st.subheader("Term Frequency (TF)")
    temp = st.empty()
    with check:
        if ui.button("Show formula",key="tf",variant="outline"):
            asyncio.run(document_formulas(temp,"TF"))

    formula_name,check = st.columns(2,gap="large")
    with formula_name:
        st.subheader("Inverse Document Frequency (IDF)")
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


def input_documents(testing:bool = False) -> None:
    st.subheader("Add your documents")
    if testing==True:
        document = "data/CV-BimaIRv3.3.docx"
        st.session_state.docs_data = "CV-BimaIRv3.3.docx"

    else:
        document = st.file_uploader("Add your document",type=['pdf'])
        if document!=None:
            st.session_state.docs_data = document.name
            
    if document!=None:
        document_strings = ""

        if "pdf"== st.session_state.docs_data[-3::]:
            appended_docs = PdfReader(document)
            for page in appended_docs.pages:
                document_strings = document_strings+page.extract_text()
        elif "doc"== st.session_state.docs_data[-3::] or  "docx"== st.session_state.docs_data[-4::]:
            appended_docs = Document(document)
            doc_list = [page.text for page in appended_docs.paragraphs]
            document_strings = document_strings+"\n"
            document_strings = document_strings.join(doc_list)

        potential_splits_5_most = FreqDist([i for i in re.findall('[^a-zA-Z]',document_strings) if any(re.findall('[^ ]',i))])
        st.session_state.common_splits = potential_splits_5_most.most_common(5)
        print(potential_splits_5_most.most_common(5))
        # print(pdf_reader.metadata)
        # filtered_values = re.sub('[^a-zA-Z]'," ",document_strings)
        st.session_state.document_added = document_strings


def preprocessing() -> None:
    default_split = st.text_input("What split do you want?", value="  ",label_visibility=st.session_state.confusion_split)
    if len(default_split)==0:
        st.error("Please insert a split character (\n,' ',etc)")
        if ui.button("Want to know how your text looks?",key="show_docs",variant="destructive"):
            st.write(st.session_state.document_added)
        st.stop()

    if ui.checkbox(label="Confused? Let me give you suggestions",key="split_suggestion"):
        st.session_state.confusion_split = 'hidden'
        st.write("Here are the top stop words I found")
        default_split = st.selectbox("Select and see if you like it",options=[i[0] for i in st.session_state.common_splits],index=0)
    
    large_split = [i.lower().strip() for i in st.session_state.document_added.split(default_split) if any(re.findall('[^ ]',i.strip())) and len(i)>0]
    if len(large_split)>=5:
        if ui.checkbox(label="See snippet?",key="snippet_result"):
            for i in range(5):
                st.write(f"Page {i+1}")
                st.write(large_split[i])
                print(large_split[i])
                st.write(f"-----")
    word_counts = [len(splits.split(" ")) for splits in large_split]
    
    st.subheader("Initial Analysis")
    st.write(f"Total splitted document = {len(large_split)}")
    st.write(f"Average word count: {round((np.mean(word_counts)),2)}")
    st.write(f"Standard deviation count: {round((np.std(word_counts)),2)}")
    
    if ui.button("Start Processing",variant="secondary",key="add_docs"):
        st.session_state.document_input = large_split
        st.rerun()

