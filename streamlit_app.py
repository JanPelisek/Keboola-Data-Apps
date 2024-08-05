import streamlit as st
import pandas as pd
import pyarrow as pa
import datetime as dt
from keboola_streamlit import KeboolaStreamlit

st.set_page_config(layout="wide")

# Page Title
st.write("# Welcome to the 'Dimension tables managment in Keboola' App!")
st.write("This Streamlit app will allow you to change dimension tables stored in Keboola by comuniacting with the Keboola Storage API. Have fun expolring our solution.")
st.write("""
         The idea behind this app is allowing users not familiar with the Keboola UI or users who don't need acceess, like backoffice or human resources departments, to make changes directly to the dimension tables.
         The tasks handled here are managing worker records (adding deleting updating using SCD type 3), projects, orders (to connect workers to projects) and accounnts (CRM). 
         This information is then enriched in Keboola with data from other company systems and finance data to create a report for executives.
         """)
# Page Navigator
with st.sidebar:
    st.page_link("streamlit_app.py", label="Home", icon = "🏠")
    st.page_link("pages/1_workers.py", label="Workers", icon="👷‍♂️")
    st.page_link("pages/2_accounts.py", label = "Accounts", icon="💼")
    st.page_link("pages/3_projects.py", label="Projects", icon = "📂")
    st.page_link("pages/4_orders.py", label="Orders", icon="🧾")


with st.spinner("Please wait while we establish connection to Keboola and load the required data."):
    # Establish a connection to Keboola storage
    kbc = KeboolaStreamlit("https://connection.north-europe.azure.keboola.com/", st.secrets["API_TOKEN"])

    # Load data from Keboola storage

    if 'worker_data' not in st.session_state:
        st.session_state['worker_data'] = kbc.read_table('in.c-keboola-ex-google-drive-81159909.Zapis-dat-d_worker')
    
    if 'account_data' not in st.session_state:
        st.session_state['account_data'] = kbc.read_table('in.c-keboola-ex-google-drive-81159909.Zapis-dat-d_client')
    
    if 'project_data' not in st.session_state:
        st.session_state['project_data']= kbc.read_table('in.c-keboola-ex-google-drive-81159909.Zapis-dat-d_client')

    if 'orders_data' not in st.session_state:
        st.session_state['order_data'] = kbc.read_table('in.c-keboola-ex-google-drive-81159909.Zapis-dat-d_order')


st.divider()
st.page_link("streamlit_app.py", label="Home", icon = "🏠")
st.page_link("pages/1_workers.py", label="Workers", icon="👷‍♂️")
st.page_link("pages/2_accounts.py", label = "Accounts", icon="💼")
st.page_link("pages/3_projects.py", label="Projects", icon = "📂")
st.page_link("pages/4_orders.py", label="Orders", icon="🧾")

st.divider()
st.write("When you are happy with your changes to all the dimenstion tables send them back to Keboola.")
send_data = st.button("Send Data to Keboola")

## Add:
## Export updated dat to Keboola
## Order form
## Project form
## Account form
## Worker form - to prod (directly to st.sessionstate not just df)
