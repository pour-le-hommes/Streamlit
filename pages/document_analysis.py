import streamlit as st
from utils.navbar import Navbar
from utils.document_analysis_function import formula_section
from pypdf import PdfReader
import numpy as np
import streamlit_shadcn_ui as ui
import time
from utils.Chatbot_config import text_stream
from docx import Document
import re

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import FreqDist, download
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

download('wordnet')
download('stopwords')
lemmatizer = WordNetLemmatizer()

Navbar()

if "document_added" not in st.session_state:
    st.session_state.document_added = None

if "docs_data" not in st.session_state:
    st.session_state.docs_data = None

if "document_input" not in st.session_state:
    st.session_state.document_input = None

if "common_splits" not in st.session_state:
    st.session_state.common_splits = None

if "vector_embedding" not in st.session_state:
    st.session_state.vector_embedding = None

if "t_f" not in st.session_state:
    st.session_state.t_f = None




if st.session_state.document_added == None:
    st.subheader("Add your documents")
    # document = st.file_uploader("Add your document",type=['pdf'])
    document = "data/CV-BimaIRv3.3.docx"
    if document!=None:
        # st.session_state.docs_data = document.name
        st.session_state.docs_data = "CV-BimaIRv3.3.docx"
        document_strings = ""

        if "pdf"== st.session_state.docs_data[-3::]:
            appended_docs = PdfReader(document)
            for page in appended_docs.pages:
                document_strings = document_strings+page.extract_text()
        elif "doc"== st.session_state.docs_data[-3::] or  "docx"== st.session_state.docs_data[-4::]:
            appended_docs = Document(document)
            doc_list = [page.text.lower() for page in appended_docs.paragraphs]
            document_strings = document_strings+"\n"
            document_strings = document_strings.join(doc_list)

        potential_splits_5_most = FreqDist([i for i in re.findall('[^a-zA-Z]',document_strings) if any(re.findall('[^ ]',i))])
        st.session_state.common_splits = potential_splits_5_most.most_common(5)
        print(potential_splits_5_most.most_common(5))
        # print(pdf_reader.metadata)
        # filtered_values = re.sub('[^a-zA-Z]'," ",document_strings)
        st.session_state.document_added = document_strings

if (st.session_state.document_added != None) and (st.session_state.document_input == None):
    if ui.checkbox(label="Confused? Let me give you suggestions",key="split_suggestion"):
        default_split = st.selectbox("Here's the top non words I found in your document",options=[i[0] for i in st.session_state.common_splits],index=0)
    else:
        default_split = st.text_input("What split do you want?",value="  ")
        if len(default_split)==0:
            st.error("Please insert a split character (\n,' ',etc)")
            if ui.button("Want to know how your text looks?",key="show_docs",variant="destructive"):
                st.write(st.session_state.document_added)
            st.stop()
    
    large_split = [i.strip() for i in st.session_state.document_added.split(default_split) if any(re.findall('[^ ]',i.strip())) and len(i)>0]
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


# tokenized = [word_tokenize(words) for large_splits in st.session_state.document_input for words in sent_tokenize(large_splits)]
# st.write(tokenized)

if st.session_state.document_input != None and st.session_state.vector_embedding == None:
    smaller_split = [splits.lower().split(" ") for splits in st.session_state.document_input]
    first_filter = [[re.sub('[^a-zA-Z]',"",each_word)for each_word in each_split if each_word not in stopwords.words('english')]  for each_split in smaller_split]
    frequency = [FreqDist(lemmatizer.lemmatize(i)) for i in first_filter]
    # for asd in frequency:
    #     print(asd.elements())
    #     print()
    frequency = [{k: v for k, v in sorted(splits.items(), key=lambda item: item[1],reverse=True)} for splits in frequency]
    st.write(frequency)
    st.stop()
    with st.status("Start document analysis", expanded=True) as status:
        st.write("Add document")
        st.write("User input: Large split")
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


if st.session_state.document_input != None:
    # st.header(f"Title: {st.session_state.docs_data}")
    st.header(f"Title: {st.session_state.docs_data.split('.')[0]}")

    st.subheader("Vector Embedding")
    if st.session_state.vector_embedding !=None:
        st.write_stream(text_stream(st.session_state.vector_embedding,delay=0.03))

    st.subheader("Term Frequency")
    if st.session_state.t_f !=None:
        st.write_stream(text_stream(st.session_state.t_f,delay=0.03))


st.header("Formulas")
with st.expander("Check formulas"):
    formula_section()