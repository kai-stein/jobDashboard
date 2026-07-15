import pandas as pd
import datetime as dt

data_file = "./content/data.parquet"
df = pd.read_parquet(data_file, engine="pyarrow")

print(df)
print(df.dtypes)

print(dt.date.today())

df["AppliedDate"] = pd.to_datetime(df["AppliedDate"])

print(df)
print(df.dtypes)

print((((dt.datetime.now() - df["AppliedDate"]).dt.days) > 3).sum())

print(dt.datetime.now())