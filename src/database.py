from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Float, String, Integer, DateTime 
from datetime import datetime

base = declarative_base()

class BitcoinPreco(base):
    __tablename__ = "bitcoin_preco"

    id = Column(Integer, primary_key= True, Auto_increment = True)
    valor = Column(Float, nullable=False)
    Criptomoeda = Column(String(50), nullable=False)
    timestamp = Column(DateTime, default=datetime.now())
