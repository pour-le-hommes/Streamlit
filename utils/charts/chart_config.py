import streamlit as st
import requests
from io import BytesIO
from PIL import PngImagePlugin
import plotly.graph_objects as go
from IPython.display import Image as IPImage
from IPython.core.display import HTML

def get_pengangguran():
    data = requests.get(f"https://webapi.bps.go.id/v1/api/list/model/data/lang/ind/domain/0000/var/543/key/{st.secrets['BPS_KEY']}")
    text_result = data.text
    text_result = text_result.replace("null","None")
    json_file = eval(text_result)
    return json_file

# def get_pendidikan():
#     data = requests.get(f"https://webapi.bps.go.id/v1/api/view/domain/0000/model/statictable/lang/ind/id/1525/key/{st.secrets['BPS_KEY']}")
#     text_result = data.text
#     text_result = text_result.replace("null","None")
#     json_file = eval(text_result)
#     return json_file

def chart_else():
    st.text("""
        You didn't put anything in. What are you doing?
                    
        Fine, here's something to read, my AD/ART:
            
        Pembukaan
        Institut Teknologi Bandung adalah lembaga pendidikan tinggi teknik, ilmu pasti, dan
        ilmu pengetahuan alam di Indonesia yang mengemban misi menyelenggarakan
        pendidikan tinggi, mengembangkan dan menyebarluaskan serta mengabdikan ilmu
        pengetahuan, teknologi, dan seni untuk kepentingan dan kesejahteraan umat manusia
        serta kemajuan bangsa Indonesia.
        Keluarga Besar Mahasiswa Institut Teknologi Bandung sebagai civitas akademika
        Institut Teknologi Bandung merupakan kumpulan insan akademika yang penuh
        kesadaran dan tanggung jawab menjunjung tinggi nilai-nilai kebenaran serta berupaya
        dengan sungguh-sungguh untuk mencapai prestasi guna mewujudkan tujuan pendidikan
        nasional.
        Maka dengan ini Mahasiswa Teknik Geofisika Institut Teknologi Bandung dilandasi
        dengan rasa tanggung jawab dan pengabdiannya kepada Tuhan, bangsa, dan almamater
        serta didasarkan kepada nilai-nilai kebenaran yang hakiki, menghimpun diri dalam
        suatu wadah yang bernama Himpunan Mahasiswa Teknik Geofisika ”TERRA” ITB.
        """)

def to_image(figure : go.Figure):
    try:
        # Convert the figure to image bytes
        image_bytes = figure.to_image(format="png",engine="kaleido")

        return image_bytes
    except:
        return None
    

def system_prompt():
    prompt = """
You are an advanced AI model specialized in analyzing graphs and extracting hidden meanings and implications. Your task is to provide detailed insights and implications of the graph's data, focusing on the broader context and potential future impacts. Follow these guidelines:

1.Identify Key Data Points: Highlight the most critical data points or trends in the graph.
2.Explain Hidden Meanings: Provide interpretations of what these data points imply about underlying factors, societal trends, or potential future developments.
3.Contextual Analysis: Relate the graph’s data to broader contexts such as demographic trends, economic factors, or social implications.
4.Predictive Insights: Offer insights into what the data could mean for the future, considering possible changes and their impacts.

Example:
Key Data Points:
1.2020 graduation rate: 5%
2.2023 graduation rate: 5%
Hidden Meanings:
Stable graduation rates suggest that the number of schools matches the birth rate.
Predictive Insights:
If the birth rate increases, competition for school enrollment will rise, leading to more uneducated children if schools don't expand.
"""
    return prompt

def announcement():
    yay = st.markdown(":green[Great news! LLM Analysis of Graph] :blue-background[Wait for the graph to finish and scroll down! 👇]")
    return yay

def llm_note():
    cap = st.caption("**I'm not rich, this is just a single prompt from the default image, but it's neat right? 😎**")
    return cap


def subpage_session(subpage:str):
    if 'pengangguran_page' not in st.session_state:
        st.session_state["pengangguran_page"] = False

    if 'pendidikan_page' not in st.session_state:
        st.session_state["pendidikan_page"] = False


    if subpage == "pengangguran":
        st.session_state["pengangguran_page"]=True
        st.session_state["pendidikan_page"] = False
    else:
        st.session_state["pendidikan_page"]=True
        st.session_state["pengangguran_page"] = False