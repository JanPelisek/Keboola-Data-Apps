import streamlit as st
import pandas as pd
# from kbcstorage.client import Client

# Page Title
st.write("# Data Entry")
st.write("You can enter data on this page")

# Page Navigator
with st.sidebar:
    st.page_link("streamlit_app.py", label="Home", icon = "🏠")
    st.page_link("pages/1_workers.py", label="Workers", icon="👷‍♂️")
    st.page_link("pages/2_projects.py", label="Projects", icon = "📂")

# kbcClientToken = st.secrets["kbc_storage_token"]
# kbcUrl = st.secrets["kbc_url"]

# client = Client(kbcUrl, kbcClientToken)

df = pd.read_csv("/data/in/table/Zapis-dat-d_worker")

st.dataframe(df)