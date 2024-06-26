import hmac
import streamlit as st


def check_password():
    """Returns `True` if the user had a correct password."""
    if "wrong_counter" not in st.session_state:
        st.session_state["wrong_counter"] = 0

    if st.session_state["wrong_counter"] >3:
        st.error("Too many wrong answers. Lmao")
        st.stop()

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Untuk Tuhan,", key="username")
            st.text_input("dan", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False
            st.session_state["wrong_counter"] = st.session_state["wrong_counter"]+1

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False


if not check_password():
    st.write("Don't mind if there's an error, I have no fucking clue why.")
    st.stop()