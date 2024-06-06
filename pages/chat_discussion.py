import streamlit as st
from utils.Chatbot_config import generate_response, text_stream
from utils.charts.chart_config import system_prompt
from utils.navbar import Navbar

Navbar()


if st.session_state["first_time"]==True:
    for message in st.session_state.chart_message:
        if message["role"] == "user":
            with st.chat_message(message["role"],avatar="data/itb.jpg"):
                if type(message["parts"]) == str:
                    st.markdown(f'<regular>{message["parts"]}</regular>',unsafe_allow_html=True)
                else:
                    st.plotly_chart(message["parts"])
        else:
            with st.chat_message(message["role"],avatar="data/287981.jpg"):
                st.markdown(f'<regular>{message["parts"]}</regular>',unsafe_allow_html=True)

    if prompt := st.chat_input("What is up?"):
        st.session_state.chart_message.append({"role": "user", "parts": prompt})
        with st.chat_message("user",avatar="data/itb.jpg"):
            st.markdown(f'<regular>{prompt}</regular>',unsafe_allow_html=True)

        with st.chat_message("model",avatar="data/287981.jpg"):
            stream = generate_response(prompt=prompt,context_chat=st.session_state.chart_message,input_prompt=system_prompt(),max_tokens=100)
            response = st.write_stream(text_stream(stream,delay=0.03,type="word"))
            st.session_state.chart_message.append(
                {"role": "model", "parts": response}
            )
            # try:
            #     stream = generate_response(prompt=prompt,context_chat=st.session_state.chart_message,input_prompt=system_prompt())
            #     response = st.write_stream(text_stream(stream,delay=0.03))
            #     st.session_state.chart_message.append(
            #         {"role": "model", "parts": response}
            #     )
            # except:
            #     st.session_state.max_messages = len(st.session_state.chart_message)
            #     rate_limit_message = """
            #         Oops! Sorry, I can't talk now. Too many people have used
            #         this service recently.
            #     """
            #     st.session_state.chart_message.append(
            #         {"role": "model", "parts": rate_limit_message}
            #     )