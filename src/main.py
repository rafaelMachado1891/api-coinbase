import requests
from datetime import datetime, time
from time import sleep
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from database import base, BitcoinPreco
from logging import basicConfig, getLogger
import logging
import logfire

logfire.configure()
basicConfig(handlers=[logfire.LogfireLoggingHandler()])
logger = getLogger(__name__)
logger.setLevel(logging.INFO)
logfire.instrument_requests()
logfire.instrument_sqlalchemy()

load_dotenv()

user = os.getenv("user")
password = os.getenv("password")
host = os.getenv("host")
port = os.getenv("port")
db = os.getenv("db")

database_url = (
    f"postgresql://{user}:{password}"
    f"@{host}:{port}/{db}"
)

engine = create_engine(database_url)
Session = sessionmaker(bind=engine)

def criar_tabela_no_banco():
   base.metadata.create_all(engine)
   logger.info("Tabela criada com sucesso!")
  

def extract_dados_bitcoin():
    url = "https://api.coinbase.com/v2/prices/spot"
    response = requests.get(url)
    if response.status_code== 200:
        dados = response.json()
        return dados
    else:
        logger.error(f"Erro na api: {response.status_code}")
        return None
        

def transformar_dados_bitcoin(dados):
    valor = float(dados["data"]["amount"])
    criptomoeda = dados["data"]["base"]
    moeda = dados["data"]["currency"]
    timestamp = datetime.now()

    dados_transformados = {
        "valor": valor,
        "criptomoeda": criptomoeda,
        "moeda": moeda,
        "timestamp": timestamp
    }
    return dados_transformados


def carregar_dados_postgres(dados):
   session = Session()
   try:
        novo_registro = BitcoinPreco(**dados)
        session.add(novo_registro)
        session.commit()
        logger.info(f"[{dados['timestamp']}] Dados salvos no Postgres!")
   except Exception as ex:
        logger.error(f"Erro ao inserir dados no PostgreSQL: {ex}")
        session.rollback()
   finally:
        session.close()
        

if __name__ == "__main__":
    criar_tabela_no_banco()
    while True:
        dados_json = extract_dados_bitcoin()
        dados_tratados = transformar_dados_bitcoin(dados_json)
        carregar_dados_postgres(dados_tratados)
        sleep(15)        
