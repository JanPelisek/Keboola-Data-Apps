import streamlit as st
import pandas as pd
from keboola_streamlit import KeboolaStreamlit
# Page Title
st.write("# Data Entry")
st.write("You can enter data on this page")

# Page Navigator
with st.sidebar:
    st.page_link("streamlit_app.py", label="Home", icon = "🏠")
    st.page_link("pages/1_workers.py", label="Workers", icon="👷‍♂️")
    st.page_link("pages/2_projects.py", label="Projects", icon = "📂")

kbc = KeboolaStreamlit("https://connection.north-europe.azure.keboola.com/", st.secrets["API_TOKEN"])

if st.session_state.get("data") is None:
    st.session_state["data"] = kbc.read_table('in.c-keboola-ex-google-drive-81159909/Zapis-dat-d_worker')

st.write(st.session_state["data"])