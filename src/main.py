import os
import sys
import pandas as pd
import streamlit as st
from datetime import date
import time

def main():
    
    df = check_data_exists()
    st.session_state.has_run = True


    st.markdown("# job hunt dashboard")

    #placeholder to popluated after the dataframe so its "live"
    empyt_summary = st.empty()
    empyt_in_progress = st.empty()
    #form - must click submit
    with st.form("Done a new application?"):
        df = st.data_editor(
            df,
            num_rows="dynamic",
            column_config = {
                "website" : st.column_config.LinkColumn(),
                "status" :  st.column_config.SelectboxColumn(
                    "Job Applcation Status",
                    options = ["In Progress", "Waiting Responce", "Interview", "Closed",],
                    help = "chose from In Progress, Waiting Responce, Interview, Closed"
                ),
                "AppliedDate" : st.column_config.DateColumn(required=True, default=date.today()),
            })
        submit_button = st.form_submit_button("save jobs?")
    
    if submit_button:
        df = save_data(df)
        success = st.success("data saved")
        time.sleep(1)
        success.empty()

    empyt_summary.markdown(f"Jobs currently listed: {len(df.index)}")
    empyt_in_progress.markdown(f"Number of jobs in progress: {df_basic_stats(df)}")

def df_basic_stats(datafame):
    return (datafame["status"]=="In Progress").sum()

def save_data(df_to_save):
    data_file = "./content/data.parquet"
    df_to_save.to_parquet(data_file, engine="pyarrow")
    return df_to_save


@st.cache_data
def check_data_exists():
    print("checking for saved data in ./content")
    content_dir = "./content"
    if not os.path.exists(content_dir):
        os.mkdir(content_dir)
    
    data_file = os.path.join(content_dir,"data.parquet")

    if not os.path.exists(data_file):
        #new dataframe create df skelaton
        data_struc = {
            "jobName" : ["first"],
            "website" : ["www.google.com"],
            "status" : [None],
            "AppliedDate" : [date.today()],
            "Action" : [""]
        }
        df = pd.DataFrame(data_struc)
        #print(df)
        df.to_parquet(data_file, engine="pyarrow")
        return df
    
    #else read in the file
    df = pd.read_parquet(data_file, engine="pyarrow")
    return df
    


if __name__ == "__main__":
    main()