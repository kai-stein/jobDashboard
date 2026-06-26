import os
import sys
import pandas as pd
import streamlit as st

def main():
    
    df = check_data_exists()
    st.session_state.has_run = True


    st.markdown("# job hunt dashboard")
    #summary of data
    df_basic_stats(df)
    #
    with st.form("Done a new application?"):
        df_basic_stats(df)
        df = st.data_editor(df,num_rows="dynamic")
        submit_button = st.form_submit_button("save jobs?")
    
    if submit_button:
        df = save_data(df)
        print("data saved")
    
    st.markdown(f"Jobs currently listed: {len(df.index)}")
    #st.button

def df_basic_stats(datafame):
    st.markdown(f"Jobs currently listed: {len(datafame.index)}")
    st.markdown(f"In Progress: {datafame.query('status==True').count()}")

def save_data(df_to_save):
    data_file = "./content/data.parquet"
    df_to_save.to_parquet(data_file, engine="fastparquet")
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
            "website" : ["web"],
            "status" : [False],
        }
        df = pd.DataFrame(data_struc)
        df.to_parquet(data_file, engine="fastparquet")
        return df
    
    #else read in the file
    df = pd.read_parquet(data_file, engine="fastparquet")
    return df
    


if __name__ == "__main__":
    main()