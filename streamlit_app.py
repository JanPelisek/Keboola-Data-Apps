import streamlit as st
import pandas as pd
import pyarrow as pa
import datetime as dt
from keboola_streamlit import KeboolaStreamlit

st.set_page_config(layout="wide")

# Page Title
st.write("# Welcome to the dimension tables managment in Keboola App!")
st.write("This Streamlit app will allow you to change dimension tables store in Keboola by comuniacting with Keboola Storage API. Have fun expolring our solution.")

# Page Navigator
with st.sidebar:
    st.page_link("streamlit_app.py", label="Home", icon = "🏠")
    st.page_link("pages/1_workers.py", label="Workers", icon="👷‍♂️")
    st.page_link("pages/2_accounts.py", label = "Accounts", icon="💼")
    st.page_link("pages/3_projects.py", label="Projects", icon = "📂")

with st.spinner("Please wait while we establish connection to Keboola and load the required data."):
    # Establish a connection to Keboola storage
    kbc = KeboolaStreamlit("https://connection.north-europe.azure.keboola.com/", st.secrets["API_TOKEN"])

    # Load data from Keboola storage

    if 'data' not in st.session_state:
        st.session_state['data'] = kbc.read_table('in.c-keboola-ex-google-drive-81159909.Zapis-dat-d_worker')

    df = st.session_state['data']
st.divider()
st.page_link("streamlit_app.py", label="Home", icon="🏠")
st.page_link("pages/1_workers.py", label="Workers", icon="👷‍♂️")
st.page_link("pages/2_accounts.py", label = "Accounts", icon="💼")
st.page_link("pages/3_projects.py", label="Projects", icon = "📂")
st.divider()
st.write("When you are happy with your changes to all the dimenstion tables send them back to Keboola.")
st.button("Send Data to Keboola")

    