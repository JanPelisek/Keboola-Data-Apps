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
    st.session_state["data"] = kbc.read_table('in.c-keboola-ex-google-drive-81159909.Zapis-dat-d_worker')

df = st.session_state["data"]


with st.form("Worker"):
    st.write("Worker data entry form")
    name = st.text_input("Name:")
    hire_date = st.text_input("Hire Date:")
    salary = st.number_input("Salary:")
    FTE = st.number_input("FTE:")
    type = st.selectbox(
        "Type:",
        ["IČO", "Full-time", "Part-Time"]
    )
    email = st.text_input("Email:")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        new_record = st.form_submit_button("New")
    with col2:
        search_record = st.form_submit_button("Search")
    with col3:
        update_record = st.submit_button("Update")
    with col4:
        clear_form = st.submit_button("Clear")

st.dataframe(df)