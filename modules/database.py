import sys
import os
from sqlalchemy import create_engine, MetaData, Table, Column,String,Numeric,Integer,Time,Date
sys.path.append(os.getcwd()+'\\modules\\')
import credentials 
# zawiera login i hasło do bazy danych 

engine = create_engine("postgresql://postgres:"+credentials.PASSWORD + "@localhost/" + credentials.DATABASE_NAME,echo = True)
conn = engine.connect()

meta = MetaData()

# Towrzy tabele stocks
stocks = Table(
    "stocks", meta,
    Column("TICKER", String, primary_key=True),
    Column("NAME",String),
    Column("ISIN",String)
)

# Tworzy tabelę transactions
transactions = Table(
    'transactions', meta, 
    Column("TICKER", String),
    Column("DATE", Date, primary_key=True),
    Column("OPEN",Numeric),
    Column("HIGH",Numeric),
    Column("LOW",Numeric),
    Column("CLOSE",Numeric),
    Column("VOLUME",Numeric)
)

# Tworzy tabele z transakcjami w ciągu dnia
day_transactions = Table(
    'day_transactions', meta, 
    Column("TICKER", String),
    Column("DATE", Date),
    Column("HOUR",Time),
    Column("OPEN",Numeric),
    Column("HIGH",Numeric),
    Column("LOW",Numeric),
    Column("CLOSE",Numeric),
    Column("VOLUME",Numeric)
)

def test():
    print("test")


