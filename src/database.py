from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Float, String, Integer, DateTime 
from datetime import datetime

base = declarative_base()

class BitcoinPreco(base):
    __tablename__ = "bitcoin_precos"

    id = Column(Integer, primary_key= True, autoincrement= True)
    valor = Column(Float, nullable=False)
    criptomoeda = Column(String(50), nullable=False)
    moeda = Column(String(50), nullable=True)
    timestamp = Column(DateTime, default=datetime.now())
