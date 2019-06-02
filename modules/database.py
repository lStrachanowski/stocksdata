import sys
import os
import requests
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

# Tworzy tabelę z podsumowaniem transakcji dnia
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

# Metoda, która pobiera dane walorów z pliku csv i dodaje je do bazy danych
def load_stock_data():
    with open(os.getcwd()+'\\stock_tickers.csv' ,newline='', mode='r') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=';')
        stocks_data = []
        for row in csv_data:
            stocks_data.append( {"TICKER":row[1], "NAME":row[0],"ISIN":row[2]})
        conn = engine.connect()
        conn.execute(stocks.insert(), stocks_data)
        conn.close()


# Pobiera wartości z bazy danych 
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
    elif value =='details_day_transactions':
        selected = details_day_transactions.select()
        conn = engine.connect()
        results = conn.execute(selected)
        conn.close()
        return results

# Pobiera dane end of day ze strony BOŚ
def download_data():
    url = "http://bossa.pl/pub/metastock/mstock/mstall.zip"
    url_newconnect = "http://bossa.pl/pub/newconnect/mstock/mstncn.zip"
    path = os.getcwd()+'\\data\\'
    try:
        print("Downloading GPW data.")
        r = requests.get(url)
        with open(path + 'mstall.zip' , "wb") as code:
            code.write(r.content)
        print("Downloading GPW data ended.")
    except:
        print("Something went wrong with dowloading GPW data.")
    try:
        print("Downloading NewConnect data.")
        r = requests.get(url_newconnect)
        with open(path + 'mstncn.zip' , "wb") as code:
            code.write(r.content)
        print("Downloading NewConnect data ended.")
    except:
        print("Something went wrong with dowloading NewConnect data.")