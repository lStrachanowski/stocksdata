import sys
import os
import requests
import zipfile
import datetime
from sqlalchemy import create_engine, MetaData, Table, Column,String,Numeric,Integer,Time,Date, select,exists, func, and_, text,Float,desc
sys.path.append(os.getcwd()+'\\modules\\')
import credentials 
# zawiera login i hasło do bazy danych 
import csv

engine = create_engine("postgresql://postgres:"+credentials.PASSWORD + "@localhost/" + credentials.DATABASE_NAME)
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
    Column("NAME", String),
    Column("DATE", Date),
    Column("OPEN",Numeric),
    Column("HIGH",Numeric),
    Column("LOW",Numeric),
    Column("CLOSE",Numeric),
    Column("VOLUME",Float )
)

# Tworzy tabele z transakcjami w ciągu dnia
details_day_transactions = Table(
    'details_day_transactions', meta, 
    Column("NAME", String),
    Column("DATE", Date),
    Column("HOUR",Time),
    Column("OPEN",Numeric),
    Column("HIGH",Numeric),
    Column("LOW",Numeric),
    Column("CLOSE",Numeric),
    Column("VOLUME",Numeric )
)

# Inicjuje tabele w bazie danych
# meta.create_all(engine)

# Usuwa / tworzy tabele z bazy danych 
# d-drop
# c-create
def table_operations(table_name, operation):
    if table_name == 'stocks':
        if operation == 'd':
            stocks.drop(engine)
        if operation == 'c':
            stocks.create(engine)
    elif table_name == 'daytransactions':
        if operation == 'd':
            day_transactions.drop(engine)
        if operation == 'c':
            day_transactions.create(engine)
    else:
        if operation == 'd':
            details_day_transactions.drop(engine)
        if operation == 'c':
            details_day_transactions.create(engine)
        
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

# Pobiera z bazy dane o walorze z podanego okresu
def get_data_from_db(from_date,to_date,stock_name):
    selected = day_transactions.select().where(and_(day_transactions.c.DATE >= from_date , day_transactions.c.DATE <= to_date, day_transactions.c.NAME == stock_name.upper())).order_by(day_transactions.c.DATE)
    conn = engine.connect()
    data = conn.execute(selected)
    conn.close()
    return data 

# Sprawdza datę ostatniego wpisu w bazie danych 
def check_last_entry():
    selected = day_transactions.select().where(day_transactions.c.NAME == 'WIG20').order_by(desc(day_transactions.c.DATE)).limit(1)
    conn = engine.connect()
    data = conn.execute(selected)
    conn.close()
    return data

# Pobiera dane z plików i inicjuje je w bazie danych
def load_stocks_details():
    directory = os.getcwd()+'\\data\\'
    for file in os.listdir(directory):
        print(file)
        with open(directory+file,newline='', mode="r" ) as csv_file:
            csv_data = csv.reader(csv_file, delimiter=',')
            stocks_data = []
            itercsv = iter(csv_data)
            next(itercsv)
            for row in itercsv:
                datetime_object = datetime.datetime.strptime(row[1],"%Y%m%d")
                name = row[0]
                stock_open = row[2]
                stock_high = row[3]
                stock_low = row[4]
                stock_close = row[5]
                stock_volume = row[6]
                stocks_data.append({"NAME":name,"DATE":datetime_object, "OPEN": float(stock_open),"HIGH": float(stock_high), "LOW": float(stock_close), "CLOSE": float(stock_low), "VOLUME": float(stock_volume)  })
            conn = engine.connect()
            conn.execute(day_transactions.insert(), stocks_data)
            conn.close()

#Dodaje pozycje o walorze do bazy danych
def add_stock_data(stock):
    stocks_data = []
    datetime_object = datetime.datetime.strptime(stock[1],"%Y%m%d")
    name = stock[0]
    stock_open = stock[2]
    stock_high = stock[3]
    stock_low = stock[4]
    stock_close = stock[5]
    stock_volume = stock[6]
    stocks_data.append({"NAME":name,"DATE":datetime_object, "OPEN": float(stock_open),"HIGH": float(stock_high), "LOW": float(stock_close), "CLOSE": float(stock_low), "VOLUME": float(stock_volume)  })
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
def unzip_file(directory, file_list):
    try:
        for item in file_list:
            print('Unzipping ' + item + ' file.')
            with zipfile.ZipFile(directory + item) as myzip:
                myzip.extractall(directory)
            print(item + ' files unziped.')
            if os.path.isfile(directory + item):
                os.remove(directory + item ) 
    except:
        print("Something went wrong with file unzipping")

# Usuwa pliki ze starymi akcjami 
def delete_old_files():
    directory = os.getcwd()+'\\data\\'
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

# Pobiera aktualne dane
def download_week():
    url = "https://info.bossa.pl/pub/metastock/mstock/sesjaall/few_last.zip"
    path = os.getcwd()+'\\temp\\'
    try:
        r = requests.get(url)
        with open(path + "gpw.zip", "wb" ) as code:
            code.write(r.content)
    except:
        print("Something went wrong with dowloading GPW data.")
        
# Sprawdza czy plik z danym walorem jest w bazie danych
def check_stock(stock):
    conn = engine.connect()
    check = exists(select([stocks]).where(stocks.c.NAME == stock)).select()
    pr = conn.execute(check)
    conn.close()
    return pr.first()[0]

# Aktualizuje bazę danych w zalezności od tego , kiedy miała miejsce ostatnia aktualizacja
def update_db(): 
    today_date = datetime.date.today()
    last_date = list(check_last_entry())[0][1]
    diff = today_date - last_date
    if diff.days < 7:
        download_week()
        unzip_file(os.getcwd()+'\\temp\\',['gpw.zip'])
        file_list = os.listdir(os.getcwd()+'\\temp\\')
        for file in file_list:
            s = file.split(".")[0]
            if s[0] == '2':
                file_time = datetime.datetime.strptime(s, '%Y%m%d' )
                db_last_time = datetime.datetime(last_date.year, last_date.month, last_date.day)
                t_diff = file_time - db_last_time
                if t_diff.days > 0 :
                    print("do dodania " + file)
                    with open(os.getcwd()+'\\temp\\'+file, newline='') as prn_file:
                        reader = csv.reader(prn_file, delimiter=',')
                        for r in reader:
                            if check_stock(r[0]):
                                add_stock_data(r)
        print('Baza aktualna')
    else:
        print('Odświeżanie bazy danych')
        table_operations('daytransactions','d')
        table_operations('daytransactions','c')
        download_data()
        unzip_file(os.getcwd()+'\\data\\',['mstall.zip','mstncn.zip'])
        delete_old_files()
        load_stocks_details()
        print('Baza aktualna')
