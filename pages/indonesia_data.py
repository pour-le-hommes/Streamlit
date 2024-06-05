import streamlit as st
from utils.navbar import Navbar, RadioChart
from utils.charts.pengangguran import pengangguran_chart
from utils.charts.pendidikan import pendidikan_chart
from utils.Chatbot_config import generate_response, text_stream

Navbar()
result = RadioChart()
if "chart_message" not in st.session_state:
    st.session_state.chart_message=None

st.title(f"Data {result.title()} Indonesia")
st.caption("from Badan Pusat Statistik (BPS)")
with st.expander("ℹ️ Disclaimer! Please Read",expanded=True):
    st.caption("""
The data is from the BPS API. I am directly using the BPS API and given BPS won't take
responsibility if there's misinformation or virus on the website, I too won't take any accountability for any
misinformation in the data or (somehow) there's a virus somewhere along your journey in my website.

Citation at the bottom of the page for me to not to get sued by BPS.
""")

eval(f"{result}_chart()")



if st.session_state["pengangguran_page"]==True:
    st.session_state.chart_message = st.session_state["pengangguran_messages"]
elif st.session_state["pendidikan_page"]==True:
    st.session_state.chart_message = st.session_state["pendidikan_messages"]

if "first_time" not in st.session_state:
    st.session_state["first_time"]=False

if st.session_state.chart_message!=[] and st.session_state.chart_message!=None:
    st.session_state["first_time"]=True
    st.page_link("pages/chat_discussion.py", label='Continue discussion?', icon='🗨️')

else:
    st.divider()
    st.text("""
    Sitasi:
    Badan Pusat Statistik Jakarta Pusat , 2024. Statistik Indonesia Tahun 2024. Jakarta
    Pusat : Badan Pusat Statistik
    """)