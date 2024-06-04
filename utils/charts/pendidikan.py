import streamlit as st
import pandas as pd
from utils.charts.chart_config import chart_else, to_image, system_prompt,announcement,llm_note, subpage_session
from utils.Chatbot_config import generate_response, text_stream
import numpy as np
import plotly.graph_objects as go
import time
from IPython.display import Image as IPImage

def pendidikan_chart():

    st.write("Last Updated: 2 June 2024")
    horray = announcement()

    subpage_session("pendidikan")

    if "pendidikan_messages" not in st.session_state:
        st.session_state.pendidikan_messages = []

    if "pendidikan_max_messages" not in st.session_state:
        # Counting both user and assistant messages, so 10 rounds of conversation
        st.session_state.max_messages = 20
    # Configurations
    if 'pendidikan' not in st.session_state:
        raw_df = pd.read_csv("data/Indikator_Pendidikan.csv")
        raw_df.fillna("None",inplace=True)
        raw_df.Kategori = raw_df.Kategori.apply(lambda x:x.title())
        st.session_state["pendidikan"] = raw_df

    if 'indicators' not in st.session_state:
        all_df = st.session_state["pendidikan"]
        st.session_state["indicators"] = all_df["Indikator"]

    if "chat_tab" not in st.session_state:
        st.session_state["chat_tab"] = False

    # Remove "Indikator" column
    df = st.session_state["pendidikan"]
    # table_names = [i.title() for i in st.session_state["indicators"]]
    # if "Indikator" in df.columns:
    #     df.drop(["Indikator"],axis=1,inplace=True)

    category = df.Kategori.unique()
    # Large category selector
    large_selector = st.multiselect(
        "Pick a category:",
        category,
        [category[2]]
    )

    if large_selector:

        large_filtered_df = df[df['Kategori'].isin(large_selector)]

        sub_category = large_filtered_df['Indikator'].unique()

        small_selector = st.multiselect(
            "Pick a sub-category from {}:".format(", ".join(large_selector)),
            sub_category,
            [sub_category[i] for i in [0,3,-1]]
        )

        if small_selector:

            small_filtered_df = large_filtered_df[large_filtered_df['Indikator'].isin(small_selector)]

            df_dropped = small_filtered_df.drop(columns=['Kategori', 'Indikator'])
            df_category_array = df_dropped.values.tolist()

            year_range = [int(i) for i in list(df_dropped.columns)]

            fig = go.Figure()
            title_name = "Kategori "+", ".join(large_selector)+" Tahun "+ str(year_range[0]) +" hingga "+str(year_range[-1])
            fig.update_layout(
                title=title_name,
                xaxis_title="Year",
                yaxis_title="Percentage (%)",
            )
            for each_category in range(len(df_category_array)):
                fig.add_trace(go.Scatter(y=df_category_array[each_category][0:1], mode='lines', name=small_selector[each_category]))

            chart = st.plotly_chart(fig, use_container_width=True)

            progress_bar = st.sidebar.progress(0)
            status_text = st.sidebar.empty()

            for i in range(1, len(year_range)):
                for idx,_ in enumerate(small_selector):
                    fig.data[idx].x = year_range[:i+1]
                    fig.data[idx].y = np.append(fig.data[idx].y, df_category_array[idx][i])
                
                # Update the status text and progress bar
                status_text.text("{}% Complete (from {} to {})".format((i * 100 // len(year_range)+4),year_range[0],(year_range[-1]+1)))
                progress_bar.progress((i * 100 // len(year_range))+4)

                # Update the chart
                chart.plotly_chart(fig, use_container_width=True)

                time.sleep(0.05) # Adjust the sleep time as needed

            with st.spinner("Processing Graph"):
                horray.empty()
                pillow_image = to_image(figure=fig)

            st.header("What's Torch's opinion?")
            if st.button("Want to find out?"):
                user_prompt = f"Please explain this graph for me, the title is {title_name} with the x-axis being\
                years and the y-axis being percentage of people in the population"
                st.session_state.pendidikan_messages.append(
                            {"role": "user", "content": fig}
                        )
                result = generate_response(prompt=user_prompt,_image=pillow_image,max_tokens=1000,input_prompt=system_prompt())
                st.session_state.pendidikan_messages.append(
                            {"role": "assistant", "content": result}
                        )
                st.write_stream(text_stream(result,delay=0.03))
            llm_note()

        else:
            chart_else()

    else:
        chart_else()
