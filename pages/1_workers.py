import streamlit as st
import pandas as pd
from kbcstorage.client import Client

st.write("# Workers Entry Form")

with st.sidebar:
    st.page_link("streamlit_app.py", label="Home", icon = "🏠")
    st.page_link("pages/1_workers.py", label="Workers", icon="👷‍♂️")
    st.page_link("pages/2_projects.py", label="Projects", icon = "📂")

