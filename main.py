import streamlit as st
from utils.navbar import Navbar

def main():
    Navbar()

    st.title(f'🔥 **TERRA17066**')
    st.logo("data/itb.jpg")
    st.sidebar.markdown("Welcome! My personal information page!")
    st.sidebar.title("Navigation")
    pages = ["Home", "My Skills", "First Portfolio"]
    page = st.sidebar.radio("Go to", pages)


    def home():
        st.write("Welcome to the home page! I'm a machine learning engineer who dwells in hugging face or kaggle. You'll see that I'm working on a lot of LLMs (or ChatGPT-esque for those people who are normal and don't know any jargons)")
        st.write("I'm working on this website because of it's ease with python's data libraries. Be sure to come here often because I'll update this alot 🤘")
        st.info("What do I have in store for you? Scroll down 👇")

        st.header("*Badan Pusat Statistik Graph* with LLM Analysis")
        st.image("data/pendidikan.png")
        st.image("data/pengangguran.png")

        st.header("**Personal Chatbot** (so long as you know the password 😆)")
        st.image("data/terra_chatbot.png")
        with st.expander("For the password"):
            st.markdown(" if you have colleague from ITB, ask them lmao, or just google them")

    if page == "Home":
        home()
    elif page == "First Portfolio":
        st.write("Lmao, fucking none")

    # your content


if __name__ == '__main__':
    main()