# python interpreter path to install modules: C:\Users\steve\AppData\Local\Programs\Python\Python312\python.exe -m pip install sqlalchemy
#run script with py api_test.py

import os
import numpy as np
import pandas as pd
import requests as re
from sqlalchemy import create_engine

def extract() -> dict:
    API_URL = "http://universities.hipolabs.com/search?country=United+States"
    data = re.get(API_URL).json()
    return data

def transform(data: dict) -> pd.DataFrame:
    df = pd.DataFrame(data)
    df = df[df["name"].str.contains("California")]
    df['domains'] = [','.join(map(str, l)) for l in df['domains']]
    df['web_pages'] = [','.join(map(str, l)) for l in df['web_pages']]
    df = df.reset_index(drop=True)
    return df[["domains", "country", "web_pages", "name"]]

def load(df: pd.DataFrame) -> None:
    disk_engine = create_engine('sqlite:///my_lite_store.db')
    df.to_sql('cal_uni', disk_engine, if_exists='replace')

# Get the current directory where this script resides
current_directory = os.path.dirname(os.path.abspath(__file__))

# Change the current directory to this directory
os.chdir(current_directory)


# %%
data = extract()
df = transform(data)
load(df)

# %%
