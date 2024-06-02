import streamlit as st
import numpy as np
import time
from utils.charts.chart_config import get_pengangguran, to_image, system_prompt
from utils.Chatbot_config import generate_response, text_stream
import plotly.graph_objects as go

def pengangguran_chart():

    if 'pengangguran' not in st.session_state:
        st.session_state["pengangguran"] = get_pengangguran()

    if "pengangguran_prompt" not in st.session_state:
        st.session_state["pengangguran_prompt"] = "Nothing" 

    json_file = st.session_state["pengangguran"]

    data_list = [list(i.values()) for i in json_file["vervar"]]
    locations = [i[1].title() for i in data_list]
    sample_text = locations[0:1]+locations[11:12]
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

        range_picked = st.sidebar.slider("Time Range:",start_year,end_year,(start_year,end_year))

        year_range = np.arange(*range_picked)

        fig = go.Figure()
        title_name = "Pengangguran "+", ".join(options)+" Tahun "+ str(year_range[0]) +" hingga "+str(year_range[-1])
        fig.update_layout(
            title=title_name,
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
            status_text.text("{}% Complete (from {} to {})".format((i * 100 // len(year_range))+3,year_range[0],(year_range[-1]+1)))
            progress_bar.progress((i * 100 // len(year_range))+3)

            # Update the chart
            chart.plotly_chart(fig, use_container_width=True)

            time.sleep(0.1)  # Adjust the sleep time as needed

        st.button("Re-run")

        pillow_image = to_image(figure=fig)

        st.header("What's Torch's opinion?")
        if st.session_state["pengangguran_prompt"]== "Nothing":
            user_prompt = f"Please explain this graph for me, the title is {title_name} with the x-axis being\
                years and the y-axis being percentage of people in the population"
            result = generate_response(prompt=user_prompt,_image=pillow_image,max_tokens=1000,input_prompt=system_prompt())
            
            st.session_state["pengangguran_prompt"] = result
        
        st.write_stream(text_stream(st.session_state["pengangguran_prompt"]))
        st.caption("I'm not rich, this is just a single prompt, but it's neat right? :D")
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
