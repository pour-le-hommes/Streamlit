import streamlit as st
import pandas as pd
from utils.navbar import Navbar
import numpy as np
import time
from utils.chart_config import get_pengangguran
import plotly.graph_objects as go

Navbar()

st.title("Data Pengangguran Indonesia from Badan Pusat Statistik (BPS)")
with st.expander("ℹ️ Disclaimer! Please Read"):
    st.caption("The plot from 1986 to the latest year from the BPS API. Citation at the bottom of the page for me to not to get sued by BPS.")


if 'pengangguran' not in st.session_state:
    st.session_state["pengangguran"] = get_pengangguran()

json_file = st.session_state["pengangguran"]

data_list = [list(i.values()) for i in json_file["vervar"]]
locations = [i[1].title() for i in data_list]
sample_text = locations[0:2]
loc_values = [i[0] for i in data_list]

options = st.multiselect(
    "Select any/multiple Regions:",
    locations,
    sample_text)

if options:
    options_picked = [locations.index(loc) for loc in options]
    loc_values = [loc_values[loc] for loc in options_picked]

    options_multi_array = [[v for k, v in json_file["datacontent"].items() if k.startswith(str(option_val)) and (k.endswith("191") or k.endswith("190"))] for option_val in loc_values]
    data_lengths = [len(i) for i in options_multi_array]
    if min(data_lengths) <=0:
        missing_data = options[data_lengths.index(0)]
        st.subheader(missing_data+" is missing it's data. Don't blame me, ask BPS why there isn't any data there.")
        st.stop()

    start_year = 1986
    end_year = start_year+min(data_lengths)
    year_range = np.arange(start_year,end_year)

    fig = go.Figure()
    fig.update_layout(
        title="Pengangguran "+", ".join(options)+" Tahun 1986 hingga "+str(end_year),
        xaxis_title="Year",
        yaxis_title="Percentage (%)",
    )
    for option in range(len(options_multi_array)):
        fig.add_trace(go.Scatter(y=options_multi_array[option][0:1], mode='lines', name=options[option]))

    chart = st.plotly_chart(fig, use_container_width=True)


    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()

    for i in range(1, len(year_range)):
        for idx,_ in enumerate(options):
            fig.data[idx].x = year_range[:i+1]
            fig.data[idx].y = np.append(fig.data[idx].y, options_multi_array[idx][i])
        
        # Update the status text and progress bar
        status_text.text("{}% Complete (from {} to {})".format((i * 100 // len(year_range))+3,start_year,end_year))
        progress_bar.progress((i * 100 // len(year_range))+3)

        # Update the chart
        chart.plotly_chart(fig, use_container_width=True)

        time.sleep(0.1)  # Adjust the sleep time as needed


    st.button("Re-run")
else:
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

st.divider()
st.text("""
Sitasi:
Badan Pusat Statistik Jakarta Pusat , 2024. Statistik Indonesia Tahun 2024. Jakarta
Pusat : Badan Pusat Statistik
""")