import streamlit as st
import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os
import time
from datetime import datetime

load_dotenv()

user= os.getenv("user")
password= os.getenv("password")
host= os.getenv("host")
port= os.getenv("port")
db= os.getenv("db")


conn = psycopg2.connect(
    user = user, 
    password = password,
    host = host,
    db= db
    port = port
)

query = 'SELECT * FROM bitcoin_precos ORDER BY timestamp DESC'

df = pd.read_sql_query(query, conn)

conn.close()

print(df)