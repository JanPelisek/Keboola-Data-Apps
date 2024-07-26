import streamlit as st
import pandas as pd
from keboola_streamlit import KeboolaStreamlit
import datetime
# Page Title
st.write("# Data Entry")
st.write("You can enter data on this page")

# Page Navigator
with st.sidebar:
    st.page_link("streamlit_app.py", label="Home", icon = "🏠")
    st.page_link("pages/1_workers.py", label="Workers", icon="👷‍♂️")
    st.page_link("pages/2_projects.py", label="Projects", icon = "📂")

# Establish a connection to keboola storage
kbc = KeboolaStreamlit("https://connection.north-europe.azure.keboola.com/", st.secrets["API_TOKEN"])

# Load data from Keboola storage
if st.session_state.get("data") is None:
    st.session_state["data"] = kbc.read_table('in.c-keboola-ex-google-drive-81159909.Zapis-dat-d_worker')
df = st.session_state["data"]

# Define data manipuation actions
def Add_new_record():
    st.write("Are you sure you want to add this record?")
    new_record = pd.DataFrame(
        [{
           "worker_name" :      st.session_state["worker_name"],
           "worker_hire_date":  st.session_state["worker_hire_date"],
           "worker_salary":     st.session_state["worker_salary"],
           "worker_FTE":        st.session_state["worker_FTE"],
           "worker_type":       st.session_state["worker_type"],
           "worker_email":      st.session_state["worker_email"]
        }]
    )
    st.write(new_record)
    col1, col2 = st.columns([0.1,0.7])
    col1.form_submit_button("Submit")
    col2.form_submit_button("Cancel")

def clear_form():
    st.session_state['name'] = ''
    st.session_state['hire_date']= datetime.date(2024,1,1)
    st.session_state['salary'] = 0
    st.session_state['fte'] = 0.0
    st.session_state['type'] = ''
    st.session_state['email'] = ''

if 'name' not in st.session_state:
    st.session_state['name']=''

if 'hire_date' not in st.session_state:
    st.session_state['hire_date']=datetime.date(2024,1,1)

if 'salary' not in st.session_state:
    st.session_state['salary']=0

if 'fte' not in st.session_state:
    st.session_state['fte']=float('0')

if 'type' not in st.session_state:
    st.session_state['type']=''

if 'email' not in st.session_state:
    st.session_state['email']=''

tab1, tab2 =st.tabs(["📝 Data Entry Form", "📊Data"])


# Data entry form
with tab1:
    with st.form("Worker", clear_on_submit=False):
        st.title("Worker data entry form")
        st.text_input("Name:", placeholder="Doe John", value=st.session_state['name'], key="worker_name")
        st.date_input("Hire Date:",format="DD/MM/YYYY", value=st.session_state['hire_date'], key="worker_hire_date")
        st.number_input("Salary:", min_value=0, value=st.session_state['salary'], key="worker_salary")
        st.number_input("FTE:",min_value=0.0, max_value=1.4,step=0.1, format="%0.1f", value=st.session_state['fte'], key="worker_FTE")
        st.selectbox("Type:", ["IČO", "Full-time", "Part-Time"], key="worker_type")
        st.text_input("Email:", value=st.session_state['email'], key="worker_email")
        col1, col2, col3, col4 = st.columns ([1.6,2.1,3.4,0.9])
        with col1:
            new_record = st.form_submit_button("New record")
        with col2:
            search_record = st.form_submit_button("Search for record")
        with col3:
            update_record = st.form_submit_button("Update record")
        with col4:
            clear_input = st.form_submit_button("Clear")

        # Run data manipulation actions
        if new_record:
            Add_new_record()

if clear_input:
    clear_form()

# Display the dataframe
with tab2:
    st.dataframe(df)