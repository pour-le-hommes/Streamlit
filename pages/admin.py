import streamlit as st
from utils.navbar import Navbar
# from utils.password import check_password
from utils.admin.todos import check_todos, add_sidebar,update_todos, get_column_config
from utils.password import check_password
import time

Navbar()
check_password()

if "todo_table" not in st.session_state or "todo_column_config" not in st.session_state:
    with st.spinner("Loading to do list"):
        check_todos()
        get_column_config()

with st.sidebar:
    add_sidebar()
        

st.title("My Todos")
st.caption("Things I need to do for my website")

db_table_config = st.session_state["todo_column_config"]
db_table = st.session_state["todo_table"]

if st.checkbox("Unfinished only",value=True):
    db_table = db_table[db_table.finished==False]

website_table = st.data_editor(db_table,column_config=db_table_config,hide_index=True,width=2000,key="website_table")

# Check Difference for Update DB
if not db_table.compare(website_table).empty:
    df_compared = db_table.compare(website_table,result_names=("Before","After"))

    st.write("Changes made:")
    st.table(df_compared)

    # Checking for unchecking boxes
    cols_changed = list(set(column[0] for column in df_compared.columns))
    if "finished" in cols_changed:
        if not all(list(df_compared.finished.After)):
            st.error("You can't change checked tasks, don't make me mad 😠. Uncheck it or refresh if you're lazy")
            st.stop()
    
    #Continue
    # data_changed = [json.dumps(website_table.iloc[i].to_dict()) for i in list(df_compared.index)]
    data_changed = website_table.to_dict(orient='records')

    update_warning = st.warning("Update needed")

    if update_warning:
        if st.button("Update?",key="update_db"):
            update_todos(data_changed)
            update_warning.empty()
            update_success = st.success("Updated successfully")
            time.sleep(1)
            update_success.empty()
            st.cache_data.clear()
            check_todos(force=True)
            st.rerun()