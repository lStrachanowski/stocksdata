import sys
import os
import requests
import zipfile
from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table, Column,String,Numeric,Integer,Time,Date, select,exists, func, and_
sys.path.append(os.getcwd()+'\\modules\\')
import credentials 
# zawiera login i hasło do bazy danych 
import csv

engine = create_engine("postgresql://postgres:"+credentials.PASSWORD + "@localhost/" + credentials.DATABASE_NAME)
meta = MetaData()
directory = os.getcwd()+'\\data\\'
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
    Column("DATE", Date),
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
meta.create_all(engine)

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

# Pobiera dane z plików i inicjuje je w bazie danych
def load_stocks_details():
    for file in os.listdir(directory):
        print(file)
        with open(directory+file,newline='', mode="r" ) as csv_file:
            csv_data = csv.reader(csv_file, delimiter=',')
            stocks_data = []
            itercsv = iter(csv_data)
            next(itercsv)
            for row in itercsv:
                datetime_object = datetime.strptime(row[1],"%Y%m%d")
                name = row[0]
                stock_open = row[2]
                stock_high = row[3]
                stock_low = row[4]
                stock_close = row[5]
                stock_volume = row[6]
                stocks_data.append({"TICKER":name,"DATE":datetime_object, "OPEN": float(stock_open),"HIGH": float(stock_high), "LOW": float(stock_close), "CLOSE": float(stock_low), "VOLUME": int(stock_volume)  })
            conn = engine.connect()
            conn.execute(day_transactions.insert(), stocks_data)
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

# Wypakowuje dane z pliku zip I usuwa zbędne pliki      
def unzip_file():
    gpw_file = 'mstall.zip'
    newconnect_file = 'mstncn.zip'
    try:
        print('Unzipping GPW file.')
        with zipfile.ZipFile(directory + gpw_file) as myzip:
            myzip.extractall(directory)
        print('GPW files unziped.')
        if os.path.isfile(directory + gpw_file):
            os.remove(directory + gpw_file) 
        print('Unzipping Newconnect file.')
        with zipfile.ZipFile(directory + newconnect_file) as myzip_newconnect:
            myzip_newconnect.extractall(directory)
        print('Newconnect files unziped.')
        if os.path.isfile(directory + newconnect_file):
            os.remove(directory + newconnect_file) 

        # Usuwa pliki ze starymi akcjami  
        print('Start to delete old files')
        with open('oldstocks.csv', newline='') as file:
            reader = csv.reader(file, delimiter=' ')
            for item in list(reader)[:-1]:
                file_path = directory + item[0]
                if os.path.isfile(file_path):
                    os.remove(file_path)
        print('Old files deleted')
        print('Start to delete old files')
        for file in os.listdir(directory):
            conn = engine.connect()
            check = exists(select([stocks]).where(stocks.c.NAME == file[:-4])).select()
            pr = conn.execute(check)
            conn.close()
            if pr.first()[0] == False:
                if os.path.isfile(directory + file):
                    os.remove(directory + file)
        print('Old files deleted')
    except:
        print("Something went wrong with file unzipping")


