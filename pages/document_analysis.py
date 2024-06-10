import spacy.vectors
import streamlit as st
from utils.navbar import Navbar
from utils.document_analysis_function import formula_section, state_creation, input_documents, preprocessing
import numpy as np
import streamlit_shadcn_ui as ui
import time
from utils.Chatbot_config import text_stream
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import FreqDist
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

import spacy
from spacy import displacy
import spacy.cli

# if "spacy_nlp" not in st.session_state:
#     st.session_state.spacy_nlp = None


try:
    nlp = spacy.load("en_core_web_lg")
    print("Fail")
except:
    spacy.cli.download("en_core_web_lg")
    nlp = spacy.load("en_core_web_lg")

lemmatizer = WordNetLemmatizer()

Navbar()

# Session state creations
state_creation()

if st.session_state.first_load == True:
    st.session_state.first_load = False
    st.rerun()

if st.session_state.document_added == None:
    # Input document function
    ## Available for .pdf, .doc, and .docx
    input_documents()

# text1 = nlp(st.session_state.document_added)
# text1 = nlp("OpenCV is a library in Python that specializes in Computer Vision")
# text2 = nlp("Llama 7B is a Large language model being used as an open sourced alternative to GhatGPT")


# st.markdown(displacy.render(text1, style="ent"),unsafe_allow_html=True)
# st.write("text 1")
# for word in text1.ents:
#     st.write(word.text,word.label_)

# st.write("text 2")
# for word in text2.ents:
#     st.write(word.text,word.label_)

if (st.session_state.document_added != None) and (st.session_state.document_input == None):
    preprocessing()


# tokenized = [word_tokenize(words) for large_splits in st.session_state.document_input for words in sent_tokenize(large_splits)]
# st.write(tokenized)

if st.session_state.document_input != None and st.session_state.vector_embedding == None:
    smaller_split = [splits.lower().split(" ") for splits in st.session_state.document_input]
    first_filter = [[re.sub('[^a-zA-Z]',"",each_word) for each_word in each_split if each_word not in stopwords.words('english')]  for each_split in smaller_split]
    frequency = [FreqDist([lemmatizer.lemmatize(words) for words in batch]) for batch in first_filter]
    # for asd in frequency:
    #     print(asd.elements())
    #     print()
    frequency = [{k: v for k, v in sorted(splits.items(), key=lambda item: item[1],reverse=True)} for splits in frequency]
    st.write(frequency)
    with st.status("Start document analysis", expanded=True) as status:
        st.write("Add document")
        st.write("User input: Large split")
        status.update(label="Named Entity Recognition (NER)",state="running",expanded=True)
        st.write("Named Entity Recognition (NER)")
        spacy_ner = nlp(st.session_state.document_added)
        st.session_state.spacy_ner = spacy_ner
        status.update(label="Vector Embedding",state="running",expanded=True)
        st.write("Vector embedding") ##TODO: Insert vector embedding from cloudflare text embedding https://developers.cloudflare.com/workers-ai/models/#text-embeddings
        st.session_state.vector_embedding = "Hello how are you?"
        st.write("Cosine similarity") ##TODO: Add cosine similarity from nltk after the vector embedding and correlate all documents to ensure the goal/context is still the same
        status.update(label="Cosine Similarity",state="running",expanded=True)
        time.sleep(3)
        st.write("Smaller split")
        ##TODO: Add NER
        status.update(label="Term Frequency",state="running",expanded=True)
        st.write("Term Frequency")

        st.session_state.t_f = "I'm good maybe?"
        status.update(label="Inverse Document Frequency",state="running",expanded=True)
        st.write("Inverse Document Frequency")
        status.update(label="P(W|Z)",state="running",expanded=True)
        st.write("Probability of a word given a topic")
        status.update(label="P(Z|D)",state="running",expanded=True)
        st.write("Probability of a topic given a document")
        status.update(label="Download complete!", state="complete", expanded=True)


if st.session_state.document_input != None and st.session_state.vector_embedding != None:
    # st.header(f"Title: {st.session_state.docs_data}")
    st.header(f"Title: {st.session_state.docs_data.split('.')[0]}")

    st.subheader("Named Entity Recognition (NER)")
    if st.session_state.spacy_ner !=None:
        with st.expander("Result"):
            st.markdown(displacy.render(st.session_state.spacy_ner,style="ent"),unsafe_allow_html=True)
    

    st.subheader("Vector Embedding")
    if st.session_state.vector_embedding !=None:
        with st.expander("Result"):
            st.write_stream(text_stream(st.session_state.vector_embedding,delay=0.03))

    st.subheader("Term Frequency")
    if st.session_state.t_f !=None:
        with st.expander("Result"):
            st.write_stream(text_stream(st.session_state.t_f,delay=0.03))


st.header("Formulas")
with st.expander("Check formulas"):
    formula_section()