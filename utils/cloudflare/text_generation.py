import requests
import streamlit as st

def text_generation_inputs():
    with st.sidebar:
        check_system_prompt = st.checkbox("System Prompt")

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
                max_chars=1500,
                height=200
                )
        else:
            system_input=""
    
    return system_input


def text_generation(system:str,user:str,payload:dict=None):
    API_BASE_URL = f"https://api.cloudflare.com/client/v4/accounts/{st.secrets['CLOUDFLARE_ID']}/ai/run/"
    headers = {"Authorization": f"Bearer {st.secrets['CLOUDFLARE_KEY']}"}
    inputs = {
        "prompt":[
            {"role": "user", "content": user}
        ]
    }
    testing = {
      "messages": st.session_state[f"{st.session_state.model_picked}"]
    }
    testing.update(payload)
    print(testing)
    try:
        cloudflare_response = requests.post(f"{API_BASE_URL}{st.session_state.model_picked}", headers=headers, json=testing).json()
        print(cloudflare_response)
    except ConnectionRefusedError as err:
        st.write(err)
        raise err

    if cloudflare_response["success"]==True:
        output = cloudflare_response["result"]["response"]
        return output
    else:
        return st.error("Fail to prompt to cloudflare")
    

def text_gen_hyperparameter():
    with st.sidebar:
        if st.checkbox("Hyperparameter"):
            col1, col2,col3 = st.columns(3)
            with col1:
                column1 =  {
                    "frequency_penalty": st.number_input("Frequency penalty",0,2,2,key="frequency_penalty",help="Controls how much to penalize new tokens based on their existing frequency in the text so far. Higher values make the model less likely to repeat the same line of text."),
                    "presence_penalty": st.number_input("Presence penalty",0,2,0,key="presence_penalty",help="Controls how much to penalize new tokens based on whether they appear in the text so far. Higher values make the model more likely to talk about new topics.")
                }
            with col2:
                column2 = {
                "repetition_penalty": st.number_input("Repetition penalty",0,2,1,key="repetition_penalty",help="A parameter to penalize the model for repeating the same tokens in the generated text. Higher values reduce repetition."),
                "temperature": st.number_input("Temperature",0,5,4,key="temperature",help="Controls the randomness of the model's outputs. Lower values make the output more focused and deterministic, while higher values make it more random.")
                }
            with col3:
                column3 = {
                "top_k": st.number_input("Top K",0,50,4,key="top_k",help="Limits the sampling pool to the top k tokens. A higher value of k increases the diversity of the generated text."),
                "top_p": st.number_input("Top P",0,2,1,key="top_p",help="Also known as nucleus sampling. It limits the sampling pool to a subset of the most probable tokens with a cumulative probability of top_p. This helps to ensure the generated text is coherent.")
                }
            default = {
                "max_tokens": st.number_input("Max token",0,9999,256,key="max_tokens",disabled=True),
                "seed": st.number_input("Seed value",0,9999999999,12317066,key="seed",disabled=True)
                # "lora": "string",
                # "prompt": "string",
                # "raw": False,
                # "stream": False,
            }
            hyperparameter = default | column1 | column2 | column3
        else:
            hyperparameter = {}

    return hyperparameter