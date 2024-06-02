import streamlit as st
from utils.navbar import Navbar, RadioChart
from utils.charts.pengangguran import pengangguran_chart
from utils.charts.pendidikan import pendidikan_chart

Navbar()
result = RadioChart()

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
    
st.divider()
st.text("""
Sitasi:
Badan Pusat Statistik Jakarta Pusat , 2024. Statistik Indonesia Tahun 2024. Jakarta
Pusat : Badan Pusat Statistik
""")