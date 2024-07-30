import streamlit as st
import pandas as pd
import pyarrow as pa
import datetime
from keboola_streamlit import KeboolaStreamlit

# Page Title
st.write("# Data Entry")
st.write("You can enter data on this page")

# Page Navigator
with st.sidebar:
    st.page_link("streamlit_app.py", label="Home", icon="🏠")
    st.page_link("pages/1_workers.py", label="Workers", icon="👷‍♂️")
    st.page_link("pages/2_projects.py", label="Projects", icon="📂")

# Establish a connection to Keboola storage
kbc = KeboolaStreamlit("https://connection.north-europe.azure.keboola.com/", st.secrets["API_TOKEN"])

# Load data from Keboola storage
if 'data' not in st.session_state:
    st.session_state['data'] = kbc.read_table('in.c-keboola-ex-google-drive-81159909.Zapis-dat-d_worker')

df = st.session_state['data']

# Tabs for data entry and data display
tab1, tab2 = st.tabs(["📝 Data Entry Form", "📊 Data"])
# Data entry form
with tab1:
    with st.form("worker_form"):
        st.title("Worker data entry form")
        worker_name = st.text_input("Name:", placeholder="Doe John", key="worker_name")
        worker_hire_date = st.date_input("Hire Date:", format="DD/MM/YYYY", key="worker_hire_date")
        worker_salary = st.number_input("Salary:", min_value=0, key="worker_salary")
        worker_fte = st.number_input("FTE:", min_value=0.0, max_value=1.4, step=0.1, format="%0.1f", key="worker_FTE")
        worker_type = st.selectbox("Type:",["Part-Time", "Full-Time", "IČO"], key="worker_type")
        worker_email = st.text_input("Email:", key="worker_email")

        col1, col2, col3, col4 = st.columns([1.6, 2.1, 3.4, 0.9])
        submit_new = st.form_submit_button("New record")

        if submit_new:
            emp_records = df[df['worker_email'] == worker_email]
            old_record_index = emp_records[emp_records['is_current'] == 'Y'].index
            if not old_record_index.empty:
                df.loc[old_record_index, 'is_current'] = 'N'
                df.loc[old_record_index, 'effective_end_date'] = pa.scalar(datetime.date.today(), type=pa.date32())
            new_record = pd.DataFrame([{
                "worker_name":              worker_name,
                "worker_hire_date":         worker_hire_date,
                "worker_salary":            worker_salary,
                "worker_FTE":               worker_fte,
                "worker_type":              worker_type,
                "worker_email":             worker_email,
                "worker_hr_id":             df.loc[old_record_index, 'worker_hr_id'].values[0] if not old_record_index.empty else None,
                "effective_start_date":     pa.scalar(datetime.date.today(), type=pa.date32()),
                "effective_end_date":       pd.Timestamp('2100-12-31').date(),
                "is_current":               'Y'
            }])
            st.session_state['data'] = pd.concat([df, new_record], ignore_index=True)


with tab2:
    st.data_editor(st.session_state['data'])