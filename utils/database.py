from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv(override=True)

import streamlit as st



def init_db():
    supabase : Client = create_client(st.secrets["SUPA_URL"],st.secrets["SUPA_KEY"])
    return supabase