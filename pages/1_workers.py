import streamlit as st
import pandas as pd
import pyarrow as pa
import datetime as dt
from keboola_streamlit import KeboolaStreamlit
st.write("# Workers Entry Form")

with st.sidebar:
    st.page_link("streamlit_app.py", label="Home", icon = "🏠")
    st.page_link("pages/1_workers.py", label="Workers", icon="👷‍♂️")
    st.page_link("pages/2_accounts.py", label = "Accounts", icon="💼")
    st.page_link("pages/3_projects.py", label="Projects", icon = "📂")

# Tabs for data entry and data display
tab1, tab2, tab3 = st.tabs(["📝 Add new or update old records","❌ Delete records", "📊 Data"])
# Data entry form
with tab1:
    with st.form("worker_add_form"):
        st.write("""
                 ## Worker data entry form
                Fill in the form to submit the new record. Historization will happen automaticaly.
                """)
        worker_name = st.text_input("Name:", placeholder="John Doe")
        worker_hire_date = st.date_input("Hire Date:", format="DD/MM/YYYY")
        worker_salary = st.number_input("Salary:", min_value=0)
        worker_fte = st.number_input("FTE:", min_value=0.0, max_value=1.4, step=0.1, format="%0.1f")
        worker_type = st.selectbox("Type:",["Part-Time", "Full-Time", "IČO"])
        worker_email = st.text_input("Email:", placeholder="john.doe@epptec.eu")

        submit_new = st.form_submit_button("New record")
        

        if submit_new:
            emp_records = df[df['worker_email'] == worker_email]
            old_record_index = emp_records[emp_records['is_current'] == 'Y'].index
            if not old_record_index.empty:
                df.loc[old_record_index, 'is_current'] = 'N'
                df.loc[old_record_index, 'effective_end_date'] = pa.scalar(dt.date.today(), type=pa.date32())
            new_record = pd.DataFrame([{
                "worker_name":              worker_name,
                "worker_hire_date":         worker_hire_date,
                "worker_salary":            worker_salary,
                "worker_FTE":               worker_fte,
                "worker_type":              worker_type,
                "worker_email":             worker_email,
                "worker_hr_id":             df.loc[old_record_index, 'worker_hr_id'].values[0] if not old_record_index.empty else None,
                "effective_start_date":     pa.scalar(dt.date.today(), type=pa.date32()),
                "effective_end_date":       pd.Timestamp('2100-12-31').date(),
                "is_current":               'Y'
            }])
            st.session_state['data'] = pd.concat([df, new_record], ignore_index=True)
            st.success("New record has been added", icon="✔")

