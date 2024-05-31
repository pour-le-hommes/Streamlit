import streamlit as st
import pandas as pd
from utils.database import init_db
import time
from utils.myskills_singleton import MyData

singletonInstance = MyData()

def skillspage():
    st.title("My Skills Progression")
    with st.spinner('Loading Skills Level Chart'):
        myskills = singletonInstance.dbskills()
        if myskills !=None:
            df = pd.DataFrame(myskills)
        else:
            db = init_db()
            response = db.table('LifeRPG_Skills').select("name","desc","level","exp","currentLevelExp","untilNextLevelExp").execute()
            singletonInstance.input_localskills(response.data)
            df = pd.DataFrame(response.data)

        df.sort_values("level",ascending=False,inplace=True)
        df.reset_index(inplace=True)
    success = st.success("Loaded Successfully!", icon="✅")

    row1 = st.columns(2)
    row2 = st.columns(3)
    row3 = st.columns(3)
    row4 = st.columns(3)
    full_row = row1 + row2 + row3 + row4

    for i in range(len(df)):
        data = df.iloc[i]
        skill_name = data["name"]
        skill_level = data["level"]
        skill_desc = data["desc"]

        tile = full_row[i].container(height=120)
        tile.metric(label=skill_name, value=f"Level:{skill_level}", help=skill_desc)


    st.bar_chart(df,x="name",y="level", width=100,height=500,color="#c14a09")

    time.sleep(3)
    success.empty()