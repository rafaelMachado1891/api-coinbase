import requests
from datetime import datetime, time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from database import base, BitcoinPreco

load_dotenv()

user = os.getenv("user")
password = os.getenv("password")
host = os.getenv("host")
port = os.getenv("port")
db = os.getenv("db")

database_url = (
    f"postgressql://{user}:{password}"
    f"@{host}:{port}:{db}"
)

engine = create_engine(database_url)
session = sessionmaker(bind=engine)

def criar_tabela_no_banco():
   base.metadata.create_all(engine)
   print(f"tabela criada com sucesso!")


def extract_dados_bitcoin():
    url = "https://api.coinbase.com/v2/prices/spot"
    response = requests.get(url)
    dados = response.json()
    return dados


def transformar_dados_bitcoin(dados):
    valor = dados["data"]["amount"]
    criptomoeda = dados["data"]["base"]
    moeda = dados["data"]["currency"]
    timestamp = datetime.now().timestamp()

    dados_transformados = {
        "valor": valor,
        "criptomoeda": criptomoeda,
        "moeda": moeda,
        "timestamp": timestamp
    }
    return dados_transformados


def carregar_dados_postgres(dados):
   session = session()
   novo_registro = BitcoinPreco(**dados)
   session.add(novo_registro)
   session.commit()
   session.close()
   print(f"[{dados["timestamp"]}]Dados salvos no postgres!")


if __name__ == "__main__":

    while True:
        dados_json = extract_dados_bitcoin()
        dados_tratados = transformar_dados_bitcoin(dados_json)
        carregar_dados_postgres(dados_tratados)
        time.sleep(15)        