with tab2:
    if 'df_searched' not in st.session_state:
        st.session_state['df_searched'] = []

    with st.form("worker_delete_form"):
        st.write("""
                 ## Worker data delete form
                 Search for the records you want to delete either by workers name or workers email.
                 """)
        worker_name_del = st.text_input("Name:", placeholder="John Doe")
        worker_email_del = st.text_input("Email:", placeholder="john.doe@epptec.eu")

        st.write("⬇ Look at records you are about to delete.")
        submit_search = st.form_submit_button("Search for records")

        if submit_search:
            if (worker_name_del == '') & (worker_email_del == ''):
                st.warning("You have not selected any records", icon="‼") 
            else:
                df = st.session_state['data']
                if df.loc[df['worker_name'] == worker_name_del, 'worker_hr_id'].empty:
                    st.error("The record you are looking for doesn't exist or doesn't have a unique identified. Please check your input or search directly in the data tab.", icon="💣")
                else:
                    hr_id = df.loc[df['worker_name'] == worker_name_del, 'worker_hr_id'].values[0]
                    df_searched = df[(df['worker_hr_id'] ==  hr_id)]
                    st.session_state['df_searched'] = df_searched
                    st.dataframe(df_searched)

        st.write("⬇ Choose what records to delete.")

        col1, col2, col3 = st.columns([0.3, 0.4, 0.3])
        with col1:
            submit_del_latest = st.form_submit_button("Delete Latest Record")
        with col2:
            submit_del_all = st.form_submit_button("Delete All Records")
        with col3:
            submit_del_condition = st.form_submit_button("Delete On Condition")

        if submit_del_all:
            if (worker_name_del == '') & (worker_email_del == ''):
                st.warning("You have not selected any records", icon="‼")
            else:
                df = st.session_state['data']
                hr_id = df.loc[df['worker_name'] == worker_name_del, 'worker_hr_id'].values[0]
                indexHrId = df[df['worker_hr_id'] == hr_id].index
                df_new = df.drop(indexHrId) # in production add parameter inplace=True
                st.success("All selected records have been deleted.", icon="✔")
                st.dataframe(df_new)
            
        if submit_del_latest:
            if (worker_name_del == '') & (worker_email_del == ''):
                st.warning("You have not selected any records", icon="‼")
            else:
                df = st.session_state['data']
                hr_id = df.loc[df['worker_name'] == worker_name_del, 'worker_hr_id'].values[0]
                latest_active = df[(df['is_current'] == 'Y') & (df['worker_hr_id'] == hr_id)].index
                inactive_df = df[(df['worker_hr_id'] == hr_id) & (df['is_current'] == 'N')].sort_values(by='effective_end_date', ascending=False)
                if not inactive_df.empty:
                    latest_inactive_index = inactive_df.iloc[0].name
                    df_new = df.drop(latest_active) # in production add parameter inplace=True
                    df_new.loc[latest_inactive_index, ['is_current', 'effective_end_date']] = ['Y', pd.Timestamp('2100-12-31').date()]
                    st.success("Latest active record has been deleted. Latest inactive has been set to active.", icon="✔")
                    st.dataframe(df_new)
                else:
                    st.warning("Latest inactive record was not found. Please use 'Delete All' if you want to loose the only record of this worker.", icon="‼")

        
        @st.experimental_dialog("Add conditions", width="large")
        def delete_where():
            st.write("Set at least one condition. Conditions can be combined")
            hireDate = st.date_input("Hire date older than: (DD/MM/YYYY)",format="DD/MM/YYYY", value=pd.Timestamp('2000-12-31').date(), max_value=dt.date.today(), min_value=pd.Timestamp('2000-12-31').date())
            type = st.selectbox(label="Choose type:", options=[None, "Part-time", "Full-time", "IČO"])
            min_salary = st.number_input("Select minimal value for salary:", min_value=0, step=100)
            max_salary = st.number_input("Select maximal value for salary: (if set to 0 this condition is omited)", step=100)
            if st.button("Submit"):
                if min_salary > max_salary:
                    st.error("Maximum Salary should be bigger than minimum slary or 0", icon="💣")
                else:
                    df = st.session_state['df_searched']
                    if not (hireDate == pd.Timestamp('2000-12-31').date()):
                        df[df['worker_hire_date']< pd.to_datetime(hireDate)]

                    if not (type == None):
                        df = df[df['worker_type'] == type]

                    if min_salary:
                        df[df['worker_salary'] >= min_salary]

                    if max_salary > 0:
                        df = df[df['worker_salary'] <= max_salary]
                    st.success("Records have been deleted.", icon="✔")
                    st.write(df)
                                                          

        if submit_del_condition:
            if (worker_name_del == '') & (worker_email_del == ''):
                st.warning("You have not selected any records", icon="‼")
            else:
                delete_where()

with tab3:

    st.write("""
             ## Data
             On this page you can view and edit the date directly in the table bellow.
             """)
    edited_df = st.data_editor(st.session_state['data'], width=2000, use_container_width=False, num_rows="dynamic")
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        if st.button("Save changes"):
            st.session_state['data'] = edited_df
    with col2:
        if st.button("Abort changes"):
            st.write("duh..")
    