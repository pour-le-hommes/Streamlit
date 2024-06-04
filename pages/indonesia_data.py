import streamlit as st
from utils.navbar import Navbar, RadioChart
from utils.charts.pengangguran import pengangguran_chart
from utils.charts.pendidikan import pendidikan_chart
from utils.Chatbot_config import generate_response, text_stream

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



if st.session_state["pengangguran_page"]==True:
    st.session_state.chart_message = st.session_state["pengangguran_messages"]
elif st.session_state["pendidikan_page"]==True:
    st.session_state.chart_message = st.session_state["pendidikan_messages"]

if "first_time" not in st.session_state:
    st.session_state["first_time"]=False

if st.session_state.chart_message!=[]:
    if st.button("Continue to chat?",type="primary"):
        st.session_state["first_time"]=True
    if st.session_state["first_time"]==True:
        for message in st.session_state.chart_message:
            if message["role"] == "user":
                with st.chat_message(message["role"],avatar="data/itb.jpg"):
                    if type(message["content"]) == str:
                        st.markdown(message["content"])
                    else:
                        st.plotly_chart(message["content"])
            else:
                with st.chat_message(message["role"],avatar="data/287981.jpg"):
                    st.markdown(message["content"])

        if prompt := st.chat_input("What is up?"):
            st.session_state.chart_message.append({"role": "user", "content": prompt})
            # with st.chat_message("user",avatar="data/itb.jpg"):
            #     st.markdown(prompt)

            with st.chat_message("assistant",avatar="data/287981.jpg"):
                # stream = generate_response(prompt=prompt)
                # response = st.write_stream(text_stream(stream))
                # st.session_state.chart_message.append(
                #     {"role": "assistant", "content": response}
                # )
                try:
                    stream = generate_response(prompt=prompt)
                    response = st.write_stream(text_stream(stream))
                    st.session_state.chart_message.append(
                        {"role": "assistant", "content": response}
                    )
                except:
                    st.session_state.max_messages = len(st.session_state.chart_message)
                    rate_limit_message = """
                        Oops! Sorry, I can't talk now. Too many people have used
                        this service recently.
                    """
                    st.session_state.chart_message.append(
                        {"role": "assistant", "content": rate_limit_message}
                    )
    else:
        st.divider()
        st.text("""
        Sitasi:
        Badan Pusat Statistik Jakarta Pusat , 2024. Statistik Indonesia Tahun 2024. Jakarta
        Pusat : Badan Pusat Statistik
        """)