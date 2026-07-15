import os
import sys
import pandas as pd
import streamlit as st
import datetime as dt
#from datetime import date
import time

def main():
    
    df = check_data_exists()
    st.session_state.has_run = True


    st.markdown("# job hunt dashboard")

    #Adding columns to hold general stats about the data
    col1, col2, col3 = st.columns(3)

    #form - must click submit
    with st.form("Done a new application?"):
        editedDF = st.data_editor(
            df,
            num_rows="dynamic",
            column_config = {
                "website" : st.column_config.LinkColumn(),
                "status" :  st.column_config.SelectboxColumn(
                    "Job Applcation Status",
                    options = ["In Progress", "Waiting Responce", "Interview", "Closed",],
                    help = "chose from In Progress, Waiting Responce, Interview, Closed"
                ),
                "AppliedDate" : st.column_config.DateColumn(required=True, default=dt.date.today()),
            })
        submit_button = st.form_submit_button("save jobs?")
    
    if submit_button:
        df = save_data(editedDF)
        success = st.success("data saved")
        time.sleep(1)
        success.empty()

    dataStats = df_basic_stats(df)
    col1.metric("Jobs on Board",dataStats["TOT"])
    col2.metric("In Progress", dataStats["INP"])
    col3.metric("Review",dataStats["REV"])


def df_basic_stats(dataframe):
    summary_dict = {}
    summary_dict["TOT"] = len(dataframe.index)
    summary_dict["INP"] = (dataframe["status"]=="In Progress").sum()
    summary_dict["REV"] = (((dt.datetime.now() - dataframe["AppliedDate"]).dt.days) > 3).sum()
    return summary_dict

def save_data(df_to_save):
    print("saving")
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
            "AppliedDate" : [dt.date.today()],
            "Action" : [""]
        }
        df = pd.DataFrame(data_struc)
        #print(df)
        df.to_parquet(data_file, engine="pyarrow")
        df["AppliedDate"] = pd.to_datetime(df["AppliedDate"])
        return df
    
    #else read in the file
    df = pd.read_parquet(data_file, engine="pyarrow")
    df["AppliedDate"] = pd.to_datetime(df["AppliedDate"])
    return df
    


if __name__ == "__main__":
    main()