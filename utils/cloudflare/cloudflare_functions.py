import requests
import streamlit as st

def get_list_models():
    url = f"https://api.cloudflare.com/client/v4/accounts/{st.secrets['CLOUDFLARE_ID']}/ai/models/search"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {st.secrets['CLOUDFLARE_KEY']}"
    }

    response = requests.request("GET", url, headers=headers)
    to_json = eval(response.text.replace("true","True"))
    return to_json["result"]

def check_api_token():
    try:
        url = f"https://api.cloudflare.com/client/v4/user/tokens/{st.secrets['CLOUDFLARE_KEY']}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {st.secrets['CLOUDFLARE_KEY']}"
        }

        response = requests.request("GET", url, headers=headers)

        return response.text
    except Exception as e:
        st.error(e)