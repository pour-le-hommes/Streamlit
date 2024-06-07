import streamlit as st
from utils.document_analysis_function import formula_section
from io import StringIO
from pypdf import PdfReader

st.subheader("Add your documents")
document = st.file_uploader("Add your document",type=['pdf'])

if document != None:
    pdf_reader = PdfReader(document)
    for page in pdf_reader.pages:
        print(page.extract_text())
# if document != None:
#     reader = PdfReader("example.pdf")
#     page = reader.pages[0]
#     print(page.extract_text())

st.header("Formulas")
with st.expander("Check formulas"):
    formula_section()



# st.markdown("<h4>TF (Term Frequency)</h4>",unsafe_allow_html=True)
# st.latex(r'''TF(t,d) = 
#          \frac
#             {\text{Number of times term }t\text{ appears in document }d}
#             {\text{Total number of terms in document }d}
#          ''')

# st.markdown("<h4>IDF (Inverse Document Frequency)</h4>",unsafe_allow_html=True)
# st.latex(r'''IDF(t) = 
#          \log\left(
#             \frac
#                 {\text{Total number of documents}}
#                 {1 + \text{Number of documents containing term } t}
#             \right)
#          ''')

# st.subheader("LDA - Latent Dirichlet Allocation")
# st.markdown("<h4>Probability of a word given a topic</h4>",unsafe_allow_html=True)
# st.latex(r'''P(w|z) = 
#          \frac
#             {\beta_w + n_w^{(z)}}
#             {\sum_w'(\beta_w' + n_w'^{(z)})}
#          ''')

# st.markdown("<h4>Probability of a topic given a document</h4>",unsafe_allow_html=True)
# st.latex(r'''P(z|d) = 
#         \frac
#             {\alpha_w + n_w^{(d)}}
#             {\sum_w'(\alpha_z' + n_z'^{(d)})}
#          ''')

# st.subheader("Cosine Similarity")
# st.latex(r'''Cosine\text{ }Similarity(A,B) = \frac{A.B}{\|A\|.\|B\|}''')
