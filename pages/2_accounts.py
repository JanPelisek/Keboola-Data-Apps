import streamlit as st
import pandas as pd
import pyarrow as pa
import datetime as dt
from keboola_streamlit import KeboolaStreamlit
import streamlit_phone_number
st.write("# Accounts Entry Form")
df = st.session_state['account_data']

with st.sidebar:
    st.page_link("streamlit_app.py", label="Home", icon = "🏠")
    st.page_link("pages/1_workers.py", label="Workers", icon="👷‍♂️")
    st.page_link("pages/2_accounts.py", label = "Accounts", icon="💼")
    st.page_link("pages/3_projects.py", label="Projects", icon = "📂")
    st.page_link("pages/4_orders.py", label="Orders", icon="🧾")


# Tabs for data entry and data display
tab1, tab2, tab3 = st.tabs(["📝 Add new or update old records","❌ Delete records", "📊 Data"])

with tab1:
    with st.form("account_data_entry"):
        st.write("## Account Data Entry Form")
        st.write("Fill in the form and hit submit to add a new account.")
        account_name = st.text_input("Account name:", placeholder="John Doe's rich company")
        account_contact = st.text_input("Account Contact Person Name:", placeholder=" John Doe")
        account_phone = streamlit_phone_number.st_phone_number("Account Phone Number:", default_country="CZ",placeholder="123 456 789")
        account_email = st.text_input("Account Contact Email:",placeholder="account@email.com")
        submit = st.form_submit_button("Submit")

with tab3:

    st.write("""
             ## Data
             On this page you can view and edit the date directly in the table bellow.
             """)
    edited_df = st.data_editor(st.session_state['account_data'], width=2000, use_container_width=False, num_rows="dynamic")
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        if st.button("Save changes"):
            st.session_state['account_data'] = edited_df
    with col2:
        if st.button("Abort changes"):
            st.write("duh.. not yet supported")