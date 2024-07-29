import streamlit as st
import pandas as pd
from keboola_streamlit import KeboolaStreamlit
from datetime import date
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

if 'df' not in st.session_state:
    st.session_state['df'] = df

# Define data manipuation actions
def add_new_record(df):
    emp_records = df[df['worker_email'] == st.session_state['worker_email']]
    old_record_index = emp_records[emp_records['is_current'] == 'Y'].index
    df.loc[old_record_index, 'is_current'] = 'N'
    df.loc[old_record_index, 'effective_end_date'] = date.today()
    new_record = pd.DataFrame({
        "worker_name" :             st.session_state["worker_name"],
        "worker_hire_date":         st.session_state["worker_hire_date"],
        "worker_salary":            st.session_state["worker_salary"],
        "worker_FTE":               st.session_state["worker_FTE"],
        "worker_type":              st.session_state["worker_type"],
        "worker_email":             st.session_state["worker_email"],
        "worker_hr_id":             df.loc[old_record_index, 'worker_hr_id'],
        "effective_start_date":     date.today(),
        "effective_end_date":       date(2100, 12, 31),
        "is_current":               ['Y']
    })
    df = pd.concat([df,new_record], ignore_index=True)
    st.session_state['df'] = df
    st.session_state["new_record"] = False
    return df

def add_new_record_confirmation():
    st.write("Are you sure you want to add this record?")
    check_record = pd.DataFrame(
        [{
           "worker_name" :      st.session_state["worker_name"],
           "worker_hire_date":  st.session_state["worker_hire_date"],
           "worker_salary":     st.session_state["worker_salary"],
           "worker_FTE":        st.session_state["worker_FTE"],
           "worker_type":       st.session_state["worker_type"],
           "worker_email":      st.session_state["worker_email"]
        }]
    )
    st.dataframe(check_record)

    if "confirmed" not in st.session_state:
        st.session_state["confirmed"] = False

    col1, col2 = st.columns([0.1,0.7])
    if col1.form_submit_button("Submit"):
        st.session_state["confirmed"] = True

    if col2.form_submit_button("Cancel"):
        st.session_state["confirmed"] = False

    if st.session_state["confirmed"]:
        st.session_state['df']= add_new_record(st.session_state['df'])
        st.session_state["confirmed"] = False
        for key in ["worker_name", "worker_hire_date", "worker_salary", "worker_FTE", "worker_type", "worker_email"]:
            st.session_state.pop(key, None)
        st.experimental_rerun()
    

# Define from manipulation actions
def clear_form():
    st.session_state['worker_name'] = ''
    st.session_state['hire_date']= date(2024,1,1)
    st.session_state['salary'] = 0
    st.session_state['fte'] = 0.0
    st.session_state['type'] = ''
    st.session_state['email'] = ''

if 'worker_name' not in st.session_state:
    st.session_state['worker_name']=''

if 'worker_hire_date' not in st.session_state:
    st.session_state['worker_hire_date']=date(2024,1,1)

if 'worker_salary' not in st.session_state:
    st.session_state['worker_salary']=0

if 'worker_fte' not in st.session_state:
    st.session_state['worker_fte']=float('0')

if 'worker_type' not in st.session_state:
    st.session_state['worker_type']=''

if 'worker_email' not in st.session_state:
    st.session_state['worker_email']=''

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
        if "new_record" not in st.session_state:
            st.session_state["new_record"] = False

        if new_record:
            st.session_state["new_record"] = True
            if st.session_state["new_record"]:
                add_new_record_confirmation()

        if clear_input:
            clear_form()


# Display the dataframe
with tab2:
    st.data_editor(st.session_state['df'])