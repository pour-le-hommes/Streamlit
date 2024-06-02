import streamlit as st
import requests

def get_pengangguran():
    data = requests.get(f"https://webapi.bps.go.id/v1/api/list/model/data/lang/ind/domain/0000/var/543/key/{st.secrets['BPS_KEY']}")
    text_result = data.text
    text_result = text_result.replace("null","None")
    json_file = eval(text_result)
    return json_file

def get_pendidikan():
    data = requests.get(f"https://webapi.bps.go.id/v1/api/view/domain/0000/model/statictable/lang/ind/id/1525/key/{st.secrets['BPS_KEY']}")
    text_result = data.text
    text_result = text_result.replace("null","None")
    json_file = eval(text_result)
    return json_file