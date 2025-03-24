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
    port = port,
    dbname= db
)

query = 'SELECT * FROM bitcoin_precos ORDER BY timestamp DESC'

query_2= "SELECT timestamp,(valor - LAG(valor) OVER (ORDER BY timestamp ASC)) / valor *100 AS variacao FROM bitcoin_precos ORDER BY id DESC"

df2= pd.read_sql_query(query_2, conn)

df = pd.read_sql_query(query, conn)

conn.close()

st.set_page_config(page_title="Dashboard de Preços do Bitcoin", layout="wide")

st.title("Dashboard de histórico de preços do bitcoin")

st.subheader("Estatíticas gerais")
col1, col2, col3 = st.columns(3)
col1.metric("Preço Atual",f'${df['valor'].iloc[0]:,.2f}')
col2.metric("Preço Máximo",f'${df["valor"].max():,.2f}')
col3.metric("Preço Mínimo",f'${df["valor"].min():,.2f}')


st.subheader("Dados mais recentes extraídos do banco de dados", divider="gray")

st.dataframe(df)

st.subheader("📈 Evolução do Preço do Bitcoin")
st.line_chart(data=df2, x='timestamp', y='variacao', use_container_width=True)
