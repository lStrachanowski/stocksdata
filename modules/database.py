import sys
import os
from sqlalchemy import create_engine, MetaData, Table, Column,String,Numeric,Integer,Time,Date
sys.path.append(os.getcwd()+'\\modules\\')
import credentials 
# zawiera login i hasło do bazy danych 
import csv

engine = create_engine("postgresql://postgres:"+credentials.PASSWORD + "@localhost/" + credentials.DATABASE_NAME,echo = True)
meta = MetaData()

# Towrzy tabele stocks
stocks = Table(
    "stocks", meta,
    Column("TICKER", String, primary_key=True),
    Column("NAME",String),
    Column("ISIN",String)
)

# Tworzy tabelę transactions
day_transactions = Table(
    'day_transactions', meta, 
    Column("TICKER", String),
    Column("DATE", Date, primary_key=True),
    Column("OPEN",Numeric),
    Column("HIGH",Numeric),
    Column("LOW",Numeric),
    Column("CLOSE",Numeric),
    Column("VOLUME",Numeric)
)

# Tworzy tabele z transakcjami w ciągu dnia
details_day_transactions = Table(
    'details_day_transactions', meta, 
    Column("TICKER", String),
    Column("DATE", Date),
    Column("HOUR",Time),
    Column("OPEN",Numeric),
    Column("HIGH",Numeric),
    Column("LOW",Numeric),
    Column("CLOSE",Numeric),
    Column("VOLUME",Numeric)
)

# Inicjuje tabele w bazie danych
# meta.create_all(engine)

# Metoda, która pobiera dane z pliku csv i dodaje je do bazy danych
def load_stock_data():
    with open(os.getcwd()+'\\stock_tickers.csv' ,newline='', mode='r') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=';')
        stocks_data = []
        for row in csv_data:
            stocks_data.append( {"TICKER":row[1], "NAME":row[0],"ISIN":row[2]})
        conn = engine.connect()
        conn.execute(stocks.insert(), stocks_data)
        conn.close()
        

def get_data(value):
    if value == 'stocks':
        selected = stocks.select()
        conn = engine.connect()
        results = conn.execute(selected)
        conn.close()
        return results
    elif value =='day_transactions':
        selected = day_transactions.select()
        conn = engine.connect()
        results = conn.execute(selected)
        conn.close()
        return results
    else:
        selected = details_day_transactions.select()
        conn = engine.connect()
        results = conn.execute(selected)
        conn.close()
        return results


