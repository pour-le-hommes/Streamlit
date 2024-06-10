import streamlit as st

def Navbar():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    with st.sidebar:
        st.page_link('main.py', label='Home page', icon='🔥')
        st.page_link('pages/skills.py', label='Skills', icon='🛡️')
        st.page_link('pages/terra.py', label='TERRA Impersonator', icon='💯')
        st.page_link('pages/indonesia_data.py', label="Indonesia's Data", icon='🇮🇩')
        st.page_link('pages/document_analysis.py', label="Document Analysis", icon='📄')
        with st.expander("Experimental"):
            st.page_link("pages/cloudflare_main_page.py", label="Testing Cloudflare LLMs", icon='☁️')
        if st.session_state["password_correct"]==True:
            st.page_link('pages/admin.py', label="Admin", icon='🔒')
        if st.button("Clear terminal?"):
            for _ in range(50):
                print("")
        # st.page_link('pages/password.py', label="Password Entry", icon='🧭')

def RadioChart():
    with st.sidebar:
        pages = ["Pengangguran", "pendidikan"]
        page = st.sidebar.radio("Go to", pages,index=1)

        if page == "Pengangguran":
            return "pengangguran"
        elif page == "pendidikan":
            return "pendidikan"