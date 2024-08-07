import streamlit as st
import pandas as pd
import pyarrow as pa
import datetime as dt
from keboola_streamlit import KeboolaStreamlit
st.write("# Projects Entry Form")
df = st.session_state['project_data']

with st.sidebar:
    st.page_link("streamlit_app.py", label="Home", icon = "🏠")
    st.page_link("pages/1_workers.py", label="Workers", icon="👷‍♂️")
    st.page_link("pages/2_accounts.py", label = "Accounts", icon="💼")
    st.page_link("pages/3_projects.py", label="Projects", icon = "📂")
    st.page_link("pages/4_orders.py", label="Orders", icon="🧾")


# Tabs for data entry and data display
tab1, tab2, tab3 = st.tabs(["📝 Add new or update old records","❌ Delete records", "📊 Data"])