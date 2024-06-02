import streamlit as st

def Navbar():
    with st.sidebar:
        st.page_link('main.py', label='Home page', icon='🔥')
        st.page_link('pages/skills.py', label='Skills', icon='🛡️')
        st.page_link('pages/terra.py', label='TERRA Impersonator', icon='💯')
        st.page_link('pages/indonesia_data.py', label="Indonesia's Data", icon='🇮🇩')
        # st.page_link('pages/password.py', label="Password Entry", icon='🧭')

def RadioChart():
    with st.sidebar:
        pages = ["Pengangguran", "pendidikan", "Pengangguran2"]
        page = st.sidebar.radio("Go to", pages,index=1)

        if page == "Pengangguran":
            return "pengangguran"
        elif page == "pendidikan":
            return "pendidikan"
        elif page == "Pengangguran2":
            st.write("Lmao, fucking none")