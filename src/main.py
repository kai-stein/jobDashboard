import os
import sys
import pandas as pd

def main():
    print("checking for saved data in ./content")
    df = check_data_exists()



def check_data_exists():
    content_dir = "./content"
    if not os.path.exists(content_dir):
        os.mkdir(content_dir)
    
    data_file = os.path.join(content_dir,"data.parquet")

    if not os.path.exists(data_file):
        #new dataframe create df skelaton
        data_struc = {
            "jobName" : [],
            "website" : [],
            "status" : [],
        }
        df = pd.DataFrame(data_struc)
        df.to_parquet(data_file, engine="fastparquet")
        return df
    
    #else read in the file
    df = pd.read_parquet(data_file, engine="fastparquet")
    return df
    


if __name__ == "__main__":
    main()