from utils.database import init_db
import streamlit as st
import pandas as pd
import datetime as dt

db_todo = init_db()

def get_column_config():
    column_config={
            "tasks": st.column_config.TextColumn("Todo Tasks",disabled=True,help="What's the name of the task?"),
            "complexity": st.column_config.NumberColumn("Complexity",help="How difficult is the task?"),
            "finished": st.column_config.CheckboxColumn(
            "Finished",
            default=False,
            ),
            "finished_at": st.column_config.DateColumn(
                "Time Finished",
                format="D MMM YYYY, h:mm a",
                disabled=True
            )
        }
    if "todo_column_config" not in st.session_state:
        st.session_state["todo_column_config"] = column_config
@st.cache_data
def check_todos(force=False):
    if "todo_table" not in st.session_state:
        todo_query = db_todo.table('website_todos').select("id","tasks","complexity","finished","finished_at").execute()
        df = pd.DataFrame(todo_query.data)
        df.finished_at = df.finished_at.apply(lambda x: dt.datetime.fromisoformat(str(x)) if x=="None" else x)

        st.session_state["todo_table"] = df

    if force==True:
        todo_query = db_todo.table('website_todos').select("id","tasks","complexity","finished","finished_at").execute()
        df = pd.DataFrame(todo_query.data)
        df.finished_at = df.finished_at.apply(lambda x: dt.datetime.fromisoformat(str(x)) if x=="None" else x)

        st.session_state["todo_table"] = df

def add_sidebar():
    with st.expander("Add todo"):
        name = st.text_input("Task name:")
        desc = st.slider("Complexity:",0,100)
        if st.button("Submit",key="submit_todo"):
            if len(name)==0:
                st.warning("No task name added")
            else:
                add_todos(name,desc)
                st.success("Yay")

def add_todos(task_name, task_desc):
    try:
        db_todo.table('website_todos').insert({"tasks":task_name,"complexity":task_desc}).execute()
    except ConnectionError as conn:
        raise conn
    
def update_todos(data_change):
    try:
        db_todo.table('website_todos').upsert(data_change).execute()
    except ConnectionError as conn:
        raise conn