import streamlit as st
import pandas as pd
from utils.navbar import Navbar
import numpy as np
import time
from utils.chart_config import get_pengangguran
import plotly.graph_objects as go

Navbar()

st.title("Data Pengangguran Indonesia")

if 'pengangguran' not in st.session_state:
    st.session_state["pengangguran"] = get_pengangguran()

json_file = st.session_state["pengangguran"]

data_list = [list(i.values()) for i in json_file["vervar"]]
locations = [i[1].capitalize() for i in data_list]
loc_values = [i[0] for i in data_list]

options = st.multiselect(
    "Select any/multiple Regions:",
    locations,
    ["Indonesia", "Dki jakarta"])

options_picked = [locations.index(loc) for loc in options]
loc_values = [loc_values[loc] for loc in options_picked]

options_multi_array = [[v for k, v in json_file["datacontent"].items() if k.startswith(str(option_val)) and (k.endswith("191") or k.endswith("190"))] for option_val in loc_values]

start_year = 1986
end_year = start_year+len(options_multi_array[0])
year_range = np.arange(start_year,end_year)

fig = go.Figure()
fig.update_layout(
    title="Pengangguran "+", ".join(options)+" Tahun 1986 hingga "+str(end_year),
    xaxis_title="Time",
    yaxis_title="Percentage",
)
for option in range(len(options_multi_array)):
    fig.add_trace(go.Scatter(y=options_multi_array[option][0:1], mode='lines', name=options[option]))

chart = st.plotly_chart(fig, use_container_width=True)


progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()

for i in range(1, len(options_multi_array[0])):
    for idx,_ in enumerate(options):
        fig.data[idx].x = year_range[:i+1]
        fig.data[idx].y = np.append(fig.data[idx].y, options_multi_array[idx][i])
    
    # Update the status text and progress bar
    status_text.text("%i%% Complete" % ((i * 100 // len(options_multi_array[0]) + 1)))
    progress_bar.progress((i * 100 // len(options_multi_array[0])) + 1)

    # Update the chart
    chart.plotly_chart(fig, use_container_width=True)

    time.sleep(0.1)  # Adjust the sleep time as needed

st.button("Re-run")

st.write("""
Sitasi:
Badan Pusat Statistik Jakarta Pusat , 2024. Statistik Indonesia Tahun 2024. Jakarta
Pusat : Badan Pusat Statistik
""")