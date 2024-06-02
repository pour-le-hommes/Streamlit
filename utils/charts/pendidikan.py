import streamlit as st
import pandas as pd
from utils.charts.chart_config import get_pendidikan

def pendidikan_chart():

    st.write("Last Updated: 2 June 2024")

    if 'pendidikan' not in st.session_state:
        st.session_state["pendidikan"] = get_pendidikan()

    json_file = st.session_state["pendidikan"]

    all_types = ["PARTISIPASI PENDIDIKAN FORMAL",
                 "PARTISIPASI PENDIDIKAN FORMAL DAN NONFORMAL",
                 "Pendidikan yang Ditamatkan Penduduk 15 Tahun ke Atas",
                 "Partisipasi Pra Sekolah (sedang)",
                 "Partisipasi Pra Sekolah (pernah + sedang)",
                 "BUTA HURUF"]
    
    all_divisions = [0,12,22,27,30,33,37]

    df = pd.read_csv("data/Indikator_Pendidikan.csv")
    # df.dropna(how="all",inplace=True)
    df.fillna("None",inplace=True)

    value_picked = [df.index[all_divisions[i+1]] for i in [0,3]]
    st.write(value_picked)

    st.write(df.loc[value_picked])

    st.table(df)

    # st.write(json_file)