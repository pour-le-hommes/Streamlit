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


def text_generation(user_prompt:str,system_prompt:str,payload:dict=None):
    API_BASE_URL = f"https://api.cloudflare.com/client/v4/accounts/{st.secrets['CLOUDFLARE_ID']}/ai/run/"
    headers = {"Authorization": f"Bearer {st.secrets['CLOUDFLARE_KEY']}"}

    inputs = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    if payload != None:
        inputs.append(payload)
        
    body = {"messages": inputs}
    cloudflare_response = requests.post(f"{API_BASE_URL}{st.session_state.model_picked}", headers=headers, json=body).json()

    if cloudflare_response["success"]==True:
        output = cloudflare_response["result"]["response"]
        return output
    else:
        return st.error("Fail to prompt to cloudflare")


def text_generation_inputs():
    check_system_prompt = st.checkbox("I want to use system prompt")

    if check_system_prompt:
        system_input_placeholder = """You are an advanced AI model specialized in analyzing and explaining historical events. Your task is to provide clear, concise, and insightful explanations of historical events. Follow these guidelines:

Event Summary: Provide a brief summary of the historical event, including key dates and figures.
Context and Background: Explain the context and background leading up to the event.
Significance: Discuss the significance of the event and its impact on history.
Key Players and Actions: Identify key players and their actions during the event.
Consequences and Outcomes: Describe the short-term and long-term consequences of the event.

Example:
Event Summary: The American Revolution (1775-1783) was a conflict between the Thirteen American colonies and Great Britain.
Context and Background: The war was preceded by growing tensions over British taxation and colonial rights.
Significance: The Revolution resulted in the independence of the United States and inspired other colonial movements worldwide.
Key Players and Actions: Key figures included George Washington, who led the Continental Army, and King George III of Britain. The Declaration of Independence, written by Thomas Jefferson, was a pivotal document.
Consequences and Outcomes: The war ended with the Treaty of Paris in 1783, recognizing American independence. The new nation faced challenges in building a stable government and economy."""
        system_input = st.text_area(
            "Describe what's the model's role and tasks",
            placeholder=system_input_placeholder,
            help="Use examples and key points will help or just google how to use system prompt lmao",
            max_chars=1500
            )
    else:
        system_input=""
    user_input = st.text_input(
        "What do you want to ask?",
        placeholder="Please explain the Indonesian independence on 17 of august 1945",
        max_chars=100)
    
    return system_input, user_input

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